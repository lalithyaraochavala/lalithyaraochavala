"""
make_ascii_svg.py

Converts source-prepped.png (grayscale, background-removed, contrast-boosted)
into a monochrome ASCII-art SVG that "types" itself row by row using SMIL
animation. GitHub renders SMIL/CSS-keyframe animation inside <img>-embedded
SVGs, so this plays on the profile page with no JS.

Usage:
    python scripts/make_ascii_svg.py

Reads:  source-prepped.png
Writes: avi-ascii.svg   (renamed here to match the profile's own image name)
"""
from PIL import Image

# Bright (sparse) -> dark (dense). Leading space clears background to nothing.
RAMP = " .`:-=+*cs#%@"

COLS = 100
ROWS = 53
FONT_SIZE = 8
CHAR_W = FONT_SIZE * 0.6
CHAR_H = FONT_SIZE * 1.05
FILL_COLOR = "#8b949e"  # single light-gray, monochrome by design
BG_COLOR = "transparent"

INPUT_IMAGE = "source-prepped.png"
OUTPUT_SVG = "avi-ascii.svg"


def image_to_ascii_grid(path: str, cols: int, rows: int):
    img = Image.open(path).convert("L").resize((cols, rows))
    pixels = list(img.getdata())
    grid = []
    ramp_len = len(RAMP)
    for r in range(rows):
        row_chars = []
        for c in range(cols):
            brightness = pixels[r * cols + c]  # 0 dark .. 255 bright
            # invert: bright -> low ramp index (sparse), dark -> high index (dense)
            idx = int((255 - brightness) / 255 * (ramp_len - 1))
            row_chars.append(RAMP[idx])
        grid.append("".join(row_chars))
    return grid


def escape_xml(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_svg(grid):
    width = COLS * CHAR_W + 20
    height = ROWS * CHAR_H + 20
    rows_svg = []

    for r, row_text in enumerate(grid):
        row_text = escape_xml(row_text) or " "
        y = 10 + (r + 1) * CHAR_H
        delay = r * 0.035  # stagger top -> bottom
        row_id = f"row{r}"

        # Each row lives inside a clipPath that wipes left-to-right.
        rows_svg.append(f'''
  <clipPath id="clip-{row_id}">
    <rect x="0" y="{y - CHAR_H}" width="0" height="{CHAR_H + 2}">
      <animate attributeName="width" from="0" to="{width}"
        begin="{delay}s" dur="0.4s" fill="freeze" />
    </rect>
  </clipPath>
  <text x="10" y="{y}" font-family="Menlo, Consolas, monospace"
    font-size="{FONT_SIZE}" fill="{FILL_COLOR}"
    clip-path="url(#clip-{row_id})" xml:space="preserve">{row_text}</text>
  <rect x="10" y="{y - CHAR_H + 1}" width="{CHAR_W}" height="{CHAR_H - 1}"
    fill="{FILL_COLOR}" opacity="0.9">
    <animate attributeName="x" from="10" to="{width - CHAR_W}"
      begin="{delay}s" dur="0.4s" fill="freeze" />
    <animate attributeName="opacity" from="0.9" to="0"
      begin="{delay + 0.4}s" dur="0.05s" fill="freeze" />
  </rect>''')

    body = "\n".join(rows_svg)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {height:.0f}"
     width="{width:.0f}" height="{height:.0f}">
  <rect width="100%" height="100%" fill="{BG_COLOR}" />
{body}
</svg>'''


def main():
    grid = image_to_ascii_grid(INPUT_IMAGE, COLS, ROWS)
    svg = build_svg(grid)
    with open(OUTPUT_SVG, "w") as f:
        f.write(svg)
    print(f"Wrote {OUTPUT_SVG}")


if __name__ == "__main__":
    main()
