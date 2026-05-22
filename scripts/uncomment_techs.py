import re
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
file_path = repo_root / "bakasekai" / "common" / "scripted_effects" / "_bsm_fallen_empire_effects.txt"

with open(file_path, 'r') as f:
    lines = f.readlines()

new_lines = []
in_tech_block = False

for line in lines:
    if "bsm_fallen_empire_unlock_tech = {" in line:
        in_tech_block = True
        new_lines.append(line)
        continue
    
    if in_tech_block and "}" in line and line.strip() == "}":
        in_tech_block = False
        new_lines.append(line)
        continue

    if in_tech_block:
        # Uncomment lines that start with optional whitespace and #
        # But keep the indentation
        # The file has "  #   tech = 1" format
        # We want "    tech = 1"
        stripped = line.strip()
        if stripped.startswith("#"):
            # Remove the first # and any following whitespace, but keep the initial indentation of the line if possible
            # Actually, let's just replace "  #   " with "    " or similar
            # Regex to match "#" and surrounding whitespace
            # The lines look like: "  #   BEL_chasseurs_ardennais = 1"
            # We want: "    BEL_chasseurs_ardennais = 1"
            
            # Simple approach: remove all # characters
            cleaned_line = line.replace("#", "")
            # Ensure it's not just empty or whitespace
            if cleaned_line.strip():
                new_lines.append(cleaned_line)
            else:
                new_lines.append(line) # Keep empty lines if they were just comments? No, probably not.
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(file_path, 'w') as f:
    f.writelines(new_lines)
