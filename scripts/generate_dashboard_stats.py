"""Genera docs/data/stats.json con lo stato completo del progetto.

Viene eseguito:
- localmente: python scripts/generate_dashboard_stats.py
- in CI: dal workflow GitHub Actions ad ogni push, prima del deploy su Pages

Il JSON alimenta la dashboard statica in docs/index.html.
"""

from __future__ import annotations

import csv
import json
import math
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "data" / "stats.json"

# Cartelle escluse dalla scansione
EXCLUDE_DIRS = {".git", "__pycache__", ".obsidian", "node_modules", ".claude", "docs"}

# Estensioni raggruppate per categoria
EXT_CATEGORIES = {
    ".md": "Markdown",
    ".py": "Python",
    ".csv": "CSV",
    ".json": "JSON",
    ".pdf": "PDF",
    ".png": "Immagini",
    ".pine": "PineScript",
    ".ps1": "Script",
    ".bat": "Script",
    ".pkl": "Binari",
    ".pyc": "Binari",
    ".xlsx": "Excel",
    ".txt": "Testo",
    ".log": "Log",
}


def iter_files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue
        yield path, rel


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def scan_files():
    files = []
    by_category: dict[str, dict] = {}
    by_folder: dict[str, dict] = {}
    total_size = 0
    py_loc = 0
    md_words = 0

    for path, rel in iter_files():
        stat = path.stat()
        total_size += stat.st_size
        cat = EXT_CATEGORIES.get(path.suffix.lower(), "Altro")
        c = by_category.setdefault(cat, {"files": 0, "size": 0})
        c["files"] += 1
        c["size"] += stat.st_size

        top = rel.parts[0] if len(rel.parts) > 1 else "(root)"
        f = by_folder.setdefault(top, {"files": 0, "size": 0})
        f["files"] += 1
        f["size"] += stat.st_size

        if path.suffix == ".py":
            py_loc += sum(1 for line in read_text(path).splitlines() if line.strip())
        elif path.suffix == ".md":
            md_words += len(read_text(path).split())

        files.append(
            {
                "path": str(rel).replace("\\", "/"),
                "size": stat.st_size,
                "mtime": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
            }
        )

    files.sort(key=lambda x: x["mtime"], reverse=True)
    return {
        "total_files": len(files),
        "total_size": total_size,
        "python_loc": py_loc,
        "markdown_words": md_words,
        "by_category": by_category,
        "by_folder": by_folder,
        "recent_files": files[:25],
    }


def parse_project_state():
    """Estrae lo stato delle strategie da PROJECT_STATE.md."""
    text = read_text(ROOT / "Pipeline_01" / "11_MEMORY" / "PROJECT_STATE.md")
    strategies = []
    section = re.search(r"## Stato delle strategie\n(.*?)(?:\n## |\Z)", text, re.S)
    if section:
        for line in section.group(1).splitlines():
            line = line.strip()
            if line.startswith("- ") and ":" in line:
                name, _, desc = line[2:].partition(":")
                desc = desc.strip()
                low = desc.lower()
                if low.startswith("testato"):
                    status = "testato"
                elif "non ancora" in low or "non validato" in low:
                    status = "da fare"
                else:
                    status = "in corso"
                strategies.append({"name": name.strip(), "status": status, "note": desc})
    updated = re.search(r"^updated:\s*(\S+)", text, re.M)
    return {
        "strategies": strategies,
        "state_updated": updated.group(1) if updated else None,
    }


def parse_backlog():
    """Estrae il backlog per priorita da DEVELOPMENT_BACKLOG.md."""
    text = read_text(ROOT / "Pipeline_01" / "11_MEMORY" / "DEVELOPMENT_BACKLOG.md")
    items = []
    current_priority = None
    current_item = None
    for line in text.splitlines():
        prio = re.match(r"### PRIORITA (\d+)\s*-\s*(.+)", line)
        if prio:
            current_priority = {"level": int(prio.group(1)), "title": prio.group(2).strip()}
            continue
        item = re.match(r"\*\*(#\d+)\s*-\s*(.+?)\*\*", line.strip())
        if item and current_priority:
            current_item = {
                "id": item.group(1),
                "title": item.group(2).strip(),
                "priority": current_priority["level"],
                "priority_title": current_priority["title"],
                "done": False,
            }
            items.append(current_item)
            continue
        if current_item and re.match(r"-\s*completat", line.strip(), re.I):
            current_item["done"] = True
    return items


def parse_tested_strategies():
    tested_dir = ROOT / "Pipeline_01" / "03_STRATEGIES" / "TESTED"
    ideas_dir = ROOT / "Pipeline_01" / "03_STRATEGIES" / "IDEAS"
    tested = []
    for f in sorted(tested_dir.glob("*.md")):
        if f.stem.startswith("template"):
            continue
        text = read_text(f)
        h1 = re.search(r"^# (.+)", text, re.M)
        decision = re.search(r"## Decisione\n(.*?)(?:\n## |\Z)", text, re.S)
        tested.append(
            {
                "file": f"Pipeline_01/03_STRATEGIES/TESTED/{f.name}",
                "title": h1.group(1).strip() if h1 else f.stem,
                "decision": decision.group(1).strip()[:300] if decision else None,
            }
        )
    ideas = [
        {"file": f"Pipeline_01/03_STRATEGIES/IDEAS/{f.name}", "title": f.stem.replace("_", " ")}
        for f in sorted(ideas_dir.glob("*.md"))
    ]
    return {"tested": tested, "ideas": ideas}


