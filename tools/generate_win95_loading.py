#!/usr/bin/env python3
"""Build BSM's deterministic Setup-style loading chrome; HOI4 drives real progress.

UI chrome and a procedural wallpaper fallback are reproducible here. The active
wallpaper is a separately generated and checked imagegen source artifact. The
MOD's existing thumbnail is rendered by the GUI without changing its pixels.
"""
from pathlib import Path
import argparse
import math
import re
import shutil
import hashlib
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'bakasekai/gfx/interface/win95/loading/setup'
ART_SHA256 = 'ec006e32beafa3b287d46f1c7ccb8bc641cd5d73fca1acaef9482a92e0c37715'


def bevel(draw, box, inset=False):
    x, y, r, b = box
    hi, lo = ('#808080', '#ffffff') if inset else ('#ffffff', '#202020')
    draw.line((x, b, x, y, r, y), fill=hi)
    draw.line((r, y, r, b, x, b), fill=lo)
    draw.line((x+1, b-1, x+1, y+1, r-1, y+1), fill='#dfdfdf' if not inset else '#202020')
    draw.line((r-1, y+1, r-1, b-1, x+1, b-1), fill='#808080' if not inset else '#c0c0c0')


def wallpaper():
    """Procedural comparison/fallback; the active GUI uses desktop-art-v2.png."""
    im = Image.new('RGBA', (1280, 960), '#000040')
    d = ImageDraw.Draw(im)
    for y in range(960):
        blue = round(54 + 42 * (1-y/960) + 11 * math.sin(y/150))
        d.line((0, y, 1279, y), fill=(0, 0, blue, 255))
    # Coarse overlaid ribbons echo a 1990s installer background.
    for band in range(-10, 20):
        points = [(x, int(86*band + 68*math.sin(x/270) - 0.26*x)) for x in range(-80, 1360, 12)]
        d.line(points, fill='#000047' if band % 2 else '#080867', width=24)
        d.line([(x, y+19) for x, y in points], fill='#080884', width=1)
    # Globe stays to the right, away from the heading.
    cx, cy, radius = 1040, 340, 320
    d.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), outline='#14149b', width=2)
    for ratio in (0.2, 0.4, 0.65, 0.85):
        rx = int(radius*ratio)
        d.ellipse((cx-rx, cy-radius, cx+rx, cy+radius), outline='#0e0e86')
    for ratio in (0.0, 0.3, 0.55, 0.8):
        offset = int(radius*ratio)
        rx = int(math.sqrt(radius*radius-offset*offset))
        for direction in ((1,) if offset == 0 else (-1, 1)):
            yy = cy + direction*offset
            d.ellipse((cx-rx, yy-22, cx+rx, yy+22), outline='#14148c')
    # Sparse ordered dots provide a low-color, period-appropriate texture.
    for y in range(0, 960, 4):
        for x in range((y//4 % 2)*2, 1280, 4):
            r, g, b, a = im.getpixel((x, y))
            d.point((x, y), fill=(r, g, max(0, b-13), a))
    return im


def welcome():
    im = Image.new('RGBA', (760, 424), '#c0c0c0')
    d = ImageDraw.Draw(im)
    bevel(d, (0, 0, 759, 423))
    bevel(d, (3, 3, 756, 420))
    d.rectangle((10, 10, 217, 413), fill='#50a0a0')
    d.rectangle((218, 10, 749, 413), fill='#ffffff')
    # Raised frame for the unmodified MOD thumbnail (150x150 in the GUI).
    bevel(d, (31, 27, 186, 182), inset=True)
    d.line((236, 62, 731, 62), fill='#808080')
    d.line((236, 63, 731, 63), fill='#dfdfdf')
    d.line((236, 247, 731, 247), fill='#c0c0c0')
    return im


def footer():
    im = Image.new('RGBA', (760, 70), '#c0c0c0')
    d = ImageDraw.Draw(im)
    bevel(d, (0, 0, 759, 69))
    bevel(d, (14, 39, 745, 61), inset=True)
    return im


def images():
    fill = Image.new('RGBA', (728, 18), '#ffffff')
    d = ImageDraw.Draw(fill)
    for x in range(0, 728, 10):
        d.rectangle((x, 1, min(x+7, 727), 16), fill='#000080')
    return {
        'desktop.png': wallpaper(),
        'welcome_panel.png': welcome(),
        'status_footer.png': footer(),
        'progress_fill.png': fill,
        'progress_empty.png': Image.new('RGBA', (728, 18), '#ffffff'),
    }


def font_metrics(check):
    # HOI4 resolves each atlas by the font basename, not just the BMFont page field.
    # Publish byte-identical atlas aliases alongside the roomier loading-only metrics.
    fonts = ROOT / 'bakasekai/gfx/fonts'
    for source, target in [('jis16', 'bsm_setup_body'), ('jis16_2', 'bsm_setup_body_2')]:
        original = (fonts / (source + '.fnt')).read_text(encoding='utf-8-sig')
        expected, count = re.subn(r'(?m)^(common lineHeight=)16\b', r'\g<1>22', original, count=1)
        assert count == 1, source
        expected, pages = re.subn(r'(?m)^(page .*?file=")[^"]+(".*)$',
                                 lambda match: match[1] + target + '.dds' + match[2], expected, count=1)
        assert pages == 1, source
        path = fonts / (target + '.fnt')
        atlas = fonts / (target + '.dds')
        source_atlas = fonts / (source + '.dds')
        if check:
            assert path.read_text(encoding='utf-8') == expected, path
            assert atlas.read_bytes() == source_atlas.read_bytes(), atlas
        else:
            path.write_text(expected, encoding='utf-8')
            shutil.copyfile(source_atlas, atlas)



def bootstrap_contract():
    # These exact paths are explicitly loaded by the engine before general GUI discovery.
    interface = ROOT / 'bakasekai/interface'
    gui = (interface / 'load_screen.gui').read_text(encoding='utf-8-sig')
    gfx = (interface / 'load_screen.gfx').read_text(encoding='utf-8-sig')
    fonts = (interface / 'load_screen_font.gfx').read_text(encoding='utf-8-sig')
    sprite_uses = set(re.findall(r'(?:quadTextureSprite|spriteType)\s*=\s*"([^"]+)"', gui))
    sprite_definitions = set(re.findall(r'name\s*=\s*"([^"]+)"', gfx))
    font_uses = set(re.findall(r'font\s*=\s*"([^"]+)"', gui))
    font_definitions = set(re.findall(r'name\s*=\s*"([^"]+)"', fonts))
    assert sprite_uses <= sprite_definitions, sprite_uses - sprite_definitions
    assert font_uses <= font_definitions, font_uses - font_definitions
    assert not (interface / 'replace/load_screen.gui').exists()
    assert not (interface / 'replace/_bsm_win95_loading.gfx').exists()


def run(check):
    OUT.mkdir(parents=True, exist_ok=True)
    expected_images = images()
    font_metrics(check)
    bootstrap_contract()
    # The AI-authored wallpaper is a source artifact, never overwritten by this generator.
    art = OUT / 'desktop-art-v2.png'
    assert hashlib.sha256(art.read_bytes()).hexdigest() == ART_SHA256, art
    with Image.open(art) as source:
        assert source.size == (1448, 1086) and source.mode == 'RGB'
    for name, expected in expected_images.items():
        path = OUT / name
        if check:
            with Image.open(path) as actual:
                assert actual.mode == 'RGBA' and actual.size == expected.size, path
                assert actual.tobytes() == expected.tobytes(), path
        else:
            expected.save(path)
    print(f'PASS: {len(expected_images)} Setup textures + AI wallpaper + 2 font metrics/atlases; RGBA/dimensions/pixels/line advance/bootstrap verified' if check
          else f'Generated {len(expected_images)} BSM Setup textures')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    run(parser.parse_args().check)
