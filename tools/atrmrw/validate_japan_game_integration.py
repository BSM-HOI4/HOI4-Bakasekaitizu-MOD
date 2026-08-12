#!/usr/bin/env python3
"""生成済みATRMRW日本5艦級の船体/module/variant/OOB接続を検証する。"""

from __future__ import annotations

import json
import re
from pathlib import Path

from tools.atrmrw.generate_japan_game_files import (
    CONTRACT,
    HULL_OUTPUT,
    LOC_EN_OUTPUT,
    LOC_JA_OUTPUT,
    MODULE_LEDGER,
    MODULE_OUTPUT,
    PACKING,
    PROTOTYPES,
    TECH_OUTPUT,
    VARIANT_OUTPUT,
)
from tools.atrmrw.migrate_japan_oob import MIGRATIONS, OOB


def extract_block(text: str, block_id: str) -> str:
    match = re.search(rf"(?m)^\s*{re.escape(block_id)}\s*=\s*\{{", text)
    if not match:
        raise ValueError(f"missing block: {block_id}")
    depth = 0
    for index in range(match.end() - 1, len(text)):
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[match.start():index + 1]
    raise ValueError(f"unclosed block: {block_id}")


def assignments(block: str) -> dict[str, str]:
    return {
        key: value
        for key, value in re.findall(r"(?m)^\s+([A-Za-z0-9_]+)\s*=\s*([A-Za-z0-9_]+)\s*$", block)
    }


def validate() -> list[str]:
    errors: list[str] = []
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    packing = json.loads(PACKING.read_text(encoding="utf-8"))
    prototypes = json.loads(PROTOTYPES.read_text(encoding="utf-8"))
    module_ledger = json.loads(MODULE_LEDGER.read_text(encoding="utf-8"))
    hull_text = HULL_OUTPUT.read_text(encoding="utf-8")
    module_text = MODULE_OUTPUT.read_text(encoding="utf-8")
    variant_text = VARIANT_OUTPUT.read_text(encoding="utf-8")
    tech_text = TECH_OUTPUT.read_text(encoding="utf-8")
    prototype_by_key = {row["prototype_key"]: row for row in prototypes["prototypes"]}
    known_modules = {row["module_id"] for row in module_ledger["modules"]} | {"atrmrw_locked_visible", "empty"}

    for path, text in ((HULL_OUTPUT, hull_text), (MODULE_OUTPUT, module_text), (VARIANT_OUTPUT, variant_text), (TECH_OUTPUT, tech_text)):
        if text.count("{") != text.count("}"):
            errors.append(f"brace imbalance: {path}")
        if "hidden_" in text:
            errors.append(f"hidden slot leaked into generated game file: {path}")

    for packed in packing["prototypes"]:
        prototype = prototype_by_key[packed["prototype_key"]]
        hull_id = prototype["implementation_hull_id"]
        profile = contract["profiles"][prototype["slot_profile_id"]]
        game_ids = {slot["id"]: slot["game_slot_id"] for slot in profile["slots"]}
        try:
            hull_block = extract_block(hull_text, hull_id)
        except ValueError as error:
            errors.append(str(error))
            continue
        for slot in profile["slots"]:
            if len(re.findall(rf"(?m)^\s+{re.escape(slot['game_slot_id'])}\s*=", hull_block)) != 2:
                errors.append(f"{hull_id}/{slot['game_slot_id']}: must be declared and defaulted exactly once")
        if len(profile["slots"]) != profile["total_slot_count"]:
            errors.append(f"{hull_id}: profile total mismatch")
        try:
            defaults = assignments(extract_block(hull_block, "default_modules"))
            variant_block = next(
                block for block in re.findall(r"create_equipment_variant\s*=\s*\{.*?\n\s*\}", variant_text, re.S)
                if f"type = {hull_id}" in block
            )
        except (ValueError, StopIteration):
            errors.append(f"{hull_id}: missing defaults or variant")
            continue
        for slot in packed["slots"]:
            expected = slot.get("default_module_id")
            if expected is None:
                expected = "atrmrw_locked_visible" if slot["state"] == "locked" else "empty"
            game_slot_id = game_ids[slot["logical_slot_id"]]
            if defaults.get(game_slot_id) != expected:
                errors.append(f"{hull_id}/{game_slot_id}: hull default mismatch")
            if expected not in known_modules:
                errors.append(f"{hull_id}/{game_slot_id}: undefined module {expected}")
            if f"{game_slot_id} = {expected}" not in variant_block:
                errors.append(f"{hull_id}/{game_slot_id}: variant default mismatch")
        if hull_id not in tech_text:
            errors.append(f"{hull_id}: not enabled by ATRMRW technology")

    for module_id in known_modules - {"empty"}:
        if module_text.count(f"  {module_id} = {{") != 1:
            errors.append(f"module definition count mismatch: {module_id}")
        if module_id not in tech_text:
            errors.append(f"module not enabled by ATRMRW technology: {module_id}")

    oob_text = OOB.read_text(encoding="utf-8")
    for old, (new, expected) in MIGRATIONS.items():
        if oob_text.count(old) != 0 or oob_text.count(new) != expected:
            errors.append(f"OOB migration mismatch: {new}")

    for path, language in ((LOC_EN_OUTPUT, "english"), (LOC_JA_OUTPUT, "japanese")):
        raw = path.read_bytes()
        if not raw.startswith(b"\xef\xbb\xbf"):
            errors.append(f"localisation BOM missing: {path}")
        text = raw.decode("utf-8-sig")
        if not text.startswith(f"l_{language}:\n"):
            errors.append(f"localisation header mismatch: {path}")
        for prototype in prototypes["prototypes"]:
            if f" {prototype['implementation_hull_id']}:0 " not in text:
                errors.append(f"localisation hull key missing: {prototype['implementation_hull_id']}/{language}")
    return errors


def main() -> int:
    errors = validate()
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"ATRMRW Japan game integration FAILED: {len(errors)} error(s)")
        return 1
    print("ATRMRW Japan game integration PASSED: 5 hulls, 59 modules, 5 variants, OOB=28")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
