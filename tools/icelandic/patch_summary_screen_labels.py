#!/usr/bin/env python3
"""Bake Icelandic fixed labels into the Pokemon summary-screen tile atlas."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
ATLAS_PATH = ROOT / "graphics" / "summary_screen" / "bg.png"


# Compact 4x7-style capitals matching the fixed labels in the original atlas.
# Glyphs are variable-width so the longer Icelandic labels still fit their plates.
GLYPHS = {
    " ": ("...",) * 7,
    ".": (".", ".", ".", ".", ".", "#", "#"),
    "A": (".##.", "#..#", "#..#", "####", "#..#", "#..#", "#..#"),
    "B": ("###.", "#..#", "#..#", "###.", "#..#", "#..#", "###."),
    "C": (".###", "#...", "#...", "#...", "#...", "#...", ".###"),
    "D": ("###.", "#..#", "#..#", "#..#", "#..#", "#..#", "###."),
    "E": ("####", "#...", "#...", "###.", "#...", "#...", "####"),
    "F": ("####", "#...", "#...", "###.", "#...", "#...", "#..."),
    "G": (".###", "#...", "#...", "#.##", "#..#", "#..#", ".###"),
    "H": ("#..#", "#..#", "#..#", "####", "#..#", "#..#", "#..#"),
    "I": ("###", ".#.", ".#.", ".#.", ".#.", ".#.", "###"),
    "J": ("..##", "...#", "...#", "...#", "...#", "#..#", ".##."),
    "K": ("#..#", "#.#.", "##..", "#...", "##..", "#.#.", "#..#"),
    "L": ("#...", "#...", "#...", "#...", "#...", "#...", "####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#..#", "##.#", "##.#", "#.##", "#.##", "#..#", "#..#"),
    "O": (".##.", "#..#", "#..#", "#..#", "#..#", "#..#", ".##."),
    "P": ("###.", "#..#", "#..#", "###.", "#...", "#...", "#..."),
    "R": ("###.", "#..#", "#..#", "###.", "#.#.", "#..#", "#..#"),
    "S": (".###", "#...", "#...", ".##.", "...#", "...#", "###."),
    "T": ("####", ".##.", ".##.", ".##.", ".##.", ".##.", ".##."),
    "U": ("#..#", "#..#", "#..#", "#..#", "#..#", "#..#", ".##."),
    "V": ("#...#", "#...#", "#...#", "#...#", ".#.#.", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#..#", "#..#", ".##.", ".##.", ".##.", "#..#", "#..#"),
    "Y": ("#..#", "#..#", ".##.", ".##.", ".##.", ".##.", ".##."),
    "Z": ("####", "...#", "..#.", ".#..", "#...", "#...", "####"),
    "Á": ("..#.", ".##.", "#..#", "#..#", "####", "#..#", "#..#"),
    "Í": ("..#", "###", ".#.", ".#.", ".#.", ".#.", "###"),
    "Ð": (".###.", "#...#", "###.#", "#...#", "#...#", "#...#", ".###."),
    "Þ": ("#....", "###..", "#..#.", "#..#.", "###..", "#....", "#...."),
    "Æ": (".#####", "#.#...", "#.#...", "######", "#.#...", "#.#...", "#.####"),
    "Ö": ("#..#", ".##.", "#..#", "#..#", "#..#", "#..#", ".##."),
}


# (text, x0, x1, y, foreground palette index, plate palette index)
LABELS = (
    ("MINNISBLAÐ", 52, 126, 8, 46, 45),
    ("NR", 4, 45, 31, 46, 45),
    ("NAFN", 4, 45, 46, 46, 45),
    ("GERÐ", 4, 45, 61, 46, 45),
    ("ÞJ", 4, 45, 76, 46, 45),
    ("AUÐK.", 4, 45, 91, 46, 45),
    ("HLUTUR", 4, 45, 106, 46, 45),
    ("STAÐA", 76, 118, 106, 46, 45),
    ("LÍF", 4, 49, 126, 62, 61),
    ("ÁRÁS", 4, 49, 144, 62, 61),
    ("VÖRN", 4, 49, 157, 62, 61),
    ("S.ÁRÁS", 4, 49, 170, 62, 61),
    ("S.VÖRN", 4, 49, 183, 62, 61),
    ("HRAÐI", 4, 49, 196, 62, 61),
    ("KRAFTUR", 76, 118, 124, 78, 77),
    ("HITTNI", 76, 118, 138, 78, 77),
    ("ÁHRIF", 76, 118, 151, 78, 77),
    ("STIG", 4, 65, 220, 62, 61),
    ("HÆFILEIKI", 4, 65, 244, 62, 61),
)


def text_width(text: str) -> int:
    return sum(len(GLYPHS[char][0]) for char in text) + max(0, len(text) - 1)


def clear_old_text(image: Image.Image, x0: int, x1: int, y: int, fg: int, bg: int) -> None:
    for py in range(max(0, y - 1), min(image.height, y + 9)):
        for px in range(x0, min(image.width, x1)):
            if image.getpixel((px, py)) == fg:
                image.putpixel((px, py), bg)


def draw_centered_text(image: Image.Image, text: str, x0: int, x1: int, y: int, fg: int) -> None:
    width = text_width(text)
    available = x1 - x0
    if width > available:
        raise ValueError(f"{text!r} is {width}px wide but only {available}px are available")

    x = x0 + (available - width) // 2
    for char in text:
        glyph = GLYPHS[char]
        glyph_width = len(glyph[0])
        for row, pixels in enumerate(glyph):
            for column, pixel in enumerate(pixels):
                if pixel == "#":
                    image.putpixel((x + column, y + row), fg)
        x += glyph_width + 1


def main() -> None:
    image = Image.open(ATLAS_PATH)
    if image.mode != "P" or image.size != (128, 256):
        raise ValueError(f"Expected indexed 128x256 atlas, got {image.mode} {image.size}")

    for text, x0, x1, y, fg, bg in LABELS:
        clear_old_text(image, x0, x1, y, fg, bg)
        draw_centered_text(image, text, x0, x1, y, fg)

    image.save(ATLAS_PATH, optimize=False)


if __name__ == "__main__":
    main()
