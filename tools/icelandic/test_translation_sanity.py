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
    def test_first_partner_species_are_available_as_rare_grass_encounters(self) -> None:
        root = Path(__file__).resolve().parents[2]
        encounters_path = root / "src" / "data" / "wild_encounters.json"
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


if __name__ == "__main__":
    unittest.main()
