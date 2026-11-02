#!/usr/bin/env python3
"""Regenerate the static scenario focus preview from current source files.

Run from the repository root. This is not a game screenshot.
"""
import sys,json,re,html
from pathlib import Path
sys.path.insert(0,'tools')
from verify_scenario_focus_layout import *
meta = {}
for name in ('france', 'spain', 'nsi'):
 _, fs = load(f'bakasekai/common/national_focus/{name}.txt')
 bounds = LAYOUT['countries'][name]['category_bounds']
 meta[name] = {'categories': {fid: 'political' if resolve(fs, fid)[0] < bounds[0] else 'industry' if resolve(fs, fid)[0] < bounds[1] else 'military' for fid in fs}}
from datetime import datetime
from zoneinfo import ZoneInfo
updated = datetime.now(ZoneInfo('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S JST')
loc={}
for p in Path('bakasekai/localisation/japanese').rglob('*.yml'):
 for k,v in re.findall(r'^\s*([^\s:]+):\d*\s+"(.*)"',p.read_text(encoding='utf-8-sig'),re.M):loc[k]=v
colors={'political':'#d5e6ff','industry':'#ffe6ad','military':'#bce8d5'}
labels={'political':'政治・外交','industry':'産業・研究','military':'軍事'}
sections=[]
nw, nh = GEOMETRY["node_width"], GEOMETRY["node_height"]
for name,jp in [('france','フランス'),('spain','スペイン'),('nsi','北センチネル島')]:
 _,fs=load(f'bakasekai/common/national_focus/{name}.txt');pos={k:resolve(fs,k) for k in fs};minx=min(x for x,y in pos.values()); maxx=max(x for x,y in pos.values());maxy=max(y for x,y in pos.values())
 width=(maxx-minx)*GEOMETRY["x_step"]+240;height=(maxy+1)*GEOMETRY["y_step"]+120
 def xy(fid):x,y=pos[fid];return ((x-minx)*GEOMETRY["x_step"]+120,y*GEOMETRY["y_step"]+80)
 parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
 for cat in colors:
  pts=[pos[k][0] for k in fs if meta[name]['categories'][k]==cat];left=(min(pts)-minx)*GEOMETRY["x_step"]+20;right=(max(pts)-minx)*GEOMETRY["x_step"]+220
  parts.append(f'<rect x="{left}" width="{right-left}" y="0" height="{height}" fill="{colors[cat]}" opacity=".25"/><text x="{left+12}" y="28" font-size="20">{labels[cat]}</text>')
 for fid,f in fs.items():
  for _,_,b in blocks(f['b'],'prerequisite'):
   for pre in re.findall(r'\bfocus\s*=\s*(\w+)',b):
    px,py=xy(pre);x,y=xy(fid)
    parts.append(f'<path d="M {px},{py+nh/2} L {x},{y-nh/2}" fill="none" stroke="#a2a9b5" stroke-width="1.5"/>')
 for fid in fs:
  x,y=xy(fid);cat=meta[name]['categories'][fid];label=re.sub(r'§.','',loc.get(get(fs[fid]['b'],'text',fid),fid));lines=[label[i:i+11] for i in range(0,len(label),11)][:3]
  parts.append(f'<g data-focus-id="{fid}"><title>{html.escape(fid+" / "+label)}</title><rect x="{x-nw/2}" y="{y-nh/2}" width="176" height="60" rx="7" fill="{colors[cat]}" stroke="#617082"/>')
  for i,line in enumerate(lines):parts.append(f'<text x="{x}" y="{y-(len(lines)-1)*8+i*16+5}" text-anchor="middle" font-size="13">{html.escape(line)}</text>')
  parts.append('</g>')
 parts.append('</svg>');Path('documents/verification/scenario-focus-layout-2026-11-01').mkdir(parents=True,exist_ok=True);Path(f'documents/verification/scenario-focus-layout-2026-11-01/{name}.svg').write_text(''.join(parts));sections.append(f'<section id="{name}" '+('' if name=='france' else 'hidden')+'>'+''.join(parts)+'</section>')
text='''<!doctype html><html lang="ja"><meta charset="utf-8"><title>国家方針・分野別独立・政治外交は共通親</title><style>body{margin:0;font:15px system-ui;background:#f8fafc;color:#17263b}header{position:sticky;top:0;z-index:2;background:#17263b;color:white;padding:14px 20px}select,input{margin:0 12px}main{padding:20px;overflow:auto;height:calc(100vh - 125px)}section{width:max-content;transform-origin:top left}p{margin:6px 0;font-size:13px;color:#ced8e6}</style><header><b>政治・外交は共通の親／産業・軍事は独立</b><select id="country"><option value="france">フランス（117本）</option><option value="spain">スペイン（108本）</option><option value="nsi">北センチネル島（71本）</option></select><label>倍率<input id="zoom" type="range" min="20" max="100" value="50"></label><p>政治・外交の枝は共通の親につながります。ボックス幅と余白を検証済み。接続元との上下間隔は1段に統一した静的な座標図です。バニラのように政治・外交／産業・研究／軍事がそれぞれ独立した起点を持ちます。横・縦にスクロールできます。北センチネル島の共有102本は図から省略し、配置検証には含めています。実ゲーム画像ではありません。</p></header><main>'''+''.join(sections)+'''</main><script>const sections=document.querySelectorAll('section');const country=document.getElementById('country'),zoom=document.getElementById('zoom');function update(){for(const section of sections){section.hidden=section.id!==country.value;section.style.zoom=zoom.value/100}}country.onchange=update;zoom.oninput=update;update();</script></html>'''
out=Path('documents/verification/scenario-focus-layout-2026-11-01');out.mkdir(parents=True,exist_ok=True);(out/'preview.html').write_text(text.replace('</b><select', '</b><span style="margin:0 12px">分野別独立・政治外交は共通親・更新 '+updated+'</span><select'))
