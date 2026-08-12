#!/usr/bin/env python3
"""承認済みATRMRW Phase 1スロット契約と現行BSM割当表を生成する。"""

from __future__ import annotations

import csv
import json
from pathlib import Path

try:
    from .gui_layout import coordinate_for
except ImportError:
    from gui_layout import coordinate_for


REPO = Path(__file__).resolve().parents[2]
OUT_DIR = REPO / "documents/00_coding_contexts/atrmrw"
CONTRACT_PATH = OUT_DIR / "ATRMRW_PHASE1_SLOT_CONTRACT.json"
MAP_PATH = OUT_DIR / "ATRMRW_PHASE1_HULL_PROFILE_MAP.csv"
INVENTORY_PATH = OUT_DIR / "ATRMRW_PHASE0_BSM_INVENTORY.json"


PROFILE_SPECS = {
    "maximum_36": (36, 19, 4, 4, 4, 4),
    "capital_30": (30, 15, 4, 4, 3, 3),
    "large_24": (24, 11, 4, 3, 3, 2),
    "medium_18": (18, 8, 4, 2, 2, 1),
    "escort_15": (15, 6, 4, 2, 1, 1),
    "coastal_12": (12, 5, 4, 1, 1, 0),
    "minimal_9": (9, 2, 4, 1, 1, 0),
}

CUSTOM_COUNTS = {
    "maximum_36": 18,
    "capital_30": 15,
    "large_24": 12,
    "medium_18": 9,
    "escort_15": 7,
    "coastal_12": 6,
    "minimal_9": 3,
}


def slot(slot_id: str, zone: str, state: str, semantic: str) -> dict[str, object]:
    return {"id": slot_id, "zone": zone, "state": state, "semantic": [semantic]}


def build_slots(total: int, weapons: int, engineering: int, protection: int,
                sensors: int, special: int) -> list[dict[str, object]]:
    # SSW互換のship_type_slotはfixed_接頭辞を持たず、custom 0へ入る。
    result = [slot("role_slot", "fixed", "editable", "role")]

    weapon_semantics = [
        "primary_armament", "secondary_armament", "primary_sub_armament",
        "secondary_sub_armament", "primary_light_armament",
        "secondary_light_armament", "historical_overflow",
    ]
    zones = ["front", "rear", "mid", "mid", "front", "rear", "optional"]
    for index in range(weapons):
        semantic_index = index if index < 6 else 6
        result.append(slot(
            f"weapon_slot_{index + 1:02d}", zones[index % len(zones)], "editable",
            weapon_semantics[semantic_index],
        ))

    engineering_semantics = [
        "propulsion_type", "propulsion_power", "fuel_energy", "fuel_endurance",
    ]
    for index in range(engineering):
        result.append(slot(
            f"engineering_slot_{index + 1:02d}", "mid", "editable",
            engineering_semantics[index],
        ))

    protection_semantics = [
        "hull_structure", "protection", "armor_thickness", "damage_control",
    ]
    for index in range(protection):
        result.append(slot(
            f"protection_slot_{index + 1:02d}", "fixed",
            "fixed_visible" if index == 0 else "editable",
            protection_semantics[index],
        ))

    sensor_semantics = ["fire_control", "detection", "electronic_warfare", "sonar"]
    for index in range(sensors):
        result.append(slot(
            f"sensor_slot_{index + 1:02d}", "optional", "editable",
            sensor_semantics[index],
        ))

    for index in range(special):
        result.append(slot(
            f"special_slot_{index + 1:02d}", "optional", "editable", "hull_feature",
        ))

    if len(result) != total:
        raise ValueError(f"profile generation mismatch: expected {total}, got {len(result)}")
    return result


def assign_ui_indices(profile_id: str, slots: list[dict[str, object]]) -> None:
    """最大fixed 18/custom 18のSSW互換nested index契約を付与する。"""
    custom_budget = CUSTOM_COUNTS[profile_id]
    weapon_ids = [slot["id"] for slot in slots if str(slot["id"]).startswith("weapon_slot_")]
    fixed_weapon_count = len(weapon_ids) - (custom_budget - 1)
    fixed_weapon_ids = set(weapon_ids[:fixed_weapon_count])
    indices = {"fixed": 0, "custom": 0}
    for slot in slots:
        slot_id = str(slot["id"])
        group = (
            "custom"
            if slot_id == "role_slot" or (slot_id.startswith("weapon_slot_") and slot["id"] not in fixed_weapon_ids)
            else "fixed"
        )
        slot["ui_group"] = group
        slot["ui_index"] = indices[group]
        if slot_id == "role_slot":
            slot["game_slot_id"] = "ship_type_slot"
        else:
            slot["game_slot_id"] = (
                f"fixed_atrmrw_{slot['id']}"
                if group == "fixed"
                else f"atrmrw_{slot['id']}_custom_slot"
            )
        slot["profile_min"] = int(profile_id.rsplit("_", 1)[1])
        slot["x"], slot["y"] = coordinate_for(group, indices[group])
        slot["coordinate_status"] = "verified_static_HOI4_1.19.2_baseline"
        indices[group] += 1
    if indices["custom"] != custom_budget:
        raise ValueError(f"{profile_id}: custom budget mismatch")


