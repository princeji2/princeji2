"""
make_ascii_svg.py
Downsamples data/prepped.png to a character grid and writes it out as a
monochrome SVG that "types" itself in, row by row, then freezes.

Usage:
    python scripts/make_ascii_svg.py
"""
from PIL import Image

RAMP = " .`:-=+*cs#%@"   # bright (sparse) -> dark (dense); leading space = blank
COLS = 84
CHAR_W = 7.1
CHAR_H = 12.4
FONT_SIZE = 12.4
FILL = "#3A3A3D"          # single monochrome ink color — no per-glyph color
BG = "#FFFBD4"             # canvas behind the portrait
STAGGER = 0.028            # seconds between each row starting to type
ROW_DURATION = 0.35


def to_grid(path: str, cols: int = COLS):
    img = Image.open(path).convert("L")
    w, h = img.size
    rows = round(cols * (h / w) * (CHAR_W / CHAR_H))
    small = img.resize((cols, rows), Image.LANCZOS)
    px = small.load()

    grid = []
    for y in range(rows):
        line = []
        for x in range(cols):
            brightness = px[x, y]                # 0 dark .. 255 light
            idx = int((255 - brightness) / 255 * (len(RAMP) - 1))
            line.append(RAMP[idx])
        grid.append("".join(line))
    return grid


def escape(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def build_svg(grid, out_path="assets/portrait.svg"):
    rows = len(grid)
    cols = len(grid[0])
    width = cols * CHAR_W + 24
    height = rows * CHAR_H + 24

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" '
                  f'height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}">')
    parts.append(f'<rect width="100%" height="100%" fill="{BG}"/>')
    parts.append(f'<style>text{{font-family:"SF Mono","JetBrains Mono",Menlo,'
                  f'Consolas,monospace;font-size:{FONT_SIZE}px;fill:{FILL};'
                  f'white-space:pre;}}</style>')

    for i, row in enumerate(grid):
        y = 18 + i * CHAR_H
        row_w = cols * CHAR_W
        begin = i * STAGGER
        clip_id = f"clip{i}"
        parts.append(f'<clipPath id="{clip_id}">')
        parts.append(f'<rect x="12" y="{y - CHAR_H + 2:.1f}" width="0" height="{CHAR_H:.1f}">'
                      f'<animate attributeName="width" from="0" to="{row_w:.1f}" '
                      f'begin="{begin:.3f}s" dur="{ROW_DURATION}s" fill="freeze" '
                      f'calcMode="spline" keySplines="0.2 0 0.1 1"/></rect>')
        parts.append('</clipPath>')
        parts.append(f'<text x="12" y="{y:.1f}" clip-path="url(#{clip_id})">{escape(row)}</text>')

        # small cursor block riding the wipe edge of each row
        parts.append(f'<rect x="12" y="{y - CHAR_H + 2:.1f}" width="{CHAR_W:.1f}" '
                      f'height="{CHAR_H:.1f}" fill="#A90E02" opacity="0">'
                      f'<animate attributeName="x" from="12" to="{12 + row_w - CHAR_W:.1f}" '
                      f'begin="{begin:.3f}s" dur="{ROW_DURATION}s" fill="freeze" '
                      f'calcMode="spline" keySplines="0.2 0 0.1 1"/>'
                      f'<animate attributeName="opacity" values="0.9;0.9;0" '
                      f'keyTimes="0;0.92;1" begin="{begin:.3f}s" dur="{ROW_DURATION}s" fill="freeze"/>'
                      f'</rect>')

    parts.append('</svg>')

    with open(out_path, "w") as f:
        f.write("\n".join(parts))
    print(f"wrote {out_path}  ({cols}x{rows} chars)")


if __name__ == "__main__":
    grid = to_grid("data/prepped.png")
    build_svg(grid)
