"""
make_info_card.py

Hand-authored neofetch-style SVG panel: a title bar plus colored key/value
rows that fade + slide in on a short stagger, like text printing next to
the ASCII portrait.

Edit the CONTENT dict below to change what shows up on the card.

Env:
    STATIC=1   emits a frozen (non-animated) frame, useful for local
               Quick Look / image-viewer previews where SMIL doesn't play.

Usage:
    python scripts/make_info_card.py

Writes: info-card.svg
"""
import os

USERNAME = "lalithyaraochavala"
TITLE = f"{USERNAME}@github"

# Edit this to change the card content. Keep it to story numbers can't
# tell -- the heatmap already covers your GitHub stats.
CONTENT = [
    ("Now", "Building AI tools & automation"),
    ("Prev", "Ad-tech / weather-driven campaigns"),
    ("Stack", "Python · FastAPI · JavaScript · HTML/CSS · Git"),
    ("Highlights", "ai-prompt-checker — free AI prompt scorer"),
    ("", "dynamo-mvp — weather-driven ad engine, live on Railway"),
    ("Base", "Bangalore, India"),
]

WIDTH = 490
ROW_H = 34
PADDING_TOP = 70
FONT_FAMILY = "Menlo, Consolas, monospace"
KEY_COLOR = "#39d353"
VAL_COLOR = "#c9d1d9"
BG_COLOR = "#0d1117"
BORDER_COLOR = "#30363d"
TITLE_COLOR = "#8b949e"

STATIC = os.environ.get("STATIC") == "1"
OUTPUT_SVG = "info-card.svg"


def escape_xml(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg():
    height = PADDING_TOP + len(CONTENT) * ROW_H + 20
    rows_svg = []

    for i, (key, val) in enumerate(CONTENT):
        y = PADDING_TOP + i * ROW_H
        delay = 0.3 + i * 0.12
        key_x = 24
        val_x = 130 if key else 24

        anim = "" if STATIC else f'''
        <animate attributeName="opacity" from="0" to="1"
          begin="{delay}s" dur="0.3s" fill="freeze" />
        <animateTransform attributeName="transform" type="translate"
          from="-12 0" to="0 0" begin="{delay}s" dur="0.3s" fill="freeze"
          additive="sum" />'''
        opacity_attr = "1" if STATIC else "0"

        line = f'''
  <g opacity="{opacity_attr}">{anim}
    {f'<text x="{key_x}" y="{y}" font-family="{FONT_FAMILY}" font-size="13" font-weight="bold" fill="{KEY_COLOR}">{escape_xml(key)}</text>' if key else ''}
    <text x="{val_x}" y="{y}" font-family="{FONT_FAMILY}" font-size="13" fill="{VAL_COLOR}">{escape_xml(val)}</text>
  </g>'''
        rows_svg.append(line)

    body = "\n".join(rows_svg)

    title_anim = "" if STATIC else '''
    <animate attributeName="opacity" from="0" to="1" begin="0s" dur="0.3s" fill="freeze" />'''
    title_opacity = "1" if STATIC else "0"

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}"
     width="{WIDTH}" height="{height}">
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="8"
    fill="{BG_COLOR}" stroke="{BORDER_COLOR}" />
  <g opacity="{title_opacity}">{title_anim}
    <circle cx="24" cy="26" r="6" fill="#ff5f56" />
    <circle cx="44" cy="26" r="6" fill="#ffbd2e" />
    <circle cx="64" cy="26" r="6" fill="#27c93f" />
    <text x="86" y="31" font-family="{FONT_FAMILY}" font-size="13"
      fill="{TITLE_COLOR}">{escape_xml(TITLE)}</text>
  </g>
  <line x1="0" y1="46" x2="{WIDTH}" y2="46" stroke="{BORDER_COLOR}" />
{body}
</svg>'''


def main():
    svg = build_svg()
    with open(OUTPUT_SVG, "w") as f:
        f.write(svg)
    print(f"Wrote {OUTPUT_SVG}" + (" (static)" if STATIC else ""))


if __name__ == "__main__":
    main()
