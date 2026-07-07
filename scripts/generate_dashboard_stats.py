"""Genera docs/data/stats.json con lo stato completo del progetto.

Viene eseguito:
- localmente: python scripts/generate_dashboard_stats.py
- in CI: dal workflow GitHub Actions ad ogni push, prima del deploy su Pages

Il JSON alimenta la dashboard statica in docs/index.html.
"""

from __future__ import annotations

import json
import re
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
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"OK: {OUT} ({OUT.stat().st_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
