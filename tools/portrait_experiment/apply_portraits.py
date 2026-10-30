#!/usr/bin/env python3
"""Prepare, apply, verify or restore the explicitly approved portrait profile.

Only existing full-size portrait paths under bakasekai/gfx/leaders may be replaced.
Original bytes, staged replacements and a recovery manifest remain in documents/.
GUI/GFX and other generators are never written. No commit, push or publication.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import stat
import struct
import sys
import tempfile
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True

from PIL import Image, __version__ as PILLOW_VERSION
import run_experiment as experiment

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "documents/portrait_experiment"
BATCH = OUT / "production/2026-10-29-r104x140_c256_fs"
MANIFEST = BATCH / "manifest.json"
LEADERS = ROOT / "bakasekai/gfx/leaders"
PROFILE = {"key": "r104x140_c256_fs", "size": [104, 140], "colors": 256, "dither": "fs"}
MIP_FLAG, MIP_CAPS = 0x20000, 0x400008


def sha(raw: bytes) -> str:
  return experiment.sha256(raw)


def atomic_write(path: Path, raw: bytes, mode: int = 0o644) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  temp_name = None
  try:
    with tempfile.NamedTemporaryFile(prefix=".portrait-", dir=path.parent, delete=False) as stream:
      temp_name = Path(stream.name)
      stream.write(raw)
      stream.flush()
      os.fsync(stream.fileno())
    temp_name.chmod(mode)
    os.replace(temp_name, path)
  finally:
    if temp_name is not None and temp_name.exists():
      temp_name.unlink()  # Only this function's disposable temporary file.


def write_json(path: Path, value) -> None:
  atomic_write(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def live_path(relative: str) -> Path:
  path = ROOT / relative
  if not path.is_relative_to(LEADERS) or not path.resolve().is_relative_to(LEADERS.resolve()):
    raise ValueError(f"Not a portrait path: {relative}")
  if path.is_symlink() or not path.is_file() or path.suffix.lower() not in {".dds", ".png", ".tga"}:
    raise ValueError(f"Not an existing regular portrait: {relative}")
  return path


def stored_path(kind: str, relative: str) -> Path:
  live_path(relative)
  path = BATCH / kind / relative
  if not path.resolve().is_relative_to(BATCH.resolve()):
    raise ValueError(f"Backup/staging path escapes batch: {relative}")
  return path


def mip_count(raw: bytes) -> int:
  return max(1, struct.unpack_from("<I", raw, 28)[0]) if raw[:4] == b"DDS " else 1


def mip_images(image: Image.Image, count: int) -> list[Image.Image]:
  levels = [image.convert("RGBA")]
  for _ in range(1, count):
    width, height = levels[-1].size
    if width == height == 1:
      raise ValueError("Invalid excess mip levels")
    levels.append(experiment.downsample(levels[-1], (max(1, width // 2), max(1, height // 2))))
  return levels


def encode(source: Image.Image, image: Image.Image, raw_source: bytes) -> bytes:
  # DDS stays DDS; uncompressed RGBA32 preserves palette RGB and alpha exactly.
  # This matches a large existing DDS family in the repository and avoids BC loss.
  if source.format == "DDS":
    buffer = io.BytesIO()
    image.convert("RGBA").save(buffer, format="DDS")
    encoded = buffer.getvalue()
    count = mip_count(raw_source)
    header = bytearray(encoded[:128])
    if count > 1:
      struct.pack_into("<I", header, 8, struct.unpack_from("<I", header, 8)[0] | MIP_FLAG)
      struct.pack_into("<I", header, 108, struct.unpack_from("<I", header, 108)[0] | MIP_CAPS)
    # Preserve the source's raw mip-count convention (0 and 1 both mean one level).
    struct.pack_into("<I", header, 28, struct.unpack_from("<I", raw_source, 28)[0])
    return bytes(header) + b"".join(level.tobytes("raw", "BGRA") for level in mip_images(image, count))
  output = io.BytesIO()
  options = {}
  if source.format == "TGA" and source.info.get("compression") == "tga_rle":
    options["compression"] = "tga_rle"
  # Two pre-existing .dds paths contain PNG bytes; retain their actual encoding.
  image.convert(source.mode).save(output, format=source.format, **options)
  return output.getvalue()


def validate_encoding(raw: bytes, expected: Image.Image, source_format: str, levels: int) -> None:
  with Image.open(io.BytesIO(raw)) as image:
    if image.format != source_format or image.size != expected.size or getattr(image, "n_frames", 1) != 1:
      raise ValueError("Format, dimensions or frame count differs")
    if image.convert("RGBA").tobytes() != expected.convert("RGBA").tobytes():
      raise ValueError("Encoded portrait is not pixel-exact")
  if source_format == "DDS":
    if raw[:4] != b"DDS " or mip_count(raw) != levels:
      raise ValueError("DDS header/mip count differs")
    if struct.unpack_from("<I", raw, 88)[0] != 32:
      raise ValueError("DDS is not lossless RGBA32")
    position = 128
    for level in mip_images(expected, levels):
      length = level.width * level.height * 4
      decoded = Image.frombytes("RGBA", level.size, raw[position:position + length], "raw", "BGRA")
      if decoded.tobytes() != level.tobytes():
        raise ValueError("DDS mip pixels differ")
      position += length
    if position != len(raw):
      raise ValueError("DDS mip payload size differs")


def protected_snapshot() -> dict[str, str]:
  files = [p for p in (ROOT / "bakasekai/interface").rglob("*") if p.is_file() and p.suffix.lower() in {".gui", ".gfx"}]
  files += [p for p in (ROOT / "tools").glob("*.py") if p.is_file()]
  return {p.relative_to(ROOT).as_posix(): sha(p.read_bytes()) for p in sorted(files)}


def load_manifest() -> dict:
  manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
  if manifest["profile"] != PROFILE or manifest["root"] != str(ROOT):
    raise ValueError("Unexpected batch root/profile")
  return manifest


def prepare() -> None:
  if MANIFEST.exists():
    manifest = load_manifest()
    print(f"Existing batch preserved: {manifest['status']}; {len(manifest['entries'])} entries.", flush=True)
    if manifest["status"] not in {"prepared", "applied", "restored"}:
      raise ValueError("Incomplete batch retained; inspect its manifest before continuing")
    return
  inventory = json.loads((OUT / "audit/source_audit.json").read_text(encoding="utf-8"))["images"]
  manifest = {
    "root": str(ROOT), "date": "2026-10-29", "authorization": "User explicitly requested 本番適用 in this chat",
    "status": "preparing", "profile": PROFILE, "pillow": PILLOW_VERSION,
    "selection_rule": "156x210 portraits plus nine CHI 156x212 portraits with verified large references; small/advisor assets and three unreferenced nonstandard large assets excluded",
    "entries": [], "excluded": [], "protected_before": protected_snapshot(), "applied_count": 0,
  }
  BATCH.mkdir(parents=True, exist_ok=True)
  write_json(MANIFEST, manifest)
  for index, row in enumerate(inventory, 1):
    relative = row["path"]
    path = live_path(relative)
    raw = path.read_bytes()
    if sha(raw) != row["sha256"]:
      raise ValueError(f"Portrait changed since experiment; refusing replacement: {relative}")
    native = row["size"] == [156, 210]
    chi = row["size"] == [156, 212] and relative.startswith("bakasekai/gfx/leaders/CHI/")
    if not native and not chi:
      reason = "small/advisor/focus image" if max(row["size"]) <= 135 else "unreferenced nonstandard portrait"
      manifest["excluded"].append({"path": relative, "size": row["size"], "sha256": row["sha256"], "reason": reason})
      continue
    backup = stored_path("backup", relative)
    if backup.exists() and backup.read_bytes() != raw:
      raise ValueError(f"Different original backup retained: {relative}")
    if not backup.exists():
      atomic_write(backup, raw)
    spec = {**PROFILE, "size": [104, 140] if native else [104, 141]}
    with Image.open(io.BytesIO(raw)) as source:
      if source.mode not in {"RGB", "RGBA"} or getattr(source, "n_frames", 1) != 1:
        raise ValueError(f"Unsupported portrait shape: {relative}")
      original = source.convert("RGBA")
      _, display = experiment.make_variant(original, spec)
      encoded = encode(source, display, raw)
      validate_encoding(encoded, display, source.format, mip_count(raw))
      if display.getchannel("A").tobytes() != original.getchannel("A").tobytes() or experiment.color_count(display) > 256:
        raise ValueError(f"Alpha/color invariant failed: {relative}")
      entry = {
        "path": relative, "before_sha256": sha(raw), "after_sha256": sha(encoded),
        "source_format": source.format, "source_mode": source.mode, "native_size": row["size"],
        "spec": spec, "mip_levels": mip_count(raw), "rgb_colors": experiment.color_count(display),
        "rgba_sha256": experiment.image_sha(display), "alpha_sha256": sha(original.getchannel("A").tobytes()),
        "mode": stat.S_IMODE(path.stat().st_mode), "before_bytes": len(raw), "after_bytes": len(encoded),
      }
    atomic_write(stored_path("staged", relative), encoded)
    manifest["entries"].append(entry)
    if len(manifest["entries"]) % 50 == 0:
      write_json(MANIFEST, manifest)
      print(f"PREPARE {len(manifest['entries'])} portraits; originals backed up and replacements verified.", flush=True)
  if len(manifest["entries"]) != 793 or len(manifest["excluded"]) != 25:
    raise ValueError("Selection count differs from reviewed 793 portraits / 25 exclusions")
  manifest["status"] = "prepared"
  manifest["summary"] = {
    "portraits": len(manifest["entries"]), "excluded": len(manifest["excluded"]),
    "formats": dict(Counter(e["source_format"] for e in manifest["entries"])),
    "mipmapped_dds": sum(e["mip_levels"] > 1 for e in manifest["entries"]),
    "backup_bytes": sum(e["before_bytes"] for e in manifest["entries"]),
    "output_bytes": sum(e["after_bytes"] for e in manifest["entries"]),
  }
  write_json(MANIFEST, manifest)
  print("PREPARED " + json.dumps(manifest["summary"], ensure_ascii=False), flush=True)


def preflight(manifest: dict) -> None:
  for entry in manifest["entries"]:
    relative = entry["path"]
    current = sha(live_path(relative).read_bytes())
    if current not in {entry["before_sha256"], entry["after_sha256"]}:
      raise ValueError(f"Concurrent portrait edit; will not overwrite it: {relative}")
    if sha(stored_path("backup", relative).read_bytes()) != entry["before_sha256"]:
      raise ValueError(f"Original backup hash mismatch: {relative}")
    if sha(stored_path("staged", relative).read_bytes()) != entry["after_sha256"]:
      raise ValueError(f"Staged replacement hash mismatch: {relative}")
  for row in manifest["excluded"]:
    if sha(live_path(row["path"]).read_bytes()) != row["sha256"]:
      raise ValueError(f"Excluded portrait changed: {row['path']}")


def apply() -> None:
  manifest = load_manifest()
  if manifest["status"] not in {"prepared", "applying", "applied", "restored"}:
    raise ValueError(f"Cannot apply batch in state: {manifest['status']}")
  # Verify every backup and replacement before crossing the mutation boundary.
  preflight(manifest)
  manifest["status"] = "applying"
  write_json(MANIFEST, manifest)
  written = []
  try:
    for index, entry in enumerate(manifest["entries"], 1):
      relative = entry["path"]
      path = live_path(relative)
      current = sha(path.read_bytes())
      if current != entry["after_sha256"]:
        if current != entry["before_sha256"]:
          raise ValueError(f"Concurrent edit before atomic replacement: {relative}")
        atomic_write(path, stored_path("staged", relative).read_bytes(), entry["mode"])
        written.append(entry)
      manifest["applied_count"] = index
      if index % 50 == 0:
        write_json(MANIFEST, manifest)
        print(f"APPLY {index}/{len(manifest['entries'])}", flush=True)
    manifest["status"] = "applied"
    write_json(MANIFEST, manifest)
  except Exception as error:
    conflicts = []
    for entry in reversed(written):
      path = live_path(entry["path"])
      if sha(path.read_bytes()) == entry["after_sha256"]:
        atomic_write(path, stored_path("backup", entry["path"]).read_bytes(), entry["mode"])
      else:
        conflicts.append(entry["path"])
    manifest["status"] = "failed_with_conflicts" if conflicts else "failed_rolled_back"
    manifest["failure"] = {"error": str(error), "concurrent_edits_left_untouched": conflicts}
    write_json(MANIFEST, manifest)
    raise
  print(f"APPLIED {len(manifest['entries'])} portraits; original backups retained.", flush=True)


def check() -> dict:
  manifest = load_manifest()
  failures = []
  counts = Counter()
  for index, entry in enumerate(manifest["entries"], 1):
    try:
      original_raw = stored_path("backup", entry["path"]).read_bytes()
      raw = live_path(entry["path"]).read_bytes()
      if sha(original_raw) != entry["before_sha256"] or sha(raw) != entry["after_sha256"]:
        raise ValueError("Original/live file hash mismatch")
      if sha(stored_path("staged", entry["path"]).read_bytes()) != entry["after_sha256"]:
        raise ValueError("Staged file hash mismatch")
      with Image.open(io.BytesIO(original_raw)) as original_image:
        original = original_image.convert("RGBA")
      _, expected = experiment.make_variant(original, entry["spec"])
      validate_encoding(raw, expected, entry["source_format"], entry["mip_levels"])
      if experiment.image_sha(expected) != entry["rgba_sha256"] or experiment.color_count(expected) > 256:
        raise ValueError("Color/RGBA invariant mismatch")
      if sha(expected.getchannel("A").tobytes()) != entry["alpha_sha256"]:
        raise ValueError("Original alpha differs")
      counts["portraits"] += 1
      counts["mipmapped_dds"] += entry["mip_levels"] > 1
    except Exception as error:
      failures.append({"path": entry["path"], "error": str(error)})
    if index % 100 == 0:
      print(f"CHECK {index}/{len(manifest['entries'])}", flush=True)
  for row in manifest["excluded"]:
    if sha(live_path(row["path"]).read_bytes()) != row["sha256"]:
      failures.append({"path": row["path"], "error": "Excluded asset changed"})
  selected = json.loads((OUT / "source_selection.json").read_text(encoding="utf-8"))["samples"]
  for sample in selected:
    with Image.open(live_path(sample["source"])) as image:
      with Image.open(OUT / f"variants/{sample['id']}/{PROFILE['key']}.png") as approved:
        if image.convert("RGBA").tobytes() != approved.convert("RGBA").tobytes():
          failures.append({"path": sample["source"], "error": "Differs from approved experiment variant"})
  drift = [path for path, digest in manifest["protected_before"].items() if not (ROOT / path).exists() or sha((ROOT / path).read_bytes()) != digest]
  if manifest["status"] != "applied":
    failures.append({"path": "manifest.json", "error": f"Batch state is {manifest['status']}"})
  runtime_path = BATCH / "runtime_verification.json"
  runtime = json.loads(runtime_path.read_text(encoding="utf-8")) if runtime_path.exists() else None
  report = {
    "result": "FAIL" if failures else "PASS", "profile": PROFILE["key"],
    "verified_live_portraits": counts["portraits"], "excluded_unchanged": len(manifest["excluded"]),
    "native_dimensions": "preserved", "alpha": "byte-exact to originals", "rgb_color_limit": 256,
    "mipmap_levels_and_payloads_verified": counts["mipmapped_dds"], "approved_sample_matches": len(selected),
    "original_backups": "SHA-256 verified", "protected_gui_gfx_or_other_generator_drift": drift,
    "write_scope": "only manifest-listed existing bakasekai/gfx/leaders image paths",
    "actual_game_verification": "See runtime_verification.json" if runtime else "NOT RUN",
    "failures": failures,
  }
  write_json(BATCH / "verification.json", report)
  print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
  if failures:
    raise SystemExit(1)
  return report


def restore() -> None:
  manifest = load_manifest()
  preflight(manifest)
  for entry in manifest["entries"]:
    path = live_path(entry["path"])
    if sha(path.read_bytes()) == entry["after_sha256"]:
      atomic_write(path, stored_path("backup", entry["path"]).read_bytes(), entry["mode"])
  if any(sha(live_path(e["path"]).read_bytes()) != e["before_sha256"] for e in manifest["entries"]):
    raise ValueError("Restore verification failed")
  manifest["status"] = "restored"
  manifest["applied_count"] = 0
  write_json(MANIFEST, manifest)
  print(f"RESTORED {len(manifest['entries'])} original portraits; later unrelated edits were not overwritten.", flush=True)


def main() -> None:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("command", choices=["prepare", "apply", "check", "restore"])
  command = parser.parse_args().command
  {"prepare": prepare, "apply": apply, "check": check, "restore": restore}[command]()


if __name__ == "__main__":
  main()
