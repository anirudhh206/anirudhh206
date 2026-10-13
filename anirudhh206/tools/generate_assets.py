#!/usr/bin/env python3
"""
Regenerates every hand-designed SVG in assets/ (hero, divider, section headers,
focus panel, project cards, stack, badges, typing line, footer) plus the
placeholder cards that GitHub Actions overwrite on their first run.

Edit the CONFIG block, then:   python3 tools/generate_assets.py

Pure standard library. Every SVG is self-contained (no external fonts/images),
because GitHub renders README SVGs in a sandbox that blocks external requests.
"""
import math
import pathlib
import random
from xml.sax.saxutils import escape as esc

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
PROJ = ASSETS / "projects"
PROFILE = ROOT / "profile"
CONTRIB3D = ROOT / "profile-3d-contrib"
for d in (ASSETS, PROJ, PROFILE, CONTRIB3D):
    d.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------------
# CONFIG - edit text here
# ----------------------------------------------------------------------------
NAME = "ANIRUDH VASHISTH"
HANDLE = "@anirudhh206"
ALIAS = "aka Pheonix"
OVERLINE = "QUANT   ·   CRYPTO   ·   ML / AI"
TAGLINE = "Building at the intersection of markets, blockchains and machine intelligence."

TYPING = [
    "Quantitative finance  ·  systematic trading  ·  risk",
    "Solana  ·  Rust  ·  DeFi  ·  onchain settlement",
    "Machine learning  ·  AI agents  ·  confidential compute",
]

VIOLET, VIOLET_L, CYAN, EMERALD = "#7C3AED", "#A78BFA", "#22D3EE", "#10B981"
VOID, OBSIDIAN, TEXT, MUTED = "#07070B", "#0B0B12", "#E4E4E7", "#A1A1AA"

SANS = "Inter, 'SF Pro Display', 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SF Mono', 'Fira Code', Consolas, 'Courier New', monospace"

FOCUS = [
    dict(tag="01", icon="candles", color=VIOLET_L, title="Quant",
         lines=["Systematic strategies & backtesting",
                "Pricing, risk & portfolio math",
                "Market data & execution systems"]),
    dict(tag="02", icon="chain", color=CYAN, title="Crypto & Blockchain",
         lines=["Solana programs in Rust (Pinocchio)",
                "Stablecoin payments & DeFi credit",
                "Onchain settlement & agents"]),
    dict(tag="03", icon="neural", color=EMERALD, title="ML & AI",
         lines=["AI agents with onchain execution",
                "Credit & risk modelling",
                "Confidential compute (TEE) pipelines"]),
]

PROJECTS = [
    dict(file="auron", label="01 · PAYMENTS", color=VIOLET_L, title="Auron",
         tagline="Programmable stablecoin settlement on Solana",
         desc=["Scan any UPI QR, pay with USDC, and the merchant",
               "receives INR in seconds. Verified on-chain, with no",
               "merchant onboarding required."],
         chips=["TypeScript", "Solana", "USDC", "UPI"]),
    dict(file="ashlar", label="02 · AI AGENTS", color=CYAN, title="Ashlar",
         tagline="Financial workflow engine for AI agents",
         desc=["Type one plain-English instruction, like “pay every",
               "approved invoice every Friday”, and it becomes a",
               "fixed, on-chain workflow on Solana."],
         chips=["TypeScript", "Solana", "AI Agents"]),
    dict(file="xypher", label="03 · DEFI CREDIT", color=EMERALD, title="Xypher",
         tagline="Confidential credit intelligence layer for DeFi",
         desc=["Enables undercollateralized lending by privately",
               "aggregating cross-platform financial data and",
               "computing risk inside a TEE."],
         chips=["TypeScript", "TEE", "DeFi", "Risk"]),
    dict(file="pinocchio", label="04 · SOLANA CORE", color="#C4B5FD", title="Solana Native Dev",
         tagline="Native Solana programs with Pinocchio",
         desc=["Lean, framework-free on-chain programs written in",
               "Rust with Pinocchio, built for minimal compute",
               "units and full control."],
         chips=["Rust", "Solana", "Pinocchio"]),
]

STACK = [
    ("LANGUAGES", VIOLET_L, ["Rust", "TypeScript", "Python"]),
    ("ONCHAIN", CYAN, ["Solana", "Pinocchio", "SPL Tokens", "USDC", "DeFi"]),
    ("QUANT & AI", EMERALD, ["Backtesting", "Risk Models", "Machine Learning", "AI Agents", "TEE"]),
]

