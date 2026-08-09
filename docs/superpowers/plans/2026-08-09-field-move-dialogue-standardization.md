# Field Move Dialogue Standardization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the reported English move and Safari terminology with consistent Icelandic text in the ROM and its translation generators, including the approved `HÖGGVA` and `STUÐBYLGJA` names.

**Architecture:** Canonical move names remain in `move_names.h`; visible map, script, and quest-log prose uses those names with natural Icelandic sentence structure. The terminology scanner protects runtime text, while focused unit tests protect canonical mappings and generated translation source text.

**Tech Stack:** C data tables, event-script text, Python 3 `unittest`, regex-based terminology checks, GNU Make through WSL.

## Global Constraints

- Use `HÖGGVA`, `FLUG`, `STYRKUR`, `GRAFA`, `LEIFTUR`, `STUÐBYLGJA`, `HLJÓÐBYLGJA`, `SKELVÖRN`, and `SAFARI SVÆÐI` as approved terminology.
- Rewrite prose around `HÖGGVA` where necessary instead of forcing the infinitive into an unnatural sentence.
- Preserve control codes, placeholders, capitalization, and dialogue pagination.
- Update runtime sources and every Icelandic generator that can recreate the corrected text.
- Do not change unrelated dialogue or gameplay behavior.

---

### Task 1: Teach The Terminology Scanner The Approved Move Names

**Files:**
- Modify: `tools/icelandic/test_translation_sanity.py`
- Modify: `tools/icelandic/check_terms.py`

**Interfaces:**
- Consumes: `check_terms.Rule`, `check_terms.scan_file()`, and `check_terms.DEFAULT_INCLUDE`.
- Produces: scanner rule IDs `cut-move`, `fly-move`, `strength-move`, `dig-move`, `flash-move`, `shock-wave-move`, and `sonic-boom-move`.

- [ ] **Step 1: Add failing scanner expectations**

Extend `TerminologyScannerTests.test_flags_visible_inconsistent_terms` with this visible string:

```python
'\t.string "CUT, FLY, STRENGTH, DIG, FLASH, SHOCK WAVE og SONICBOOM.$"\n'
```

Then add these assertions:

```python
self.assertIn("cut-move", found)
self.assertIn("fly-move", found)
self.assertIn("strength-move", found)
self.assertIn("dig-move", found)
self.assertIn("flash-move", found)
self.assertIn("shock-wave-move", found)
self.assertIn("sonic-boom-move", found)
```

Extend `test_accepts_approved_icelandic_terms` with:

```python
'\t.string "HÖGGVA, FLUG, STYRKUR, GRAFA, LEIFTUR, STUÐBYLGJA, HLJÓÐBYLGJA og SAFARI SVÆÐI.$"\n'
```

- [ ] **Step 2: Run the scanner test and confirm failure**

Run:

```powershell
python -m unittest tools.icelandic.test_translation_sanity.TerminologyScannerTests -v
```

Expected: `test_flags_visible_inconsistent_terms` fails because the seven new rule IDs are absent.

- [ ] **Step 3: Add scoped scanner rules and script coverage**

Add `data/scripts` to `DEFAULT_INCLUDE`, then add uppercase visible-text rules beside the existing field-move rules:

```python
Rule("cut-move", re.compile(r"\bCUT\b"), "HÖGGVA"),
Rule("fly-move", re.compile(r"\bFLY\b"), "FLUG"),
Rule("strength-move", re.compile(r"\bSTRENGTH\b"), "STYRKUR"),
Rule("dig-move", re.compile(r"\bDIG\b"), "GRAFA"),
Rule("flash-move", re.compile(r"\bFLASH\b"), "LEIFTUR"),
Rule("shock-wave-move", re.compile(r"\bSHOCK\s+WAVE\b"), "STUÐBYLGJA"),
Rule("sonic-boom-move", re.compile(r"\bSONICBOOM\b"), "HLJÓÐBYLGJA"),
```

The uppercase-only patterns avoid matching English prose such as Pokédex descriptions and source comments.

- [ ] **Step 4: Run the focused scanner tests**

Run:

```powershell
python -m unittest tools.icelandic.test_translation_sanity.TerminologyScannerTests -v
```

Expected: all `TerminologyScannerTests` pass.

- [ ] **Step 5: Commit the scanner protection**

```powershell
git add tools/icelandic/check_terms.py tools/icelandic/test_translation_sanity.py
git commit -m "Detect untranslated field move names"
```

---

### Task 2: Correct Canonical Move Names And The Terminology Reference

**Files:**
- Modify: `tools/icelandic/test_translation_sanity.py`
- Modify: `src/data/text/move_names.h`
- Modify: `docs/icelandic_translation_reference.md`

