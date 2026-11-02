#!/usr/bin/env python3
"""Check Decision chrome, engine widget contracts, and text-column separation."""
import argparse
from collections import Counter
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import generate_win95_major_gui as g
from win95_materials import bevel


def verify(before, output):
    config = json.loads((g.CONFIG / 'decision_finish.json').read_text())
    manifest = json.loads(g.MANIFEST.read_text())
    records = manifest['sprites']
    old = json.loads((before / 'bakasekai/gfx/interface/win95/major/manifest.json').read_text())['sprites']
    relative = 'bakasekai/interface/replace/countrydecisionview.gui'
    current = g.read(g.ROOT / relative)
    prior = g.read(before / relative)
    ast = g.nodes(current)
    checks = []

    def check(condition, message):
        if not condition:
            raise AssertionError(message)
        checks.append(message)

    def root(node, text=current):
        while node.parent and node.parent.key.lower() != 'guitypes':
            node = node.parent
        return g.value(text, node, 'name')

    def widget(r, name):
        return next(n for n in ast if root(n) == r and g.value(current, n, 'name') == name)

    def rect(r, name):
        n = widget(r, name)
        x, y = g.pair(current, n, 'position')
        return x, y, int(g.value(current, n, 'maxWidth')), int(g.value(current, n, 'maxHeight'))

    def identities(text):
        return Counter((root(n, text), n.key.lower(), name) for n in g.nodes(text) if (name := g.value(text, n, 'name')))

    check(identities(current) == identities(prior), 'All native widget types and IDs retained')
    for key in ['clicksound', 'show_sound', 'hide_sound', 'pdx_tooltip', 'shortcut', 'frame']:
        def values(text):
            return Counter((root(n, text), g.value(text, n, 'name'), v)
                           for n in g.nodes(text) if (v := g.value(text, n, key)) is not None)
        check(values(current) == values(prior), f'Native {key} bindings retained')
    for n in g.nodes(prior):
        if n.parent and n.parent.key.lower() == 'guitypes':
            rn = g.value(prior, n, 'name')
            now = widget(rn, rn)
            check(g.pair(current, now, 'size', 'width', 'height') == g.pair(prior, n, 'size', 'width', 'height'),
                  f'{rn}: native engine-sized root dimensions retained')
    changed = {name for name, data in records.items() if old.get(name, {}).get('sha256') != data['sha256']}
    check(changed == set(config['material_profiles']), 'Only the four reviewed Decision textures changed')
    game = g.game_directory()
    definitions, _, _ = g.definitions(game)
    images = {}

    def image(name):
        if name not in images:
            if name in records:
                images[name] = Image.open(g.MOD / records[name]['texture']).convert('RGBA')
            else:
                images[name] = Image.open(g.source_image(definitions[name], game)).convert('RGBA')
        return images[name]

    for name in config['material_profiles']:
        data, im = records[name], image(name)
        definition = definitions[name]
        native = Image.open(g.source_image(definition, game, data['source']))
        check(im.size == native.size, f'{name}: original image dimensions retained')
        check(data['frames'] == int(g.value(definition['text'], definition['node'], 'noOfFrames', '1')), f'{name}: native frame count retained')
        check(data['material_profile'] == config['material_profiles'][name], f'{name}: explicit profile recorded')
    header = image('GFX_event_header_bg')
    check(header.getchannel('A').crop((0, 4, 515, 74)).getextrema() == (255, 255), 'Event settings panel has four complete edges')
    for box in [(0, 0, 515, 4), (0, 74, 515, 83)]:
        check(header.getchannel('A').crop(box).getextrema() == (0, 0), 'Native header spacing remains transparent')
    main_pos = g.pair(current, widget('countrydecisionview', 'production_header_bg'), 'position')
    grid_pos = g.pair(current, widget('countrydecisionview', 'decision_grid_container'), 'position')
    check(grid_pos[1] + header.getbbox()[1] >= main_pos[1] + image('GFX_header_bg').height,
          'Event settings panel does not paint over main title bar')
    for name in ['GFX_category_header_bg', 'GFX_event_item_bg', 'GFX_decision_item_bg']:
        check(image(name).getchannel('A').getextrema() == (255, 255), f'{name}: no leftover ornamental alpha')
    row = image('GFX_decision_item_bg')
    states = [row.crop((i * 512, 0, (i + 1) * 512, 40)).tobytes() for i in range(3)]
    check(len(set(states)) == 3, 'Neutral, green, and red Decision states stay distinct')
    check(row.getpixel((512 + 4, 20))[:3] == (0, 128, 0), 'Green state has a visible status stripe')
    check(row.getpixel((1024 + 4, 10))[:3] == (176, 0, 0), 'Red state has a visible warning stripe')
    check(row.getpixel((1024 + 6, 19))[:3] == (255, 255, 255), 'Red warning gutter includes a contrasting cross')
    for rn, fields in [('event_item', ['name_text', 'timer_text']), ('decision_item', ['name_text', 'cost_and_timer_text']),
                       ('targeted_decision_item', ['name_text', 'cost_and_timer_text', 'timer_text']),
                       ('timed_decision_item', ['name_text', 'cost_and_timer_text', 'timer_text'])]:
        boxes = [rect(rn, name) for name in fields]
        for a, b in zip(boxes, boxes[1:]):
            check(a[0] + a[2] <= b[0], f'{rn}: text columns do not overlap')
        for name, box in zip(fields, boxes):
            check(box[1] + box[3] <= (33 if rn == 'event_item' else 40), f'{rn}/{name}: text fits its row height')
            check(g.value(current, widget(rn, name), 'font').endswith('__black'), f'{rn}/{name}: dark glyphs on light background')
            if rn != 'event_item':
                progress_y = g.pair(current, widget(rn, 'btn_progress_good'), 'position')[1]
                check(box[1] + box[3] <= progress_y, f'{rn}/{name}: text clears the progress lane')
    for rn in ['event_header', 'category_header']:
        check(g.value(current, widget(rn, 'name_text'), 'font') == 'bsm_w95_gui__hoi_20bs__white', f'{rn}: white glyph family on navy heading')
    for group_name, label_name in [('event_checkbox_window', 'events_popup_text'),
                                   ('news_checkbox_window', 'news_popup_text'),
                                   ('minor_event_checkbox_window', 'minor_events_popup_text')]:
        group = widget('event_header', group_name)
        label = widget('event_header', label_name)
        gx, gy = g.pair(current, group, 'position')
        lx, ly, lw, lh = rect('event_header', label_name)
        check(gx + lx + lw <= header.width and gy + ly + lh <= 74, f'{group_name}: label fits the settings panel')
        expected = {'events_popup_text': 'BSM_W95_DECISION_POPUP_EVENTS',
                    'news_popup_text': 'BSM_W95_DECISION_POPUP_NEWS',
                    'minor_events_popup_text': 'BSM_W95_DECISION_POPUP_MINOR'}[label_name]
        check(g.value(current, label, 'text') == expected, f'{label_name}: valid localisation key scalar')
    for language in ['japanese', 'english']:
        p = g.MOD / f'localisation/{language}/_bsm_win95_decisions_l_{language}.yml'
        check(p.read_bytes().startswith(b'\xef\xbb\xbf'), f'{language}: localisation has UTF-8 BOM')
        keys = [s.split(':')[0].strip() for s in g.read(p).splitlines() if ':0 ' in s]
        check(len(keys) == len(set(keys)) == 3, f'{language}: three unique popup label keys')

    # Composition for visual inspection. Sample labels use a preview font; this
    # is deliberately labelled separately from native game rendering evidence.
    canvas = Image.new('RGBA', (1130, 700), '#008080')
    font_path = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
    fonts = {size: ImageFont.truetype(font_path, size) for size in [14, 16, 18, 20, 24]}
    def text(dst, xy, content, size=16, color='#000000'):
        ImageDraw.Draw(dst).text(xy, content, fill=color, font=fonts[size])
    def put(dst, name, xy, frame=0):
        asset = image(name)
        frames = records[name]['frames'] if name in records else int(g.value(definitions[name]['text'], definitions[name]['node'], 'noOfFrames', '1'))
        fw = asset.width / frames
        asset = asset.crop((round(frame * fw), 0, round((frame + 1) * fw), asset.height))
        dst.alpha_composite(asset, xy)
    pane = Image.new('RGBA', (550, 642), '#c0c0c0')
    bevel(ImageDraw.Draw(pane), (0, 0, 550, 642))
    put(pane, 'GFX_header_bg', (5, 7))
    text(pane, (16, 10), 'イベントとディシジョン', 24, '#ffffff')
    put(pane, 'GFX_closebutton', (507, 9))
    ox, oy = 5, 45
    put(pane, 'GFX_event_header_bg', (ox, oy))
    text(pane, (ox + 12, oy + 9), 'イベント', 20, '#ffffff')
    for x, label in [(12, 'イベント'), (180, 'ニュース'), (348, '小規模イベント')]:
        put(pane, 'GFX_generic_checkbox3', (ox + x, oy + 40), 1)
        text(pane, (ox + x + 30, oy + 43), label)
    y = oy + 74
    for label, timer, warning in [('新しいお知らせがあります', '残り 14日', 0), ('外交についての報告', '残り 7日', 1)]:
        put(pane, 'GFX_event_item_bg', (ox - 1, y))
        put(pane, 'GFX_event_type_strip', (ox + 15, y + 3), warning)
        text(pane, (ox + 50, y + 7), label)
        text(pane, (ox + 406, y + 7), timer)
        y += 33
    def category(y, label):
        put(pane, 'GFX_category_header_bg', (ox - 4, y + 3))
        put(pane, 'GFX_decision_category_generic', (ox + 10, y + 12))
        text(pane, (ox + 74, y + 18), label, 20, '#ffffff')
        put(pane, 'GFX_checkbox_small5', (ox + 447, y + 17), 1)
        put(pane, 'GFX_conveyor_collapse_btn', (ox + 475, y + 16), 1)
    category(y, '国内の政策')
    y += 58
    text(pane, (ox + 14, y + 6), '政策の説明と関連するディシジョンを確認します。')
    y += 40
    for frame, label, cost, timer in [(0, '新しい計画を準備する', '50', ''), (1, '進行中の計画', '25', '30日'), (2, '条件を満たしていない計画', '100', '')]:
        put(pane, 'GFX_decision_item_bg', (ox, y), frame)
        icon = image('GFX_decision_unknown')
        pane.alpha_composite(icon, (ox + 30 - icon.width // 2, y + 19 - icon.height // 2))
        text(pane, (ox + 63, y + 7), label)
        text(pane, (ox + (320 if timer else 390), y + 7), cost, color='#b00000' if frame == 2 else '#006000' if frame == 1 else '#000000')
        if timer:
            text(pane, (ox + 402, y + 7), timer)
        put(pane, 'GFX_decision_select_icon_strip', (ox + 465, y + 6), frame)
        y += 41
    category(y, '地図上のディシジョン')
    y += 58
    put(pane, 'GFX_decision_item_bg', (ox, y), 1)
    text(pane, (ox + 62, y + 12), '対象の地域を地図で確認する')
    put(pane, 'GFX_locator_item_icon', (ox + 462, y + 4))
    # A scrollbar marks the native scrollable content area; it does not change
    # the game's dynamic grid or introduce a fixed-height window.
    d = ImageDraw.Draw(pane)
    d.rectangle((532, 53, 547, 631), fill='#dfdfdf')
    for top, down in [(53, False), (615, True)]:
        d.rectangle((533, top, 546, top + 15), fill='#c0c0c0')
        bevel(d, (533, top, 547, top + 16))
        cy = top + 8
        points = [(540, cy + 3), (536, cy - 2), (544, cy - 2)] if down else [(540, cy - 3), (536, cy + 2), (544, cy + 2)]
        d.polygon(points, fill='#000000')
    d.rectangle((533, 75, 546, 300), fill='#c0c0c0')
    bevel(d, (533, 75, 547, 301))
    text(canvas, (15, 5), 'Decision GUI 素材結合プレビュー（実機画面ではありません）', 18, '#ffffff')
    canvas.alpha_composite(pane, (15, 38))
    text(canvas, (590, 52), 'イベント見出し / 通知設定', 18, '#ffffff')
    put(canvas, 'GFX_event_header_bg', (590, 86))
    text(canvas, (590 + 12, 86 + 9), 'イベント', 20, '#ffffff')
    for x, label in [(12, 'イベント'), (180, 'ニュース'), (348, '小規模イベント')]:
        put(canvas, 'GFX_generic_checkbox3', (590 + x, 126), 1)
        text(canvas, (620 + x, 129), label)
    text(canvas, (590, 200), 'Decision行の3状態', 18, '#ffffff')
    for frame, label in enumerate(['通常の項目', '緑の状態を維持', '赤い警告状態を維持']):
        y = 241 + frame * 60
        put(canvas, 'GFX_decision_item_bg', (590, y), frame)
        text(canvas, (653, y + 9), label)
    text(canvas, (590, 455), '元のウィンドウ幅・行の高さを維持', 18, '#ffffff')
    text(canvas, (590, 492), '項目名 / コスト / 残り時間を分離', 18, '#ffffff')
    text(canvas, (590, 529), '時計・進捗・実行アイコンは元の図案', 18, '#ffffff')
    output.mkdir(parents=True, exist_ok=True)
    canvas.convert('RGB').save(output / 'assembled-decisions.png')
    report = dict(result='PASS', checks=len(checks), assertions=checks, changed_textures=sorted(changed),
                  backup=str(before), preview='Material composition with sample labels, not native rendering', runtime='NOT RUN')
    (output / 'verification.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(f'PASS: {len(checks)} Decision geometry/state/widget checks; {output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--before', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    verify(args.before, args.output)
