from __future__ import annotations

import argparse
import csv
from pathlib import Path

from common import FIXED_TABLES, game_len, load_csv_rows, mapped_chars, repo_root, row_issues, row_translation


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args()

    chars = mapped_chars(args.root)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    report_rows: list[dict[str, str | int]] = []
    fatal_unsupported: list[dict[str, str | int]] = []

    for table in FIXED_TABLES:
        for row in load_csv_rows(args.csv_dir, table):
            value = row_translation(row)
            if not value:
                continue
            issues = row_issues(row, table, chars)
            for issue in issues:
                report_row = {
                    "category": table.category,
                    "index": row.get("index", ""),
                    "original": row.get("original", ""),
                    "icelandic": value,
                    "limit": table.limit,
                    "length": game_len(value),
                    "issue": issue,
                }
                report_rows.append(report_row)
                if (
                    issue.startswith("unsupported:")
                    and game_len(value) <= table.limit
                    and value != row.get("original", "")
                ):
                    fatal_unsupported.append(report_row)

    with args.report.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["category", "index", "original", "icelandic", "limit", "length", "issue"])
        writer.writeheader()
        writer.writerows(report_rows)

    by_category: dict[str, int] = {}
    for row in report_rows:
        by_category[row["category"]] = by_category.get(row["category"], 0) + 1
    print(f"wrote {args.report}")
    for category, count in sorted(by_category.items()):
        print(f"{category}: {count} issues")
    if fatal_unsupported:
        print(f"fatal unsupported rows: {len(fatal_unsupported)}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
