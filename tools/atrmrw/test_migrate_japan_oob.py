#!/usr/bin/env python3

import unittest

from tools.atrmrw.migrate_japan_oob import MIGRATIONS, OOB, migrate


class MigrateJapanOobTest(unittest.TestCase):
    def test_checked_in_oob_is_fully_migrated(self) -> None:
        text = OOB.read_text(encoding="utf-8")
        for old, (new, expected) in MIGRATIONS.items():
            self.assertEqual(text.count(old), 0)
            self.assertEqual(text.count(new), expected)

    def test_migration_is_idempotent(self) -> None:
        text = OOB.read_text(encoding="utf-8")
        self.assertEqual(migrate(text), text)


if __name__ == "__main__":
    unittest.main()
