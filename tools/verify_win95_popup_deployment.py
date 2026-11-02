#!/usr/bin/env python3
"""Native-contract checks and composition previews for popup/deployment chrome."""
import argparse
from collections import Counter
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import generate_win95_major_gui as g
from win95_materials import bevel


def verify(before, output):
    config = json.loads((g.CONFIG / 'popup_deployment_finish.json').read_text())
    manifest = json.loads(g.MANIFEST.read_text())
    records = manifest['sprites']
    old = json.loads((before / 'bakasekai/gfx/interface/win95/major/manifest.json').read_text())['sprites']
    checks = []
    def check(condition, description):
        if not condition:
            raise AssertionError(description)
        checks.append(description)
    def root(text, n):
        while n.parent and n.parent.key.lower() != 'guitypes':
            n = n.parent
        return g.value(text, n, 'name')
    # Check every reviewed GUI against the pre-edit snapshot, including aliases
    # that the new shared footer introduces outside popupwindow.gui.
    for entry in manifest['guis']:
        relative = 'bakasekai/interface/' + entry['gui']
        current, prior = g.read(g.ROOT / relative), g.read(before / relative)
        def identities(text):
            return Counter((root(text, n), n.key.lower(), name) for n in g.nodes(text) if (name := g.value(text, n, 'name')))
        check(identities(current) == identities(prior), entry['gui'] + ': widget types/IDs retained')
        def bindings(text):
            result = []
            for n in g.nodes(text):
                owner = (root(text, n), g.value(text, n, 'name'))
                if sp := g.sprite(text, n):
                    result.append((owner, 'sprite', g.original(sp[0])))
                for key in ['clicksound', 'show_sound', 'hide_sound', 'pdx_tooltip', 'shortcut', 'frame']:
                    if (v := g.value(text, n, key)) is not None:
                        result.append((owner, key, v))
                if n.parent and n.parent.key.lower() == 'guitypes':
                    result.append((owner, 'root_size', str(g.pair(text, n, 'size', 'width', 'height'))))
            return Counter(result)
        check(bindings(current) == bindings(prior), entry['gui'] + ': original sprites, callbacks, frames and root sizes retained')
    changed = {n for n, d in records.items() if old.get(n, {}).get('sha256') != d['sha256']}
    check(changed == set(config['material_profiles']), 'Exactly eight popup/deployment textures changed')
    game = g.game_directory()
    definitions, _, _ = g.definitions(game)
    generated_text = g.read(g.GFX)
    aliases = {g.value(generated_text, n, 'name'): n for n in g.nodes(generated_text) if n.key.lower() in g.TYPES}
    def signature(text, n):
        edits = [(v[1], v[2], '__REFERENCE__') for key in ['name', 'texturefile'] if (v := g.prop(text, n, key))]
        from win95_gui_lib import TOKEN
        return [m[0] for m in TOKEN.finditer(g.cloned_block(text, n, edits)) if not m[0].startswith('#')]
    images = {}
    def image(name):
        if name not in images:
            p = g.MOD / records[name]['texture'] if name in records else g.source_image(definitions[name], game)
            images[name] = Image.open(p).convert('RGBA')
        return images[name]
    for name in config['material_profiles']:
        d, native = records[name], definitions[name]
        with Image.open(g.source_image(native, game, d['source'])) as original:
            check(image(name).size == original.size, name + ': native image dimensions retained')
        check(d['frames'] == int(g.value(native['text'], native['node'], 'noOfFrames', '1')), name + ': native frame count retained')
        check(signature(native['text'], native['node']) == signature(generated_text, aliases[d['alias']]), name + ': native GFX effects/settings retained')
        check(d['material_profile'] == config['material_profiles'][name], name + ': reviewed finish is recorded')
    normal, obsolete = image('GFX_deployment_named_division_bg'), image('GFX_deployment_named_division_obsolete_bg')
    check(normal.getchannel('A').getextrema() == (255, 255), 'Normal division card has no ragged alpha')
    check(obsolete.getchannel('A').crop((0, 0, 346, 78)).getextrema() == (255, 255), 'Obsolete division card has a complete 346x78 face')
    check(obsolete.getchannel('A').crop((346, 0, 348, 79)).getextrema() == (0, 0), 'Obsolete card retains two transparent right columns')
    check(obsolete.getchannel('A').crop((0, 78, 348, 79)).getextrema() == (0, 0), 'Obsolete card keeps one transparent alignment row')
    for box in [(0, 0, 346, 1), (0, 77, 346, 78), (0, 0, 1, 78), (345, 0, 346, 78)]:
        check(normal.crop(box).tobytes() == obsolete.crop(box).tobytes(), 'Normal/obsolete outer frame aligns without jumping')
    check(normal.getpixel((4, 40)) != obsolete.getpixel((4, 40)), 'Obsolete amber state remains distinct')
    header_uses = 0
    for relative in ['replace/popupwindow.gui', 'replace/frontendmultiplayerview.gui']:
        text = g.read(g.MOD / 'interface' / relative)
        for n in g.nodes(text):
            sp = g.sprite(text, n)
            if not sp or g.original(sp[0]) not in ('GFX_diplo_popup_header_bg', 'GFX_diplo_popup_header_bg_large'):
                continue
            header_uses += 1
            parent = n.parent
            title = next(c for c in parent.children if c.key.lower() == 'instanttextboxtype' and g.value(text, c, 'name') in ('title', 'Title'))
            x, y = g.pair(text, n, 'position')
            tx, ty = g.pair(text, title, 'position')
            tw, th = int(g.value(text, title, 'maxWidth')), int(g.value(text, title, 'maxHeight'))
            width = image(g.original(sp[0])).width
            check(g.value(text, title, 'font').endswith('__white'), root(text, title) + ': white title on navy')
            check(x + 4 <= tx and tx + tw <= x + width - 4 and y + 4 <= ty and ty + th <= y + 56,
                  root(text, title) + ': complete title box fits the navy band')
    check(header_uses == 15, 'All 15 popup-header consumers checked')
    for name in ['GFX_diplo_popup_header_bg', 'GFX_diplo_popup_header_bg_large', 'GFX_diplo_popup_bottom', 'GFX_diplo_popup_bottom_large', 'GFX_agency_popup_bg', 'GFX_focus_popup_bg']:
        im = image(name)
        bounds = config['material_profiles'][name].get('bounds', [0, 0, im.width, im.height])
        check(im.getchannel('A').crop(bounds).getextrema() == (255, 255), name + ': complete rectangular face')
        x, y, r, b = bounds
        for margin in [(0, 0, im.width, y), (0, b, im.width, im.height)]:
            if margin[3] > margin[1]:
                check(im.getchannel('A').crop(margin).getextrema() == (0, 0), name + ': placement margin is transparent')
    text = g.read(g.MOD / 'interface/replace/popupwindow.gui')
    focus = next(n for n in g.nodes(text) if g.value(text, n, 'name') == 'focus_name')
    check(g.pair(text, focus, 'position')[1] + int(g.value(text, focus, 'maxHeight')) <= 197, 'Focus caption ends above the visible button bar')
    check(g.value(text, focus, 'font').endswith('__black'), 'Focus caption uses dark glyphs on its white field')
    check(image('GFX_focus_popup_bg').getpixel((235, 90))[:3] == (255, 255, 255), 'Focus metal/laurel background is replaced with a white client field')
    def pick(rn, name):
        return next(n for n in g.nodes(text) if root(text, n) == rn and g.value(text, n, 'name') == name)
    for rn, client, caption in [('research_finished_popup_window', 'paper_background', 'tech_name'),
                                ('focus_finished_popup_window', 'focus_popup_bg', 'focus_name')]:
        header_y = g.pair(text, pick(rn, 'diplo_popup_header_bg'), 'position')[1]
        client_y = g.pair(text, pick(rn, client), 'position')[1]
        footer_y = g.pair(text, pick(rn, 'diplo_popup_bottom'), 'position')[1]
        caption_node = pick(rn, caption)
        caption_end = g.pair(text, caption_node, 'position')[1] + int(g.value(text, caption_node, 'maxHeight'))
        check(header_y + config['material_profiles']['GFX_diplo_popup_header_bg']['bounds'][3] <= client_y,
              rn + ': header does not cover the client top edge')
        check(caption_end <= footer_y + config['material_profiles']['GFX_diplo_popup_bottom']['bounds'][1],
              rn + ': footer does not cover the client caption')
    deployment = g.read(g.MOD / 'interface/replace/countrydeploymentview.gui')
    priority_node = next(n for n in g.nodes(deployment) if root(deployment, n) == 'named_division_template_entry' and g.value(deployment, n, 'name') == 'division_priority_icon')
    px, py = g.pair(deployment, priority_node, 'position')
    priority = image('GFX_div_deploy_priority_icon_strip')
    for i in range(3):
        glyph = priority.crop((i * 16, 0, (i + 1) * 16, priority.height)).getbbox()
        if glyph:
            check(px + glyph[2] <= 95 and py + glyph[3] <= 72, 'Priority arrow stays in its native lane, clear of caption/control columns')

    # Material compositions, not screenshots of the game. Preserve the native
    # image/flag/portrait art in these examples and use a labelled preview font.
    font_path = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
    fonts = {s: ImageFont.truetype(font_path, s) for s in [16, 18, 24]}
    def text_at(dst, xy, label, size=18, color='#000000'):
        ImageDraw.Draw(dst).text(xy, label, font=fonts[size], fill=color, spacing=8)
    def put(dst, name, xy, frame=0, scale=1):
        asset = image(name)
        f = records[name]['frames'] if name in records else int(g.value(definitions[name]['text'], definitions[name]['node'], 'noOfFrames', '1'))
        fw = asset.width / f
        frame = min(frame, f - 1)
        asset = asset.crop((round(frame * fw), 0, round((frame + 1) * fw), asset.height))
        if scale != 1:
            asset = asset.resize((round(asset.width * scale), round(asset.height * scale)))
        dst.alpha_composite(asset, xy)
    def window(size):
        dst = Image.new('RGBA', size, '#c0c0c0')
        bevel(ImageDraw.Draw(dst), (0, 0, *size))
        return dst
    small = window((500, 262))
    put(small, 'GFX_agency_popup_bg', (13, 75))
    put(small, 'GFX_diplo_popup_header_bg', (3, 8))
    text_at(small, (100, 29), '研究が完了しました', 24, '#ffffff')
    put(small, 'GFX_technology_medium', (225, 103))
    text_at(small, (160, 167), '歩兵装備の改良', 18)
    put(small, 'GFX_diplo_popup_bottom', (3, 189))
    for x, caption in [(40, '詳細'), (340, '確認')]:
        put(small, 'GFX_button_123x34', (x, 203))
        text_at(small, (x + 40, 208), caption)
    large = window((584, 320))
    put(large, 'GFX_diplo_popup_header_bg_large', (0, 8))
    text_at(large, (180, 30), '外交上の提案', 24, '#ffffff')
    # GFX_shield_medium is supplied dynamically by the engine. Use concrete MOD
    # flags for this labelled fixture instead of pretending it is a disk sprite.
    for x, filename in [(24, 'JAP_neutrality.tga'), (476, 'NTS.tga')]:
        with Image.open(g.MOD / 'gfx/flags' / filename) as im:
            large.alpha_composite(im.convert('RGBA').resize((80, 52)), (x, 18))
    for x in [18, 472]:
        put(large, 'GFX_leader_unknown', (x, 88), scale=.6)
    text_at(large, (132, 112), '各国からの提案を確認します。\n国旗・人物画像はそのままに、\n本文と操作欄を整えています。', 16)
    put(large, 'GFX_diplo_popup_bottom_large', (0, 248))
    for x, caption in [(77, '閉じる'), (386, '承認')]:
        put(large, 'GFX_button_123x34', (x, 261))
        text_at(large, (x + 32, 267), caption)
    focus_preview = window((500, 262))
    put(focus_preview, 'GFX_diplo_popup_header_bg', (3, 8))
    text_at(focus_preview, (130, 29), '国家方針が完了', 24, '#ffffff')
    put(focus_preview, 'GFX_focus_popup_bg', (15, 72))
    put(focus_preview, 'GFX_goal_unknown', (220, 95))
    text_at(focus_preview, (160, 165), '新しい国家方針', 18, '#000000')
    put(focus_preview, 'GFX_diplo_popup_bottom', (3, 189))
    for x, caption in [(40, '詳細'), (340, '確認')]:
        put(focus_preview, 'GFX_button_123x34', (x, 203))
        text_at(focus_preview, (x + 40, 208), caption)
    def division(old=False):
        dst = image('GFX_deployment_named_division_obsolete_bg' if old else 'GFX_deployment_named_division_bg').copy()
        put(dst, 'GFX_technology_medium', (10, 16))
        put(dst, 'GFX_div_deploy_priority_icon_strip', (60, 16))
        if old:
            put(dst, 'GFX_obsolete_template_warning', (14, 15))
        text_at(dst, (110, 20), '旧式の歩兵師団' if old else '一般歩兵師団', 16)
        text_at(dst, (105, 48), '10/10', 16)
        for x, label in [(163, '訓練'), (233, '編集')]:
            put(dst, 'GFX_small_button_71x26', (x, 48))
            text_at(dst, (x + 18, 51), label, 16)
        put(dst, 'GFX_toggle_obsolete_button', (307, 22), int(old))
        put(dst, 'GFX_delete_template_button', (303, 48))
        return dst
    canvas = Image.new('RGBA', (1130, 730), '#008080')
    text_at(canvas, (16, 6), 'Popup / Deployment 素材結合プレビュー（実機画面ではありません）', 18, '#ffffff')
    canvas.alpha_composite(large, (16, 42))
    canvas.alpha_composite(small, (614, 42))
    canvas.alpha_composite(focus_preview, (16, 405))
    text_at(canvas, (630, 378), '通常の師団テンプレート', 18, '#ffffff')
    canvas.alpha_composite(division(), (630, 411))
    text_at(canvas, (630, 514), '旧式の状態を維持', 18, '#ffffff')
    canvas.alpha_composite(division(True), (630, 548))
    output.mkdir(parents=True, exist_ok=True)
    canvas.convert('RGB').save(output / 'assembled-popup-deployment.png')
    report = dict(result='PASS', checks=len(checks), assertions=checks, changed_textures=sorted(changed), header_consumers=header_uses,
                  backup=str(before), preview='Material composition with sample labels, not native rendering', runtime='NOT RUN')
    (output / 'verification.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(f'PASS: {len(checks)} checks; 8 textures, {header_uses} popup consumers; {output}')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--before', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    verify(a.before, a.output)