**Interfaces:**
- Consumes: `MOVE_CUT` and `MOVE_SHOCK_WAVE` constants.
- Produces: canonical display names `HÖGGVA` and `STUÐBYLGJA` used by battle, party, and summary screens.

- [ ] **Step 1: Add a failing canonical-name test**

Add this method to `GameplaySanityTests`:

```python
def test_reported_move_names_are_icelandic(self) -> None:
    move_names = (self.root / "src" / "data" / "text" / "move_names.h").read_text(encoding="utf-8")

    for snippet in [
        '[MOVE_CUT]           = _("HÖGGVA")',
        '[MOVE_FLY]           = _("FLUG")',
        '[MOVE_STRENGTH]      = _("STYRKUR")',
        '[MOVE_DIG]           = _("GRAFA")',
        '[MOVE_FLASH]         = _("LEIFTUR")',
        '[MOVE_SONIC_BOOM]    = _("HLJÓÐBYLGJA")',
        '[MOVE_WITHDRAW]      = _("SKELVÖRN")',
        '[MOVE_SHOCK_WAVE]    = _("STUÐBYLGJA")',
    ]:
        self.assertIn(snippet, move_names)
```

- [ ] **Step 2: Run the canonical-name test and confirm failure**

Run:

```powershell
python -m unittest tools.icelandic.test_translation_sanity.GameplaySanityTests.test_reported_move_names_are_icelandic -v
```

Expected: FAIL because `MOVE_CUT` is `SKURÐUR` and `MOVE_SHOCK_WAVE` is `ÁFALLABYLGJA`.

- [ ] **Step 3: Update the canonical names and reference table**

Change the two entries in `move_names.h` to:

```c
[MOVE_CUT]           = _("HÖGGVA"),
[MOVE_SHOCK_WAVE]    = _("STUÐBYLGJA"),
```

Add the complete approved mapping table to the moves section of `docs/icelandic_translation_reference.md`, including the note that `HÖGGVA` is also the preferred verb for removing small trees.

- [ ] **Step 4: Run the canonical-name test**

Run:

```powershell
python -m unittest tools.icelandic.test_translation_sanity.GameplaySanityTests.test_reported_move_names_are_icelandic -v
```

Expected: PASS.

- [ ] **Step 5: Commit canonical terminology**

```powershell
git add src/data/text/move_names.h docs/icelandic_translation_reference.md tools/icelandic/test_translation_sanity.py
git commit -m "Standardize Icelandic field move names"
```

---

### Task 3: Replace Legacy Terms In Runtime Dialogue

**Files:**
- Modify: `data/scripts/field_moves.inc`
- Modify: `src/data/text/quest_log.h`
- Modify: `data/maps/CeruleanCity/text.inc`
- Modify: `data/maps/CeruleanCity_Gym/text.inc`
- Modify: `data/maps/CeruleanCity_House1/text.inc`
- Modify: `data/maps/CeruleanCity_House2/text.inc`
- Modify: `data/maps/CeladonCity_Gym/text.inc`
- Modify: `data/maps/Route2_House/text.inc`
- Modify: `data/maps/Route14/text.inc`
- Modify: `data/maps/VermilionCity_Gym/text.inc`
- Modify: `data/maps/VermilionCity_PokemonFanClub/text.inc`
- Modify: `data/maps/SSAnne_2F_Corridor/text.inc`
- Modify: `data/maps/SSAnne_2F_Room3/text.inc`
- Modify: `data/maps/SSAnne_3F_Corridor/text.inc`
- Modify: `data/maps/SSAnne_B1F_Room5/text.inc`
- Modify: `data/maps/SSAnne_CaptainsOffice/text.inc`

**Interfaces:**
- Consumes: canonical move names from Task 2 and existing event-script control codes.
- Produces: fully Icelandic visible dialogue with unchanged labels and script references.

- [ ] **Step 1: Run the repository terminology check and capture the expected failures**

Run:

```powershell
python tools/icelandic/check_terms.py --root . --max-errors 100
```

Expected: FAIL with `cut-move`, `fly-move`, `strength-move`, `dig-move`, `flash-move`, and `sonic-boom-move` findings in runtime text.

- [ ] **Step 2: Replace straightforward move-name references**

Use these mappings in visible runtime strings while preserving each existing label and control code:

```text
CUT -> HÖGGVA
FLY -> FLUG
STRENGTH -> STYRKUR
DIG -> GRAFA
FLASH -> LEIFTUR
SONICBOOM -> HLJÓÐBYLGJA
```

Rewrite sentences around `HÖGGVA` rather than retaining forms such as `CUT-a`. Representative final wording:

