#!/usr/bin/env python3
"""Exercise apply/recovery against copied fixtures, never against production assets."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

import apply_portraits as subject


def main() -> None:
  production_batch = subject.BATCH
  prepared = subject.load_manifest()
  fixture_root = Path(tempfile.mkdtemp(prefix="safety-fixture-", dir=production_batch.parent))
  subject.ROOT = fixture_root
  subject.LEADERS = fixture_root / "bakasekai/gfx/leaders"
  subject.BATCH = fixture_root / "batch"
  subject.MANIFEST = subject.BATCH / "manifest.json"
  entries = [next(e for e in prepared["entries"] if e["source_format"] == format_name) for format_name in ["PNG", "DDS"]]
  for entry in entries:
    for kind in ["backup", "staged"]:
      path = subject.BATCH / kind / entry["path"]
      subject.atomic_write(path, (production_batch / kind / entry["path"]).read_bytes())
    subject.atomic_write(fixture_root / entry["path"], (production_batch / "backup" / entry["path"]).read_bytes())
  base = {"root": str(fixture_root), "profile": subject.PROFILE, "status": "prepared", "entries": entries, "excluded": [], "applied_count": 0}
  subject.write_json(subject.MANIFEST, base)
  passed = []

  def check_hashes(which: str) -> None:
    for entry in entries:
      assert subject.sha((fixture_root / entry["path"]).read_bytes()) == entry[which]

  subject.apply()
  check_hashes("after_sha256")
  passed.append("apply exact staged bytes")
  subject.apply()
  check_hashes("after_sha256")
  passed.append("repeated apply is idempotent")
  subject.restore()
  check_hashes("before_sha256")
  passed.append("restore exact original bytes")
  subject.restore()
  check_hashes("before_sha256")
  passed.append("repeated restore is idempotent")

  first = fixture_root / entries[0]["path"]
  external = b"fixture: concurrent portrait edit must survive"
  first.write_bytes(external)
  for name, operation in [("apply", subject.apply), ("restore", subject.restore)]:
    try:
      operation()
    except ValueError:
      assert first.read_bytes() == external
      passed.append(f"concurrent edit blocks {name} without overwriting it")
    else:
      raise AssertionError(f"Concurrent edit did not block {name}")
  subject.atomic_write(first, (production_batch / "backup" / entries[0]["path"]).read_bytes())

  write = subject.atomic_write
  second = fixture_root / entries[1]["path"]
  for introduce_external_edit in [False, True]:
    subject.write_json(subject.MANIFEST, {**base, "status": "prepared"})

    def fail_second(path: Path, raw: bytes, mode: int = 0o644) -> None:
      if path == second and subject.sha(raw) == entries[1]["after_sha256"]:
        if introduce_external_edit:
          first.write_bytes(external)
        raise OSError("injected fixture write failure")
      write(path, raw, mode)

    subject.atomic_write = fail_second
    try:
      subject.apply()
    except OSError:
      result = json.loads(subject.MANIFEST.read_text(encoding="utf-8"))
      if introduce_external_edit:
        assert first.read_bytes() == external
        assert result["status"] == "failed_with_conflicts"
        passed.append("rollback preserves a concurrent edit")
      else:
        check_hashes("before_sha256")
        assert result["status"] == "failed_rolled_back"
        passed.append("partial apply failure rolls back owned replacements")
    else:
      raise AssertionError("Injected write failure did not occur")
    finally:
      subject.atomic_write = write
    subject.atomic_write(first, (production_batch / "backup" / entries[0]["path"]).read_bytes())
  check_hashes("before_sha256")
  report = {"result": "PASS", "fixture_root": str(fixture_root), "cases": passed, "production_assets_written": False}
  subject.write_json(production_batch / "safety_verification.json", report)
  print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
  main()
