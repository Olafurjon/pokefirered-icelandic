from __future__ import annotations

import argparse
import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

from common import repo_root


CONTROL_RE = re.compile(
    r"(\{[^}]+\}|\\[npl]|\\x[0-9A-Fa-f]{2}|\\[0-7]{1,3}|\[[A-Z0-9_ +.-]+\])"
)
CJK_RE = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
LETTER_RE = re.compile(r"[A-Za-zÁÉÍÓÚÝÞÆÖÐáéíóúýþæöð]")
LOWER_RE = re.compile(r"[a-záéíóúýþæöð]")
ALL_CAPS_WORD_RE = re.compile(r"(?<![A-Za-zÁÉÍÓÚÝÞÆÖÐáéíóúýþæöð])([A-ZÁÉÍÓÚÝÞÆÖÐ0-9][A-ZÁÉÍÓÚÝÞÆÖÐ0-9.'-]{1,})(?![A-Za-zÁÉÍÓÚÝÞÆÖÐáéíóúýþæöð])")
STRING_LITERAL_RE = re.compile(r'"((?:\\.|[^"\\])*)"')
CONCAT_MACRO_RE = re.compile(r'_\(\s*((?:"(?:\\.|[^"\\])*"\s*)+)\)', re.DOTALL)
ASM_STRING_RE = re.compile(r'^([ \t]*)\.string\s+"((?:\\.|[^"\\])*)"\s*$')

PROTECTED_TERMS = [
    "Vasaskrímsli",
    "VASASKRÍMSLI",
    "VASaSKRÍMSLI",
    "POKéMON",
    "POKEMON",
    "POKéDEXES",
    "POKéDEX",
    "POKé BALLS",
    "POKé BALL",
    "POKé",
    "HP",
    "PP",
    "EXP",
    "TM",
    "HM",
    "PC",
    "ID",
    "LV",
    "ATTACK",
    "DEFENSE",
    "SPEED",
    "SP. ATK",
    "SP. DEF",
    "SP. DEFENSE",
    "ACCURACY",
    "EVASION",
    "POISON",
    "PARALYSIS",
    "BURN",
    "SLEEP",
    "FREEZE",
]

NORMALIZE_REPLACEMENTS = {
    "Pokémon": "Vasaskrímsli",
    "POKéMON": "VASaSKRÍMSLI",
    "Pokemon": "Vasaskrímsli",
    "POKEMON": "VASASKRÍMSLI",
    "{PKMN}": "VASaSKRÍMSLI",
    "“": "'",
    "”": "'",
    "„": "'",
    "’": "'",
    "‘": "'",
    "–": "-",
    "—": "-",
    "\u200b": "",
    "\u200c": "",
    "\u200d": "",
    "\ufeff": "",
}

CORE_TEXT_FILES = [
    "src/strings.c",
    "src/battle_message.c",
    "src/move_descriptions.c",
    "src/mystery_event_msg.c",
    "src/union_room_message.c",
    "src/data/text/abilities.h",
    "src/data/text/quest_log.h",
    "src/data/text/teachy_tv.h",
    "src/data/pokemon/pokedex_text_fr.h",
    "src/data/pokemon/pokedex_text_lg.h",
    "src/data/region_map/region_map_entry_strings.h",
    "data/mystery_event_msg.s",
]

CORE_TEXT_GLOBS = [
    "data/text/*.inc",
    "data/scripts/*.inc",
]

MAP_TEXT_GLOBS = [
    "data/maps/**/text.inc",
]


@dataclass
class Stats:
    files_changed: int = 0
    strings_changed: int = 0
    strings_seen: int = 0
    strings_skipped: int = 0


