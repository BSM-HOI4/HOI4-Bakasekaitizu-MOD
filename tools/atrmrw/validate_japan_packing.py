#!/usr/bin/env python3
"""Phase 3日本5艦級packingの全可視スロット契約を検証する。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
EXPECTED_KEYS = {"jap_yamato", "jap_takao", "jap_fubuki", "jap_akagi", "jap_i15"}
ALLOWED_STATES = {"editable", "fixed_visible", "locked_visible"}
HISTORICAL_BATCH_KINDS = {"weapon_batch", "aviation_batch"}


def contains_hidden(value: Any) -> bool:
    if isinstance(value, dict):
        return any(str(key).lower() == "hidden" or contains_hidden(item) for key, item in value.items())
    if isinstance(value, list):
        return any(contains_hidden(item) for item in value)
    return isinstance(value, str) and "hidden" in value.lower()


def validate(packing: dict[str, Any], contract: dict[str, Any], ledger: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    rows = packing.get("prototypes", [])
    ledger_rows = {row["prototype_key"]: row for row in ledger.get("prototypes", [])}
    keys = [row.get("prototype_key") for row in rows]
    if len(keys) != len(set(keys)):
        errors.append("duplicate prototype_key")
    if set(keys) != EXPECTED_KEYS:
        errors.append(f"prototype set mismatch: {sorted(keys)}")
    if packing.get("prototype_count") != len(rows):
        errors.append("prototype_count mismatch")
    if packing.get("policy", {}).get("hidden_slot_count") != 0:
        errors.append("hidden_slot_count must be zero")
    if contains_hidden(rows):
        errors.append("hidden slots or states are prohibited")

    for row in rows:
        key = row.get("prototype_key")
        ledger_row = ledger_rows.get(key)
        if ledger_row is None:
            continue
        for field in ("implementation_hull_id", "slot_profile_id", "role_id"):
            if row.get(field) != ledger_row.get(field):
                errors.append(f"{key}: {field} differs from prototype ledger")
        profile_id = row.get("slot_profile_id")
        profile = contract.get("profiles", {}).get(profile_id)
        if profile is None:
            errors.append(f"{key}: unknown slot profile {profile_id}")
            continue
        contract_slots = {slot["id"]: slot for slot in profile["slots"]}
        slots = row.get("slots", [])
        slot_ids = [slot.get("logical_slot_id") for slot in slots]
        if len(slot_ids) != len(set(slot_ids)):
            errors.append(f"{key}: duplicate logical slot assignment")
        if set(slot_ids) != set(contract_slots):
            missing = sorted(set(contract_slots) - set(slot_ids))
            extra = sorted(set(slot_ids) - set(contract_slots))
            errors.append(f"{key}: logical slot IDs mismatch; missing={missing}, extra={extra}")
        if len(slots) != profile["total_slot_count"] or row.get("slot_count") != len(slots):
            errors.append(f"{key}: total slot count mismatch")

        fixed_structures = []
        batch_keys = []
        for slot in slots:
            slot_id = slot.get("logical_slot_id")
            state = slot.get("state")
            kind = slot.get("assignment_kind")
            default_present = "default_module_id" in slot
            default = slot.get("default_module_id")
            source = slot.get("source")
            if state not in ALLOWED_STATES:
                errors.append(f"{key}/{slot_id}: invalid state {state}")
            if not default_present:
                errors.append(f"{key}/{slot_id}: default_module_id key is required")
            if not isinstance(source, dict) or not source.get("source_type") or not source.get("source_ref") or not source.get("evidence"):
                errors.append(f"{key}/{slot_id}: complete source provenance is required")
            if state == "fixed_visible":
                if kind != "hull_structure":
                    errors.append(f"{key}/{slot_id}: only hull_structure may be fixed_visible")
                fixed_structures.append(slot)
            if kind == "hull_structure":
                semantic = contract_slots.get(slot_id, {}).get("semantic", [])
                if state != "fixed_visible" or "hull_structure" not in semantic or not default:
                    errors.append(f"{key}/{slot_id}: hull_structure must be a populated fixed singleton in its contract slot")
            if kind == "role":
                if state != "editable":
                    errors.append(f"{key}/{slot_id}: role must be editable")
                if default != f"atrmrw_role_{row.get('role_id')}":
                    errors.append(f"{key}/{slot_id}: role default does not match role_id")
            if kind in HISTORICAL_BATCH_KINDS:
                if state != "editable" or not default or not slot.get("batch_key"):
                    errors.append(f"{key}/{slot_id}: historical batch must be populated, editable and batch-keyed")
                else:
                    batch_keys.append(slot["batch_key"])
            if slot_id in contract_slots and "historical_overflow" in contract_slots[slot_id].get("semantic", []) and kind != "unused" and state != "editable":
                errors.append(f"{key}/{slot_id}: occupied historical overflow must be editable")
            if kind == "unused":
                if state != "locked_visible" or default is not None or not slot.get("unused_reason"):
                    errors.append(f"{key}/{slot_id}: unused slot must be empty locked_visible with unused_reason")
            elif default is None:
                if state != "editable" or not slot.get("unresolved_reason"):
                    errors.append(f"{key}/{slot_id}: unresolved editable slot needs unresolved_reason")
            elif state == "locked_visible":
                errors.append(f"{key}/{slot_id}: populated slot may not be locked_visible")
        if len(fixed_structures) != 1:
            errors.append(f"{key}: expected exactly one fixed_visible hull_structure, got {len(fixed_structures)}")
        role_slots = [slot for slot in slots if slot.get("assignment_kind") == "role"]
        if len(role_slots) != 1 or role_slots[0].get("logical_slot_id") != "role_slot":
            errors.append(f"{key}: expected exactly one role assignment in role_slot")
        if len(batch_keys) != len(set(batch_keys)):
            errors.append(f"{key}: duplicate historical batch_key")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packing", type=Path, default=REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE3_JAPAN_SLOT_PACKING.json")
    parser.add_argument("--contract", type=Path, default=REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE1_SLOT_CONTRACT.json")
    parser.add_argument("--ledger", type=Path, default=REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE3_JAPAN_PROTOTYPE_LEDGER.json")
    args = parser.parse_args()
    packing = json.loads(args.packing.read_text(encoding="utf-8"))
    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    errors = validate(packing, contract, ledger)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"ATRMRW Japan slot packing FAILED: {len(errors)} error(s)")
        return 1
    count = sum(row["slot_count"] for row in packing["prototypes"])
    print(f"ATRMRW Japan slot packing PASSED: {len(packing['prototypes'])} classes, {count} visible slots, hidden=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