# colonne metrica riconosciute nei CSV dei risultati (nomi alternativi per famiglia)
METRIC_ALIASES = {
    "oos_pf": ["oos_profit_factor", "oos_gated_profit_factor"],
    "train_pf": ["train_profit_factor", "train_gated_profit_factor"],
    "oos_dd": ["oos_max_drawdown_pct", "oos_gated_max_drawdown_pct"],
    "oos_trades": ["oos_trades", "oos_gated_trades"],
    "oos_win_rate": ["oos_win_rate", "oos_gated_win_rate"],
    "oos_pnl": ["oos_pnl_pct", "oos_gated_pnl_pct"],
}
MAX_POINTS = 250


def _num(v):
    """Converte in float finito, altrimenti None (JSON non ammette inf/nan)."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if math.isfinite(f) else None


def analyze_results_csv(family_dir: Path):
    """Estrae punti e riassunto dal CSV principale dei risultati di una famiglia."""
    data_dir = family_dir / "data"
    if not data_dir.is_dir():
        return None
    candidates = sorted(data_dir.glob("*_all.csv")) or sorted(
        (f for f in data_dir.glob("*.csv") if "combined" not in f.name),
        key=lambda f: f.stat().st_size, reverse=True,
    )
    if not candidates:
        return None
    csv_path = candidates[0]
    try:
        with csv_path.open(encoding="utf-8", errors="replace", newline="") as fh:
            reader = csv.DictReader(fh)
            fields = reader.fieldnames or []
            keymap = {}
            for name, aliases in METRIC_ALIASES.items():
                for a in aliases:
                    if a in fields:
                        keymap[name] = a
                        break
            if "oos_pf" not in keymap:
                return None
            metric_cols = set(keymap.values())
            param_cols = [
                f for f in fields
                if not f.startswith(("train_", "oos_", "total_"))
                and f not in metric_cols and f != "avg_bars"
            ]
            rows = []
            for r in reader:
                point = {name: _num(r.get(col)) for name, col in keymap.items()}
                if point["oos_pf"] is None:
                    continue
                point["params"] = {p: r.get(p) for p in param_cols}
                rows.append(point)
    except OSError:
        return None
    if not rows:
        return None
    rows.sort(key=lambda x: x["oos_pf"], reverse=True)
    pfs = [r["oos_pf"] for r in rows]
    n = len(pfs)
    # il "best" deve avere un minimo di trade OOS per non premiare combo degeneri
    MIN_TRADES = 30
    best = next((r for r in rows if (r.get("oos_trades") or 0) >= MIN_TRADES), rows[0])
    summary = {
        "combos": n,
        "best": best,
        "median_pf": round(pfs[n // 2], 4),
        "pct_pf_above_1": round(sum(1 for p in pfs if p > 1) / n * 100, 1),
        "pct_pf_above_1_3": round(sum(1 for p in pfs if p > 1.3) / n * 100, 1),
        "source_csv": csv_path.name,
    }
    # top per PF + campionamento uniforme del resto, per scatter rappresentativi
    # (il best selezionato sta sempre in testa: il client evidenzia points[0])
    top = [best] + [r for r in rows[: MAX_POINTS // 2] if r is not best]
    rest = rows[MAX_POINTS // 2:]
    step = max(1, len(rest) // (MAX_POINTS - len(top)))
    points = top + rest[::step]
    return {"param_cols": param_cols, "summary": summary, "points": points[:MAX_POINTS]}


def git_commits(limit=30):
    """Feed commit generato in build: evita il rate-limit dell'API GitHub lato client."""
    try:
        out = subprocess.run(
            ["git", "log", f"-{limit}", "--pretty=format:%H%x1f%an%x1f%aI%x1f%s"],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=30,
        )
        if out.returncode != 0:
            return []
        commits = []
        for line in out.stdout.splitlines():
            parts = line.split("\x1f")
            if len(parts) == 4:
                commits.append({"sha": parts[0], "author": parts[1],
                                "date": parts[2], "message": parts[3]})
        return commits
    except (OSError, subprocess.SubprocessError):
        return []


def scan_backtests():
    """Riassume ogni famiglia di backtest in artifacts/."""
    artifacts = ROOT / "artifacts"
    families = []
    for d in sorted(artifacts.iterdir()):
        if not d.is_dir() or not d.name.endswith("_backtests"):
            continue
        data_files = [f for f in (d / "data").glob("*") if f.is_file()] if (d / "data").is_dir() else []
        report_files = (
            [f for f in (d / "reports").glob("*.md") if f.is_file()] if (d / "reports").is_dir() else []
        )
        all_files = data_files + report_files
        last = max((f.stat().st_mtime for f in all_files), default=0)
        families.append(
            {
                "name": d.name.replace("_backtests", "").replace("_", " ").title(),
                "dir": f"artifacts/{d.name}",
                "data_files": len(data_files),
                "reports": [f"artifacts/{d.name}/reports/{f.name}" for f in sorted(report_files)],
                "size": sum(f.stat().st_size for f in all_files),
                "last_run": datetime.fromtimestamp(last, tz=timezone.utc).isoformat() if last else None,
                "analysis": analyze_results_csv(d),
            }
        )
    return families


def main():
    stats = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project": "TRADING_BOT_SYSTEM_HYBRID_PRO",
        "files": scan_files(),
        "project_state": parse_project_state(),
        "backlog": parse_backlog(),
        "strategies": parse_tested_strategies(),
        "backtests": scan_backtests(),
        "commits": git_commits(),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"OK: {OUT} ({OUT.stat().st_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
