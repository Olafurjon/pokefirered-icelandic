# Field Move Dialogue Standardization

## Goal

Remove the remaining English field-move names and related mixed-language text from visible Icelandic dialogue, while keeping natural Icelandic grammar and preventing translation generators from restoring the old wording.

## Terminology

Use the established Icelandic move names whenever the move itself is named:

| English | Icelandic |
| --- | --- |
| CUT | HÖGGVA |
| FLY | FLUG |
| STRENGTH | STYRKUR |
| DIG | GRAFA |
| SHOCK WAVE | STUÐBYLGJA |
| SONICBOOM | HLJÓÐBYLGJA |
| WITHDRAW | SKELVÖRN |
| SAFARI ZONE | SAFARI SVÆÐI |

Use `HÖGGVA` consistently as both the move name and the action associated with removing small trees. Prompts and explanatory prose should be rewritten around the infinitive where needed, for example `Viltu höggva tréð?`, instead of inserting it into an unnatural phrase.

## Dialogue Changes

Update visible dialogue and quest-log text in Cerulean City, Vermilion City, S.S. Anne, Route 2, Route 14, Celadon Gym, and shared field-move scripts where the English names remain.

The Cerulean Slowbro demonstration will be fully Icelandic:

- `SLJÓNATAN, punch!` becomes `SLJÓNATAN, kýldu!`
- `SONICBOOM` becomes `HLJÓÐBYLGJA`
- the remaining English action lines become natural Icelandic descriptions
- `SKELVÖRN` remains unchanged

`SHOCK WAVE` will be renamed to `STUÐBYLGJA` in the canonical move-name table. Its existing description may continue to describe the attack as a rapid electrical wave.

## Source Of Truth

Apply each correction in both places where applicable:

1. Runtime text and canonical move-name data used by the ROM.
2. Icelandic translation batch generators that can recreate those files.

Update the Icelandic terminology reference with the approved mappings. This keeps later translation work and future games consistent.

## Regression Protection

Extend the Icelandic term checker to flag visible uses of the English names covered by this change, including `SAFARI ZONE`. Rules must be scoped so identifiers, comments, and legitimate technical constants are not rejected.

Add focused regression tests for the canonical move mappings and representative corrected dialogue. Existing translation and build checks remain authoritative.

## Verification

Before opening a pull request:

1. Run the Icelandic terminology checker and focused translation tests.
2. Search runtime text and translation generators for the old visible terms.
3. Build the modern ROM successfully.
4. Review the diff for control-code, capitalization, and line-wrapping regressions.

## Scope

This change is limited to the reported field-move terminology, the Cerulean Slowbro sequence, Safari terminology, and the safeguards needed to keep those fixes stable. A broader rewrite of unrelated dialogue is outside this batch.
