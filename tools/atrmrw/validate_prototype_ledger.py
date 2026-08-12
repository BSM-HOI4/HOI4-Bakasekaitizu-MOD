#!/usr/bin/env python3
"""Phase 3日本5艦級入力台帳の再現性・契約整合を検証する。"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .calculations import (
        calculate_base_org,
        calculate_base_strength,
        target_naval_range,
        target_naval_speed,
    )
except ImportError:
    from calculations import (
        calculate_base_org,
        calculate_base_strength,
        target_naval_range,
        target_naval_speed,
    )


EXPECTED_KEYS = {"jap_yamato", "jap_takao", "jap_fubuki", "jap_akagi", "jap_i15"}
EXPECTED_DB_HASH = "6d5418efa26f8c73afb386b8eb3f0dea47cf65fa03303d3c0f8c17e52122f1ad"
EXPECTED_HULL_IDS = {
    "jap_yamato": "ship_hull_JAP_BB_3",
    "jap_takao": "ship_hull_JAP_CA_0",
    "jap_fubuki": "ship_hull_JAP_DD_13",
    "jap_akagi": "ship_hull_JAP_CV_0",
    "jap_i15": "ship_hull_JAP_SS_9",
}


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ledger",
        type=Path,
        default=repo / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE3_JAPAN_PROTOTYPE_LEDGER.json",
    )
    parser.add_argument(
        "--contract",
        type=Path,
        default=repo / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE1_SLOT_CONTRACT.json",
    )
    args = parser.parse_args()
    ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    errors: list[str] = []

    rows = ledger.get("prototypes", [])
    keys = [row.get("prototype_key") for row in rows]
    if len(keys) != len(set(keys)):
        errors.append("duplicate prototype_key")
    if set(keys) != EXPECTED_KEYS:
        errors.append(f"prototype set mismatch: {sorted(keys)}")
    if ledger.get("prototype_count") != len(rows):
        errors.append("prototype_count mismatch")
    if ledger.get("database_manifest", {}).get("sha256") != EXPECTED_DB_HASH:
        errors.append("unexpected NSDB hash")

    profiles = contract["profiles"]
    role_ids = set(json.loads(
        (repo / "documents/00_coding_contexts/atrmrw/ATRMRW_SSW_ROLE_AND_ARCHETYPE_INVENTORY.json")
        .read_text(encoding="utf-8")
    )["role_ids"])
    for row in rows:
        key = row["prototype_key"]
        if row.get("implementation_hull_id") != EXPECTED_HULL_IDS[key]:
            errors.append(f"{key}: implementation hull ID mismatch")
        profile_id = row.get("slot_profile_id")
        if profile_id not in profiles:
            errors.append(f"{key}: unknown slot profile {profile_id}")
        if row.get("role_id") not in role_ids:
            errors.append(f"{key}: role is not in fixed SSW taxonomy")
        source = row.get("source", {})
        if source.get("database_sha256") != EXPECTED_DB_HASH:
            errors.append(f"{key}: source DB hash mismatch")
        if source.get("review_status") != "selected_by_exact_source_url":
            errors.append(f"{key}: source URL was not selected exactly")
        inputs = row.get("inputs", {})
        digest_payload = json.dumps(
            {"prototype_key": key, "source_id": source.get("source_id"), "inputs": inputs},
            ensure_ascii=False,
            sort_keys=True,
        ).encode()
        digest = hashlib.sha256(digest_payload).hexdigest()
        if digest != row.get("input_digest_sha256"):
            errors.append(f"{key}: input digest mismatch")
        computed = row.get("computed", {})
        expected = {
            "max_strength_unrounded": calculate_base_strength(
                inputs["displacement_full_or_submerged_t"], inputs["length_oa_m"],
                inputs["breadth_m"], row["hull_type"], row["reference_year"],
            ),
            "max_organisation_unrounded": calculate_base_org(
                inputs["displacement_full_or_submerged_t"], inputs["length_oa_m"],
                inputs["breadth_m"], row["hull_type"], row["reference_year"],
            ),
            "target_naval_speed_kn": target_naval_speed(
                inputs["maximum_speed_kn"], inputs["cruising_speed_kn"],
            ),
            "target_naval_range_km": target_naval_range(inputs["endurance_nm"]),
        }
        for name, value in expected.items():
            if abs(value - computed.get(name, float("inf"))) > 1e-9:
                errors.append(f"{key}: recomputed {name} mismatch")
        values = [*inputs.values(), *(
            value for name, value in row.get("computed", {}).items()
            if name.endswith("_unrounded") or name.startswith("target_")
        )]
        if any(not isinstance(value, (int, float)) or value <= 0 for value in values):
            errors.append(f"{key}: numeric input/output must be positive")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"ATRMRW prototype ledger FAILED: {len(errors)} error(s)")
        return 1
    print(f"ATRMRW prototype ledger PASSED: {len(rows)} classes, DB={EXPECTED_DB_HASH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
