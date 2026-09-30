#!/usr/bin/env python3
"""gantt.py — render a clean, readable SVG Gantt chart from release data.

Stdlib only. Workstreams are swimlanes, milestones are bars colored by
status, gates are diamonds, dependencies are arrows, and the status-as-of
date is drawn as a vertical "today" line.

Public entry point: render_gantt(milestones, workstreams, as_of, title, out_path)
where milestones is a list of dicts with keys:
    id, name, workstream, start (date), end (date), deps (list of ids),
    status ('done' | 'on-track' | 'at-risk'), type ('milestone' | 'gate')
"""

import datetime
from xml.sax.saxutils import escape

# ---------------------------------------------------------------- layout ----
WIDTH = 1500
LABEL_W = 310          # left column for "ID - name"
RIGHT_PAD = 30
TOP = 84               # space for title + month labels
ROW_H = 30
LANE_GAP = 10          # extra space between workstream swimlanes
BOTTOM = 76            # legend + footer
FONT = "font-family='-apple-system,Segoe UI,Helvetica,Arial,sans-serif'"

STATUS_FILL = {
    "done": "#9ca3af",
    "on-track": "#2563eb",
    "at-risk": "#dc2626",
}
STATUS_LABEL = {"done": "done", "on-track": "on track", "at-risk": "at risk"}


def _truncate(text, max_chars):
    return text if len(text) <= max_chars else text[: max_chars - 1] + "…"