@dataclass
class RunContext:
    cache_path: Path
    cache: dict[str, str]
    progress_every: int
    retry_identical_cache: bool = False
    refresh_cache: bool = False
    translated_requests: int = 0

    def save_cache(self) -> None:
        self.cache_path.write_text(
            json.dumps(self.cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )


class Translator:
    def __init__(self, timeout: float) -> None:
        self.timeout = timeout

    def translate(self, text: str) -> str:
        query = urlencode({
            "client": "gtx",
            "sl": "en",
            "tl": "is",
            "dt": "t",
            "q": text,
        })
        url = f"https://translate.googleapis.com/translate_a/single?{query}"
        with urlopen(url, timeout=self.timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return "".join(part[0] for part in payload[0] if part and part[0])


def normalize_text(text: str) -> str:
    for old, new in NORMALIZE_REPLACEMENTS.items():
        text = text.replace(old, new)
    return text


def protect_text(text: str) -> tuple[str, dict[str, str]]:
    replacements: dict[str, str] = {}

    def put(value: str, prefix: str) -> str:
        key = f"ZX{prefix}{len(replacements)}XZ"
        replacements[key] = value
        return key

    def repl_control(match: re.Match[str]) -> str:
        return put(match.group(0), "C")

    text = CONTROL_RE.sub(repl_control, text)
    for term in sorted(PROTECTED_TERMS, key=len, reverse=True):
        text = re.sub(rf"\b{re.escape(term)}\b", lambda m: put(m.group(0), "T"), text)

    def repl_caps(match: re.Match[str]) -> str:
        value = match.group(0)
        if value.startswith("ZX") and value.endswith("XZ"):
            return value
        if LOWER_RE.search(value):
            return value
        if not any(char.isalpha() for char in value):
            return value
        return put(value, "U")

    text = ALL_CAPS_WORD_RE.sub(repl_caps, text)
    return text, replacements


def restore_text(text: str, replacements: dict[str, str]) -> str:
    for _ in range(len(replacements) + 1):
        changed = False
        for key, value in replacements.items():
            if key in text:
                text = text.replace(key, value)
                changed = True
        if not changed:
            break
    return normalize_text(text)


def split_outer_space(text: str) -> tuple[str, str, str]:
    start = len(text) - len(text.lstrip())
    end = len(text.rstrip())
    return text[:start], text[start:end], text[end:]


def should_translate(text: str) -> bool:
    if not text.strip():
        return False
    if CJK_RE.search(text):
        return False
    if not LETTER_RE.search(text):
        return False
    stripped = text.strip()
    if stripped.startswith("data/"):
        return False
    if "/" in stripped and " " not in stripped:
        return False
    if stripped.endswith((".h", ".inc", ".s", ".c", ".json", ".png", ".4bpp", ".pal")):
        return False
    return True


def cache_key(text: str) -> str:
    return normalize_text(text.strip())


def translate_segment(text: str, translator: Translator, ctx: RunContext, delay: float) -> str:
    leading, core, trailing = split_outer_space(normalize_text(text))
    if not should_translate(core):
        return text

    key = cache_key(core)
    if (
        key in ctx.cache
        and not ctx.refresh_cache
        and not (ctx.retry_identical_cache and ctx.cache[key] == key)
    ):
        return leading + ctx.cache[key] + trailing

    protected, replacements = protect_text(core)
    try:
        translated = translator.translate(protected)
    except Exception as exc:  # Keep source text and report through stderr-ish print.
        print(f"translate failed: {core!r}: {exc}")
        ctx.cache[key] = core
        ctx.save_cache()
        return text

    if delay:
        time.sleep(delay)
    translated = restore_text(translated, replacements)
    ctx.cache[key] = translated
    ctx.translated_requests += 1
    if ctx.progress_every and ctx.translated_requests % ctx.progress_every == 0:
        print(f"translated_requests={ctx.translated_requests} cache_entries={len(ctx.cache)}", flush=True)
    ctx.save_cache()
    return leading + translated + trailing


def translate_literal(raw: str, translator: Translator, ctx: RunContext, delay: float) -> tuple[str, bool]:
    translated = translate_segment(raw, translator, ctx, delay)
    return translated, translated != raw


def transform_quoted_strings(text: str, translator: Translator, ctx: RunContext, delay: float) -> tuple[str, Stats]:
    out: list[str] = []
    current: list[str] = []
    in_string = False
    escaped = False
    stats = Stats()

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
            raw = "".join(current)
            stats.strings_seen += 1
            translated, changed = translate_literal(raw, translator, ctx, delay)
            if changed:
                stats.strings_changed += 1
            else:
                stats.strings_skipped += 1
            out.append(translated)
            out.append(char)
            in_string = False
            current = []
            continue

        current.append(char)

    if in_string:
        out.extend(current)
    return "".join(out), stats


def c_block_to_paragraph(block: str) -> str:
    raw = "".join(match.group(1) for match in STRING_LITERAL_RE.finditer(block))
    raw = re.sub(r"\\[npl]", " ", raw)
    return re.sub(r"\s+", " ", raw).strip()


def wrap_words(text: str, width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        if not current:
            current = word
            continue
        if len(current) + 1 + len(word) <= width:
            current += " " + word
            continue
        lines.append(current)
        current = word
    if current:
        lines.append(current)
    return lines or [""]


def escape_c_literal(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def format_concat_macro(lines: list[str], indent: str) -> str:
    rendered = "_(\n"
    for index, line in enumerate(lines):
        suffix = r"\n" if index < len(lines) - 1 else ""
        rendered += f'{indent}"{escape_c_literal(line)}{suffix}"'
        if index < len(lines) - 1:
            rendered += "\n"
    return rendered + ")"


def plain_asm_text(raw: str) -> str:
    body = raw[:-1] if raw.endswith("$") else raw
    body = re.sub(r"\\[npl]", " ", body)
    return re.sub(r"\s+", " ", body).strip()


def should_skip_asm_block(label: str | None, raw: str) -> bool:
    text = plain_asm_text(raw)
    if not should_translate(text):
        return True
    if label and "NameChoice" in label:
        return True
    letters = re.sub(r"[^A-Za-z]", "", text)
    if letters and letters.upper() == letters and len(text) <= 14:
        return True
    return False


def translate_asm_page(page: str, translator: Translator, ctx: RunContext, delay: float) -> str:
    paragraph = re.sub(r"\\[nl]", " ", page)
    paragraph = re.sub(r"\s+", " ", normalize_text(paragraph)).strip()
    if not should_translate(paragraph):
        return paragraph
    return translate_segment(paragraph, translator, ctx, delay)


def format_asm_string_block(
    translated_pages: list[str],
    indent: str,
    wrap_width: int,
    lines_per_page: int,
) -> list[str]:
    units: list[tuple[str, str]] = []
    for page_index, page in enumerate(translated_pages):
        wrapped = wrap_words(page, wrap_width)
        chunks = [
            wrapped[index : index + lines_per_page]
            for index in range(0, len(wrapped), lines_per_page)
        ]
        for chunk_index, chunk in enumerate(chunks):
            for line_index, line in enumerate(chunk):
                is_last_page = page_index == len(translated_pages) - 1
                is_last_chunk = chunk_index == len(chunks) - 1
                is_last_line = line_index == len(chunk) - 1
                if is_last_page and is_last_chunk and is_last_line:
                    suffix = "$"
                elif is_last_line:
                    suffix = r"\p"
                else:
                    suffix = r"\n"
                units.append((line, suffix))
    if not units:
        units.append(("", "$"))
    return [f'{indent}.string "{escape_c_literal(line)}{suffix}"\n' for line, suffix in units]


def transform_asm_strings(
    text: str,
    translator: Translator,
    ctx: RunContext,
    delay: float,
    wrap_width: int,
    lines_per_page: int,
) -> tuple[str, Stats]:
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    stats = Stats()
    index = 0
    current_label: str | None = None

    while index < len(lines):
        stripped = lines[index].strip()
        if stripped.endswith("::"):
            current_label = stripped[:-2]

        match = ASM_STRING_RE.match(lines[index].rstrip("\r\n"))
        if not match:
            out.append(lines[index])
            index += 1
            continue

        start = index
        group: list[tuple[str, str]] = []
        while index < len(lines):
            group_match = ASM_STRING_RE.match(lines[index].rstrip("\r\n"))
            if not group_match:
                break
            group.append((group_match.group(1), group_match.group(2)))
            index += 1

        raw = "".join(part for _, part in group)
        stats.strings_seen += 1
        if should_skip_asm_block(current_label, raw):
            stats.strings_skipped += 1
            out.extend(lines[start:index])
            continue

        terminator = raw.endswith("$")
        body = raw[:-1] if terminator else raw
        pages = [part for part in body.split(r"\p") if part.strip()]
        translated_pages = [translate_asm_page(page, translator, ctx, delay) for page in pages]
        rebuilt = "".join(translated_pages) + ("$" if terminator else "")
        if rebuilt == raw:
            stats.strings_skipped += 1
            out.extend(lines[start:index])
            continue

        stats.strings_changed += 1
        out.extend(format_asm_string_block(translated_pages, group[0][0], wrap_width, lines_per_page))

    return "".join(out), stats


def transform_concat_macros(
    text: str,
    translator: Translator,
    ctx: RunContext,
    delay: float,
    wrap_width: int,
) -> tuple[str, Stats]:
    stats = Stats()

    def repl(match: re.Match[str]) -> str:
        block = match.group(1)
        paragraph = c_block_to_paragraph(block)
        stats.strings_seen += 1
        if not should_translate(paragraph):
            stats.strings_skipped += 1
            return match.group(0)

        translated = translate_segment(paragraph, translator, ctx, delay)
        if translated == paragraph:
            stats.strings_skipped += 1
            return match.group(0)

        stats.strings_changed += 1
        indent_match = re.search(r'\n([ \t]*)"', match.group(0))
        indent = indent_match.group(1) if indent_match else "    "
        return format_concat_macro(wrap_words(translated, wrap_width), indent)

    return CONCAT_MACRO_RE.sub(repl, text), stats


def iter_files(root: Path, scope: str) -> list[Path]:
    files: set[Path] = {root / rel for rel in CORE_TEXT_FILES}
    for pattern in CORE_TEXT_GLOBS:
        files.update(path for path in root.glob(pattern) if path.is_file())
    if scope in {"maps", "all"}:
        for pattern in MAP_TEXT_GLOBS:
            files.update(path for path in root.glob(pattern) if path.is_file())
    if scope == "core":
        files = {path for path in files if "/maps/" not in path.as_posix()}
    return sorted(path for path in files if path.exists())


def translate_item_descriptions(
    root: Path,
    translator: Translator,
    ctx: RunContext,
    delay: float,
    wrap_width: int,
) -> tuple[int, int]:
    path = root / "src/data/items.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = 0
    seen = 0
    for item in data["items"]:
        value = item.get("description_english")
        if not isinstance(value, str):
            continue
        seen += 1
        translated, did_change = translate_wrapped_text(value, translator, ctx, delay, wrap_width)
        if did_change:
            item["description_english"] = translated
            changed += 1
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return seen, changed


def translate_wrapped_text(
    value: str,
    translator: Translator,
    ctx: RunContext,
    delay: float,
    wrap_width: int,
) -> tuple[str, bool]:
    paragraph = normalize_text(value)
    paragraph = re.sub(r"\\[npl]", " ", paragraph)
    paragraph = re.sub(r"\s+", " ", paragraph).strip()
    if not should_translate(paragraph):
        return value, False
    translated = translate_segment(paragraph, translator, ctx, delay)
    if translated == paragraph:
        return value, False
    return "\\n".join(wrap_words(translated, wrap_width)), True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--scope", choices=["core", "maps", "all"], default="core")
    parser.add_argument("--cache", type=Path, default=repo_root() / "translation_reports/auto_translation_cache.json")
    parser.add_argument("--delay", type=float, default=0.0)
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--max-files", type=int, default=0)
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--progress-every", type=int, default=25)
    parser.add_argument("--include-items", action="store_true")
    parser.add_argument("--items-only", action="store_true")
    parser.add_argument("--item-wrap-width", type=int, default=34)
    parser.add_argument("--concat-macros", action="store_true")
    parser.add_argument("--wrap-width", type=int, default=36)
    parser.add_argument("--asm-strings", action="store_true")
    parser.add_argument("--asm-wrap-width", type=int, default=36)
    parser.add_argument("--asm-lines-per-page", type=int, default=2)
    parser.add_argument("--retry-identical-cache", action="store_true")
    parser.add_argument("--refresh-cache", action="store_true")
    args = parser.parse_args()

    if args.items_only:
        args.include_items = True

    args.cache.parent.mkdir(parents=True, exist_ok=True)
    cache: dict[str, str] = {}
    if args.cache.exists():
        cache = json.loads(args.cache.read_text(encoding="utf-8"))

    translator = Translator(timeout=args.timeout)
    ctx = RunContext(args.cache, cache, args.progress_every, args.retry_identical_cache, args.refresh_cache)
    total = Stats()

    if args.items_only:
        files = []
    elif args.path:
        files = [args.root / path for path in args.path]
    else:
        files = iter_files(args.root, args.scope)
    if args.max_files:
        files = files[: args.max_files]

    for path in files:
        print(f"translating {path.relative_to(args.root)}", flush=True)
        text = path.read_text(encoding="utf-8")
        if args.asm_strings:
            new_text, stats = transform_asm_strings(
                text,
                translator,
                ctx,
                args.delay,
                args.asm_wrap_width,
                args.asm_lines_per_page,
            )
        elif args.concat_macros:
            new_text, stats = transform_concat_macros(text, translator, ctx, args.delay, args.wrap_width)
        else:
            new_text, stats = transform_quoted_strings(text, translator, ctx, args.delay)
        total.strings_seen += stats.strings_seen
        total.strings_changed += stats.strings_changed
        total.strings_skipped += stats.strings_skipped
        if new_text != text:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            total.files_changed += 1
            print(f"{path.relative_to(args.root)}: changed={stats.strings_changed} seen={stats.strings_seen}", flush=True)
        ctx.save_cache()

    if args.include_items:
        print("translating src/data/items.json descriptions", flush=True)
        seen, changed = translate_item_descriptions(args.root, translator, ctx, args.delay, args.item_wrap_width)
        total.strings_seen += seen
        total.strings_changed += changed
        if changed:
            total.files_changed += 1
        print(f"src/data/items.json: changed={changed} seen={seen}", flush=True)

    ctx.save_cache()
    print(
        f"files_changed={total.files_changed} strings_changed={total.strings_changed} "
        f"strings_seen={total.strings_seen} cache_entries={len(ctx.cache)}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
