#!/usr/bin/env python3

import subprocess
import sys
import unittest
from pathlib import Path

from tools.atrmrw.build_japan_prototype_ledger import PROTOTYPES, length_oa, numbers


REPO = Path(__file__).resolve().parents[2]


class JapanPrototypeLedgerTest(unittest.TestCase):
    def test_compound_nsdb_values_are_preserved_for_explicit_selection(self) -> None:
        self.assertEqual(numbers("2589 / 3654"), [2589.0, 3654.0])
        self.assertEqual(numbers("23.6 / 8"), [23.6, 8.0])
        self.assertEqual(numbers("14000(16) / 96(3)"), [14000.0, 16.0, 96.0, 3.0])

    def test_length_prefers_explicit_oa(self) -> None:
        self.assertEqual(length_oa("244.0 pp 256.0 wl 263.0 oa"), 263.0)
        with self.assertRaisesRegex(ValueError, "no OA"):
            length_oa("244.0 pp 256.0 wl")

    def test_approved_ssw_hull_ids_are_fixed(self) -> None:
        self.assertEqual(PROTOTYPES["jap_yamato"]["implementation_hull_id"], "ship_hull_JAP_BB_3")
        self.assertEqual(PROTOTYPES["jap_takao"]["implementation_hull_id"], "ship_hull_JAP_CA_0")
        self.assertEqual(PROTOTYPES["jap_fubuki"]["implementation_hull_id"], "ship_hull_JAP_DD_13")
        self.assertEqual(PROTOTYPES["jap_akagi"]["implementation_hull_id"], "ship_hull_JAP_CV_0")
        self.assertEqual(PROTOTYPES["jap_i15"]["implementation_hull_id"], "ship_hull_JAP_SS_9")

    def test_checked_in_ledger_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(REPO / "tools/atrmrw/validate_prototype_ledger.py")],
            cwd=REPO,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("5 classes", result.stdout)


if __name__ == "__main__":
    unittest.main()
