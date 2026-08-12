#!/usr/bin/env python3

import sqlite3
import tempfile
import unittest
from pathlib import Path

from nsdb_readonly import (
    connect_readonly,
    database_manifest,
    normalize_source_url,
    search_candidates,
    select_by_source_url,
)


class NsdbReadonlyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.db = Path(self.tempdir.name) / "fixture.db"
        connection = sqlite3.connect(self.db)
        connection.execute(
            "CREATE TABLE CLASS (CLASS_NAME TEXT, TYPE TEXT, COUNTRY TEXT, source_url TEXT, Photo TEXT)"
        )
        connection.executemany(
            "INSERT INTO CLASS VALUES (?, ?, ?, ?, ?)",
            [
                ("AKAGI Class", "aircraft-carrier", "Japan", "https://www.navypedia.org/ships/japan/jap_cv_akagi.htm", "blob"),
                ("AKAGI Class", "patrol-craft", "Japan", "https://www.navypedia.org/ships/japan/jap_cg_akagi.htm", "blob"),
            ],
        )
        connection.commit()
        connection.close()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_manifest_fixes_database_identity(self) -> None:
        manifest = database_manifest(self.db)
        self.assertEqual(manifest["class_rows"], 2)
        self.assertEqual(len(str(manifest["sha256"])), 64)

    def test_search_returns_ambiguous_candidates_without_selecting(self) -> None:
        candidates = search_candidates(self.db, "AKAGI", country="Japan")
        self.assertEqual(len(candidates), 2)
        self.assertTrue(all(row["review_status"] == "candidate" for row in candidates))

    def test_exact_source_url_selects_one_row(self) -> None:
        payload = select_by_source_url(
            self.db, "https://myownonpmirror.com/ships/japan/jap_cv_akagi.html"
        )
        self.assertEqual(payload["raw"]["TYPE"], "aircraft-carrier")
        self.assertEqual(payload["review_status"], "selected")
        self.assertNotIn("Photo", payload["raw"])

    def test_connection_is_query_only(self) -> None:
        with connect_readonly(self.db) as connection:
            with self.assertRaises(sqlite3.OperationalError):
                connection.execute("DELETE FROM CLASS")

    def test_url_normalization(self) -> None:
        self.assertEqual(
            normalize_source_url("https://old-navypedia.org/ships/x.htm"),
            "https://myownonpmirror.com/ships/x.html",
        )


if __name__ == "__main__":
    unittest.main()
