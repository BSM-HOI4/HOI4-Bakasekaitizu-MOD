#!/usr/bin/env python3
"""Theme reviewed major GUI chrome, preserving every widget and native GFX contract.

Only sprite/font scalar references change in GUI files. New unique GFX/font names
avoid global load-order overrides. --plan is read-only; --check verifies outputs.
Original art, dimensions, frame counts and shaders are retained. Reviewed finish
profiles replace ornamental alpha with complete window edges and picture openings.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from PIL import Image, ImageDraw, ImageStat, ImageChops
from win95_gui_lib import nodes, prop, value, child, pair, numeric, replacements, game_directory
from win95_materials import bevel, render_material, pictogram_patch

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'bakasekai'
OUT = MOD / 'gfx/interface/win95/major'
GFX = MOD / 'interface/_bsm_win95_major_gui.gfx'
FONTS = MOD / 'interface/_bsm_win95_major_gui_fonts.gfx'
MANIFEST = OUT / 'manifest.json'
CONFIG = ROOT / 'tools/win95_themes'
PREFIX = 'GFX_bsm_w95_gui__'
FONT_PREFIX = 'bsm_w95_gui__'
SPRITE_KEYS = ('quadTextureSprite', 'spriteType')
TYPES = {'spritetype', 'corneredtilespritetype', 'textspritetype', 'frameanimatedspritetype'}
ROLES = {'panel', 'header', 'row', 'production_row', 'selection_overlay', 'obsolete_row', 'mio_header', 'production_summary', 'field', 'button', 'tab', 'close',
         'scroll_up', 'scroll_down', 'scroll_left', 'scroll_right', 'scroll_thumb', 'scroll_track'}


def read(path):
    return path.read_text(encoding='utf-8-sig')


def original(name):
    return name[len(PREFIX):] if name.startswith(PREFIX) else name


def sprite(text, node):
    return next((p for key in SPRITE_KEYS if (p := prop(text, node, key))), None)


def definitions(game):
    sprites, fonts, overrides = {}, {}, {}
    paths = sorted((game / 'interface').rglob('*.gfx')) + sorted((MOD / 'interface').rglob('*.gfx'))
    for path in paths:
        if path in (GFX, FONTS):
            continue
        text = read(path)
        try:
            parsed = nodes(text, tolerate_outer=path.is_relative_to(game))
        except ValueError as error:
            raise ValueError(f'{path}: {error}') from error
        for node in parsed:
            kind = node.key.lower()
            if kind not in TYPES | {'bitmapfont', 'bitmapfont_override'}:
                continue
            name = value(text, node, 'name')
            if not name:
                continue
            definition = dict(path=path, text=text, node=node)
            if kind in TYPES:
                sprites[name] = definition
            elif kind == 'bitmapfont':
                fonts[name] = definition
                overrides[name] = []
            else:
                overrides.setdefault(name, []).append(definition)
    return sprites, fonts, overrides


def source_image(definition, game, reference=None):
    raw = reference or value(definition['text'], definition['node'], 'texturefile')
    if not raw:
        return None
    raw = re.sub('/+', '/', raw.replace('\\', '/'))
    for base in (MOD, game):
        path = base / raw
        if path.exists():
            return path
        if path.with_suffix('.dds').exists():
            return path.with_suffix('.dds')
    return None


def active_guis(requested, game):
    result = {}
    for relative in sorted(requested):
        relative = relative.removeprefix('replace/')
        matches = [p for p in (MOD / 'interface' / relative, MOD / 'interface/replace' / relative) if p.exists()]
        if matches:
            for path in matches:
                result[path] = path
        elif (game / 'interface' / relative).exists():
            result[MOD / 'interface/replace' / relative] = game / 'interface' / relative
        else:
            raise ValueError(f'GUI source missing: {relative}')
    return result


def font_name(name, shade):
    if name.startswith(FONT_PREFIX):
        name = name[len(FONT_PREFIX):].rsplit('__', 1)[0]
    return FONT_PREFIX + name + '__' + shade


def baseline_font(name):
    return name[len(FONT_PREFIX):].rsplit('__', 1)[0] if name.startswith(FONT_PREFIX) else name


def cloned_block(text, node, edits):
    return replacements(text[node.start:node.end],
                        [(a - node.start, b - node.start, new) for a, b, new in edits])


def flat_image(size, frames, role, bbox=None, source_alpha=None, selected=False):
    width, height = size
    if width % frames:
        raise ValueError(f'Non-integral frame width: {size}, {frames}')
    fw = width // frames
    result = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(result)
    for frame in range(frames):
        left = frame * fw
        x, y, right, bottom = bbox or (0, 0, fw, height)
        x += left
        right += left
        right -= 1
        bottom -= 1
        if right < x or bottom < y:
            continue
        fill = '#ffffff' if role in ('field', 'row', 'production_row') else '#c0c0c0'
        if role == 'selection_overlay':
            fill = (0, 0, 0, 0)
        if role == 'obsolete_row':
            fill = '#fff2d4'
        if role == 'row' and frames > 1:
            fill = ('#ffffff', '#dce8ff', '#dedede', '#c8c8c8')[min(frame, 3)]
        if role == 'scroll_track':
            fill = '#dfdfdf'
        if selected and role in ('row', 'panel'):
            fill = '#dce8ff'
        if role in ('button', 'tab', 'close', 'scroll_thumb') or role.startswith('scroll_'):
            fill = ('#c0c0c0', '#d4d0c8', '#e4e4e4', '#b0b0b0')[min(frame, 3)]
        draw.rectangle((x, y, right, bottom), fill=fill)
        pressed = role in ('row', 'field', 'scroll_track') or (frame == 1 and role in ('button', 'tab', 'close', 'scroll_thumb'))
        bevel(draw, (x, y, right + 1, bottom + 1), sunken=pressed)
        if role == 'header' and bottom - y > 5 and right - x > 5:
            draw.rectangle((x + 2, y + 2, right - 2, bottom - 2), fill='#000080')
        if role in ('button', 'tab', 'row') and frames > 1 and frame == 1:
            draw.rectangle((x + 2, y + 2, right - 2, bottom - 2), outline='#000080')
        if selected and role in ('row', 'panel', 'button', 'tab'):
            draw.rectangle((x + 2, y + 2, right - 2, bottom - 2), outline='#000080', width=2)
        if role == 'obsolete_row':
            draw.rectangle((x + 2, y + 2, right - 2, bottom - 2), outline='#9b6400', width=2)
        if role == 'mio_header':
            # A silver/gold strip still identifies an assigned MIO above a white row.
            draw.rectangle((x + 2, y + 2, right - 2, bottom - 2), outline='#9b6400')
        if role == 'selection_overlay':
            # The native selection sprite is an opaque copy of the old row.
            # Keep a pale-blue name band and navy border; let the underlying
            # 5/10/15-slot background and equipment field show through.
            draw.rectangle((x + 2, y + 2, right - 2, min(y + 27, bottom - 2)), fill='#dce8ff')
            draw.rectangle((x + 1, y + 1, right - 1, bottom - 1), outline='#000080', width=2)
        if role == 'production_summary':
            for divider in (48, 85, 117, 167, 211):
                draw.line((left + 9, divider, left + fw - 10, divider), fill='#808080')
                draw.line((left + 9, divider + 1, left + fw - 10, divider + 1), fill='#ffffff')
            draw.line((left + 275, 86, left + 275, height - 5), fill='#808080')
        cx, cy = (x + right) // 2, (y + bottom) // 2
        radius = max(2, min(5, (right - x) // 4, (bottom - y) // 4))
        if role == 'close':
            draw.line((cx - radius, cy - radius, cx + radius, cy + radius), fill='#000000', width=2)
            draw.line((cx - radius, cy + radius, cx + radius, cy - radius), fill='#000000', width=2)
        elif role in ('scroll_up', 'scroll_down', 'scroll_left', 'scroll_right'):
            points = {
                'scroll_up': [(cx, cy - radius), (cx - radius, cy + radius), (cx + radius, cy + radius)],
                'scroll_down': [(cx, cy + radius), (cx - radius, cy - radius), (cx + radius, cy - radius)],
                'scroll_left': [(cx - radius, cy), (cx + radius, cy - radius), (cx + radius, cy + radius)],
                'scroll_right': [(cx + radius, cy), (cx - radius, cy - radius), (cx - radius, cy + radius)],
            }[role]
            draw.polygon(points, fill='#000000')
    if source_alpha is not None and role in ('panel', 'row', 'production_row', 'selection_overlay', 'obsolete_row', 'mio_header', 'production_summary', 'field', 'header'):
        # Portrait/flag/window frames can be drawn above content. Their transparent
        # centres and cut-outs must remain transparent rather than becoming panels.
        result.putalpha(ImageChops.multiply(result.getchannel('A'), source_alpha))
    return result


def contract(text):
    """Compare every source token except the two explicitly permitted value families."""
    edits = []
    for node in nodes(text):
        for key in (*SPRITE_KEYS, 'font', 'buttonFont'):
            if found := prop(text, node, key):
                edits.append((found[1], found[2], '__THEME_REFERENCE__'))
    from win95_gui_lib import TOKEN
    return [m[0] for m in TOKEN.finditer(replacements(text, edits)) if not m[0].startswith('#')]


def run(args):
    game = Path(args.game_dir).expanduser() if args.game_dir else game_directory()
    roles, protected, requested = {}, set(), set()
    preserve_roots, light_roots, dark_roots = set(), set(), set()
    preserve_font_files, light_files, recolor_bsm_roots = set(), set(), set()
    font_overrides, runtime_bindings, documented_layout_fixes, preserve_regions, grid_regions = [], {}, {}, {}, {}
    material_profiles = {}
    previous_manifest = json.loads(read(MANIFEST)) if MANIFEST.exists() else {}
    for path in sorted(CONFIG.glob('*.json')):
        config = json.loads(read(path))
        requested.update(config['gui_files'])
        protected.update(config.get('preserve_sprites', []))
        preserve_roots.update(config.get('preserve_roots', []))
        light_roots.update(config.get('light_roots', []))
        dark_roots.update(config.get('dark_roots', []))
        preserve_font_files.update(config.get('preserve_font_files', []))
        light_files.update(config.get('light_files', []))
        recolor_bsm_roots.update(config.get('recolor_bsm_roots', []))
        font_overrides.extend(config.get('font_overrides', []))
        runtime_bindings.update(config.get('runtime_sprite_bindings', {}))
        documented_layout_fixes.update(config.get('documented_layout_fixes', {}))
        preserve_regions.update(config.get('preserve_regions', {}))
        grid_regions.update(config.get('grid_regions', {}))
        for name, profile in config.get('material_profiles', {}).items():
            if name in material_profiles:
                raise ValueError(f'Duplicate material finish profile: {name}')
            material_profiles[name] = profile
        for name, role in config['sprites'].items():
            if name in roles and roles[name] != role:
                raise ValueError(f'Conflicting role for {name}: {roles[name]} vs {role}')
            if role not in ROLES:
                raise ValueError(f'Unsupported role {role}')
            roles[name] = role
    if set(roles) & protected:
        raise ValueError(f'Role/preserve conflict: {sorted(set(roles) & protected)}')
    sprites, fonts, overrides = definitions(game)
    guis = active_guis(requested, game)
    texts = {target: read(source) for target, source in guis.items()}
    ast = {path: nodes(text) for path, text in texts.items()}
    used_sprites = {original(found[0]) for p, ns in ast.items() for n in ns if (found := sprite(texts[p], n))}
    used_sprites.update(runtime_bindings)
    missing_definitions = sorted(set(roles) - set(sprites))
    if missing_definitions:
        raise ValueError(f'Sprite definitions missing: {missing_definitions}')
    # Explicitly reviewed native shared backgrounds used across all primary screens.
    for name in ('GFX_tiled_window', 'GFX_tiled_bg', 'GFX_tiled_plain_bg2', 'GFX_tiled_generic_bg2',
                 'GFX_tiled_generic_overlay_bg1', 'GFX_tiled_generic_overlay_bg1_small'):
        if name in sprites and name not in protected:
            roles.setdefault(name, 'panel')
    for name in used_sprites:
        # Dimension-named native text buttons are blank chrome, unlike icon buttons.
        if name in sprites and name not in protected and re.fullmatch(r'GFX_button_\d+x\d+(?:_light|_alt|_\d+)?', name):
            roles.setdefault(name, 'button')
    # Existing generated shared chrome participates in contrast detection, not re-generation.
    shared = json.loads(read(MOD / 'gfx/interface/win95/shared/manifest.json'))
    existing_roles = {record['name']: 'header' if 'header' in record['name'] else
                      'button' if 'button' in record['name'] else 'panel' for record in shared}
    metadata, generated, definitions_out, aliases, role_lookup = {}, {}, [], {}, dict(existing_roles)
    missing_images = []
    for name, role in sorted(roles.items()):
        if name not in used_sprites:
            continue
        definition = sprites[name]
        text, node = definition['text'], definition['node']
        current_texture = value(text, node, 'texturefile', '')
        upstream = previous_manifest.get('sprites', {}).get(name, {}).get('source') if current_texture.startswith('gfx/interface/win95/major/') else None
        source = source_image(definition, game, upstream)
        if not source:
            missing_images.append(name)
            continue
        with Image.open(source) as image:
            image = image.convert('RGBA')
            size = image.size
            frames = int(value(text, node, 'noOfFrames', '1'))
            if size[0] % frames:
                raise ValueError(f'Invalid frame geometry for {name}: {size}/{frames}')
            # Native PNG outer alpha often includes intentional placement/shadow margins.
            frame_bounds = [image.crop((i * size[0] // frames, 0, (i + 1) * size[0] // frames, size[1])).getbbox() for i in range(frames)]
            bbox = (min(b[0] for b in frame_bounds if b), min(b[1] for b in frame_bounds if b),
                    max(b[2] for b in frame_bounds if b), max(b[3] for b in frame_bounds if b)) if any(frame_bounds) else None
        role_lookup[name] = role
        metadata[name] = dict(size=size, frames=frames, role=role)
        if 'gfx/interface/win95/' in str(source) or name.startswith('GFX_bsm_') and role != 'panel':
            continue
        alias = PREFIX + name
        texture = f'gfx/interface/win95/major/{name}.png'
        aliases[name] = alias
        if profile := material_profiles.get(name):
            generated[name] = render_material(image, frames, profile)
            metadata[name]['material_profile'] = profile
        else:
            generated[name] = flat_image(size, frames, role, bbox, image.getchannel('A'),
                                         selected=bool(re.search(r'_(?:hl|selected|highlighted|active)$', name)))
        if regions := preserve_regions.get(name):
            # Reviewed content baked into an otherwise neutral panel (factory glyphs).
            for region in regions:
                a, b, c, d = region['source']
                px, py = region['position']
                if not (0 <= a < c <= size[0] and 0 <= b < d <= size[1]
                        and 0 <= px <= size[0] - (c - a) and 0 <= py <= size[1] - (d - b)):
                    raise ValueError(f'Invalid preserved content region: {name}: {region}')
                if region.get('mode') == 'pictogram':
                    generated[name].alpha_composite(pictogram_patch(image, (a, b, c, d)), (px, py))
                else:
                    generated[name].paste(image.crop((a, b, c, d)), (px, py))
            metadata[name]['preserve_regions'] = regions
        if grids := grid_regions.get(name):
            # Slot count is gameplay information: the naval strip has 1/2/3 rows.
            draw = ImageDraw.Draw(generated[name])
            fw = size[0] // frames
            for grid in grids:
                frame = grid.get('frame', 0)
                gx, gy = grid['position']
                cw, ch = grid['cell']
                cols, rows = grid['slots']
                if not (0 <= frame < frames and gx >= 0 and gy >= 0 and cw > 2 and ch > 2
                        and cols > 0 and rows > 0 and gx + cw * cols <= fw and gy + ch * rows <= size[1]):
                    raise ValueError(f'Invalid production slot grid: {name}: {grid}')
                for row in range(rows):
                    for col in range(cols):
                        x, y = frame * fw + gx + cw * col, gy + ch * row
                        draw.rectangle((x + 1, y + 1, x + cw - 2, y + ch - 2), fill='#ffffff', outline='#808080')
            metadata[name]['grid_regions'] = grids
        name_prop, texture_prop = prop(text, node, 'name'), prop(text, node, 'texturefile')
        block = cloned_block(text, node, [(name_prop[1], name_prop[2], alias), (texture_prop[1], texture_prop[2], texture)])
        definitions_out.append(block)
        definition_path = str(definition['path'].relative_to(game if definition['path'].is_relative_to(game) else MOD))
        if name in runtime_bindings:
            definition_path = previous_manifest.get('sprites', {}).get(name, {}).get('definition', definition_path)
        metadata[name].update(alias=alias, texture=texture,
                              source=upstream or value(text, node, 'texturefile'), definition=definition_path)
    if missing_images:
        raise ValueError(f'Cannot generate missing source images: {missing_images}')

    image_brightness = {}

    def surface(name):
        name = original(name)
        if name in role_lookup:
            return 'white' if role_lookup[name] == 'header' else 'black'
        if name in ('GFX_tiled_window_transparent', 'GFX_tiled_window_transparent_transparent', 'GFX_tiled_empty'):
            return None
        if name in image_brightness:
            return image_brightness[name]
        result = None
        if name in sprites and (source := source_image(sprites[name], game)):
            with Image.open(source) as image:
                image = image.convert('RGBA')
                if ImageStat.Stat(image.getchannel('A')).mean[0] > 140:
                    sample = ImageStat.Stat(image.convert('RGB').resize((24, 24))).mean
                    result = 'black' if sum(sample) / 3 > 140 else 'white'
        image_brightness[name] = result
        return result

    font_usage, reports, updated = {}, [], {}
    for path, text in texts.items():
        ns, edits = ast[path], []
        sizes = {}
        root_names = {}

        def widget_root(node):
            while node.parent and node.parent.key.lower() != 'guitypes':
                node = node.parent
            if id(node) not in root_names:
                root_names[id(node)] = value(text, node, 'name', '')
            return root_names[id(node)]

        def widget_path(node):
            names = []
            while node.parent and node.parent.key.lower() != 'guitypes':
                names.append(value(text, node, 'name', node.key))
                node = node.parent
            return '/'.join(reversed(names))

        def extent(node):
            if node is None:
                return (1280, 720)
            if id(node) not in sizes:
                parent_size = extent(node.parent)
                size = pair(text, node, 'size', 'width', 'height', parent_size) or pair(text, node, 'size', extent=parent_size)
                sizes[id(node)] = tuple(size[i] if size and size[i] is not None and size[i] > 0 else parent_size[i] for i in range(2))
            return sizes[id(node)]

        def rectangle(node):
            pos = pair(text, node, 'position', extent=extent(node.parent)) or (0, 0)
            if None in pos:
                return None
            sp = sprite(text, node)
            name = original(sp[0]) if sp else None
            size = pair(text, node, 'size', 'width', 'height', extent(node.parent)) or pair(text, node, 'size', extent=extent(node.parent))
            if not size and name in metadata:
                data = metadata[name]
                size = data['size'][0] / data['frames'], data['size'][1]
            if not size or None in size:
                return None
            scale = numeric(value(text, node, 'scale', '1')) or 1
            width, height = size[0] * scale, size[1] * scale
            x, y = pos
            orientation = value(text, node, 'Orientation', 'upper_left').lower()
            origo = value(text, node, 'Origo', 'upper_left').lower()
            pw, ph = extent(node.parent)
            if 'right' in orientation:
                x += pw
            if 'lower' in orientation or 'bottom' in orientation:
                y += ph
            if orientation == 'center':
                x += pw / 2
                y += ph / 2
            if 'right' in origo:
                x -= width
            if 'lower' in origo or 'bottom' in origo:
                y -= height
            return x, y, width, height

        def shade_for(node):
            if sp := sprite(text, node):
                return surface(sp[0])
            pos = pair(text, node, 'position', extent=extent(node.parent))
            # A navy sibling header is a separate sprite inside otherwise silver windows.
            if pos and None not in pos and node.parent:
                candidates = []
                for sibling in node.parent.children:
                    if sibling is node or sibling.start > node.start:
                        continue
                    sp = sprite(text, sibling)
                    if not sp or original(sp[0]) not in role_lookup:
                        continue
                    rect = rectangle(sibling)
                    if rect and rect[0] <= pos[0] + 3 < rect[0] + rect[2] and rect[1] <= pos[1] + 8 < rect[1] + rect[3]:
                        candidates.append((rect[2] * rect[3], surface(sp[0])))
                if candidates:
                    return min(candidates, key=lambda c: c[0])[1]
            parent = node.parent
            while parent:
                for bg in reversed(parent.children):
                    if bg.key.lower() != 'background':
                        continue
                    sp = sprite(text, bg)
                    if sp and (shade := surface(sp[0])):
                        return shade
                parent = parent.parent
            root = widget_root(node)
            return 'black' if root in light_roots or path.name in light_files or str(path.relative_to(MOD / 'interface')).removeprefix('replace/') in light_files else 'white' if root in dark_roots else None

        changed_fonts, unresolved, unresolved_contexts = 0, [], []
        for node in ns:
            if sp := sprite(text, node):
                name = original(sp[0])
                if name in aliases:
                    edits.append((sp[1], sp[2], aliases[name]))
                elif sp[0].startswith(PREFIX):
                    # A later review may move a previously themed image to preserve.
                    edits.append((sp[1], sp[2], name))
            for key in ('font', 'buttonFont'):
                fm = prop(text, node, key)
                if not fm:
                    continue
                name = baseline_font(fm[0])
                forced = next((item for item in font_overrides if item['gui'].removeprefix('replace/') == str(path.relative_to(MOD / 'interface')).removeprefix('replace/')
                               and item['root'] == widget_root(node) and item['widget'] == value(text, node, 'name')
                               and (not item.get('path') or item['path'] == widget_path(node))), None)
                if (path.name in preserve_font_files or widget_root(node) in preserve_roots) and not forced:
                    if fm[0].startswith(FONT_PREFIX):
                        edits.append((fm[1], fm[2], name))
                    continue
                # Hand-authored BSM fonts encode established silver/navy/illustration
                # contrast. Only generic native and earlier shared clones are recolored.
                if name.startswith('bsm_') and not name.startswith('bsm_w95_') and widget_root(node) not in recolor_bsm_roots and not forced:
                    if fm[0].startswith(FONT_PREFIX):
                        edits.append((fm[1], fm[2], name))
                    continue
                shade = forced['shade'] if forced else shade_for(node)
                if forced and forced.get('source'):
                    name = forced['source']
                if shade and name in fonts:
                    new = font_name(name, shade)
                    font_usage[new] = name, shade
                    if fm[0] != new:
                        changed_fonts += 1
                    edits.append((fm[1], fm[2], new))
                elif not shade and not fm[0].startswith(('bsm_', 'Main_14_black')):
                    unresolved.append(value(text, node, 'name', node.key))
                    unresolved_contexts.append(dict(root=widget_root(node), name=value(text, node, 'name', ''),
                                                    font=name, line=text.count('\n', 0, node.start) + 1))
                elif fm[0].startswith(FONT_PREFIX):
                    edits.append((fm[1], fm[2], name))
        output = replacements(text, edits)
        if contract(output) != contract(text):
            raise ValueError(f'Functional GUI token changed: {path}')
        updated[path] = output
        reports.append(dict(gui=str(path.relative_to(MOD / 'interface')), new=not path.exists(),
                            safety_sha256=hashlib.sha256(json.dumps(contract(text)).encode()).hexdigest(),
                            font_bindings=sum(1 for e in edits if e[2].startswith(FONT_PREFIX)),
                            changed_fonts=changed_fonts, sprite_bindings=sum(1 for e in edits if e[2].startswith(PREFIX)),
                            unresolved_fonts=unresolved, unresolved_contexts=unresolved_contexts))

    font_blocks = []
    for alias, (name, shade) in sorted(font_usage.items()):
        for definition in [fonts[name], *overrides.get(name, [])]:
            text, node = definition['text'], definition['node']
            nm = prop(text, node, 'name')
            changes = [(nm[1], nm[2], alias)]
            if node.key.lower() == 'bitmapfont':
                color = prop(text, node, 'color')
                if not color:
                    raise ValueError(f'Font has no tint: {name}')
                changes.append((color[1], color[2], '0xffffffff' if shade == 'white' else '0xff000000'))
            block = cloned_block(text, node, changes)
            if shade == 'black':
                # C++ values and localisation can select inline colours even when
                # the base tint is black. Keep their meaning legible on light faces.
                palette = {'T': (0, 0, 0), 'W': (0, 0, 0), 'G': (0, 112, 24),
                           'R': (176, 0, 0), 'Y': (128, 92, 0), 'H': (128, 92, 0),
                           'O': (168, 72, 0), 'g': (96, 96, 96), 'B': (0, 0, 128)}
                color_edits = []
                color_sections = []
                for section in nodes(block):
                    if section.key.lower() != 'textcolors':
                        continue
                    color_sections.append(section)
                    present = {entry.key for entry in section.children}
                    for entry in section.children:
                        if entry.key in palette:
                            color_edits.append((entry.body, entry.end - 1, ' ' + ' '.join(map(str, palette[entry.key])) + ' '))
                    missing = ''.join('\n\t\t\t' + key + ' = { ' + ' '.join(map(str, rgb)) + ' }'
                                      for key, rgb in palette.items() if key not in present)
                    if missing:
                        color_edits.append((section.end - 1, section.end - 1, missing + '\n\t\t'))
                if not color_sections and node.key.lower() == 'bitmapfont':
                    root_node = nodes(block)[0]
                    colors = '\n\t\ttextcolors = { ' + ' '.join(key + ' = { ' + ' '.join(map(str, rgb)) + ' }'
                                                                   for key, rgb in palette.items()) + ' }\n\t'
                    color_edits.append((root_node.end - 1, root_node.end - 1, colors))
                block = replacements(block, color_edits)
            font_blocks.append(block)
    gfx_output = '# Generated by tools/generate_win95_major_gui.py; reviewed chrome only.\nspriteTypes = {\n' + '\n'.join(definitions_out) + '\n}\n'
    gfx_output = re.sub(r'(?m)[ \t]+$', '', gfx_output)
    font_output = '# Generated clones retain native glyph metrics and language overrides.\nbitmapfonts = {\n' + '\n'.join(font_blocks) + '\n}\n'
    # A few C++ widgets replace their GUI sprite at runtime (e.g. the no-DLC
    # politics backdrop). Bind those reviewed original IDs in the owning MOD GFX.
    # Retain all unrelated definitions, including custom BSM political artwork.
    runtime_outputs = {}
    for name, relative in sorted(runtime_bindings.items()):
        target = MOD / 'interface' / relative
        contents = runtime_outputs.get(target, read(target) if target.exists() else 'spriteTypes = {\n}\n')
        parsed = nodes(contents)
        existing = next((n for n in parsed if value(contents, n, 'name') == name and n.key.lower() in TYPES), None)
        definition = sprites[name]
        tm = prop(definition['text'], definition['node'], 'texturefile')
        replacement = cloned_block(definition['text'], definition['node'], [(tm[1], tm[2], metadata[name]['texture'])])
        if existing:
            contents = contents[:existing.start] + replacement + contents[existing.end:]
        else:
            wrapper = next(n for n in parsed if n.key.lower() == 'spritetypes')
            contents = contents[:wrapper.end - 1] + '\n\t' + replacement + '\n' + contents[wrapper.end - 1:]
        runtime_outputs[target] = contents
    # Fail before touching files if a changed configuration would strand an alias
    # in an unlisted GUI; listed GUIs automatically restore removed bindings above.
    available_sprites, available_fonts = set(aliases.values()), set(font_usage)
    all_gui_paths = set((MOD / 'interface').rglob('*.gui')) | set(updated)
    for path in all_gui_paths:
        candidate = updated[path] if path in updated else read(path)
        for node in nodes(candidate):
            if (sp := sprite(candidate, node)) and sp[0].startswith(PREFIX) and sp[0] not in available_sprites:
                raise ValueError(f'Unresolved theme sprite in {path}: {sp[0]}; re-add GUI to reviewed targets')
            for key in ('font', 'buttonFont'):
                name = value(candidate, node, key, '')
                if name.startswith(FONT_PREFIX) and name not in available_fonts:
                    raise ValueError(f'Unresolved theme font in {path}: {name}; re-add GUI to reviewed targets')
    records = {name: dict(data, sha256=hashlib.sha256(generated[name].tobytes()).hexdigest())
               for name, data in metadata.items() if name in generated}
    manifest = dict(sprites=records, guis=reports, font_clones=len(font_usage), runtime_sprite_bindings=runtime_bindings,
                    documented_layout_fixes=documented_layout_fixes)
    if args.plan:
        print(json.dumps(dict(gui_files=len(guis), new_gui_files=sum(r['new'] for r in reports),
                              textures=len(generated), fonts=len(font_usage),
                              gui_bindings=reports, unused_configured_sprites=sorted(set(roles) - used_sprites)), indent=2, ensure_ascii=False))
        return
    if args.check:
        stored = json.loads(read(MANIFEST))
        if stored['sprites'] != json.loads(json.dumps(records)):
            raise ValueError('Texture manifest drift')
        if {r['gui']: r['safety_sha256'] for r in stored['guis']} != {r['gui']: r['safety_sha256'] for r in reports}:
            raise ValueError('GUI widget/callback/layout contract drift')
        for name, image in generated.items():
            with Image.open(OUT / f'{name}.png') as actual:
                if actual.mode != 'RGBA' or actual.size != image.size or actual.tobytes() != image.tobytes():
                    raise ValueError(f'Texture drift: {name}')
        if read(GFX) != gfx_output or read(FONTS) != font_output:
            raise ValueError('Generated definition drift')
        for path, text in updated.items():
            if not path.exists() or read(path) != text:
                raise ValueError(f'GUI theme drift: {path}')
        for path, text in runtime_outputs.items():
            if not path.exists() or read(path) != text:
                raise ValueError(f'Runtime sprite binding drift: {path}')
    else:
        # Do not overwrite edits made by another task while this long pass ran.
        for target, source in guis.items():
            if read(source) != texts[target]:
                raise ValueError(f'GUI changed during generation; retry with current edits: {source}')
        OUT.mkdir(parents=True, exist_ok=True)
        for name, image in generated.items():
            image.save(OUT / f'{name}.png')
        GFX.write_text(gfx_output, encoding='utf-8')
        FONTS.write_text(font_output, encoding='utf-8')
        for path, text in runtime_outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')
        for path, text in updated.items():
            if not path.exists() or read(path) != text:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding='utf-8')
        MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'PASS: {len(guis)} GUI files, {len(generated)} textures, {len(font_usage)} font clones; widget/callback tokens retained')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--plan', action='store_true')
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--game-dir')
    run(parser.parse_args())
