"""
render_heatmap_svg.py

Renders data/contributions.json as the classic 53-week x 7-day calendar of
rounded, colored boxes (GitHub-ish green ramp), revealed once with a
diagonal line-after-line slide-down (plays once on load, then freezes --
no looping). Adds a Less -> More legend and a stats footer.

Usage:
    python scripts/render_heatmap_svg.py

Reads:  data/contributions.json
Writes: contrib-heatmap.svg
"""
import json
from collections import defaultdict
from datetime import datetime

INPUT_JSON = "data/contributions.json"
OUTPUT_SVG = "contrib-heatmap.svg"

# none -> brightest (level 5 kept as a neon top end beyond GitHub's native 4)
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

CELL = 12
GAP = 3
LEFT_PAD = 30
TOP_PAD = 20
BOTTOM_PAD = 40
FONT_FAMILY = "Menlo, Consolas, monospace"
TEXT_COLOR = "#8b949e"

MONTH_LABELS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]


def clamp_level(level: int) -> int:
    return max(0, min(level, len(PALETTE) - 1))


def build_week_grid(days):
    """Group days into weeks (columns), Sun-Sat (rows), like GitHub's own graph."""
    parsed = [
        {**d, "dt": datetime.strptime(d["date"], "%Y-%m-%d")} for d in days
    ]
    parsed.sort(key=lambda d: d["dt"])
    if not parsed:
        return []

    weeks = []
    current_week = [None] * 7
    first_dow = parsed[0]["dt"].weekday()  # Monday=0 .. Sunday=6
    first_dow_sun0 = (first_dow + 1) % 7  # convert to Sunday=0

    idx = 0
    for i in range(first_dow_sun0):
        current_week[i] = None
    for d in parsed:
        dow = (d["dt"].weekday() + 1) % 7  # Sunday=0
        if dow == 0 and any(c is not None for c in current_week):
            weeks.append(current_week)
            current_week = [None] * 7
        current_week[dow] = d
    weeks.append(current_week)
    return weeks


def escape_xml(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg(payload):
    days = payload["days"]
    stats = payload["stats"]
    username = payload.get("username", "")

    weeks = build_week_grid(days)
    n_weeks = len(weeks)

    grid_width = n_weeks * (CELL + GAP)
    grid_height = 7 * (CELL + GAP)
    width = LEFT_PAD + grid_width + 20
    height = TOP_PAD + grid_height + BOTTOM_PAD + 30

    cells_svg = []
    month_labels_svg = []
    last_month = None

    for w, week in enumerate(weeks):
        x = LEFT_PAD + w * (CELL + GAP)

        for entry in week:
            if entry is None:
                continue
            month = entry["dt"].month
            if month != last_month:
                month_labels_svg.append(
                    f'<text x="{x}" y="{TOP_PAD - 6}" font-family="{FONT_FAMILY}" '
                    f'font-size="10" fill="{TEXT_COLOR}">{MONTH_LABELS[month - 1]}</text>'
                )
                last_month = month

        for dow in range(7):
            entry = week[dow]
            if entry is None:
                continue
            y = TOP_PAD + dow * (CELL + GAP)
            level = clamp_level(entry["level"])
            color = PALETTE[level]

            # Diagonal reveal: delay grows with week index + day-of-week.
            delay = 0.15 + (w + dow) * 0.012
            cells_svg.append(f'''
    <rect x="{x}" y="{y - 6}" width="{CELL}" height="{CELL}" rx="2" ry="2"
      fill="{color}" opacity="0">
      <animate attributeName="y" from="{y - 6}" to="{y}"
        begin="{delay}s" dur="0.28s" fill="freeze" calcMode="spline"
        keySplines="0.2 0.8 0.2 1" />
      <animate attributeName="opacity" from="0" to="1"
        begin="{delay}s" dur="0.28s" fill="freeze" />
    </rect>''')

    total = stats.get("total_contributions", 0)
    current_streak = stats.get("current_streak", 0)
    longest_streak = stats.get("longest_streak", 0)

    footer_y = TOP_PAD + grid_height + 24
    footer_text = (
        f"{total} contributions in the last year"
        f"   \u00b7   current streak {current_streak}"
        f"   \u00b7   longest streak {longest_streak}"
    )

    legend_x = width - 150
    legend_y = footer_y
    legend_swatches = "".join(
        f'<rect x="{legend_x + 34 + i * (CELL + GAP)}" y="{legend_y - 10}" '
        f'width="{CELL}" height="{CELL}" rx="2" ry="2" fill="{PALETTE[i]}" />'
        for i in range(len(PALETTE))
    )

    cells_body = "\n".join(cells_svg)
    months_body = "\n  ".join(month_labels_svg)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}"
     width="{width}" height="{height}">
  <rect width="100%" height="100%" fill="transparent" />
  {months_body}
{cells_body}
  <text x="{LEFT_PAD}" y="{footer_y}" font-family="{FONT_FAMILY}" font-size="11"
    fill="{TEXT_COLOR}">{escape_xml(footer_text)}</text>
  <text x="{legend_x}" y="{legend_y}" font-family="{FONT_FAMILY}" font-size="10"
    fill="{TEXT_COLOR}">Less</text>
  {legend_swatches}
  <text x="{legend_x + 34 + len(PALETTE) * (CELL + GAP) + 4}" y="{legend_y}"
    font-family="{FONT_FAMILY}" font-size="10" fill="{TEXT_COLOR}">More</text>
</svg>'''


def main():
    with open(INPUT_JSON) as f:
        payload = json.load(f)

    svg = build_svg(payload)
    with open(OUTPUT_SVG, "w") as f:
        f.write(svg)
    print(f"Wrote {OUTPUT_SVG}")


if __name__ == "__main__":
    main()