```text
Vissirðu að þú getur höggvið niður lítil tré?
Jafnvel litla tréð fyrir framan búðina má höggva niður.
Nú máttu HÖGGVA hvenær sem er, jafnvel utan bardaga.
Kenndu vasaskrímslinu þínu HÖGGVA, þá getur það höggvið niður lítil tré.
```

Use `FLUG`, `STYRKUR`, `GRAFA`, and `LEIFTUR` as named moves in badge explanations, NPC speech, field prompts, and quest-log entries.

- [ ] **Step 3: Translate the complete Cerulean Slowbro sequence**

Keep the existing labels and replace the visible strings with these meanings and punctuation:

```text
Allt í lagi, SLJÓNATAN! Notaðu HLJÓÐBYLGJU!
SLJÓNATAN, kýldu!
SLJÓNATAN fékk sér blund…
SLJÓNATAN er að slóra…
SLJÓNATAN sneri sér undan…
SLJÓNATAN hunsaði skipanir…
```

Leave `SLJÓNATAN, SKELVÖRN!` unchanged.

- [ ] **Step 4: Run the terminology checker**

Run:

```powershell
python tools/icelandic/check_terms.py --root .
```

Expected: PASS with `No terminology suspects found.`

- [ ] **Step 5: Commit the runtime dialogue cleanup**

```powershell
git add data/scripts/field_moves.inc src/data/text/quest_log.h data/maps
git commit -m "Translate remaining field move dialogue"
```

---

### Task 4: Synchronize Translation Generators

**Files:**
- Modify: `tools/icelandic/test_translation_sanity.py`
- Modify: `tools/icelandic/create_cerulean_v1_batch.py`
- Modify: `tools/icelandic/create_cerulean_cleanup_v1_batch.py`
- Modify: `tools/icelandic/create_vermilion_v1_batch.py`
- Modify: `tools/icelandic/create_ssanne_v1_batch.py`
- Modify: `tools/icelandic/create_route11_diglett_route2_v1_batch.py`
- Modify: `tools/icelandic/create_fuchsia_safari_v1_batch.py`
- Modify: `tools/icelandic/generate_safe_translation_batch.py`

**Interfaces:**
- Consumes: the finalized runtime wording from Task 3.
- Produces: generators that cannot restore the replaced English move names or `SAFARI ZONE`.

- [ ] **Step 1: Add a failing generator regression test**

Add this method to `GameplaySanityTests`:

```python
def test_translation_generators_do_not_emit_legacy_field_terms(self) -> None:
    generators = [
        "create_cerulean_v1_batch.py",
        "create_cerulean_cleanup_v1_batch.py",
        "create_vermilion_v1_batch.py",
        "create_ssanne_v1_batch.py",
        "create_route11_diglett_route2_v1_batch.py",
        "create_fuchsia_safari_v1_batch.py",
    ]
    pattern = re.compile(r"\b(?:CUT|FLY|STRENGTH|DIG|FLASH|SONICBOOM)\b|SAFARI ZONE")
    offenders: list[str] = []
    for filename in generators:
        path = self.root / "tools" / "icelandic" / filename
        if pattern.search(path.read_text(encoding="utf-8")):
            offenders.append(filename)

    self.assertEqual([], offenders)

    safe_batch = (self.root / "tools" / "icelandic" / "generate_safe_translation_batch.py").read_text(encoding="utf-8")
    self.assertIn('"SAFARI ZONE": "SAFARI SVÆÐI"', safe_batch)
```

- [ ] **Step 2: Run the generator test and confirm failure**

Run:

```powershell
python -m unittest tools.icelandic.test_translation_sanity.GameplaySanityTests.test_translation_generators_do_not_emit_legacy_field_terms -v
```

Expected: FAIL and list the six stale generators.

- [ ] **Step 3: Mirror the approved runtime wording in every generator**

Replace each stale output string with the corresponding final text from Task 3. Replace every generator occurrence of `SAFARI ZONE` with `SAFARI SVÆÐI`, and change the safe replacement mapping to:

```python
"SAFARI ZONE": "SAFARI SVÆÐI",
```

Do not rename Python files, dictionary keys that identify map labels, or source-code identifiers.

- [ ] **Step 4: Run the generator regression test**

Run:

```powershell
python -m unittest tools.icelandic.test_translation_sanity.GameplaySanityTests.test_translation_generators_do_not_emit_legacy_field_terms -v
```

Expected: PASS.

- [ ] **Step 5: Commit generator synchronization**

```powershell
git add tools/icelandic
git commit -m "Keep translation generators aligned with move terms"
```

---

### Task 5: Protect Move-Learning And Forgetting Text

**Files:**
- Modify: `tools/icelandic/test_translation_sanity.py`
- Verify: `src/battle_message.c`
- Verify: `src/strings.c`

