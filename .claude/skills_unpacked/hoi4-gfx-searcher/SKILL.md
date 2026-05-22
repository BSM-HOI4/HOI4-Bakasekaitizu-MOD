---
name: hoi4-gfx-searcher
description: Search and locate Hearts of Iron 4 sprite definitions in .gfx files. Use when working with HOI4 mods and needing to (1) Find which .gfx file defines a sprite ID, (2) Locate the texture file path for an idea/event/GUI element, (3) Reverse-lookup which sprite IDs use a specific image file, (4) Verify if image files actually exist in the mod directory. Triggers on queries like "What image does GFX_idea_X use?", "Where is X.png defined?", "Show me the idea image for Y", or "Does this texture file exist?"
---

# HOI4 GFX Searcher

## Overview

Search Hearts of Iron 4 `.gfx` sprite definitions to quickly find sprite IDs, texture paths, and verify file existence. Essential for HOI4 mod development when working with ideas, events, decisions, and GUI elements.

## Quick Start

The skill provides a Python script that parses all `.gfx` files in a mod's `interface/` directory and enables fast searching.

**Basic usage pattern:**
1. Run the search script with the mod's base directory
2. Search by sprite ID or texture path
3. View results with file locations and existence checks

## Search by Sprite ID

Find texture paths and definitions for sprite IDs (like `GFX_idea_JAP_industrial_standard`).

```bash
python3 scripts/search_gfx.py --base ~/path/to/mod --id <sprite_name>
```

**Examples:**

```bash
# Partial match (finds all sprites containing "JAP_sea")
python3 scripts/search_gfx.py --base ~/HOI4_modding/Empire-of-Breakwaters --id JAP_sea

# Exact match
python3 scripts/search_gfx.py --base ~/HOI4_modding/Empire-of-Breakwaters --id GFX_idea_JAP_sea_power --exact
```

**Output includes:**
- Sprite ID (name)
- Texture file path
- Source .gfx file and line number
- File existence check (✅ found / ❌ missing)

## Reverse Lookup by Texture Path

Find which sprite IDs reference a specific image file.

```bash
python3 scripts/search_gfx.py --base ~/path/to/mod --path <filename_or_path>
```

**Examples:**

```bash
# Find all sprites using images with "night_vision" in the path
python3 scripts/search_gfx.py --base ~/HOI4_modding/Empire-of-Breakwaters --path night_vision

# Search for specific file
python3 scripts/search_gfx.py --base ~/HOI4_modding/Empire-of-Breakwaters --path idea_JAP_night_vision.png
```

**Use cases:**
- "Which sprite IDs use this image?"
- "Is this PNG file actually referenced anywhere?"
- "Find all ideas using images in a specific directory"

## File Existence Verification

The script automatically checks if texture files exist and tries common extensions (.dds, .tga, .png, .jpg).

**Status indicators:**
- ✅ **File exists**: Shows actual path found
- ❌ **File NOT found**: Texture path is defined but file is missing

This helps identify:
- Missing texture files
- Broken references
- Files with different extensions than specified

## Command Options

```bash
--base, -b <path>       # Mod base directory (default: current directory)
--interface, -i <path>  # Interface directory (default: <base>/interface)
--id <name>            # Search by sprite ID/name
--path, -p <path>      # Search by texture file path
--exact, -e            # Use exact match instead of partial match
--limit, -l <number>   # Maximum results to show (default: 50)
```

## Workflow Examples

### "What image does this idea use?"

User asks: *"What's the image for the JAP_industrial_standard idea?"*

```bash
python3 scripts/search_gfx.py --base ~/HOI4_modding/Empire-of-Breakwaters --id JAP_industrial
```

Expected output shows the texture path and whether the file exists.

### "Is this PNG file implemented?"

User asks: *"Is night_vision.png actually being used in the mod?"*

```bash
python3 scripts/search_gfx.py --base ~/HOI4_modding/Empire-of-Breakwaters --path night_vision.png
```

Shows all sprite IDs referencing that file, or none if unused.

### "Show me all idea images for Japan"

User asks: *"Show me all JAP idea images"*

```bash
python3 scripts/search_gfx.py --base ~/HOI4_modding/Empire-of-Breakwaters --id JAP_idea --limit 100
```

Lists all matching sprites with their texture paths.

## Understanding .gfx File Format

HOI4 `.gfx` files define sprites using this structure:

```
spriteTypes = {
    SpriteType = {
        name = GFX_idea_JAP_industrial_standard
        texturefile = "gfx/interface/ideas/idea_JAP_industrial_standard.png"
    }
    SpriteType = {
        name = GFX_idea_JAP_night_vision
        texturefile = "gfx/interface/ideas/idea_JAP_night_vision.png"
    }
}
```

**Key points:**
- `name` is the sprite ID referenced in code/definitions
- `texturefile` (or `textureFile`) is the image path relative to mod root
- Multiple `.gfx` files can exist in `interface/` and subdirectories
- The script automatically scans all `.gfx` files recursively

## Notes

- The script caches nothing; each run re-parses all `.gfx` files
- Texture paths are case-sensitive on Linux/macOS but not on Windows
- HOI4 supports .dds, .tga, .png, and .jpg formats
- The script tries common extensions if the specified one doesn't exist
