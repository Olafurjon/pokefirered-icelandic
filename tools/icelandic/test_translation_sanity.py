from __future__ import annotations

import json
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
                '\t.string "Storage System, SURF, VIRIDIAN FOREST, NIDORAN og SKORDÝ Vasaskrímsli.$"\n',
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
        self.assertIn("viridian-forest", found)
        self.assertIn("nidoran-species", found)
        self.assertIn("bug-species-phrase", found)
        self.assertIn("nature-name", found)

    def test_accepts_approved_icelandic_terms(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            text_file = root / "data" / "maps" / "TestMap" / "text.inc"
            text_file.parent.mkdir(parents=True)
            text_file.write_text(
                'Test_Text::\n'
                '\t.string "VASaSKRÍMSLI fá SEYÐI við HJÓLAVEGINN.$"\n',
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


if __name__ == "__main__":
    unittest.main()
