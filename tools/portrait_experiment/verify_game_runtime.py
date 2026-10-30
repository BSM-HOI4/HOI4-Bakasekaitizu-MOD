#!/usr/bin/env python3
"""Start one isolated local HOI4 verification; no normal settings/save/playset writes."""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "documents/portrait_experiment/production/2026-10-29-r104x140_c256_fs"
GAME = Path("/Users/eightman/Library/Application Support/Steam/steamapps/common/Hearts of Iron IV")
BINARY = GAME / "hoi4.app/Contents/MacOS/hoi4"
BASE_SETTINGS = Path(__file__).with_name("runtime_settings.txt")


def main() -> None:
  processes = subprocess.run(["ps", "-axo", "pid=,comm="], text=True, capture_output=True, check=True).stdout
  if any(line.strip().endswith("/MacOS/hoi4") for line in processes.splitlines()):
    raise SystemExit("An existing HOI4 process is running; leave it untouched and skip isolated launch.")
  if not BINARY.is_file() or not BASE_SETTINGS.is_file():
    raise SystemExit("Installed game or isolated test settings template unavailable; no launch performed.")
  userdir = Path(tempfile.mkdtemp(prefix="bsm-portrait-production-"))
  settings = BASE_SETTINGS.read_text(encoding="utf-8-sig")
  settings = re.sub(r"size=\{ x=1024 y=768 \}", "size={ x=1280 y=720 }", settings, count=1)
  settings = settings.replace("gui_scale=0.800000", "gui_scale=1.000000")
  settings = settings.replace("telemetry_enabled=yes", "telemetry_enabled=no").replace("save_career_to_cloud=yes", "save_career_to_cloud=no")
  settings = re.sub(r"(?m)^master_volume=.*$", "master_volume=0.000000", settings)
  settings = re.sub(r"(?m)^music_volume=.*$", "music_volume=0.000000", settings)
  (userdir / "settings.txt").write_text(settings, encoding="utf-8")
  (userdir / "mod").mkdir()
  descriptor = (ROOT / "bakasekai/descriptor.mod").read_text(encoding="utf-8-sig")
  (userdir / "mod/bsm_local.mod").write_text(descriptor + f'\npath="{ROOT / "bakasekai"}"\n', encoding="utf-8")
  (userdir / "dlc_load.json").write_text(json.dumps({"disabled_dlcs": [], "enabled_mods": ["mod/bsm_local.mod"]}), encoding="utf-8")
  command = [str(BINARY), "-debug", f"-userdir={userdir}"]
  with (userdir / "launch.log").open("wb") as log:
    process = subprocess.Popen(command, cwd=GAME, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
  record = {"pid": process.pid, "userdir": str(userdir), "command": command, "normal_user_settings_or_saves_used": False, "credentials_copied": False, "runtime_state_stored_in_repository": False}
  (OUTPUT / "runtime_launch.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
  print(json.dumps(record, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
  main()
