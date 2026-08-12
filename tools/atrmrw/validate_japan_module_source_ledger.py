#!/usr/bin/env python3
"""日本5艦級module source ledgerのpacking・継承整合を検証する。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
COMMIT = "4bcb07d5c11f3c78c3383db393abc9bbbf4dbdc1"
ALLOWED = {"exact", "aggregate_required", "historical_new", "unresolved"}


def merge(parent: dict[str, float], child: dict[str, float]) -> dict[str, float]:
    result = dict(parent)
    result.update(child)
    return result


def validate(ledger: dict[str, Any], packing: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    scan = ledger.get("source_scan", {})
    if ledger.get("source_commit") != COMMIT:
        errors.append("unexpected SSW source commit")
    for field in ("duplicate_module_ids", "missing_parent_ids", "parent_cycles", "missing_required_source_module_ids"):
        if scan.get(field):
            errors.append(f"source scan {field} is not empty: {scan[field]}")

    expected_usages: dict[str, list[tuple[str, str, str, str | None]]] = {}
    for prototype in packing.get("prototypes", []):
        for slot in prototype.get("slots", []):
            logical_id = slot.get("default_module_id")
            if not logical_id or logical_id == "empty":
                continue
            expected_usages.setdefault(logical_id, []).append((
                prototype["prototype_key"], slot["logical_slot_id"],
                slot["assignment_kind"], slot.get("batch_key"),
            ))
    rows = ledger.get("logical_modules", [])
    logical_ids = [row.get("logical_module_id") for row in rows]
    if len(logical_ids) != len(set(logical_ids)):
        errors.append("duplicate logical_module_id")
    if set(logical_ids) != set(expected_usages):
        errors.append("occupied packing module set mismatch")
    if ledger.get("logical_module_count") != len(rows):
        errors.append("logical_module_count mismatch")

    registry = ledger.get("source_modules", {})
    for source_id, source in registry.items():
        parent_id = source.get("parent_id")
        chain = source.get("parent_chain", [])
        if parent_id:
            if parent_id not in registry:
                errors.append(f"{source_id}: parent {parent_id} missing from source registry")
                continue
            if not chain or chain[0] != parent_id or source_id in chain or len(chain) != len(set(chain)):
                errors.append(f"{source_id}: invalid parent_chain")
            parent = registry[parent_id]
            expected_add = merge(parent.get("effective_add_stats", {}), source.get("raw_add_stats", {}))
            expected_multiply = merge(parent.get("effective_multiply_stats", {}), source.get("raw_multiply_stats", {}))
        else:
            if chain:
                errors.append(f"{source_id}: root module has a parent_chain")
            expected_add = source.get("raw_add_stats", {})
            expected_multiply = source.get("raw_multiply_stats", {})
        if source.get("effective_add_stats") != expected_add or source.get("effective_multiply_stats") != expected_multiply:
            errors.append(f"{source_id}: effective stats do not match resolved parent inheritance")
        if not source.get("source_path") or not source.get("source_file_sha256"):
            errors.append(f"{source_id}: source path/hash missing")

    counts = {name: 0 for name in ALLOWED}
    for row in rows:
        logical_id = row.get("logical_module_id")
        classification = row.get("classification")
        if classification not in ALLOWED:
            errors.append(f"{logical_id}: invalid classification {classification}")
            continue
        counts[classification] += 1
        actual_usages = sorted((
            usage.get("prototype_key"), usage.get("logical_slot_id"),
            usage.get("assignment_kind"), usage.get("batch_key"),
        ) for usage in row.get("usages", []))
        if actual_usages != sorted(expected_usages.get(logical_id, [])):
            errors.append(f"{logical_id}: usage list mismatch")
        source_ids = row.get("source_module_ids")
        if not isinstance(source_ids, list) or len(source_ids) != len(set(source_ids)):
            errors.append(f"{logical_id}: duplicate or missing source_module_ids list")
            continue
        for source_id in source_ids:
            if source_id not in registry:
                errors.append(f"{logical_id}: source module {source_id} missing from registry")
        batch_kinds = {usage[2] for usage in expected_usages.get(logical_id, [])}
        if batch_kinds & {"weapon_batch", "aviation_batch"} and classification != "aggregate_required":
            errors.append(f"{logical_id}: historical weapon/aviation batch must be aggregate_required")
        if classification == "exact" and len(source_ids) != 1:
            errors.append(f"{logical_id}: exact classification requires one source module")
        elif classification == "historical_new" and source_ids:
            errors.append(f"{logical_id}: historical_new may not copy an SSW module")
        elif classification == "aggregate_required":
            aggregation = row.get("aggregation", {})
            mounts = aggregation.get("source_mounts", [])
            if not source_ids or not mounts or not isinstance(aggregation.get("historical_mount_count"), int) or aggregation["historical_mount_count"] <= 0:
                errors.append(f"{logical_id}: aggregate requires sources and positive historical_mount_count")
            mount_source_ids = {mount.get("source_module_id") for mount in mounts}
            if mount_source_ids != set(source_ids):
                errors.append(f"{logical_id}: aggregate source_mounts do not match source_module_ids")
            for mount in mounts:
                if not isinstance(mount.get("source_mount_count"), int) or mount["source_mount_count"] <= 0:
                    errors.append(f"{logical_id}: source_mount_count must be positive")
            if "do not" not in row.get("effective_stats_policy", "").lower():
                errors.append(f"{logical_id}: aggregate must prohibit naive stat scaling")
        elif classification == "unresolved" and not row.get("unresolved_reason"):
            errors.append(f"{logical_id}: unresolved classification needs a reason")

    expected_counts = {name: value for name, value in counts.items() if value}
    if ledger.get("classification_counts") != dict(sorted(expected_counts.items())):
        errors.append("classification_counts mismatch")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE3_JAPAN_MODULE_SOURCE_LEDGER.json")
    parser.add_argument("--packing", type=Path, default=REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE3_JAPAN_SLOT_PACKING.json")
    args = parser.parse_args()
    ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    packing = json.loads(args.packing.read_text(encoding="utf-8"))
    errors = validate(ledger, packing)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"ATRMRW Japan module source ledger FAILED: {len(errors)} error(s)")
        return 1
    print(f"ATRMRW Japan module source ledger PASSED: {ledger['logical_module_count']} logical modules, classes={ledger['classification_counts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
