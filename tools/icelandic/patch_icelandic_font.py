from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from common import ICELANDIC_GLYPHS, repo_root


BASE_CODES = {
    "Þ": 0xCA,             # P
    "þ": 0xE4,             # p
    "Æ": 0xBB,             # A
    "æ": 0xD5,             # a
    "Ð": 0xBE,             # D
    "ð": 0xD8,             # d
    "Ý": 0xD3,             # Y
    "ý": 0xED,             # y
}


FONT_FILES = {
    "graphics/fonts/latin_normal.png": 16,
    "graphics/fonts/latin_male.png": 16,
    "graphics/fonts/latin_female.png": 16,
    "graphics/fonts/latin_small.png": 8,
}


def cell_box(code: int, cell_width: int) -> tuple[int, int, int, int]:
    columns = 256 // cell_width
    x = (code % columns) * cell_width
    y = (code // columns) * 16
    return x, y, x + cell_width, y + 16


def draw_pixel(cell: Image.Image, x: int, y: int, color: int = 1) -> None:
    if 0 <= x < cell.width and 0 <= y < cell.height:
        cell.putpixel((x, y), color)
    if 0 <= x + 1 < cell.width and 0 <= y + 1 < cell.height and color == 1:
        if cell.getpixel((x + 1, y + 1)) == 0:
            cell.putpixel((x + 1, y + 1), 2)


def clear_pixel(cell: Image.Image, x: int, y: int) -> None:
    if 0 <= x < cell.width and 0 <= y < cell.height:
        cell.putpixel((x, y), 0)


def clear_rect(cell: Image.Image, x1: int, y1: int, x2: int, y2: int) -> None:
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            clear_pixel(cell, x, y)


def hline(cell: Image.Image, x1: int, x2: int, y: int) -> None:
    for x in range(x1, x2 + 1):
        draw_pixel(cell, x, y)


def vline(cell: Image.Image, x: int, y1: int, y2: int) -> None:
    for y in range(y1, y2 + 1):
        draw_pixel(cell, x, y)


def acute(cell: Image.Image, x: int, y: int) -> None:
    draw_pixel(cell, x + 1, y)
    draw_pixel(cell, x, y + 1)


def patch_cell(cell: Image.Image, glyph: str) -> Image.Image:
    w = cell.width
    if glyph == "Þ":
        # Uppercase thorn needs to differ from P in the bitmap font: extend
        # the stem above and below the bowl so it reads as Þ in-game.
        vline(cell, 0, 1, 13)
    elif glyph == "þ":
        vline(cell, 0, 2, 13)
    elif glyph == "Æ":
        patch_ae(cell)
    elif glyph == "æ":
        if w <= 8:
            hline(cell, 4, 7, 7)
            hline(cell, 4, 7, 10)
            vline(cell, 7, 7, 10)
        else:
            hline(cell, 6, 10, 7)
            hline(cell, 6, 10, 10)
            vline(cell, 10, 7, 10)
    elif glyph == "Ð":
        hline(cell, 1, min(w - 5, 8), 7)
    elif glyph == "ð":
        hline(cell, 3, min(w - 3, 8), 5)
        draw_pixel(cell, min(w - 4, 7), 3)
    elif glyph == "Ý":
        acute(cell, min(w - 6, 7), 1)
    elif glyph == "ý":
        acute(cell, min(w - 5, 4), 1)
    return cell


def patch_ae(cell: Image.Image) -> Image.Image:
    # Build Æ as a ligature, not as a separated A+E.  The E arms share the
    # right stem of A so the in-game shadow still reads as one letter.
    w = cell.width
    if w <= 8:
        clear_rect(cell, 0, 4, 7, 13)
        rows = {
            4: "#####...",
            5: "#++#+...",
            6: "#+.#....",
            7: "#####...",
            8: "#++#+...",
            9: "#+.#....",
            10: "#+.#....",
            11: "++.#....",
            12: "...####.",
        }
    else:
        clear_rect(cell, 0, 3, 15, 14)
        rows = {
            3: ".########...",
            4: "#++++#+++...",
            5: "#+...#......",
            6: "#+...#......",
            7: "########....",
            8: "#++++#+++...",
            9: "#+...#......",
            10: "#+...#......",
            11: "++...#......",
            12: ".....######.",
        }
    for y, row in rows.items():
        for x, value in enumerate(row):
            if value == "#":
                draw_pixel(cell, x, y, 1)
            elif value == "+":
                draw_pixel(cell, x, y, 2)
    return cell


def patch_font(path: Path, cell_width: int) -> None:
    image = Image.open(path)
    if image.mode != "P":
        image = image.convert("P")
    original_size = image.size
    for glyph, dst_code in ICELANDIC_GLYPHS.items():
        src_box = cell_box(BASE_CODES[glyph], cell_width)
        dst_box = cell_box(dst_code, cell_width)
        cell = image.crop(src_box)
        cell = patch_cell(cell, glyph)
        image.paste(cell, dst_box)
    if image.size != original_size:
        raise RuntimeError(f"{path} changed size from {original_size} to {image.size}")
    image.save(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args()
    for rel_path, cell_width in FONT_FILES.items():
        patch_font(args.root / rel_path, cell_width)
        print(f"patched {rel_path}")


if __name__ == "__main__":
    main()
