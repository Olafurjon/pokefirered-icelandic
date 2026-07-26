from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path


ICELANDIC_GLYPHS = {
    "Þ": 0x38,
    "þ": 0x39,
    "Æ": 0x3A,
    "æ": 0x3B,
    "Ð": 0x3C,
    "ð": 0x3D,
    "Ý": 0x3E,
    "ý": 0x3F,
}


@dataclass(frozen=True)
class FixedTable:
    category: str
    csv_name: str
    limit: int
    source_path: str
    entry_offset: int
    marker: str | None = None


FIXED_TABLES = [
    FixedTable("species", "species_is.csv", 15, "src/data/text/species_names.h", 1),
    FixedTable("moves", "moves_is_updated.csv", 12, "src/data/text/move_names.h", 1),
    FixedTable("abilities", "abilities_is_updated.csv", 12, "src/data/text/abilities.h", 1, "const u8 gAbilityNames"),
    FixedTable("trainer_classes", "trainer_classes_is_updated.csv", 12, "src/data/text/trainer_class_names.h", 0),
    FixedTable("types", "types_is_updated.csv", 6, "src/battle_main.c", 0, "const u8 gTypeNames"),
    FixedTable("items", "items_is_updated.csv", 14, "src/data/items.json", 1),
]


TOKEN_RE = re.compile(r"(\{[A-Z0-9_]+\}|\\[npl]|\\l|\\p|\\n|\[U\+[0-9A-Fa-f]{2}\])")
CHARMAP_LITERAL_RE = re.compile(r"'((?:\\'|.)+)'\s*=")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_csv_rows(csv_dir: Path, table: FixedTable) -> list[dict[str, str]]:
    with (csv_dir / table.csv_name).open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def mapped_chars(root: Path) -> set[str]:
    text = (root / "charmap.txt").read_text(encoding="utf-8")
    chars: set[str] = set()
    for line in text.splitlines():
        match = CHARMAP_LITERAL_RE.match(line.strip())
        if not match:
            continue
        value = match.group(1).replace("\\'", "'")
        if len(value) == 1:
            chars.add(value)
    return chars


def literal_chars(text: str) -> list[str]:
    cleaned = TOKEN_RE.sub("", text)
    return [char for char in cleaned]


def game_len(text: str) -> int:
    length = 0
    pos = 0
    for match in TOKEN_RE.finditer(text):
        length += len(text[pos:match.start()])
        token = match.group(0)
        length += 1 if token.startswith("[U+") else 2 if token == "{PKMN}" else 1
        pos = match.end()
    length += len(text[pos:])
    return length


def is_placeholder(text: str) -> bool:
    stripped = text.replace(" ", "")
    return bool(stripped) and set(stripped) <= {"?"}


def row_translation(row: dict[str, str]) -> str:
    return (row.get("icelandic") or "").strip()


def c_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def row_issues(row: dict[str, str], table: FixedTable, chars: set[str]) -> list[str]:
    value = row_translation(row)
    if not value:
        return ["blank"]
    issues: list[str] = []
    if is_placeholder(value):
        issues.append("placeholder")
    length = game_len(value)
    if length > table.limit:
        issues.append(f"over_limit:{length}>{table.limit}")
    missing = sorted({char for char in literal_chars(value) if char not in chars})
    if missing:
        issues.append("unsupported:" + "".join(missing))
    return issues


def safe_to_apply(row: dict[str, str], table: FixedTable, chars: set[str]) -> bool:
    issues = row_issues(row, table, chars)
    return not issues or issues == []