BADGES = [
    ("linkedin", "LINKEDIN", CYAN),
    ("x", "X / TWITTER", VIOLET_L),
    ("github-alt", "GITHUB", EMERALD),
]

SECTIONS = [
    ("focus", "01", "FOCUS"),
    ("work", "02", "FEATURED WORK"),
    ("stack", "03", "STACK"),
    ("proof", "04", "PROOF OF WORK"),
    ("city", "05", "CONTRIBUTION CITY"),
]

# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
HEAD = '<?xml version="1.0" encoding="UTF-8"?>\n'
REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def write(path, text):
    pathlib.Path(path).write_text(text, encoding="utf-8")
    print("wrote", pathlib.Path(path).relative_to(ROOT), f"({len(text)/1024:.1f} KB)")


def svg(w, h, title, body, defs="", style=""):
    return (HEAD +
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{esc(title)}">\n<title>{esc(title)}</title>\n'
            f'<defs>{defs}</defs>\n<style>{style}{REDUCED}</style>\n{body}\n</svg>\n')


BLUR_DEFS = (
    '<filter id="blur" x="-60%" y="-120%" width="220%" height="340%"><feGaussianBlur stdDeviation="70"/></filter>'
    '<filter id="blurS" x="-60%" y="-120%" width="220%" height="340%"><feGaussianBlur stdDeviation="28"/></filter>'
    '<filter id="glow" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="12"/></filter>'
    '<filter id="grain" x="0" y="0" width="100%" height="100%">'
    '<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/>'
    '<feColorMatrix type="saturate" values="0"/></filter>'
)


