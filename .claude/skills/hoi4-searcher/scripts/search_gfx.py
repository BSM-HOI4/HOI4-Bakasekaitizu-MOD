#!/usr/bin/env python3
"""
HOI4 GFX Searcher - Search for sprite definitions in .gfx files
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class GFXEntry:
    """Represents a single sprite entry in a .gfx file"""
    def __init__(self, name: str, texture_path: str, source_file: str, line_num: int):
        self.name = name
        self.texture_path = texture_path
        self.source_file = source_file
        self.line_num = line_num

    def __repr__(self):
        return f"GFXEntry({self.name}, {self.texture_path})"


class GFXDatabase:
    """Database of all GFX entries parsed from .gfx files"""

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.entries: List[GFXEntry] = []
        self.name_index: Dict[str, GFXEntry] = {}
        self.texture_index: Dict[str, List[GFXEntry]] = {}

    def parse_gfx_file(self, gfx_file: Path) -> int:
        """Parse a single .gfx file and extract sprite definitions"""
        count = 0
        try:
            with open(gfx_file, 'r', encoding='utf-8-sig', errors='ignore') as f:
                content = f.read()

            # Find all SpriteType blocks
            # Pattern matches: SpriteType = { name = ... texturefile = ... }
            sprite_pattern = re.compile(
                r'SpriteType\s*=\s*\{[^}]*?name\s*=\s*([^\s\n]+)[^}]*?texture[fF]ile\s*=\s*"([^"]+)"',
                re.MULTILINE | re.DOTALL
            )

            for match in sprite_pattern.finditer(content):
                name = match.group(1).strip()
                texture_path = match.group(2).strip()

                # Calculate line number
                line_num = content[:match.start()].count('\n') + 1

                entry = GFXEntry(name, texture_path, str(gfx_file), line_num)
                self.entries.append(entry)
                self.name_index[name.lower()] = entry

                # Add to texture index
                texture_key = texture_path.lower()
                if texture_key not in self.texture_index:
                    self.texture_index[texture_key] = []
                self.texture_index[texture_key].append(entry)

                count += 1

        except Exception as e:
            print(f"⚠️  Error parsing {gfx_file}: {e}", file=sys.stderr)

        return count

    def scan_directory(self, interface_dir: Optional[Path] = None) -> int:
        """Scan directory for .gfx files and parse them"""
        if interface_dir is None:
            interface_dir = self.base_path / "interface"

        if not interface_dir.exists():
            print(f"❌ Interface directory not found: {interface_dir}", file=sys.stderr)
            return 0

        total_count = 0
        gfx_files = list(interface_dir.rglob("*.gfx"))

        print(f"🔍 Scanning {len(gfx_files)} .gfx files in {interface_dir}...", file=sys.stderr)

        for gfx_file in gfx_files:
            count = self.parse_gfx_file(gfx_file)
            total_count += count

        print(f"✅ Parsed {total_count} sprite entries from {len(gfx_files)} files\n", file=sys.stderr)
        return total_count

    def search_by_id(self, query: str, exact: bool = False) -> List[GFXEntry]:
        """Search for sprites by ID/name"""
        query_lower = query.lower()

        if exact:
            entry = self.name_index.get(query_lower)
            return [entry] if entry else []
        else:
            # Partial match
            results = []
            for name, entry in self.name_index.items():
                if query_lower in name:
                    results.append(entry)
            return results

    def search_by_path(self, query: str, exact: bool = False) -> List[GFXEntry]:
        """Search for sprites by texture path"""
        query_lower = query.lower()
        results = []

        if exact:
            return self.texture_index.get(query_lower, [])
        else:
            # Partial match on path
            for texture_path, entries in self.texture_index.items():
                if query_lower in texture_path:
                    results.extend(entries)
            return results

    def check_file_exists(self, entry: GFXEntry) -> Tuple[bool, Optional[Path]]:
        """Check if the texture file actually exists"""
        # Try relative to base path
        texture_path = Path(entry.texture_path)

        # HOI4 uses paths like "gfx/interface/ideas/..."
        full_path = self.base_path / texture_path

        if full_path.exists():
            return True, full_path

        # Try common variations
        for ext in ['.dds', '.tga', '.png', '.jpg']:
            test_path = full_path.with_suffix(ext)
            if test_path.exists():
                return True, test_path

        return False, None


def format_result(entry: GFXEntry, db: GFXDatabase, show_image: bool = False) -> str:
    """Format a search result for display"""
    exists, actual_path = db.check_file_exists(entry)

    result = []
    result.append(f"📋 ID: {entry.name}")
    result.append(f"   Path: {entry.texture_path}")
    result.append(f"   Defined in: {entry.source_file}:{entry.line_num}")

    if exists:
        result.append(f"   ✅ File exists: {actual_path}")
    else:
        result.append(f"   ❌ File NOT found")

    return "\n".join(result)


def main():
    parser = argparse.ArgumentParser(
        description="Search for HOI4 GFX sprite definitions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search by ID (partial match)
  %(prog)s --id JAP_industrial

  # Search by exact ID
  %(prog)s --id GFX_idea_JAP_industrial_standard --exact

  # Search by texture path
  %(prog)s --path idea_JAP_night_vision.png

  # Search in specific mod directory
  %(prog)s --id JAP_sea --base ~/HOI4_modding/Empire-of-Breakwaters
        """
    )

    parser.add_argument('--base', '-b', type=str,
                        help='Base directory of the mod (default: current directory)')
    parser.add_argument('--interface', '-i', type=str,
                        help='Interface directory path (default: <base>/interface)')
    parser.add_argument('--id', type=str,
                        help='Search by sprite ID/name')
    parser.add_argument('--path', '-p', type=str,
                        help='Search by texture file path')
    parser.add_argument('--exact', '-e', action='store_true',
                        help='Use exact match instead of partial match')
    parser.add_argument('--show-image', action='store_true',
                        help='Display image path for viewing')
    parser.add_argument('--limit', '-l', type=int, default=50,
                        help='Maximum number of results to show (default: 50)')

    args = parser.parse_args()

    # Determine base path
    if args.base:
        base_path = Path(args.base).expanduser().resolve()
    else:
        base_path = Path.cwd()

    if not base_path.exists():
        print(f"❌ Base path does not exist: {base_path}", file=sys.stderr)
        sys.exit(1)

    # Initialize database
    db = GFXDatabase(base_path)

    # Determine interface directory
    if args.interface:
        interface_dir = Path(args.interface).expanduser().resolve()
    else:
        interface_dir = base_path / "interface"

    # Scan files
    total_entries = db.scan_directory(interface_dir)

    if total_entries == 0:
        print("❌ No sprite entries found. Check the base/interface directory.", file=sys.stderr)
        sys.exit(1)

    # Perform search
    results = []

    if args.id:
        results = db.search_by_id(args.id, exact=args.exact)
        search_term = f"ID: {args.id}"
    elif args.path:
        results = db.search_by_path(args.path, exact=args.exact)
        search_term = f"Path: {args.path}"
    else:
        print("❌ Please specify either --id or --path for search", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    # Display results
    if not results:
        print(f"\n❌ No results found for {search_term}")
        sys.exit(0)

    print(f"🔎 Found {len(results)} result(s) for {search_term}")
    print(f"{'=' * 70}\n")

    for i, entry in enumerate(results[:args.limit], 1):
        print(f"Result {i}:")
        print(format_result(entry, db, args.show_image))
        print()

    if len(results) > args.limit:
        print(f"... and {len(results) - args.limit} more results (use --limit to show more)")


if __name__ == "__main__":
    main()
