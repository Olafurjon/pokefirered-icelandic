from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
from pathlib import Path

from common import repo_root


ASM_STRING_RE = re.compile(r'^([ \t]*)\.string\s+"((?:\\.|[^"\\])*)"\s*$')
C_STRING_RE = re.compile(r'"((?:\\.|[^"\\])*)"')
C_SYMBOL_RE = re.compile(r'\b(?:const|static const)\s+u8\s+([A-Za-z0-9_]+)')
NON_VISIBLE_C_STRING_RE = re.compile(r"^[A-Za-z0-9_./-]+\.(?:h|inc|c|s)$")
ACCEPTED_UNCHANGED_RE = re.compile(
    r"^(?:"
    r"TM\d{0,2}|HM\d{0,2}|FNT|[BF]?\d{1,2}F|B\d{1,2}F|"
    r"OK!?|HP|PP|ID|Lv|TIME|EGG|KANTO|SEPIA|VERMILION|GAME FREAK|"
    r"S\.S\. ANNE|BILL|DAISY|FUJI|OAK|"
    r"ARCHIE|MAXIE|LT\. SURGE|KOGA|"
    r"Mew!|Ha\?|Arr+gh!|……|‥ ‥ ‥ ‥ ‥!|"
    r"\?{2,5}|-+|[.!?:/▶♂♀×+%¥]|"
    r"\d+:|10P\s+30P\s+50P\s+\{EMOJI_MINUS\}50P|L=A|LR|"
    r"OAK: \{PLAYER\}!|'s|"
    r"¥\{STR_VAR_1\}|\{[^}]+\}|"
    r"\{A_BUTTON\}OK|\{NO\}\{CLEAR 0x01\}|\{ID\}\{NO\}|×\{STR_VAR_1\}|"
    r"\{STR_VAR_1\}\.\{STR_VAR_2\}|\{STR_VAR_1\}%|"
    r"\{FONT_SMALL\}(?:\{PLUS\}|-)\{FONT_NORMAL\}|"
    r"\{PALETTE 5\}\{COLOR_HIGHLIGHT_SHADOW 13 14 15\}|"
    r"1\. (?:\{COLOR BLUE\}\{SHADOW LIGHT_BLUE\})?\{DYNAMIC 0x00\}|"
    r"\{(?:NO|ID|PP|LV_2|PLUS|RIGHT_ARROW_2|PAUSE_UNTIL_PRESS|FONT_SMALL|FONT_NORMAL|ESCAPE 0x03)\}"
    r")$"
)
ENGLISH_WORD_RE = re.compile(
    r"\b("
    r"the|you|your|this|that|with|from|please|choose|want|not|can|will|"
    r"save|game|button|press|cancel|there|have|which|where|battle|attack|"
    r"move|item|mail|waiting|friend|other|trainer|pokemon|pok[eé]mon|bag|"
    r"mart|center|city|route|island|prof|oak|mom|mother|catch|caught|wild|"
    r"use|used|select|open|close|menu|check|help|card|news|wonder|berry|"
    r"powder|secret|key|ticket|pass|went|bought|spent|switched|traded|"
    r"obtained|received|restored|defeated|leader|elite|four|journal|feature|"
    r"room|trade|communication|available|ready|level|type|power|points|effect|"
    r"foe|enemy|damage|target|user|turn|turns|stat|stats|is|are|was|were|"
    r"has|had|for|and|or|in|on|at"
    r")\b",
    re.IGNORECASE,
)

ASM_GLOBS = [
    "data/maps/**/text.inc",
    "data/text/*.inc",
    "data/scripts/*.inc",
    "data/mystery_event_msg.s",
]

C_FILES = [
    "src/data/text/abilities.h",
    "src/move_descriptions.c",
    "src/data/pokemon/pokedex_text_fr.h",
    "src/data/pokemon/pokedex_text_lg.h",
    "src/data/text/quest_log.h",
    "src/data/text/teachy_tv.h",
    "src/battle_message.c",
    "src/strings.c",
    "src/mystery_event_msg.c",
    "src/union_room_message.c",
]


def git_head_text(root: Path, path: Path) -> str:
    rel = path.relative_to(root).as_posix()
    try:
        return subprocess.check_output(["git", "show", f"HEAD:{rel}"], cwd=root, text=True, encoding="utf-8")
    except subprocess.CalledProcessError:
        return ""


def compact_control_text(text: str) -> str:
    return text.replace(r"\n", "\n").replace(r"\p", "\n\n").replace(r"\l", "\n")


