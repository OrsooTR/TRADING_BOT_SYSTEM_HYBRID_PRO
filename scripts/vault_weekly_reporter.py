from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import os
import sqlite3
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, time as dtime, timedelta
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VAULT_ROOT = PROJECT_ROOT / "Pipeline_01"
REPORTS_DIR = VAULT_ROOT / "09_LOGS" / "WEEKLY_REPORTS"
ARTIFACT_DIR = PROJECT_ROOT / "artifacts" / "vault_reporting"
DB_PATH = ARTIFACT_DIR / "vault_memory.sqlite"
STATE_PATH = ARTIFACT_DIR / "reporter_state.json"
LOG_PATH = ARTIFACT_DIR / "vault_weekly_reporter.log"

POLL_SECONDS = 60
WEEKLY_REPORT_DAY = 6  # Sunday
WEEKLY_REPORT_TIME = dtime(23, 30)

IGNORED_DIRS = {
    ".git",
    ".obsidian",
    ".claude",
    "__pycache__",
    "node_modules",
    ".pytest_cache",
}
IGNORED_SUFFIXES = {
    ".pyc",
    ".pkl",
    ".sqlite",
    ".db",
    ".log",
    ".tmp",
    ".bak",
}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".csv", ".py", ".pine", ".ps1", ".bat"}


@dataclass(frozen=True)
class FileStat:
    rel_path: str
    size: int
    mtime: float
    sha256: str


def local_now() -> datetime:
    # Tutto il reporter usa il tempo LOCALE naive: gli eventi devono cadere nella
    # stessa settimana calcolata da week_bounds() e dal trigger della domenica sera,
    # che ragionano in ora locale. (Prima gli eventi erano in UTC naive → mismatch
    # ai confini di settimana.)
    return datetime.now().replace(microsecond=0)


def log(message: str) -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = local_now().isoformat(sep=" ")
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(f"[{stamp}] {message}\n")


