#!/usr/bin/env python3

import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
LEDGER = REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE3_JAPAN_MODULE_LEDGER.json"


class CompileJapanModuleStatsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(LEDGER.read_text(encoding="utf-8"))

    def test_all_modules_are_compiled_without_unresolved_classification(self) -> None:
        self.assertEqual(self.payload["module_count"], 59)
        self.assertEqual(len(self.payload["modules"]), 59)
        self.assertNotIn("unresolved", {row["classification"] for row in self.payload["modules"]})

    def test_reference_hulls_forward_compose_to_historical_targets(self) -> None:
        self.assertEqual(len(self.payload["hulls"]), 5)
        for hull in self.payload["hulls"]:
            for stat in hull["calibration"].values():
                self.assertGreaterEqual(stat["base"], 0)
                self.assertTrue(math.isclose(stat["target"], stat["forward_result"], abs_tol=1e-5))

    def test_historical_unknowns_do_not_receive_fabricated_stats(self) -> None:
        structure = next(row for row in self.payload["modules"] if row["module_id"] == "atrmrw_structure_yamato_1942")
        self.assertEqual(structure["add_stats"], {})
        self.assertEqual(structure["multiply_stats"], {})

    def test_builder_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "ledger.json"
            result = subprocess.run(
                [sys.executable, str(REPO / "tools/atrmrw/compile_japan_module_stats.py"), "--output", str(output)],
                cwd=REPO, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), self.payload)


if __name__ == "__main__":
    unittest.main()