def render_gantt(milestones, workstreams, as_of, title, out_path):
    """Render milestones to an SVG file. Returns the output path."""
    ws_order = [w["id"] for w in workstreams]
    ws_name = {w["id"]: w["name"] for w in workstreams}

    # Group rows by workstream, preserving milestone file order.
    lanes = [(wid, [m for m in milestones if m["workstream"] == wid])
             for wid in ws_order]
    lanes = [(wid, rows) for wid, rows in lanes if rows]

    starts = [m["_start"] for m in milestones]
    ends = [m["_end"] for m in milestones]
    d_min = min(starts) - datetime.timedelta(days=3)
    d_max = max(ends) + datetime.timedelta(days=3)
    total_days = (d_max - d_min).days or 1

    plot_w = WIDTH - LABEL_W - RIGHT_PAD

    def x_of(day):
        return LABEL_W + (day - d_min).days / total_days * plot_w

    # Assign y positions.
    row_y = {}          # milestone id -> top y of its row
    lane_bands = []     # (workstream id, y_top, y_bottom)
    y = TOP
    for wid, rows in lanes:
        top = y
        for m in rows:
            row_y[m["id"]] = y
            y += ROW_H
        lane_bands.append((wid, top, y))
        y += LANE_GAP
    height = int(y - LANE_GAP + BOTTOM)

    parts = []
    a = parts.append
    a(f"<svg xmlns='http://www.w3.org/2000/svg' width='{WIDTH}' height='{height}' "
      f"viewBox='0 0 {WIDTH} {height}' role='img'>")
    a("<defs>"
      "<marker id='arr' viewBox='0 0 10 10' refX='8' refY='5' "
      "markerWidth='7' markerHeight='7' orient='auto-start-reverse'>"
      "<path d='M 0 1 L 9 5 L 0 9 z' fill='#4b5563'/></marker>"
      "</defs>")
    a(f"<rect x='0' y='0' width='{WIDTH}' height='{height}' fill='#ffffff'/>")

    # Title.
    a(f"<text x='{LABEL_W}' y='30' {FONT} font-size='20' font-weight='700' "
      f"fill='#111827'>{escape(title)}</text>")
    a(f"<text x='{LABEL_W}' y='52' {FONT} font-size='12' fill='#6b7280'>"
      f"Fictional / illustrative release program — generated {as_of.isoformat()}</text>")

    # Swimlane bands + labels.
    for i, (wid, top, bottom) in enumerate(lane_bands):
        fill = "#f9fafb" if i % 2 == 0 else "#f3f4f6"
        a(f"<rect x='0' y='{top}' width='{WIDTH}' height='{bottom - top}' fill='{fill}'/>")
        a(f"<text x='14' y='{top + 20}' {FONT} font-size='12' font-weight='700' "
          f"fill='#374151'>{escape(ws_name[wid])}</text>")

    # Month gridlines + labels; light weekly lines.
    day = d_min
    while day <= d_max:
        x = x_of(day)
        if day.day == 1:
            a(f"<line x1='{x:.1f}' y1='{TOP - 22}' x2='{x:.1f}' y2='{height - BOTTOM}' "
              f"stroke='#d1d5db' stroke-width='1'/>")
            a(f"<text x='{x + 4:.1f}' y='{TOP - 28}' {FONT} font-size='11' "
              f"fill='#6b7280'>{day.strftime('%b %Y')}</text>")
        elif day.weekday() == 0:
            a(f"<line x1='{x:.1f}' y1='{TOP - 22}' x2='{x:.1f}' y2='{height - BOTTOM}' "
              f"stroke='#e5e7eb' stroke-width='1' stroke-dasharray='2,3'/>")
        day += datetime.timedelta(days=1)

    by_id = {m["id"]: m for m in milestones}

    def bar_geom(m):
        """Return (x1, x2, y_mid) anchor points for arrows/bars."""
        yt = row_y[m["id"]]
        y_mid = yt + ROW_H / 2
        x1 = x_of(m["_start"])
        x2 = x_of(m["_end"])
        return x1, x2, y_mid

    # Dependency arrows (drawn under the bars).
    for m in milestones:
        _, x2m, ym = bar_geom(m)
        for dep_id in m["deps"]:
            dep = by_id.get(dep_id)
            if dep is None:
                continue
            xd1, xd2, yd = bar_geom(dep)
            # elbow: from dep end -> horizontal -> vertical -> into milestone start
            x_start = x_of(m["_start"])
            mid_x = (xd2 + x_start) / 2
            a(f"<path d='M {xd2:.1f} {yd:.1f} L {mid_x:.1f} {yd:.1f} "
              f"L {mid_x:.1f} {ym:.1f} L {x_start - 2:.1f} {ym:.1f}' "
              f"fill='none' stroke='#4b5563' stroke-width='1.2' marker-end='url(#arr)'/>")

    # Bars, diamonds, and row labels.
    for m in milestones:
        yt = row_y[m["id"]]
        y_mid = yt + ROW_H / 2
        fill = STATUS_FILL[m["status"]]
        x1 = x_of(m["_start"])
        x2 = x_of(m["_end"])
        label = _truncate(f"{m['id']} — {m['name']}", 44)
        a(f"<text x='14' y='{y_mid + 4:.1f}' {FONT} font-size='12' fill='#1f2937'>"
          f"{escape(label)}</text>")
        if m["type"] == "gate":
            cx = (x1 + x2) / 2
            r = 9
            a(f"<path d='M {cx:.1f} {y_mid - r:.1f} L {cx + r:.1f} {y_mid:.1f} "
              f"L {cx:.1f} {y_mid + r:.1f} L {cx - r:.1f} {y_mid:.1f} Z' "
              f"fill='{fill}' stroke='#111827' stroke-width='2'/>")
        else:
            w = max(x2 - x1, 3)
            a(f"<rect x='{x1:.1f}' y='{yt + 7:.1f}' width='{w:.1f}' height='16' "
              f"rx='4' fill='{fill}'/>")
            # date range inside the label column area for short bars
            a(f"<text x='{x2 + 6:.1f}' y='{y_mid + 4:.1f}' {FONT} font-size='10' "
              f"fill='#6b7280'>{m['_start'].strftime('%m/%d')}–{m['_end'].strftime('%m/%d')}</text>")

    # Today / status-as-of line.
    xt = x_of(as_of)
    a(f"<line x1='{xt:.1f}' y1='{TOP - 22}' x2='{xt:.1f}' y2='{height - BOTTOM}' "
      f"stroke='#111827' stroke-width='1.5' stroke-dasharray='6,4'/>")
    a(f"<text x='{xt + 6:.1f}' y='{TOP - 8}' {FONT} font-size='11' font-weight='700' "
      f"fill='#111827'>status as of {as_of.strftime('%b %d, %Y')}</text>")

    # Legend.
    ly = height - BOTTOM + 28
    lx = LABEL_W
    a(f"<text x='{lx}' y='{ly}' {FONT} font-size='12' font-weight='700' fill='#111827'>Legend:</text>")
    lx += 70
    for key in ("done", "on-track", "at-risk"):
        a(f"<rect x='{lx}' y='{ly - 11}' width='34' height='12' rx='3' fill='{STATUS_FILL[key]}'/>")
        a(f"<text x='{lx + 40}' y='{ly}' {FONT} font-size='12' fill='#374151'>{STATUS_LABEL[key]}</text>")
        lx += 118
    a(f"<path d='M {lx} {ly - 6} l 7 -7 l 7 7 l -7 7 Z' fill='#ffffff' "
      f"stroke='#111827' stroke-width='2'/>")
    a(f"<text x='{lx + 20}' y='{ly}' {FONT} font-size='12' fill='#374151'>phase gate</text>")
    a(f"<text x='{LABEL_W}' y='{ly + 22}' {FONT} font-size='11' fill='#6b7280'>"
      f"Arrows show finish-to-start dependencies. All data fictional and illustrative.</text>")

    a("</svg>")
    with open(out_path, "w") as f:
        f.write("\n".join(parts))
    return out_path


if __name__ == "__main__":
    print("gantt.py is a library module — run src/build.py to generate the chart.")
