from __future__ import annotations

import argparse
from pathlib import Path

from common import repo_root


REPLACEMENTS = (
    ("{PKMN}", "Vasaskrímsli"),
    ("POKéMON", "Vasaskrímsli"),
    ("POKEMON", "Vasaskrímsli"),
    ("Pokémon", "Vasaskrímsli"),
    ("Pokemon", "Vasaskrímsli"),
)


TEXT_GLOBS = (
    "src/**/*.c",
    "src/**/*.h",
    "data/maps/**/text.inc",
    "data/scripts/**/*.inc",
    "data/text/**/*.inc",
    "data/mystery_event_msg.s",
)


def replace_terms(value: str) -> str:
    for old, new in REPLACEMENTS:
        value = value.replace(old, new)
    return value


def replace_inside_quoted_strings(text: str) -> tuple[str, int]:
    out: list[str] = []
    current: list[str] = []
    in_string = False
    escaped = False
    replacements = 0

    for char in text:
        if not in_string:
            out.append(char)
            if char == '"':
                in_string = True
                current = []
                escaped = False
            continue

        if escaped:
            current.append(char)
            escaped = False
            continue

        if char == "\\":
            current.append(char)
            escaped = True
            continue

        if char == '"':
            original = "".join(current)
            replaced = replace_terms(original)
            if replaced != original:
                replacements += sum(original.count(old) for old, _ in REPLACEMENTS)
            out.append(replaced)
            out.append(char)
            in_string = False
            current = []
            continue

        current.append(char)

    if in_string:
        out.extend(current)
    return "".join(out), replacements


def iter_text_files(root: Path) -> list[Path]:
    files: set[Path] = set()
    for pattern in TEXT_GLOBS:
        files.update(path for path in root.glob(pattern) if path.is_file())
    files.add(root / "src/data/items.json")
    return sorted(files)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args()

    total_files = 0
    total_replacements = 0
    for path in iter_text_files(args.root):
        text = path.read_text(encoding="utf-8")
        new_text, replacements = replace_inside_quoted_strings(text)
        if replacements == 0:
            continue
        path.write_text(new_text, encoding="utf-8", newline="\n")
        total_files += 1
        total_replacements += replacements
        print(f"{path.relative_to(args.root)}: {replacements}")

    print(f"files={total_files} replacements={total_replacements}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
