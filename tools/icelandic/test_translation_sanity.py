from __future__ import annotations

import ast
import json
import re
import tempfile
import textwrap
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_terms


def asm_string_literals(path: Path, label: str) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    try:
        start = lines.index(f"{label}::") + 1
    except ValueError as exc:
        raise AssertionError(f"missing ASM label {label} in {path}") from exc

    literals: list[str] = []
    for line in lines[start:]:
        match = re.match(r'\s*\.string\s+"((?:\\"|[^"])*)"\s*$', line)
        if match:
            literals.append(match.group(1).replace(r'\"', '"'))
            continue
        if literals:
            break
    if not literals:
        raise AssertionError(f"missing ASM strings for {label} in {path}")
    return literals


def normalize_dialogue(text: str) -> str:
    text = text.removesuffix("$")
    text = text.replace(r"\p", "\n\n").replace(r"\n", "\n").replace(r"\l", "\n")
    return "\n\n".join(" ".join(page.split()) for page in re.split(r"\n\s*\n", text))


def normalized_asm_dialogue(path: Path, label: str) -> str:
    return normalize_dialogue("".join(asm_string_literals(path, label)))


def generator_translations(path: Path) -> dict[str, str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "TRANSLATIONS" for target in node.targets):
            continue
        if not isinstance(node.value, ast.Dict):
            break
        translations: dict[str, str] = {}
        for key_node, value_node in zip(node.value.keys, node.value.values):
            if not isinstance(key_node, ast.Constant) or not isinstance(key_node.value, str):
                continue
            if not isinstance(value_node, ast.Call) or not value_node.args:
                continue
            raw = ast.literal_eval(value_node.args[0])
            translations[key_node.value] = textwrap.dedent(raw).strip()
        return translations
    raise AssertionError(f"missing TRANSLATIONS dictionary in {path}")


