"""
fetch_contributions.py

Fetches the real contribution calendar from GitHub's public HTML fragment
(no GraphQL API, no personal access token needed):

    https://github.com/users/<username>/contributions

Parses each day cell's data-date / data-level, plus the "N contributions on
<date>." tooltip for exact counts, and writes data/contributions.json with
raw days + derived stats (current streak, longest streak, best day, total).

Usage:
    python scripts/fetch_contributions.py
"""
import json
import re
import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup

USERNAME = "lalithyaraochavala"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUTPUT_JSON = "data/contributions.json"


def fetch_html(url: str) -> str:
    resp = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0 (profile-readme-bot)"},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.text


def parse_days(html: str):
    soup = BeautifulSoup(html, "html.parser")

    # Build a lookup from cell id -> tooltip text, so we can pull exact counts.
    tooltip_by_id = {}
    for tip in soup.find_all("tool-tip"):
        target_id = tip.get("for")
        if target_id:
            tooltip_by_id[target_id] = tip.get_text(strip=True)

    days = []
    for td in soup.select("td.ContributionCalendar-day"):
        date_str = td.get("data-date")
        level_str = td.get("data-level")
        if not date_str or level_str is None:
            continue

        cell_id = td.get("id", "")
        tooltip_text = tooltip_by_id.get(cell_id, "")
        count = 0
        match = re.match(r"(\d+)\s+contributions?", tooltip_text)
        if match:
            count = int(match.group(1))
        # "No contributions on ..." -> count stays 0

        days.append(
            {
                "date": date_str,
                "level": int(level_str),
                "count": count,
            }
        )

    days.sort(key=lambda d: d["date"])
    return days


def compute_stats(days):
    total = sum(d["count"] for d in days)

    # Current streak: consecutive days with count > 0, walking back from the
    # most recent day.
    current_streak = 0
    for d in reversed(days):
        if d["count"] > 0:
            current_streak += 1
        else:
            break

    # Longest streak anywhere in the window.
    longest_streak = 0
    running = 0
    for d in days:
        if d["count"] > 0:
            running += 1
            longest_streak = max(longest_streak, running)
        else:
            running = 0

    best_day = max(days, key=lambda d: d["count"], default=None)

    monthly_totals = {}
    for d in days:
        month_key = d["date"][:7]  # YYYY-MM
        monthly_totals[month_key] = monthly_totals.get(month_key, 0) + d["count"]

    return {
        "total_contributions": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "monthly_totals": monthly_totals,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def main():
    try:
        html = fetch_html(URL)
    except requests.RequestException as e:
        print(f"ERROR fetching {URL}: {e}", file=sys.stderr)
        sys.exit(1)

    days = parse_days(html)
    if not days:
        print("ERROR: no contribution cells parsed, GitHub markup may have changed.", file=sys.stderr)
        sys.exit(1)

    stats = compute_stats(days)
    payload = {"username": USERNAME, "days": days, "stats": stats}

    with open(OUTPUT_JSON, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {OUTPUT_JSON}: {len(days)} days, {stats['total_contributions']} total contributions")


if __name__ == "__main__":
    main()
