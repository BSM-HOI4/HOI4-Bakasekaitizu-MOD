#!/usr/bin/env python3

import unittest

from tools.atrmrw.composition import calibrate_reference, compose_stat, evaluate_design


class CompositionTest(unittest.TestCase):
    def test_add_then_multiply_reference_round_trip(self) -> None:
        modules = [{
            "slot_id": "engineering_slot_02",
            "module_id": "engine_reference",
            "add_stats": {"naval_speed": 4.0},
            "multiply_stats": {"naval_speed": 0.25},
        }]
        calibration = calibrate_reference({"naval_speed": 30.0}, modules, {"naval_speed": 0.01})
        self.assertAlmostEqual(calibration["stats"]["naval_speed"]["frozen_base"], 20.0)
        self.assertAlmostEqual(evaluate_design(calibration, modules)["naval_speed"], 30.0)

    def test_module_change_does_not_recompute_base(self) -> None:
        reference = [{
            "slot_id": "engineering_slot_02",
            "module_id": "strong_engine",
            "add_stats": {"naval_speed": 10.0},
        }]
        weak = [{
            "slot_id": "engineering_slot_02",
            "module_id": "weak_engine",
            "add_stats": {"naval_speed": 2.0},
        }]
        calibration = calibrate_reference({"naval_speed": 30.0}, reference)
        self.assertEqual(calibration["stats"]["naval_speed"]["frozen_base"], 20.0)
        self.assertEqual(evaluate_design(calibration, weak)["naval_speed"], 22.0)

    def test_invalid_multiplier_and_negative_base_fail(self) -> None:
        invalid = [{"slot_id": "s", "module_id": "m", "multiply_stats": {"x": -1.0}}]
        with self.assertRaisesRegex(ValueError, "greater than -1"):
            compose_stat(1.0, "x", invalid)
        too_large = [{"slot_id": "s", "module_id": "m", "add_stats": {"x": 11.0}}]
        with self.assertRaisesRegex(ValueError, "non-negative"):
            calibrate_reference({"x": 10.0}, too_large)

    def test_duplicate_slot_contribution_fails(self) -> None:
        duplicate = [
            {"slot_id": "weapon_slot_01", "module_id": "a"},
            {"slot_id": "weapon_slot_01", "module_id": "b"},
        ]
        with self.assertRaisesRegex(ValueError, "duplicate slot_id"):
            calibrate_reference({"x": 1.0}, duplicate)


if __name__ == "__main__":
    unittest.main()
