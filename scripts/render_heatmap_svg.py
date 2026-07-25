"""
render_heatmap_svg.py
Draws data/contributions.json as the classic 53-week x 7-day grid of
rounded boxes, revealed once with a diagonal slide-down, then frozen.

Usage:
    python scripts/render_heatmap_svg.py
"""
import json
from collections import defaultdict
from datetime import date, datetime

# warm palette in place of GitHub green
PALETTE = ["#F2ECD2", "#E8CFA0", "#D9A85E", "#C96A33", "#A90E02"]
BG = "#FFFBD4"
INK = "#2B2A25"
MUTED = "#8A8370"
ACCENT = "#CBA35C"

CELL = 11
GAP = 3
LEFT_PAD = 34
TOP_PAD = 28
STAGGER = 0.012
DUR = 0.4


def load():
    with open("data/contributions.json") as f:
        return json.load(f)


def to_weeks(days):
    """Group day records into 53 columns of 7 rows (Sun..Sat), like the GitHub grid."""
    by_date = {d["date"]: d["level"] for d in days}
    if not days:
        return []
    first = datetime.strptime(days[0]["date"], "%Y-%m-%d").date()
    last = datetime.strptime(days[-1]["date"], "%Y-%m-%d").date()

    # back up to the preceding Sunday so weeks align to columns
    start = first
    while start.weekday() != 6:  # Sunday = 6 in Python's Mon=0 scheme? Mon=0..Sun=6, so 6 IS Sunday
        start = date.fromordinal(start.toordinal() - 1)

    weeks = defaultdict(dict)
    cur = start
    col = 0
    while cur <= last:
        row = (cur.weekday() + 1) % 7  # convert Mon=0..Sun=6 -> Sun=0..Sat=6
        weeks[col][row] = by_date.get(cur.isoformat(), None)
        if row == 6:
            col += 1
        cur = date.fromordinal(cur.toordinal() + 1)
    return weeks


MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def build(data):
    weeks = to_weeks(data["days"])
    n_cols = max(weeks.keys()) + 1 if weeks else 0
    width = LEFT_PAD + n_cols * (CELL + GAP) + 140
    height = TOP_PAD + 7 * (CELL + GAP) + 46

    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
              f'viewBox="0 0 {width} {height}">')
    p.append('<style>text{font-family:"SF Mono","JetBrains Mono",Menlo,Consolas,monospace;}</style>')
    p.append(f'<rect width="100%" height="100%" fill="{BG}"/>')

    day_labels = {1: "Mon", 3: "Wed", 5: "Fri"}
    for row, label in day_labels.items():
        y = TOP_PAD + row * (CELL + GAP) + CELL - 1
        p.append(f'<text x="0" y="{y}" font-size="9" fill="{MUTED}">{label}</text>')

    last_month = None
    dates_by_col = {}
    by_date_list = data["days"]
    if by_date_list:
        first = datetime.strptime(by_date_list[0]["date"], "%Y-%m-%d").date()
        start = first
        while start.weekday() != 6:
            start = date.fromordinal(start.toordinal() - 1)
        cur = start
        col = 0
        while col < n_cols:
            row = (cur.weekday() + 1) % 7
            if row == 0:
                dates_by_col[col] = cur
            if row == 6:
                col += 1
            cur = date.fromordinal(cur.toordinal() + 1)

    for col in sorted(dates_by_col.keys()):
        d = dates_by_col[col]
        if d.month != last_month:
            x = LEFT_PAD + col * (CELL + GAP)
            p.append(f'<text x="{x}" y="{TOP_PAD - 10}" font-size="9" fill="{MUTED}">'
                      f'{MONTH_NAMES[d.month-1]}</text>')
            last_month = d.month

    idx = 0
    for col in sorted(weeks.keys()):
        for row in range(7):
            lvl = weeks[col].get(row)
            x = LEFT_PAD + col * (CELL + GAP)
            y = TOP_PAD + row * (CELL + GAP)
            color = PALETTE[lvl] if lvl is not None else "#00000000"
            if lvl is None:
                continue
            begin = (col + row) * STAGGER
            p.append(f'<rect x="{x}" y="{y - 6}" width="{CELL}" height="{CELL}" rx="2.5" '
                      f'fill="{color}" opacity="0">'
                      f'<animate attributeName="y" from="{y-6}" to="{y}" begin="{begin:.3f}s" '
                      f'dur="{DUR}s" fill="freeze" calcMode="spline" keySplines="0.2 0 0.1 1"/>'
                      f'<animate attributeName="opacity" from="0" to="1" begin="{begin:.3f}s" '
                      f'dur="{DUR}s" fill="freeze"/>'
                      f'</rect>')
            idx += 1

    # legend
    ly = TOP_PAD + 7 * (CELL + GAP) + 22
    lx = LEFT_PAD
    p.append(f'<text x="{lx}" y="{ly+8}" font-size="9" fill="{MUTED}">Less</text>')
    for i, c in enumerate(PALETTE):
        p.append(f'<rect x="{lx + 34 + i*(CELL+3)}" y="{ly}" width="{CELL}" height="{CELL}" '
                  f'rx="2.5" fill="{c}"/>')
    p.append(f'<text x="{lx + 34 + len(PALETTE)*(CELL+3) + 6}" y="{ly+8}" font-size="9" '
              f'fill="{MUTED}">More</text>')

    stats = (f"{data['total']} contributions in the last year  ·  "
             f"current streak {data['current_streak']}  ·  longest {data['longest_streak']}")
    p.append(f'<text x="{width - 24}" y="{ly+8}" text-anchor="end" font-size="10.5" '
              f'fill="{INK}">{stats}</text>')

    p.append('</svg>')

    out = "assets/contrib-heatmap.svg"
    with open(out, "w") as f:
        f.write("\n".join(p))
    print(f"wrote {out}  ({width:.0f}x{height:.0f})")


if __name__ == "__main__":
    build(load())
