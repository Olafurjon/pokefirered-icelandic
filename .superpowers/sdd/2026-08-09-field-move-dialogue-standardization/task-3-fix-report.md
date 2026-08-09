# Task 3 Fix Report

## Status

Complete.

## Change

Replaced the visible `FLASH HM` wording in `data/text/pokedex_rating.inc` with the natural Icelandic wording `HM fyrir LEIFTUR`, preserving the existing string terminator and player-facing meaning.

## Verification

- `python tools/icelandic/check_terms.py --root .`
- `python -m unittest tools.icelandic.test_translation_sanity -v`
- `git diff --check`

## Concerns

None.
