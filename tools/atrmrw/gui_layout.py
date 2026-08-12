#!/usr/bin/env python3
"""HOI4 1.19.2 Equipment Designer内のATRMRW 36枠座標契約。"""

from __future__ import annotations


SLOT_WIDTH = 76
SLOT_HEIGHT = 47
PANEL_WIDTH = 512
PANEL_HEIGHT = 350
COLUMNS = (0, 73, 146, 219, 292, 365, 438)

CUSTOM_COORDINATES = {
    **{index: (x, 0) for index, x in enumerate(COLUMNS)},
    **{index + 7: (x, 50) for index, x in enumerate(COLUMNS)},
    **{index + 14: (x, 100) for index, x in enumerate(COLUMNS[:4])},
}

FIXED_COORDINATES = {
    **{index: (x, 300) for index, x in enumerate(COLUMNS)},
    **{index + 7: (x, 200) for index, x in enumerate(COLUMNS)},
    **{index + 14: (x, 250) for index, x in enumerate(COLUMNS[:4])},
}


def coordinate_for(group: str, index: int) -> tuple[int, int]:
    table = {"custom": CUSTOM_COORDINATES, "fixed": FIXED_COORDINATES}.get(group)
    if table is None or index not in table:
        raise ValueError(f"unknown GUI coordinate: {group}[{index}]")
    return table[index]
