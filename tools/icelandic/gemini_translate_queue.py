from __future__ import annotations

import argparse
import csv
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path


JAPANESE_RE = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
PLACEHOLDER_ONLY_RE = re.compile(r"^[\s{}A-Z0-9_.$:/\\\-+×▶♂♀#?!.,'\";()]+$")
SHOP_LABEL_RE = re.compile(r"^[A-Z0-9 .'\-]+(?:\{CLEAR_TO 0x[0-9A-Fa-f]+\}\{FONT_SMALL\})?[¥0-9,]*$")
CONTROL_TOKEN_RE = re.compile(r"^(?:\{[^}]+\}|[¥0-9, .:;!?/#()+\-])+$")


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_rows(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_good_candidate(row: dict[str, str], kinds: set[str]) -> bool:
    if row.get("kind") not in kinds:
        return False
    label = row.get("label", "")
    if label.startswith("line_"):
        return False
    text = (row.get("current_text") or "").strip()
    if not text:
        return False
    if JAPANESE_RE.search(text):
        return False
    if len(text) <= 2:
        return False
    if CONTROL_TOKEN_RE.fullmatch(text):
        return False
    if SHOP_LABEL_RE.fullmatch(text) and ("{CLEAR_TO" in text or len(text.split()) <= 3):
        return False
    if PLACEHOLDER_ONLY_RE.fullmatch(text) and " " not in text and "\n" not in text:
        return False
    return True


def select_rows(rows: list[dict[str, str]], limit: int, files: list[str], kinds: set[str]) -> list[dict[str, str]]:
    candidates = [row for row in rows if is_good_candidate(row, kinds)]
    if files:
        order = {name: i for i, name in enumerate(files)}
        candidates = [row for row in candidates if row.get("file") in order]
        candidates.sort(key=lambda row: (order[row.get("file", "")], int(row.get("line") or 0)))
    else:
        candidates.sort(key=lambda row: (row.get("file", ""), int(row.get("line") or 0)))
    return candidates[:limit]


def extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text).strip()
        text = re.sub(r"```$", "", text).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON object found in model response")
    return json.loads(text[start : end + 1])


def call_gemini(model: str, items: list[dict[str, str]], temperature: float) -> dict[int, str]:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise SystemExit("GEMINI_API_KEY is not set")

    prompt_items = [
        {
            "id": i,
            "file": row.get("file", ""),
            "label": row.get("label", ""),
            "english": row.get("current_text", ""),
        }
        for i, row in enumerate(items)
    ]
    prompt = f"""
You are translating Pokemon FireRed game text into Icelandic for a ROM hack.
Return ONLY valid JSON in this exact shape:
{{"translations":[{{"id":0,"is":"..."}}]}}

Rules:
- Translate naturally to Icelandic, with correct grammar and inflection.
- Preserve all placeholders/control codes exactly, e.g. {{PLAYER}}, {{STR_VAR_1}}, {{A_BUTTON}}, \\p, \\n, {{PAUSE_UNTIL_PRESS}}.
- Preserve explicit line breaks where useful; keep text concise for GBA text boxes.
- Pokemon/Poké* concepts become Vasaskrímsli. Stylized POKéMON/POKEMON becomes VASaSKRÍMSLI if the source is all-caps/stylized.
- Poké Ball/Poke Ball concepts become Vasa bolti / VASABOLTI depending on capitalization.
- Preserve capitalization style: all-caps source should usually produce all-caps Icelandic.
- Keep proper names such as OAK, KANTO, CELADON, SILPH, TEAM ROCKET, move names, and item identifiers when they are clearly names.
- Do not translate source-code identifiers, only the visible game text in "english".
- Do not add explanations.

Items:
{json.dumps(prompt_items, ensure_ascii=False)}
"""
    body = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "responseMimeType": "application/json",
        },
    }
    url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={key}"
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.load(r)
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed = extract_json(text)
            return {int(item["id"]): str(item["is"]) for item in parsed.get("translations", [])}
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", errors="replace")
            if e.code in {429, 500, 502, 503, 504} and attempt < 3:
                time.sleep(2**attempt)
                continue
            raise RuntimeError(f"Gemini HTTP {e.code}: {msg[:1000]}") from e
    raise RuntimeError("Gemini request failed after retries")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=80)
    parser.add_argument("--model", default="models/gemini-2.5-flash")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--files", nargs="*", default=[])
    parser.add_argument("--kinds", nargs="*", default=["untranslated"])
    args = parser.parse_args()

    rows = load_rows(args.input_csv)
    selected = select_rows(rows, args.limit, args.files, set(args.kinds))
    if not selected:
        print("selected=0")
        return 0

    translations = call_gemini(args.model, selected, args.temperature)
    out_rows: list[dict[str, str]] = []
    for i, row in enumerate(selected):
        translated = translations.get(i, "").strip()
        if not translated:
            continue
        out = dict(row)
        out["icelandic"] = translated
        out_rows.append(out)

    fieldnames = list(rows[0].keys()) if rows else ["file", "line", "label", "kind", "source_english", "current_text", "icelandic", "notes"]
    write_rows(args.output, out_rows, fieldnames)
    print(f"selected={len(selected)} translated={len(out_rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
