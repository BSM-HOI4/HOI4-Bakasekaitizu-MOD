#!/usr/bin/env python3
"""ATRMRW用NSDB read-onlyアダプタ。DBを変更・複製しない。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
from pathlib import Path
from typing import Any, Sequence
from urllib.parse import quote


IMAGE_COLUMNS = {"Photo", "images", "Graphics"}


def database_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def connect_readonly(path: Path) -> sqlite3.Connection:
    if not path.is_file():
        raise FileNotFoundError(f"NSDB not found: {path}")
    uri = f"file:{quote(str(path.resolve()))}?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only = ON")
    return connection


def clean_cell(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value).replace("\r", " ").replace("\n", " ")).strip()


def normalize_source_url(url: str) -> str:
    normalized = re.sub(
        r"https?://(?:www\.)?(?:old-)?navypedia\.org",
        "https://myownonpmirror.com",
        url,
    )
    if normalized.startswith("https://myownonpmirror.com/"):
        normalized = re.sub(r"\.htm($|[?#])", r".html\1", normalized)
    return normalized


def database_manifest(path: Path) -> dict[str, object]:
    with connect_readonly(path) as connection:
        tables = [
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
        ]
        if "CLASS" not in tables:
            raise ValueError("NSDB is missing CLASS table")
        columns = [row[1] for row in connection.execute("PRAGMA table_info(CLASS)")]
        class_rows = int(connection.execute("SELECT COUNT(*) FROM CLASS").fetchone()[0])
    return {
        "path": str(path.resolve()),
        "size_bytes": path.stat().st_size,
        "sha256": database_sha256(path),
        "class_rows": class_rows,
        "tables": tables,
        "class_columns": columns,
    }


def row_payload(row: sqlite3.Row, db_manifest: dict[str, object]) -> dict[str, object]:
    raw = {key: clean_cell(row[key]) for key in row.keys() if key not in IMAGE_COLUMNS}
    raw_url = raw.get("source_url", "")
    return {
        "source_id": f"nsdb:{normalize_source_url(raw_url) or raw.get('CLASS_NAME', 'unknown')}",
        "source_type": "nsdb",
        "database_sha256": db_manifest["sha256"],
        "source_url_raw": raw_url,
        "source_url_normalized": normalize_source_url(raw_url),
        "raw": raw,
        "review_status": "candidate",
    }


def search_candidates(
    path: Path,
    query: str,
    country: str | None = None,
    type_name: str | None = None,
    limit: int = 20,
) -> list[dict[str, object]]:
    if limit < 1:
        raise ValueError("limit must be >= 1")
    clauses = ["(CLASS_NAME LIKE ? OR source_url LIKE ?)"]
    params: list[object] = [f"%{query}%", f"%{query}%"]
    if country:
        clauses.append("COUNTRY = ?")
        params.append(country)
    if type_name:
        clauses.append("TYPE = ?")
        params.append(type_name)
    params.append(limit)
    sql = (
        "SELECT * FROM CLASS WHERE "
        + " AND ".join(clauses)
        + " ORDER BY COUNTRY, TYPE, CLASS_NAME, source_url LIMIT ?"
    )
    manifest = database_manifest(path)
    with connect_readonly(path) as connection:
        rows = connection.execute(sql, params).fetchall()
    return [row_payload(row, manifest) for row in rows]


def select_by_source_url(path: Path, source_url: str) -> dict[str, object]:
    normalized = normalize_source_url(source_url)
    manifest = database_manifest(path)
    with connect_readonly(path) as connection:
        rows = connection.execute("SELECT * FROM CLASS").fetchall()
    matches = [
        row for row in rows if normalize_source_url(clean_cell(row["source_url"])) == normalized
    ]
    if not matches:
        raise LookupError(f"no CLASS row for source URL: {normalized}")
    if len(matches) != 1:
        raise LookupError(f"ambiguous source URL ({len(matches)} rows): {normalized}")
    payload = row_payload(matches[0], manifest)
    payload["review_status"] = "selected"
    return payload


def resolve_db_path(value: str | None) -> Path:
    configured = value or os.environ.get("ATRMRW_NSDB_PATH")
    if not configured:
        raise ValueError("pass --db or set ATRMRW_NSDB_PATH")
    return Path(configured).expanduser().resolve()


def dump(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("manifest")
    search = subparsers.add_parser("search")
    search.add_argument("query")
    search.add_argument("--country")
    search.add_argument("--type", dest="type_name")
    search.add_argument("--limit", type=int, default=20)
    select = subparsers.add_parser("select")
    select.add_argument("--source-url", required=True)
    args = parser.parse_args(argv)

    try:
        db_path = resolve_db_path(args.db)
        if args.command == "manifest":
            dump(database_manifest(db_path))
        elif args.command == "search":
            dump(
                search_candidates(
                    db_path,
                    args.query,
                    country=args.country,
                    type_name=args.type_name,
                    limit=args.limit,
                )
            )
        elif args.command == "select":
            dump(select_by_source_url(db_path, args.source_url))
    except (FileNotFoundError, LookupError, ValueError, sqlite3.Error) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
