#!/usr/bin/env python3
"""ATRMRWの承認済み海軍計算式。import時のI/Oや設定生成を行わない。"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


HP_FORMULA_ID = "atrmrw_hp_v1_ssw_4bcb"
ORG_FORMULA_ID = "atrmrw_org_v1_ssw_4bcb"
GUN_FORMULA_ID = "atrmrw_gun_v1_ssw_4bcb_tracked_config"
RANGE_FORMULA_ID = "atrmrw_range_v1"
SPEED_FORMULA_ID = "atrmrw_speed_v1"

HULL_TYPE_MULTIPLIERS = {
    "small_craft": 0.3,
    "light": 0.5,
    "submarine": 0.5,
    "frigate": 0.8,
    "support": 0.8,
    "cruiser": 1.5,
    "carrier": 1.5,
    "capital": 2.0,
}


@dataclass(frozen=True)
class GunInputs:
    bore_cm: float
    caliber_length: float
    muzzle_velocity_mps: float
    barrels_per_mount: int
    rounds_per_minute: float
    shell_weight_kg: float
    elevation_deg: float
    elevation_rate_deg_s: float
    train_rate_deg_s: float
    mount_weight_kg: float
    mount_count: int
    tier: int


@dataclass(frozen=True)
class GunResult:
    lg_attack: float
    hg_attack: float
    lg_armor_piercing: float
    hg_armor_piercing: float
    anti_air_attack: float
    build_cost_ic: float
    role_ratio_lg: float
    role_ratio_hg: float
    formula_id: str
    config_sha256: str


def load_gun_config(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_bytes()
    config = json.loads(raw.decode("utf-8"))
    required = {"攻撃力", "貫通力", "対空", "建造コスト", "tier係数", "役割比率"}
    missing = sorted(required - set(config))
    if missing:
        raise ValueError(f"gun config missing sections: {missing}")
    return config, hashlib.sha256(raw).hexdigest()


def era_strength_multiplier(year: int | None) -> float:
    if year is None:
        return 1.0
    if year <= 1905:
        return 0.90
    if year <= 1919:
        return 0.95
    if year <= 1945:
        return 1.00
    if year <= 1975:
        return 1.03
    return 1.05


def era_org_multiplier(year: int | None) -> float:
    if year is None:
        return 1.0
    for upper, multiplier in (
        (1905, 0.60), (1913, 0.68), (1919, 0.75), (1935, 0.85),
        (1945, 1.00), (1960, 1.15), (1975, 1.30), (1990, 1.50),
    ):
        if year <= upper:
            return multiplier
    return 1.70


def _positive(name: str, value: float) -> None:
    if value <= 0 or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite value > 0")


def calculate_base_strength(displacement_full_t: float, length_oa_m: float,
                            breadth_m: float, hull_type: str,
                            year: int | None = None) -> float:
    for name, value in (
        ("displacement_full_t", displacement_full_t),
        ("length_oa_m", length_oa_m),
        ("breadth_m", breadth_m),
    ):
        _positive(name, value)
    if hull_type not in HULL_TYPE_MULTIPLIERS:
        raise ValueError(f"unknown hull_type: {hull_type}")
    area = length_oa_m * breadth_m
    raw = (
        1100 * math.sqrt(displacement_full_t / (displacement_full_t + 45000))
        + 300 * math.sqrt(area / (area + 15000))
        + 50
    )
    hull_multiplier = 0.85 + 0.10 * HULL_TYPE_MULTIPLIERS[hull_type]
    return max(20.0, raw * hull_multiplier * era_strength_multiplier(year))


def calculate_base_org(displacement_full_t: float, length_oa_m: float,
                       breadth_m: float, hull_type: str,
                       year: int | None = None) -> float:
    for name, value in (
        ("displacement_full_t", displacement_full_t),
        ("length_oa_m", length_oa_m),
        ("breadth_m", breadth_m),
    ):
        _positive(name, value)
    if hull_type not in HULL_TYPE_MULTIPLIERS:
        raise ValueError(f"unknown hull_type: {hull_type}")
    area = length_oa_m * breadth_m
    raw = (
        100 + 800 * (HULL_TYPE_MULTIPLIERS[hull_type] / 2)
        + 150 * math.sqrt(displacement_full_t / (displacement_full_t + 25000))
        + 80 * math.sqrt(area / (area + 15000))
    )
    return max(50.0, raw * era_org_multiplier(year))


def target_naval_range(endurance_nm: float) -> float:
    _positive("endurance_nm", endurance_nm)
    return endurance_nm * 1.852 / 2


def target_naval_speed(maximum_speed_kn: float,
                       cruising_speed_kn: float | None = None) -> float:
    _positive("maximum_speed_kn", maximum_speed_kn)
    cruise = maximum_speed_kn * 0.80 if cruising_speed_kn is None else cruising_speed_kn
    _positive("cruising_speed_kn", cruise)
    if cruise > maximum_speed_kn:
        raise ValueError("cruising_speed_kn must not exceed maximum_speed_kn")
    return (maximum_speed_kn + cruise) / 2


def gun_role_ratio(bore_cm: float, config: dict[str, Any]) -> tuple[float, float]:
    _positive("bore_cm", bore_cm)
    for threshold, lg, hg in config["役割比率"]["閾値リスト"]:
        if threshold is None or bore_cm >= threshold:
            return float(lg), float(hg)
    raise ValueError("gun role ratio table has no fallback")


def calculate_gun(inputs: GunInputs, config: dict[str, Any],
                  config_sha256: str) -> GunResult:
    for name, value in asdict(inputs).items():
        if name in {"rounds_per_minute", "elevation_deg", "elevation_rate_deg_s", "train_rate_deg_s"}:
            if value < 0 or not math.isfinite(value):
                raise ValueError(f"{name} must be a finite value >= 0")
        else:
            _positive(name, float(value))
    if inputs.tier < 1:
        raise ValueError("tier must be >= 1")

    attack = config["攻撃力"]
    penetration = config["貫通力"]
    anti_air = config["対空"]
    cost_cfg = config["建造コスト"]
    lg_ratio, hg_ratio = gun_role_ratio(inputs.bore_cm, config)

    base_attack = (
        inputs.shell_weight_kg ** attack["砲弾重量_指数"]
        * inputs.muzzle_velocity_mps ** attack["砲口速度_指数"]
        * (inputs.rounds_per_minute + 1) ** attack["発射速度_指数"]
        * inputs.barrels_per_mount ** attack["砲身数_指数"]
        * (inputs.caliber_length / 10) ** attack["口径_指数"]
        // attack["除数"]
        * inputs.mount_count ** 0.8
    )
    base_penetration = (
        inputs.shell_weight_kg ** penetration["砲弾重量_指数"]
        * inputs.muzzle_velocity_mps ** penetration["砲口速度_指数"]
        * inputs.bore_cm ** penetration["口径_指数"]
        * (inputs.caliber_length / 10) ** penetration["口径mm_指数"]
        // penetration["除数"]
    )
    aa_index = (
        (inputs.rounds_per_minute + 1) ** anti_air["発射速度_指数"]
        * (inputs.elevation_deg / 90) ** anti_air["仰角_指数"]
        * (inputs.elevation_rate_deg_s + 1) ** anti_air["仰角速度_指数"]
        * (inputs.train_rate_deg_s + 1) ** anti_air["旋回速度_指数"]
        * (inputs.shell_weight_kg + 1) ** anti_air["砲弾重量_指数"]
        * inputs.barrels_per_mount ** anti_air["砲身数_指数"]
        * inputs.mount_count ** anti_air["砲塔数_指数"]
        // anti_air["除数"]
    )
    anti_air_attack = aa_index * (
        anti_air["対空基礎係数"] + anti_air["対空LG係数"] * lg_ratio
    )
    tier_cost_multiplier = 1 + (inputs.tier - 1) * config["tier係数"]["コスト乗数"]
    weight_term = (
        (inputs.mount_weight_kg / cost_cfg["重量除数"]) ** cost_cfg["砲塔重量_指数"]
        * (1 + inputs.bore_cm / cost_cfg["口径除数"])
        * (1 + inputs.caliber_length / cost_cfg["口径mm除数"])
        * inputs.barrels_per_mount ** attack["砲身数_指数"]
        * inputs.mount_count
        * (1 + inputs.muzzle_velocity_mps / cost_cfg["速度除数"])
    )
    bore_base = inputs.bore_cm * inputs.caliber_length * cost_cfg["口径基礎係数"]
    build_cost = (weight_term + bore_base) * tier_cost_multiplier // cost_cfg["最終除数"]
    return GunResult(
        lg_attack=base_attack * lg_ratio,
        hg_attack=base_attack * hg_ratio,
        lg_armor_piercing=base_penetration * lg_ratio,
        hg_armor_piercing=base_penetration * hg_ratio,
        anti_air_attack=anti_air_attack,
        build_cost_ic=build_cost,
        role_ratio_lg=lg_ratio,
        role_ratio_hg=hg_ratio,
        formula_id=GUN_FORMULA_ID,
        config_sha256=config_sha256,
    )
