<img width="1979" height="1259" alt="image" src="https://github.com/user-attachments/assets/695f6854-3e3b-4b41-9da7-1d2f1d7bd6a4" />


# Pokefirered Icelandic / Vasaskrímsli

This is an Icelandic localization and gameplay-friendly fork of the English
Pokemon FireRed/LeafGreen decompilation.

The project goal is a playable Icelandic FireRed ROM with Icelandic dialogue,
menus, item names, move names, species names, graphics, fonts, and supporting
quality-of-life changes where they make the game work better as a standalone
Icelandic release.

## Project Rules

- Do not commit ROMs, save states, baseroms, generated ELF/MAP files, or other
  copyrighted binary dumps.
- Build artifacts such as `*.gba`, `*.elf`, `*.map`, `*.sgm`, and `build/` are
  ignored by git.
- Keep translation terminology consistent with
  `docs/icelandic_translation_reference.md`.
- Preserve visible capitalization patterns where possible. For example,
  `POKeMON` becomes `VASaSKRIMSLI` in stylized all-caps contexts.
- Use Icelandic inflection in dialogue, even when the glossary term is listed
  in nominative form.

## Build

Set up the repository as described in `INSTALL.md`, then build the modern ROM:

```sh
make modern -j$(nproc)
```

On Windows with WSL installed, run:

```powershell
wsl make modern -j8
```

The output ROM is generated locally as `pokefirered_modern.gba`.

## Translation Workflow

Useful files:

- `docs/icelandic_translation_reference.md` - approved terms, species names,
  style rules, and gameplay localization notes.
- `translation_reports/` - generated queues, validation reports, and applied
  translation batches.
- `tools/icelandic/` - helper scripts for extracting, validating, applying, and
  checking Icelandic text.

Before submitting a change, run:

```powershell
python tools\icelandic\check_terms.py --root .
wsl make modern -j8
```

## Current Gameplay Tweaks

- Trade-only evolutions are available without trading.
- Trade-with-item evolutions happen by leveling up while holding the original
  trade item. The item is consumed when evolution starts.

## Upstream

This project is based on the pret FireRed/LeafGreen decompilation:

https://github.com/pret/pokefirered

For setup details and upstream documentation, see `INSTALL.md`.
