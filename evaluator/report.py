from pathlib import Path


def write_report(candidate: str, rows: list[dict], target: Path) -> None:
    target.parent.mkdir(exist_ok=True)
    lines = [
        f"# Evaluation report: {candidate}", "",
        "Score = round(100 × passed / (passed + failed)). Collection errors invalidate the run.",
        "Only observed test outcomes are scored; human review remains necessary.", "",
        "| Task | Passed | Failed | Errors | Score |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(f"| {row['task']} | {row['passed']} | {row['failed']} | {row['errors']} | {row['score']}/100 |")
    lines += ["", "## Failed tests", ""]
    for row in rows:
        lines.append(f"### {row['task']}")
        lines.extend(f"- `{name}`" for name in row["failed_tests"])
        if not row["failed_tests"]:
            lines.append("- None")
        lines.append("")
    target.write_text("\n".join(lines), encoding="utf-8")