# ----------------------------------------------------------------------------
# hero
# ----------------------------------------------------------------------------
def hero():
    W, H = 1280, 360
    rnd = random.Random(206)
    pts, y, n = [], 340.0, 64
    for i in range(n + 1):
        y += rnd.uniform(-8, 6.5) - 0.7
        y = min(max(y, 312), 350)
        pts.append((i * W / n, y))
    line_d = "M" + " L".join(f"{x:.1f} {yy:.1f}" for x, yy in pts)
    area_d = line_d + f" L{W} {H} L0 {H} Z"

    nodes = [(930, 62), (1040, 128), (1150, 58), (1000, 212), (1135, 188), (1232, 132), (868, 168)]
    edges = [(0, 1), (1, 2), (1, 3), (3, 4), (4, 5), (2, 5), (0, 6), (6, 3), (1, 4)]
    net = "".join(
        f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" '
        f'stroke="url(#edge)" stroke-width="1"/>' for a, b in edges)
    net += "".join(f'<circle cx="{x}" cy="{yy}" r="3.2" fill="{VIOLET_L}" opacity=".75"/>' for x, yy in nodes)
    net += "".join(
        f'<circle cx="{nodes[i][0]}" cy="{nodes[i][1]}" r="5" fill="none" stroke="{CYAN}" stroke-width="1.5">'
        f'<animate attributeName="r" values="5;22;5" dur="{5+j}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values=".9;0;.9" dur="{5+j}s" repeatCount="indefinite"/></circle>'
        for j, i in enumerate((1, 4)))

    defs = BLUR_DEFS + f'''
<clipPath id="clip"><rect width="{W}" height="{H}" rx="22"/></clipPath>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{VOID}"/><stop offset="1" stop-color="#0A0A14"/></linearGradient>
<pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse"><path d="M48 0H0V48" fill="none" stroke="#fff" stroke-opacity=".05"/></pattern>
<radialGradient id="fade" cx=".72" cy=".45" r=".75"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
<mask id="gridmask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
<linearGradient id="line" x1="0" x2="1"><stop offset="0" stop-color="{VIOLET}" stop-opacity="0"/><stop offset=".45" stop-color="{VIOLET_L}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".22"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></linearGradient>
<linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{VIOLET_L}" stop-opacity=".1"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".45"/></linearGradient>
<linearGradient id="name" x1="0" x2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".55" stop-color="#DDD6FE"/><stop offset="1" stop-color="#A5F3FC"/></linearGradient>
<linearGradient id="hair" x1="0" x2="1"><stop offset="0" stop-color="{VIOLET_L}"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
<linearGradient id="rim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".5" stop-color="#fff" stop-opacity=".04"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".25"/></linearGradient>
'''
    style = '''
.a1{animation:d1 19s ease-in-out infinite alternate}
.a2{animation:d2 23s ease-in-out infinite alternate}
.a3{animation:d3 17s ease-in-out infinite alternate}
@keyframes d1{from{transform:translate(0,0)}to{transform:translate(150px,50px)}}
@keyframes d2{from{transform:translate(0,0)}to{transform:translate(-170px,-40px)}}
@keyframes d3{from{transform:translate(0,0)}to{transform:translate(110px,-30px)}}
'''
    body = f'''
<g clip-path="url(#clip)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <ellipse class="a1" cx="250" cy="120" rx="360" ry="150" fill="{VIOLET}" opacity=".5" filter="url(#blur)"/>
  <ellipse class="a2" cx="1040" cy="270" rx="380" ry="140" fill="{CYAN}" opacity=".30" filter="url(#blur)"/>
  <ellipse class="a3" cx="640" cy="360" rx="280" ry="90" fill="{EMERALD}" opacity=".16" filter="url(#blur)"/>
  <ellipse class="a2" cx="1120" cy="40" rx="250" ry="90" fill="{VIOLET}" opacity=".30" filter="url(#blur)"/>
  <rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gridmask)"/>
  <path d="{area_d}" fill="url(#area)"/>
  <path d="{line_d}" fill="none" stroke="url(#line)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" opacity=".9"/>
  <g>
    <circle r="9" fill="{CYAN}" opacity=".35" filter="url(#glow)"/><circle r="3.4" fill="#fff"/>
    <animateMotion dur="16s" repeatCount="indefinite" path="{line_d}"/>
  </g>
  {net}
  <text x="84" y="108" font-family="{MONO}" font-size="15" letter-spacing="3" fill="{CYAN}">{esc(OVERLINE)}</text>
  <text x="84" y="190" font-family="{SANS}" font-size="66" font-weight="800" fill="{VIOLET}" opacity=".6" filter="url(#glow)" textLength="724" lengthAdjust="spacing">{esc(NAME)}</text>
  <text x="84" y="190" font-family="{SANS}" font-size="66" font-weight="800" fill="url(#name)" textLength="724" lengthAdjust="spacing">{esc(NAME)}</text>
  <text x="86" y="232" font-family="{MONO}" font-size="17" fill="{VIOLET_L}">{esc(HANDLE)}<tspan fill="{MUTED}">  ·  {esc(ALIAS)}</tspan></text>
  <text x="86" y="276" font-family="{SANS}" font-size="20" fill="{MUTED}">{esc(TAGLINE)}</text>
  <rect x="86" y="300" width="420" height="2" rx="1" fill="url(#hair)"/>
  <rect width="{W}" height="{H}" filter="url(#grain)" opacity=".07"/>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="21.5" fill="none" stroke="url(#rim)"/>
'''
    return svg(W, H, f"{NAME.title()} - quant, crypto and ML/AI engineer", body, defs, style)


# ----------------------------------------------------------------------------
# typing line
# ----------------------------------------------------------------------------
def typing():
    W, H = 900, 44
    texts = "".join(
        f'<text class="t t{i+1}" x="{W/2}" y="28" text-anchor="middle" font-family="{MONO}" font-size="18" fill="{MUTED}">'
        f'<tspan fill="{CYAN}">&gt; </tspan>{esc(t)}</text>' for i, t in enumerate(TYPING))
    n = len(TYPING)
    cyc = 4 * n
    style = (f'.t{{opacity:0;animation:cyc {cyc}s infinite}}'
             + "".join(f'.t{i+1}{{animation-delay:{i*4}s}}' for i in range(n))
             + f'@keyframes cyc{{0%{{opacity:0;transform:translateY(7px)}}4%{{opacity:1;transform:translateY(0)}}'
               f'{100/n-5:.1f}%{{opacity:1;transform:translateY(0)}}{100/n-1:.1f}%{{opacity:0;transform:translateY(-7px)}}100%{{opacity:0}}}}'
             + '@media (prefers-reduced-motion: reduce){.t1{opacity:1!important}.t2,.t3{display:none}}')
    return svg(W, H, " / ".join(TYPING), texts, "", style)


