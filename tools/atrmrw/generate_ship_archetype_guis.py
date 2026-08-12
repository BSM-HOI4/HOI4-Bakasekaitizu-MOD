#!/usr/bin/env python3
"""HOI4 1.19.2の艦種GUIへATRMRW可視slot containerを決定論的に追加する。"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
VANILLA_DIR = Path(
    "/Users/eightman/Library/Application Support/Steam/steamapps/common/"
    "Hearts of Iron IV/interface/equipmentdesigner/ships"
)
OUTPUT_DIR = REPO / "bakasekai/interface/equipmentdesigner/ships"
CONTRACT_PATH = REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE1_SLOT_CONTRACT.json"

BASELINE_SHA256 = {
    "ship_hull_heavy.gui": "36cdefb8528805fcf208f885bea5ef10765057c8deee8ac2381821612fc46414",
    "ship_hull_cruiser.gui": "e7feca58fe7eeeadb17905f5d67f08ccde2cb55bf047b856a28d641a49670855",
    "ship_hull_light.gui": "0c263d5cc17b7112725bcccb722911ee70f0c477487f7f5de83ace332c3fac3a",
    "ship_hull_carrier.gui": "3cca95dc113270e95cc548a4c7243d7ac2068bc5ee4cfdef46fee78b72493b63",
    "ship_hull_submarine.gui": "73544d44cfd4d98f5ee0705be45a43cc4ffd71d6dcec86dfe19bccc22525bd79",
}

MODULE_SLOTS_MARKER = (
    '\t\tcontainerWindowType = {\n'
    '\t\t\tname = "module_slots"\n'
    '\t\t\tposition = { x=0 y=0 }\n'
    '\t\t\tsize = { width=100% height=100% }\n'
)


def slot_container(game_slot_id: str) -> str:
    return (
        "\n\t\t\t# ATRMRW visible physical slot\n"
        "\t\t\tcontainerWindowType = {\n"
        f'\t\t\t\tname = "{game_slot_id}"\n'
        "\t\t\t\tposition = { x=0 y=0 }\n"
        "\t\t\t\tsize = { width=100% height=100% }\n"
        "\t\t\t}\n"
    )


def maximum_slot_ids(contract: dict[str, object]) -> list[str]:
    slots = contract["profiles"]["maximum_36"]["slots"]
    return [str(slot["game_slot_id"]) for slot in slots]


def generate(source_text: str, game_slot_ids: list[str]) -> str:
    if source_text.count(MODULE_SLOTS_MARKER) != 1:
        raise ValueError("vanilla module_slots marker must occur exactly once")
    if len(game_slot_ids) != 36 or len(set(game_slot_ids)) != 36:
        raise ValueError("maximum profile must expose exactly 36 unique game slot IDs")
    additions = "\n\t\t\t# ATRMRW: SSW-compatible order; group indices follow slot ID prefixes.\n"
    additions += "".join(slot_container(slot_id) for slot_id in game_slot_ids)
    return source_text.replace(MODULE_SLOTS_MARKER, MODULE_SLOTS_MARKER + additions, 1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, default=VANILLA_DIR)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--contract", type=Path, default=CONTRACT_PATH)
    args = parser.parse_args()

    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    game_slot_ids = maximum_slot_ids(contract)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for filename, expected_digest in BASELINE_SHA256.items():
        source = args.source_dir / filename
        source_bytes = source.read_bytes()
        digest = hashlib.sha256(source_bytes).hexdigest()
        if digest != expected_digest:
            raise ValueError(f"unexpected HOI4 GUI baseline for {filename}: {digest}")
        output = generate(source_bytes.decode("ascii"), game_slot_ids)
        (args.output_dir / filename).write_text(output, encoding="ascii", newline="")
        print(f"ATRMRW ship GUI generated: {filename}, baseline={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
