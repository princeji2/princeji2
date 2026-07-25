"""
make_info_card.py
Hand-authors a neofetch-style panel: title bar, then key/value rows that
fade and slide in on a short stagger, like the portrait "printing" beside it.

Usage:
    python scripts/make_info_card.py
    STATIC=1 python scripts/make_info_card.py   # frozen frame, no animation
"""
import os

BG = "#FFFBD4"
PANEL = "#FFF8E0"
BORDER = "#E8DFC2"
INK = "#2B2A25"
MUTED = "#8A8370"
LABEL = "#A90E02"
ACCENT = "#CBA35C"

WIDTH = 560
ROW_H = 30
STAGGER = 0.09
DUR = 0.5
STATIC = os.environ.get("STATIC") == "1"

ROWS = [
    ("user", "prince@naruka-ai-labs"),
    ("os", "B.Tech CSE (IoT) — Poornima Institute of Eng. & Tech."),
    ("now", "Naruka AI Labs — solo AI R&D studio"),
    ("prev", "College Council Event Management System"),
    ("stack", "Python · TypeScript · Next.js · PostgreSQL"),
    ("ai", "LangGraph · Langfuse · RAGAS · MCP · Ollama"),
    ("highlight", "AEGIS NOCTURNE — 360° radar on an ESP32"),
    ("learning", "NeetCode 150 · pgvector · agentic systems"),
]


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def anim(attr, frm, to, begin, dur=DUR):
    if STATIC:
        return ""
    return (f'<animate attributeName="{attr}" from="{frm}" to="{to}" '
            f'begin="{begin:.3f}s" dur="{dur}s" fill="freeze" '
            f'calcMode="spline" keySplines="0.2 0 0.1 1"/>')


def build():
    height = 78 + len(ROWS) * ROW_H + 24
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
              f'viewBox="0 0 {WIDTH} {height}">')
    p.append(f'<style>text{{font-family:"SF Mono","JetBrains Mono",Menlo,Consolas,monospace;}}</style>')
    p.append(f'<rect width="100%" height="100%" fill="{BG}"/>')
    p.append(f'<rect x="0.5" y="0.5" width="{WIDTH-1}" height="{height-1}" rx="10" '
              f'fill="{PANEL}" stroke="{BORDER}"/>')

    # title bar
    p.append(f'<rect x="0.5" y="0.5" width="{WIDTH-1}" height="40" rx="10" fill="{PANEL}"/>')
    p.append(f'<rect x="0.5" y="30.5" width="{WIDTH-1}" height="10" fill="{PANEL}"/>')
    p.append(f'<line x1="0.5" y1="40.5" x2="{WIDTH-0.5}" y2="40.5" stroke="{BORDER}"/>')
    p.append(f'<circle cx="24" cy="20" r="5" fill="{ACCENT}" opacity="0.5"/>')
    p.append(f'<circle cx="42" cy="20" r="5" fill="{ACCENT}" opacity="0.3"/>')
    p.append(f'<circle cx="60" cy="20" r="5" fill="{ACCENT}" opacity="0.15"/>')
    p.append(f'<text x="{WIDTH/2}" y="25" text-anchor="middle" font-size="12" '
              f'letter-spacing="2" fill="{MUTED}">prince@github ~ whoami</text>')

    y = 78
    for i, (label, value) in enumerate(ROWS):
        begin = 0.15 + i * STAGGER
        opacity_start = "1" if STATIC else "0"
        transform_start = "" if STATIC else f'translate(-8,0)'
        row_group_open = f'<g opacity="{opacity_start}">' if not STATIC else '<g>'
        p.append(row_group_open)
        if not STATIC:
            p.append(f'<animate attributeName="opacity" from="0" to="1" begin="{begin:.3f}s" '
                      f'dur="{DUR}s" fill="freeze"/>')
        p.append(f'<text x="28" y="{y}" font-size="13" font-weight="600" fill="{LABEL}">{esc(label)}</text>')
        p.append(f'<text x="118" y="{y}" font-size="13" fill="{INK}">{esc(value)}</text>')
        p.append('</g>')
        y += ROW_H

    p.append(f'<line x1="28" x2="{WIDTH-28}" y1="{78 - 22}" y2="{78 - 22}" stroke="{BORDER}"/>')
    p.append('</svg>')

    out = "assets/info-card.svg"
    with open(out, "w") as f:
        f.write("\n".join(p))
    print(f"wrote {out}")


if __name__ == "__main__":
    build()
