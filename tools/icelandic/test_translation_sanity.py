from __future__ import annotations

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
                '\t.string "POKéMON CENTER sells POTIONS near CYCLING ROAD.$"\n',
                encoding="utf-8",
            )

            rows = check_terms.scan_file(text_file, root)
            found = {row["rule"] for row in rows}

        self.assertIn("pokemon-term", found)
        self.assertIn("potion", found)
        self.assertIn("cycling-road", found)

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


if __name__ == "__main__":
    unittest.main()