def extract_asm_blocks(text: str) -> list[dict[str, str | int]]:
    lines = text.splitlines()
    rows: list[dict[str, str | int]] = []
    label = ""
    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped.endswith("::"):
            label = stripped[:-2]
        match = ASM_STRING_RE.match(lines[index])
        if not match:
            index += 1
            continue
        start_line = index + 1
        parts: list[str] = []
        while index < len(lines):
            match = ASM_STRING_RE.match(lines[index])
            if not match:
                break
            parts.append(match.group(2))
            index += 1
        rows.append({
            "line": start_line,
            "label": label,
            "text": compact_control_text("".join(parts).rstrip("$")),
        })
    return rows


def extract_c_strings(text: str) -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    current_symbol = ""
    for line_no, line in enumerate(text.splitlines(), start=1):
        symbol_match = C_SYMBOL_RE.search(line)
        if symbol_match:
            current_symbol = symbol_match.group(1)
        for match in C_STRING_RE.finditer(line):
            value = match.group(1)
            if not value.strip() or value.startswith(("data/", "graphics/", "sound/", "constants/")):
                continue
            if NON_VISIBLE_C_STRING_RE.fullmatch(value.strip()):
                continue
            rows.append({
                "line": line_no,
                "label": current_symbol or f"line_{line_no}",
                "text": compact_control_text(value.rstrip("$")),
            })
    return rows


def extract_items(text: str) -> list[dict[str, str | int]]:
    data = json.loads(text)
    rows: list[dict[str, str | int]] = []
    for index, item in enumerate(data["items"]):
        item_id = item.get("itemId") or f"item_{index}"
        for key in ("english", "description_english"):
            value = item.get(key)
            if isinstance(value, str) and value.strip() and set(value.strip()) != {"?"}:
                rows.append({
                    "line": index,
                    "label": f"{item_id}.{key}",
                    "text": compact_control_text(value),
                })
    return rows


def keyed(rows: list[dict[str, str | int]]) -> dict[str, dict[str, str | int]]:
    return {str(row["label"]): row for row in rows}


def row_kind(source: str, current: str) -> str:
    if ACCEPTED_UNCHANGED_RE.fullmatch(current.strip()):
        return "machine_draft_or_terms"
    if current == source:
        return "untranslated"
    if ENGLISH_WORD_RE.search(current):
        return "term_replaced_or_partial"
    if any(ord(ch) > 127 for ch in current):
        return "machine_draft_or_terms"
    if not ENGLISH_WORD_RE.search(current):
        return "machine_draft_or_terms"
    return "term_replaced_or_partial"


def collect_rows(root: Path) -> list[dict[str, str]]:
    files: set[Path] = set()
    for pattern in ASM_GLOBS:
        files.update(path for path in root.glob(pattern) if path.is_file())
    files.update(root / rel for rel in C_FILES if (root / rel).exists())
    files.add(root / "src/data/items.json")

    out: list[dict[str, str]] = []
    for path in sorted(files):
        current_text = path.read_text(encoding="utf-8")
        source_text = git_head_text(root, path) or current_text
        if path.name == "items.json":
            source_rows = keyed(extract_items(source_text))
            current_rows = keyed(extract_items(current_text))
        elif path.suffix in {".inc", ".s"}:
            source_rows = keyed(extract_asm_blocks(source_text))
            current_rows = keyed(extract_asm_blocks(current_text))
        else:
            source_rows = keyed(extract_c_strings(source_text))
            current_rows = keyed(extract_c_strings(current_text))

        for label, current in current_rows.items():
            source = source_rows.get(label, current)
            source_value = str(source["text"])
            current_value = str(current["text"])
            if not source_value.strip() or source_value == "?????":
                continue
            kind = row_kind(source_value, current_value)
            if kind == "untranslated":
                is_proper_name_row = (
                    label.startswith("gNameChoice_")
                    or label.startswith("gFameCheckerFlavorTextOriginObjectName_")
                )
                if is_proper_name_row and re.fullmatch(r"[A-Z][A-Z .'-]*", current_value.strip()):
                    kind = "machine_draft_or_terms"
            out.append({
                "file": path.relative_to(root).as_posix(),
                "line": str(current["line"]),
                "label": label,
                "kind": kind,
                "source_english": source_value,
                "current_text": current_value,
                "icelandic": "",
                "notes": "",
            })
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--output", type=Path, default=repo_root() / "translation_reports/manual_translation_queue.csv")
    args = parser.parse_args()

    rows = collect_rows(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["file", "line", "label", "kind", "source_english", "current_text", "icelandic", "notes"],
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {args.output} rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
