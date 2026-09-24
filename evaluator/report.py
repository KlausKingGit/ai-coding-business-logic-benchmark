from pathlib import Path


def write_report(rows: list[dict], target: Path) -> None:
    lines = ["# Evaluation report", "", "Scores measure only automated test outcomes. Review evaluation_notes.md for engineering judgment.", "", "| Task | Passed | Failed | Score |", "|---|---:|---:|---:|"]
    for row in rows:
        lines.append(f"| {row['task']} | {row['passed']} | {row['failed']} | {row['score']}/100 |")
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
