from __future__ import annotations

import argparse
import csv
import json
import re
import textwrap
from pathlib import Path

from common import mapped_chars, repo_root


ASM_STRING_RE = re.compile(r'(?P<prefix>\.string\s+")(?P<text>(?:\\.|[^"\\])*)(?P<suffix>")')
C_STRING_RE = re.compile(r'"(?P<text>(?:\\.|[^"\\])*)"')

DISPLAY_GLOBS = [
    "data/maps/**/text.inc",
    "data/text/*.inc",
    "data/scripts/*.inc",
    "data/mystery_event_msg.s",
    "src/data/pokemon/pokedex_text_fr.h",
    "src/data/pokemon/pokedex_text_lg.h",
    "src/data/text/*.h",
    "src/move_descriptions.c",
    "src/battle_message.c",
    "src/strings.c",
    "src/mystery_event_msg.c",
    "src/union_room_message.c",
    "src/data/decoration/description.h",
    "src/trainer_tower_sets.c",
]


def load_species_terms(csv_dir: Path) -> list[tuple[re.Pattern[str], str]]:
    terms: list[tuple[str, str]] = []
    with (csv_dir / "species_is.csv").open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            original = (row.get("original") or "").strip()
            icelandic = (row.get("icelandic") or "").strip()
            if not original or not icelandic:
                continue
            terms.append((original, icelandic))

    compiled: list[tuple[re.Pattern[str], str]] = []
    for original, icelandic in sorted(terms, key=lambda item: len(item[0]), reverse=True):
        pattern = re.compile(rf"(?<![A-Za-zÁÉÍÓÚÝÞÆÖÐáéíóúýþæöð]){re.escape(original)}(?![A-Za-zÁÉÍÓÚÝÞÆÖÐáéíóúýþæöð])")
        compiled.append((pattern, icelandic.upper()))
    return compiled


def explicit_terms() -> list[tuple[re.Pattern[str], str]]:
    pairs = [
        ("BOULDERBADGE", "STEINMERKIÐ"),
        ("BOULDER BADGE", "STEINMERKIÐ"),
        ("CASCADEBADGE", "FOSSMERKIÐ"),
        ("CASCADE BADGE", "FOSSMERKIÐ"),
        ("THUNDERBADGE", "ÞRUMUMERKIÐ"),
        ("THUNDER BADGE", "ÞRUMUMERKIÐ"),
        ("HELIX FOSSIL", "SPÍRALGERVING"),
        ("DOME FOSSIL", "HVOLFGERVING"),
        ("ROOT FOSSIL", "RÓTARGERVING"),
        ("CLAW FOSSIL", "KLÓGERVING"),
        ("OLD ROD", "GÖMUL STÖNG"),
        ("BIKE VOUCHER", "REIÐHJÓLSMIÐI"),
        ("FAME CHECKER", "FRÆGÐARSJÁ"),
        ("VS SEEKER", "VS LEITARI"),
        ("TRI-PASS", "ÞRÍPASSI"),
        ("RAINBOW PASS", "REGNBOGAPASSI"),
        ("S.S. TICKET", "S.S. MIÐI"),
        ("S♀S♀ TICKET", "S.S. MIÐI"),
        ("S♀S♀ MIÐI", "S.S. MIÐI"),
        ("POKéDEX", "VasaDEX"),
        ("POKÉDEX", "VasaDEX"),
        ("POKEDEX", "VasaDEX"),
        ("POKé BALLS", "VASA BOLTAR"),
        ("POKé BALL", "VASA BOLTI"),
        ("POKÉ BALLS", "VASA BOLTAR"),
        ("POKÉ BALL", "VASA BOLTI"),
        ("POKÉBOLTI", "VASABOLTI"),
        ("POKéMON", "VASaSKRÍMSLI"),
        ("POKEMON", "VASASKRÍMSLI"),
        ("{PKMN}", "VASaSKRÍMSLI"),
    ]
    return [(re.compile(re.escape(source)), target) for source, target in pairs]


def replace_terms(text: str, terms: list[tuple[re.Pattern[str], str]]) -> str:
    for pattern, target in terms:
        text = pattern.sub(target, text)
    return text


def transform_c_like_text(text: str, terms: list[tuple[re.Pattern[str], str]]) -> tuple[str, int]:
    changed = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal changed
        value = match.group("text")
        if value.startswith(("data/", "graphics/", "sound/")):
            return match.group(0)
        new_value = replace_terms(value, terms)
        if new_value != value:
            changed += 1
        return '"' + new_value + '"'

    return C_STRING_RE.sub(repl, text), changed


def transform_asm_text(text: str, terms: list[tuple[re.Pattern[str], str]]) -> tuple[str, int]:
    changed = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal changed
        value = match.group("text")
        new_value = replace_terms(value, terms)
        if new_value != value:
            changed += 1
        return match.group("prefix") + new_value + match.group("suffix")

    return ASM_STRING_RE.sub(repl, text), changed


def transform_items_json(path: Path, terms: list[tuple[re.Pattern[str], str]]) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = 0
    for item in data["items"]:
        for key in ("english", "description_english"):
            value = item.get(key)
            if not isinstance(value, str):
                continue
            new_value = replace_terms(value, terms)
            if key == "description_english" and new_value.strip() and set(new_value.strip()) != {"?"}:
                paragraph = " ".join(new_value.replace(r"\n", " ").split())
                new_value = r"\n".join(textwrap.wrap(paragraph, width=34, break_long_words=False, break_on_hyphens=False))
            if new_value != value:
                item[key] = new_value
                changed += 1
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return changed


def iter_default_files(root: Path) -> list[Path]:
    files: set[Path] = set()
    for pattern in DISPLAY_GLOBS:
        files.update(path for path in root.glob(pattern) if path.is_file())
    files.add(root / "src/data/items.json")
    return sorted(path for path in files if path.exists())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--csv-dir", type=Path, required=True)
    parser.add_argument("--path", action="append", default=[])
    args = parser.parse_args()

    chars = mapped_chars(args.root)
    terms = explicit_terms() + load_species_terms(args.csv_dir)
    files = [args.root / path for path in args.path] if args.path else iter_default_files(args.root)

    files_changed = 0
    replacements = 0
    for path in files:
        if path.name == "items.json":
            changed = transform_items_json(path, terms)
        else:
            text = path.read_text(encoding="utf-8")
            if path.suffix in {".inc", ".s"}:
                new_text, changed = transform_asm_text(text, terms)
            else:
                new_text, changed = transform_c_like_text(text, terms)
            if new_text != text:
                missing = sorted({char for char in new_text if ord(char) > 127 and char not in chars})
                if missing:
                    raise SystemExit(f"{path}: unsupported characters after term replacement: {missing}")
                path.write_text(new_text, encoding="utf-8", newline="\n")
        if changed:
            files_changed += 1
            replacements += changed
            print(f"{path.relative_to(args.root)}: replacements={changed}")

    print(f"files_changed={files_changed} replacements={replacements}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
