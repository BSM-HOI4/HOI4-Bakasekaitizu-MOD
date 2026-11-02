#!/usr/bin/env python3
"""Offline, opt-in portrait experiment. All writes stay in documents/portrait_experiment.

No game asset, GUI/GFX, existing generator, or source portrait is ever written.
Pillow is the only non-standard dependency. See README.md in the output directory.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import platform
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, __version__ as PILLOW_VERSION

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent.parent
OUT = ROOT / "documents/portrait_experiment"
CONFIG = json.loads((TOOLS / "experiment.json").read_text(encoding="utf-8"))
NATIVE = (156, 210)
RESAMPLE = Image.Resampling
GRAY, WHITE, NAVY = "#c0c0c0", "#ffffff", "#000080"


def output_path(relative: str) -> Path:
  target = (OUT / relative).resolve()
  if not target.is_relative_to(OUT.resolve()):
    raise ValueError(f"Output escapes experiment directory: {relative}")
  target.parent.mkdir(parents=True, exist_ok=True)
  return target


def write_json(relative: str, value) -> None:
  output_path(relative).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(data: bytes) -> str:
  return hashlib.sha256(data).hexdigest()


def image_sha(image: Image.Image) -> str:
  return sha256(image.convert("RGBA").tobytes())


def image_info(image: Image.Image) -> dict:
  alpha = image.convert("RGBA").getchannel("A")
  hist = alpha.histogram()
  return {
    "size": list(image.size), "mode": image.mode, "format": image.format,
    "alpha_extrema": list(alpha.getextrema()), "transparent_pixels": hist[0],
    "partial_alpha_pixels": sum(hist[1:255]),
    "alpha_kind": "opaque" if hist[255] == image.width * image.height else "partial" if sum(hist[1:255]) else "binary",
  }


def references(path: Path, pattern: str) -> list[dict]:
  result = []
  for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
    active = line.split("#", 1)[0]
    if re.search(pattern, active):
      result.append({"file": path.relative_to(ROOT).as_posix(), "line": number, "text": active.strip()})
  return result


def audit() -> None:
  """Capture exact original bytes once; refuse to replace different snapshots."""
  selection, inventory = [], []
  for sample in CONFIG["samples"]:
    src = ROOT / sample["source"]
    raw = src.read_bytes()
    snap_name = f"originals/{sample['id']}{src.suffix}"
    snap = output_path(snap_name)
    if snap.exists() and snap.read_bytes() != raw:
      raise RuntimeError(f"Source changed; preserving previous snapshot: {src}")
    if not snap.exists():
      snap.write_bytes(raw)
    with Image.open(io.BytesIO(raw)) as source:
      info = image_info(source)
      if source.size != NATIVE:
        raise ValueError(f"This experiment expects 156x210 portraits: {src}")
      decoded = source.convert("RGBA")
      decoded.save(output_path(f"originals/{sample['id']}.decoded.png"))
    chain = {
      "portrait": references(ROOT / sample["character_file"], re.escape(sample["portrait_token"]) + r'(?:"|\s|$)'),
      "recruit": references(ROOT / sample["history_file"], r"\brecruit_character\s*=\s*" + re.escape(sample["character"]) + r"\b"),
    }
    if sample["sprite_file"]:
      chain["sprite"] = references(ROOT / sample["sprite_file"], re.escape(sample["source"].removeprefix("bakasekai/")))
    if not all(chain.values()):
      raise ValueError(f"Incomplete live reference chain: {sample['id']}: {chain}")
    selection.append({**sample, **info, "snapshot": snap_name, "sha256": sha256(raw), "decoded_rgba_sha256": image_sha(decoded), "references": chain})
  for path in sorted((ROOT / "bakasekai/gfx/leaders").rglob("*")):
    if path.suffix.lower() not in {".png", ".dds", ".tga"}:
      continue
    raw = path.read_bytes()
    with Image.open(io.BytesIO(raw)) as source:
      inventory.append({"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(raw), **image_info(source)})
  gui = []
  for path in ["bakasekai/interface/replace/frontendgamesetupview.gui", "bakasekai/interface/replace/countrypoliticsview.gui"]:
    gui.append({"file": path, "sha256": sha256((ROOT / path).read_bytes()), "observed_lines": references(ROOT / path, r'name\s*=\s*"(?:country_leader|minor_country_leader|leader)"|scale\s*=\s*0\.(?:55|42)')})
  status = subprocess.run(["git", "status", "--short", "--branch"], cwd=ROOT, text=True, capture_output=True, check=True).stdout
  output_path("audit/git_status_at_audit.txt").write_text(status, encoding="utf-8")
  write_json("source_selection.json", {"samples": selection})
  write_json("audit/source_audit.json", {
    "captured_at_utc": datetime.now(timezone.utc).isoformat(), "inventory_scope": "repository gfx/leaders .png/.dds/.tga, not a claim that every file is in use",
    "count": len(inventory), "sizes": dict(Counter(f"{x['size'][0]}x{x['size'][1]}" for x in inventory)),
    "alpha": dict(Counter(x["alpha_kind"] for x in inventory)), "images": inventory,
    "gui_snapshot_read_only": gui, "descriptor_sha256": sha256((ROOT / "bakasekai/descriptor.mod").read_bytes()),
    "existing_generators_read_only": {p.relative_to(ROOT).as_posix(): sha256(p.read_bytes()) for p in sorted((ROOT / "tools").glob("*win95*.py"))},
  })
  print(f"AUDIT PASS: {len(inventory)} readable portrait assets; {len(selection)} complete portrait/recruit reference chains; originals preserved.")


def load_sources() -> dict[str, Image.Image]:
  selection = json.loads((OUT / "source_selection.json").read_text(encoding="utf-8"))["samples"]
  result = {}
  for sample in selection:
    snap = OUT / sample["snapshot"]
    if sha256(snap.read_bytes()) != sample["sha256"]:
      raise ValueError(f"Snapshot hash mismatch: {snap}")
    with Image.open(snap) as source:
      result[sample["id"]] = source.convert("RGBA")
  return result


def downsample(source: Image.Image, size: tuple[int, int]) -> Image.Image:
  # Premultiplied RGBa prevents hidden RGB in transparent pixels bleeding into edges.
  # BOX averages in encoded sRGB. No contrast, sharpening, color grading or redraw.
  if size == source.size:
    return source.copy()
  return source.convert("RGBa").resize(size, RESAMPLE.BOX).convert("RGBA")


def quantize(reduced: Image.Image, colors: int, dither: str) -> Image.Image:
  # Build ONE adaptive RGB palette for both dither choices, from visible pixels only.
  # Passing dither to automatic-palette quantize alone does not provide this control.
  visible = [p[:3] for p in reduced.get_flattened_data() if p[3] > 0]
  if not visible:
    raise ValueError("Cannot make an adaptive palette for a completely transparent portrait")
  seed = Image.new("RGB", (len(visible), 1))
  seed.putdata(visible)
  indexed = seed.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
  indices = sorted(index for _, index in indexed.getcolors(maxcolors=256))
  table = indexed.getpalette()
  entries = [table[3 * index:3 * index + 3] for index in indices]
  # Repeat the last real color; avoid introducing unused black palette entries.
  palette = Image.new("P", (1, 1))
  palette.putpalette(sum(entries + [entries[-1]] * (256 - len(entries)), []))
  mode = Image.Dither.NONE if dither == "none" else Image.Dither.FLOYDSTEINBERG
  rgb = reduced.convert("RGB").quantize(palette=palette, dither=mode).convert("RGB")
  result = rgb.convert("RGBA")
  result.putalpha(reduced.getchannel("A"))
  return result


def make_variant(source: Image.Image, spec: dict) -> tuple[Image.Image, Image.Image]:
  working = downsample(source, tuple(spec["size"]))
  if spec["colors"]:
    working = quantize(working, spec["colors"], spec["dither"])
  display = working.convert("RGB").resize(source.size, RESAMPLE.NEAREST).convert("RGBA")
  # Native output retains original alpha byte for byte. Only RGB is pixelated.
  display.putalpha(source.getchannel("A"))
  return working, display


def specs() -> list[dict]:
  result = []
  for width, height in CONFIG["sizes"]:
    result.append({"key": f"r{width}x{height}_rgb", "size": [width, height], "colors": None, "dither": "none"})
    for colors in CONFIG["colors"]:
      for dither in CONFIG["dithers"]:
        result.append({"key": f"r{width}x{height}_c{colors:03d}_{dither}", "size": [width, height], "colors": colors, "dither": dither})
  result.append({"key": "r156x210_c064_none", "size": list(NATIVE), "colors": 64, "dither": "none"})
  return result


def color_count(image: Image.Image) -> int:
  return len({p[:3] for p in image.convert("RGBA").get_flattened_data() if p[3] > 0})


def font(size: int) -> ImageFont.ImageFont:
  for path in ["/System/Library/Fonts/Geneva.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
    if Path(path).is_file():
      return ImageFont.truetype(path, size)
  return ImageFont.load_default(size=size)


def canvas(width: int, height: int, title: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
  image = Image.new("RGB", (width, height), GRAY)
  draw = ImageDraw.Draw(image)
  draw.rectangle((2, 2, width - 3, 27), fill=NAVY)
  draw.text((10, 6), title, fill=WHITE, font=font(14))
  draw.text((10, 35), "OFFLINE COMPARISON / UI MOCKUP / NOT AN IN-GAME SCREENSHOT", fill="black", font=font(12))
  return image, draw


def tile(canvas_image: Image.Image, at: tuple[int, int], portrait: Image.Image) -> None:
  x, y = at
  draw = ImageDraw.Draw(canvas_image)
  draw.rectangle((x - 2, y - 2, x + portrait.width + 1, y + portrait.height + 1), fill="white", outline="#808080")
  canvas_image.paste(portrait, at, portrait.getchannel("A"))


def read_variant(sample: str, key: str) -> Image.Image:
  with Image.open(OUT / f"variants/{sample}/{key}.png") as image:
    return image.convert("RGBA")


def sheets(sources: dict[str, Image.Image]) -> None:
  entries = CONFIG["samples"]
  shortlist = CONFIG["shortlist"]
  contact, contact_draw = canvas(1260, 535, "ORIGINALS / six active portraits / native-size previews + head crops")
  for col, sample in enumerate(entries):
    portrait = sources[sample["id"]]
    x = col * 210
    contact_draw.text((x + 8, 65), sample["label"], font=font(12), fill="black")
    tile(contact, (x + 27, 95), portrait)
    crop = portrait.crop(tuple(sample["face_box"]))
    factor = min(180 / crop.width, 180 / crop.height)
    crop = crop.resize((round(crop.width * factor), round(crop.height * factor)), RESAMPLE.NEAREST)
    tile(contact, (x + 15, 335), crop)
  contact.save(output_path("originals/contact.png"))
  summary, draw = canvas(1190, 1110, "PORTRAIT LAB / 6 subjects / original + three candidates")
  labels = ["Original", *[s["label"] for s in shortlist]]
  for col, sample in enumerate(entries):
    x = 142 + col * 174
    draw.text((x, 67), sample["label"], font=font(12), fill="black")
    for row, key in enumerate([None, *[s["key"] for s in shortlist]]):
      y = 106 + row * 246
      if col == 0:
        # Split long row captions into compact, readable lines.
        parts = labels[row].split(" / ")
        for j, part in enumerate(parts):
          draw.text((10, y + 30 + j * 22), part, font=font(14), fill="black")
      portrait = sources[sample["id"]] if key is None else read_variant(sample["id"], key)
      tile(summary, (x, y), portrait)
  summary.save(output_path("comparisons/shortlist.png"))
  chosen = [
    CONFIG["preferred"],
    {"id": "P0", "key": "r104x140_c256_none", "label": "Control / 104x140 / 256c / none"},
    shortlist[1],
  ]
  preferred, pdraw = canvas(1190, 1110, "SELECTED / 104x140 / 256 colors / Floyd-Steinberg / six subjects")
  for col, sample in enumerate(entries):
    x = 142 + col * 174
    pdraw.text((x, 67), sample["label"], font=font(12), fill="black")
    for row, candidate in enumerate([None, *chosen]):
      y = 106 + row * 246
      if col == 0:
        label = "Original" if candidate is None else candidate["label"]
        for j, part in enumerate(label.split(" / ")):
          pdraw.text((10, y + 30 + j * 22), part, font=font(14), fill="black")
      tile(preferred, (x, y), sources[sample["id"]] if candidate is None else read_variant(sample["id"], candidate["key"]))
  preferred.save(output_path("comparisons/preferred.png"))
  preferred.crop((0, 0, 1190, 586)).save(output_path("comparisons/preferred_pair.png"))
  columns = [(256, "none"), (256, "fs"), (64, "none"), (64, "fs"), (32, "none"), (32, "fs")]
  for sample in entries:
    sid = sample["id"]
    image, draw = canvas(1320, 850, f"{sample['label']} / resolution x color budget x dithering")
    draw.text((106, 67), "Original", font=font(13), fill="black")
    for col, (colors, dither) in enumerate(columns, 1):
      draw.text((106 + col * 172, 67), f"{colors}c / {dither.upper()}", font=font(13), fill="black")
    for row, (width, height) in enumerate(CONFIG["sizes"]):
      y = 100 + row * 246
      draw.text((8, y + 80), f"{width}x{height}", font=font(13), fill="black")
      tile(image, (106, y), sources[sid])
      for col, (colors, dither) in enumerate(columns, 1):
        key = f"r{width}x{height}_c{colors:03d}_{dither}"
        tile(image, (106 + col * 172, y), read_variant(sid, key))
    image.save(output_path(f"comparisons/{sid}_matrix.png"))
    enlarged, edraw = canvas(1470, 525, f"{sample['label']} / face crops / exact 3x nearest-neighbor")
    for col, candidate in enumerate([None, *shortlist]):
      portrait = sources[sid] if candidate is None else read_variant(sid, candidate["key"])
      key = "original" if candidate is None else candidate["id"]
      portrait.resize((624, 840), RESAMPLE.NEAREST).save(output_path(f"enlarged/{sid}/{key}_4x.png"))
      crop = portrait.crop(tuple(sample["face_box"]))
      crop = crop.resize((crop.width * 3, crop.height * 3), RESAMPLE.NEAREST)
      edraw.text((14 + col * 365, 70), "Original" if candidate is None else candidate["label"], font=font(12), fill="black")
      tile(enlarged, (14 + col * 365, 110), crop)
    enlarged.save(output_path(f"comparisons/{sid}_face_3x.png"))
    chosen_face, fdraw = canvas(1470, 525, f"{sample['label']} / selected 256c FS + controls / exact 3x face crops")
    for col, candidate in enumerate([None, *chosen]):
      portrait = sources[sid] if candidate is None else read_variant(sid, candidate["key"])
      crop = portrait.crop(tuple(sample["face_box"]))
      crop = crop.resize((crop.width * 3, crop.height * 3), RESAMPLE.NEAREST)
      fdraw.text((14 + col * 365, 70), "Original" if candidate is None else candidate["label"], font=font(12), fill="black")
      tile(chosen_face, (14 + col * 365, 110), crop)
    chosen_face.save(output_path(f"comparisons/{sid}_preferred_face_3x.png"))
    read_variant(sid, CONFIG["preferred"]["key"]).resize((624, 840), RESAMPLE.NEAREST).save(output_path(f"enlarged/{sid}/P_4x.png"))
  controls, draw = canvas(1020, 1600, "CONTROLS / spatial reduction only vs palette reduction only")
  headers = ["Original RGB", "104x140 RGB", "78x105 RGB", "52x70 RGB", "156x210 / 64c"]
  for col, title in enumerate(headers):
    draw.text((142 + col * 174, 67), title, font=font(12), fill="black")
  for row, sample in enumerate(entries):
    sid = sample["id"]
    y = 105 + row * 246
    draw.text((10, y + 75), sid, font=font(13), fill="black")
    for col, key in enumerate([None, "r104x140_rgb", "r78x105_rgb", "r52x70_rgb", "r156x210_c064_none"]):
      tile(controls, (142 + col * 174, y), sources[sid] if key is None else read_variant(sid, key))
  controls.save(output_path("comparisons/controls.png"))
  small, draw = canvas(1190, 690, "APPROXIMATE UI SCALES / each cell: original, A, B, C / bilinear sampling")
  for col, sample in enumerate(entries):
    x = 12 + col * 196
    draw.text((x, 67), sample["label"], font=font(12), fill="black")
    for row, scale in enumerate([0.55, 0.42]):
      y = 110 + row * 310
      draw.text((x, y - 18), f"scale {scale} (approx.)", font=font(12), fill="black")
      size = tuple(round(v * scale) for v in NATIVE)
      for i, candidate in enumerate([None, *shortlist]):
        portrait = sources[sample["id"]] if candidate is None else read_variant(sample["id"], candidate["key"])
        px = x + (i % 2) * 95
        py = y + (i // 2) * (size[1] + 16)
        tile(small, (px, py), portrait.resize(size, RESAMPLE.BILINEAR))
        draw.text((px, py + size[1] + 2), "Orig" if candidate is None else candidate["id"], font=font(10), fill="black")
  small.save(output_path("comparisons/ui_scales_approx.png"))


def generate() -> None:
  sources = load_sources()
  records = []
  for sid, source in sources.items():
    for spec in specs():
      working, display = make_variant(source, spec)
      key = spec["key"]
      working.save(output_path(f"working/{sid}/{key}.png"))
      display.save(output_path(f"variants/{sid}/{key}.png"))
      records.append({"sample": sid, **spec, "rgb_colors": color_count(display), "alpha_preserved": display.getchannel("A").tobytes() == source.getchannel("A").tobytes(), "rgba_sha256": image_sha(display)})
  manifest = {"environment": {"python": platform.python_version(), "pillow": PILLOW_VERSION}, "config": CONFIG, "variants": records}
  write_json("manifest.json", manifest)
  with output_path("metrics.csv").open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, fieldnames=["sample", "key", "width", "height", "color_budget", "dither", "rgb_colors", "alpha_preserved"], lineterminator="\n")
    writer.writeheader()
    for r in records:
      writer.writerow({"sample": r["sample"], "key": r["key"], "width": r["size"][0], "height": r["size"][1], "color_budget": r["colors"] or "RGB", "dither": r["dither"], "rgb_colors": r["rgb_colors"], "alpha_preserved": r["alpha_preserved"]})
  sheets(sources)
  data = json.dumps({"config": CONFIG, "records": records}, ensure_ascii=False).replace("<", "\\u003c")
  template = (TOOLS / "gallery.html").read_text(encoding="utf-8")
  output_path("index.html").write_text(template.replace("__EXPERIMENT_DATA__", data), encoding="utf-8")
  print(f"GENERATE PASS: {len(records)} variants + working images, six factor matrices, shortlist, face crops, 4x enlargements and offline gallery.")


def check() -> None:
  sources = load_sources()
  manifest = json.loads((OUT / "manifest.json").read_text(encoding="utf-8"))
  # Production application is separately authorized and verified. Original snapshots
  # remain immutable; only the recorded, backed-up replacement hashes are accepted.
  applied_hashes = {}
  batch = OUT / "production/2026-10-29-r104x140_c256_fs"
  if (batch / "manifest.json").exists():
    application = json.loads((batch / "manifest.json").read_text(encoding="utf-8"))
    if application.get("status") == "applied" and application.get("profile", {}).get("key") == CONFIG["preferred"]["key"]:
      for entry in application["entries"]:
        backup = batch / "backup" / entry["path"]
        if sha256(backup.read_bytes()) != entry["before_sha256"]:
          raise ValueError(f"Production original backup changed: {entry['path']}")
        applied_hashes[entry["path"]] = (entry["before_sha256"], entry["after_sha256"])

  def original_or_recorded_production(path: str, before_hash: str) -> bool:
    current = sha256((ROOT / path).read_bytes())
    approved = applied_hashes.get(path)
    return current == before_hash or bool(approved and approved[0] == before_hash and current == approved[1])
  expected = {(sid, spec["key"]) for sid in sources for spec in specs()}
  actual = {(row["sample"], row["key"]) for row in manifest["variants"]}
  failures = []
  if actual != expected or len(manifest["variants"]) != len(expected):
    failures.append("Variant manifest is incomplete or duplicated")
  for row in manifest["variants"]:
    source = sources[row["sample"]]
    work_expected, display_expected = make_variant(source, row)
    for directory, expected_image in [("working", work_expected), ("variants", display_expected)]:
      path = OUT / directory / row["sample"] / f"{row['key']}.png"
      with Image.open(path) as image:
        if image.mode != "RGBA" or image.size != expected_image.size or image.tobytes() != expected_image.tobytes():
          failures.append(f"Pixel/dimension/mode mismatch: {path.relative_to(OUT)}")
    if row["colors"] and color_count(display_expected) > row["colors"]:
      failures.append(f"Color budget exceeded: {row['sample']}/{row['key']}")
    if display_expected.getchannel("A").tobytes() != source.getchannel("A").tobytes():
      failures.append(f"Alpha changed: {row['sample']}/{row['key']}")
    if image_sha(display_expected) != row["rgba_sha256"] or color_count(display_expected) != row["rgb_colors"] or not row["alpha_preserved"]:
      failures.append(f"Manifest/metrics mismatch: {row['sample']}/{row['key']}")
  selected = json.loads((OUT / "source_selection.json").read_text(encoding="utf-8"))["samples"]
  for sample in selected:
    if not original_or_recorded_production(sample["source"], sample["sha256"]):
      failures.append(f"Production source changed since capture: {sample['source']}")
    with Image.open(OUT / f"originals/{sample['id']}.decoded.png") as decoded:
      if image_sha(decoded) != sample["decoded_rgba_sha256"]:
        failures.append(f"Decoded source mismatch: {sample['id']}")
    for category, refs in sample["references"].items():
      for ref in refs:
        lines = (ROOT / ref["file"]).read_text(encoding="utf-8-sig").splitlines()
        if len(lines) < ref["line"] or lines[ref["line"] - 1].split("#", 1)[0].strip() != ref["text"]:
          failures.append(f"Reference drift: {ref['file']}:{ref['line']} ({category})")
  audit_data = json.loads((OUT / "audit/source_audit.json").read_text(encoding="utf-8"))
  portrait_changes = [row["path"] for row in audit_data["images"] if not original_or_recorded_production(row["path"], row["sha256"])]
  recorded_production = sum(1 for row in audit_data["images"] if row["path"] in applied_hashes and sha256((ROOT / row["path"]).read_bytes()) == applied_hashes[row["path"]][1])
  if portrait_changes:
    failures.append(f"Portrait inventory changed since audit: {portrait_changes}")
  # Shared GUI may legitimately change in the other chat. Report drift; never revert it.
  gui_drift = [row["file"] for row in audit_data["gui_snapshot_read_only"] if sha256((ROOT / row["file"]).read_bytes()) != row["sha256"]]
  generator_drift = [path for path, digest in audit_data["existing_generators_read_only"].items() if sha256((ROOT / path).read_bytes()) != digest]
  dither_pairs = 0
  for sid in sources:
    for size in CONFIG["sizes"]:
      for colors in CONFIG["colors"]:
        prefix = f"r{size[0]}x{size[1]}_c{colors:03d}"
        plain = read_variant(sid, prefix + "_none")
        fs = read_variant(sid, prefix + "_fs")
        if plain.tobytes() == fs.tobytes():
          failures.append(f"Dithering produced no difference: {sid}/{prefix}")
        dither_pairs += 1
  for path in (OUT / "comparisons").glob("*.png"):
    with Image.open(path) as image:
      image.verify()
  for sid, source in sources.items():
    for candidate in [None, *CONFIG["shortlist"], CONFIG["preferred"]]:
      key = "original" if candidate is None else candidate["id"]
      expected_image = source if candidate is None else read_variant(sid, candidate["key"])
      with Image.open(OUT / f"enlarged/{sid}/{key}_4x.png") as image:
        if image.tobytes() != expected_image.resize((624, 840), RESAMPLE.NEAREST).tobytes():
          failures.append(f"4x enlargement differs from nearest-neighbor: {sid}/{key}")
  page = (OUT / "index.html").read_text(encoding="utf-8")
  gallery_data = json.dumps({"config": CONFIG, "records": manifest["variants"]}, ensure_ascii=False).replace("<", "\\u003c")
  expected_page = (TOOLS / "gallery.html").read_text(encoding="utf-8").replace("__EXPERIMENT_DATA__", gallery_data)
  if page != expected_page:
    failures.append("Gallery differs from template/manifest; regenerate it")
  local_links = re.findall(r'(?:href|src)="([^"#]+)"', page)
  for link in local_links:
    if ":" in link or link.startswith("/") or not (OUT / link).is_file():
      failures.append(f"Missing or nonlocal HTML reference: {link}")
  if "__EXPERIMENT_DATA__" in page:
    failures.append("Gallery data was not embedded")
  report = {
    "result": "FAIL" if failures else "PASS", "checked_variants": len(expected),
    "checked_working_and_native_pngs": len(expected) * 2, "checked_dither_pairs": dither_pairs,
    "unchanged_portrait_inventory": len(audit_data["images"]) - len(portrait_changes) - recorded_production,
    "recorded_production_portraits": recorded_production,
    "original_snapshots_and_reference_chains": len(selected), "native_alpha": "byte-exact",
    "checked_4x_enlargements": len(sources) * 5, "checked_static_gallery_links": len(local_links),
    "native_dimensions": list(NATIVE), "shared_gui_drift_observed": gui_drift,
    "existing_generator_drift_observed": generator_drift, "failures": failures,
    "actual_game_verification": "NOT RUN; offline previews only",
  }
  write_json("verification.json", report)
  print(json.dumps(report, ensure_ascii=False, indent=2))
  if failures:
    raise SystemExit(1)


def main() -> None:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("command", choices=["audit", "generate", "check", "all"])
  command = parser.parse_args().command
  if command in {"audit", "all"}:
    audit()
  if command in {"generate", "all"}:
    generate()
  if command in {"check", "all"}:
    check()


if __name__ == "__main__":
  main()
