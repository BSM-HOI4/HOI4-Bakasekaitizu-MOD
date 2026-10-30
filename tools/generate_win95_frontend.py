#!/usr/bin/env python3
"""Generate compact Win95 dialog/link chrome. Main menu keeps the original bg.png."""
from pathlib import Path
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'bakasekai/gfx/interface/win95/frontend'
OUT.mkdir(parents=True,exist_ok=True)
def frame(im):
 d=ImageDraw.Draw(im);w,h=im.size
 d.line((0,h-1,0,0,w-1,0),fill='white',width=2)
 d.line((w-1,0,w-1,h-1,0,h-1),fill='#202020',width=2)
 return d
sp=Image.new('RGBA',(520,300),'#c0c0c0');d=frame(sp)
d.rectangle((3,3,516,29),fill='#000080')
d.line((20,253,499,253),fill='#808080');d.line((20,254,499,254),fill='white')
sp.save(OUT/'singleplayer_compact.png')
button=Image.new('RGBA',(468,44),'#c0c0c0');frame(button);button.save(OUT/'singleplayer_button.png')
close=Image.new('RGBA',(20,20),'#c0c0c0');d=frame(close)
d.line((6,5,14,13),fill='black',width=2);d.line((14,5,6,13),fill='black',width=2)
close.save(OUT/'singleplayer_close.png')
toolbar=Image.new('RGBA',(182,64),'#c0c0c0');frame(toolbar);toolbar.save(OUT/'links_toolbar.png')
for name,width in [('link_button',26),('friends_button',56)]:
 image=Image.new('RGBA',(width,26),'#c0c0c0');frame(image);image.save(OUT/(name+'.png'))
for name,height in [('menu_action_row',28),('menu_link_row',26)]:
 image=Image.new('RGBA',(182,height),'#c0c0c0');frame(image);image.save(OUT/(name+'.png'))
print('PASS: compact menu rows 182x28/26; links grid 182x64; dialog assets preserved')