def connect() -> sqlite3.Connection:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS files (
            rel_path TEXT PRIMARY KEY,
            size INTEGER NOT NULL,
            mtime REAL NOT NULL,
            sha256 TEXT NOT NULL,
            first_seen TEXT NOT NULL,
            last_seen TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_time TEXT NOT NULL,
            event_type TEXT NOT NULL,
            rel_path TEXT NOT NULL,
            old_sha256 TEXT,
            new_sha256 TEXT,
            old_size INTEGER,
            new_size INTEGER,
            summary TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS reports (
            week_start TEXT PRIMARY KEY,
            week_end TEXT NOT NULL,
            generated_at TEXT NOT NULL,
            markdown_path TEXT NOT NULL,
            pdf_path TEXT NOT NULL,
            event_count INTEGER NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def should_track(path: Path) -> bool:
    parts = set(path.parts)
    if parts & IGNORED_DIRS:
        return False
    if path.suffix.lower() in IGNORED_SUFFIXES:
        return False
    if path.name.startswith("~$"):
        return False
    return path.is_file()


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def scan_files() -> dict[str, FileStat]:
    result: dict[str, FileStat] = {}
    roots = [VAULT_ROOT, PROJECT_ROOT / "src", PROJECT_ROOT / "scripts", PROJECT_ROOT / "tradingview"]
    artifacts_reports = PROJECT_ROOT / "artifacts"
    if artifacts_reports.exists():
        roots.append(artifacts_reports)

    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not should_track(path):
                continue
            try:
                stat = path.stat()
                rel = path.relative_to(PROJECT_ROOT).as_posix()
                result[rel] = FileStat(rel, stat.st_size, stat.st_mtime, file_hash(path))
            except OSError as exc:
                log(f"skip unreadable file {path}: {exc}")
    return result


def summarize_file(path: Path) -> str:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return ""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""
    if path.suffix.lower() == ".md":
        headings = [line.lstrip("# ").strip() for line in lines if line.startswith("#")]
        return "; ".join(headings[:4])[:500]
    return " ".join(lines[:5])[:500]


def record_scan(conn: sqlite3.Connection) -> int:
    now = local_now().isoformat()
    current = scan_files()
    known_rows = conn.execute("SELECT * FROM files").fetchall()
    known = {row["rel_path"]: row for row in known_rows}
    event_count = 0

    for rel_path, stat in current.items():
        row = known.get(rel_path)
        abs_path = PROJECT_ROOT / rel_path
        summary = summarize_file(abs_path)
        if row is None:
            conn.execute(
                """
                INSERT INTO files(rel_path, size, mtime, sha256, first_seen, last_seen)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (rel_path, stat.size, stat.mtime, stat.sha256, now, now),
            )
            conn.execute(
                """
                INSERT INTO events(event_time, event_type, rel_path, new_sha256, new_size, summary)
                VALUES (?, 'created', ?, ?, ?, ?)
                """,
                (now, rel_path, stat.sha256, stat.size, summary),
            )
            event_count += 1
        elif row["sha256"] != stat.sha256 or int(row["size"]) != stat.size:
            conn.execute(
                """
                UPDATE files SET size = ?, mtime = ?, sha256 = ?, last_seen = ?
                WHERE rel_path = ?
                """,
                (stat.size, stat.mtime, stat.sha256, now, rel_path),
            )
            conn.execute(
                """
                INSERT INTO events(
                    event_time, event_type, rel_path, old_sha256, new_sha256, old_size, new_size, summary
                )
                VALUES (?, 'modified', ?, ?, ?, ?, ?, ?)
                """,
                (now, rel_path, row["sha256"], stat.sha256, row["size"], stat.size, summary),
            )
            event_count += 1
        else:
            conn.execute("UPDATE files SET last_seen = ? WHERE rel_path = ?", (now, rel_path))

    deleted = set(known) - set(current)
    for rel_path in sorted(deleted):
        row = known[rel_path]
        conn.execute("DELETE FROM files WHERE rel_path = ?", (rel_path,))
        conn.execute(
            """
            INSERT INTO events(event_time, event_type, rel_path, old_sha256, old_size)
            VALUES (?, 'deleted', ?, ?, ?)
            """,
            (now, rel_path, row["sha256"], row["size"]),
        )
        event_count += 1

    conn.commit()
    if event_count:
        log(f"scan recorded {event_count} event(s)")
    return event_count


def week_bounds(anchor: date | None = None) -> tuple[datetime, datetime]:
    day = anchor or date.today()
    start = day - timedelta(days=day.weekday())
    end = start + timedelta(days=6)
    return datetime.combine(start, dtime.min), datetime.combine(end, dtime.max.replace(microsecond=0))


def read_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def write_state(state: dict[str, Any]) -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=True), encoding="utf-8")


def recently_changed_events(conn: sqlite3.Connection, start: datetime, end: datetime) -> list[sqlite3.Row]:
    return conn.execute(
        """
        SELECT * FROM events
        WHERE event_time >= ? AND event_time <= ?
        ORDER BY event_time ASC, id ASC
        """,
        (start.isoformat(), end.isoformat()),
    ).fetchall()


def file_counts() -> dict[str, int]:
    counts: Counter[str] = Counter()
    for path in VAULT_ROOT.rglob("*"):
        if should_track(path):
            top = path.relative_to(VAULT_ROOT).parts[0]
            counts[top] += 1
    return dict(sorted(counts.items()))


def read_project_state() -> str:
    path = VAULT_ROOT / "11_MEMORY" / "PROJECT_STATE.md"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def markdown_title(path: Path) -> str:
    try:
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if line.startswith("#"):
                return line.lstrip("# ").strip()
            if line.startswith("title:"):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return path.stem.replace("_", " ")


def infer_concepts() -> list[dict[str, str]]:
    concepts: dict[str, dict[str, str]] = {}
    tested = VAULT_ROOT / "03_STRATEGIES" / "TESTED"
    ideas = VAULT_ROOT / "03_STRATEGIES" / "IDEAS"

    for path in tested.glob("*.md") if tested.exists() else []:
        title = markdown_title(path)
        status = "Testato"
        lower = title.lower()
        if "ma crossover" in lower:
            status = "Scartato"
        elif any(key in lower for key in ("rsi", "vwap", "fft", "volatility", "derivative", "fractal")):
            status = "Integrato / promettente"
        concepts[title] = {
            "concept": title,
            "status": status,
            "note": f"Presente in {path.relative_to(PROJECT_ROOT).as_posix()}",
        }

    for path in ideas.glob("*.md") if ideas.exists() else []:
        title = markdown_title(path)
        concepts.setdefault(
            title,
            {
                "concept": title,
                "status": "In studio",
                "note": f"Idea nel vault: {path.relative_to(PROJECT_ROOT).as_posix()}",
            },
        )

    preferred = [
        "FFT Dominant Cycle",
        "FFT Spectral Regime Classifier",
        "RSI Mean-Reversion",
        "Fractal S/R Bounce",
        "Derivative 1st 2nd Order",
        "Volatility Regime Gate",
        "FFT Derivative Confluence",
    ]
    rows = list(concepts.values())
    rows.sort(key=lambda row: (preferred.index(row["concept"]) if row["concept"] in preferred else 999, row["concept"]))
    return rows[:18]


def infer_maturity() -> list[list[str]]:
    counts = file_counts()
    state = read_project_state().lower()
    areas = [
        ("Infrastruttura dati", 90 if "data" in counts or "02_DATA" in counts else 60, "Dataset e cartelle dati presenti nel vault."),
        ("Motore di backtest", 85 if (PROJECT_ROOT / "scripts").exists() else 50, "Runner e report di backtest disponibili in scripts/artifacts."),
        ("Ricerca FFT", 82 if "fft" in state else 55, "Layer FFT gia ricorrente nella memoria di progetto."),
        ("Ricerca Frattali", 72 if "frattal" in state else 45, "Base concettuale presente, da rendere piu numerica."),
        ("Ricerca Regimi di Mercato", 75 if "regime" in state else 45, "Meta-filtri e classificatori in avanzamento."),
        ("Documentazione", 95 if sum(counts.values()) > 50 else 70, "Vault molto ricco e navigabile."),
        ("Knowledge Base Obsidian", 95 if (PROJECT_ROOT / ".obsidian").exists() else 75, "Struttura Obsidian rilevata e aggiornata."),
        ("Integrazione Strategie", 65 if "confluence" in state else 45, "Integrazione ancora da consolidare nel bot finale."),
        ("Decision Engine", 55 if "decision" in state else 35, "Schema presente, regole finali da congelare."),
        ("Bot Prototipo", 60 if "bot" in state else 30, "Prototipi e logica disponibili, produzione non pronta."),
        ("Paper Trading", 10, "Fase successiva alla validazione."),
        ("Produzione Live", 0, "Non avviata, coerente con lo stato del progetto."),
    ]
    return [[area, f"{score}%", note] for area, score, note in areas]


def extract_decisions() -> list[str]:
    candidates = [
        VAULT_ROOT / "11_MEMORY" / "DECISIONS_LOG.md",
        VAULT_ROOT / "11_MEMORY" / "DEVELOPMENT_BACKLOG.md",
        VAULT_ROOT / "11_MEMORY" / "PROJECT_STATE.md",
    ]
    decisions: list[str] = []
    for path in candidates:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line in text.splitlines():
            clean = line.strip(" -")
            lower = clean.lower()
            if not clean or len(clean) < 18:
                continue
            if any(key in lower for key in ("decisione", "priorita", "prossimo", "scart", "validat", "confermat")):
                decisions.append(clean)
            if len(decisions) >= 8:
                return decisions
    return decisions


def quantitative_rows() -> list[list[str]]:
    rows: list[list[str]] = []
    for path in (PROJECT_ROOT / "artifacts").rglob("*.csv"):
        if not should_track(path):
            continue
        name = path.name.lower()
        if "results" not in name and "robust" not in name:
            continue
        try:
            with path.open("r", encoding="utf-8", errors="ignore", newline="") as handle:
                reader = csv.DictReader(handle)
                records = list(reader)
        except OSError:
            continue
        if not records:
            continue
        columns = {col.lower(): col for col in (reader.fieldnames or [])}
        pf_col = next((columns[key] for key in columns if "profit_factor" in key or key == "pf"), None)
        pnl_col = next((columns[key] for key in columns if "pnl" in key), None)
        dd_col = next((columns[key] for key in columns if "drawdown" in key or "dd" == key), None)
        wr_col = next((columns[key] for key in columns if "win" in key and "rate" in key), None)
        tf_col = next((columns[key] for key in columns if key in {"tf", "timeframe"}), None)
        trade_col = next((columns[key] for key in columns if "trade" in key), None)

        def score(record: dict[str, str]) -> float:
            for col in (pf_col, pnl_col):
                if col and record.get(col):
                    try:
                        return float(record[col])
                    except ValueError:
                        return -999999.0
            return -999999.0

        best = max(records, key=score)
        rel = path.relative_to(PROJECT_ROOT).as_posix()
        rows.append(
            [
                rel.replace("artifacts/", "").replace("_", " ")[:42],
                best.get(tf_col, "-") if tf_col else "-",
                best.get(pf_col, "in validazione") if pf_col else "in validazione",
                best.get(wr_col, "in validazione") if wr_col else "in validazione",
                best.get(dd_col, "in validazione") if dd_col else "in validazione",
                best.get(trade_col, "in validazione") if trade_col else "in validazione",
                rel,
            ]
        )
    rows.sort(key=lambda row: row[0])
    return rows[:12]


def event_summary(events: list[sqlite3.Row]) -> dict[str, Any]:
    by_type = Counter(row["event_type"] for row in events)
    by_area = Counter(row["rel_path"].split("/")[1] if row["rel_path"].startswith("Pipeline_01/") else row["rel_path"].split("/")[0] for row in events)
    important = [
        row
        for row in events
        if row["event_type"] != "deleted"
        and any(token in row["rel_path"].lower() for token in ("memory", "strategy", "backtest", "report", "src/", "scripts/"))
    ]
    return {
        "by_type": by_type,
        "by_area": by_area,
        "important": important[-20:],
    }


def table_markdown(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        safe = [str(value).replace("|", "/") for value in row]
        lines.append("| " + " | ".join(safe) + " |")
    return lines


def build_markdown_report(start: datetime, end: datetime, events: list[sqlite3.Row]) -> str:
    generated = local_now()
    summary = event_summary(events)
    maturity = infer_maturity()
    concepts = infer_concepts()
    quant_rows = quantitative_rows()
    decisions = extract_decisions()

    lines: list[str] = [
        "---",
        f"title: Rendicontazione Settimanale {start.date()} {end.date()}",
        "type: weekly_report",
        "priority: high",
        f"updated: {generated.date().isoformat()}",
        "---",
        "",
        f"# Rendicontazione Settimanale del Progetto Bot Ibrido - {start.date()} / {end.date()}",
        "",
        "Documento generato automaticamente dal watcher del vault. La struttura segue il template di rendicontazione completo: dashboard generale, registro concetti, ricerca, versioni bot, evidenze quantitative, decisioni e richieste operative.",
        "",
        "## Sintesi della settimana",
        f"- Eventi tracciati: {len(events)}",
        f"- File creati: {summary['by_type'].get('created', 0)}",
        f"- File modificati: {summary['by_type'].get('modified', 0)}",
        f"- File eliminati: {summary['by_type'].get('deleted', 0)}",
        f"- Aree piu attive: {', '.join(f'{area} ({count})' for area, count in summary['by_area'].most_common(5)) or 'nessuna modifica rilevata'}",
        "",
        "## 1. Dashboard generale dello stato del progetto",
    ]
    lines.extend(table_markdown(["Area", "Stato stimato", "Nota operativa"], maturity))
    lines.extend(["", "## 2. Registro dei concetti testati"])
    concept_rows = [[row["concept"], row["status"], row["note"]] for row in concepts]
    lines.extend(table_markdown(["Concetto", "Stato", "Lettura sintetica"], concept_rows))

    status_counts = Counter(row["status"] for row in concepts)
    research_rows = [
        ["Concetti analizzati", str(len(concepts))],
        ["Concetti testati / integrati", str(sum(count for key, count in status_counts.items() if "Testato" in key or "Integrato" in key))],
        ["Concetti scartati", str(status_counts.get("Scartato", 0))],
        ["Concetti promettenti", str(sum(count for key, count in status_counts.items() if "promettente" in key.lower()))],
        ["Concetti ancora in studio", str(status_counts.get("In studio", 0))],
        ["File nella knowledge base", str(sum(file_counts().values()))],
    ]
    lines.extend(["", "## 3. Dashboard della ricerca"])
    lines.extend(table_markdown(["Metrica", "Valore"], research_rows))

    lines.extend(["", "## 4. Dashboard dei bot e delle versioni"])
    bot_rows = [
        ["V1", "Esplorazione iniziale", "Storico", "Segnali singoli fragili", "Serve modularita e filtro di contesto"],
        ["V2", "FFT / ciclo dominante", "Promettente", "Lettura ritmo mercato", "Base per regime classifier"],
        ["V3", "Frattali + S/R", "Promettente", "Struttura geometrica", "Da confermare con ritmo e regime"],
        ["V4", "Hybrid multi-layer", "In sviluppo", "Regime + ciclo + trigger", "Direzione principale del progetto"],
        ["V5", "Bot finale modulare", "Prossimo obiettivo", "Session-aware e risk-aware", "Congelare decision engine"],
    ]
    lines.extend(table_markdown(["Versione", "Stato", "Esito", "Obiettivo", "Lezione chiave"], bot_rows))

    lines.extend(["", "## 5. Evidenze quantitative standard"])
    if quant_rows:
        lines.extend(table_markdown(["Strategia / report", "TF", "Profit Factor", "Win Rate", "Drawdown", "Trade", "Fonte"], quant_rows))
    else:
        lines.append("- Nessuna tabella quantitativa CSV rilevata nella settimana. Collegare i nuovi backtest a `artifacts` per popolare questa sezione.")

    lines.extend(["", "## 6. File significativi aggiunti o modificati"])
    important = summary["important"]
    if important:
        for row in important:
            label = row["summary"] or row["event_type"]
            lines.append(f"- `{row['rel_path']}` - {row['event_type']} - {label}")
    else:
        lines.append("- Nessun file critico modificato nelle aree memoria, strategie, backtest o codice.")

    lines.extend(["", "## 7. Decisioni del periodo"])
    if decisions:
        for decision in decisions:
            lines.append(f"- {decision}")
    else:
        lines.append("- Nessuna decisione esplicita rilevata nei file memoria; aggiornare `Pipeline_01/11_MEMORY/DECISIONS_LOG.md`.")

    lines.extend(
        [
            "",
            "## 8. Richieste operative",
            "- Programmatore: alta priorita per modularizzazione, orchestration dei layer e generazione metriche ripetibile.",
            "- Supporto ricerca / AI: alta priorita per sintesi settimanale, pulizia backlog e definizione esperimenti.",
            "- Server dedicato: priorita media, utile quando le grid diventano continue o molto pesanti.",
            "",
            "## 9. Roadmap suggerita",
            "- 0-30 giorni: congelare moduli del bot finale, standardizzare log/backtest e mantenere questa rendicontazione attiva.",
            "- 30-60 giorni: integrare strategie per regime e completare il decision engine.",
            "- 60-90 giorni: paper trading controllato, pulizia falsi positivi e consolidamento operativo.",
            "",
            "## Conclusione tecnica",
            "La settimana viene misurata non solo come attivita svolta, ma come avanzamento della maturita del sistema. Il watcher mantiene la memoria delle modifiche, mentre il report sintetizza lo stato del laboratorio, le evidenze quantitative e i prossimi passi operativi.",
            "",
        ]
    )
    return "\n".join(lines)


def pdf_table(rows: list[list[str]], headers: list[str], widths: list[float] | None = None) -> Table:
    data = [[Paragraph(html.escape(str(cell)), small_bold_style()) for cell in headers]]
    for row in rows:
        data.append([Paragraph(html.escape(str(cell)), small_style()) for cell in row])
    table = Table(data, colWidths=widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#16324F")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#AAB7C4")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#F7FAFC"), colors.HexColor("#EDF2F7")]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return table


def small_style() -> ParagraphStyle:
    return ParagraphStyle("Small", fontName="Helvetica", fontSize=7, leading=9, alignment=TA_LEFT)


def small_bold_style() -> ParagraphStyle:
    return ParagraphStyle("SmallBold", parent=small_style(), fontName="Helvetica-Bold", textColor=colors.white)


def add_page_number(canvas: Any, doc: Any) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#5B6770"))
    canvas.drawRightString(doc.pagesize[0] - 14 * mm, 9 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf_report(start: datetime, end: datetime, events: list[sqlite3.Row], pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    summary = event_summary(events)
    maturity = infer_maturity()
    concepts = infer_concepts()
    quant_rows = quantitative_rows()
    decisions = extract_decisions()

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=landscape(A4),
        rightMargin=12 * mm,
        leftMargin=12 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
    )
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#16324F"),
        alignment=TA_CENTER,
    )
    subtitle = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#4A5568"),
        alignment=TA_CENTER,
    )
    section = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#16324F"),
        spaceBefore=6,
        spaceAfter=5,
    )
    body = ParagraphStyle("Body", parent=styles["Normal"], fontSize=9, leading=12, textColor=colors.HexColor("#1F2933"))

    story: list[Any] = [
        Paragraph("Rendicontazione Settimanale del Progetto Bot Ibrido", title),
        Paragraph(f"Periodo: {start.date()} / {end.date()} - generato il {local_now().date()}", subtitle),
        Spacer(1, 5),
        Paragraph(
            "Documento automatico basato sulla memoria eventi del vault. Misura maturita, ricerca, versioni bot, evidenze quantitative e richieste operative.",
            body,
        ),
        Spacer(1, 5),
        Paragraph("Sintesi della settimana", section),
        Paragraph(
            f"Eventi tracciati: {len(events)} | creati: {summary['by_type'].get('created', 0)} | modificati: {summary['by_type'].get('modified', 0)} | eliminati: {summary['by_type'].get('deleted', 0)}.",
            body,
        ),
        Paragraph("1. Dashboard generale dello stato del progetto", section),
        pdf_table(maturity, ["Area", "Stato stimato", "Nota operativa"], [42 * mm, 25 * mm, 150 * mm]),
        PageBreak(),
        Paragraph("2. Registro dei concetti testati", section),
        pdf_table([[row["concept"], row["status"], row["note"]] for row in concepts], ["Concetto", "Stato", "Lettura sintetica"], [55 * mm, 35 * mm, 130 * mm]),
        Spacer(1, 6),
        Paragraph("3. Dashboard della ricerca", section),
        pdf_table(
            [
                ["Concetti analizzati", str(len(concepts))],
                ["File nella knowledge base", str(sum(file_counts().values()))],
                ["Aree attive", ", ".join(f"{area} ({count})" for area, count in summary["by_area"].most_common(5))],
            ],
            ["Metrica", "Valore"],
            [65 * mm, 150 * mm],
        ),
        PageBreak(),
        Paragraph("4. Dashboard dei bot e delle versioni", section),
        pdf_table(
            [
                ["V1", "Esplorazione iniziale", "Storico", "Segnali singoli fragili", "Serve modularita"],
                ["V2", "FFT / ciclo dominante", "Promettente", "Lettura ritmo mercato", "Base regime classifier"],
                ["V3", "Frattali + S/R", "Promettente", "Struttura geometrica", "Conferma con ritmo"],
                ["V4", "Hybrid multi-layer", "In sviluppo", "Regime + ciclo + trigger", "Direzione principale"],
                ["V5", "Bot finale modulare", "Prossimo obiettivo", "Session-aware", "Congelare engine"],
            ],
            ["Versione", "Stato", "Esito", "Obiettivo", "Lezione chiave"],
        ),
        Spacer(1, 6),
        Paragraph("5. Evidenze quantitative standard", section),
    ]
    if quant_rows:
        story.append(pdf_table(quant_rows, ["Strategia / report", "TF", "PF", "Win Rate", "Drawdown", "Trade", "Fonte"]))
    else:
        story.append(Paragraph("Nessuna tabella quantitativa CSV rilevata.", body))

    story.extend([PageBreak(), Paragraph("6. Decisioni del periodo", section)])
    if decisions:
        for decision in decisions[:8]:
            story.append(Paragraph("- " + html.escape(decision), body))
    else:
        story.append(Paragraph("- Nessuna decisione esplicita rilevata nei file memoria.", body))

    story.extend(
        [
            Spacer(1, 6),
            Paragraph("7. Richieste operative", section),
            Paragraph("- Programmatore: modularizzazione, orchestrazione layer, metriche ripetibili.", body),
            Paragraph("- Supporto ricerca / AI: sintesi risultati, backlog, esperimenti.", body),
            Paragraph("- Server dedicato: utile quando le grid diventano continue o pesanti.", body),
            Spacer(1, 6),
            Paragraph("Conclusione tecnica", section),
            Paragraph(
                "La rendicontazione misura avanzamento reale e maturita del sistema. La memoria eventi permette di ricostruire cosa e cambiato ogni settimana senza dipendere dalla cronologia della chat.",
                body,
            ),
        ]
    )

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


def generate_weekly_report(conn: sqlite3.Connection, anchor: date | None = None) -> tuple[Path, Path, int]:
    start, end = week_bounds(anchor)
    events = recently_changed_events(conn, start, end)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    suffix = f"{start.date().isoformat()}_{end.date().isoformat()}"
    md_path = REPORTS_DIR / f"rendicontazione_settimanale_{suffix}.md"
    pdf_path = ARTIFACT_DIR / f"rendicontazione_settimanale_{suffix}.pdf"
    md_path.write_text(build_markdown_report(start, end, events), encoding="utf-8")
    build_pdf_report(start, end, events, pdf_path)
    conn.execute(
        """
        INSERT OR REPLACE INTO reports(week_start, week_end, generated_at, markdown_path, pdf_path, event_count)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            start.date().isoformat(),
            end.date().isoformat(),
            local_now().isoformat(),
            md_path.relative_to(PROJECT_ROOT).as_posix(),
            pdf_path.relative_to(PROJECT_ROOT).as_posix(),
            len(events),
        ),
    )
    conn.commit()
    log(f"generated weekly report {md_path} and {pdf_path}")
    return md_path, pdf_path, len(events)


def due_week_anchor(state: dict[str, Any]) -> date | None:
    now = local_now()
    anchor: date | None = None
    if now.weekday() == WEEKLY_REPORT_DAY and now.time() >= WEEKLY_REPORT_TIME:
        anchor = now.date()
    elif now.weekday() < WEEKLY_REPORT_DAY:
        anchor = now.date() - timedelta(days=7)

    if anchor is None:
        return None
    start, _ = week_bounds(anchor)
    if state.get("last_weekly_report_start") == start.date().isoformat():
        return None
    return anchor


def run_daemon() -> None:
    conn = connect()
    log("vault weekly reporter started")
    while True:
        try:
            record_scan(conn)
            state = read_state()
            anchor = due_week_anchor(state)
            if anchor is not None:
                start, _ = week_bounds(anchor)
                generate_weekly_report(conn, anchor)
                state["last_weekly_report_start"] = start.date().isoformat()
                state["last_weekly_report_at"] = local_now().isoformat()
                write_state(state)
        except Exception as exc:  # noqa: BLE001 - daemon must keep running and log failures.
            log(f"error: {exc!r}")
        time.sleep(POLL_SECONDS)


def main() -> None:
    parser = argparse.ArgumentParser(description="Watcher e rendicontazione settimanale del vault.")
    parser.add_argument("--scan-once", action="store_true", help="Esegue una scansione e aggiorna la memoria.")
    parser.add_argument("--report-now", action="store_true", help="Genera subito il report della settimana corrente.")
    parser.add_argument("--daemon", action="store_true", help="Rimane acceso in background e genera report la domenica sera.")
    parser.add_argument("--date", help="Data di riferimento YYYY-MM-DD per il report.")
    args = parser.parse_args()

    conn = connect()
    if args.scan_once:
        count = record_scan(conn)
        print(f"Scansione completata: {count} evento/i registrato/i.")
    if args.report_now:
        anchor = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else None
        md_path, pdf_path, count = generate_weekly_report(conn, anchor)
        print(f"Report generato con {count} evento/i:")
        print(md_path)
        print(pdf_path)
    if args.daemon:
        run_daemon()
    if not (args.scan_once or args.report_now or args.daemon):
        parser.print_help()


if __name__ == "__main__":
    main()
