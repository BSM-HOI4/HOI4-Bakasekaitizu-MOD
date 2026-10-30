#!/usr/bin/env python3
"""Generate country-selector chrome without altering flags, portraits or original art."""
from pathlib import Path
import argparse
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'bakasekai/gfx/interface/win95/country_selection'

def bevel(d, box, inset=False):
    x,y,r,b=box
    a,z=('#808080','#ffffff') if inset else ('#ffffff','#404040')
    d.line((x,b,x,y,r,y),fill=a)
    d.line((r,y,r,b,x,b),fill=z)
    d.line((x+1,b-1,x+1,y+1,r-1,y+1),fill='#202020' if inset else '#dfdfdf')
    d.line((r-1,y+1,r-1,b-1,x+1,b-1),fill='#c0c0c0' if inset else '#808080')

def assets():
    main=Image.new('RGBA',(1200,690),'#c0c0c0');d=ImageDraw.Draw(main)
    bevel(d,(0,0,1199,689));d.rectangle((4,4,1195,32),fill='#000080')
    d.rectangle((12,42,1187,335),fill='#ffffff');bevel(d,(12,42,1187,335),True)
    for x,w in [(12,350),(374,400),(786,402)]:
        d.rectangle((x,348,x+w-1,629),fill='#ffffff');bevel(d,(x,348,x+w-1,629),True)
        d.rectangle((x+2,350,x+w-3,377),fill='#000080')
    d.line((12,638,1187,638),fill='#808080');d.line((12,639,1187,639),fill='white')
    result={'window.png':main}
    for name,w,h,label in [('major_card.png',150,210,True),('minor_card.png',95,58,False),('mini_card.png',62,40,False)]:
        im=Image.new('RGBA',(w*2,h),(0,0,0,0));draw=ImageDraw.Draw(im)
        for state in range(2):
            x=state*w
            # The hit-target sprite is drawn above portraits and flags: keep its centre transparent.
            draw.rectangle((x,0,x+w-1,h-1),outline='#c0c0c0',width=4)
            bevel(draw,(x,0,x+w-1,h-1))
            if state:
                draw.rectangle((x+3,3,x+w-4,h-4),outline='#000080',width=2)
            if label:
                draw.rectangle((x+4,174,x+w-5,h-5),fill='#d8e4fa' if state else '#e7e7e7')
                draw.line((x+4,173,x+w-5,173),fill='#808080')
        result[name]=im
    portrait=Image.new('RGBA',(76,100),(0,0,0,0));d=ImageDraw.Draw(portrait);bevel(d,(0,0,75,99),True)
    result['portrait_frame.png']=portrait
    return result

def run(check):
    OUT.mkdir(parents=True,exist_ok=True)
    for name,wanted in assets().items():
        path=OUT/name
        if check:
            with Image.open(path) as actual:
                assert actual.mode=='RGBA' and actual.size==wanted.size
                assert actual.tobytes()==wanted.tobytes(),path
        else:wanted.save(path)
    print('PASS: country selector 5 textures / RGBA / frame geometry / pixels' if check else 'Generated country selector 5 textures')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');run(p.parse_args().check)
