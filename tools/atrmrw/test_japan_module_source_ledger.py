#!/usr/bin/env python3

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.atrmrw.validate_japan_module_source_ledger import validate


REPO = Path(__file__).resolve().parents[2]
LEDGER_PATH = REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE3_JAPAN_MODULE_SOURCE_LEDGER.json"
PACKING_PATH = REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE3_JAPAN_SLOT_PACKING.json"


class JapanModuleSourceLedgerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        cls.packing = json.loads(PACKING_PATH.read_text(encoding="utf-8"))

    def test_checked_in_ledger_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(REPO / "tools/atrmrw/validate_japan_module_source_ledger.py")],
            cwd=REPO, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("59 logical modules", result.stdout)

    def test_builder_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "ledger.json"
            result = subprocess.run(
                [sys.executable, str(REPO / "tools/atrmrw/build_japan_module_source_ledger.py"), "--output", str(output)],
                cwd=REPO, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), self.ledger)

    def test_duplicate_source_definition_is_rejected(self) -> None:
        payload = copy.deepcopy(self.ledger)
        payload["source_scan"]["duplicate_module_ids"] = ["SRM_BB"]
        self.assertTrue(any("duplicate_module_ids" in error for error in validate(payload, self.packing)))

    def test_parent_effective_stat_tamper_is_rejected(self) -> None:
        payload = copy.deepcopy(self.ledger)
        child_id = next(module_id for module_id, module in payload["source_modules"].items() if module["parent_id"])
        payload["source_modules"][child_id]["effective_add_stats"]["tampered"] = 1.0
        self.assertTrue(any("parent inheritance" in error for error in validate(payload, self.packing)))

    def test_missing_source_reference_is_rejected(self) -> None:
        payload = copy.deepcopy(self.ledger)
        exact = next(row for row in payload["logical_modules"] if row["classification"] == "exact")
        exact["source_module_ids"] = ["not_in_registry"]
        self.assertTrue(any("missing from registry" in error for error in validate(payload, self.packing)))

    def test_weapon_batch_cannot_be_marked_exact(self) -> None:
        payload = copy.deepcopy(self.ledger)
        batch = next(row for row in payload["logical_modules"] if row["classification"] == "aggregate_required")
        batch["classification"] = "exact"
        errors = validate(payload, self.packing)
        self.assertTrue(any("batch must be aggregate_required" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
