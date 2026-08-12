#!/usr/bin/env python3
"""HOI4 1.19.2 vanilla GUIへATRMRW用anchorだけを決定論的に追加する。"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

try:
    from .gui_layout import CUSTOM_COORDINATES, FIXED_COORDINATES
except ImportError:
    from gui_layout import CUSTOM_COORDINATES, FIXED_COORDINATES


VANILLA_SHA256 = "c1a6cf7c0b74f9f428cf5d50c3f422c5f675b38adbcef9c8c1e13070fa9dbc22"
DEFAULT_SOURCE = Path(
    "/Users/eightman/Library/Application Support/Steam/steamapps/common/"
    "Hearts of Iron IV/interface/equipmentdesignerview.gui"
)


def anchor_block(group: str, index: int, x: int, y: int) -> str:
    return (
        "\n\t\t\tpositionType = {\n"
        f"\t\t\t\tname = \"pos_{group}_module_slot_window_{index}\"\n"
        f"\t\t\t\tposition = {{ x={x} y={y} }}\n"
        "\t\t\t}\n"
    )


def generate(source_text: str) -> str:
    marker = (
        "\t\t\tpositionType = {\n"
        "\t\t\t\tname = \"pos_fixed_module_slot_window_6\"\n"
        "\t\t\t\tposition = { x=@fixed_btn_mod_col_6 y=@fixed_btn_mod_row }\n"
        "\t\t\t}\n"
    )
    if source_text.count(marker) != 1:
        raise ValueError("vanilla fixed slot 6 marker must occur exactly once")
    additions = "\n\t\t\t# ATRMRW: 1.19.2 vanilla anchors 0..6 are preserved above.\n"
    for index in range(7, 18):
        additions += anchor_block("custom", index, *CUSTOM_COORDINATES[index])
    for index in range(7, 18):
        additions += anchor_block("fixed", index, *FIXED_COORDINATES[index])
    return source_text.replace(marker, marker + additions, 1)


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument(
        "--output", type=Path,
        default=repo / "bakasekai/interface/replace/equipmentdesignerview.gui",
    )
    args = parser.parse_args()
    source_bytes = args.source.read_bytes()
    digest = hashlib.sha256(source_bytes).hexdigest()
    if digest != VANILLA_SHA256:
        raise ValueError(f"unexpected HOI4 GUI baseline SHA-256: {digest}")
    output = generate(source_bytes.decode("ascii"))
    args.output.write_text(output, encoding="ascii", newline="")
    print(f"ATRMRW GUI generated: {args.output.relative_to(repo)}, baseline={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
