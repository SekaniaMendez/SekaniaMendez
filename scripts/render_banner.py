#!/usr/bin/env python3
"""Render the original MendezSoftwagic profile artwork as a seamless GIF.

Requires Python 3, rsvg-convert (librsvg), and ffmpeg on PATH.
Run from any directory: python3 scripts/render_banner.py
All frames are drawn from vector geometry; no external image service is used.
"""

from concurrent.futures import ThreadPoolExecutor
import argparse
from functools import lru_cache
from html import escape
from math import cos, pi, sin
from pathlib import Path
import random
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
WIDTH, HEIGHT = 1200, 400
FPS, SECONDS = 20, 12
CYAN, VIOLET = "#78f8e4", "#a991ff"
COPY = {
    "en": {
        "title": "MendezSoftwagic — software, with a little magic",
        "description": "Mint and violet orbital paths surround a geometric M on a dark star field. Software developer and UCR / ECCI student, Costa Rica.",
        "role": "SOFTWARE DEVELOPER · UCR / ECCI STUDENT",
        "tagline": "Software, with a little magic.",
        "fields": "AI ENGINEERING  /  SPATIAL SYSTEMS  /  INTERACTIVE WORLDS",
        "location": "BUILT IN COSTA RICA",
    },
    "es": {
        "title": "MendezSoftwagic — software, con un toque de magia",
        "description": "Órbitas cian y violeta rodean una M geométrica sobre un cielo oscuro. Desarrollador y estudiante de la UCR / ECCI, Costa Rica.",
        "role": "DESARROLLADOR · ESTUDIANTE UCR / ECCI",
        "tagline": "Software, con un toque de magia.",
        "fields": "INTELIGENCIA ARTIFICIAL  /  SISTEMAS ESPACIALES  /  MUNDOS INTERACTIVOS",
        "location": "CREADO EN COSTA RICA",
    },
}


@lru_cache(maxsize=3)
def technology_icon(slug):
    root = ET.parse(ASSETS / "icons" / f"{slug}.svg").getroot()
    return "".join(f'<path d="{escape(node.attrib["d"], quote=True)}"/>' for node in root.iter() if node.tag.rsplit("}", 1)[-1] == "path")


