#!/usr/bin/env python3

import json
import unittest
from pathlib import Path

from tools.atrmrw.generate_japan_game_files import (
    CONTRACT,
    HULL_OUTPUT,
    JAPANESE_MODULE_NAMES,
    LOC_JA_OUTPUT,
    MODULE_LEDGER,
    MODULE_OUTPUT,
    PACKING,
    PROTOTYPES,
    VARIANT_OUTPUT,
)


class GenerateJapanGameFilesTest(unittest.TestCase):
    def test_every_compiled_module_has_one_game_definition(self) -> None:
        ledger = json.loads(MODULE_LEDGER.read_text(encoding="utf-8"))
        text = MODULE_OUTPUT.read_text(encoding="utf-8")
        for row in ledger["modules"]:
            self.assertEqual(text.count(f"  {row['module_id']} = {{"), 1)

    def test_every_physical_slot_is_declared_and_defaulted_per_hull(self) -> None:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        packing = json.loads(PACKING.read_text(encoding="utf-8"))
        prototypes = {row["prototype_key"]: row for row in json.loads(PROTOTYPES.read_text(encoding="utf-8"))["prototypes"]}
        text = HULL_OUTPUT.read_text(encoding="utf-8")
        for packed in packing["prototypes"]:
            prototype = prototypes[packed["prototype_key"]]
            profile = contract["profiles"][prototype["slot_profile_id"]]
            for slot in profile["slots"]:
                self.assertGreaterEqual(text.count(f"      {slot['game_slot_id']} = "), 2)

    def test_no_hidden_slot_and_localisation_has_bom(self) -> None:
        self.assertNotIn("hidden_", HULL_OUTPUT.read_text(encoding="utf-8"))
        self.assertTrue(LOC_JA_OUTPUT.read_bytes().startswith(b"\xef\xbb\xbf"))

    def test_every_module_has_explicit_japanese_name(self) -> None:
        ledger = json.loads(MODULE_LEDGER.read_text(encoding="utf-8"))
        self.assertEqual(set(JAPANESE_MODULE_NAMES), {row["module_id"] for row in ledger["modules"]})

    def test_variants_use_atrmrw_hulls_and_all_visible_slots(self) -> None:
        text = VARIANT_OUTPUT.read_text(encoding="utf-8")
        prototypes = json.loads(PROTOTYPES.read_text(encoding="utf-8"))["prototypes"]
        for prototype in prototypes:
            self.assertEqual(text.count(f"      type = {prototype['implementation_hull_id']}"), 1)


if __name__ == "__main__":
    unittest.main()
