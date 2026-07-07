from __future__ import annotations

import html
import os
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Preformatted, SimpleDocTemplate, Spacer


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PIPELINE_ROOT = PROJECT_ROOT / "Pipeline_01"
REPORTS_ROOT = PROJECT_ROOT / "artifacts" / "derivative_backtests" / "reports"


PYTHON_DOCS = [
    {
        "source": PROJECT_ROOT / "src" / "derivatives_bt" / "backtest.py",
        "doc": PROJECT_ROOT / "src" / "derivatives_bt" / "backtest.md",
        "title": "Code Doc - backtest.py",
        "purpose": "Motore principale dei backtest a derivate con strategia Backtrader, sizing, gestione ordini e metriche finali.",
        "highlights": [
            "Definisce la strategia `DerivativeCrossStrategy` basata su EMA, derivata prima e derivata seconda.",
            "Implementa il sizing in funzione del rischio per trade, ATR e leva massima.",
            "Produce metriche aggregate come PF, win rate, drawdown e distribuzione long/short.",
            "Espone `run_optimization()` per lanciare grid search su insiemi di parametri.",
        ],
        "related": [
            PROJECT_ROOT / "Pipeline_01" / "03_STRATEGIES" / "TESTED" / "02_Derivative_1st_2nd_Order.md",
            PROJECT_ROOT / "Pipeline_01" / "04_BACKTEST" / "DERIVATIVE_tests" / "INDEX.md",
            PROJECT_ROOT / "Pipeline_01" / "06_AGENT_LOGIC" / "decision_system.md",
        ],
    },
    {
        "source": PROJECT_ROOT / "src" / "derivatives_bt" / "data_utils.py",
        "doc": PROJECT_ROOT / "src" / "derivatives_bt" / "data_utils.md",
        "title": "Code Doc - data_utils.py",
        "purpose": "Utility di caricamento, merge, resampling e split dei dataset HistData usati nei backtest.",
        "highlights": [
            "Legge i file ASCII compressi in zip e li converte in DataFrame OHLCV ordinati.",
            "Gestisce il resampling a M1, M5 e M15.",
            "Fornisce lo split train/OOS usato dal runner dei backtest.",
        ],
        "related": [
            PROJECT_ROOT / "Pipeline_01" / "02_DATA" / "INDEX.md",
            PROJECT_ROOT / "Pipeline_01" / "02_DATA" / "data_pipeline.md",
            PROJECT_ROOT / "Pipeline_01" / "03_STRATEGIES" / "TESTED" / "02_Derivative_1st_2nd_Order.md",
        ],
    },
    {
        "source": PROJECT_ROOT / "scripts" / "run_derivative_grid.py",
        "doc": PROJECT_ROOT / "scripts" / "run_derivative_grid.md",
        "title": "Code Doc - run_derivative_grid.py",
        "purpose": "Runner operativo che carica i dataset EURUSD, lancia la grid search multi-timeframe e salva report e risultati.",
        "highlights": [
            "Definisce le griglie `smoke`, `focused` e `full` per la strategia a derivate.",
            "Esegue train e out-of-sample separati su ogni timeframe richiesto.",
            "Esporta risultati in CSV, JSON e report Markdown per timeframe e ranking complessivo.",
            "E il punto di ingresso principale per i backtest sistematici del concetto `d1 + d2`.",
        ],
        "related": [
            PROJECT_ROOT / "Pipeline_01" / "03_STRATEGIES" / "TESTED" / "02_Derivative_1st_2nd_Order.md",
            PROJECT_ROOT / "Pipeline_01" / "04_BACKTEST" / "INDEX.md",
            PROJECT_ROOT / "Pipeline_01" / "09_LOGS" / "esperimenti.md",
        ],
    },
    {
        "source": PROJECT_ROOT / "scripts" / "build_daily_report_pdf.py",
        "doc": PROJECT_ROOT / "scripts" / "build_daily_report_pdf.md",
        "title": "Code Doc - build_daily_report_pdf.py",
        "purpose": "Script di publishing che prende dati dal workbook e dagli artifact e costruisce un report PDF giornaliero.",
        "highlights": [
            "Legge il workbook Excel con `openpyxl`.",
            "Legge i risultati smoke delle derivate e li integra nel report giornaliero.",
            "Costruisce sia markdown sia PDF impaginato tramite `reportlab`.",
            "E utile come base per futuri report automatici e documentazione esportabile.",
        ],
        "related": [
            PROJECT_ROOT / "Pipeline_01" / "09_LOGS" / "report_giornata_2026-04-22.md",
            PROJECT_ROOT / "Pipeline_01" / "09_LOGS" / "INDEX.md",
            PROJECT_ROOT / "Pipeline_01" / "11_MEMORY" / "PROJECT_STATE.md",
        ],
    },
    {
        "source": PROJECT_ROOT / "src" / "derivatives_bt" / "__init__.py",
        "doc": PROJECT_ROOT / "src" / "derivatives_bt" / "__init__.md",
        "title": "Code Doc - __init__.py",
        "purpose": "File di package che identifica `derivatives_bt` come modulo Python del progetto.",
        "highlights": [
            "Rende importabile il package locale `derivatives_bt`.",
            "Definisce la descrizione minimale del modulo per il contesto di ricerca.",
        ],
        "related": [
            PROJECT_ROOT / "Pipeline_01" / "03_STRATEGIES" / "TESTED" / "02_Derivative_1st_2nd_Order.md",
            PROJECT_ROOT / "Pipeline_01" / "11_MEMORY" / "PROJECT_STATE.md",
        ],
    },
]


