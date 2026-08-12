#!/usr/bin/env python3

import unittest
from dataclasses import replace
from pathlib import Path

from tools.atrmrw.calculations import (
    GunInputs,
    calculate_base_org,
    calculate_base_strength,
    calculate_gun,
    load_gun_config,
    target_naval_range,
    target_naval_speed,
)


REPO = Path(__file__).resolve().parents[2]
CONFIG = REPO / "tools/atrmrw/gun_calc_config_ssw_4bcb.json"


class CalculationsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config, cls.config_hash = load_gun_config(CONFIG)
        cls.oto_127 = GunInputs(
            bore_cm=12.7,
            caliber_length=54,
            muzzle_velocity_mps=808,
            barrels_per_mount=1,
            rounds_per_minute=40,
            shell_weight_kg=30.7,
            elevation_deg=83,
            elevation_rate_deg_s=30,
            train_rate_deg_s=40,
            mount_weight_kg=37500,
            mount_count=1,
            tier=10,
        )

    def test_fixed_ssw_gun_golden_vector(self) -> None:
        result = calculate_gun(self.oto_127, self.config, self.config_hash)
        self.assertEqual(result.lg_attack, 9.75)
        self.assertEqual(result.hg_attack, 1.3)
        self.assertEqual(result.lg_armor_piercing, 12.0)
        self.assertEqual(result.hg_armor_piercing, 1.6)
        self.assertEqual(result.anti_air_attack, 4.875)
        self.assertEqual(result.build_cost_ic, 129.0)
        self.assertEqual(
            result.config_sha256,
            "8ac721425d0c6aabb11bb47c57339a06b2e7914dc84da4fef6018ad5be5e3070",
        )

    def test_hpclc_ssw_yamato_compatibility_vector(self) -> None:
        self.assertAlmostEqual(
            calculate_base_strength(72809, 263.0, 38.9, "capital", 1941),
            1161.0838749286406,
        )
        self.assertAlmostEqual(
            calculate_base_org(72809, 263.0, 38.9, "capital", 1941),
            1080.3601472453,
        )

    def test_range_and_speed(self) -> None:
        self.assertAlmostEqual(target_naval_range(7200), 6667.2)
        self.assertEqual(target_naval_speed(27, 15), 21.0)
        self.assertEqual(target_naval_speed(30), 27.0)

    def test_mount_count_must_be_positive(self) -> None:
        with self.assertRaisesRegex(ValueError, "mount_count"):
            calculate_gun(replace(self.oto_127, mount_count=0), self.config, self.config_hash)

    def test_unknown_hull_type_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown hull_type"):
            calculate_base_strength(1000, 100, 10, "unknown", 1936)


if __name__ == "__main__":
    unittest.main()