def profile_for_hull(source_path: str, hull_id: str) -> tuple[str, str]:
    if "carrier" in source_path:
        if "escort" in hull_id:
            return "medium_18", "escort carrier aviation adjustment"
        if "mega" in hull_id:
            return "maximum_36", "large aviation platform"
        if hull_id in {"ship_hull_carrier_modern", "modern_carrier"}:
            return "maximum_36", "modern large aviation platform"
        if hull_id == "ship_hull_carrier_conversion_ca":
            return "large_24", "cruiser conversion"
        return "capital_30", "standard carrier aviation adjustment"

    if "heavy" in source_path:
        if "super_heavy" in hull_id or hull_id.startswith("SH_battleship"):
            return "maximum_36", "super-heavy capital hull"
        if "pre_dreadnought" in hull_id:
            return "large_24", "pre-dreadnought size band"
        return "capital_30", "standard capital hull"

    if "cruiser" in source_path:
        if "heavy_cruiser" in hull_id or any(token in hull_id for token in (
            "panzerschiff", "coastal_defense", "modern_aa",
        )):
            return "large_24", "heavy or specialist cruiser"
        return "medium_18", "light or generic cruiser"

    if "light" in source_path:
        return "escort_15", "destroyer/light combatant"

    if "submarine" in source_path:
        if "midget" in hull_id:
            return "minimal_9", "midget submarine"
        if hull_id in {"ship_hull_submarine", "ship_hull_submarine_1", "submarine_1"}:
            return "coastal_12", "early/coastal submarine"
        if any(token in hull_id for token in (
            "cruiser_submarine", "carrier_submarine", "fleet_submarine",
            "nuclear_missile",
        )):
            return "medium_18", "large or special-purpose submarine"
        return "escort_15", "ocean-going submarine"

    if "repair_ships" in source_path or "support_ships" in source_path:
        return "medium_18", "support vessel with visible service equipment"
    raise ValueError(f"unmapped hull source: {source_path}/{hull_id}")


def main() -> int:
    profiles = {}
    for profile_id, spec in PROFILE_SPECS.items():
        total, weapons, engineering, protection, sensors, special = spec
        profiles[profile_id] = {
            "total_slot_count": total,
            "category_budget": {
                "role": 1,
                "weapons_and_aviation": weapons,
                "engineering_and_fuel": engineering,
                "protection_and_damage_control": protection,
                "sensors": sensors,
                "special_equipment": special,
            },
            "slots": build_slots(*spec),
        }
        assign_ui_indices(profile_id, profiles[profile_id]["slots"])

    contract = {
        "status": "approved",
        "approved_on": "2026-08-02",
        "approval_basis": "user decisions 1-5 plus SSW-sync/all-visible/9-to-36 supplement",
        "ssw_source_commit": "4bcb07d5c11f3c78c3383db393abc9bbbf4dbdc1",
        "semantic_contract": {
            "required_armament_slots": [
                "primary_armament", "secondary_armament", "primary_sub_armament",
                "secondary_sub_armament", "primary_light_armament",
                "secondary_light_armament",
            ],
            "historical_overflow": "visible_same-role-and-zone_batch_modules",
            "hidden_slot_count": 0,
        },
        "profile_order": list(PROFILE_SPECS),
        "profiles": profiles,
        "assignment_contract": {
            "primary_axis": "physical_size_and_displacement",
            "role_axis": "SSW ship_type_slot taxonomy",
            "role_does_not_select_profile": True,
            "aircraft_facility_adjustment": "normally_one_size_band_up",
            "submarine_assignment": "separate size ladder; do not compare directly with surface displacement",
            "individual_override_required": True,
        },
        "role_contract": {
            "physical_slot": True,
            "visible": True,
            "editable": True,
            "implementation": "visible_ship_type_slot_using_SSW_role_taxonomy",
            "game_slot_id": "ship_type_slot",
            "ui_group": "custom",
            "ui_index": 0,
        },
        "visibility_contract": {
            "hidden_slots_allowed": False,
            "all_slots_have_gui_widget": True,
            "fixed_modules_remain_visible": True,
            "only_hull_structure_is_fixed_singleton": True,
            "locked_state_is_assigned_per_resolved_hull_not_base_profile": True,
        },
        "gui_index_contract": {
            "maximum_fixed_indices": "0..17",
            "maximum_custom_indices": "0..17",
            "nested_prefix_indices": True,
            "pixel_coordinates": "derive_from_installed_HOI4_1.19.2_vanilla_baseline",
        },
    }
    CONTRACT_PATH.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    rows = []
    for source_path, hull_ids in inventory["hulls"]["by_file"].items():
        for hull_id in hull_ids:
            profile_id, basis = profile_for_hull(source_path, hull_id)
            slots = profiles[profile_id]["slots"]
            rows.append({
                "hull_id": hull_id,
                "source_path": source_path,
                "ssw_role_source": "ship_type_slot",
                "profile_id": profile_id,
                "total_slot_count": profiles[profile_id]["total_slot_count"],
                "editable_slot_count": sum(s["state"] == "editable" for s in slots),
                "fixed_visible_slot_count": sum(s["state"] == "fixed_visible" for s in slots),
                "locked_visible_slot_count": sum(s["state"] == "locked" for s in slots),
                "hidden_slot_count": 0,
                "assignment_basis": basis,
                "provisional_displacement_review": "yes",
            })
    with MAP_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda row: row["hull_id"]))
    print(f"wrote {CONTRACT_PATH.relative_to(REPO)} ({len(profiles)} profiles)")
    print(f"wrote {MAP_PATH.relative_to(REPO)} ({len(rows)} hulls)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
