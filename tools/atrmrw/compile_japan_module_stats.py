#!/usr/bin/env python3
"""日本5艦級の論理module statsと固定船体基礎値を生成する。"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

try:
    from tools.atrmrw.composition import calibrate_reference
except ModuleNotFoundError:
    from composition import calibrate_reference


REPO = Path(__file__).resolve().parents[2]
SOURCE_LEDGER = REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE3_JAPAN_MODULE_SOURCE_LEDGER.json"
PACKING = REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE3_JAPAN_SLOT_PACKING.json"
PROTOTYPES = REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE3_JAPAN_PROTOTYPE_LEDGER.json"
OUTPUT = REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE3_JAPAN_MODULE_LEDGER.json"

BATCH_EXPONENT = 0.8
POWER_REFERENCE_SHP = 150000.0
POWER_REFERENCE_STATS = {"naval_speed": 7.0, "naval_range": 400.0, "build_cost_ic": 500.0}
TARGET_STATS = {
    "max_strength": "max_strength_unrounded",
    "max_organisation": "max_organisation_unrounded",
    "naval_speed": "target_naval_speed_kn",
    "naval_range": "target_naval_range_km",
}


def clean_number(value: float) -> float:
    return round(value, 6)


def scaled_stats(stats: dict[str, float], factor: float) -> dict[str, float]:
    return {key: clean_number(value * factor) for key, value in stats.items()}


def add_dict(target: dict[str, float], source: dict[str, float], factor: float = 1.0) -> None:
    for key, value in source.items():
        target[key] = clean_number(target.get(key, 0.0) + value * factor)


def aggregate_stats(row: dict[str, Any], registry: dict[str, Any]) -> tuple[dict[str, float], dict[str, float], str]:
    aggregation = row["aggregation"]
    add_stats: dict[str, float] = {}
    multiply_stats: dict[str, float] = {}
    if aggregation["count_unit"] == "aircraft_capacity":
        for mount in aggregation["source_mounts"]:
            source = registry[mount["source_module_id"]]
            add_dict(add_stats, source["effective_add_stats"])
            add_dict(multiply_stats, source["effective_multiply_stats"])
        return add_stats, multiply_stats, "exact_capacity_composition"

    for mount in aggregation["source_mounts"]:
        represented = float(mount["represented_historical_count"])
        if represented <= 0:
            factor = 1.0
        else:
            factor = represented ** BATCH_EXPONENT
        source = registry[mount["source_module_id"]]
        add_dict(add_stats, source["effective_add_stats"], factor)
        add_dict(multiply_stats, source["effective_multiply_stats"], factor)
    return add_stats, multiply_stats, "source_effective_stats_times_represented_count_pow_0_8"


def historical_stats(module_id: str, usage_prototype: dict[str, Any]) -> tuple[dict[str, float], dict[str, float], str]:
    if module_id.startswith("atrmrw_endurance_"):
        target = usage_prototype["computed"]["target_naval_range_km"]
        # 船体基礎値を非負に保ちつつ、燃料/endurance交換で航続距離が実際に変化する配分。
        return {"naval_range": clean_number(target * 0.5)}, {}, "half_of_nsdb_endurance_target_reserved_for_editable_endurance_module"
    if module_id.startswith("atrmrw_power_"):
        power = float(usage_prototype["inputs"]["power_shp_surface"])
        factor = power / POWER_REFERENCE_SHP
        return scaled_stats(POWER_REFERENCE_STATS, factor), {}, "linear_power_reference_SSW_JAP_150000"
    if module_id.startswith("atrmrw_armor_thickness_"):
        numbers = [float(value) for value in re.findall(r"_(\d+)(?=_|$)", module_id)]
        if not numbers:
            raise ValueError(f"armor thickness is missing from module ID: {module_id}")
        return {"armor_value": clean_number(numbers[0] * 0.13672)}, {}, "SSW_belt_mm_times_0_13672"
    return {}, {}, "identity_only_no_confirmed_numeric_contribution"


def module_semantics(packing: dict[str, Any]) -> dict[str, set[str]]:
    result: dict[str, set[str]] = defaultdict(set)
    numbered_semantics = {
        "engineering_slot": ["propulsion_type", "propulsion_power", "fuel_energy", "fuel_endurance"],
        "protection_slot": ["hull_structure", "protection", "armor_thickness", "damage_control"],
        "sensor_slot": ["fire_control", "detection", "electronic_warfare", "sonar"],
    }
    for prototype in packing["prototypes"]:
        for slot in prototype["slots"]:
            module_id = slot.get("default_module_id")
            if module_id and module_id != "empty":
                slot_id = slot["logical_slot_id"]
                if slot_id == "role_slot":
                    semantic = "role"
                elif slot_id.startswith("weapon_slot_"):
                    semantic = "weapon"
                elif slot_id.startswith("special_slot_"):
                    semantic = "hull_feature"
                else:
                    prefix, number = slot_id.rsplit("_", 1)
                    semantic = numbered_semantics[prefix][int(number) - 1]
                result[module_id].add(semantic)
    return result


def category_for(module_id: str, semantics: set[str], role_id: str | None) -> str:
    if role_id:
        return role_id
    if "hull_structure" in semantics:
        return f"{module_id}_category"
    semantic = sorted(semantics)[0] if semantics else "misc"
    return f"atrmrw_{semantic}"


def build(source_ledger: dict[str, Any], packing: dict[str, Any], prototypes: dict[str, Any]) -> dict[str, Any]:
    registry = source_ledger["source_modules"]
    prototype_by_key = {row["prototype_key"]: row for row in prototypes["prototypes"]}
    semantics = module_semantics(packing)
    compiled = []
    for row in source_ledger["logical_modules"]:
        module_id = row["logical_module_id"]
        usage_key = row["usages"][0]["prototype_key"]
        usage_prototype = prototype_by_key[usage_key]
        role_id = usage_prototype["role_id"] if "role" in semantics[module_id] else None
        if row["classification"] == "exact":
            source = registry[row["source_module_ids"][0]]
            add_stats = dict(source["effective_add_stats"])
            multiply_stats = dict(source["effective_multiply_stats"])
            formula = "identity_preserving_effective_stat_copy"
        elif row["classification"] == "aggregate_required":
            add_stats, multiply_stats, formula = aggregate_stats(row, registry)
        elif row["classification"] == "historical_new":
            add_stats, multiply_stats, formula = historical_stats(module_id, usage_prototype)
        else:
            raise ValueError(f"uncompilable module classification: {module_id}/{row['classification']}")
        payload = {
            "module_id": module_id,
            "category": category_for(module_id, semantics[module_id], role_id),
            "semantics": sorted(semantics[module_id]),
            "classification": row["classification"],
            "add_stats": {key: clean_number(value) for key, value in sorted(add_stats.items()) if value != 0},
            "multiply_stats": {key: clean_number(value) for key, value in sorted(multiply_stats.items()) if value != 0},
            "formula": formula,
            "source_module_ids": row.get("source_module_ids", []),
            "source_usages": row["usages"],
        }
        if role_id:
            payload["role_id"] = role_id
            payload["add_equipment_type"] = {
                "SRM_BB": "capital_ship",
                "SRM_CA": "capital_ship",
                "SRM_CV": "carrier",
            }.get(role_id)
            payload["mega_carrier"] = role_id == "SRM_CV"
        compiled.append(payload)

    compiled_by_id = {row["module_id"]: row for row in compiled}
    hulls = []
    packing_by_key = {row["prototype_key"]: row for row in packing["prototypes"]}
    for prototype in prototypes["prototypes"]:
        reference_modules = []
        defaults = []
        for slot in packing_by_key[prototype["prototype_key"]]["slots"]:
            module_id = slot.get("default_module_id")
            if module_id in {None, "empty"}:
                continue
            defaults.append(module_id)
            module_row = compiled_by_id[module_id]
            reference_modules.append({
                "slot_id": slot["logical_slot_id"],
                "module_id": module_id,
                "add_stats": module_row["add_stats"],
                "multiply_stats": module_row["multiply_stats"],
            })
        targets = {
            output_stat: float(prototype["computed"][target_key])
            for output_stat, target_key in TARGET_STATS.items()
        }
        raw_calibration = calibrate_reference(targets, reference_modules, {key: 1e-5 for key in targets})
        calibration = {
            stat: {
                "target": clean_number(record["target"]),
                "base": clean_number(record["frozen_base"]),
                "reference_add_total": clean_number(record["reference_add"]),
                "reference_multiply_total": clean_number(record["reference_multiply"]),
                "forward_result": clean_number(record["forward_value"]),
            }
            for stat, record in raw_calibration["stats"].items()
        }
        digest_payload = json.dumps(defaults, ensure_ascii=False, separators=(",", ":"))
        hulls.append({
            "prototype_key": prototype["prototype_key"],
            "hull_id": prototype["implementation_hull_id"],
            "profile_id": prototype["slot_profile_id"],
            "reference_modules": defaults,
            "reference_modules_digest_sha256": raw_calibration["reference_module_digest"],
            "calibration": calibration,
            "runtime_calibration_status": "pending_HOI4_1.19.2_controlled_experiment",
        })

    return {
        "status": "compiled_static_pending_runtime_calibration",
        "source_commit": source_ledger["source_commit"],
        "formula_contract": {
            "composition": "final=(base+A)*(1+M)",
            "batch_exponent": BATCH_EXPONENT,
            "power_reference_shp": POWER_REFERENCE_SHP,
            "power_reference_stats": POWER_REFERENCE_STATS,
            "unknown_numeric_policy": "identity module with no numeric contribution; never fabricate a stat",
        },
        "module_count": len(compiled),
        "modules": compiled,
        "hulls": hulls,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-ledger", type=Path, default=SOURCE_LEDGER)
    parser.add_argument("--packing", type=Path, default=PACKING)
    parser.add_argument("--prototypes", type=Path, default=PROTOTYPES)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    result = build(
        json.loads(args.source_ledger.read_text(encoding="utf-8")),
        json.loads(args.packing.read_text(encoding="utf-8")),
        json.loads(args.prototypes.read_text(encoding="utf-8")),
    )
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"ATRMRW module stats compiled: {result['module_count']} modules, {len(result['hulls'])} hulls")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