# ----------------------------------------------------------------------------
# divider / footer / section headers
# ----------------------------------------------------------------------------
def divider():
    W, H = 1280, 24
    defs = (f'<linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{VIOLET}" stop-opacity="0"/>'
            f'<stop offset=".3" stop-color="{VIOLET_L}"/><stop offset=".7" stop-color="{CYAN}"/>'
            f'<stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>'
            '<filter id="gl" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="4"/></filter>')
    body = f'''
<rect x="0" y="11.5" width="{W}" height="1" fill="url(#g)" opacity=".7"/>
<rect x="{W/2-4}" y="8" width="8" height="8" fill="{OBSIDIAN}" stroke="{VIOLET_L}" transform="rotate(45 {W/2} 12)"/>
<g><circle r="6" fill="{CYAN}" filter="url(#gl)"/><circle r="2.4" fill="#fff"/>
<animateMotion dur="9s" repeatCount="indefinite" path="M0 12 H{W}"/></g>'''
    return svg(W, H, "Section divider", body, defs)


def footer():
    W, H = 1280, 150
    waves = ""
    for k, (col, amp, ph, op) in enumerate([(VIOLET, 18, 0.0, .65), (CYAN, 14, 1.7, .45), (EMERALD, 10, 3.1, .28)]):
        d = "M0 " + " L".join(
            f"{x} {80 + amp*math.sin(x/170 + ph) + 6*math.sin(x/61 + ph*2):.1f}" for x in range(0, W + 1, 16))
        d += f" L{W} {H} L0 {H} Z"
        waves += f'<path d="{d}" fill="{col}" opacity="{op}"/>'
    defs = BLUR_DEFS + f'<clipPath id="clip"><rect width="{W}" height="{H}" rx="22"/></clipPath>'
    body = f'''
<g clip-path="url(#clip)">
  <rect width="{W}" height="{H}" fill="{VOID}"/>
  <g filter="url(#blurS)">{waves}</g>
  <text x="{W/2}" y="64" text-anchor="middle" font-family="{MONO}" font-size="15" letter-spacing="8" fill="{TEXT}" opacity=".85">BUILD   ·   SHIP   ·   COMPOUND</text>
  <text x="{W/2}" y="92" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{MUTED}">{esc(HANDLE)}  ·  2026</text>
  <rect width="{W}" height="{H}" filter="url(#grain)" opacity=".06"/>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="21.5" fill="none" stroke="#fff" stroke-opacity=".08"/>'''
    return svg(W, H, "Footer", body, defs)


def section(slug, idx, title):
    W, H = 1280, 68
    tl = len(title) * 22
    defs = (f'<linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{VIOLET_L}"/>'
            f'<stop offset=".5" stop-color="{CYAN}" stop-opacity=".5"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="t" x1="0" x2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#DDD6FE"/></linearGradient>')
    body = f'''
<text x="2" y="20" font-family="{MONO}" font-size="13" letter-spacing="4" fill="{CYAN}">{idx} / {esc(slug.upper())}</text>
<text x="0" y="56" font-family="{SANS}" font-size="32" font-weight="800" fill="url(#t)" textLength="{tl}" lengthAdjust="spacing">{esc(title)}</text>
<rect x="{tl+28}" y="46" width="{W-tl-28}" height="1.5" fill="url(#g)"/>
<rect x="{tl+28}" y="43" width="6" height="7" rx="1.5" fill="{VIOLET_L}"/>'''
    return svg(W, H, f"{title}", body, defs)


# ----------------------------------------------------------------------------
# focus panel
# ----------------------------------------------------------------------------
def icon(kind, c):
    if kind == "candles":
        bars = [(0, 30, 22, .55), (18, 14, 30, .9), (36, 22, 24, .7), (54, 6, 34, 1)]
        s = ""
        for x, top, h, op in bars:
            s += (f'<line x1="{x+6}" y1="{top-8}" x2="{x+6}" y2="{top+h+8}" stroke="{c}" stroke-width="2" opacity="{op}"/>'
                  f'<rect x="{x}" y="{top}" width="12" height="{h}" rx="3" fill="{c}" opacity="{op*.85}"/>')
        return s
    if kind == "chain":
        def hexa(cx, cy, r):
            return " ".join(f"{cx + r*math.cos(math.radians(60*i-30)):.1f},{cy + r*math.sin(math.radians(60*i-30)):.1f}" for i in range(6))
        return (f'<polygon points="{hexa(22,34,20)}" fill="none" stroke="{c}" stroke-width="3" stroke-linejoin="round"/>'
                f'<polygon points="{hexa(50,34,20)}" fill="{c}" fill-opacity=".18" stroke="{c}" stroke-width="3" stroke-linejoin="round"/>')
    l1, l2, l3 = [(6, 12), (6, 34), (6, 56)], [(36, 20), (36, 48)], [(66, 34)]
    s = "".join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{c}" stroke-opacity=".5" stroke-width="1.6"/>'
                for A, B in ((l1, l2), (l2, l3)) for a in A for b in B)
    s += "".join(f'<circle cx="{x}" cy="{y}" r="5.5" fill="{c}"/>' for x, y in l1 + l2 + l3)
    return s


