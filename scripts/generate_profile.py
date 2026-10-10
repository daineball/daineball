#!/usr/bin/env python3
"""Generate a standalone GitHub-safe SVG profile banner. Standard library only."""
from pathlib import Path
from datetime import datetime, timezone
from html import escape
import json, os, urllib.request
ROOT = Path(__file__).resolve().parents[1]
USER = os.getenv('GITHUB_PROFILE_USER', 'daineball')
TOKEN = os.getenv('GH_STATS_TOKEN') or os.getenv('GITHUB_TOKEN')

def github_json(path):
    req=urllib.request.Request('https://api.github.com/'+path,headers={'Accept':'application/vnd.github+json','User-Agent':'GoFirestorm-Profile','Authorization':f'Bearer {TOKEN}'} if TOKEN else {'Accept':'application/vnd.github+json','User-Agent':'GoFirestorm-Profile'})
    with urllib.request.urlopen(req,timeout=15) as resp: return json.load(resp)

stats={'repos':'—','followers':'—','public_gists':'—'}
try:
    data=github_json('users/'+USER)
    stats={k:str(data.get(k,'—')) for k in stats}
except Exception as e:
    print('GitHub API unavailable; rendering fallback:',type(e).__name__)

W,H=1080,490
out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="GoFirestorm terminal profile for {escape(USER)}">',
'<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#0a1018"/><stop offset="1" stop-color="#101923"/></linearGradient><linearGradient id="fire" x2="0" y2="1"><stop stop-color="#ffd16d"/><stop offset=".55" stop-color="#ff8d35"/><stop offset="1" stop-color="#e24a29"/></linearGradient></defs>',
'<rect width="1080" height="490" rx="18" fill="url(#bg)"/>','<rect x="1" y="1" width="1078" height="488" rx="17" fill="none" stroke="#2b3947"/>',
'<rect x="1" y="1" width="1078" height="48" rx="17" fill="#151e29"/>','<rect x="1" y="32" width="1078" height="17" fill="#151e29"/>',
'<circle cx="29" cy="24" r="7" fill="#ff605c"/><circle cx="51" cy="24" r="7" fill="#ffbd44"/><circle cx="73" cy="24" r="7" fill="#00ca4e"/>',
'<text x="540" y="30" fill="#92a2b3" font-family="monospace" font-size="14" text-anchor="middle">gofirestorm — profile@terminal</text>',
'<text x="35" y="84" fill="#ff9e47" font-family="monospace" font-size="17" font-weight="bold">GOFIRESTORM // SYSTEM PROFILE</text>',
'<text x="35" y="109" fill="#7893a6" font-family="monospace" font-size="12">AI COMPUTE · INFERENCE · TRAINING · ORCHESTRATION</text>',
'<line x1="35" y1="126" x2="1045" y2="126" stroke="#2a3a48"/>',
'<path d="M270 154 C230 210 292 236 253 293 C252 247 220 245 222 202 C182 266 201 315 238 348 C196 335 174 301 171 273 C146 352 205 409 272 411 C345 406 393 347 366 272 C363 305 342 334 307 348 C351 307 355 264 316 202 C318 244 286 246 289 292 C248 239 309 211 270 154Z" fill="url(#fire)" opacity=".95"/>',
'<path d="M270 274 C251 313 235 333 249 365 C258 391 282 389 293 365 C306 335 289 309 270 274Z" fill="#111922"/>',
'<text x="270" y="440" text-anchor="middle" fill="#ff9e47" font-family="monospace" font-size="18" font-weight="bold">GO // FIRESTORM</text>',
'<line x1="480" y1="148" x2="480" y2="449" stroke="#2a3a48"/>']
def line(y,key,value,color='#dce6ef'):
    out.append(f'<text x="510" y="{y}" fill="#e49c5d" font-family="monospace" font-size="15">{escape(key)}</text>')
    out.append(f'<text x="760" y="{y}" fill="{color}" font-family="monospace" font-size="15">{escape(value)}</text>')
line(171,'Handle', '@'+USER)
line(207,'Primary stack','Go / Rust / C++')
line(243,'Compute','ROCm / GPU kernels')
line(279,'Orchestration','Kubernetes / PodBro')
line(315,'Inference','GoInferno / llama.cpp')
line(351,'Training','GoIgnite / GoSpark')
line(387,'Public repos',stats['repos'],'#8ee1b1')
line(415,'Followers',stats['followers'],'#8ee1b1')
out += ['<line x1="510" y1="436" x2="1045" y2="436" stroke="#2a3a48"/>',
'<text x="510" y="463" fill="#8ee1b1" font-family="monospace" font-size="13">$ building AI infrastructure from the kernels up_</text>',
'</svg>']
(ROOT/'assets'/'gofirestorm-terminal.svg').write_text('\n'.join(out)+'\n',encoding='utf-8')
print('Wrote assets/gofirestorm-terminal.svg')
