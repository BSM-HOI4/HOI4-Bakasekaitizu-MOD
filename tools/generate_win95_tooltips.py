#!/usr/bin/env python3
"""Generate classic pale-yellow tooltip tiles and pair them with the native black font."""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw
from win95_gui_lib import nodes, value, prop, replacements

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'bakasekai'
CORE = MOD / 'interface/replace/core.gfx'
OUT = MOD / 'gfx/interface/win95/tooltips'


def run(check):
    text = CORE.read_text(encoding='utf-8-sig')
    specs = {'ToolTip': (64, 64), 'GFX_mini_tooltip': (32, 32)}
    # Keep each native tile's actual dimensions instead of assuming a platform's install.
    old = json.loads((OUT / 'manifest.json').read_text()) if (OUT / 'manifest.json').exists() else {}
    edits, records = [], {}
    for node in nodes(text):
        name = value(text, node, 'name')
        if name in specs:
            texture = prop(text, node, 'texturefile')
            original = old.get(name, {}).get('source', texture[0])
            from win95_gui_lib import game_directory
            source = None
            relative = Path(original.replace('//', '/'))
            for base in (MOD, game_directory()):
                candidate = base / relative
                if candidate.exists():
                    source = candidate
                    break
                if candidate.with_suffix('.dds').exists():
                    source = candidate.with_suffix('.dds')
                    break
            if source is None:
                raise ValueError(f'Missing original tooltip tile: {original}')
            with Image.open(source) as source_image:
                size = source_image.size
            image = Image.new('RGBA', size, '#ffffe1')
            draw = ImageDraw.Draw(image)
            draw.rectangle((0, 0, size[0] - 1, size[1] - 1), outline='#000000')
            destination = OUT / (name + '.png')
            reference = destination.relative_to(MOD).as_posix()
            records[name] = dict(source=original, texture=reference, size=list(size))
            if check:
                with Image.open(destination) as actual:
                    assert actual.mode == 'RGBA' and actual.size == size and actual.tobytes() == image.tobytes(), name
                assert texture[0] == reference
            else:
                OUT.mkdir(parents=True, exist_ok=True)
                image.save(destination)
            edits.append((texture[1], texture[2], reference))
        elif name == 'ToolTip_Font' and node.key.lower() == 'bitmapfont':
            color = prop(text, node, 'color')
            if check:
                assert color[0].lower() == '0xff000000'
            edits.append((color[1], color[2], '0xff000000'))
    assert set(records) == set(specs)
    updated = replacements(text, edits)
    if check:
        assert updated == text and old == records
    else:
        CORE.write_text(updated, encoding='utf-8')
        (OUT / 'manifest.json').write_text(json.dumps(records, indent=2) + '\n')
    print('PASS: 2 pale-yellow tooltip tiles; original dimensions and native font metrics retained')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    run(parser.parse_args().check)