class TerminologyScannerTests(unittest.TestCase):
    def test_flags_visible_inconsistent_terms(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            text_file = root / "data" / "maps" / "TestMap" / "text.inc"
            text_file.parent.mkdir(parents=True)
            text_file.write_text(
                'Test_Text::\n'
                '\t.string "POKéMON CENTER sells POTIONS near CYCLING ROAD.$"\n'
                '\t.string "Viltu fyllja formið? Við alum upp eggið. Gagnhögg! SPEED!$"\n'
                '\t.string "Storage System, SURF, VIRIDIAN FOREST, NIDORAN og SKORDÝ Vasaskrímsli.$"\n'
                '\t.string "MT. MOON, MOONFJALL, ROCK SMASH og WATERFALL.$"\n'
                '\t.string "CUT, FLY, STRENGTH, DIG, FLASH, SHOCK WAVE og SONICBOOM.$"\n'
                '\t.string "LIGHT SCREEN, GAGNÁTAK, ICE BEAM, BODY SLAM og SWORDS DANCE.$"\n'
                '\t.string "SAFEGUARD, BIND, MIST, UPROAR, STOCKPILE, RAGE, ENCORE, CURSE, SPIKES, TORMENT, TAUNT og WISH.$"\n'
                '\t.string "SAND TOMB, LEECH SEED, SUBSTITUTE, SKETCH, NIGHTMARE, PERISH SONG, SPIT UP, SWALLOW og HEAT WAVE.$"\n'
                '\t.string "SUPER ROD, EXP. SHARE, SILPH SCOPE, REPEL og FULL HEAL.$"\n'
                '\t.string "SÓKN, Vasaskrímsli MIÐSTÖÐ, ELÍTUFERNINGUR, PROF. OAK og KORT BORGAR.$"\n'
                '\t.string "DEFENSE, SP. ATK og SP. DEF eru stöðuheiti.$"\n'
                '\t.string "BIKERS hittu WARDEN í Vasaskrímsla-MIÐSTÖÐ.$"\n'
                '\t.string "TELEPORTER birtist á\\nPC skjánum.$"\n'
                '\t.string "Handtekin vasaskrímsli virtust vera veidd og annað var handtekið.$"\n'
                '\t.string "VASAFLAUTAN, LEMONADE, REVIVE, OLD AMBER, RÁÐGÁTUBER og NUGGET.$"\n'
                '\t.string "SOFTBOILED, MILK DRINK, ILMANGAN og KALA.$"\n',
                encoding="utf-8",
            )
            nature_file = root / "src" / "data" / "text" / "nature_names.h"
            nature_file.parent.mkdir(parents=True)
            nature_file.write_text('static const u8 sQuirkyNatureName[] = _("QUIRKY");\n', encoding="utf-8")

            rows = check_terms.scan_file(text_file, root) + check_terms.scan_file(nature_file, root)
            found = {row["rule"] for row in rows}

        self.assertIn("pokemon-term", found)
        self.assertIn("potion", found)
        self.assertIn("cycling-road", found)
        self.assertIn("questionnaire-fill", found)
        self.assertIn("daycare-raise", found)
        self.assertIn("critical-hit", found)
        self.assertIn("speed-stat", found)
        self.assertIn("storage-system", found)
        self.assertIn("surf", found)
        self.assertIn("mt-moon", found)
        self.assertIn("rock-smash", found)
        self.assertIn("waterfall", found)
        self.assertIn("viridian-forest", found)
        self.assertIn("nidoran-species", found)
        self.assertIn("bug-species-phrase", found)
        self.assertIn("nature-name", found)
        self.assertIn("cut-move", found)
        self.assertIn("fly-move", found)
        self.assertIn("strength-move", found)
        self.assertIn("dig-move", found)
        self.assertIn("flash-move", found)
        self.assertIn("shock-wave-move", found)
        self.assertIn("sonic-boom-move", found)
        self.assertIn("move-name-alias", found)
        self.assertIn("item-name-alias", found)
        self.assertIn("attack-stat-alias", found)
        self.assertIn("defense-stat", found)
        self.assertIn("special-stat", found)
        self.assertIn("pokemon-center-alias", found)
        self.assertIn("elite-four-alias", found)
        self.assertIn("professor-oak-alias", found)
        self.assertIn("biker-class-alias", found)
        self.assertIn("warden-alias", found)
        self.assertIn("pc-computer", found)
        self.assertIn("teleporter", found)
        self.assertIn("capture-term", found)
        self.assertIn("poke-flute-alias", found)

    def test_accepts_approved_icelandic_terms(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            text_file = root / "data" / "maps" / "TestMap" / "text.inc"
            text_file.parent.mkdir(parents=True)
            text_file.write_text(
                'Test_Text::\n'
                '\t.string "VASaSKRÍMSLI fá SEYÐI við HJÓLAVEGINN.$"\n'
                '\t.string "HÖGGVA, FLUG, STYRKUR, GRAFA, LEIFTUR, STUÐBYLGJA, HLJÓÐBYLGJA og SAFARI SVÆÐI.$"\n',
                encoding="utf-8",
            )

            rows = check_terms.scan_file(text_file, root)

        self.assertEqual([], rows)

    def test_ignores_non_visible_map_json_identifiers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            map_file = root / "data" / "maps" / "TestMap" / "map.json"
            map_file.parent.mkdir(parents=True)
            map_file.write_text(
                '{\n'
                '  "id": "MAP_TEST_POKEMON_CENTER",\n'
                '  "layout": "LAYOUT_POKEMON_CENTER_1F"\n'
                '}\n',
                encoding="utf-8",
            )

            rows = check_terms.scan_file(map_file, root)

        self.assertEqual([], rows)

    def test_scans_visible_item_names_and_descriptions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            item_file = root / "src" / "data" / "items.json"
            item_file.parent.mkdir(parents=True)
            item_file.write_text(
                '[\n'
                '  {\n'
                '    "english": "SUPER ROD",\n'
                '    "description_english": "Hækkar SÓKN."\n'
                '  }\n'
                ']\n',
                encoding="utf-8",
            )

            rows = check_terms.scan_file(item_file, root)
            found = {row["rule"] for row in rows}

        self.assertIn("item-name-alias", found)
        self.assertIn("attack-stat-alias", found)

    def test_default_scan_includes_data_scripts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            script_file = root / "data" / "scripts" / "field_moves.inc"
            script_file.parent.mkdir(parents=True)
            script_file.write_text(
                'Test_Text::\n\t.string "Viltu nota STRENGTH?$"\n',
                encoding="utf-8",
            )

            discovered = check_terms.iter_files(root, check_terms.DEFAULT_INCLUDE)
            rows = [row for path in discovered for row in check_terms.scan_file(path, root)]

        self.assertIn(script_file, discovered)
        self.assertIn("strength-move", {row["rule"] for row in rows})

    def test_default_scan_includes_trainer_tower_nicknames(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tower_file = root / "src" / "trainer_tower_sets.c"
            tower_file.parent.mkdir(parents=True)
            tower_file.write_text('.nickname = _("NIDORAN♀"),\n', encoding="utf-8")

            discovered = check_terms.iter_files(root, check_terms.DEFAULT_INCLUDE)
            rows = check_terms.scan_file(tower_file, root)

        self.assertIn(tower_file, discovered)
        self.assertEqual(["nidoran-species"], [row["rule"] for row in rows])


class GameplaySanityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]

    def test_capture_dialogue_uses_fanga_terminology(self) -> None:
        department_store = (
            self.root / "data" / "maps" / "CeladonCity_DepartmentStore_3F" / "text.inc"
        ).read_text(encoding="utf-8")
        battle_messages = (self.root / "src" / "battle_message.c").read_text(encoding="utf-8")

        self.assertIn("Fönguð vasaskrímsli eru skráð", department_store)
        self.assertNotRegex(department_store, r"(?i)handtekin")
        self.assertIn("Það virtist vera fangað!", battle_messages)
        self.assertIn("{B_OPPONENT_MON1_NAME} var fangað!", battle_messages)
        self.assertIn("Gefa fangaða {B_OPPONENT_MON1_NAME}", battle_messages)
        self.assertNotRegex(battle_messages, r"(?i)(?:var|vera) veitt|veiddu \{B_OPPONENT_MON1_NAME\}")

        capture_texts = "\n".join(
            (self.root / relative_path).read_text(encoding="utf-8")
            for relative_path in [
                "data/text/help_system.inc",
                "data/text/pokedex_rating.inc",
                "data/maps/PokemonLeague_LancesRoom/text.inc",
                "data/maps/ViridianForest/text.inc",
                "data/maps/SafariZone_East_RestHouse/text.inc",
                "tools/icelandic/create_fuchsia_safari_v1_batch.py",
            ]
        )
        for expected in [
            "reynir að fanga það",
            "því að vera fangað",
            "ÞJÁLFARANNA sem fönguðu þau",
            "Vasaskrímslum með því að fanga",
            "Erfitt er að fanga þá og þjálfa",
            "fanga mér sterkari",
            "Hversu mörg fangaðirðu?",
            "Ég fangaði SÆLEGG!",
        ]:
            self.assertIn(expected, capture_texts)

        self.assertNotRegex(
            capture_texts,
            r"reynir að veiða það|vera veidd|sem veiddu þau|með því að veiða|"
            r"Erfitt er að veiða þá|veiða mér sterkari|Hversu mörg (?:veiddirðu|náðirðu)|"
            r"Ég náði SÆLEGGI",
        )

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

    def test_translation_generators_do_not_emit_legacy_field_terms(self) -> None:
        generators = [
            "create_cinnabar_v1_batch.py",
            "create_cerulean_v1_batch.py",
            "create_cerulean_cleanup_v1_batch.py",
            "create_cycling_road_v1_batch.py",
            "create_vermilion_v1_batch.py",
            "create_ssanne_v1_batch.py",
            "create_lavender_tower_v1_batch.py",
            "create_route11_diglett_route2_v1_batch.py",
            "create_route13_15_v1_batch.py",
            "create_fuchsia_safari_v1_batch.py",
        ]
        pattern = re.compile(
            r"\b(?:CUT|FLY|STRENGTH|DIG|FLASH|SONICBOOM)\b"
            r"|SAFARI(?:\s|\\n)+ZONE"
            r"|TEAM ROCKET"
            r"|VASASKRÍMSLAMIÐSTÖÐ"
            r"|Vasaskrímslamiðstöð"
            r"|PROF\.\s+OAK"
        )
        offenders: list[str] = []
        for filename in generators:
            path = self.root / "tools" / "icelandic" / filename
            if pattern.search(path.read_text(encoding="utf-8")):
                offenders.append(filename)

        self.assertEqual([], offenders)

        safe_batch = (self.root / "tools" / "icelandic" / "generate_safe_translation_batch.py").read_text(encoding="utf-8")
        self.assertIn('"SAFARI ZONE": "SAFARI SVÆÐI"', safe_batch)

    def test_polished_field_move_dialogue_and_line_lengths(self) -> None:
        expected = [
            (
                "data/scripts/field_moves.inc",
                "Text_UseStrength",
                "Þetta er stór steinn. Vasaskrímsli gæti fært hann.\n\nViltu nota hreyfinguna STYRKUR?",
            ),
            (
                "data/scripts/field_moves.inc",
                "Text_MonUsedStrengthCanMoveBoulders",
                "{STR_VAR_1} notaði hreyfinguna STYRKUR!\n\nNú er hægt að færa stóra steina!",
            ),
            (
                "data/scripts/field_moves.inc",
                "Text_MonMayPushBoulder",
                "Þetta er stór steinn. Vasaskrímsli gæti fært hann.",
            ),
            (
                "data/maps/CeladonCity_Gym/text.inc",
                "CeladonCity_Gym_Text_ExplainRainbowBadgeTakeThis",
                "RAINBOWBADGE mun láta vasaskrímsli allt að Lv. 50 hlýða.\n\nÞú getur líka notað hreyfinguna STYRKUR innan og utan bardaga.\n\nVinsamlegast taktu þetta líka með þér.",
            ),
            (
                "data/text/pokedex_rating.inc",
                "PokedexRating_Text_LessThan20",
                "Það lítur út fyrir að þú sért á réttri leið!\n\nÉg gaf einum AÐSTOÐARMANNA minna HM fyrir LEIFTUR.\n\nVertu viss um að sækja það!",
            ),
            (
                "data/maps/SSAnne_2F_Corridor/text.inc",
                "SSAnne_2F_Corridor_Text_RivalPostBattle",
                "{RIVAL}: Ég heyrði að það væri meistari í HÖGGVA um borð.\n\nEn hann var bara sjóveikur gamall maður!\n\nHÖGGVA er mjög gagnlegt. Það kemur sér vel.\n\nÞú ættir líka að hitta hann. Sjáumst!",
            ),
            (
                "data/maps/SSAnne_3F_Corridor/text.inc",
                "SSAnne_3F_Corridor_Text_CaptainTeachesCutToMons",
                "SKIPSTJÓRINN er sverðmeistari. Hann er magnaður í HÖGGVA.\n\nÞeir segja að hann kenni jafnvel vasaskrímslum HÖGGVA!",
            ),
            (
                "data/maps/SSAnne_CaptainsOffice/text.inc",
                "SSAnne_CaptainsOffice_Text_ThankYouHaveHMForCut",
                "SKIPSTJÓRI: Úff! Takk fyrir! Mér líður miklu betur núna.\n\nViltu sjá leynilegu tæknina sem heitir HÖGGVA?\n\nÉg gæti kennt þér HÖGGVA ef ég væri ekki svona veikur...\n\nÉg veit! Þú mátt fá þessa FÖLDU VÉL!\n\nKenndu vasaskrímslinu þínu HÖGGVA.\n\nÞá getur það höggvið tré hvenær sem er!",
            ),
            (
                "data/maps/SSAnne_CaptainsOffice/text.inc",
                "SSAnne_CaptainsOffice_Text_ExplainCut",
                "Með HÖGGVA má höggva niður lítil tré.\n\nPrófaðu það á trjánum í kringum VERMILION BORG!",
            ),
            (
                "data/maps/VermilionCity_PokemonFanClub/text.inc",
                "VermilionCity_PokemonFanClub_Text_ExplainBikeVoucher",
                "Farðu með REIÐHJÓLSMIÐANN í HJÓLABÚÐINA í CERULEAN BORG.\n\nSkiptu honum fyrir REIÐHJÓL, alveg ókeypis!\n\nEkki hafa áhyggjur. GEIGHEGRINN minn kann FLUG.\n\nHann flytur mig hvert sem ég þarf.\n\nÞess vegna þarf ég ekkert REIÐHJÓL.\n\nÉg vona að þér líki að hjóla!",
            ),
            (
                "data/maps/CeruleanCity_House1/text.inc",
                "CeruleanCity_House1_Text_SpeedStatFly",
                "HRAÐI allra vasaskrímslanna þinna hækkar örlítið.\n\nÞað leyfir þér líka að nota FLUG utan bardaga.",
            ),
            (
                "data/maps/CeruleanCity_House1/text.inc",
                "CeruleanCity_House1_Text_ObeyLv50Strength",
                "Vasaskrímsli upp að Lv. 50 hlýða þér.\n\nÞað gildir líka um þau sem þú færð í skiptum.\n\nVasaskrímsli á hærri stigum verða þó óstýrilát í bardaga.\n\nÞú getur líka notað hreyfinguna STYRKUR utan bardaga.",
            ),
            (
                "data/maps/SSAnne_B1F_Room5/text.inc",
                "SSAnne_B1F_Room5_Text_MachokeHasStrengthToMoveRocks",
                "Félagi minn AFLGARPUR er ofursterkur!\n\nHann kann hreyfinguna STYRKUR og getur fært stóra steina!",
            ),
        ]

        for relative_path, label, wanted in expected:
            path = self.root / relative_path
            with self.subTest(label=label):
                self.assertEqual(wanted, normalized_asm_dialogue(path, label))
                for literal in asm_string_literals(path, label):
                    for segment in re.split(r"\\[npl]", literal):
                        visible = re.sub(r"\{[^}]+\}", "", segment).removesuffix("$")
                        self.assertLessEqual(len(visible), 36, visible)

    def test_field_move_generators_match_runtime(self) -> None:
        parity = [
            (
                "create_cerulean_cleanup_v1_batch.py",
                "CeruleanCity_Text_IfSlowbroWasntThereCouldCutTree",
                "data/maps/CeruleanCity/text.inc",
            ),
            (
                "create_cerulean_cleanup_v1_batch.py",
                "CeruleanCity_House1_Text_ObeyLv30Cut",
                "data/maps/CeruleanCity_House1/text.inc",
            ),
            (
                "create_cerulean_cleanup_v1_batch.py",
                "CeruleanCity_House1_Text_SpeedStatFly",
                "data/maps/CeruleanCity_House1/text.inc",
            ),
            (
                "create_cerulean_cleanup_v1_batch.py",
                "CeruleanCity_House1_Text_ObeyLv50Strength",
                "data/maps/CeruleanCity_House1/text.inc",
            ),
            (
                "create_route11_diglett_route2_v1_batch.py",
                "Route2_House_Text_FaintedMonsCanUseFieldMoves",
                "data/maps/Route2_House/text.inc",
            ),
            (
                "create_ssanne_v1_batch.py",
                "SSAnne_2F_Corridor_Text_RivalPostBattle",
                "data/maps/SSAnne_2F_Corridor/text.inc",
            ),
            (
                "create_ssanne_v1_batch.py",
                "SSAnne_3F_Corridor_Text_CaptainTeachesCutToMons",
                "data/maps/SSAnne_3F_Corridor/text.inc",
            ),
            (
                "create_ssanne_v1_batch.py",
                "SSAnne_B1F_Room5_Text_MachokeHasStrengthToMoveRocks",
                "data/maps/SSAnne_B1F_Room5/text.inc",
            ),
            (
                "create_ssanne_v1_batch.py",
                "SSAnne_CaptainsOffice_Text_ThankYouHaveHMForCut",
                "data/maps/SSAnne_CaptainsOffice/text.inc",
            ),
            (
                "create_ssanne_v1_batch.py",
                "SSAnne_CaptainsOffice_Text_ExplainCut",
                "data/maps/SSAnne_CaptainsOffice/text.inc",
            ),
            (
                "create_vermilion_v1_batch.py",
                "VermilionCity_PokemonFanClub_Text_ExplainBikeVoucher",
                "data/maps/VermilionCity_PokemonFanClub/text.inc",
            ),
            (
                "create_fuchsia_safari_v1_batch.py",
                "FuchsiaCity_House1_Text_WardenIsOldHasFalseTeeth",
                "data/maps/FuchsiaCity_House1/text.inc",
            ),
            (
                "create_fuchsia_safari_v1_batch.py",
                "SafariZone_East_Text_KeepAnyItemFoundOnSafari",
                "data/maps/SafariZone_North_RestHouse/text.inc",
            ),
            (
                "create_fuchsia_safari_v1_batch.py",
                "SafariZone_East_Text_PrizeInDeepestPartOfSafariZone",
                "data/maps/SafariZone_North_RestHouse/text.inc",
            ),
        ]
        cache: dict[str, dict[str, str]] = {}
        for generator, label, runtime in parity:
            if generator not in cache:
                cache[generator] = generator_translations(
                    self.root / "tools" / "icelandic" / generator
                )
            translations = cache[generator]
            with self.subTest(generator=generator, label=label):
                self.assertIn(label, translations)
                self.assertEqual(
                    normalized_asm_dialogue(self.root / runtime, label),
                    normalize_dialogue(translations[label]),
                )

    def test_move_learning_and_forgetting_prompts_are_icelandic(self) -> None:
        battle_messages = (self.root / "src" / "battle_message.c").read_text(encoding="utf-8")
        shared_strings = (self.root / "src" / "strings.c").read_text(encoding="utf-8")
        fuchsia_move_deleter = (
            self.root / "data" / "maps" / "FuchsiaCity_House3" / "text.inc"
        ).read_text(encoding="utf-8")

        battle_definitions = [
            'sText_PkmnLearnedMove[] = _("{B_BUFF1} lærði\\n{B_BUFF2}!{WAIT_SE}")',
            'sText_TryToLearnMove1[] = _("{B_BUFF1} reynir að\\nlæra {B_BUFF2}.")',
            'sText_TryToLearnMove2[] = _("En {B_BUFF1} getur ekki lært\\nmeira en fjögur brögð.")',
            'sText_TryToLearnMove3[] = _("Eyða bragði til að búa\\ntil pláss fyrir {B_BUFF2}?")',
            'sText_PkmnForgotMove[] = _("{B_BUFF1} gleymdi\\n{B_BUFF2}.")',
            'sText_StopLearningMove[] = _("{PAUSE 32}Hætta að læra\\n{B_BUFF2}?")',
            'sText_DidNotLearnMove[] = _("{B_BUFF1} lærði ekki\\n{B_BUFF2}.")',
            'sText_PkmnLearnedMove2[] = _("{B_ATK_NAME_WITH_PREFIX} lærði\\n{B_BUFF1}!")',
        ]
        for definition in battle_definitions:
            self.assertIn(definition, battle_messages)

        shared_definitions = [
            'gText_PkmnLearnedMove3[] = _("{STR_VAR_1} lærði\\n{STR_VAR_2}!")',
            'gText_PkmnNeedsToReplaceMove[] = _("{STR_VAR_1} vill læra hreyfinguna\\n{STR_VAR_2}.\\pHins vegar kann {STR_VAR_1} nú þegar\\nfjórar hreyfingar.\\pÁ að eyða hreyfingu og\\nskipta henni út fyrir {STR_VAR_2}?")',
            'gText_StopLearningMove2[] = _("Hætta að reyna að kenna\\n{STR_VAR_2}?")',
            'gText_MoveNotLearned[] = _("{STR_VAR_1} lærði ekki hreyfinguna\\n{STR_VAR_2}.{PAUSE_UNTIL_PRESS}")',
            'gText_WhichMoveToForget[] = _("Hvaða hreyfingu á að gleyma?{PAUSE_UNTIL_PRESS}")',
            'gText_12PoofForgotMove[] = _("1, {PAUSE 0x0F}2, og{PAUSE 0x0F}‥ {PAUSE 0x0F}‥ {PAUSE 0x0F}‥ {PAUSE 0x0F}{PLAY_SE SE_BALL_BOUNCE_1}Púff!\\p{STR_VAR_1} gleymdi hvernig á að\\nnota {STR_VAR_2}.\\pOg...{PAUSE_UNTIL_PRESS}")',
            'gText_MonIsTryingToLearnMove[] = _("{STR_VAR_1} er að reyna að læra\\n{STR_VAR_2}.\\pEn {STR_VAR_1} getur ekki lært fleiri\\nen fjórar hreyfingar.\\pEyða eldri hreyfingu til að gera\\npláss fyrir {STR_VAR_2}?")',
            'gText_MonLearnedMove[] = _("{STR_VAR_1} lærði\\n{STR_VAR_2}.")',
            'gText_StopLearningMove[] = _("Hætta að læra {STR_VAR_2}?")',
            'gText_1_2_and_Poof[] = _("{PAUSE 0x20}1, {PAUSE 0x0F}2, og {PAUSE 0x0F}‥ {PAUSE 0x0F}‥ {PAUSE 0x0F}‥ {PAUSE 0x0F}{PLAY_SE SE_BALL_BOUNCE_1}Púff!")',
            'gText_MonForgotOldMoveAndMonLearnedNewMove[] = _("{STR_VAR_1} gleymdi {STR_VAR_3}.\\pOg‥\\p{STR_VAR_1}\\nlærði {STR_VAR_2}.")',
            'gText_GiveUpTryingToTeachNewMove[] = _("Hætta að reyna að kenna\\n{STR_VAR_1} nýja hreyfingu?")',
            'gText_WhichMoveShouldBeForgotten[] = _("Hvaða hreyfingu á að gleyma?")',
            'gText_PokeSum_Controls_PickDelete[] = _("{DPAD_UPDOWN}VELJA {A_BUTTON}EYÐA")',
            'gText_Counting_1[] = _("1,")',
            'gText_Counting_2And[] = _("2, og ‥ ‥ ‥")',
            'gText_Poof[] = _("Púff!")',
            'gText_MonForgotMove[] = _("{DYNAMIC 0x00} gleymdi\\n{DYNAMIC 0x01}.")',
            'gText_And[] = _("Og‥")',
            'gText_MonLearnedTMHM[] = _("{DYNAMIC 0x00} lærði\\n{DYNAMIC 0x01}!")',
        ]
        for definition in shared_definitions:
            self.assertIn(definition, shared_strings)

        fuchsia_definitions = [
            """FuchsiaCity_House3_Text_WouldYouLikeToForgetMove::
    .string "Óli gerði mig atvinnulausan…\\p"
    .string "Nú einbeiti ég mér að ræktinni!\\p"
    .string "En ég get enn látið Vasaskrímsli\\n"
    .string "gleyma brögðum.\\p"
    .string "Viltu að ég geri það?$""",
            """FuchsiaCity_House3_Text_WhichMonShouldForgetMove::
    .string "Hvaða Vasaskrímsli á að gleyma\\n"
    .string "hreyfingu?$""",
            """FuchsiaCity_House3_Text_WhichMoveShouldBeForgotten::
    .string "Hvaða hreyfingu á að gleyma?$""",
            """FuchsiaCity_House3_Text_MonOnlyKnowsOneMove::
    .string "{STR_VAR_1} virðist aðeins kunna\\n"
    .string "eina hreyfingu…$""",
            """FuchsiaCity_House3_Text_MonsMoveShouldBeForgotten::
    .string "Hm! {STR_VAR_1}, {STR_VAR_2}? Á að\\n"
    .string "gleyma þessari hreyfingu?$""",
            """FuchsiaCity_House3_Text_MonHasForgottenMoveCompletely::
    .string "Það virkaði fullkomlega!\\p"
    .string "{STR_VAR_1} hefur gleymt {STR_VAR_2}\\n"
    .string "alveg.$""",
            """FuchsiaCity_House3_Text_ComeAgainToForgetOtherMoves::
    .string "Komdu aftur ef það eru aðrar\\n"
    .string "hreyfingar til að gleyma.$""",
            """FuchsiaCity_House3_Text_NoEggShouldKnowMoves::
    .string "Hvað? Ekkert EGG ætti að kunna\\n"
    .string "hreyfingar.$""",
        ]
        for definition in fuchsia_definitions:
            self.assertIn(definition, fuchsia_move_deleter)

    def test_first_partner_species_are_available_as_rare_grass_encounters(self) -> None:
        encounters_path = self.root / "src" / "data" / "wild_encounters.json"
        data = json.loads(encounters_path.read_text(encoding="utf-8"))

        expected = {
            ("MAP_VIRIDIAN_FOREST", "SPECIES_BULBASAUR"),
            ("MAP_ROUTE3", "SPECIES_CHARMANDER"),
            ("MAP_ROUTE24", "SPECIES_SQUIRTLE"),
        }
        found: set[tuple[str, str]] = set()
        for group in data["wild_encounter_groups"]:
            for encounter in group["encounters"]:
                land_mons = encounter.get("land_mons")
                if land_mons is None:
                    continue
                for mon in land_mons["mons"]:
                    pair = (encounter["map"], mon["species"])
                    if pair in expected:
                        found.add(pair)

        self.assertEqual(expected, found)

    def test_eevee_is_available_near_celadon(self) -> None:
        encounters_path = self.root / "src" / "data" / "wild_encounters.json"
        data = json.loads(encounters_path.read_text(encoding="utf-8"))

        expected_maps = {"MAP_ROUTE7", "MAP_ROUTE16"}
        found_maps: set[str] = set()
        for group in data["wild_encounter_groups"]:
            for encounter in group["encounters"]:
                if encounter["map"] not in expected_maps:
                    continue
                land_mons = encounter.get("land_mons")
                if land_mons is None:
                    continue
                if any(mon["species"] == "SPECIES_EEVEE" for mon in land_mons["mons"]):
                    found_maps.add(encounter["map"])

        self.assertEqual(expected_maps, found_maps)

    def test_trade_item_evolutions_use_direct_items(self) -> None:
        evolution_text = (self.root / "src" / "data" / "pokemon" / "evolution.h").read_text(encoding="utf-8")
        item_effects_text = (
            self.root / "src" / "data" / "pokemon" / "item_effects.h"
        ).read_text(encoding="utf-8")
        item_constants_text = (
            self.root / "include" / "constants" / "items.h"
        ).read_text(encoding="utf-8")

        expected = [
            "[SPECIES_POLIWHIRL]  = {{EVO_ITEM, ITEM_WATER_STONE, SPECIES_POLIWRATH},\n                            {EVO_ITEM, ITEM_KINGS_ROCK, SPECIES_POLITOED}}",
            "[SPECIES_SLOWPOKE]   = {{EVO_LEVEL, 37, SPECIES_SLOWBRO},\n                            {EVO_ITEM, ITEM_KINGS_ROCK, SPECIES_SLOWKING}}",
            "[SPECIES_ONIX]       = {{EVO_ITEM, ITEM_METAL_COAT, SPECIES_STEELIX}}",
            "[SPECIES_SEADRA]     = {{EVO_ITEM, ITEM_DRAGON_SCALE, SPECIES_KINGDRA}}",
            "[SPECIES_SCYTHER]    = {{EVO_ITEM, ITEM_METAL_COAT, SPECIES_SCIZOR}}",
            "[SPECIES_PORYGON]    = {{EVO_ITEM, ITEM_UP_GRADE, SPECIES_PORYGON2}}",
            "[SPECIES_CLAMPERL]   = {{EVO_ITEM, ITEM_DEEP_SEA_TOOTH, SPECIES_HUNTAIL},\n                            {EVO_ITEM, ITEM_DEEP_SEA_SCALE, SPECIES_GOREBYSS}}",
        ]
        for snippet in expected:
            self.assertIn(snippet, evolution_text)

        items = json.loads(
            (self.root / "src" / "data" / "items.json").read_text(encoding="utf-8")
        )["items"]
        items_by_id = {item["itemId"]: item for item in items}
        for item_id in [
            "ITEM_KINGS_ROCK",
            "ITEM_METAL_COAT",
            "ITEM_DRAGON_SCALE",
            "ITEM_UP_GRADE",
            "ITEM_DEEP_SEA_TOOTH",
            "ITEM_DEEP_SEA_SCALE",
        ]:
            with self.subTest(item_id=item_id):
                self.assertEqual("ITEM_TYPE_PARTY_MENU", items_by_id[item_id]["type"])
                self.assertEqual("FieldUseFunc_EvoItem", items_by_id[item_id]["fieldUseFunc"])
                self.assertRegex(
                    item_effects_text,
                    rf"\[{item_id} - ITEM_POTION\]\s+= sItemEffect_TradeEvolutionItem,",
                )
                self.assertIn(
                    f"(item) == {item_id}",
                    item_constants_text,
                )
        self.assertIn(
            "static const u8 sItemEffect_TradeEvolutionItem[6] = {\n"
            "    [4] = ITEM4_EVO_STONE,\n"
            "};",
            item_effects_text,
        )
        self.assertIn(
            "IS_DIRECT_EVOLUTION_ITEM(item)",
            item_constants_text,
        )

    def test_eevee_uses_stones_for_espeon_and_umbreon(self) -> None:
        evolution_text = (self.root / "src" / "data" / "pokemon" / "evolution.h").read_text(encoding="utf-8")

        self.assertIn("{EVO_ITEM, ITEM_SUN_STONE, SPECIES_ESPEON}", evolution_text)
        self.assertIn("{EVO_ITEM, ITEM_MOON_STONE, SPECIES_UMBREON}", evolution_text)

    def test_fighting_dojo_rematch_unlocks_the_other_reward(self) -> None:
        flags_text = (self.root / "include" / "constants" / "flags.h").read_text(encoding="utf-8")
        dojo_text = (
            self.root / "data" / "maps" / "SaffronCity_Dojo" / "scripts.inc"
        ).read_text(encoding="utf-8")
        master_start = dojo_text.index("SaffronCity_Dojo_EventScript_MasterKoichi::")
        master_end = dojo_text.index("SaffronCity_Dojo_EventScript_MasterKoichiRematch::", master_start)
        master_script = dojo_text[master_start:master_end]
        master_commands = [
            line.strip()
            for line in master_script.splitlines()[1:]
            if line.strip()
        ]

        self.assertIn("#define FLAG_GOT_BOTH_HITMON_FROM_DOJO", flags_text)
        self.assertTrue(master_commands[0].startswith("trainerbattle_single TRAINER_BLACK_BELT_KOICHI,"))
        self.assertIn("cleartrainerflag TRAINER_BLACK_BELT_KOICHI", dojo_text)
        self.assertIn("setvar VAR_MAP_SCENE_SAFFRON_CITY_DOJO, 2", dojo_text)
        self.assertGreaterEqual(
            dojo_text.count(
                "goto_if_set FLAG_GOT_BOTH_HITMON_FROM_DOJO, "
                "SaffronCity_Dojo_EventScript_AlreadyGotHitmon"
            ),
            2,
        )
        self.assertIn("setflag FLAG_GOT_BOTH_HITMON_FROM_DOJO", dojo_text)
        self.assertGreaterEqual(
            dojo_text.count("call SaffronCity_Dojo_EventScript_RecordHitmonReward"),
            2,
        )

    def test_national_dex_upgrade_has_no_caught_or_one_island_gate(self) -> None:
        script_text = (self.root / "data" / "maps" / "PalletTown" / "scripts.inc").read_text(encoding="utf-8")
        start = script_text.index("PalletTown_EventScript_OakRatingScene::")
        end = script_text.index("PalletTown_Movement_OakWalkToPlayersDoor:", start)
        oak_rating_scene = script_text[start:end]

        self.assertNotIn("goto_if_lt VAR_0x8009, 60", oak_rating_scene)
        self.assertNotIn("goto_if_unset FLAG_WORLD_MAP_ONE_ISLAND", oak_rating_scene)

    def test_evolutions_do_not_require_national_dex(self) -> None:
        evolution_scene_text = (self.root / "src" / "evolution_scene.c").read_text(encoding="utf-8")
        pokemon_text = (self.root / "src" / "pokemon.c").read_text(encoding="utf-8")
        start = pokemon_text.index("u16 GetEvolutionTargetSpecies(")
        end = pokemon_text.index("static u16 HoennPokedexNumToSpecies", start)
        evolution_target_text = pokemon_text[start:end]

        self.assertNotIn("!IsNationalPokedexEnabled()", evolution_scene_text)
        self.assertNotIn("IsNationalPokedexEnabled()", evolution_target_text)
        self.assertNotIn("targetSpecies <= KANTO_SPECIES_END", evolution_target_text)

    def test_hm_moves_can_be_replaced_when_learning_a_move(self) -> None:
        summary_text = (self.root / "src" / "pokemon_summary_screen.c").read_text(encoding="utf-8")
        battle_text = (self.root / "src" / "battle_script_commands.c").read_text(encoding="utf-8")
        evolution_text = (self.root / "src" / "evolution_scene.c").read_text(encoding="utf-8")

        self.assertNotIn("IsMoveHm(move)", summary_text)
        self.assertNotIn("IsHMMove2(moveId)", battle_text)
        self.assertNotIn("IsHMMove2(move)", evolution_text)

    def test_celadon_department_store_sells_evolution_items(self) -> None:
        shop_text = (
            self.root / "data" / "maps" / "CeladonCity_DepartmentStore_4F" / "scripts.inc"
        ).read_text(encoding="utf-8")
        start = shop_text.index("CeladonCity_DepartmentStore_4F_Items::")
        end = shop_text.index("ITEM_NONE", start)
        shop_items = shop_text[start:end]

        for item in [
            "ITEM_MOON_STONE",
            "ITEM_SUN_STONE",
            "ITEM_KINGS_ROCK",
            "ITEM_METAL_COAT",
            "ITEM_DRAGON_SCALE",
            "ITEM_UP_GRADE",
            "ITEM_DEEP_SEA_TOOTH",
            "ITEM_DEEP_SEA_SCALE",
        ]:
            self.assertIn(item, shop_items)

    def test_tms_are_reusable(self) -> None:
        party_menu_text = (self.root / "src" / "party_menu.c").read_text(encoding="utf-8")
        start = party_menu_text.rindex("static void Task_LearnedMove")
        end = party_menu_text.index("static void Task_TryLearningNextMove", start)
        learned_move = party_menu_text[start:end]

        self.assertIn("LEARN_VIA_TMHM", learned_move)
        self.assertNotIn("RemoveBagItem(item, 1)", learned_move)

    def test_running_is_allowed_indoors_after_running_shoes(self) -> None:
        avatar_text = (self.root / "src" / "field_player_avatar.c").read_text(encoding="utf-8")
        start = avatar_text.rindex("static void PlayerNotOnBikeMoving")
        end = avatar_text.index("bool32 PlayerIsMovingOnRockStairs", start)
        movement = avatar_text[start:end]

        self.assertIn("FlagGet(FLAG_SYS_B_DASH)", movement)
        self.assertNotIn("IsRunningDisallowed", movement)

    def test_shiny_odds_are_increased(self) -> None:
        pokemon_constants = (self.root / "include" / "constants" / "pokemon.h").read_text(encoding="utf-8")

        self.assertIn("#define SHINY_ODDS 64", pokemon_constants)

    def test_pokedex_uses_metric_height_and_weight(self) -> None:
        pokedex_screen = (self.root / "src" / "pokedex_screen.c").read_text(encoding="utf-8")
        shared_strings = (self.root / "src" / "strings.c").read_text(encoding="utf-8")

        height_start = pokedex_screen.index("void DexScreen_PrintMonHeight")
        weight_start = pokedex_screen.index("void DexScreen_PrintMonWeight", height_start)
        flavor_start = pokedex_screen.index("void DexScreen_PrintMonFlavorText", weight_start)
        height_function = pokedex_screen[height_start:weight_start]
        weight_function = pokedex_screen[weight_start:flavor_start]

        self.assertIn("height / 10", height_function)
        self.assertIn("height % 10", height_function)
        self.assertIn("gText_Meters", height_function)
        self.assertNotIn("CHAR_SGL_QUOTE_RIGHT", height_function)
        self.assertNotIn("CHAR_DBL_QUOTE_RIGHT", height_function)

        self.assertIn("weight / 10", weight_function)
        self.assertIn("weight % 10", weight_function)
        self.assertIn("gText_Kilograms", weight_function)
        self.assertNotIn("4536", weight_function)
        self.assertNotIn("gText_Lbs", weight_function)

        self.assertIn('gText_Meters[] = _("m")', shared_strings)
        self.assertIn('gText_Kilograms[] = _("kg")', shared_strings)

    def test_snorlax_pokedex_entry_is_fully_icelandic(self) -> None:
        entries = (self.root / "src" / "data" / "pokemon" / "pokedex_entries.h").read_text(encoding="utf-8")
        descriptions = (self.root / "src" / "data" / "pokemon" / "pokedex_text_fr.h").read_text(encoding="utf-8")

        snorlax_entry_start = entries.index("[NATIONAL_DEX_SNORLAX]")
        snorlax_entry_end = entries.index("[NATIONAL_DEX_ARTICUNO]", snorlax_entry_start)
        snorlax_entry = entries[snorlax_entry_start:snorlax_entry_end]
        self.assertIn('.categoryName = _("SOFANDI")', snorlax_entry)
        self.assertNotIn("SLEEPING", snorlax_entry)

        snorlax_text_start = descriptions.index("const u8 gSnorlaxPokedexText[]")
        snorlax_text_end = descriptions.index("const u8 gSnorlaxPokedexTextUnused[]", snorlax_text_start)
        snorlax_text = descriptions[snorlax_text_start:snorlax_text_end]
        self.assertIn("400 kg", snorlax_text)
        self.assertNotRegex(
            snorlax_text,
            r"(?i)\b(it|is|not|unless|eats|over|pounds|food|every|day|when|done)\b",
        )

    def test_national_pokedex_descriptions_have_no_obvious_english(self) -> None:
        descriptions = (self.root / "src" / "data" / "pokemon" / "pokedex_text_fr.h").read_text(encoding="utf-8")
        national_start = descriptions.index("const u8 gBulbasaurPokedexText[]")
        national_descriptions = descriptions[national_start:]
        english_words = re.compile(
            r"(?i)\b(the|this|these|those|it|its|they|their|them|when|where|which|who|"
            r"with|without|unless|over|under|every|from|into|about|because|cannot|will|"
            r"has|have|was|were|are|and|but|than|that|while|after|before|during|lives|"
            r"uses|eats|feeds|makes|becomes|found|said|body|head|tail|legs|moves)\b"
        )

        matches = sorted(set(match.group(0) for match in english_words.finditer(national_descriptions)))
        self.assertEqual([], matches)
        self.assertNotIn("\ufffd", national_descriptions)
        self.assertEqual([], [char for char in "„“”’°ﬁﬂ" if char in national_descriptions])

    def test_national_pokedex_description_lines_fit_the_display(self) -> None:
        descriptions = (self.root / "src" / "data" / "pokemon" / "pokedex_text_fr.h").read_text(encoding="utf-8")
        national_start = descriptions.index("const u8 gBulbasaurPokedexText[]")
        national_descriptions = descriptions[national_start:]
        blocks = re.findall(
            r"const u8 g([A-Za-z0-9]+)PokedexText\[\] = _\((.*?)\);",
            national_descriptions,
            re.DOTALL,
        )

        self.assertEqual(386, len(blocks))
        for revision in (0, 1):
            for species, body in blocks:
                active = True
                visible_lines = []
                for source_line in body.splitlines():
                    stripped = source_line.strip()
                    if stripped == "#if REVISION == 0":
                        active = revision == 0
                    elif stripped == "#else":
                        active = not active
                    elif stripped == "#endif":
                        active = True
                    elif active:
                        match = re.match(r'^"([^"\\]*(?:\\.[^"\\]*)*)"', stripped)
                        if match:
                            visible_lines.append(match.group(1).removesuffix(r"\n"))

                with self.subTest(species=species, revision=revision):
                    self.assertEqual(3, len(visible_lines))
                    self.assertEqual([], [line for line in visible_lines if len(line) > 40])

    def test_national_pokedex_categories_fit_the_display(self) -> None:
        entries = (self.root / "src" / "data" / "pokemon" / "pokedex_entries.h").read_text(encoding="utf-8")
        categories = re.findall(r'\.categoryName\s*=\s*_\("([^"]+)"\)', entries)[1:387]

        self.assertEqual(386, len(categories))
        self.assertEqual([], [category for category in categories if len(category) > 11])

    def test_pokedex_fallback_and_national_labels_are_icelandic(self) -> None:
        entries = (self.root / "src" / "data" / "pokemon" / "pokedex_entries.h").read_text(encoding="utf-8")
        shared_strings = (self.root / "src" / "strings.c").read_text(encoding="utf-8")

        self.assertIn('.categoryName = _("ÓÞEKKT")', entries)
        self.assertNotIn('.categoryName = _("UNKNOWN")', entries)
        self.assertIn('gText_NumericalModeNational[] = _("TÖLURÖÐ: LANDSVÍS")', shared_strings)
        self.assertNotIn('gText_NumericalModeNational[] = _("TÖLURÖÐ: NATIONAL")', shared_strings)
        self.assertIn('gText_PokedexPokemon[] = _(" Vasaskrímsli")', shared_strings)

    def test_core_type_names_are_icelandic(self) -> None:
        battle_main = (self.root / "src" / "battle_main.c").read_text(encoding="utf-8")

        for snippet in [
            '[TYPE_NORMAL] = _("VENJL.")',
            '[TYPE_FIRE] = _("ELDUR")',
            '[TYPE_WATER] = _("VATN")',
            '[TYPE_ELECTRIC] = _("RAFM")',
            '[TYPE_GRASS] = _("GRAS")',
        ]:
            self.assertIn(snippet, battle_main)

    def test_ability_names_fit_the_configured_buffer(self) -> None:
        battle_main_header = (self.root / "include" / "battle_main.h").read_text(encoding="utf-8")
        abilities_text = (self.root / "src" / "data" / "text" / "abilities.h").read_text(encoding="utf-8")

        length_match = re.search(r"#define ABILITY_NAME_LENGTH (\d+)", battle_main_header)
        self.assertIsNotNone(length_match)
        max_length = int(length_match.group(1))
        ability_names = re.findall(r"\[ABILITY_[A-Z0-9_]+\]\s*=\s*_\(\"([^\"]*)\"\)", abilities_text)

        self.assertTrue(ability_names)
        self.assertEqual([], [name for name in ability_names if len(name) > max_length])


if __name__ == "__main__":
    unittest.main()
