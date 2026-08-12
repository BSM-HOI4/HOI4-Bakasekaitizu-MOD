#!/usr/bin/env python3

import hashlib
import re
import unittest
from pathlib import Path

from tools.atrmrw.generate_equipmentdesigner_gui import DEFAULT_SOURCE, VANILLA_SHA256, generate
from tools.atrmrw.gui_layout import (
    CUSTOM_COORDINATES,
    FIXED_COORDINATES,
    PANEL_HEIGHT,
    PANEL_WIDTH,
    SLOT_HEIGHT,
    SLOT_WIDTH,
)


REPO = Path(__file__).resolve().parents[2]
GENERATED = REPO / "bakasekai/interface/replace/equipmentdesignerview.gui"


class GuiLayoutTest(unittest.TestCase):
    def test_layout_is_complete_unique_and_inside_panel(self) -> None:
        self.assertEqual(set(CUSTOM_COORDINATES), set(range(18)))
        self.assertEqual(set(FIXED_COORDINATES), set(range(18)))
        coordinates = list(CUSTOM_COORDINATES.values()) + list(FIXED_COORDINATES.values())
        self.assertEqual(len(coordinates), 36)
        self.assertEqual(len(set(coordinates)), 36)
        for x, y in coordinates:
            self.assertGreaterEqual(x, 0)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(x + SLOT_WIDTH, PANEL_WIDTH + 2)  # vanilla列間/右端の既存2px許容
            self.assertLessEqual(y + SLOT_HEIGHT, PANEL_HEIGHT)

    def test_generated_file_matches_fixed_vanilla_plus_anchor_patch(self) -> None:
        source = DEFAULT_SOURCE.read_bytes()
        self.assertEqual(hashlib.sha256(source).hexdigest(), VANILLA_SHA256)
        expected = generate(source.decode("ascii"))
        self.assertEqual(GENERATED.read_text(encoding="ascii"), expected)
        names = re.findall(r'name = "pos_(?:custom|fixed)_module_slot_window_\d+"', expected)
        self.assertEqual(len(names), 36)
        self.assertEqual(len(names), len(set(names)))


if __name__ == "__main__":
    unittest.main()
