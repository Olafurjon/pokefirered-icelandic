# GitHub Setup

Recommended public setup:

1. Create a fork of the upstream repository, usually `pret/pokefirered`.
2. Push this work to a branch named `pokefirered-icelandic`.
3. Set that branch as the default branch for the Icelandic fork if the fork is
   dedicated to this localization.
4. Keep `master` or `main` close to upstream if you want an easy upstream merge
   path later.

## Repository Rules

- Do not upload ROMs, baseroms, save states, or generated build binaries.
- Use pull requests for translation and playtest fixes.
- Ask contributors to include screenshots for visual/text issues.
- Keep terminology updates in `docs/icelandic_translation_reference.md`.

## Suggested Labels

- `translation`
- `playtest`
- `font`
- `graphics`
- `battle-ui`
- `catchability`
- `needs-icelandic-review`
- `good first issue`

## Useful Commands

```powershell
git remote add upstream https://github.com/pret/pokefirered.git
git switch pokefirered-icelandic
python tools\icelandic\check_terms.py --root .
wsl make modern -j8
```

To publish the branch after creating the GitHub fork:

```powershell
git push -u origin pokefirered-icelandic
```
