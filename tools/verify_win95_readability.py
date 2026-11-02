#!/usr/bin/env python3
"""Check screenshot-driven contrast, layouts and complete Win95 components."""
import argparse
from collections import Counter
import json
from pathlib import Path

from PIL import Image
import generate_win95_major_gui as g


def verify(before):
    configs = [json.loads((g.CONFIG / name).read_text()) for name in
               ['readability_finish.json', 'components95_finish.json']]
    definitions, fonts, _ = g.definitions(g.game_directory())
    records = json.loads(g.MANIFEST.read_text())['sprites']
    checks = 0

    def check(result, message):
        nonlocal checks
        assert result, message
        checks += 1

    for config in configs:
        for item in config['font_overrides']:
            for path in g.active_guis([item['gui']], g.game_directory()):
                text = g.read(path)
                matched = 0
                for node in g.nodes(text):
                    root, parts = node, []
                    while root.parent and root.parent.key.lower() != 'guitypes':
                        parts.append(g.value(text, root, 'name', root.key))
                        root = root.parent
                    if g.value(text, root, 'name') != item['root'] or g.value(text, node, 'name') != item['widget']:
                        continue
                    if item.get('path') and item['path'] != '/'.join(reversed(parts)):
                        continue
                    actual = g.value(text, node, 'font') or g.value(text, node, 'buttonFont')
                    expected = g.font_name(item['source'], item['shade'])
                    check(actual == expected, (path.name, item, actual, expected))
                    check(item['source'] in fonts, ('Native glyph source exists', item['source']))
                    matched += 1
                check(matched > 0, ('Contrast rule binds a real widget', path, item))
        for name in config['sprites']:
            record = records[name]
            source = Image.open(g.source_image(definitions[name], g.game_directory(), record['source'])).convert('RGBA')
            actual = Image.open(g.MOD / record['texture']).convert('RGBA')
            check(actual.size == source.size, (name, 'dimensions'))
            check(record['frames'] == int(g.value(definitions[name]['text'], definitions[name]['node'], 'noOfFrames', '1')), (name, 'frame mapping'))
            fw = actual.width // record['frames']
            for a in range(record['frames']):
                for b in range(a + 1, record['frames']):
                    boxes = [(i * fw, 0, (i + 1) * fw, actual.height) for i in (a, b)]
                    if source.crop(boxes[0]).tobytes() != source.crop(boxes[1]).tobytes():
                        check(actual.crop(boxes[0]).tobytes() != actual.crop(boxes[1]).tobytes(), (name, 'distinct states', a, b))

    for old in before.rglob('*.gui'):
        current = g.MOD / 'interface' / old.relative_to(before)
        left, right = g.read(old), g.read(current)
        identity = lambda t: Counter((n.key.lower(), g.value(t, n, 'name')) for n in g.nodes(t))
        check(identity(left) == identity(right), (current.name, 'control IDs and types'))
        for key in ['clicksound', 'shortcut', 'pdx_tooltip', 'tooltip', 'buttonText', 'text']:
            values = lambda t: Counter(g.value(t, n, key) for n in g.nodes(t) if g.value(t, n, key) is not None)
            check(values(left) == values(right), (current.name, key))
    text = g.read(g.MOD / 'interface/replace/countryintelligenceagencyview.gui')
    for node in g.nodes(text):
        if g.value(text, node, 'name') == 'progressbar_days' and g.value(text, node, 'maxWidth') == '74':
            check(g.value(text, node, 'multiline') == 'no' and g.value(text, node, 'maxHeight') == '20', 'Agency ready/day text stays on one line')
    print(f'PASS: {checks} checks; contrast, state distinctions and native control IDs retained')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--before', type=Path, required=True)
    verify(parser.parse_args().before)
