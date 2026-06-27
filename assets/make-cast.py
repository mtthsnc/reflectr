#!/usr/bin/env python3
"""
Generate assets/reflect-review.cast — an asciicast v2 recording of a /reflect-review
session, used to render assets/reflect-review.gif for the README.

This is an illustrative, scripted demo (the real flow is interactive with Claude),
but every line mirrors the actual /reflect-review skill output. Regenerate the gif:

    python3 assets/make-cast.py
    agg --theme monokai --font-size 14 assets/reflect-review.cast assets/reflect-review.gif
"""
import json
import os

WIDTH, HEIGHT = 92, 28

# ANSI helpers
R = "\033[0m"
DIM = "\033[2m"
B = "\033[1m"
GRN = "\033[32m"
RED = "\033[31m"
CYN = "\033[36m"
YLW = "\033[33m"

events = []
t = 0.4


def out(s, dt=0.0):
    global t
    t += dt
    events.append([round(t, 3), "o", s])


def line(s="", dt=0.25):
    out(s + "\r\n", dt)


def typed(prefix, text, dt=0.06, after=0.5):
    """Type `text` char-by-char after a prompt prefix."""
    out(prefix)
    for ch in text:
        out(ch, dt)
    out("\r\n", after)


# ---- session ----
line(f"{DIM}$ claude{R}", 0.6)
line(f"{DIM}  Claude Code — reflect demo{R}", 0.4)
line("", 0.3)
typed(f"{CYN}>{R} ", "/reflect-review", dt=0.07, after=0.7)

line("", 0.2)
line(f"{DIM}Reading the queue…{R}", 0.9)
line("", 0.3)
line(f"{B}▸ Reflection queue{R}  {DIM}(3 candidates){R}", 0.5)
line("", 0.2)

line(f"{B}Memories (2){R}", 0.4)
line(f"  • {CYN}user-frontend-engineer{R}    {DIM}[user]{R}", 0.35)
line(f"      {DIM}Use when … a frontend-oriented, AI-first engineer{R}", 0.35)
line(f"  • {CYN}project-fcp{R}               {DIM}[project]{R}", 0.35)
line(f"      {DIM}Use when … the Frontend Context Protocol: conventions-as-code{R}", 0.35)
line("", 0.2)
line(f"{B}Docs (1){R}", 0.4)
line(f"  • {CYN}frontend-context-protocol{R}  {DIM}BCP→frontend mapping table{R}", 0.5)
line("", 0.4)

line(f"{B}Approve all, reject all, or pick per-item?{R}", 0.6)
typed(f"{CYN}>{R} ", "accept project-fcp, reject the rest", dt=0.045, after=0.8)

line("", 0.2)
line(f"{DIM}Promoting…{R}", 0.8)
line(f"  {GRN}✓{R} project-fcp {DIM}→ store/memories/{R}", 0.45)
line(f"  {GRN}✓{R} INDEX.md regenerated", 0.45)
line(f"  {RED}✗{R} rejected: user-frontend-engineer", 0.45)
line(f"  {YLW}✓{R} queue cleared", 0.6)
line("", 0.3)
line(f"{B}Done.{R} 1 promoted, 1 rejected.", 0.4)
line(f"{DIM}The retrieval hook will surface it in future prompts automatically.{R}", 1.8)

header = {"version": 2, "width": WIDTH, "height": HEIGHT,
         "env": {"TERM": "xterm-256color", "SHELL": "/bin/bash"}}

dst = os.path.join(os.path.dirname(__file__), "reflect-review.cast")
with open(dst, "w", encoding="utf-8") as f:
    f.write(json.dumps(header) + "\n")
    for e in events:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")
print(f"wrote {dst} ({len(events)} events, {events[-1][0]}s)")
