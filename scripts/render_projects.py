#!/usr/bin/env python3
"""Render bilingual vector project headers and language selectors, offline.

Run: python3 scripts/render_projects.py
Copy for project descriptions lives in README.md and README.es.md.
"""

from html import escape
from math import cos, sin
from pathlib import Path
import random

ASSETS = Path(__file__).resolve().parents[1] / "assets"
PROJECTS = [
    ("topotools", "TopoTools", "#78f8e4", "GEOSPATIAL AUTOMATION", "AUTOMATIZACIÓN GEOESPACIAL"),
    ("atlas", "Atlas", "#82c7ff", "SPATIAL INTELLIGENCE", "INTELIGENCIA ESPACIAL"),
    ("umbra-caeli", "Umbra Caeli", "#b49bff", "INTERACTIVE WORLDS", "MUNDOS INTERACTIVOS"),
    ("wedding-manager", "Wedding Manager", "#f1becf", "EVENT EXPERIENCES", "EXPERIENCIAS Y EVENTOS"),
]


def illustration(slug, color):
    elements = []
    if slug == "topotools":
        for i in range(8):
            rx, ry = 20 + i * 11, 11 + i * 7
            elements.append(f'<ellipse cx="433" cy="94" rx="{rx}" ry="{ry}" transform="rotate(-27 433 94)" fill="none" stroke="{color}" stroke-opacity="{.55-i*.05}"/>')
        elements.append(f'<path d="M405 87h20m-10-10v20" stroke="{color}"/><circle cx="415" cy="87" r="3" fill="{color}"/>')
    elif slug == "atlas":
        rng = random.Random(17)
        for row in range(12):
            for col in range(14):
                x = 358 + col * 11 + row * 3
                y = 46 + row * 7 + sin(col * .5 + row * .22) * 14
                elements.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{rng.uniform(.8,1.8):.2f}" fill="{color}" opacity="{rng.uniform(.14,.65):.2f}"/>')
        elements.append(f'<path d="m421 35 44 25v52l-44 25-44-25V60Z M421 86l44-26m-44 26-44-26m44 26v51" fill="none" stroke="{color}" stroke-opacity=".65"/>')
    elif slug == "umbra-caeli":
        elements.append(f'<circle cx="431" cy="89" r="59" fill="none" stroke="{color}" stroke-opacity=".18"/><circle cx="431" cy="89" r="48" fill="none" stroke="{color}" stroke-opacity=".13" stroke-dasharray="2 7"/>')
        points = [(388, 106), (412, 61), (437, 97), (470, 63), (456, 126)]
        elements.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in points)}" fill="none" stroke="{color}" stroke-opacity=".55"/>')
        for x, y in points:
            elements.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{color}" opacity=".09"/><circle cx="{x}" cy="{y}" r="2.2" fill="{color}"/>')
    else:
        elements.append(f'<g transform="rotate(-18 431 87)"><ellipse cx="413" cy="87" rx="30" ry="39" fill="none" stroke="{color}" stroke-width="1.6" stroke-opacity=".65"/><ellipse cx="449" cy="87" rx="30" ry="39" fill="none" stroke="{color}" stroke-width="1.6" stroke-opacity=".4"/></g>')
        for i in range(16):
            a = i * 6.283 / 16
            x, y = 431 + cos(a) * 65, 87 + sin(a) * 60
            elements.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="1" fill="{color}" opacity=".35"/>')
        elements.append(f'<path d="M431 18v12m-6-6h12" stroke="{color}"/>')
    return "".join(elements)


def main():
    directory = ASSETS / "projects"
    directory.mkdir(exist_ok=True)
    for index, (slug, name, color, category_en, category_es) in enumerate(PROJECTS, 1):
        for lang, category in (("en", category_en), ("es", category_es)):
            svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="520" height="168" viewBox="0 0 520 168" role="img" aria-label="{escape(name)} — {escape(category)}">
            <title>{escape(name)} — {escape(category)}</title>
            <defs>
              <linearGradient id="bg"><stop stop-color="#0c1119"/><stop offset="1" stop-color="#111c26"/></linearGradient>
              <linearGradient id="fade"><stop stop-color="#0c1119"/><stop offset="1" stop-color="#0c1119" stop-opacity="0"/></linearGradient>
              <clipPath id="bounds"><rect width="520" height="168" rx="12"/></clipPath>
            </defs>
            <g clip-path="url(#bounds)">
              <rect width="520" height="168" fill="url(#bg)"/>
              {illustration(slug, color)}
              <rect x="300" width="90" height="168" fill="url(#fade)"/>
              <path d="M25 0h88" stroke="{color}" stroke-width="3"/>
              <text x="26" y="39" fill="{color}" font-family="Arial,Helvetica,sans-serif" font-size="10" letter-spacing="1.5">0{index} / {escape(category)}</text>
              <text x="25" y="94" fill="#f0f3f4" font-family="Arial,Helvetica,sans-serif" font-size="{31 if slug == 'wedding-manager' else 35}" letter-spacing="-1">{escape(name)}</text>
              <path d="M27 127h28" stroke="{color}" stroke-opacity=".7"/>
              <text x="66" y="131" fill="#83979f" font-family="Arial,Helvetica,sans-serif" font-size="10" letter-spacing="1.8">MENDEZSOFTWAGIC</text>
            </g>
            <rect x=".5" y=".5" width="519" height="167" rx="12" fill="none" stroke="#2b3845"/>
            </svg>'''
            (directory / f"{slug}-{lang}.svg").write_text(svg, encoding="utf-8")

    languages = ASSETS / "languages"
    languages.mkdir(exist_ok=True)
    for lang, label in (("es", "Español"), ("en", "English")):
        for active in (False, True):
            state = "active" if active else "available"
            color, background = ("#78f8e4", "#102825") if active else ("#a9b9c4", "#0c131c")
            svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="132" height="36" viewBox="0 0 132 36" role="img" aria-label="{label}">
            <title>{label}</title>
            <rect x=".5" y=".5" width="131" height="35" rx="9" fill="{background}" stroke="{color}" stroke-opacity=".5"/>
            <text x="14" y="23" fill="{color}" font-family="Arial,Helvetica,sans-serif" font-size="10" font-weight="bold">{lang.upper()}</text>
            <path d="M36 10v16" stroke="{color}" stroke-opacity=".25"/>
            <text x="46" y="23" fill="{color}" font-family="Arial,Helvetica,sans-serif" font-size="13">{label}</text>
            </svg>'''
            (languages / f"{lang}-{state}.svg").write_text(svg, encoding="utf-8")
    print("Rendered 8 project headers and 4 language selectors.")


if __name__ == "__main__":
    main()
