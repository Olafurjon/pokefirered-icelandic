# Contributing

Thanks for helping with the Icelandic FireRed localization.

## What To Work On

Good contribution types:

- Icelandic dialogue fixes.
- Menu, battle text, item, move, ability, and type consistency fixes.
- Font or glyph fixes for Icelandic letters.
- Title-screen and other graphic localization.
- Playtest reports with screenshots and exact location/context.
- Catchability and no-trade evolution improvements.

## Translation Standards

Use `docs/icelandic_translation_reference.md` as the source of truth.

Important examples:

- Pokemon / Pokemon -> Vasaskrímsli
- POKeMON -> VASaSKRIMSLI
- Poke Ball -> Vasa bolti
- POKe BALL -> VASA BOLTI
- Trainer Tips -> Þjálfara ráð
- TRAINER TIPS -> ÞJÁLFARA RÁÐ
- Route 1 -> Vegur 1
- ROUTE 1 -> VEGUR 1
- Pallet Town -> Pallet bær
- PALLET TOWN -> PALLET BÆR
- City -> borg
- Pocket -> hólf
- TV -> sjónvarp

Preserve source capitalization where it is visible in-game. Do not translate C
symbols, labels, constants, flags, or filenames unless the file is specifically
intended to contain visible text.

## Before Opening A Pull Request

Run the translation tests and consistency checker:

```powershell
python -m unittest tools.icelandic.test_translation_sanity
python tools\icelandic\check_terms.py --root .
```

Build the ROM:

```powershell
wsl make modern -j8
```

If a visual issue is involved, include a screenshot and where it happened.

Pull requests to `main` also run these checks in GitHub Actions, plus a modern
ROM build.

## Manual Translation CSVs

When submitting manual CSV translations:

- Keep placeholders unchanged, such as `{PLAYER}`, `{RIVAL}`, `{STR_VAR_1}`,
  `\n`, `\p`, and `$`.
- Keep line breaks and control codes deliberate.
- Do not translate internal source anchors.
- Prefer shorter wording when text appears in menus or small message boxes.

## Git Hygiene

- Keep PRs focused when possible.
- Do not commit generated ROMs or build outputs.
- Do not include API keys or credentials in commits.
- If a change updates terminology, update `docs/icelandic_translation_reference.md`
  in the same PR.
