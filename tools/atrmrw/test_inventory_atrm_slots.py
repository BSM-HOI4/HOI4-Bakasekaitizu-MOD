#!/usr/bin/env python3

import unittest
from pathlib import Path

from inventory_atrm_slots import (
    DEFAULT_PATHS,
    DEFAULT_REF,
    Hull,
    load_hulls,
    parse_document,
    slot_map,
    strip_comments,
)


REPO = Path(__file__).resolve().parents[2]


class InventoryAtrmSlotsTest(unittest.TestCase):
    def test_comments_inside_quotes_are_preserved(self) -> None:
        self.assertEqual(strip_comments('name = "a#b" # comment'), 'name = "a#b" ')

    def test_explicit_slot_block_replaces_omitted_parent_slots(self) -> None:
        document = parse_document(
            """
            equipments = {
              base = {
                module_slots = {
                  fixed_a = { required = yes }
                  rear_a = { required = no }
                }
              }
              child = {
                archetype = base
                module_slots = {
                  fixed_a = inherit
                  front_a = { required = no }
                  rear_a = front_a
                }
              }
            }
            """
        )
        equipments = document.first("equipments")
        self.assertIsNotNone(equipments)
        hulls = {
            assignment.key: Hull(assignment.key, "fixture", assignment.value)
            for assignment in equipments.assignments  # type: ignore[union-attr]
        }
        self.assertEqual(
            list(slot_map("child", hulls, {})),
            ["fixed_a", "front_a", "rear_a"],
        )

    def test_whole_block_inherit_uses_parent_before_archetype(self) -> None:
        document = parse_document(
            """
            equipments = {
              base = { module_slots = { fixed_a = { required = yes } } }
              parent = {
                archetype = base
                module_slots = { fixed_b = { required = yes } }
              }
              child = {
                archetype = base
                parent = parent
                module_slots = inherit
              }
            }
            """
        )
        equipments = document.first("equipments")
        hulls = {
            assignment.key: Hull(assignment.key, "fixture", assignment.value)
            for assignment in equipments.assignments  # type: ignore[union-attr]
        }
        self.assertEqual(list(slot_map("child", hulls, {})), ["fixed_b"])

    def test_missing_alias_target_fails(self) -> None:
        document = parse_document(
            "equipments = { bad = { module_slots = { rear_a = missing_slot } } }"
        )
        equipments = document.first("equipments")
        hulls = {
            assignment.key: Hull(assignment.key, "fixture", assignment.value)
            for assignment in equipments.assignments  # type: ignore[union-attr]
        }
        with self.assertRaisesRegex(ValueError, "aliases missing"):
            slot_map("bad", hulls, {})

    def test_real_atrm_reference_counts(self) -> None:
        hulls = load_hulls(REPO, DEFAULT_REF, DEFAULT_PATHS)
        self.assertEqual(len(hulls), 62)
        memo: dict[str, dict[str, str]] = {}
        expected = {
            "ship_hull_carrier": 36,
            "ship_hull_cruiser": 10,
            "ship_hull_heavy": 11,
            "ship_hull_light": 8,
            "ship_hull_submarine": 3,
            "ship_hull_midget_submarine": 2,
        }
        self.assertEqual(
            {hull_id: len(slot_map(hull_id, hulls, memo)) for hull_id in expected},
            expected,
        )


if __name__ == "__main__":
    unittest.main()
