from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_terms


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
                '\t.string "CUT, FLY, STRENGTH, DIG, FLASH, SHOCK WAVE og SONICBOOM.$"\n',
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


class GameplaySanityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]

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
            "create_cerulean_v1_batch.py",
            "create_cerulean_cleanup_v1_batch.py",
            "create_vermilion_v1_batch.py",
            "create_ssanne_v1_batch.py",
            "create_route11_diglett_route2_v1_batch.py",
            "create_fuchsia_safari_v1_batch.py",
        ]
        pattern = re.compile(r"\b(?:CUT|FLY|STRENGTH|DIG|FLASH|SONICBOOM)\b|SAFARI(?:\s|\\n)+ZONE")
        offenders: list[str] = []
        for filename in generators:
            path = self.root / "tools" / "icelandic" / filename
            if pattern.search(path.read_text(encoding="utf-8")):
                offenders.append(filename)

        self.assertEqual([], offenders)

        safe_batch = (self.root / "tools" / "icelandic" / "generate_safe_translation_batch.py").read_text(encoding="utf-8")
        self.assertIn('"SAFARI ZONE": "SAFARI SVÆÐI"', safe_batch)

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
            'gText_GiveUpTryingToTeachNewMove[] = _("Gefast upp á að reyna að kenna nýja\\nhreyfingu til {STR_VAR_1}?")',
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
    .string "Uh… Ó, já, ég eyði hreyfingum.\\p"
    .string "Ég get látið Vasaskrímsli gleyma\\n"
    .string "hreyfingum sínum.\\p"
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

    def test_eevee_uses_stones_for_espeon_and_umbreon(self) -> None:
        evolution_text = (self.root / "src" / "data" / "pokemon" / "evolution.h").read_text(encoding="utf-8")

        self.assertIn("{EVO_ITEM, ITEM_SUN_STONE, SPECIES_ESPEON}", evolution_text)
        self.assertIn("{EVO_ITEM, ITEM_MOON_STONE, SPECIES_UMBREON}", evolution_text)

    def test_national_dex_upgrade_has_no_caught_or_one_island_gate(self) -> None:
        script_text = (self.root / "data" / "maps" / "PalletTown" / "scripts.inc").read_text(encoding="utf-8")
        start = script_text.index("PalletTown_EventScript_OakRatingScene::")
        end = script_text.index("PalletTown_Movement_OakWalkToPlayersDoor:", start)
        oak_rating_scene = script_text[start:end]

        self.assertNotIn("goto_if_lt VAR_0x8009, 60", oak_rating_scene)
        self.assertNotIn("goto_if_unset FLAG_WORLD_MAP_ONE_ISLAND", oak_rating_scene)

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