def rel_link(from_path: Path, target: Path, label: str) -> str:
    rel = os.path.relpath(target, from_path.parent).replace("\\", "/")
    return f"[{label}]({rel})"


def project_rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    ensure_dir(path)
    path.write_text(content, encoding="utf-8")


def generate_python_docs() -> list[Path]:
    generated: list[Path] = []
    code_index_path = PIPELINE_ROOT / "12_CODE" / "INDEX.md"

    for item in PYTHON_DOCS:
        source = item["source"]
        doc = item["doc"]
        code = source.read_text(encoding="utf-8")
        code_index_label = "Torna all indice del codice"

        lines: list[str] = []
        lines.append(f"# {item['title']}")
        lines.append("")
        lines.append("## Source")
        lines.append(f"- `{project_rel(source)}`")
        lines.append(f"- {rel_link(doc, source, 'Apri il file Python sorgente')}")
        lines.append(f"- {rel_link(doc, code_index_path, code_index_label)}")
        lines.append("")
        lines.append("## Scopo")
        lines.append(item["purpose"])
        lines.append("")
        lines.append("## Punti Chiave")
        for bullet in item["highlights"]:
            lines.append(f"- {bullet}")
        lines.append("")
        lines.append("## Collegamenti")
        for related in item["related"]:
            lines.append(f"- {rel_link(doc, related, related.stem)}")
        lines.append("")
        lines.append("## Codice Completo")
        lines.append("```python")
        lines.append(code.rstrip())
        lines.append("```")
        lines.append("")

        write_text(doc, "\n".join(lines))
        generated.append(doc)

    return generated


def generate_code_index() -> Path:
    index_path = PIPELINE_ROOT / "12_CODE" / "INDEX.md"
    lines: list[str] = []
    lines.append("# Code Index")
    lines.append("")
    lines.append("## Scopo")
    lines.append("Raccogliere la documentazione affiancata ai file Python del progetto.")
    lines.append("")
    lines.append("## Moduli Python Documentati")
    for item in PYTHON_DOCS:
        doc = item["doc"]
        lines.append(f"- {rel_link(index_path, doc, doc.stem)}")
    lines.append("")
    lines.append("## Collegamenti")
    lines.append(f"- {rel_link(index_path, PIPELINE_ROOT / '04_BACKTEST' / 'INDEX.md', 'Backtest Index')}")
    lines.append(f"- {rel_link(index_path, PIPELINE_ROOT / '11_MEMORY' / 'INDEX.md', 'Memory Index')}")
    lines.append(f"- {rel_link(index_path, PIPELINE_ROOT / '03_STRATEGIES' / 'TESTED' / '02_Derivative_1st_2nd_Order.md', 'Derivative 1st and 2nd Order')}")
    lines.append("")
    write_text(index_path, "\n".join(lines))
    return index_path


def collect_markdown_targets() -> list[Path]:
    targets: list[Path] = []
    for root in (PIPELINE_ROOT, REPORTS_ROOT):
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.md")):
            targets.append(path)
    return targets


