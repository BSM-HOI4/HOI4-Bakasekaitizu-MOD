#!/usr/bin/env python3
"""ATRMRW Phase 1のスロット契約と全船体割当を検証する。"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

try:
    from .gui_layout import PANEL_HEIGHT, PANEL_WIDTH, SLOT_HEIGHT, SLOT_WIDTH
except ImportError:
    from gui_layout import PANEL_HEIGHT, PANEL_WIDTH, SLOT_HEIGHT, SLOT_WIDTH


ALLOWED_COUNTS = {36, 30, 24, 18, 15, 12, 9}
ALLOWED_STATES = {"editable", "fixed_visible", "locked"}
ALLOWED_ZONES = {"fixed", "front", "mid", "rear", "optional"}


def main() -> int:
    parser = argparse.ArgumentParser()
    repo = Path(__file__).resolve().parents[2]
    parser.add_argument(
        "--contract",
        type=Path,
        default=repo / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE1_SLOT_CONTRACT.json",
    )
    parser.add_argument(
        "--inventory",
        type=Path,
        default=repo / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE0_BSM_INVENTORY.json",
    )
    parser.add_argument(
        "--mapping",
        type=Path,
        default=repo / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE1_HULL_PROFILE_MAP.csv",
    )
    parser.add_argument("--resolved-csv", type=Path)
    args = parser.parse_args()

    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
    errors: list[str] = []
    profiles = contract["profiles"]
    order = contract["profile_order"]
    if contract.get("status") != "approved":
        errors.append(f"invalid contract status: {contract.get('status')!r}")
    role_contract = contract.get("role_contract", {})
    if (
        role_contract.get("physical_slot") is not True
        or role_contract.get("visible") is not True
        or role_contract.get("editable") is not True
    ):
        errors.append("role_contract must define an editable visible physical slot")
    visibility_contract = contract.get("visibility_contract", {})
    if visibility_contract.get("hidden_slots_allowed") is not False:
        errors.append("hidden slots must be prohibited")
    semantic_contract = contract.get("semantic_contract", {})
    required_semantics = set(semantic_contract.get("required_armament_slots", []))
    if len(required_semantics) != 6:
        errors.append("semantic_contract must define the six armament slots")

    if set(order) != set(profiles):
        errors.append("profile_order and profiles contain different IDs")
    totals = [profiles[name]["total_slot_count"] for name in order]
    if totals != sorted(totals, reverse=True) or len(totals) != len(set(totals)):
        errors.append(f"profile totals are not strictly descending: {totals}")
    if set(totals) != ALLOWED_COUNTS:
        errors.append(f"profile totals must be {sorted(ALLOWED_COUNTS, reverse=True)}: {totals}")

    for profile_id, profile in profiles.items():
        slots = profile["slots"]
        slot_ids = [slot["id"] for slot in slots]
        game_slot_ids = [slot.get("game_slot_id") for slot in slots]
        if len(slot_ids) != len(set(slot_ids)):
            errors.append(f"{profile_id}: duplicate slot IDs")
        if len(game_slot_ids) != len(set(game_slot_ids)) or any(
            not isinstance(slot_id, str) or not slot_id for slot_id in game_slot_ids
        ):
            errors.append(f"{profile_id}: invalid or duplicate game slot IDs")
        if len(slots) != profile["total_slot_count"]:
            errors.append(
                f"{profile_id}: total={profile['total_slot_count']} but slots={len(slots)}"
            )
        for slot in slots:
            if slot["state"] not in ALLOWED_STATES:
                errors.append(f"{profile_id}/{slot['id']}: invalid state {slot['state']}")
            if slot["zone"] not in ALLOWED_ZONES:
                errors.append(f"{profile_id}/{slot['id']}: invalid zone {slot['zone']}")
            if not slot["semantic"]:
                errors.append(f"{profile_id}/{slot['id']}: semantic is empty")
        covered_semantics = {
            semantic for slot in slots for semantic in slot.get("semantic", [])
        }
        missing_semantics = sorted(required_semantics - covered_semantics)
        # 9/12枠は同用途batchへ集約するため、6基本武装の個別物理枠を要求しない。
        if profile["total_slot_count"] >= 15 and missing_semantics:
            errors.append(
                f"{profile_id}: missing logical armament semantics {missing_semantics}"
            )
        hidden = [slot["id"] for slot in slots if slot.get("state") == "hidden" or slot["id"].startswith("hidden_")]
        if hidden:
            errors.append(f"{profile_id}: hidden slots are prohibited: {hidden}")
        if not any("role" in slot.get("semantic", []) for slot in slots):
            errors.append(f"{profile_id}: visible role slot is missing")
        if not any("hull_structure" in slot.get("semantic", []) for slot in slots):
            errors.append(f"{profile_id}: visible hull structure slot is missing")
        role_slots = [slot for slot in slots if "role" in slot.get("semantic", [])]
        if len(role_slots) != 1 or role_slots[0].get("state") != "editable":
            errors.append(f"{profile_id}: role must be exactly one editable slot")
        structure_slots = [slot for slot in slots if "hull_structure" in slot.get("semantic", [])]
        fixed_slots = [slot for slot in slots if slot.get("state") == "fixed_visible"]
        if len(structure_slots) != 1 or structure_slots[0].get("state") != "fixed_visible":
            errors.append(f"{profile_id}: hull structure must be exactly one fixed_visible slot")
        if fixed_slots != structure_slots:
            errors.append(f"{profile_id}: only hull structure may be fixed_visible")
        engineering_semantics = {
            semantic
            for slot in slots
            if str(slot.get("id", "")).startswith("engineering_slot_")
            for semantic in slot.get("semantic", [])
        }
        required_engineering = {
            "propulsion_type", "propulsion_power", "fuel_energy", "fuel_endurance",
        }
        if engineering_semantics != required_engineering:
            errors.append(f"{profile_id}: engineering/fuel semantics mismatch")
        for group, maximum in (("fixed", 18), ("custom", 18)):
            group_slots = [slot for slot in slots if slot.get("ui_group") == group]
            indices = [slot.get("ui_index") for slot in group_slots]
            if indices != list(range(len(group_slots))):
                errors.append(f"{profile_id}: {group} UI indices are not contiguous: {indices}")
            if len(group_slots) > maximum:
                errors.append(f"{profile_id}: {group} UI count exceeds {maximum}")
        unknown_ui_groups = sorted({slot.get("ui_group") for slot in slots} - {"fixed", "custom"})
        if unknown_ui_groups:
            errors.append(f"{profile_id}: invalid UI groups {unknown_ui_groups}")
        for slot in slots:
            game_slot_id = str(slot.get("game_slot_id", ""))
            if slot.get("ui_group") == "fixed" and not game_slot_id.startswith("fixed_atrmrw_"):
                errors.append(f"{profile_id}/{slot['id']}: fixed game slot ID naming mismatch")
            if (
                slot.get("ui_group") == "custom"
                and game_slot_id != "ship_type_slot"
                and not game_slot_id.endswith("_custom_slot")
            ):
                errors.append(f"{profile_id}/{slot['id']}: custom game slot ID naming mismatch")
        role_slot = role_slots[0]
        if (
            role_slot.get("ui_group") != "custom"
            or role_slot.get("ui_index") != 0
            or role_slot.get("game_slot_id") != "ship_type_slot"
        ):
            errors.append(f"{profile_id}: role must be SSW-compatible ship_type_slot at custom 0")
        if any(slot.get("profile_min") != profile["total_slot_count"] for slot in slots):
            errors.append(f"{profile_id}: profile_min mismatch")
        coordinates = [(slot.get("x"), slot.get("y")) for slot in slots]
        if len(coordinates) != len(set(coordinates)):
            errors.append(f"{profile_id}: duplicate GUI coordinates")
        for slot, (x, y) in zip(slots, coordinates):
            if not isinstance(x, int) or not isinstance(y, int):
                errors.append(f"{profile_id}/{slot['id']}: GUI coordinates must be integers")
                continue
            if x < 0 or y < 0 or x + SLOT_WIDTH > PANEL_WIDTH + 2 or y + SLOT_HEIGHT > PANEL_HEIGHT:
                errors.append(f"{profile_id}/{slot['id']}: GUI coordinate is outside panel")
            if slot.get("coordinate_status") != "verified_static_HOI4_1.19.2_baseline":
                errors.append(f"{profile_id}/{slot['id']}: GUI coordinate status is not verified")

    with args.mapping.open(encoding="utf-8", newline="") as handle:
        mapping_rows = list(csv.DictReader(handle))
    mapping_by_hull = {row["hull_id"]: row for row in mapping_rows}
    if len(mapping_by_hull) != len(mapping_rows):
        errors.append("mapping contains duplicate hull IDs")
    resolved: list[dict[str, object]] = []
    known_hulls: set[str] = set()
    for source_path, hulls in inventory["hulls"]["by_file"].items():
        for hull_id in hulls:
            known_hulls.add(hull_id)
            mapping = mapping_by_hull.get(hull_id)
            if mapping is None:
                errors.append(f"{hull_id}: missing mapping row")
                continue
            if mapping["source_path"] != source_path:
                errors.append(f"{hull_id}: mapping source path mismatch")
            profile_id = mapping["profile_id"]
            if profile_id not in profiles:
                errors.append(f"{hull_id}: unresolved or unknown profile {profile_id!r}")
                continue
            profile = profiles[profile_id]
            states = Counter(slot["state"] for slot in profile["slots"])
            resolved.append(
                {
                    "hull_id": hull_id,
                    "source_path": source_path,
                    "profile_id": profile_id,
                    "total_slot_count": profile["total_slot_count"],
                    "editable_slot_count": states["editable"],
                    "fixed_visible_slot_count": states["fixed_visible"],
                    "hidden_slot_count": 0,
                    "locked_visible_slot_count": states["locked"],
                }
            )
            row = resolved[-1]
            state_total = sum(
                int(row[key])
                for key in (
                    "editable_slot_count",
                    "fixed_visible_slot_count",
                    "hidden_slot_count",
                    "locked_visible_slot_count",
                )
            )
            if state_total != row["total_slot_count"]:
                errors.append(
                    f"{hull_id}: slot-state ledger sums to {state_total}, "
                    f"expected {row['total_slot_count']}"
                )
            if int(mapping["total_slot_count"]) != profile["total_slot_count"]:
                errors.append(f"{hull_id}: mapping total does not match profile")
            if int(mapping["hidden_slot_count"]) != 0:
                errors.append(f"{hull_id}: mapping hidden_slot_count must be zero")
    unknown_mappings = sorted(set(mapping_by_hull) - known_hulls)
    if unknown_mappings:
        errors.append(f"mapping references unknown hulls: {unknown_mappings}")
    if len(resolved) != inventory["hulls"]["count"]:
        errors.append(
            f"resolved {len(resolved)} hulls, inventory has {inventory['hulls']['count']}"
        )
    assigned_profiles = {str(row["profile_id"]) for row in resolved}
    unused_profiles = sorted(set(profiles) - assigned_profiles)
    if unused_profiles:
        errors.append(f"profiles have no assigned hulls: {unused_profiles}")

    if args.resolved_csv and not errors:
        args.resolved_csv.parent.mkdir(parents=True, exist_ok=True)
        with args.resolved_csv.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(resolved[0]))
            writer.writeheader()
            writer.writerows(sorted(resolved, key=lambda row: str(row["hull_id"])))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"ATRMRW slot contract FAILED: {len(errors)} error(s)")
        return 1
    print(
        f"ATRMRW slot contract PASSED: {len(profiles)} profiles, "
        f"{len(resolved)} hulls, status={contract['status']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
