#!/usr/bin/env python3
"""Render an exact, text-led GitHub social card from the product's shipped features."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/assets/social-preview.png"
im = Image.new("RGB", (1280, 640), "#101923")
d = ImageDraw.Draw(im)
regular = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
mono = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
def text(x, y, value, size, color="#f2f5f3", font=regular, width=1168):
    face = ImageFont.truetype(font, size)
    assert d.textlength(value, font=face) <= width, value
    d.text((x,y), value, font=face, fill=color, anchor="lt")
text(56, 36, "JEV DECISION GATE", 28, "#d4ff77", bold)
text(1120, 39, "by BPJ", 20, "#b7c6ce", width=110)
text(56, 95, "Issue triage. Ready for your agent.", 48, font=bold)
text(56, 164, "MCP server + Agent Skill + Python CLI", 27, "#b7c6ce")
columns = [
    ("LLM API", "Model output", "Build the workflow"),
    ("DIRECT JEV", "Typed judgments", "Build the workflow"),
    ("OUR MCP", "Batch + validate", "Calibrate + review")]
for i,(title,line1,line2) in enumerate(columns):
    x=56+i*395
    d.rounded_rectangle((x,228,x+378,420),radius=20,fill="#203124" if i==2 else "#1a2836",outline="#d4ff77" if i==2 else "#334554",width=3)
    text(x+22,253,title,25,"#d4ff77" if i==2 else "#8bdded",bold,width=332)
    text(x+22,310,line1,27,width=332)
    text(x+22,357,line2,24,"#b7c6ce",width=332)
text(56,461,"6 MCP tools  /  No-key local demo  /  MIT open source",25,"#d4ff77")
d.line((56,513,1224,513),fill="#334554",width=2)
text(56,553,"github.com/f-tiger/jev-decision-gate",31,font=mono)
OUT.parent.mkdir(parents=True,exist_ok=True)
im.save(OUT,optimize=True)
print(f"{OUT.relative_to(ROOT)}: {OUT.stat().st_size} bytes")
