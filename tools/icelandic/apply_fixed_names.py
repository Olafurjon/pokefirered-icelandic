from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from common import FIXED_TABLES, FixedTable, c_escape, load_csv_rows, mapped_chars, repo_root, row_issues, row_translation


ENTRY_RE = re.compile(r'(?P<prefix>\[[^\]]+\]\s*=\s*_\(")(?P<text>(?:\\.|[^"\\])*)(?P<suffix>"\),)')


def source_region(text: str, marker: str | None) -> tuple[str, str]:
    if marker is None:
        return "", text
    index = text.index(marker)
    return text[:index], text[index:]


def apply_c_array(root: Path, csv_dir: Path, table: FixedTable, chars: set[str]) -> tuple[int, int]:
    path = root / table.source_path
    original_text = path.read_text(encoding="utf-8")
    prefix, region = source_region(original_text, table.marker)
    matches = list(ENTRY_RE.finditer(region))
    rows = load_csv_rows(csv_dir, table)
    applied = 0
    skipped = 0
    replacements: dict[int, str] = {}

    for row in rows:
        value = row_translation(row)
        if not value or value == row.get("original", ""):
            continue
        issues = [issue for issue in row_issues(row, table, chars) if issue != "blank"]
        if issues:
            skipped += 1
            continue
        try:
            index = int(row["index"]) - 1 + table.entry_offset
        except (KeyError, ValueError):
            skipped += 1
            continue
        if index < 0 or index >= len(matches):
            skipped += 1
            continue
        replacements[index] = c_escape(value)

    pieces: list[str] = []
    last = 0
    for idx, match in enumerate(matches):
        pieces.append(region[last:match.start()])
        if idx in replacements:
            pieces.append(match.group("prefix") + replacements[idx] + match.group("suffix"))
            applied += 1
        else:
            pieces.append(match.group(0))
        last = match.end()
    pieces.append(region[last:])
    new_text = prefix + "".join(pieces)
    if new_text != original_text:
        path.write_text(new_text, encoding="utf-8", newline="\n")
    return applied, skipped


def apply_items(root: Path, csv_dir: Path, table: FixedTable, chars: set[str]) -> tuple[int, int]:
    path = root / table.source_path
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = load_csv_rows(csv_dir, table)
    applied = 0
    skipped = 0
    items = data["items"]

    for row in rows:
        value = row_translation(row)
        if not value or value == row.get("original", ""):
            continue
        issues = [issue for issue in row_issues(row, table, chars) if issue != "blank"]
        if issues:
            skipped += 1
            continue
        try:
            index = int(row["index"])
        except (KeyError, ValueError):
            skipped += 1
            continue
        if index <= 0 or index >= len(items):
            skipped += 1
            continue
        if items[index].get("english") != value:
            items[index]["english"] = value
            applied += 1

    if applied:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return applied, skipped


def run_validator(root: Path, csv_dir: Path, report: Path) -> None:
    cmd = [
        sys.executable,
        str(root / "tools/icelandic/validate_translations.py"),
        "--csv-dir",
        str(csv_dir),
        "--report",
        str(report),
        "--root",
        str(root),
    ]
    subprocess.run(cmd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args()

    run_validator(args.root, args.csv_dir, args.report)
    chars = mapped_chars(args.root)
    for table in FIXED_TABLES:
        if table.category == "items":
            applied, skipped = apply_items(args.root, args.csv_dir, table, chars)
        else:
            applied, skipped = apply_c_array(args.root, args.csv_dir, table, chars)
        print(f"{table.category}: applied={applied} skipped={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