def focus():
    W, H = 1280, 300
    defs = BLUR_DEFS + (f'<clipPath id="pclip"><rect width="400" height="{H}" rx="22"/></clipPath>'
                        '<linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".06"/>'
                        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    body = ""
    for i, p in enumerate(FOCUS):
        c = p["color"]
        bullets = "".join(
            f'<circle cx="38" cy="{196+j*32-5}" r="3" fill="{c}"/>'
            f'<text x="54" y="{196+j*32}" font-family="{SANS}" font-size="16" fill="{MUTED}">{esc(t)}</text>'
            for j, t in enumerate(p["lines"]))
        body += f'''
<g transform="translate({i*440},0)">
  <rect width="400" height="{H}" rx="22" fill="{OBSIDIAN}"/>
  <ellipse cx="70" cy="20" rx="150" ry="90" fill="{c}" opacity=".30" filter="url(#blur)" clip-path="url(#pclip)"/>
  <rect width="400" height="{H}" rx="22" fill="url(#sheen)"/>
  <rect x=".5" y=".5" width="399" height="{H-1}" rx="21.5" fill="none" stroke="#fff" stroke-opacity=".10"/>
  <g transform="translate(34,30)">{icon(p["icon"], c)}</g>
  <text x="366" y="52" text-anchor="end" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{MUTED}">{p["tag"]}</text>
  <text x="34" y="144" font-family="{SANS}" font-size="27" font-weight="700" fill="{TEXT}">{esc(p["title"])}</text>
  <rect x="34" y="158" width="38" height="3" rx="1.5" fill="{c}"/>
  {bullets}
</g>'''
    return svg(W, H, "Focus areas: Quant, Crypto and Blockchain, ML and AI", body, defs)


# ----------------------------------------------------------------------------
# project cards (600 x 300)
# ----------------------------------------------------------------------------
def project(p):
    W, H = 600, 300
    c = p["color"]
    chips, x = "", 32
    for t in p["chips"]:
        w = len(t) * 7.6 + 26
        chips += (f'<rect x="{x:.1f}" y="244" width="{w:.1f}" height="26" rx="13" fill="{c}" fill-opacity=".10" stroke="{c}" stroke-opacity=".45"/>'
                  f'<text x="{x+w/2:.1f}" y="261.5" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{TEXT}">{esc(t)}</text>')
        x += w + 10
    desc = "".join(f'<text x="32" y="{166+i*24}" font-family="{SANS}" font-size="15" fill="{MUTED}">{esc(t)}</text>'
                   for i, t in enumerate(p["desc"]))
    defs = BLUR_DEFS + (f'<clipPath id="clip"><rect width="{W}" height="{H}" rx="22"/></clipPath>'
                        '<linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".06"/>'
                        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
                        f'<linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{c}"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></linearGradient>')
    body = f'''
<g clip-path="url(#clip)">
  <rect width="{W}" height="{H}" fill="{OBSIDIAN}"/>
  <ellipse cx="520" cy="10" rx="190" ry="100" fill="{c}" opacity=".28" filter="url(#blur)"/>
  <ellipse cx="40" cy="320" rx="150" ry="70" fill="{VIOLET}" opacity=".14" filter="url(#blur)"/>
  <rect width="{W}" height="{H}" fill="url(#sheen)"/>
  <rect x="0" y="0" width="{W}" height="3" fill="url(#bar)"/>
  <rect width="{W}" height="{H}" filter="url(#grain)" opacity=".05"/>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="21.5" fill="none" stroke="#fff" stroke-opacity=".10"/>
<text x="32" y="50" font-family="{MONO}" font-size="12.5" letter-spacing="3" fill="{c}">{esc(p["label"])}</text>
<g transform="translate(540,34)" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M0 14 L14 0 M3 0 H14 V11"/></g>
<text x="32" y="100" font-family="{SANS}" font-size="38" font-weight="800" fill="{TEXT}">{esc(p["title"])}</text>
<text x="32" y="130" font-family="{SANS}" font-size="16.5" font-weight="600" fill="{c}">{esc(p["tagline"])}</text>
{desc}
{chips}'''
    return svg(W, H, f'{p["title"]}: {p["tagline"]}', body, defs)


# ----------------------------------------------------------------------------
# stack
# ----------------------------------------------------------------------------
def stack():
    W, H = 1280, 214
    body = ""
    for r, (label, c, items) in enumerate(STACK):
        y = 24 + r * 66
        body += f'<text x="4" y="{y+26}" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{MUTED}">{esc(label)}</text>'
        x = 190
        for t in items:
            w = len(t) * 9.2 + 40
            body += (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="40" rx="20" fill="{c}" fill-opacity=".09" stroke="{c}" stroke-opacity=".5"/>'
                     f'<circle cx="{x+20:.1f}" cy="{y+20}" r="3.5" fill="{c}"/>'
                     f'<text x="{x+32:.1f}" y="{y+25}" font-family="{MONO}" font-size="15" fill="{TEXT}">{esc(t)}</text>')
            x += w + 14
    return svg(W, H, "Tech stack: " + "; ".join(f"{l}: {', '.join(i)}" for l, _, i in STACK), body)


# ----------------------------------------------------------------------------
# badges
# ----------------------------------------------------------------------------
def badge(slug, label, c):
    w, h = len(label) * 9.4 + 58, 42
    body = (f'<rect x=".5" y=".5" width="{w-1:.1f}" height="{h-1}" rx="20.5" fill="{OBSIDIAN}" stroke="{c}" stroke-opacity=".55"/>'
            f'<circle cx="24" cy="21" r="4" fill="{c}"/>'
            f'<text x="40" y="26" font-family="{MONO}" font-size="13.5" letter-spacing="1.5" fill="{TEXT}">{esc(label)}</text>')
    return svg(round(w), h, label, body)


# ----------------------------------------------------------------------------
# placeholders (overwritten by workflows on first run)
# ----------------------------------------------------------------------------
def placeholder(w, h, title, sub):
    body = (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="{OBSIDIAN}" stroke="#fff" stroke-opacity=".10"/>'
            f'<text x="{w/2}" y="{h/2-6}" text-anchor="middle" font-family="{MONO}" font-size="14" letter-spacing="4" fill="{VIOLET_L}">{esc(title)}</text>'
            f'<text x="{w/2}" y="{h/2+20}" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{MUTED}">{esc(sub)}</text>')
    return svg(w, h, f"{title} placeholder", body)


def main():
    write(ASSETS / "hero.svg", hero())
    write(ASSETS / "typing.svg", typing())
    write(ASSETS / "divider.svg", divider())
    write(ASSETS / "footer.svg", footer())
    write(ASSETS / "focus.svg", focus())
    write(ASSETS / "stack.svg", stack())
    for slug, idx, title in SECTIONS:
        write(ASSETS / f"h-{slug}.svg", section(slug, idx, title))
    for p in PROJECTS:
        write(PROJ / f'{p["file"]}.svg', project(p))
    for slug, label, c in BADGES:
        write(ASSETS / f"badge-{slug}.svg", badge(slug, label, c))

    sub = "Initialising. Run the “Update profile cards” workflow once."
    # only create placeholders if the workflow has not produced the real file yet
    for path, args in [
        (PROFILE / "stats.svg", (495, 195, "GITHUB STATS", sub)),
        (PROFILE / "top-langs.svg", (495, 195, "TOP LANGUAGES", sub)),
        (PROFILE / "streak.svg", (495, 195, "CONTRIBUTION STREAK", sub)),
        (CONTRIB3D / "profile-night-rainbow.svg",
         (1280, 320, "3D CONTRIBUTION CITY", "Initialising. Run the “GitHub-Profile-3D-Contrib” workflow once.")),
    ]:
        if path.exists() and "placeholder" not in path.read_text(encoding="utf-8", errors="ignore")[:600]:
            print("kept real", path.relative_to(ROOT))
            continue
        write(path, placeholder(*args))


if __name__ == "__main__":
    main()
