#!/usr/bin/env python3
"""日本5艦級packingの論理moduleをSSW固定commitへ照合する。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
SSW_REPO = Path("/Users/eightman/dev/hoi4/SSW_mod")
SSW_COMMIT = "4bcb07d5c11f3c78c3383db393abc9bbbf4dbdc1"
DEFAULT_PACKING = REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE3_JAPAN_SLOT_PACKING.json"
DEFAULT_OUTPUT = REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE3_JAPAN_MODULE_SOURCE_LEDGER.json"
MODULE_ROOT = "common/units/equipment/modules"


EXACT: dict[str, tuple[str, str]] = {
    "atrmrw_role_SRM_BB": ("SRM_BB", "SSW role module is directly reusable."),
    "atrmrw_role_SRM_CA": ("SRM_CA", "SSW role module is directly reusable."),
    "atrmrw_role_SRM_DD": ("SRM_DD", "SSW role module is directly reusable."),
    "atrmrw_role_SRM_CV": ("SRM_CV", "SSW role module is directly reusable."),
    "atrmrw_role_SRM_SC": ("SRM_SC", "SSW role module is directly reusable."),
    "atrmrw_power_150000_shp": ("SM_ENPOWER_JAP_150000", "The SSW module identifies the same 150,000 shp plant."),
    "atrmrw_power_130000_shp": ("SM_ENPOWER_JAP_130000", "The SSW module identifies the same 130,000 shp plant."),
    "atrmrw_armor_material_vh": ("SM_Armor_VH", "SSW defines the same VH armor material."),
    "atrmrw_armor_material_nvnc": ("SM_Armor_NVNC", "SSW defines the same NVNC armor material."),
    "atrmrw_protection_unarmored": ("SM_OT_hull_only", "SSW's unarmored hull-only material is directly reusable."),
    "atrmrw_jap_fire_control_gen0": ("ship_fire_control_system_0", "The logical generation maps one-to-one to SSW generation 0."),
    "atrmrw_jap_fire_control_gen1": ("ship_fire_control_system_1", "The logical generation maps one-to-one to SSW generation 1."),
}


def aggregate(source_id: str, historical_count: int, label: str, *, match: str = "exact_mount") -> dict[str, Any]:
    return {
        "count_unit": "mounts",
        "historical_mount_count": historical_count,
        "source_mounts": [{
            "source_module_id": source_id,
            "source_mount_count": 1,
            "represented_historical_count": historical_count,
        }],
        "source_match": match,
        "rationale": label,
    }


AGGREGATE: dict[str, dict[str, Any]] = {
    "atrmrw_jap_460mm_3x3_1942": aggregate("SM_TSHG_JAP_460_L45", 3, "Three historical triple 460 mm mounts must be recomputed as one batch."),
    "atrmrw_jap_155mm_4x3_1942": aggregate("SM_TLM_JAP_155_L60", 4, "Four historical triple 155 mm mounts must be recomputed as one batch."),
    "atrmrw_jap_127mm_6x2_1942": aggregate("SM_DAA_JAP_127_L40", 6, "Six historical twin 127 mm mounts must be recomputed as one batch."),
    "atrmrw_jap_25mm_8x3_1942": aggregate("SM_TAA_JAP_25_L60", 8, "Eight historical triple 25 mm mounts must be recomputed as one batch."),
    "atrmrw_jap_13_2mm_2x2_1942": aggregate("ship_old_anti_air_1", 2, "SSW has no Japanese 13.2 mm twin identity; the old-AA module is only a stat proxy.", match="proxy_missing_caliber_identity"),
    "atrmrw_jap_203mm_5x2_1932": aggregate("SM_DHG_JAP_203_L50", 5, "Five historical twin 203 mm mounts must be recomputed as one batch."),
    "atrmrw_jap_120mm_4x1_1932": aggregate("SM_SLG_JAP_120_L45", 4, "Four historical single 120 mm mounts must be recomputed as one batch."),
    "atrmrw_jap_610mm_tt_4x2_16reload": aggregate("SM_TP_D_T7", 4, "The SSW twin launcher is generic and lacks the Japanese 610 mm identity and reload allowance.", match="proxy_layout_only"),
    "atrmrw_jap_40mm_2x1_1932": aggregate("SM_SAA_T6_40_L65", 2, "The closest SSW single 40 mm mount is L/65, not the historical L/62 weapon.", match="proxy_caliber_only"),
    "atrmrw_jap_7_7mm_2x1_1932": aggregate("ship_old_anti_air_1", 2, "SSW has no uniquely identified Japanese 7.7 mm single mount; old-AA is only a proxy.", match="proxy_missing_caliber_identity"),
    "atrmrw_jap_127mm_1x2_forward_1932": aggregate("SM_DLG_JAP_127_L50", 1, "One forward historical twin 127 mm mount remains an explicit batch."),
    "atrmrw_jap_127mm_2x2_aft_1932": aggregate("SM_DLG_JAP_127_L50", 2, "Two aft historical twin 127 mm mounts must be recomputed as one batch."),
    "atrmrw_jap_610mm_tt_3x3_15reload": aggregate("SM_TOTP_JAP_61_T10", 3, "Three historical triple 610 mm mounts and the 15-round allowance require batch recomputation.", match="mount_exact_reload_requires_new_aggregation"),
    "atrmrw_jap_depth_charge_2dct_18": aggregate("SM_DC_D_3", 2, "Two DCT and 18 charges cannot be obtained by copying the SSW delivery-module stats linearly.", match="proxy_delivery_tier"),
    "atrmrw_jap_120mm_6x2_1927": aggregate("SM_DLG_T7_120_L45", 6, "The generic SSW twin 120 mm mount matches layout and caliber but lacks a Japanese identity.", match="generic_exact_layout"),
    "atrmrw_jap_6_5mm_22x1_1927": aggregate("ship_old_anti_air_1", 22, "SSW has no unique 6.5 mm single-mount source; old-AA is only a proxy.", match="proxy_missing_caliber_identity"),
    "atrmrw_jap_140mm_1x1_i15": aggregate("SM_SLG_JAP_140_L40", 1, "The single historical 140 mm deck gun remains a batch boundary for validator consistency."),
    "atrmrw_jap_25mm_1x2_i15": aggregate("SM_DAA_JAP_25_L60", 1, "The historical twin 25 mm mount remains a batch boundary for validator consistency."),
}

AGGREGATE["atrmrw_jap_air_group_capacity_60_1927"] = {
    "count_unit": "aircraft_capacity",
    "historical_mount_count": 60,
    "source_mounts": [
        {"source_module_id": "SM_HNG_32", "source_mount_count": 1, "represented_historical_count": 32},
        {"source_module_id": "SM_HNG_28", "source_mount_count": 1, "represented_historical_count": 28},
    ],
    "source_match": "exact_capacity_composition",
    "rationale": "Compose the two fixed SSW hangar capacities; do not scale one hangar module to 60 aircraft.",
}

AGGREGATE["atrmrw_jap_200mm_2x2_6x1_1927"] = {
    "count_unit": "mounts",
    "historical_mount_count": 8,
    "source_mounts": [
        {"source_module_id": "SM_DMed_T7_203_L50", "source_mount_count": 1, "represented_historical_count": 2},
        {"source_module_id": "SM_SMed_T7_203_L50", "source_mount_count": 1, "represented_historical_count": 6},
    ],
    "source_match": "proxy_203mm_for_200mm_mixed_layout",
    "rationale": "The fixed SSW commit has no Japanese 200/50 source; twin and single 203/50 modules preserve the mixed layout only.",
}

AGGREGATE["atrmrw_jap_533mm_bow_6_torpedo_17"] = {
    "count_unit": "tubes",
    "historical_mount_count": 6,
    "source_mounts": [
        {"source_module_id": "SM_SUB_TP_JAP_53_T10", "source_mount_count": 1, "represented_historical_count": 0},
        {"source_module_id": "SM_SUB_L_B6S0_T10", "source_mount_count": 6, "represented_historical_count": 6},
    ],
    "source_match": "weapon_type_plus_launcher_layout",
    "rationale": "The torpedo type and six-tube launcher are separate SSW modules; the 17-round allowance requires a new aggregate.",
}


UNRESOLVED: dict[str, dict[str, Any]] = {
    "atrmrw_jap_type93_sonar_hydrophone": {
        "candidate_source_module_ids": ["ship_sonar_1"],
        "unresolved_reason": "The generic SSW sonar tier cannot uniquely identify the Japanese Type 93 sonar plus hydrophone set.",
    },
}


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout


def strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        quoted = False
        escaped = False
        result = []
        for char in line:
            if char == '"' and not escaped:
                quoted = not quoted
            if char == "#" and not quoted:
                break
            result.append(char)
            escaped = char == "\\" and not escaped
            if char != "\\":
                escaped = False
        lines.append("".join(result))
    return "\n".join(lines)


def matching_brace(text: str, opening: int) -> int:
    depth = 0
    quoted = False
    escaped = False
    for index in range(opening, len(text)):
        char = text[index]
        if char == '"' and not escaped:
            quoted = not quoted
        if not quoted:
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return index
        escaped = char == "\\" and not escaped
        if char != "\\":
            escaped = False
    raise ValueError("unbalanced braces")


def direct_blocks(body: str) -> list[tuple[str, str]]:
    result = []
    index = 0
    pattern = re.compile(r"([A-Za-z_][A-Za-z0-9_.-]*)\s*=\s*\{")
    while index < len(body):
        match = pattern.match(body, index)
        if match:
            opening = match.end() - 1
            closing = matching_brace(body, opening)
            result.append((match.group(1), body[opening + 1:closing]))
            index = closing + 1
            continue
        index += 1
    return result


def direct_scalar(body: str, name: str) -> str | None:
    depth = 0
    for line in body.splitlines():
        if depth == 0:
            match = re.match(rf"\s*{re.escape(name)}\s*=\s*([A-Za-z0-9_.-]+)\s*$", line)
            if match:
                return match.group(1)
        depth += line.count("{") - line.count("}")
    return None


def stats(block: str) -> dict[str, float]:
    values: dict[str, float] = {}
    for match in re.finditer(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(-?\d+(?:\.\d+)?)", block):
        values[match.group(1)] = float(match.group(2))
    return values


def parse_modules(ssw_repo: Path, commit: str) -> tuple[dict[str, dict[str, Any]], list[str], int]:
    paths = [
        path for path in git(ssw_repo, "ls-tree", "-r", "--name-only", commit, "--", MODULE_ROOT).splitlines()
        if path.endswith(".txt")
    ]
    modules: dict[str, dict[str, Any]] = {}
    duplicates = []
    for path in paths:
        raw = git(ssw_repo, "show", f"{commit}:{path}")
        clean = strip_comments(raw)
        for container_match in re.finditer(r"\bequipment_modules\s*=\s*\{", clean):
            opening = container_match.end() - 1
            closing = matching_brace(clean, opening)
            container = clean[opening + 1:closing]
            for module_id, body in direct_blocks(container):
                blocks = defaultdict(list)
                for block_name, block_body in direct_blocks(body):
                    blocks[block_name].append(block_body)
                entry = {
                    "source_path": path,
                    "source_file_sha256": hashlib.sha256(raw.encode()).hexdigest(),
                    "parent_id": direct_scalar(body, "parent"),
                    "raw_add_stats": stats(blocks["add_stats"][-1]) if blocks["add_stats"] else {},
                    "raw_multiply_stats": stats(blocks["multiply_stats"][-1]) if blocks["multiply_stats"] else {},
                }
                if module_id in modules:
                    duplicates.append(module_id)
                modules[module_id] = entry
            break
    return modules, sorted(set(duplicates)), len(paths)


def resolve_modules(modules: dict[str, dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], list[str], list[str]]:
    resolved: dict[str, dict[str, Any]] = {}
    missing_parents: set[str] = set()
    cycles: set[str] = set()

    def resolve(module_id: str, stack: tuple[str, ...] = ()) -> dict[str, Any]:
        if module_id in resolved:
            return resolved[module_id]
        if module_id in stack:
            cycles.update((*stack, module_id))
            return {"effective_add_stats": {}, "effective_multiply_stats": {}, "parent_chain": []}
        entry = modules[module_id]
        parent_id = entry["parent_id"]
        add: dict[str, float] = {}
        multiply: dict[str, float] = {}
        chain: list[str] = []
        if parent_id:
            if parent_id not in modules:
                missing_parents.add(parent_id)
            else:
                parent = resolve(parent_id, (*stack, module_id))
                add.update(parent["effective_add_stats"])
                multiply.update(parent["effective_multiply_stats"])
                chain = [parent_id, *parent["parent_chain"]]
        add.update(entry["raw_add_stats"])
        multiply.update(entry["raw_multiply_stats"])
        result = {**entry, "parent_chain": chain, "effective_add_stats": add, "effective_multiply_stats": multiply}
        resolved[module_id] = result
        return result

    for module_id in modules:
        resolve(module_id)
    return resolved, sorted(missing_parents), sorted(cycles)


def source_ids_for(logical_id: str) -> list[str]:
    if logical_id in EXACT:
        return [EXACT[logical_id][0]]
    if logical_id in AGGREGATE:
        return list(dict.fromkeys(item["source_module_id"] for item in AGGREGATE[logical_id]["source_mounts"]))
    if logical_id in UNRESOLVED:
        return UNRESOLVED[logical_id]["candidate_source_module_ids"]
    return []


def build(packing: dict[str, Any], modules: dict[str, dict[str, Any]], duplicates: list[str], file_count: int, missing_parents: list[str], cycles: list[str]) -> dict[str, Any]:
    usages: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for prototype in packing["prototypes"]:
        for slot in prototype["slots"]:
            logical_id = slot.get("default_module_id")
            if not logical_id or logical_id == "empty":
                continue
            usage = {
                "prototype_key": prototype["prototype_key"],
                "logical_slot_id": slot["logical_slot_id"],
                "assignment_kind": slot["assignment_kind"],
            }
            if "batch_key" in slot:
                usage["batch_key"] = slot["batch_key"]
            usages[logical_id].append(usage)

    entries = []
    required_source_ids: set[str] = set()
    for logical_id, logical_usages in usages.items():
        source_ids = source_ids_for(logical_id)
        required_source_ids.update(source_ids)
        if logical_id in EXACT:
            classification = "exact"
            rationale = EXACT[logical_id][1]
            extra: dict[str, Any] = {"source_module_ids": source_ids}
        elif logical_id in AGGREGATE:
            classification = "aggregate_required"
            rationale = AGGREGATE[logical_id]["rationale"]
            extra = {
                "source_module_ids": source_ids,
                "aggregation": AGGREGATE[logical_id],
                "effective_stats_policy": "Use each source module's effective stats as an input; do not multiply or sum them into a final historical batch without the ATRMRW gun/aviation calculator.",
            }
        elif logical_id in UNRESOLVED:
            classification = "unresolved"
            rationale = UNRESOLVED[logical_id]["unresolved_reason"]
            extra = {
                "source_module_ids": source_ids,
                "unresolved_reason": rationale,
                "effective_stats_policy": "Candidate stats are recorded for audit only and are not approved for transfer.",
            }
        else:
            classification = "historical_new"
            kinds = sorted({usage["assignment_kind"] for usage in logical_usages})
            rationale = f"No identity-preserving SSW module exists for this historical {', '.join(kinds)} definition; implement a new visible module."
            extra = {
                "source_module_ids": [],
                "effective_stats_policy": "Derive new stats from the historical ledger and frozen composition calculation, not from an SSW module copy.",
            }
        entries.append({
            "logical_module_id": logical_id,
            "classification": classification,
            "rationale": rationale,
            "usages": logical_usages,
            **extra,
        })

    closure = set(required_source_ids)
    pending = list(required_source_ids)
    while pending:
        module_id = pending.pop()
        if module_id not in modules:
            continue
        parent_id = modules[module_id]["parent_id"]
        if parent_id and parent_id not in closure:
            closure.add(parent_id)
            pending.append(parent_id)
    registry = {module_id: modules[module_id] for module_id in sorted(closure) if module_id in modules}
    missing_sources = sorted(required_source_ids - set(modules))
    counts = defaultdict(int)
    for entry in entries:
        counts[entry["classification"]] += 1
    return {
        "status": "ssw_fixed_commit_source_classification_complete",
        "source_repository": str(SSW_REPO),
        "source_commit": SSW_COMMIT,
        "source_scan": {
            "module_file_count": file_count,
            "parsed_module_count": len(modules),
            "duplicate_module_ids": duplicates,
            "missing_parent_ids": missing_parents,
            "parent_cycles": cycles,
            "missing_required_source_module_ids": missing_sources,
        },
        "classification_counts": dict(sorted(counts.items())),
        "logical_module_count": len(entries),
        "logical_modules": entries,
        "source_modules": registry,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packing", type=Path, default=DEFAULT_PACKING)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--ssw-repo", type=Path, default=SSW_REPO)
    parser.add_argument("--commit", default=SSW_COMMIT)
    args = parser.parse_args()
    packing = json.loads(args.packing.read_text(encoding="utf-8"))
    raw_modules, duplicates, file_count = parse_modules(args.ssw_repo, args.commit)
    modules, missing_parents, cycles = resolve_modules(raw_modules)
    result = build(packing, modules, duplicates, file_count, missing_parents, cycles)
    result["source_repository"] = str(args.ssw_repo)
    result["source_commit"] = args.commit
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print(f"ATRMRW Japan module source ledger: {result['logical_module_count']} logical modules, {len(result['source_modules'])} SSW sources, commit={args.commit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
