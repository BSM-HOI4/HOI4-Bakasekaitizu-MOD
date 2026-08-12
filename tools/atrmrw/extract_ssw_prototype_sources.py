#!/usr/bin/env python3
"""固定SSWコミットから日本4艦級の移植元slot/default/statを抽出する。"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .inventory_atrm_slots import Block, git_revision, git_text, parse_document, scalar
except ImportError:
    from inventory_atrm_slots import Block, git_revision, git_text, parse_document, scalar


DEFAULT_COMMIT = "4bcb07d5c11f3c78c3383db393abc9bbbf4dbdc1"
SOURCES = {
    "jap_yamato": (
        "common/units/equipment/ship_hull_heavy.txt",
        "ship_hull_JAP_BB_3",
    ),
    "jap_takao": (
        "common/units/equipment/ship_hull_cruiser.txt",
        "ship_hull_JAP_CA_0",
    ),
    "jap_fubuki": (
        "common/units/equipment/ship_hull_light.txt",
        "ship_hull_JAP_DD_13",
    ),
    "jap_akagi": (
        "common/units/equipment/ship_hull_carrier.txt",
        "ship_hull_JAP_CV_0",
    ),
}
STAT_KEYS = (
    "naval_speed", "naval_range", "surface_visibility", "sub_visibility",
    "surface_detection", "sub_detection", "reliability", "max_strength",
    "max_organisation", "fuel_consumption", "build_cost_ic", "manpower",
    "naval_dominance_factor",
)


def equipment_block(text: str, equipment_id: str) -> Block:
    document = parse_document(text)
    equipments = document.first("equipments")
    if not isinstance(equipments, Block):
        raise ValueError("equipments block missing")
    matches = [a.value for a in equipments.assignments if a.key == equipment_id]
    if len(matches) != 1 or not isinstance(matches[0], Block):
        raise ValueError(f"expected one equipment block for {equipment_id}, got {len(matches)}")
    return matches[0]


def block_scalars(block: Block | str | None) -> dict[str, str]:
    if not isinstance(block, Block):
        return {}
    result = {}
    for assignment in block.assignments:
        if isinstance(assignment.value, str):
            result[assignment.key] = assignment.value
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ssw-repo", type=Path, required=True)
    parser.add_argument("--commit", default=DEFAULT_COMMIT)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    revision = git_revision(args.ssw_repo, args.commit)
    rows = []
    for prototype_key, (source_path, source_hull_id) in SOURCES.items():
        text = git_text(args.ssw_repo, revision, source_path)
        block = equipment_block(text, source_hull_id)
        slots = block.first("module_slots")
        defaults = block_scalars(block.first("default_modules"))
        slot_ids = [a.key for a in slots.assignments] if isinstance(slots, Block) else []
        missing_defaults = sorted(set(slot_ids) - set(defaults))
        extra_defaults = sorted(set(defaults) - set(slot_ids))
        rows.append({
            "prototype_key": prototype_key,
            "source_hull_id": source_hull_id,
            "source_path": source_path,
            "source_blob_sha256": hashlib.sha256(text.encode()).hexdigest(),
            "year": scalar(block, "year"),
            "archetype": scalar(block, "archetype"),
            "slot_count": len(slot_ids),
            "visible_slot_count": sum(not slot_id.startswith("hidden_") for slot_id in slot_ids),
            "hidden_slot_count": sum(slot_id.startswith("hidden_") for slot_id in slot_ids),
            "slot_ids": slot_ids,
            "default_modules": defaults,
            "missing_defaults": missing_defaults,
            "extra_defaults": extra_defaults,
            "base_stats": {key: scalar(block, key) for key in STAT_KEYS if scalar(block, key)},
        })
    payload = {
        "source_repository": str(args.ssw_repo.resolve()),
        "source_commit": revision,
        "note": "I-15/Otsu-Gata B1 has no exact hull in the fixed SSW commit",
        "prototypes": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"SSW prototype sources: {len(rows)} hulls, commit={revision}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
