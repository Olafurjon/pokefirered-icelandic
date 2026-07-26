# Translation Reports

This folder is for generated localization reports and temporary translation
queues.

Most generated CSVs are ignored by git so the public repository does not fill up
with historical batches. Curated reports can be force-added when they are useful
for contributors.

Tracked by default:

- `README.md`
- `terminology_suspects-current.csv`

Useful generated reports:

- Manual translation queues for human review.
- Gemini or other machine-translation batches before application.
- Validation reports for unsupported glyphs, overlong fixed-width names, or
  visible English remnants.
- Terminology suspect reports from `tools/icelandic/check_terms.py`.
