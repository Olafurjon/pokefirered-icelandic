from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path

from apply_manual_translation_queue import compact_control_text, normalize_translation, validate_translation
from common import mapped_chars, repo_root


C_STRING_RE = re.compile(r'"((?:\\.|[^"\\])*)"')
PARAGRAPH_SENTINEL = "\x07"


@dataclass
class ApplyResult:
    file: str
    line: str
    label: str
    status: str
    reason: str = ""


def escape_c_control_text(text: str) -> str:
    text = normalize_translation(text)
    text = re.sub(r"\n[ \t]*\n+", PARAGRAPH_SENTINEL, text)
    out: list[str] = []
    for char in text:
        if char == PARAGRAPH_SENTINEL:
            out.append(r"\p")
        elif char == "\n":
            out.append(r"\n")
        elif char == "\\":
            out.append(r"\\")
        elif char == '"':
            out.append('\\"')
        else:
            out.append(char)
    return "".join(out)


def c_literal_text(source_literal: str) -> str:
    return compact_control_text(source_literal.rstrip("$"))


def rows_by_file(input_csv: Path) -> dict[str, list[dict[str, str]]]:
    with input_csv.open("r", encoding="utf-8-sig", newline="") as f:
        rows = [row for row in csv.DictReader(f) if (row.get("icelandic") or "").strip()]
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(row["file"], []).append(row)
    return grouped


def apply_c_like_file(
    path: Path,
    rel: str,
    rows: list[dict[str, str]],
    chars: set[str],
    allow_current_mismatch: bool,
    dry_run: bool,
) -> list[ApplyResult]:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    results: list[ApplyResult] = []
    changed = False

    for row in rows:
        line_text = row.get("line", "")
        label = row.get("label", "")
        try:
            line_no = int(line_text)
        except ValueError:
            results.append(ApplyResult(rel, line_text, label, "skipped", "invalid line number"))
            continue
        if line_no < 1 or line_no > len(lines):
            results.append(ApplyResult(rel, line_text, label, "skipped", "line number out of range"))
            continue

        expected = (row.get("current_text") or "").replace("\r\n", "\n").replace("\r", "\n").strip()
        normalized = normalize_translation(row.get("icelandic") or "")
        issue = validate_translation(row, normalized, chars)
        if issue:
            results.append(ApplyResult(rel, line_text, label, "skipped", issue))
            continue

        line = lines[line_no - 1]
        matches = list(C_STRING_RE.finditer(line))
        if not matches:
            results.append(ApplyResult(rel, line_text, label, "skipped", "string literal not found on line"))
            continue

        selected: re.Match[str] | None = None
        for match in matches:
            if c_literal_text(match.group(1)).strip() == expected:
                selected = match
                break
        if selected is None:
            if not allow_current_mismatch or len(matches) != 1:
                results.append(ApplyResult(rel, line_text, label, "skipped", "current text mismatch"))
                continue
            selected = matches[0]

        replacement = '"' + escape_c_control_text(normalized) + '"'
        new_line = line[: selected.start()] + replacement + line[selected.end() :]
        if new_line == line:
            results.append(ApplyResult(rel, line_text, label, "unchanged"))
            continue

        lines[line_no - 1] = new_line
        changed = True
        results.append(ApplyResult(rel, line_text, label, "applied"))

    if changed and not dry_run:
        path.write_text("".join(lines), encoding="utf-8", newline="\n")
    return results


def apply_items_json(
    path: Path,
    rel: str,
    rows: list[dict[str, str]],
    chars: set[str],
    allow_current_mismatch: bool,
    dry_run: bool,
) -> list[ApplyResult]:
    data = json.loads(path.read_text(encoding="utf-8"))
    by_id = {item.get("itemId"): item for item in data.get("items", [])}
    results: list[ApplyResult] = []
    changed = False

    for row in rows:
        label = row.get("label", "")
        line = row.get("line", "")
        if "." not in label:
            results.append(ApplyResult(rel, line, label, "skipped", "invalid item label"))
            continue
        item_id, key = label.rsplit(".", 1)
        item = by_id.get(item_id)
        if item is None or key not in {"english", "description_english"}:
            results.append(ApplyResult(rel, line, label, "skipped", "item field not found"))
            continue

        expected = (row.get("current_text") or "").replace("\r\n", "\n").replace("\r", "\n").strip()
        current = compact_control_text(str(item.get(key, ""))).replace("\r\n", "\n").replace("\r", "\n").strip()
        normalized = normalize_translation(row.get("icelandic") or "")
        issue = validate_translation(row, normalized, chars)
        if issue:
            results.append(ApplyResult(rel, line, label, "skipped", issue))
            continue
        if current != expected and not allow_current_mismatch:
            results.append(ApplyResult(rel, line, label, "skipped", "current text mismatch"))
            continue
        if current == normalized:
            results.append(ApplyResult(rel, line, label, "unchanged"))
            continue

        item[key] = normalized.replace("\n", r"\n") if key == "description_english" else normalized
        changed = True
        results.append(ApplyResult(rel, line, label, "applied"))

    if changed and not dry_run:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
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
    parser.add_argument("--report", type=Path, default=repo_root() / "translation_reports/structured_translation_apply_report.csv")
    parser.add_argument("--allow-current-mismatch", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    chars = mapped_chars(args.root)
    results: list[ApplyResult] = []
    for rel, rows in sorted(rows_by_file(args.input_csv).items()):
        path = args.root / rel
        if not path.exists():
            results.extend(ApplyResult(rel, row.get("line", ""), row.get("label", ""), "skipped", "file not found") for row in rows)
        elif path.name == "items.json":
            results.extend(apply_items_json(path, rel, rows, chars, args.allow_current_mismatch, args.dry_run))
        elif path.suffix in {".c", ".h"}:
            results.extend(apply_c_like_file(path, rel, rows, chars, args.allow_current_mismatch, args.dry_run))
        else:
            results.extend(ApplyResult(rel, row.get("line", ""), row.get("label", ""), "ignored", "unsupported by structured apply") for row in rows)

    write_report(args.report, results)
    counts: dict[str, int] = {}
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1
    print(" ".join(f"{key}={counts[key]}" for key in sorted(counts)))
    print(f"report={args.report}")
    return 0 if not any(result.status == "skipped" for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
