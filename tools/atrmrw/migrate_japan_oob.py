#!/usr/bin/env python3
"""JPN 1936 OOBの3艦級だけをATRMRW船体へ決定論的に移行する。"""

from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
OOB = REPO / "bakasekai/history/units/JPN_1936_naval.txt"
MIGRATIONS = {
    'ship_hull_carrier_conversion_bb = {amount = 1 owner = JPN version_name = "赤城型"}': (
        'ship_hull_JAP_CV_0 = {amount = 1 owner = JPN version_name = "赤城型"}', 1,
    ),
    'ship_hull_cruiser_1 = {amount = 1 owner = JPN version_name = "高雄型"}': (
        'ship_hull_JAP_CA_0 = {amount = 1 owner = JPN version_name = "高雄型"}', 4,
    ),
    'ship_hull_light_1 = {amount = 1 owner = JPN version_name = "吹雪型"}': (
        'ship_hull_JAP_DD_13 = {amount = 1 owner = JPN version_name = "吹雪型"}', 23,
    ),
}


def migrate(text: str) -> str:
    result = text
    for old, (new, expected) in MIGRATIONS.items():
        old_count = result.count(old)
        new_count = result.count(new)
        if old_count == expected and new_count == 0:
            result = result.replace(old, new)
        elif old_count == 0 and new_count == expected:
            continue
        else:
            raise ValueError(f"migration count mismatch: old={old_count}, new={new_count}, expected={expected}")
    return result


def main() -> int:
    before = OOB.read_text(encoding="utf-8")
    after = migrate(before)
    OOB.write_text(after, encoding="utf-8", newline="")
    print("ATRMRW OOB migration: Akagi=1, Takao=4, Fubuki=23")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
