#!/usr/bin/env python3
"""ATRMRW日本5艦級のmodule・船体・技術・localisationを生成する。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
DOCS = REPO / "documents/00_coding_contexts/atrmrw"
CONTRACT = DOCS / "ATRMRW_PHASE1_SLOT_CONTRACT.json"
PACKING = DOCS / "ATRMRW_PHASE3_JAPAN_SLOT_PACKING.json"
PROTOTYPES = DOCS / "ATRMRW_PHASE3_JAPAN_PROTOTYPE_LEDGER.json"
MODULE_LEDGER = DOCS / "ATRMRW_PHASE3_JAPAN_MODULE_LEDGER.json"
SSW_SOURCES = DOCS / "ATRMRW_PHASE3_SSW_PROTOTYPE_SOURCES.json"

MODULE_OUTPUT = REPO / "bakasekai/common/units/equipment/modules/_atrmrw_japan_modules.txt"
HULL_OUTPUT = REPO / "bakasekai/common/units/equipment/_atrmrw_japan_hulls.txt"
TECH_OUTPUT = REPO / "bakasekai/common/technologies/_atrmrw_japan_naval.txt"
VARIANT_OUTPUT = REPO / "bakasekai/common/scripted_effects/_atrmrw_japan_variants.txt"
LOC_EN_OUTPUT = REPO / "bakasekai/localisation/english/bakasekai/atrmrw_l_english.yml"
LOC_JA_OUTPUT = REPO / "bakasekai/localisation/japanese/bakasekai/atrmrw_l_japanese.yml"

ROLE_ALLOWLISTS = {
    "ship_hull_heavy": ["SRM_BB", "SRM_CA"],
    "ship_hull_cruiser": ["SRM_CA", "SRM_DD"],
    "ship_hull_light": ["SRM_DD"],
    "ship_hull_carrier": ["SRM_CV", "SRM_CA"],
    "ship_hull_submarine": ["SRM_SC"],
}

ARCHETYPE_BY_PROTOTYPE = {
    "jap_yamato": "ship_hull_heavy",
    "jap_takao": "ship_hull_cruiser",
    "jap_fubuki": "ship_hull_light",
    "jap_akagi": "ship_hull_carrier",
    "jap_i15": "ship_hull_submarine",
}

FALLBACK_BASE_STATS = {
    "jap_i15": {
        "surface_visibility": 11,
        "surface_detection": 6,
        "sub_detection": 2,
        "reliability": 0.40,
        "fuel_consumption": 4.5,
        "build_cost_ic": 300,
        "manpower": 94,
        "naval_dominance_factor": 90,
    },
}

JAPANESE_MODULE_NAMES = {
    "atrmrw_role_SRM_BB": "戦艦任務",
    "atrmrw_role_SRM_CA": "重巡洋艦任務",
    "atrmrw_role_SRM_DD": "駆逐艦任務",
    "atrmrw_role_SRM_CV": "航空母艦任務",
    "atrmrw_role_SRM_SC": "巡洋潜水艦任務",
    "atrmrw_jap_460mm_3x3_1942": "46cm三連装砲3基（1942年）",
    "atrmrw_jap_155mm_4x3_1942": "15.5cm三連装砲4基（1942年）",
    "atrmrw_jap_127mm_6x2_1942": "12.7cm連装高角砲6基（1942年）",
    "atrmrw_jap_25mm_8x3_1942": "25mm三連装機銃8基（1942年）",
    "atrmrw_jap_13_2mm_2x2_1942": "13.2mm連装機銃2基（1942年）",
    "atrmrw_jap_203mm_5x2_1932": "20.3cm連装砲5基（1932年）",
    "atrmrw_jap_120mm_4x1_1932": "12cm単装高角砲4基（1932年）",
    "atrmrw_jap_610mm_tt_4x2_16reload": "61cm連装魚雷発射管4基・予備魚雷16本",
    "atrmrw_jap_40mm_2x1_1932": "40mm単装機銃2基（1932年）",
    "atrmrw_jap_7_7mm_2x1_1932": "7.7mm単装機銃2基（1932年）",
    "atrmrw_jap_127mm_1x2_forward_1932": "艦首12.7cm連装砲1基（1932年）",
    "atrmrw_jap_127mm_2x2_aft_1932": "艦尾12.7cm連装砲2基（1932年）",
    "atrmrw_jap_610mm_tt_3x3_15reload": "61cm三連装魚雷発射管3基・魚雷15本",
    "atrmrw_jap_depth_charge_2dct_18": "爆雷投射機2基・爆雷18個",
    "atrmrw_jap_air_group_capacity_60_1927": "航空隊60機（1927年）",
    "atrmrw_jap_200mm_2x2_6x1_1927": "20cm連装砲2基・単装砲6基（1927年）",
    "atrmrw_jap_120mm_6x2_1927": "12cm連装高角砲6基（1927年）",
    "atrmrw_jap_6_5mm_22x1_1927": "6.5mm単装機銃22基（1927年）",
    "atrmrw_jap_140mm_1x1_i15": "14cm単装砲1基",
    "atrmrw_jap_533mm_bow_6_torpedo_17": "艦首53.3cm魚雷発射管6門・魚雷17本",
    "atrmrw_jap_25mm_1x2_i15": "25mm連装機銃1基",
    "atrmrw_jap_kampon_geared_turbine_4set_12boiler": "艦本式ギヤードタービン4基・ボイラー12基",
    "atrmrw_jap_kampon_geared_turbine_2set_4boiler": "艦本式ギヤードタービン2基・ボイラー4基",
    "atrmrw_jap_gihon_geared_turbine_4set_19boiler": "技本式ギヤードタービン4基・ボイラー19基",
    "atrmrw_jap_diesel_2_electric_2_i15": "艦本式ディーゼル2基・電動機2基",
    "atrmrw_power_150000_shp": "機関出力150,000馬力",
    "atrmrw_power_130000_shp": "機関出力130,000馬力",
    "atrmrw_power_50000_shp": "機関出力50,000馬力",
    "atrmrw_power_131200_shp": "機関出力131,200馬力",
    "atrmrw_power_12400_shp_2000_ehp": "水上12,400馬力・水中2,000馬力",
    "atrmrw_fuel_oil": "重油燃料",
    "atrmrw_fuel_mixed_oil_coal": "石炭・重油混焼",
    "atrmrw_fuel_diesel_oil": "ディーゼル油燃料",
    "atrmrw_endurance_oil_6300t_7200nm_16kn": "重油6,300t・航続7,200海里/16kt",
    "atrmrw_endurance_oil_2570t_8500nm_14kn": "重油2,570t・航続8,500海里/14kt",
    "atrmrw_endurance_oil_500t_4700nm_15kn": "重油500t・航続4,700海里/15kt",
    "atrmrw_endurance_mixed_6000t_8000nm_14kn": "混焼燃料6,000t・航続8,000海里/14kt",
    "atrmrw_endurance_diesel_220t_14000nm_16kn": "ディーゼル油220t・航続14,000海里/16kt",
    "atrmrw_structure_yamato_1942": "大和型船体構造（1942年）",
    "atrmrw_structure_takao_1932": "高雄型船体構造（1932年）",
    "atrmrw_structure_fubuki_1932": "吹雪型船体構造（1932年）",
    "atrmrw_structure_akagi_1927_three_flight_decks": "赤城型三段飛行甲板船体（1927年）",
    "atrmrw_structure_i15_six_bow_tubes": "伊十五型耐圧船殻・艦首発射管構造",
    "atrmrw_armor_material_vh": "VH装甲材",
    "atrmrw_armor_material_nvnc": "NVNC装甲材",
    "atrmrw_protection_unarmored": "非装甲船体",
    "atrmrw_armor_thickness_yamato_410_200": "舷側410mm・甲板200mm",
    "atrmrw_armor_thickness_takao_127_35": "舷側127mm・甲板35mm",
    "atrmrw_armor_thickness_akagi_152_79": "舷側152mm・甲板79mm",
    "atrmrw_jap_catapult_2_seaplane_7_f1m2": "射出機2基・零式水上観測機7機",
    "atrmrw_jap_catapult_2_seaplane_3": "射出機2基・水上機3機",
    "atrmrw_jap_mines_18": "機雷18個",
    "atrmrw_jap_three_flight_deck_arrangement_control": "三段飛行甲板配置管制",
    "atrmrw_jap_sub_catapult_e14y1": "潜水艦用射出機・零式小型水上機1機",
}


def number(value: float | int | str) -> str:
    numeric = float(value)
    if numeric.is_integer():
        return str(int(numeric))
    return f"{numeric:.6f}".rstrip("0").rstrip(".")


def block(name: str, values: dict[str, float], indent: str = "    ") -> list[str]:
    if not values:
        return []
    lines = [f"{indent}{name} = {{"]
    for key, value in sorted(values.items()):
        lines.append(f"{indent}  {key} = {number(value)}")
    lines.append(f"{indent}}}")
    return lines


def render_modules(module_ledger: dict[str, Any]) -> str:
    lines = ["equipment_modules = {"]
    for row in module_ledger["modules"]:
        lines.extend(["", f"  {row['module_id']} = {{", f"    category = {row['category']}", f"    gui_category = {row['category']}"])
        if row.get("add_equipment_type"):
            lines.append(f"    add_equipment_type = {row['add_equipment_type']}")
        if row.get("mega_carrier"):
            lines.append("    mega_carrier = yes")
        lines.extend(block("add_stats", row["add_stats"]))
        lines.extend(block("multiply_stats", row["multiply_stats"]))
        lines.append("  }")
    lines.extend([
        "",
        "  atrmrw_locked_visible = {",
        "    category = atrmrw_locked_visible",
        "    gui_category = atrmrw_locked_visible",
        "  }",
        "}",
        "",
    ])
    return "\n".join(lines)


def semantic_for_slot(slot_id: str) -> str:
    if slot_id == "role_slot":
        return "role"
    if slot_id.startswith("weapon_slot_"):
        return "weapon"
    if slot_id.startswith("special_slot_"):
        return "hull_feature"
    numbered = {
        "engineering_slot": ["propulsion_type", "propulsion_power", "fuel_energy", "fuel_endurance"],
        "protection_slot": ["hull_structure", "protection", "armor_thickness", "damage_control"],
        "sensor_slot": ["fire_control", "detection", "electronic_warfare", "sonar"],
    }
    prefix, suffix = slot_id.rsplit("_", 1)
    return numbered[prefix][int(suffix) - 1]


def category_for_empty(slot_id: str) -> str:
    return f"atrmrw_{semantic_for_slot(slot_id)}"


def render_hulls(contract: dict[str, Any], packing: dict[str, Any], prototypes: dict[str, Any], module_ledger: dict[str, Any], ssw_sources: dict[str, Any]) -> str:
    module_by_id = {row["module_id"]: row for row in module_ledger["modules"]}
    calibration_by_key = {row["prototype_key"]: row for row in module_ledger["hulls"]}
    prototype_by_key = {row["prototype_key"]: row for row in prototypes["prototypes"]}
    ssw_by_key = {row["prototype_key"]: row["base_stats"] for row in ssw_sources["prototypes"]}
    lines = ["equipments = {"]
    for packed in packing["prototypes"]:
        key = packed["prototype_key"]
        prototype = prototype_by_key[key]
        profile = contract["profiles"][prototype["slot_profile_id"]]
        contract_slots = {row["id"]: row for row in profile["slots"]}
        archetype = ARCHETYPE_BY_PROTOTYPE[key]
        lines.extend([
            "",
            f"  {prototype['implementation_hull_id']} = {{",
            f"    abbreviation = \"{prototype['role_id'].removeprefix('SRM_')}\"",
            f"    year = {prototype['reference_year']}",
            f"    archetype = {archetype}",
            "    module_slots = {",
        ])
        defaults: list[tuple[str, str]] = []
        for slot in packed["slots"]:
            slot_id = slot["logical_slot_id"]
            game_slot_id = contract_slots[slot_id]["game_slot_id"]
            module_id = slot.get("default_module_id")
            if slot["state"] == "locked":
                categories = ["atrmrw_locked_visible"]
                required = "yes"
                default = "atrmrw_locked_visible"
            elif slot_id == "role_slot":
                categories = ROLE_ALLOWLISTS[archetype]
                required = "yes"
                default = module_id
            elif "hull_structure" in contract_slots[slot_id]["semantic"]:
                categories = [module_by_id[module_id]["category"]]
                required = "yes"
                default = module_id
            else:
                categories = [module_by_id[module_id]["category"]] if module_id not in {None, "empty"} else [category_for_empty(slot_id)]
                required = "no"
                default = module_id or "empty"
            lines.append(f"      {game_slot_id} = {{ required = {required} allowed_module_categories = {{ {' '.join(categories)} }} }}")
            defaults.append((game_slot_id, default))
        lines.extend(["    }", "    default_modules = {"])
        for game_slot_id, default in defaults:
            lines.append(f"      {game_slot_id} = {default}")
        lines.append("    }")

        calibration = calibration_by_key[key]["calibration"]
        stats: dict[str, float | str] = {
            stat: row["base"] for stat, row in calibration.items()
        }
        stats.update(ssw_by_key.get(key, FALLBACK_BASE_STATS[key] if key in FALLBACK_BASE_STATS else {}))
        stats["armor_value"] = 0
        for stat, value in stats.items():
            lines.append(f"    {stat} = {number(value)}")
        lines.append("  }")
    lines.extend(["}", ""])
    return "\n".join(lines)


def render_technology(module_ledger: dict[str, Any], prototypes: dict[str, Any]) -> str:
    prototype_by_key = {row["prototype_key"]: row for row in prototypes["prototypes"]}
    hull_by_key = {row["prototype_key"]: row for row in module_ledger["hulls"]}
    prewar = ["jap_takao", "jap_fubuki", "jap_akagi"]
    wartime = ["jap_i15", "jap_yamato"]

    def tech(tech_id: str, keys: list[str], year: int, hidden: bool) -> list[str]:
        hull_ids = [prototype_by_key[key]["implementation_hull_id"] for key in keys]
        modules = sorted({module for key in keys for module in hull_by_key[key]["reference_modules"]})
        rows = [f"  {tech_id} = {{"]
        if hidden:
            rows.append("    allow = { always = no }")
        else:
            rows.extend([
                "    allow = { tag = JPN }",
                "    research_cost = 1.5",
                f"    start_year = {year}",
                "    folder = { name = mtgnavalfolder position = { x = 8 y = 24 } }",
                "    categories = { naval_equipment }",
                "    on_research_complete = { ATRMRW_JAP_wartime_ship_design = yes }",
            ])
        rows.append(f"    enable_equipments = {{ {' '.join(hull_ids)} }}")
        rows.append("    enable_equipment_modules = {")
        rows.extend(f"      {module}" for module in modules)
        rows.extend(["      atrmrw_locked_visible", "    }", "  }"])
        return rows

    lines = ["technologies = {"]
    lines.extend(tech("atrmrw_jap_prewar_prototypes", prewar, 1932, True))
    lines.append("")
    lines.extend(tech("atrmrw_jap_wartime_prototypes", wartime, 1941, False))
    lines.extend(["}", ""])
    return "\n".join(lines)


def render_variant_effect(contract: dict[str, Any], packing: dict[str, Any], prototypes: dict[str, Any]) -> str:
    prototype_by_key = {row["prototype_key"]: row for row in prototypes["prototypes"]}
    packing_by_key = {row["prototype_key"]: row for row in packing["prototypes"]}
    name_groups = {
        "jap_yamato": "JAP_BB_HISTORICAL",
        "jap_takao": "JAP_BC_HISTORICAL",
        "jap_fubuki": "JAP_DD_HISTORICAL",
        "jap_akagi": "JAP_CV_HISTORICAL",
        "jap_i15": "JAP_SS_HISTORICAL",
    }

    def effect(effect_id: str, keys: list[str]) -> list[str]:
        rows = [f"{effect_id} = {{", "  if = {", "    limit = { has_dlc = \"Man the Guns\" }"]
        for key in keys:
            prototype = prototype_by_key[key]
            packed = packing_by_key[key]
            profile = contract["profiles"][prototype["slot_profile_id"]]
            game_ids = {slot["id"]: slot["game_slot_id"] for slot in profile["slots"]}
            rows.extend([
                "    create_equipment_variant = {",
                f"      name = \"{prototype['name_japanese']}\"",
                f"      type = {prototype['implementation_hull_id']}",
                f"      name_group = {name_groups[key]}",
                "      parent_version = 0",
                "      modules = {",
            ])
            for slot in packed["slots"]:
                default = slot.get("default_module_id")
                if default is None:
                    default = "atrmrw_locked_visible" if slot["state"] == "locked" else "empty"
                rows.append(f"        {game_ids[slot['logical_slot_id']]} = {default}")
            rows.extend(["      }", "    }"])
        rows.extend(["  }", "}"])
        return rows

    lines = effect("ATRMRW_JAP_prewar_ship_design", ["jap_takao", "jap_fubuki", "jap_akagi"])
    lines.append("")
    lines.extend(effect("ATRMRW_JAP_wartime_ship_design", ["jap_i15", "jap_yamato"]))
    lines.append("")
    return "\n".join(lines)


def display_name(module_id: str) -> str:
    return module_id.removeprefix("atrmrw_").replace("_", " ")


def render_localisation(language: str, prototypes: dict[str, Any], module_ledger: dict[str, Any]) -> str:
    japanese = language == "japanese"
    lines = [f"l_{language}:"]
    for prototype in prototypes["prototypes"]:
        name = prototype["name_japanese"] if japanese else prototype["name_english"]
        lines.append(f" {prototype['implementation_hull_id']}:0 \"{name}\"")
        description = (
            f"ATRMRW史実艦級船体。{prototype['reference_year']}年基準状態。"
            if japanese else
            f"ATRMRW historical class hull; {prototype['reference_year']} reference configuration."
        )
        lines.append(f" {prototype['implementation_hull_id']}_desc:0 \"{description}\"")
    for row in module_ledger["modules"]:
        name = JAPANESE_MODULE_NAMES[row["module_id"]] if japanese else display_name(row["module_id"])
        description = (
            f"出典と計算式を追跡したATRMRWモジュール（{row['formula']}）。"
            if japanese else
            f"ATRMRW source-tracked module ({row['formula']})."
        )
        lines.append(f" {row['module_id']}:0 \"{name}\"")
        lines.append(f" {row['module_id']}_desc:0 \"{description}\"")
    if japanese:
        lines.extend([
            " atrmrw_locked_visible:0 \"使用不能な可視スロット\"",
            " atrmrw_locked_visible_desc:0 \"この物理位置は表示されるが、この船体では使用できない。\"",
            " atrmrw_jap_prewar_prototypes:0 \"ATRMRW日本海軍戦前艦級\"",
            " atrmrw_jap_wartime_prototypes:0 \"ATRMRW日本海軍戦時艦級\"",
            " atrmrw_jap_wartime_prototypes_desc:0 \"伊十五型と大和型の史実プロトタイプ船体を解禁する。\"",
            "",
        ])
    else:
        lines.extend([
            " atrmrw_locked_visible:0 \"Locked visible slot\"",
            " atrmrw_locked_visible_desc:0 \"This physical position is visible but unavailable on this hull.\"",
            " atrmrw_jap_prewar_prototypes:0 \"ATRMRW Japanese prewar classes\"",
            " atrmrw_jap_wartime_prototypes:0 \"ATRMRW Japanese wartime classes\"",
            " atrmrw_jap_wartime_prototypes_desc:0 \"Unlocks the I-15 and Yamato historical prototype hulls.\"",
            "",
        ])
    return "\n".join(lines)


def main() -> int:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    packing = json.loads(PACKING.read_text(encoding="utf-8"))
    prototypes = json.loads(PROTOTYPES.read_text(encoding="utf-8"))
    module_ledger = json.loads(MODULE_LEDGER.read_text(encoding="utf-8"))
    ssw_sources = json.loads(SSW_SOURCES.read_text(encoding="utf-8"))
    outputs = {
        MODULE_OUTPUT: (render_modules(module_ledger), "utf-8"),
        HULL_OUTPUT: (render_hulls(contract, packing, prototypes, module_ledger, ssw_sources), "utf-8"),
        TECH_OUTPUT: (render_technology(module_ledger, prototypes), "utf-8"),
        VARIANT_OUTPUT: (render_variant_effect(contract, packing, prototypes), "utf-8"),
        LOC_EN_OUTPUT: (render_localisation("english", prototypes, module_ledger), "utf-8-sig"),
        LOC_JA_OUTPUT: (render_localisation("japanese", prototypes, module_ledger), "utf-8-sig"),
    }
    for path, (content, encoding) in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding=encoding, newline="")
        print(f"ATRMRW game file generated: {path.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
