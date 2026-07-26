from __future__ import annotations

import argparse
import csv
from pathlib import Path


TEXT_CSVS = [
    "battle_text_is.csv",
    "menu_text_is.csv",
    "dialogue_text_is.csv",
    "map_names_is.csv",
    "move_descriptions_is.csv",
    "ability_descriptions_is.csv",
    "pokedex_descriptions_is.csv",
    "pokedex_habitat_is.csv",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    args.report.parent.mkdir(parents=True, exist_ok=True)

    rows_out: list[dict[str, str | int]] = []
    for csv_name in TEXT_CSVS:
        path = args.csv_dir / csv_name
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        translated = sum(1 for row in rows if (row.get("icelandic") or "").strip())
        by_anchor: dict[str, tuple[int, int]] = {}
        for row in rows:
            anchor = row.get("source_anchor") or row.get("note") or "unknown"
            total, done = by_anchor.get(anchor, (0, 0))
            by_anchor[anchor] = (total + 1, done + (1 if (row.get("icelandic") or "").strip() else 0))
        rows_out.append({"csv": csv_name, "source_anchor": "ALL", "total": len(rows), "translated": translated, "blank": len(rows) - translated})
        for anchor, (total, done) in sorted(by_anchor.items()):
            rows_out.append({"csv": csv_name, "source_anchor": anchor, "total": total, "translated": done, "blank": total - done})

    with args.report.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["csv", "source_anchor", "total", "translated", "blank"])
        writer.writeheader()
        writer.writerows(rows_out)
    print(f"wrote {args.report}")


if __name__ == "__main__":
    main()
