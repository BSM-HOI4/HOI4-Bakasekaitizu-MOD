#!/usr/bin/env python3
"""Phase 3日本5艦級の論理スロットpackingを生成する。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
DEFAULT_CONTRACT = REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE1_SLOT_CONTRACT.json"
DEFAULT_LEDGER = REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE3_JAPAN_PROTOTYPE_LEDGER.json"
DEFAULT_OUTPUT = REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE3_JAPAN_SLOT_PACKING.json"


def module(module_id: str, kind: str, evidence: str, *, batch_key: str | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "state": "editable",
        "assignment_kind": kind,
        "default_module_id": module_id,
        "source_type": "prototype_nsdb",
        "evidence": evidence,
    }
    if batch_key is not None:
        result["batch_key"] = batch_key
    return result


def derived(module_id: str, kind: str, evidence: str) -> dict[str, Any]:
    return {
        "state": "editable",
        "assignment_kind": kind,
        "default_module_id": module_id,
        "source_type": "atrmrw_design_contract",
        "evidence": evidence,
    }


def unresolved(kind: str, reason: str) -> dict[str, Any]:
    return {
        "state": "editable",
        "assignment_kind": kind,
        "default_module_id": None,
        "source_type": "unresolved",
        "evidence": "The selected historical source does not provide a safe normalized value.",
        "unresolved_reason": reason,
    }


def empty_editable(kind: str, evidence: str) -> dict[str, Any]:
    """枠は編集可能だが、根拠のない既定装備を捏造せずemptyにする。"""
    return {
        "state": "editable",
        "assignment_kind": kind,
        "default_module_id": "empty",
        "source_type": "prototype_nsdb",
        "evidence": evidence,
    }


PACKING: dict[str, dict[str, dict[str, Any]]] = {
    "jap_yamato": {
        "role_slot": derived("atrmrw_role_SRM_BB", "role", "SSW role taxonomy: SRM_BB."),
        "weapon_slot_01": module("atrmrw_jap_460mm_3x3_1942", "weapon_batch", "3 x 3 - 460/45 94-shiki.", batch_key="yamato_460_main_3x3"),
        "weapon_slot_02": module("atrmrw_jap_155mm_4x3_1942", "weapon_batch", "4 x 3 - 155/60 3-shiki.", batch_key="yamato_155_secondary_4x3"),
        "weapon_slot_03": module("atrmrw_jap_127mm_6x2_1942", "weapon_batch", "6 x 2 - 127/40 89-shiki.", batch_key="yamato_127_dp_6x2"),
        "weapon_slot_05": module("atrmrw_jap_25mm_8x3_1942", "weapon_batch", "Yamato reference: 8 x 3 - 25/60 96-shiki.", batch_key="yamato_25_aa_8x3"),
        "weapon_slot_06": module("atrmrw_jap_13_2mm_2x2_1942", "weapon_batch", "2 x 2 - 13.2/76.", batch_key="yamato_13_2_aa_2x2"),
        "engineering_slot_01": module("atrmrw_jap_kampon_geared_turbine_4set_12boiler", "propulsion_type", "4 sets Kampon geared steam turbines + 12 Kampon boilers."),
        "engineering_slot_02": module("atrmrw_power_150000_shp", "propulsion_power", "Power: 150000 shp."),
        "engineering_slot_03": module("atrmrw_fuel_oil", "fuel_energy", "Fuel: oil 6300 t."),
        "engineering_slot_04": module("atrmrw_endurance_oil_6300t_7200nm_16kn", "fuel_endurance", "Fuel 6300 t; endurance 7200 nm at 16 kn."),
        "protection_slot_01": derived("atrmrw_structure_yamato_1942", "hull_structure", "Historical hull structure; the only fixed-visible singleton."),
        "protection_slot_02": module("atrmrw_armor_material_vh", "protection", "Yamato-class armor material normalization: VH."),
        "protection_slot_03": module("atrmrw_armor_thickness_yamato_410_200", "armor_thickness", "Ship protection: 410 mm main belt and 200 mm main deck (230 mm outer parts)."),
        "protection_slot_04": empty_editable("damage_control", "No traceable 1942 damage-control equipment record was selected; the visible editable slot starts empty."),
        "sensor_slot_01": empty_editable("fire_control", "Electronic_equipment is empty in the selected 1942 NSDB record; the visible editable slot starts empty."),
        "special_slot_01": module("atrmrw_jap_catapult_2_seaplane_7_f1m2", "special_equipment", "2 catapults + 7 F1M2 seaplanes."),
    },
    "jap_takao": {
        "role_slot": derived("atrmrw_role_SRM_CA", "role", "SSW role taxonomy: SRM_CA."),
        "weapon_slot_01": module("atrmrw_jap_203mm_5x2_1932", "weapon_batch", "5 x 2 - 203/50 3-shiki.", batch_key="takao_203_main_5x2"),
        "weapon_slot_02": module("atrmrw_jap_120mm_4x1_1932", "weapon_batch", "4 x 1 - 120/45 10-shiki.", batch_key="takao_120_dp_4x1"),
        "weapon_slot_03": module("atrmrw_jap_610mm_tt_4x2_16reload", "weapon_batch", "4 x 2 - 610 TT (16 torpedoes).", batch_key="takao_610_tt_4x2"),
        "weapon_slot_04": module("atrmrw_jap_40mm_2x1_1932", "weapon_batch", "2 x 1 - 40/62 HI 91-shiki.", batch_key="takao_40_aa_2x1"),
        "weapon_slot_05": module("atrmrw_jap_7_7mm_2x1_1932", "weapon_batch", "2 x 1 - 7.7/80.", batch_key="takao_7_7_aa_2x1"),
        "engineering_slot_01": module("atrmrw_jap_kampon_geared_turbine_4set_12boiler", "propulsion_type", "4 sets Kampon geared steam turbines + 12 Kampon boilers."),
        "engineering_slot_02": module("atrmrw_power_130000_shp", "propulsion_power", "Power: 130000 shp."),
        "engineering_slot_03": module("atrmrw_fuel_oil", "fuel_energy", "Fuel: oil 2570 t."),
        "engineering_slot_04": module("atrmrw_endurance_oil_2570t_8500nm_14kn", "fuel_endurance", "Takao/Atago endurance: 8500 nm at 14 kn."),
        "protection_slot_01": derived("atrmrw_structure_takao_1932", "hull_structure", "Historical hull structure; the only fixed-visible singleton."),
        "protection_slot_02": module("atrmrw_armor_material_nvnc", "protection", "Takao-class armor material normalization: NVNC."),
        "protection_slot_03": module("atrmrw_armor_thickness_takao_127_35", "armor_thickness", "Ship protection: 127 mm maximum belt abreast magazines and 35 mm main deck."),
        "sensor_slot_01": empty_editable("fire_control", "No exact 1932 fire-control equipment mapping was selected; the visible editable slot starts empty."),
        "special_slot_01": module("atrmrw_jap_catapult_2_seaplane_3", "special_equipment", "2 catapults + 3 seaplanes."),
    },
    "jap_fubuki": {
        "role_slot": derived("atrmrw_role_SRM_DD", "role", "SSW role taxonomy: SRM_DD."),
        "weapon_slot_01": module("atrmrw_jap_127mm_1x2_forward_1932", "weapon_batch", "One forward twin mount from 3 x 2 - 127/50 3-shiki.", batch_key="fubuki_127_forward_1x2"),
        "weapon_slot_02": module("atrmrw_jap_127mm_2x2_aft_1932", "weapon_batch", "Two aft twin mounts from 3 x 2 - 127/50 3-shiki.", batch_key="fubuki_127_aft_2x2"),
        "weapon_slot_03": module("atrmrw_jap_610mm_tt_3x3_15reload", "weapon_batch", "3 x 3 - 610 TT (15 torpedoes).", batch_key="fubuki_610_tt_3x3"),
        "weapon_slot_04": module("atrmrw_jap_depth_charge_2dct_18", "weapon_batch", "2 DCT (18 depth charges).", batch_key="fubuki_depth_charge_2dct"),
        "weapon_slot_05": module("atrmrw_jap_7_7mm_2x1_1932", "weapon_batch", "2 x 1 - 7.7/80.", batch_key="fubuki_7_7_aa_2x1"),
        "engineering_slot_01": module("atrmrw_jap_kampon_geared_turbine_2set_4boiler", "propulsion_type", "2 sets Kampon geared steam turbines + 4 Kampon boilers."),
        "engineering_slot_02": module("atrmrw_power_50000_shp", "propulsion_power", "Power: 50000 shp."),
        "engineering_slot_03": module("atrmrw_fuel_oil", "fuel_energy", "Fuel: oil 500 t."),
        "engineering_slot_04": module("atrmrw_endurance_oil_500t_4700nm_15kn", "fuel_endurance", "Fuel 500 t; endurance 4700 nm at 15 kn."),
        "protection_slot_01": derived("atrmrw_structure_fubuki_1932", "hull_structure", "Historical hull structure; the only fixed-visible singleton."),
        "protection_slot_02": derived("atrmrw_protection_unarmored", "protection", "Destroyer unarmored protection class."),
        "sensor_slot_01": empty_editable("fire_control", "No exact 1932 fire-control equipment mapping was selected; the visible editable slot starts empty."),
        "special_slot_01": module("atrmrw_jap_mines_18", "special_equipment", "Capacity: 18 mines."),
    },
    "jap_akagi": {
        "role_slot": derived("atrmrw_role_SRM_CV", "role", "SSW role taxonomy: SRM_CV."),
        "weapon_slot_01": module("atrmrw_jap_air_group_capacity_60_1927", "aviation_batch", "Air group: 60 aircraft.", batch_key="akagi_air_group_60"),
        "weapon_slot_02": module("atrmrw_jap_200mm_2x2_6x1_1927", "weapon_batch", "2 x 2 + 6 x 1 - 200/50 3-shiki.", batch_key="akagi_200_battery"),
        "weapon_slot_03": module("atrmrw_jap_120mm_6x2_1927", "weapon_batch", "6 x 2 - 120/45 10-shiki.", batch_key="akagi_120_dp_6x2"),
        "weapon_slot_04": module("atrmrw_jap_6_5mm_22x1_1927", "weapon_batch", "22 x 1 - 6.5/115.", batch_key="akagi_6_5_aa_22x1"),
        "engineering_slot_01": module("atrmrw_jap_gihon_geared_turbine_4set_19boiler", "propulsion_type", "4 sets Gihon geared steam turbines + 19 Kampon boilers."),
        "engineering_slot_02": module("atrmrw_power_131200_shp", "propulsion_power", "Power: 131200 shp."),
        "engineering_slot_03": module("atrmrw_fuel_mixed_oil_coal", "fuel_energy", "Fuel: oil 3900 t + coal 2100 t."),
        "engineering_slot_04": module("atrmrw_endurance_mixed_6000t_8000nm_14kn", "fuel_endurance", "Mixed fuel 6000 t; endurance 8000 nm at 14 kn."),
        "protection_slot_01": derived("atrmrw_structure_akagi_1927_three_flight_decks", "hull_structure", "The 1927 three-flight-deck arrangement is represented inside the sole fixed hull-structure singleton."),
        "protection_slot_02": module("atrmrw_armor_material_nvnc", "protection", "Akagi-class armor material normalization: NVNC."),
        "protection_slot_03": module("atrmrw_armor_thickness_akagi_152_79", "armor_thickness", "Ship protection: 152 mm main belt and 79-57 mm main deck."),
        "protection_slot_04": empty_editable("damage_control", "No traceable 1927 damage-control equipment record was selected; the visible editable slot starts empty."),
        "special_slot_01": derived("atrmrw_jap_three_flight_deck_arrangement_control", "special_equipment", "Editable control entry for the 1927 three-flight-deck arrangement; structural geometry remains in hull_structure."),
    },
    "jap_i15": {
        "role_slot": derived("atrmrw_role_SRM_SC", "role", "SSW role taxonomy: SRM_SC."),
        "weapon_slot_01": module("atrmrw_jap_140mm_1x1_i15", "weapon_batch", "Most boats: 1 x 1 - 140/40 11-shiki.", batch_key="i15_140_deck_gun_1x1"),
        "weapon_slot_03": module("atrmrw_jap_533mm_bow_6_torpedo_17", "weapon_batch", "6 bow 533 mm TT; 17 torpedoes.", batch_key="i15_533_tt_6_bow"),
        "weapon_slot_04": module("atrmrw_jap_25mm_1x2_i15", "weapon_batch", "1 x 2 - 25/60 96-shiki.", batch_key="i15_25_aa_1x2"),
        "engineering_slot_01": module("atrmrw_jap_diesel_2_electric_2_i15", "propulsion_type", "2 Kampon diesels / 2 electric motors."),
        "engineering_slot_02": module("atrmrw_power_12400_shp_2000_ehp", "propulsion_power", "Surface/submerged power: 12400 / 2000."),
        "engineering_slot_03": module("atrmrw_fuel_diesel_oil", "fuel_energy", "Fuel: diesel oil 220 t."),
        "engineering_slot_04": module("atrmrw_endurance_diesel_220t_14000nm_16kn", "fuel_endurance", "Surface endurance 14000 nm at 16 kn; submerged endurance 96 nm at 3 kn retained as module evidence."),
        "protection_slot_01": derived("atrmrw_structure_i15_six_bow_tubes", "hull_structure", "Pressure hull and six bow tubes are represented inside the sole fixed hull-structure singleton."),
        "protection_slot_02": derived("atrmrw_protection_unarmored", "protection", "Submarine unarmored protection class."),
        "sensor_slot_02": empty_editable(
            "detection",
            "Type 93 sonar/hydrophone is historically listed, but no identity-preserving SSW stat source was found; the visible editable slot starts empty.",
        ),
        "special_slot_01": module("atrmrw_jap_sub_catapult_e14y1", "special_equipment", "1 catapult + 1 E14Y1 seaplane."),
    },
}


def source_for(spec: dict[str, Any], prototype: dict[str, Any]) -> dict[str, str]:
    source_type = spec["source_type"]
    if source_type == "prototype_nsdb":
        source_ref = prototype["source"]["source_id"]
    elif source_type == "atrmrw_design_contract":
        source_ref = "ATRMRW_PHASE1_SLOT_CONTRACT.json"
    else:
        source_ref = prototype["source"]["source_id"]
    return {
        "source_type": source_type,
        "source_ref": source_ref,
        "evidence": spec["evidence"],
    }


def build(contract: dict[str, Any], ledger: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for prototype in ledger["prototypes"]:
        key = prototype["prototype_key"]
        profile_id = prototype["slot_profile_id"]
        profile = contract["profiles"][profile_id]
        assignments = PACKING[key]
        slots = []
        for contract_slot in profile["slots"]:
            slot_id = contract_slot["id"]
            spec = assignments.get(slot_id)
            if spec is None:
                slots.append({
                    "logical_slot_id": slot_id,
                    "state": "locked_visible",
                    "assignment_kind": "unused",
                    "default_module_id": None,
                    "source": {
                        "source_type": "packing_policy",
                        "source_ref": "ATRMRW_PHASE1_SLOT_CONTRACT.json",
                        "evidence": "No reference-year default is assigned; the visible unused slot is locked.",
                    },
                    "unused_reason": "No reference-year historical default is assigned to this logical slot.",
                })
                continue
            state = "fixed_visible" if spec["assignment_kind"] == "hull_structure" else spec["state"]
            row = {
                "logical_slot_id": slot_id,
                "state": state,
                "assignment_kind": spec["assignment_kind"],
                "default_module_id": spec["default_module_id"],
                "source": source_for(spec, prototype),
            }
            if "batch_key" in spec:
                row["batch_key"] = spec["batch_key"]
            if "unresolved_reason" in spec:
                row["unresolved_reason"] = spec["unresolved_reason"]
            slots.append(row)
        rows.append({
            "prototype_key": key,
            "implementation_hull_id": prototype["implementation_hull_id"],
            "slot_profile_id": profile_id,
            "role_id": prototype["role_id"],
            "slot_count": len(slots),
            "slots": slots,
        })
    return {
        "status": "logical_slot_packing_approved",
        "generated_from": {
            "slot_contract": "ATRMRW_PHASE1_SLOT_CONTRACT.json",
            "prototype_ledger": "ATRMRW_PHASE3_JAPAN_PROTOTYPE_LEDGER.json",
        },
        "policy": {
            "hidden_slot_count": 0,
            "editable": "role, propulsion, fuel, protection, sensors, historical batches, historical overflow and occupied special equipment",
            "fixed_visible": "exactly one hull_structure singleton per prototype",
            "locked_visible": "visible unused logical slots only",
            "module_id_status": "logical IDs pending concrete HOI4 module definitions",
        },
        "prototype_count": len(rows),
        "prototypes": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    result = build(contract, ledger)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"ATRMRW Japan slot packing: {result['prototype_count']} classes, {sum(row['slot_count'] for row in result['prototypes'])} visible slots")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
