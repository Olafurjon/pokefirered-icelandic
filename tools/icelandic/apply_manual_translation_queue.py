from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path

from common import literal_chars, mapped_chars, repo_root


ASM_STRING_RE = re.compile(r'^([ \t]*)\.string\s+"((?:\\.|[^"\\])*)"\s*$')
CONTROL_TOKEN_RE = re.compile(r"(\{[^}]+\}|\[[A-Za-z0-9_+:-]+\])")
PROTECTED_SPACE = "\x07"

PUNCTUATION_NORMALIZATION = str.maketrans({
    "\u2013": "-",
    "\u2014": "-",
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": "'",
    "\u201d": "'",
    "\u201e": "'",
})


@dataclass
class ApplyResult:
    file: str
    line: str
    label: str
    status: str
    reason: str = ""


def compact_control_text(text: str) -> str:
    return text.replace(r"\n", "\n").replace(r"\p", "\n\n").replace(r"\l", "\n")


def escape_asm_literal(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def normalize_translation(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.translate(PUNCTUATION_NORMALIZATION)
    text = text.replace('"', "'")
    lines = [line.rstrip() for line in text.split("\n")]
    return "\n".join(lines).strip()


def wrap_words(text: str, width: int) -> list[str]:
    lines: list[str] = []
    current = ""

    def protect(match: re.Match[str]) -> str:
        return match.group(0).replace(" ", PROTECTED_SPACE)

    protected_text = re.sub(r"\{[^}]+\}", protect, text)
    for raw_word in protected_text.split():
        word = raw_word.replace(PROTECTED_SPACE, " ")
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


def translation_pages(text: str) -> list[str]:
    pages: list[str] = []
    for paragraph in re.split(r"\n[ \t]*\n", text):
        paragraph = re.sub(r"[ \t]*\n[ \t]*", " ", paragraph)
        paragraph = re.sub(r"\s+", " ", paragraph).strip()
        if paragraph:
            pages.append(paragraph)
    return pages


def format_asm_string_block(
    pages: list[str],
    indent: str,
    wrap_width: int,
    lines_per_page: int,
) -> list[str]:
    units: list[tuple[str, str]] = []
    for page_index, page in enumerate(pages):
        wrapped = wrap_words(page, wrap_width)
        chunks = [wrapped[index : index + lines_per_page] for index in range(0, len(wrapped), lines_per_page)]
        for chunk_index, chunk in enumerate(chunks):
            for line_index, line in enumerate(chunk):
                is_last_page = page_index == len(pages) - 1
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
    return [f'{indent}.string "{escape_asm_literal(line)}{suffix}"\n' for line, suffix in units]


def required_tokens(*texts: str) -> set[str]:
    tokens: set[str] = set()
    for text in texts:
        tokens.update(CONTROL_TOKEN_RE.findall(text))
    return tokens


def missing_required_tokens(row: dict[str, str], translation: str) -> list[str]:
    tokens = required_tokens(row.get("source_english", ""), row.get("current_text", ""))
    return sorted(token for token in tokens if token not in translation)


def validate_translation(row: dict[str, str], translation: str, chars: set[str]) -> str:
    if not translation:
        return "blank translation"
    if "$" in translation:
        return "translation contains string terminator '$'"
    missing_tokens = missing_required_tokens(row, translation)
    if missing_tokens:
        return "missing control token(s): " + ", ".join(missing_tokens)
    bad_chars = sorted({char for char in literal_chars(translation) if ord(char) > 127 and char not in chars})
    if bad_chars:
        return "unsupported character(s): " + "".join(bad_chars)
    return ""


def rows_by_file(input_csv: Path) -> dict[str, list[dict[str, str]]]:
    with input_csv.open("r", encoding="utf-8-sig", newline="") as f:
        rows = [row for row in csv.DictReader(f) if (row.get("icelandic") or "").strip()]
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(row["file"], []).append(row)
    return grouped


def apply_asm_file(
    path: Path,
    rel: str,
    rows: list[dict[str, str]],
    chars: set[str],
    wrap_width: int,
    lines_per_page: int,
    allow_current_mismatch: bool,
    dry_run: bool,
) -> list[ApplyResult]:
    wanted: dict[str, dict[str, str]] = {}
    results: list[ApplyResult] = []
    for row in rows:
        label = row["label"]
        if label in wanted:
            results.append(ApplyResult(rel, row.get("line", ""), label, "skipped", "duplicate label in input CSV"))
            continue
        wanted[label] = row

    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    out: list[str] = []
    index = 0
    current_label = ""
    changed = False
    seen: set[str] = set()

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

        row = wanted.get(current_label)
        if row is None:
            out.extend(lines[start:index])
            continue

        seen.add(current_label)
        current_text = compact_control_text("".join(part for _, part in group).rstrip("$"))
        expected_text = (row.get("current_text") or "").replace("\r\n", "\n").replace("\r", "\n").strip()
        normalized = normalize_translation(row.get("icelandic") or "")
        issue = validate_translation(row, normalized, chars)
        if issue:
            results.append(ApplyResult(rel, row.get("line", ""), current_label, "skipped", issue))
            out.extend(lines[start:index])
            continue
        if current_text.strip() != expected_text and not allow_current_mismatch:
            results.append(ApplyResult(rel, row.get("line", ""), current_label, "skipped", "current text mismatch"))
            out.extend(lines[start:index])
            continue

        pages = translation_pages(normalized)
        rebuilt = format_asm_string_block(pages, group[0][0], wrap_width, lines_per_page)
        if rebuilt == lines[start:index]:
            results.append(ApplyResult(rel, row.get("line", ""), current_label, "unchanged"))
            out.extend(lines[start:index])
            continue

        results.append(ApplyResult(rel, row.get("line", ""), current_label, "applied"))
        out.extend(rebuilt)
        changed = True

    for row in rows:
        label = row["label"]
        if label not in seen and label in wanted:
            results.append(ApplyResult(rel, row.get("line", ""), label, "skipped", "label not found"))

    if changed and not dry_run:
        path.write_text("".join(out), encoding="utf-8", newline="\n")
    return results


def write_report(path: Path, results: list[ApplyResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "line", "label", "status", "reason"])
        writer.writeheader()
        for result in results:
            writer.writerow(result.__dict__)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--report", type=Path, default=repo_root() / "translation_reports/manual_translation_apply_report.csv")
    parser.add_argument("--wrap-width", type=int, default=36)
    parser.add_argument("--lines-per-page", type=int, default=2)
    parser.add_argument("--allow-current-mismatch", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    chars = mapped_chars(args.root)
    grouped = rows_by_file(args.input_csv)
    results: list[ApplyResult] = []

    for rel, rows in sorted(grouped.items()):
        path = args.root / rel
        if not path.exists():
            results.extend(ApplyResult(rel, row.get("line", ""), row.get("label", ""), "skipped", "file not found") for row in rows)
            continue
        if path.suffix not in {".inc", ".s"}:
            results.extend(ApplyResult(rel, row.get("line", ""), row.get("label", ""), "skipped", "unsupported file type") for row in rows)
            continue
        results.extend(
            apply_asm_file(
                path,
                rel,
                rows,
                chars,
                args.wrap_width,
                args.lines_per_page,
                args.allow_current_mismatch,
                args.dry_run,
            )
        )

    write_report(args.report, results)
    counts: dict[str, int] = {}
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1
    print(" ".join(f"{key}={counts[key]}" for key in sorted(counts)))
    print(f"report={args.report}")
    return 0 if not any(result.status == "skipped" for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