def generate_pdf_library_index(markdown_targets: list[Path]) -> Path:
    index_path = PIPELINE_ROOT / "13_PDF_LIBRARY" / "INDEX.md"
    pipeline_targets = [path for path in markdown_targets if PIPELINE_ROOT in path.parents]
    report_targets = [path for path in markdown_targets if REPORTS_ROOT in path.parents]

    lines: list[str] = []
    lines.append("# PDF Library")
    lines.append("")
    lines.append("## Scopo")
    lines.append("Mappare le note Markdown del vault ai rispettivi PDF companion generati automaticamente.")
    lines.append("")
    lines.append("## Pipeline_01")
    for path in pipeline_targets:
        lines.append(
            f"- {rel_link(index_path, path, path.stem)} -> {rel_link(index_path, path.with_suffix('.pdf'), path.with_suffix('.pdf').name)}"
        )
    lines.append("")
    lines.append("## Derivative Reports")
    for path in report_targets:
        lines.append(
            f"- {rel_link(index_path, path, path.stem)} -> {rel_link(index_path, path.with_suffix('.pdf'), path.with_suffix('.pdf').name)}"
        )
    lines.append("")
    lines.append("## Collegamenti")
    lines.append(f"- {rel_link(index_path, PIPELINE_ROOT / '11_MEMORY' / 'INDEX.md', 'Memory Index')}")
    lines.append(f"- {rel_link(index_path, PIPELINE_ROOT / '09_LOGS' / 'INDEX.md', 'Logs Index')}")
    lines.append("")

    write_text(index_path, "\n".join(lines))
    return index_path


def markdown_to_story(md_text: str) -> list[object]:
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "VaultTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#16324F"),
        alignment=TA_LEFT,
        spaceAfter=8,
    )
    h1_style = ParagraphStyle(
        "H1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#16324F"),
        spaceBefore=8,
        spaceAfter=6,
    )
    h2_style = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#1F3C5B"),
        spaceBefore=6,
        spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        textColor=colors.black,
        spaceAfter=3,
    )
    code_style = ParagraphStyle(
        "CodeBlock",
        parent=styles["Code"],
        fontName="Courier",
        fontSize=8.5,
        leading=10.5,
        textColor=colors.HexColor("#222222"),
    )

    story: list[object] = []
    in_code = False
    code_lines: list[str] = []

    for raw_line in md_text.splitlines():
        line = raw_line.rstrip()

        if line.startswith("```"):
            if in_code:
                story.append(Preformatted("\n".join(code_lines), code_style))
                story.append(Spacer(1, 4))
                code_lines = []
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        stripped = line.strip()
        if not stripped:
            story.append(Spacer(1, 4))
            continue

        escaped = html.escape(stripped)
        if stripped.startswith("# "):
            story.append(Paragraph(html.escape(stripped[2:].strip()), title_style))
        elif stripped.startswith("## "):
            story.append(Paragraph(html.escape(stripped[3:].strip()), h1_style))
        elif stripped.startswith("### "):
            story.append(Paragraph(html.escape(stripped[4:].strip()), h2_style))
        elif re.match(r"^[-*] ", stripped):
            story.append(Paragraph(f"&bull; {html.escape(stripped[2:].strip())}", body_style))
        elif re.match(r"^\d+\. ", stripped):
            story.append(Paragraph(html.escape(stripped), body_style))
        else:
            story.append(Paragraph(escaped, body_style))

    if code_lines:
        story.append(Preformatted("\n".join(code_lines), code_style))
        story.append(Spacer(1, 4))

    return story


def build_pdf_from_markdown(md_path: Path) -> Path:
    pdf_path = md_path.with_suffix(".pdf")
    md_text = md_path.read_text(encoding="utf-8")
    story = markdown_to_story(md_text)

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
    )
    doc.build(story)
    return pdf_path


def main() -> None:
    generate_python_docs()
    generate_code_index()
    markdown_targets = collect_markdown_targets()
    generate_pdf_library_index(markdown_targets)
    markdown_targets = collect_markdown_targets()

    for md_path in markdown_targets:
        build_pdf_from_markdown(md_path)

    print(f"Python docs generated: {len(PYTHON_DOCS)}")
    print(f"Markdown PDFs generated: {len(markdown_targets)}")


if __name__ == "__main__":
    main()
