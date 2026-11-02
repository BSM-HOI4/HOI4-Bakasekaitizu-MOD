#!/usr/bin/env python3
"""Verify native control contracts and exact pictograms for the military finish."""
import argparse
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw
import generate_win95_major_gui as g


def verify(destination):
    config = json.loads((g.CONFIG / 'military_controls_finish.json').read_text())
    records = json.loads(g.MANIFEST.read_text())['sprites']
    game = g.game_directory()
    definitions, _, _ = g.definitions(game)
    checks = 0
    previews = []
    for name in config['sprites']:
        record = records[name]
        source = Image.open(g.source_image(definitions[name], game, record['source'])).convert('RGBA')
        actual = Image.open(g.MOD / record['texture']).convert('RGBA')
        assert actual.size == source.size, (name, 'native dimensions')
        assert record['frames'] == int(g.value(definitions[name]['text'], definitions[name]['node'], 'noOfFrames', '1')), (name, 'native frames')
        checks += 2
        for region in config.get('preserve_regions', {}).get(name, []):
            box = region['source']
            x, y = region['position']
            output = (x, y, x + box[2] - box[0], y + box[3] - box[1])
            if region.get('mode') == 'pictogram':
                pairs = zip(actual.crop(output).getdata(), source.crop(box).getdata())
                retained = 0
                for result, original in pairs:
                    r, green, b, alpha = original
                    if alpha == 255 and (max(r, green, b) >= 105 or (max(r, green, b) > 60 and max(r, green, b) - min(r, green, b) > 25)):
                        assert result == original, (name, 'foreground RGB retained')
                        retained += 1
                # Base/button-face atlases have no baked pictogram: their glyph
                # is a separate GUI sprite. An empty foreground is intentional.
            else:
                assert actual.crop(output).tobytes() == source.crop(box).tobytes(), (name, 'pictogram pixels')
            checks += 1
        frames = record['frames']
        fw = actual.width // frames
        for a in range(frames):
            for b in range(a + 1, frames):
                boxes = [(i * fw, 0, (i + 1) * fw, actual.height) for i in (a, b)]
                if source.crop(boxes[0]).tobytes() != source.crop(boxes[1]).tobytes():
                    assert actual.crop(boxes[0]).tobytes() != actual.crop(boxes[1]).tobytes(), (name, 'distinct states', a, b)
                    checks += 1
        previews.append((name, actual.crop((0, 0, fw, actual.height))))

    # C++ control names, callbacks, bounds and tooltips must stay byte-token equivalent.
    for filename in ['naviesview.gui', 'theatreselector.gui', 'strategicairview.gui', 'leadergroups.gui', 'mapmodes_interface.gui']:
        path = g.MOD / 'interface/replace' / filename
        relative = str(path.relative_to(g.ROOT))
        previous = subprocess.run(['git', 'show', 'HEAD:' + relative], cwd=g.ROOT, capture_output=True, text=True)
        before = previous.stdout if previous.returncode == 0 else g.read(game / 'interface' / filename)
        assert g.contract(g.read(path)) == g.contract(before), (filename, 'native widget/callback/layout contract')
        checks += 1

    # Asset sheet only; it does not substitute for a runtime screenshot.
    destination.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1000, len(previews) * 80), '#008080')
    draw = ImageDraw.Draw(sheet)
    for i, (name, preview) in enumerate(previews):
        preview.thumbnail((490, 72))
        draw.text((8, i * 80 + 8), name, fill='white')
        sheet.paste(preview, (500, i * 80 + 4), preview)
    sheet.save(destination / 'military-controls-assets.png')
    result = dict(checks=checks, textures=len(previews), runtime_verified=False)
    (destination / 'checks.json').write_text(json.dumps(result, indent=2) + '\n')
    print(f'PASS: {checks} checks, {len(previews)} textures; native contracts and pictograms preserved')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    verify(parser.parse_args().output)
