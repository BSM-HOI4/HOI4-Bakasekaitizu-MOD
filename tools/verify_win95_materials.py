#!/usr/bin/env python3
"""Regression checks and assembled previews for the reviewed material finish."""
import argparse
from collections import Counter
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import generate_win95_major_gui as g


def verify(destination, before=None):
    records = json.loads(g.MANIFEST.read_text())['sprites']
    config = json.loads((g.CONFIG / 'material_finish.json').read_text())
    game = g.game_directory()
    definitions, _, _ = g.definitions(game)
    images, sources = {}, {}
    assertions = []

    def check(condition, description):
        if not condition:
            raise AssertionError(description)
        assertions.append(description)

    def texture(name):
        if name not in images:
            images[name] = Image.open(g.MOD / records[name]['texture']).convert('RGBA')
        return images[name]

    def source(name):
        if name not in sources:
            reference = records.get(name, {}).get('source')
            sources[name] = Image.open(g.source_image(definitions[name], game, reference)).convert('RGBA')
        return sources[name]

    for name, profile in config['material_profiles'].items():
        check(name in records, f'{name}: finish is bound to an active material')
        actual, original = texture(name), source(name)
        check(actual.size == original.size, f'{name}: native geometry retained')
        check(records[name]['material_profile'] == profile, f'{name}: reviewed profile recorded')
    for name, data in records.items():
        frames = data['frames']
        if frames == 1:
            continue
        actual, native = texture(name), source(name)
        fw = actual.width // frames
        for a in range(frames):
            for b in range(a + 1, frames):
                ra, rb = (a * fw, 0, (a + 1) * fw, actual.height), (b * fw, 0, (b + 1) * fw, actual.height)
                if native.crop(ra).tobytes() != native.crop(rb).tobytes():
                    check(actual.crop(ra).tobytes() != actual.crop(rb).tobytes(), f'{name}: distinct native states {a + 1}/{b + 1}')
    short = lambda suffix: texture('GFX_event_report_' + suffix)
    for a, b in [('top_win', 'tileable_midsection'), ('tileable_midsection', 'tileable_bottom_section'),
                 ('tileable_bottom_section', 'bottom_win_end'), ('tileable_midsection', 'bottom_win')]:
        above, below = short(a), short(b)
        check(above.crop((0, above.height - 1, 580, above.height)).tobytes() == below.crop((0, 0, 580, 1)).tobytes(),
              f'Event assembled seam: {a} / {b}')
    for name in ['tileable_midsection', 'tileable_bottom_section']:
        im = short(name)
        row = im.crop((0, 0, 580, 1)).tobytes()
        check(all(im.crop((0, y, 580, y + 1)).tobytes() == row for y in range(im.height)), f'Event {name}: repeat without horizontal seams')
    for name in ['top_win', 'bottom_win', 'bottom_win_end']:
        im = short(name)
        check(im.getchannel('A').crop((0, 0, 580, im.height)).getextrema() == (255, 255), f'Event {name}: no ornamental holes')
        check(im.getchannel('A').crop((580, 0, 581, im.height)).getextrema() == (0, 0), f'Event {name}: one alignment column retained')
    for name, profile in config['material_profiles'].items():
        im = texture(name)
        for cutout in profile.get('cutouts', []):
            fw = im.width // records[name]['frames']
            for frame in range(records[name]['frames']):
                x, y, r, b = cutout
                check(im.getchannel('A').crop((x + frame * fw, y, r + frame * fw, b)).getextrema() == (0, 0), f'{name}: picture opening {frame + 1}')
    check(texture('GFX_event_news_pic_overlay').getpixel((199, 77))[3] == 0, 'News photograph has no paper-fold overlay')
    check(texture('GFX_event_operative_background').tobytes() == source('GFX_event_operative_background').tobytes(), 'Operative burn animation: decoded artwork unchanged in all 24 frames')
    check(texture('GFX_naval_region_header').getchannel('A').crop((0, 38, 435, 62)).getextrema() == (0, 0), 'Naval title does not cover terrain at GUI y36')
    if before:
        current = g.read(g.MOD / 'interface/replace/eventwindow.gui')
        prior = g.read(before / 'bakasekai/interface/replace/eventwindow.gui')
        def identity(text):
            return Counter((n.key.lower(), name) for n in g.nodes(text)
                           if (name := g.value(text, n, 'name')) and name != 'bsm_window_caption')
        check(identity(current) == identity(prior), 'Event widget types and IDs retained; only three caption widgets added')
        for key in ['clicksound', 'show_sound', 'hide_sound', 'pdx_tooltip']:
            def callbacks(text):
                return Counter(v for n in g.nodes(text) if (v := g.value(text, n, key)) is not None)
            check(callbacks(current) == callbacks(prior), f'Event {key}: engine callbacks retained')

    # A material composition, NOT a runtime screenshot. Text uses a preview font;
    # actual widgets keep the game's native metrics and localisation definitions.
    font_path = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
    font = lambda size: ImageFont.truetype(font_path, size)
    def text(im, pos, content, size=16, color='#000000'):
        ImageDraw.Draw(im).text(pos, content, font=font(size), fill=color, spacing=7)
    def paste(im, name, pos):
        asset = texture(name) if name in records else source(name)
        frames = records.get(name, {}).get('frames', 1)
        if frames > 1:
            asset = asset.crop((0, 0, asset.width // frames, asset.height))
        im.alpha_composite(asset, pos)
    def body(height):
        tile = short('tileable_midsection')
        im = Image.new('RGBA', (580, height))
        for y in range(0, height, tile.height):
            im.alpha_composite(tile.crop((0, 0, 580, min(tile.height, height - y))), (0, y))
        return im
    def report(leader=False):
        middle, options = (235, 105) if leader else (100, 206)
        h = 121 + middle + options + (59 if leader else 0)
        im = Image.new('RGBA', (581, h))
        im.alpha_composite(short('top_win'))
        im.alpha_composite(body(middle), (0, 121))
        if leader:
            im.alpha_composite(body(options), (0, 121 + middle))
            im.alpha_composite(short('bottom_win_end'), (0, 121 + middle + options))
        else:
            im.alpha_composite(short('bottom_win'), (0, 121 + middle))
        text(im, (12, 9), 'バカ世界地図 - イベント', 18, '#ffffff')
        paste(im, 'GFX_event_button_minimize', (540, 4))
        text(im, (32, 72), '世界から新しいお知らせが届きました', 22)
        if leader:
            portrait = source('GFX_leader_unknown')
            portrait = portrait.resize((round(portrait.width * .85), round(portrait.height * .85)))
            im.alpha_composite(portrait, (43, 125))
            text(im, (198, 121), '人物イベントの表示確認です。\n写真の透過と本文の余白を\n保ちながら、上下の枠を\n一つにつなげています。', 16)
            button_pos = (115, 121 + middle + 10)
        else:
            text(im, (31, 121), 'ここは本文の表示確認用テキストです。\n背景は白、枠はシルバー、タイトル帯は紺色です。\n途中に余分な区切り線が入らない構成です。', 16)
            paste(im, 'GFX_report_event_001', (5, 226))
            button_pos = (215, 220)
        paste(im, 'GFX_event_option_entry', button_pos)
        text(im, (button_pos[0] + 30, button_pos[1] + 9), '確認しました', 20)
        return im
    news = texture('GFX_event_news_bg').copy()
    text(news, (12, 10), 'バカ世界地図 - 世界のニュース', 18, '#ffffff')
    paste(news, 'GFX_event_button_minimize', (492, 6))
    paste(news, 'GFX_news_event_001', (59, 91))
    paste(news, 'GFX_event_news_pic_overlay', (59, 91))
    text(news, (30, 260), '世界のニュースが更新されました', 22)
    text(news, (39, 302), '新聞イベントの表示確認です。\n写真・見出し・本文を、白い閲覧領域に\nまとめています。\n\nこの画像は素材を結合したプレビューです。', 16)
    paste(news, 'GFX_event_option_entry', (80, 526))
    text(news, (120, 535), '世界を見に行く', 20)
    canvas = Image.new('RGBA', (1170, 1140), '#008080')
    text(canvas, (18, 8), 'Win95 material composition / 素材結合プレビュー（実機画面ではありません）', 17, '#ffffff')
    canvas.alpha_composite(report(), (18, 42))
    canvas.alpha_composite(news, (620, 42))
    canvas.alpha_composite(report(True), (18, 492))
    text(canvas, (620, 672), '航空任務の4状態 / 点灯・消灯・制限表示', 17, '#ffffff')
    # Show the complete strip here, rather than first-frame-only paste().
    canvas.alpha_composite(texture('GFX_strategicair_mission_btn_bg'), (620, 711))
    canvas.alpha_composite(texture('GFX_strategicair_mission_btn_checkbox_bg'), (620, 763))
    text(canvas, (620, 825), '写真枠の内側は透過を維持', 17, '#ffffff')
    paste(canvas, 'GFX_pol_leader_frame', (620, 858))
    paste(canvas, 'GFX_diplo_leader_frame', (820, 858))
    destination.mkdir(parents=True, exist_ok=True)
    canvas.convert('RGB').save(destination / 'assembled-materials.png')
    report_data = dict(result='PASS', checks=len(assertions), material_profiles=len(config['material_profiles']),
                       multi_frame_sprites=sum(v['frames'] > 1 for v in records.values()),
                       assertions=assertions, preview='Material composition only; not an in-game screenshot', backup=str(before) if before else None)
    (destination / 'verification.json').write_text(json.dumps(report_data, indent=2, ensure_ascii=False) + '\n')
    print(f'PASS: {len(assertions)} material/state/seam checks; {destination}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--before', type=Path)
    args = parser.parse_args()
    verify(args.output, args.before)
