#!/usr/bin/env python3
"""Generate self-contained technology badges from locally stored SVG icons.

python3 scripts/render_stack.py                  # offline rebuild
python3 scripts/render_stack.py --download-icons # fetch pinned Simple Icons
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
from html import escape
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ICONS = ASSETS / "icons"
BADGES = ASSETS / "stack"
REVISION = "4ba19240849175ab4b855a732ab98c0f87cfb714"
BASE = f"https://raw.githubusercontent.com/simple-icons/simple-icons/{REVISION}"
TECHNOLOGIES = [
    ("cplusplus", "C++", "#76b7f2", 94),
    ("python", "Python", "#f3d26d", 115),
    ("typescript", "TypeScript", "#72b7fc", 143),
    ("swift", "Swift", "#ff946e", 106),
    ("react", "React", "#61dafb", 108),
    ("nodedotjs", "Node.js", "#8fd378", 122),
    ("express", "Express", "#e7eeed", 124),
    ("gsap", "GSAP", "#b2f65f", 111),
    ("unrealengine", "Unreal Engine 5", "#d9caff", 180),
    ("postgresql", "PostgreSQL", "#88badb", 154),
    ("mongodb", "MongoDB", "#82d798", 139),
    ("docker", "Docker", "#78c8fc", 116),
    ("ros", "ROS2", "#a991ff", 106),
]

# Original line pictograms for technical fields, not third-party brand marks.
FIELDS = [
    ("computer-vision", "Computer Vision", '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>', 183),
    ("lidar", "LiDAR", '<circle cx="12" cy="12" r="2"/><path d="M12 7a5 5 0 1 1-5 5M12 3a9 9 0 1 1-9 9M12 12 5 5"/>', 110),
    ("gnss", "GNSS", '<path d="m9 3 5 5-6 6-5-5ZM14 8l4-4 3 3-4 4M8 14l-4 4 3 3 4-4M13 13l3 3m0-4a4 4 0 0 1-4 4m8-4a8 8 0 0 1-8 8"/>', 111),
    ("ai-systems", "AI Systems", '<rect x="6" y="6" width="12" height="12" rx="3"/><path d="M9 2v4m6-4v4M9 18v4m6-4v4M2 9h4m-4 6h4m12-6h4m-4 6h4M10 14v-4l4 4v-4"/>', 147),
    ("geospatial", "Geospatial", '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18M5 6.5h14M5 17.5h14"/>', 146),
    ("procedural-design", "Procedural Design", '<path d="m12 2 9 5-9 5-9-5Zm-9 10 9 5 9-5M3 17l9 5 9-5"/>', 193),
]


def icon_paths(slug):
    root = ET.parse(ICONS / f"{slug}.svg").getroot()
    return "".join(f'<path d="{escape(node.attrib["d"], quote=True)}"/>' for node in root.iter() if node.tag.rsplit("}", 1)[-1] == "path")


def badge(slug, name, color, width, geometry, lines=False):
    paint = f'fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"' if lines else f'fill="{color}"'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="44" viewBox="0 0 {width} 44" role="img" aria-label="{escape(name)}">
    <title>{escape(name)}</title>
    <rect x=".5" y=".5" width="{width-1}" height="43" rx="9" fill="#0a1117" stroke="#28373e"/>
    <g transform="translate(12 11) scale(.916667)" {paint}>{geometry}</g>
    <text x="44" y="27" fill="#dce7e7" font-family="Arial,Helvetica,sans-serif" font-size="13">{escape(name)}</text>
    </svg>'''
    (BADGES / f"{slug}.svg").write_text(svg, encoding="utf-8")


def download_icons():
    ICONS.mkdir(exist_ok=True)

    def fetch(slug):
        subprocess.run(["curl", "--fail", "--silent", "--show-error", "--location", "--max-time", "30",
                        f"{BASE}/icons/{slug}.svg", "--output", str(ICONS / f"{slug}.svg")], check=True)

    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(fetch, [row[0] for row in TECHNOLOGIES]))
    subprocess.run(["curl", "--fail", "--silent", "--show-error", "--location", "--max-time", "30",
                    f"{BASE}/LICENSE.md", "--output", str(ICONS / "LICENSE.md")], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download-icons", action="store_true")
    args = parser.parse_args()
    if args.download_icons:
        download_icons()
    BADGES.mkdir(exist_ok=True)
    for slug, name, color, width in TECHNOLOGIES:
        badge(slug, name, color, width, icon_paths(slug))
    for slug, name, paths, width in FIELDS:
        badge(slug, name, "#78f8e4", width, paths, lines=True)
    # Keep the university's official signature unchanged, on a white card so
    # its dark lettering remains legible in both GitHub themes.
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    signature = ET.parse(ASSETS / "ucr.svg").getroot()
    signature.set("x", "22")
    signature.set("y", "14")
    signature.set("width", "416")
    signature.set("height", "50")
    university = f'''<svg xmlns="http://www.w3.org/2000/svg" width="460" height="104" viewBox="0 0 460 104" role="img" aria-label="Estudiante de la ECCI, Universidad de Costa Rica">
    <title>Estudiante de la ECCI, Universidad de Costa Rica</title>
    <rect x=".5" y=".5" width="459" height="103" rx="10" fill="#ffffff" stroke="#dce7eb"/>
    {ET.tostring(signature, encoding="unicode")}
    <text x="23" y="86" fill="#006b93" font-family="Arial,Helvetica,sans-serif" font-size="12" font-weight="bold" letter-spacing="1.8">ESTUDIANTE · ECCI</text>
    <text x="436" y="86" fill="#526774" font-family="Arial,Helvetica,sans-serif" font-size="11" text-anchor="end">UCR · COSTA RICA</text>
    </svg>'''
    (ASSETS / "ucr-student.svg").write_text(university, encoding="utf-8")
    print(f"Rendered {len(TECHNOLOGIES) + len(FIELDS)} local technology badges.")


if __name__ == "__main__":
    main()
