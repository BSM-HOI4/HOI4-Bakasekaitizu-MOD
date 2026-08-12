#!/usr/bin/env python3
"""NSDBの一意URLから日本海軍5艦級プロトタイプ台帳を再生成する。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

try:
    from .calculations import (
        HP_FORMULA_ID,
        ORG_FORMULA_ID,
        RANGE_FORMULA_ID,
        SPEED_FORMULA_ID,
        calculate_base_org,
        calculate_base_strength,
        target_naval_range,
        target_naval_speed,
    )
    from .nsdb_readonly import database_manifest, select_by_source_url
except ImportError:  # 直接スクリプト実行時
    from calculations import (
        HP_FORMULA_ID,
        ORG_FORMULA_ID,
        RANGE_FORMULA_ID,
        SPEED_FORMULA_ID,
        calculate_base_org,
        calculate_base_strength,
        target_naval_range,
        target_naval_speed,
    )
    from nsdb_readonly import database_manifest, select_by_source_url


PROTOTYPES = {
    "jap_yamato": {
        "implementation_hull_id": "ship_hull_JAP_BB_3",
        "name_english": "Yamato class",
        "name_japanese": "大和型",
        "url": "https://myownonpmirror.com/ships/japan/jap_bb_yamato.html",
        "reference_year": 1942,
        "role_id": "SRM_BB",
        "hull_type": "capital",
        "slot_profile_id": "maximum_36",
        "displacement_rule": "Displacement_full maximum numeric value",
    },
    "jap_takao": {
        "implementation_hull_id": "ship_hull_JAP_CA_0",
        "name_english": "Takao class",
        "name_japanese": "高雄型",
        "url": "https://myownonpmirror.com/ships/japan/jap_cr_takao.html",
        "reference_year": 1932,
        "role_id": "SRM_CA",
        "hull_type": "cruiser",
        "slot_profile_id": "large_24",
        "displacement_rule": "Displacement_full maximum numeric value",
    },
    "jap_fubuki": {
        "implementation_hull_id": "ship_hull_JAP_DD_13",
        "name_english": "Fubuki class",
        "name_japanese": "吹雪型",
        "url": "https://myownonpmirror.com/ships/japan/jap_dd_fubuki.html",
        "reference_year": 1932,
        "role_id": "SRM_DD",
        "hull_type": "light",
        "slot_profile_id": "escort_15",
        "displacement_rule": "Displacement_full maximum numeric value",
    },
    "jap_akagi": {
        "implementation_hull_id": "ship_hull_JAP_CV_0",
        "name_english": "Akagi class",
        "name_japanese": "赤城型",
        "url": "https://myownonpmirror.com/ships/japan/jap_cv_akagi.html",
        "reference_year": 1927,
        "role_id": "SRM_CV",
        "hull_type": "carrier",
        "slot_profile_id": "maximum_36",
        "displacement_rule": "Displacement_full maximum numeric value; aviation profile adjustment",
    },
    "jap_i15": {
        "implementation_hull_id": "ship_hull_JAP_SS_9",
        "name_english": "I-15 class (Otsu-Gata B1)",
        "name_japanese": "伊十五型（乙型一型）",
        "url": "https://myownonpmirror.com/ships/japan/jap_ss_b1.html",
        "reference_year": 1943,
        "role_id": "SRM_SC",
        "hull_type": "submarine",
        "slot_profile_id": "medium_18",
        "displacement_rule": "Displacement_normal second value is submerged displacement; full field absent",
    },
}


def numbers(value: str) -> list[float]:
    return [float(token) for token in re.findall(r"\d+(?:\.\d+)?", value)]


def required_numbers(field: str, value: str) -> list[float]:
    result = numbers(value)
    if not result:
        raise ValueError(f"{field} has no numeric value: {value!r}")
    return result


def length_oa(value: str) -> float:
    match = re.search(r"(\d+(?:\.\d+)?)\s*oa\b", value, re.IGNORECASE)
    if not match:
        raise ValueError(f"Length has no OA value: {value!r}")
    return float(match.group(1))


def normalize(key: str, spec: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    raw = payload["raw"]
    displacement_status = "confirmed"
    if key == "jap_i15":
        displacement_values = required_numbers("Displacement_normal", raw["Displacement_normal"])
        displacement_status = "derived_submerged_from_normal_field"
    else:
        displacement_values = required_numbers("Displacement_full", raw["Displacement_full"])
    displacement = max(displacement_values)
    normal_values = required_numbers("Displacement_normal", raw["Displacement_normal"])
    speeds = required_numbers("speed", raw["speed"])
    endurance = required_numbers("Endurance", raw["Endurance"])
    maximum_speed = speeds[0]
    cruising_speed = endurance[1] if len(endurance) >= 2 else maximum_speed * 0.8
    inputs = {
        "displacement_normal_t": normal_values[0],
        "displacement_full_or_submerged_t": displacement,
        "length_oa_m": length_oa(raw["Length"]),
        "breadth_m": required_numbers("Breadth", raw["Breadth"])[0],
        "maximum_speed_kn": maximum_speed,
        "cruising_speed_kn": cruising_speed,
        "endurance_nm": endurance[0],
        "power_shp_surface": required_numbers("Power", raw["Power"])[0],
    }
    computed = {
        "max_strength_unrounded": calculate_base_strength(
            displacement, inputs["length_oa_m"], inputs["breadth_m"],
            spec["hull_type"], spec["reference_year"],
        ),
        "max_organisation_unrounded": calculate_base_org(
            displacement, inputs["length_oa_m"], inputs["breadth_m"],
            spec["hull_type"], spec["reference_year"],
        ),
        "target_naval_speed_kn": target_naval_speed(maximum_speed, cruising_speed),
        "target_naval_range_km": target_naval_range(endurance[0]),
        "formula_ids": [HP_FORMULA_ID, ORG_FORMULA_ID, SPEED_FORMULA_ID, RANGE_FORMULA_ID],
    }
    digest_payload = json.dumps(
        {"prototype_key": key, "source_id": payload["source_id"], "inputs": inputs},
        ensure_ascii=False,
        sort_keys=True,
    ).encode()
    return {
        "prototype_key": key,
        "implementation_hull_id": spec["implementation_hull_id"],
        "name_english": spec["name_english"],
        "name_japanese": spec["name_japanese"],
        "reference_year": spec["reference_year"],
        "role_id": spec["role_id"],
        "hull_type": spec["hull_type"],
        "slot_profile_id": spec["slot_profile_id"],
        "normalization": {
            "displacement_rule": spec["displacement_rule"],
            "displacement_status": displacement_status,
            "length_rule": "prefer OA, then review instead of silent fallback",
            "speed_rule": "surface maximum and endurance cruise speed",
        },
        "inputs": inputs,
        "raw_historical": {
            field: raw.get(field, "")
            for field in (
                "CLASS_NAME", "TYPE", "Displacement_normal", "Displacement_full",
                "Length", "Breadth", "speed", "Endurance", "Power", "Fuel",
                "Machinery", "No_of_shafts", "Draught", "Complement", "Armament",
                "Armour", "Electronic_equipment", "sections",
            )
        },
        "computed": computed,
        "input_digest_sha256": hashlib.sha256(digest_payload).hexdigest(),
        "source": {
            "source_id": payload["source_id"],
            "source_type": "nsdb",
            "source_url_raw": payload["source_url_raw"],
            "source_url_normalized": payload["source_url_normalized"],
            "database_sha256": payload["database_sha256"],
            "review_status": "selected_by_exact_source_url",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = database_manifest(args.db)
    rows = []
    for key, spec in PROTOTYPES.items():
        payload = select_by_source_url(args.db, spec["url"])
        rows.append(normalize(key, spec, payload))
    result = {
        "status": "historical_inputs_and_ssw_hull_ids_approved",
        "database_manifest": manifest,
        "prototype_count": len(rows),
        "prototypes": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"ATRMRW Japan prototype ledger: {len(rows)} classes, db={manifest['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
