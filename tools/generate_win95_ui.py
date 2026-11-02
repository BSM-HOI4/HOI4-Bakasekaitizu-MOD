#!/usr/bin/env python3
"""Generate shared Win95-inspired chrome. Requires Pillow; --check validates outputs.
Original textures, sprite IDs, dimensions, frame counts and effects are preserved.
Light silver faces follow the Windows 95 palette; GUI labels use black fonts.
"""
from pathlib import Path
import argparse
import json
import re
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'bakasekai'
OUT = MOD / 'gfx/interface/win95/shared'
FILES = ['core.gfx', 'launcher.gfx']
BLOCK = re.compile(r'(?:corneredTileSpriteType|textSpriteType|spriteType)\s*=\s*\{.*?\n\t\}', re.S)
TEX = re.compile(r'(texturefile\s*=\s*")([^"]+)(")', re.I)
MANIFEST = OUT / 'manifest.json'

def selected(name):
    return (name.startswith('GFX_tiled_window') and not any(x in name for x in ('transparent', 'glow', 'scrollbar', 'color_picker', 'selectable'))) or name in {
        'GFX_tiled_plain_bg', 'GFX_tiled_header_1', 'GFX_tiled_generic_bg_1',
        'GFX_subview_header_bg_300x101', 'GFX_subview_header_bg_375x101',
    } or bool(re.fullmatch(r'GFX_button_\d+x\d+(?:_light|_alt|_2)?', name)) or bool(re.fullmatch(r'button_type_[1245679]', name))

def bevel(draw, box, pressed=False):
    x,y,r,b = box
    hi,lo = ('#404040','#ffffff') if pressed else ('#ffffff','#202020')
    for i in range(2):
        draw.line((x+i,b-i,x+i,y+i,r-i,y+i), fill=hi)
        draw.line((r-i,y+i,r-i,b-i,x+i,b-i), fill=lo)
    draw.rectangle((x+2,y+2,r-2,b-2), outline='#808080')

def make(size, frames, name):
    w,h=size
    assert w % frames == 0
    fw=w//frames
    im=Image.new('RGBA',size,(192,192,192,255)); d=ImageDraw.Draw(im)
    for f in range(frames):
        x=f*fw
        bevel(d,(x,0,x+fw-1,h-1),f==1)
        if 'header' in name:
            d.rectangle((x+3,3,x+fw-4,h-4),fill='#000080')
        elif 'button' in name:
            if f==2: d.rectangle((x+3,3,x+fw-4,h-4),fill='#d4d0c8')
    return im

def run(check=False):
    records=[]
    old = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else []
    originals={(r['file'],r['name']):r['source'] for r in old}
    for filename in FILES:
        p=MOD/'interface/replace'/filename
        text=p.read_text(encoding='utf-8-sig')
        def replace(m):
            block=m.group(); nm=re.search(r'name\s*=\s*"([^"]+)"',block)
            if not nm or not selected(nm[1]): return block
            name=nm[1]; tm=TEX.search(block)
            if not tm:return block
            source=originals.get((filename,name),tm[2])
            relative=re.sub('/+','/',source)
            src=MOD/relative
            if not src.exists() and src.with_suffix('.dds').exists():
                source = str(Path(relative).with_suffix('.dds'))
                relative = source
                src = MOD / relative
            if not src.exists():
                src = Path.home() / 'Library/Application Support/Steam/steamapps/common/Hearts of Iron IV' / relative
            if not src.exists():
                print(f'SKIP existing missing source: {source}')
                return block
            with Image.open(src) as original: size=original.size
            fm=re.search(r'noOfFrames\s*=\s*(\d+)',block); frames=int(fm[1]) if fm else 1
            dest=OUT/(name+'.png'); texture=dest.relative_to(MOD).as_posix()
            generated=make(size,frames,name)
            if check:
                with Image.open(dest) as actual:
                    assert actual.size==size and actual.convert('RGBA').tobytes()==generated.tobytes(),dest
                assert tm[2]==texture
            else:
                OUT.mkdir(parents=True,exist_ok=True); generated.save(dest)
            records.append(dict(file=filename,name=name,source=source,texture=texture,size=list(size),frames=frames))
            return TEX.sub(lambda t:t[1]+texture+t[3],block,count=1)
        updated=BLOCK.sub(replace,text)
        if not check:p.write_text(updated,encoding='utf-8')
    if check: assert records==old
    else: MANIFEST.write_text(json.dumps(records,indent=2)+'\n')
    print(f'PASS: {len(records)} sprite bindings, {len({r["texture"] for r in records})} textures; dimensions, RGBA and frames verified')
    # Contact sheet is an asset preview, not a screenshot of the game.
    if not check:
        preview=Image.new('RGB',(760,420),'#008080'); d=ImageDraw.Draw(preview)
        d.rectangle((35,35,725,385),fill='#c0c0c0');bevel(d,(35,35,725,385))
        d.rectangle((39,39,721,68),fill='#000080'); d.text((49,47),'BAKASEKAI - Windows 95 inspired UI',fill='white')
        d.text((55,90),'Classic light silver faces with black labels.',fill='black')
        for i,label in enumerate(['Research','Construction','Trade','Politics']):
            x=55+i*165; d.rectangle((x,130,x+150,165),fill='#c0c0c0');bevel(d,(x,130,x+150,165),i==1); d.text((x+15,142),label,fill='black')
        d.rectangle((55,190,705,315),fill='#ffffff');bevel(d,(55,190,705,315),True)
        d.text((70,208),'Shared windows / headers / buttons',fill='black')
        d.text((70,235),'Pixel-aligned bevels / navy title bars / teal desktop',fill='black')
        preview.save(OUT/'preview.png')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');run(parser.parse_args().check)
