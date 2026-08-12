#!/usr/bin/env python3

import hashlib
import json
import re
import tempfile
import unittest
from pathlib import Path

from tools.atrmrw.generate_ship_archetype_guis import (
    BASELINE_SHA256,
    CONTRACT_PATH,
    OUTPUT_DIR,
    VANILLA_DIR,
    generate,
    maximum_slot_ids,
)


class ShipArchetypeGuiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        cls.game_slot_ids = maximum_slot_ids(cls.contract)

    def test_ssw_role_is_custom_zero_and_groups_are_balanced(self) -> None:
        slots = self.contract["profiles"]["maximum_36"]["slots"]
        role = next(slot for slot in slots if slot["id"] == "role_slot")
        self.assertEqual((role["game_slot_id"], role["ui_group"], role["ui_index"]), ("ship_type_slot", "custom", 0))
        self.assertEqual(sum(slot["ui_group"] == "custom" for slot in slots), 18)
        self.assertEqual(sum(slot["ui_group"] == "fixed" for slot in slots), 18)

    def test_generated_files_equal_verified_vanilla_plus_exact_containers(self) -> None:
        for filename, expected_digest in BASELINE_SHA256.items():
            source = (VANILLA_DIR / filename).read_bytes()
            self.assertEqual(hashlib.sha256(source).hexdigest(), expected_digest)
            expected = generate(source.decode("ascii"), self.game_slot_ids)
            actual = (OUTPUT_DIR / filename).read_text(encoding="ascii")
            self.assertEqual(actual, expected)
            for slot_id in self.game_slot_ids:
                self.assertEqual(len(re.findall(rf'name = "{re.escape(slot_id)}"', actual)), 1)

    def test_generator_rejects_incomplete_contract(self) -> None:
        source = (VANILLA_DIR / "ship_hull_heavy.gui").read_text(encoding="ascii")
        with self.assertRaises(ValueError):
            generate(source, self.game_slot_ids[:-1])


if __name__ == "__main__":
    unittest.main()
