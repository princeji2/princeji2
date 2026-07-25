"""
fetch_contributions.py
Pulls the public contribution calendar HTML GitHub itself uses for the
profile page — no GraphQL API, no personal access token.

Usage:
    python scripts/fetch_contributions.py
"""
import json
import re
from datetime import date

import requests
from bs4 import BeautifulSoup

USERNAME = "princeji2"
URL = f"https://github.com/users/{USERNAME}/contributions"


def fetch():
    resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    resp.raise_for_status()
    return resp.text


def parse(html: str):
    soup = BeautifulSoup(html, "html.parser")

    total_match = re.search(r"([\d,]+)\s+contributions?\s+in the last year", html)
    total = int(total_match.group(1).replace(",", "")) if total_match else None

    cells = soup.select("td.ContributionCalendar-day")
    days = []
    for td in cells:
        d = td.get("data-date")
        lvl = td.get("data-level")
        if d is None or lvl is None:
            continue
        days.append({"date": d, "level": int(lvl)})

    days.sort(key=lambda x: x["date"])

    # streaks
    current_streak = longest_streak = run = 0
    for day in days:
        if day["level"] > 0:
            run += 1
            longest_streak = max(longest_streak, run)
        else:
            run = 0
    for day in reversed(days):
        if day["level"] > 0:
            current_streak += 1
        else:
            break

    best_day = max(days, key=lambda d: d["level"]) if days else None

    return {
        "username": USERNAME,
        "generated": date.today().isoformat(),
        "total": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day["date"] if best_day else None,
        "days": days,
    }


if __name__ == "__main__":
    data = parse(fetch())
    with open("data/contributions.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"wrote data/contributions.json — {data['total']} contributions, "
          f"streak {data['current_streak']} (longest {data['longest_streak']})")