**Interfaces:**
- Consumes: battle-string, party-menu, evolution, TM/HM, and summary-screen text constants.
- Produces: regression coverage proving the current ROM source has Icelandic prompts on every move-learning and forgetting path.

- [ ] **Step 1: Add exact regression coverage for all learning paths**

Add this method to `GameplaySanityTests`:

```python
def test_move_learning_and_forgetting_prompts_are_icelandic(self) -> None:
    battle_messages = (self.root / "src" / "battle_message.c").read_text(encoding="utf-8")
    shared_strings = (self.root / "src" / "strings.c").read_text(encoding="utf-8")

    for snippet in [
        'sText_TryToLearnMove1[] = _("{B_BUFF1} reynir að\\nlæra {B_BUFF2}.")',
        'sText_TryToLearnMove2[] = _("En {B_BUFF1} getur ekki lært\\nmeira en fjögur brögð.")',
        'sText_TryToLearnMove3[] = _("Eyða bragði til að búa\\ntil pláss fyrir {B_BUFF2}?")',
        'sText_PkmnForgotMove[] = _("{B_BUFF1} gleymdi\\n{B_BUFF2}.")',
        'sText_StopLearningMove[] = _("{PAUSE 32}Hætta að læra\\n{B_BUFF2}?")',
    ]:
        self.assertIn(snippet, battle_messages)

    for snippet in [
        'gText_PkmnNeedsToReplaceMove[] = _("{STR_VAR_1} vill læra hreyfinguna',
        'gText_WhichMoveToForget[] = _("Hvaða hreyfingu á að gleyma?',
        'gText_12PoofForgotMove[] = _("1, {PAUSE 0x0F}2, og',
        'gText_MonIsTryingToLearnMove[] = _("{STR_VAR_1} er að reyna að læra',
        'gText_GiveUpTryingToTeachNewMove[] = _("Gefast upp á að reyna að kenna nýja',
        'gText_PokeSum_Controls_PickDelete[] = _("{DPAD_UPDOWN}VELJA {A_BUTTON}EYÐA")',
    ]:
        self.assertIn(snippet, shared_strings)
```

- [ ] **Step 2: Run the focused regression test**

Run:

```powershell
python -m unittest tools.icelandic.test_translation_sanity.GameplaySanityTests.test_move_learning_and_forgetting_prompts_are_icelandic -v
```

Expected: PASS against the current translated source. If any assertion fails, translate that exact source constant without altering its placeholders or control codes, then rerun until it passes.

- [ ] **Step 3: Search the active learning flow for English prompt fragments**

Run:

```powershell
rg -n -i 'delete a move|make room for|which move|stop learning|give up trying|forgot move|trying to learn' src/battle_message.c src/strings.c
```

Expected: no English visible strings; source-code comments may remain English.

- [ ] **Step 4: Commit the move-learning regression coverage**

```powershell
git add tools/icelandic/test_translation_sanity.py src/battle_message.c src/strings.c
git commit -m "Protect Icelandic move learning prompts"
```

---

### Task 6: Full Verification And Branch Review

**Files:**
- Verify: all files changed in Tasks 1-4

**Interfaces:**
- Consumes: scanner, tests, runtime strings, canonical names, generators, and move-learning coverage from Tasks 1-5.
- Produces: a buildable branch ready for pull-request review.

- [ ] **Step 1: Run the full Python sanity suite**

Run:

```powershell
python -m unittest tools.icelandic.test_translation_sanity -v
```

Expected: all tests pass.

- [ ] **Step 2: Run the terminology checker**

Run:

```powershell
python tools/icelandic/check_terms.py --root .
```

Expected: `No terminology suspects found.`

- [ ] **Step 3: Search runtime and generators for legacy visible terms**

Run:

```powershell
rg -n '\b(CUT|FLY|STRENGTH|DIG|FLASH|SONICBOOM)\b|SHOCK WAVE|SAFARI ZONE' data/maps data/scripts src/data/text tools/icelandic
```

Expected: no visible legacy output strings. Technical identifiers, English replacement-map keys, and source comments must be manually confirmed as non-visible if present.

- [ ] **Step 4: Build the modern ROM through WSL**

Run:

```powershell
wsl -e bash -lc "cd /mnt/c/Github/pokefirered && make -j2 modern"
```

Expected: exit code `0` and a rebuilt `pokefirered_modern.gba`.

- [ ] **Step 5: Review the complete branch diff**

Run:

```powershell
git diff --check origin/main...HEAD
git diff --stat origin/main...HEAD
git status --short
```

Expected: no whitespace errors, only the intended design, scanner, tests, terminology, dialogue, and generator changes, and a clean worktree.