def artwork(phase=0, lang="en"):
    """A phase of 0 and 1 produces identical geometry and brightness."""
    copy = COPY[lang]
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
    <title>{copy['title']}</title>
    <desc>{copy['description']}</desc>
    <defs>
      <radialGradient id="space" cx="79%" cy="43%" r="76%">
        <stop stop-color="#112226"/><stop offset=".48" stop-color="#090e15"/><stop offset="1" stop-color="#05070a"/>
      </radialGradient>
      <radialGradient id="halo"><stop stop-color="#78f8e4" stop-opacity=".13"/><stop offset="1" stop-color="#78f8e4" stop-opacity="0"/></radialGradient>
      <linearGradient id="metal" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#c0fff3"/><stop offset=".5" stop-color="#78f8e4"/><stop offset="1" stop-color="#a991ff"/></linearGradient>
      <linearGradient id="line"><stop stop-color="#78f8e4" stop-opacity=".65"/><stop offset=".65" stop-color="#a991ff" stop-opacity=".25"/><stop offset="1" stop-color="#a991ff" stop-opacity="0"/></linearGradient>
    </defs>
    <rect width="1200" height="400" fill="#05070a"/>
    <rect width="1200" height="400" rx="18" fill="url(#space)"/>
    <rect x=".5" y=".5" width="1199" height="399" rx="18" fill="none" stroke="#263439"/>
    <circle cx="948" cy="182" r="200" fill="url(#halo)"/>
    <path d="M64 332H1136" stroke="url(#line)"/>
    ''']
    rng = random.Random(29)
    for index in range(65):
        x, y = rng.uniform(730, 1160), rng.uniform(32, 310)
        opacity = .12 + .22 * (1 + sin(2 * pi * phase + index * 1.7)) / 2
        radius = rng.choice([.65, .85, 1.1])
        parts.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{radius}" fill="#b4d6da" opacity="{opacity:.4f}"/>')

    # Editorial typography stays still throughout the loop.
    parts.append(f'''
    <g font-family="Arial, Helvetica, sans-serif">
      <path d="M64 55h18m-9-9v18" stroke="#78f8e4" stroke-width="1.5"/>
      <text x="97" y="60" fill="#b3c7c5" font-size="12" letter-spacing="2.3">{copy['role']}</text>
      <text x="62" y="150" fill="#f2f3ed" font-size="61" letter-spacing="-2.5">Mendez<tspan fill="#78f8e4">Softwagic</tspan></text>
      <text x="64" y="206" fill="#d3d8e2" font-family="Georgia, serif" font-style="italic" font-size="30">{copy['tagline']}</text>
      <text x="65" y="266" fill="#91a5ad" font-size="{11 if lang == 'es' else 12}" letter-spacing="{.8 if lang == 'es' else 1.6}">{copy['fields']}</text>
      <circle cx="69" cy="363" r="3" fill="#78f8e4"/>
      <text x="83" y="367" fill="#9dafb2" font-size="12" letter-spacing="1.6">{copy['location']}</text>
      <text x="1136" y="367" fill="#b0c5c7" text-anchor="end" font-size="13" letter-spacing="1">mendezsoftwagic.dev ↗</text>
    </g>
    <g transform="translate(948 180)">
      <path d="M-159 0h318M0-146v292" stroke="#78f8e4" stroke-opacity=".07"/>
      <circle r="123" fill="none" stroke="#78f8e4" stroke-opacity=".15"/>
      <circle r="137" fill="none" stroke="#a991ff" stroke-opacity=".12" stroke-dasharray="1 9"/>
    ''')

    for i in range(48):
        a = i * 2 * pi / 48
        r = 123
        length = 6 if i % 4 == 0 else 2.5
        parts.append(f'<path d="M{r*cos(a):.3f} {r*sin(a):.3f}L{(r-length)*cos(a):.3f} {(r-length)*sin(a):.3f}" stroke="#78f8e4" stroke-opacity=".25"/>')

    # Three tilted orbital planes, with discrete comet trails.
    for index, (tilt, rx, ry, color) in enumerate([
        (-32, 153, 57, CYAN), (38, 146, 64, VIOLET), (92, 127, 51, CYAN)
    ]):
        direction = 1 if index % 2 == 0 else -1
        angle = phase * 2 * pi * direction + index * 2 * pi / 3
        parts.append(f'<g transform="rotate({tilt})"><ellipse rx="{rx}" ry="{ry}" fill="none" stroke="{color}" stroke-opacity=".23"/>')
        for trail in range(22, -1, -1):
            a = angle - direction * trail * .014
            x, y = rx * cos(a), ry * sin(a)
            opacity = .65 * (1 - trail / 23) ** 2
            parts.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="1.7" fill="{color}" opacity="{opacity:.4f}"/>')
        x, y = rx * cos(angle), ry * sin(angle)
        slug = ("cplusplus", "python", "react")[index]
        parts.append(f'<g transform="translate({x:.3f} {y:.3f}) rotate({-tilt})"><circle r="20" fill="{color}" opacity=".06"/><rect x="-15" y="-15" width="30" height="30" rx="9" fill="#0c1920" stroke="{color}" stroke-opacity=".55"/><g transform="translate(-9 -9) scale(.75)" fill="{color}">{technology_icon(slug)}</g></g></g>')

    parts.append('''
      <path d="M0-60L52-30V30L0 60L-52 30V-30Z" fill="#091519" stroke="url(#metal)" stroke-opacity=".6"/>
      <path d="M0-52L45-26V26L0 52L-45 26V-26Z" fill="none" stroke="#78f8e4" stroke-opacity=".12"/>
      <path d="M-26 23V-23L0 6L26-23V23M-17 23V1L0 20L17 1V23" fill="none" stroke="url(#metal)" stroke-width="3" stroke-linejoin="round"/>
    </g>
    </svg>''')
    return "".join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lang", choices=COPY, default="en")
    args = parser.parse_args()
    stem = "banner" if args.lang == "en" else "banner-es"
    for executable in ("rsvg-convert", "ffmpeg"):
        if not shutil.which(executable):
            raise SystemExit(f"Missing dependency: {executable}. See assets/README.md.")
    ASSETS.mkdir(exist_ok=True)
    svg = artwork(lang=args.lang)
    (ASSETS / f"{stem}.svg").write_text(svg, encoding="utf-8")
    subprocess.run(["rsvg-convert", "-o", str(ASSETS / f"{stem}.png")], input=svg.encode(), check=True)

    with tempfile.TemporaryDirectory(prefix="mendez-banner-") as scratch:
        frames = Path(scratch)

        def render(index):
            subprocess.run([
                "rsvg-convert", "-o", str(frames / f"{index:04d}.png")
            ], input=artwork(index / (FPS * SECONDS), args.lang).encode(), check=True)

        with ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(render, range(FPS * SECONDS)))
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "warning", "-y",
            "-framerate", str(FPS), "-i", str(frames / "%04d.png"),
            "-filter_complex",
            "split[a][b];[a]palettegen=stats_mode=full:max_colors=128[p];[b][p]paletteuse=dither=none:diff_mode=rectangle",
            "-loop", "0", str(ASSETS / f"{stem}.gif")
        ], check=True)
    print(f"Rendered {FPS * SECONDS} frames; {SECONDS}s seamless loop.")
    output = ASSETS / f"{stem}.gif"
    print(f"GIF: {output} ({output.stat().st_size / 1024 / 1024:.2f} MiB)")


if __name__ == "__main__":
    main()
