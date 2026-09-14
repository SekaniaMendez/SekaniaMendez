# Profile banner

Original orbital artwork for the MendezSoftwagic GitHub profile. It uses the
portfolio's night, cyan and violet palette, with a new geometric monogram and
tilted orbital planes. The typography remains stationary while C++, Python and React icons
travel along the orbits and the background stars gently change brightness.

- `banner.gif`: README animation, 1200 × 400, 20 fps, seamless 12-second loop.
- `banner.png`: still image for reduced-motion viewers and previews.
- `banner.svg`: editable, static vector artwork of the first frame.

The profile uses a `<picture>` element to select the PNG when the viewer's
browser requests reduced motion, with the GIF as its default image. All artwork
is stored in this repository; there are no external banner-generation services.

## Regenerate

Install Python 3, librsvg (`rsvg-convert`) and FFmpeg. On macOS with Homebrew:

```sh
brew install librsvg ffmpeg
python3 scripts/render_banner.py
```

The generator uses only the Python standard library. It overwrites the three
generated banner files above and removes its own temporary render frames.
Edit `scripts/render_banner.py` to change the design; directly editing the SVG
does not change the generated GIF. Georgia and Arial are used when installed,
with serif and sans-serif fallbacks on other systems.

## Technology icons and university signature

`icons/` contains unmodified [Simple Icons](https://github.com/simple-icons/simple-icons)
SVGs, pinned to commit `4ba19240849175ab4b855a732ab98c0f87cfb714`.
Their CC0 license is included in `icons/LICENSE.md`; brand rights remain with
their respective owners. `stack/` contains locally generated icon-and-label badges.
The pictograms for AI, computer vision, LiDAR, GNSS, geospatial systems and
procedural design are original line drawings representing fields, not brand logos.

`ucr.svg` is the unchanged official university signature from
[Universidad de Costa Rica](https://www.ucr.ac.cr/vistas/webucr_ucr_7/imagenes/firma-ucr-c.svg),
retrieved on 2026-09-13. `ucr-student.svg` places it on a white card, preserving its
colors and proportions, with the user's stated student affiliation at
[ECCI](https://www.ecci.ucr.ac.cr/). It does not
indicate a particular degree, campus, or institutional endorsement.

Technology and project descriptions come from the public
[portfolio](https://www.mendezsoftwagic.dev/) and its four project case studies.
ROS2 is labeled as exploration because the Atlas case study describes it as a
future direction.

Regenerate the badges and university card without network access:

```sh
python3 scripts/render_stack.py
```

To re-fetch the exact pinned icon sources, use `--download-icons`. This also
requires `curl` and network access. The downloaded icon SVGs are inputs for both
generators; regenerate the banner after changing them.
