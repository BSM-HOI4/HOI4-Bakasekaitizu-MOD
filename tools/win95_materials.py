"""Reviewed Win95 chrome: joined edges, picture openings, and explicit states.

Rectangles use Pillow's exclusive right/bottom coordinates. Native ornamental
alpha is deliberately NOT reused: a window is rectangular; a picture frame has
only its declared content opening. Semantic illustrations opt out explicitly.
"""
from PIL import Image, ImageDraw


def pictogram_patch(source, box):
    """Lift a native coloured/bright glyph off its dark metal button face.

    Callers explicitly review the inner glyph rectangle, excluding frame edges.
    Keep original foreground RGB and alpha rather than repainting its meaning.
    """
    patch = source.crop(box).convert('RGBA')
    pixels = []
    for r, g, b, a in patch.getdata():
        foreground = max(r, g, b) >= 105 or (max(r, g, b) > 60 and max(r, g, b) - min(r, g, b) > 25)
        pixels.append((r, g, b, a if foreground else 0))
    patch.putdata(pixels)
    return patch


def bevel(draw, rect, edges='TLRB', sunken=False):
    x, y, r, b = rect
    # Win95 has four different bevel tones, not two repeated outline strokes.
    hi = ('#808080', '#404040') if sunken else ('#dfdfdf', '#ffffff')
    lo = ('#ffffff', '#dfdfdf') if sunken else ('#404040', '#808080')
    for inset in range(min(2, (r - x) // 2, (b - y) // 2)):
        a, c, right, bottom = x + inset, y + inset, r - 1 - inset, b - 1 - inset
        # Open edges must reach the neighbouring part, including the inner bevel.
        vy = y + inset if 'T' in edges else y
        vb = b - 1 - inset if 'B' in edges else b - 1
        hx = x + inset if 'L' in edges else x
        hr = r - 1 - inset if 'R' in edges else r - 1
        if 'L' in edges:
            draw.line((a, vy, a, vb), fill=hi[inset])
        if 'T' in edges:
            draw.line((hx, c, hr, c), fill=hi[inset])
        if 'R' in edges:
            draw.line((right, vy, right, vb), fill=lo[inset])
        if 'B' in edges:
            draw.line((hx, bottom, hr, bottom), fill=lo[inset])


def render_material(source, frames, profile):
    if profile.get('preserve_art'):
        return source.copy()
    width, height = source.size
    fw = width // frames
    bounds = profile.get('bounds', [0, 0, fw, height])
    variants = profile.get('frames', [{} for _ in range(frames)])
    if len(variants) != frames:
        raise ValueError(f'Material state count: {len(variants)} != {frames}')
    result = Image.new('RGBA', source.size)
    for index, variant in enumerate(variants):
        frame = Image.new('RGBA', (fw, height))
        draw = ImageDraw.Draw(frame)
        spec = dict(profile, **variant)
        layers = [dict(rect=bounds, fill=spec.get('fill', '#c0c0c0'),
                       edges=spec.get('edges', 'TLRB'), sunken=spec.get('sunken', False))]
        layers.extend(spec.get('layers', []))
        for layer in layers:
            x, y, r, b = layer['rect']
            if not (0 <= x < r <= fw and 0 <= y < b <= height):
                raise ValueError(f'Material rectangle outside frame: {layer["rect"]}, {fw}x{height}')
            if 'fill' in layer:
                fill = tuple(layer['fill']) if isinstance(layer['fill'], list) else layer['fill']
                draw.rectangle((x, y, r - 1, b - 1), fill=fill)
            if layer.get('hatch'):
                # Restricted occupation state: keep its diagonal warning cue.
                tile = Image.new('RGBA', (r - x, b - y), layer.get('fill', '#ececec'))
                hatch = ImageDraw.Draw(tile)
                for start in range(-(b - y), r - x, 12):
                    hatch.line((start, b - y, start + b - y, 0), fill=layer['hatch'], width=4)
                frame.paste(tile, (x, y))
            bevel(draw, (x, y, r, b), layer.get('edges', ''), layer.get('sunken', False))
        if box := spec.get('relief'):
            # State atlases encode level bars separately from their brown frame.
            # Keep that exact pattern in a neutral silver inset, in every frame.
            x, y, r, b = box
            if not (2 <= x < r <= fw - 2 and 2 <= y < b <= height - 2):
                raise ValueError(f'Invalid state relief: {box}')
            patch = source.crop((index * fw + x, y, index * fw + r, b)).convert('L')
            patch = patch.point(lambda v: 128 + v // 2).convert('RGBA')
            frame.paste(patch, (x, y))
        for rect in spec.get('cutouts', []):
            x, y, r, b = rect
            if not (2 <= x < r <= fw - 2 and 2 <= y < b <= height - 2):
                raise ValueError(f'Unbounded picture opening: {rect}')
            bevel(draw, (x - 2, y - 2, r + 2, b + 2), sunken=True)
            draw.rectangle((x, y, r - 1, b - 1), fill=(0, 0, 0, 0))
        for symbol in spec.get('symbols', []):
            x, y, r, b = symbol['rect']
            kind = symbol['kind']
            if kind not in ('cross', 'plus', 'minus', 'arrow_up', 'arrow_down') or not (0 <= x < r <= fw and 0 <= y < b <= height):
                raise ValueError(f'Invalid material status symbol: {symbol}')
            color = symbol['color']
            cx, cy = (x + r) // 2, (y + b) // 2
            if kind == 'cross':
                draw.line((x, y, r - 1, b - 1), fill=color, width=2)
                draw.line((x, b - 1, r - 1, y), fill=color, width=2)
            elif kind in ('plus', 'minus'):
                draw.line((x, cy, r - 1, cy), fill=color, width=2)
                if kind == 'plus':
                    draw.line((cx, y, cx, b - 1), fill=color, width=2)
            else:
                tip, base = (y, b - 1) if kind == 'arrow_up' else (b - 1, y)
                draw.polygon(((cx, tip), (x, base), (r - 1, base)), fill=color)
        if spec.get('restricted'):
            # Native frames 3/4 add this diagonal cue independently of on/off.
            draw.polygon(((fw - 3, 3), (fw - 3, height - 3), (3, height - 3)), fill='#a0a0a0')
        if indicator := spec.get('indicator'):
            if indicator == 'lamp':
                draw.ellipse((3, 3, 13, 13), fill='#008000' if spec['on'] else '#808080', outline='#404040')
                if spec['on']:
                    draw.ellipse((5, 5, 8, 8), fill='#80ff80')
            elif indicator == 'check':
                draw.rectangle((3, 3, 14, 14), fill='#ffffff')
                bevel(draw, (3, 3, 15, 15), sunken=True)
                if spec['on']:
                    draw.line((6, 8, 8, 11, 12, 6), fill='#008000', width=2)
            else:
                raise ValueError(f'Unknown native state indicator: {indicator}')
        if spec.get('symbol') == 'minimize':
            # This is the actual MINIMIZE_EVENT control, not a painted fake button.
            cx, cy = fw // 2, height // 2
            draw.rectangle((cx - 5, cy + 5, cx + 5, cy + 6), fill='#000000')
        result.paste(frame, (index * fw, 0))
    return result
