#!/usr/bin/env python3
"""Render the README walkthrough from actual offline output, with Pillow only.

Run from any directory: python tools/render_readme_demo.py
Set DEMO_CJK_FONT if Noto Sans CJK is installed somewhere else.
This is a designed walkthrough of CLI results, not a recording of a product UI.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from bpj_decision_gate.triage import triage  # noqa: E402
from price_scenario import calculate, SNAPSHOT  # noqa: E402

OUT = ROOT / "docs/assets"
W, H = 900, 760
BG, PANEL, BORDER = "#101923", "#1a2836", "#334554"
TEXT, MUTED, GREEN, AMBER, CYAN = "#f2f5f3", "#b7c6ce", "#d4ff77", "#ffcc7b", "#8bdded"
LATIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
CJK = os.environ.get("DEMO_CJK_FONT", "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")


def font(size, zh=False, bold=False, mono=False):
    return ImageFont.truetype(CJK if zh else MONO if mono else BOLD if bold else LATIN, size)


def text(d, xy, value, size=28, color=TEXT, zh=False, bold=False, mono=False, width=810):
    f = font(size, zh, bold, mono)
    if d.textlength(value, font=f) > width:
        raise ValueError(f"Text exceeds card width: {value}")
    d.text(xy, value, font=f, fill=color, anchor="lt")


def box(d, bounds, fill=PANEL, outline=BORDER):
    d.rounded_rectangle(bounds, radius=18, fill=fill, outline=outline, width=2)


def frame(lang, scene, reveal, rows, summary):
    zh = lang == "zh-CN"
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    text(d, (42, 30), "JEV DECISION GATE", 23, GREEN, bold=True)
    text(d, (740, 30), "by BPJ", 23, MUTED)
    text(d, (42, 70),
         "离线规则 · 合成案例 · 实际输出可复现" if zh else "OFFLINE RULES  /  SYNTHETIC CASES  /  REAL OUTPUT", 21, MUTED, zh)
    headers = ["先把 Issue 整理清楚", "信息不够？留给人工", "误判也要看得见", "先运行，再决定是否接入"] if zh else ["Turn issues into clear suggestions.", "Missing context? Keep it in review.", "Make the misses visible, too.", "Try it before you integrate it."]
    text(d, (42, 115), headers[scene], 36 if not zh else 42, TEXT, zh, bold=True)
    if scene < 3:
        row = rows[scene]
        titles = ["会话过期后登录失败", "用不了", "窄屏下按钮消失"] if zh else [r["title"] for r in rows]
        bodies = [
            ["复现：登录 → 闲置一小时 → 返回页面报错", "预期：重新登录并建立新会话"],
            ["正文：请修一下。", "缺少复现步骤、环境和预期行为"],
            ["复现：设置页面缩窄到 300 px，保存按钮消失", "人工标注为 bug；规则只识别出了 ui 模块"],
        ] if zh else [
            ["Sign in, wait an hour, return: login error.", "Expected: start a fresh session."],
            ["Body: Please fix this.", "No steps, environment or expected behavior."],
            ["At 300 px wide, the save button disappears.", "Human label: bug. Rules identify only ui."],
        ]
        box(d, (42, 183, 858, 341))
        text(d, (64, 202), f"{row['id']}  /  " + ("输入摘要" if zh else "ISSUE EXCERPT"), 20, MUTED, zh)
        text(d, (64, 236), titles[scene], 31, TEXT, zh, bold=True, width=772)
        for i, line in enumerate(bodies[scene]):
            text(d, (64, 279 + 30 * i), line, 23, MUTED, zh, width=772)
        for i, key in enumerate(["kind", "module", "information"]):
            left = 42 + i * 278
            box(d, (left, 365, left + 260, 469))
            name = {"kind": "类型", "module": "模块", "information": "信息"}[key] if zh else key.upper()
            text(d, (left + 19, 383), name, 20, MUTED, zh, width=225)
            if reveal >= i + 1:
                text(d, (left + 19, 419), row["prediction"][key], 28, GREEN if scene == 0 else CYAN, mono=True, width=225)
            else:
                text(d, (left + 19, 419), "...", 28, MUTED)
        box(d, (42, 493, 858, 602), "#302b24", "#6b5737")
        text(d, (64, 515), "REVIEW" if reveal >= 4 else "...", 30, AMBER, bold=True)
        if reveal >= 4:
            msg = "尚未校准，建议保留人工复核" if zh else "Uncalibrated: keep the human review step."
            text(d, (64, 560), msg, 25, AMBER, zh, width=772)
        notes = ["分类建议可检查，复核后再路由。", "unknown 和 missing 也是有用的结果。", "规则会漏判：先评估，再考虑自动接受。"] if zh else ["Inspect the suggestion before routing the issue.", "Unknown and missing are useful outputs.", "Rules miss cases. Evaluate before accepting."]
        text(d, (42, 630), notes[scene], 25, TEXT, zh)
    else:
        box(d, (42, 190, 858, 347))
        text(d, (64, 213), "安装后运行，无需 API 密钥" if zh else "AFTER INSTALLATION  /  NO API KEY", 23, MUTED, zh)
        text(d, (64, 262), "$ bpj-gate demo", 31, GREEN, mono=True)
        text(d, (100, 303), "--out demo-report.json", 26, TEXT, mono=True)
        values = [str(summary["issues"]), f"{sum(r['correct'] for r in summary['all_rows'])}/{summary['issues']}", str(summary["review"])]
        names = ["合成案例", "三项全对", "仍需复核"] if zh else ["SYNTHETIC CASES", "JOINTLY CORRECT", "NEED REVIEW"]
        for i, (value, name) in enumerate(zip(values, names)):
            left = 42 + i * 278
            box(d, (left, 370, left + 260, 499))
            text(d, (left + 19, 390), value if reveal >= i + 1 else "...", 43, GREEN, bold=True)
            text(d, (left + 19, 456), name, 19, MUTED, zh, width=226)
        text(d, (42, 530), "接入方式：CLI / MCP / Skill / Python" if zh else "CLI  /  MCP  /  SKILL  /  PYTHON", 29, TEXT, zh)
        text(d, (42, 577), "用你自己的标注数据，对比规则与 Jev。" if zh else "Compare rules and Jev on your labeled issues.", 27, CYAN, zh)
        text(d, (42, 622), "Jev 实测待完成；当前演示不会修改 GitHub。" if zh else "Live Jev results pending. No GitHub edits.", 24, MUTED, zh)
    d.line((42, 686, 858, 686), fill=BORDER, width=2)
    labels = ["分类", "缺信息", "误判", "试用"] if zh else ["CLASSIFY", "MISSING", "MISSED", "TRY IT"]
    for i, label in enumerate(labels):
        x = 42 + 207 * i
        if i == scene:
            d.rounded_rectangle((x, 684, x + 176, 689), radius=2, fill=GREEN)
        text(d, (x, 707), f"{i + 1:02}  {label}", 20, GREEN if i == scene else MUTED, zh)
    return im


def cost_frame(lang, scene, reveal, rows, summary, prices, calc):
    """Public price math stays visually separate from the actual rules example."""
    zh = lang == "zh-CN"
    if scene == 2:
        im = frame(lang, 0, reveal, rows, summary)
    elif scene == 4:
        im = frame(lang, 3, reveal, rows, summary)
    else:
        im = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(im)
        text(d, (42, 30), "JEV DECISION GATE", 23, GREEN, bold=True)
        text(d, (740, 30), "by BPJ", 23, MUTED)
        text(d, (42, 70), "公开单价测算 · 非 API 实测 · 2026-10-02" if zh else "LIST-PRICE MATH / NOT A LIVE TEST / 2026-10-02", 21, MUTED, zh)
        if scene == 0:
            text(d, (42, 118), "同样的输入 token，账单差多少？" if zh else "Same input tokens. A different bill.", 38 if zh else 36, TEXT, zh, bold=True)
            text(d, (42, 186), f"{calc['baseline_to_jev_input_price_ratio']:.0f}×", 100, GREEN, bold=True)
            text(d, (365, 204), "输入单价之比" if zh else "INPUT PRICE RATIO", 29, TEXT, zh, bold=True, width=490)
            text(d, (365, 254), "Fable 5.1 / Jev 1.13" , 25, MUTED, width=490)
            text(d, (42, 331), "按双方各 1,000,000 输入 token 计算" if zh else "Assume 1,000,000 input tokens on each side", 26, MUTED, zh)
            for i, (label, value, color) in enumerate([
                ("Claude Fable 5.1", calc["baseline_input_usd"], CYAN),
                ("Jev 1.13", calc["jev_input_usd"], GREEN),
            ]):
                y = 390 + i * 106
                text(d, (42, y), label, 27, TEXT)
                text(d, (660, y), f"${value:.3f}" if i else f"${value:.2f}", 31, color, bold=True, width=198)
                d.rounded_rectangle((42, y + 48, 858, y + 70), radius=5, fill=PANEL)
                ratio = value / calc["baseline_input_usd"]
                # Same linear dollar scale. The small Jev bar is not inflated.
                length = round(816 * ratio * ((reveal + 1) / 5))
                if length > 0:
                    d.rectangle((42, y + 48, 42 + length, y + 70), fill=color)
            text(d, (42, 617), "标准未缓存输入价；不等于 token 数减少 238 倍。" if zh else "Uncached input price. NOT 238× fewer tokens.", 25, AMBER, zh)
        elif scene == 1:
            text(d, (42, 118), "分清用量和单价，才知道省在哪" if zh else "Token volume and price are separate.", 38 if zh else 35, TEXT, zh, bold=True)
            box(d, (42, 186, 858, 487))
            text(d, (360, 207), "Fable 5.1", 27, CYAN)
            text(d, (655, 207), "Jev 1.13", 27, GREEN)
            data = [
                ("假设输入量" if zh else "Assumed input", "1,000,000", "1,000,000"),
                ("输入 / 百万" if zh else "Input / 1M", "$10", "$0.042"),
                ("输出 / 百万" if zh else "Output / 1M", "$50", "$0"),
                ("实际用量" if zh else "Live usage", "待实测" if zh else "pending", "待实测" if zh else "pending"),
            ]
            for i, (label, a, b) in enumerate(data):
                y = 265 + i * 51
                text(d, (62, y), label, 25, MUTED, zh, width=285)
                text(d, (360, y), a, 25, TEXT, zh, width=270)
                if reveal >= i + 1:
                    text(d, (655, y), b, 25, GREEN, zh, width=185)
            text(d, (42, 518), "对比 Haiku 4.5：输入单价相差 23.8×" if zh else "Against Haiku 4.5: 23.8× input-price ratio", 29, TEXT, zh)
            text(d, (42, 565), "Jev 输出免费，不代表输出 token 为零。" if zh else "Free output does not mean zero output tokens.", 26, AMBER, zh)
            text(d, (42, 612), "真实请求长度、质量、缓存和回退都要测量。" if zh else "Measure request size, quality, cache and fallback.", 24, MUTED, zh)
        else:
            text(d, (42, 118), "加上回退，收益会怎样变化？" if zh else "What if some decisions need an LLM?", 38 if zh else 35, TEXT, zh, bold=True)
            text(d, (42, 184), "假设 10% 的输入还需调用 Fable 5.1" if zh else "Assume 10% of input also goes to Fable 5.1", 27, MUTED, zh)
            for i, (label, value, color) in enumerate([
                ("Jev：处理全部输入" if zh else "Jev on all input", f"${calc['jev_input_usd']:.3f}", GREEN),
                ("Fable：额外处理 10%" if zh else "Fable on an extra 10%", "$1.000", CYAN),
            ]):
                box(d, (42, 245 + i * 94, 858, 326 + i * 94))
                text(d, (64, 272 + i * 94), label, 27, TEXT, zh, width=570)
                text(d, (665, 270 + i * 94), value if reveal >= i + 1 else "...", 31, color, bold=True, width=180)
            text(d, (42, 449), f"${calc['cascade_input_usd']:.3f}", 72, GREEN, bold=True)
            text(d, (435, 470), f"{calc['baseline_to_cascade_input_cost_ratio']:.1f}× " + ("输入费用之比" if zh else "cost ratio"), 32, TEXT, zh, width=420)
            text(d, (42, 554), "对照基准：只用 Fable 的输入费用 $10" if zh else "Baseline: $10 input cost for Fable alone", 27, TEXT, zh)
            text(d, (42, 603), "仅情景计算，未含输出、重试或人工复核。" if zh else "Scenario only. Excludes output, retries, review.", 25, AMBER, zh)
            text(d, (42, 645), "复核队列不会自动调用 Fable。" if zh else "This tool does not call Fable automatically.", 21, MUTED, zh)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 680, W, H), fill=BG)
    d.line((42, 686, 858, 686), fill=BORDER, width=2)
    labels = ["价格", "用量", "案例", "回退", "试用"] if zh else ["PRICE", "TOKENS", "CASE", "FALLBACK", "TRY IT"]
    for i, label in enumerate(labels):
        x = 42 + 166 * i
        if i == scene:
            d.rounded_rectangle((x, 684, x + 145, 689), radius=2, fill=GREEN)
        text(d, (x, 707), f"{i + 1:02} {label}", 18, GREEN if i == scene else MUTED, zh)
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    issues = json.loads((ROOT / "examples/issues.synthetic.json").read_text())
    report = triage(issues, provider="rules")
    # Exclude variable runtime measurements: the illustration makes no speed claim.
    for row, issue in zip(report["rows"], issues):
        row.pop("latency_ms", None)
        row["title"], row["body"] = issue["title"], issue["body"]
    report["provenance"] = "Actual offline rules output on original synthetic fixtures; English inputs; Chinese captions are translations. Not live Jev output or a product UI recording."
    report["fixture"] = "examples/issues.synthetic.json"
    (OUT / "demo-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    selected = [report["rows"][i] for i in [0, 4, 6]]
    summary = {**report["summary"], "all_rows": report["rows"]}
    prices = json.loads(SNAPSHOT.read_text())
    calc = calculate(prices)
    (OUT / "price-scenario.json").write_text(json.dumps(calc, indent=2) + "\n")
    for lang in ["en", "zh-CN"]:
        frames, durations, settled = [], [], []
        for scene in range(5):
            for reveal in range(5):
                image = cost_frame(lang, scene, reveal, selected, summary, prices, calc)
                frames.append(image.quantize(colors=96, method=Image.Quantize.MEDIANCUT))
                durations.append(400 if reveal < 4 else 4800)
            settled.append(image)
        path = OUT / f"token-cost-{lang}.gif"
        frames[0].save(path, save_all=True, append_images=frames[1:], duration=durations, loop=0, optimize=True, disposal=1)
        settled[0].save(OUT / f"token-cost-{lang}-poster.png", optimize=True)
        print(f"{path.relative_to(ROOT)}: {path.stat().st_size:,} bytes")
        # Contact sheet is an ephemeral QA artifact, not a repository asset.
        qa = os.environ.get("DEMO_QA_DIR")
        if qa:
            dest = Path(qa)
            dest.mkdir(parents=True, exist_ok=True)
            sheet = Image.new("RGB", (W * 2, H * 3), BG)
            for i, still in enumerate(settled):
                sheet.paste(still, ((i % 2) * W, (i // 2) * H))
            sheet.save(dest / f"contact-{lang}.png")
            settled[0].resize((390, 329), Image.Resampling.LANCZOS).save(dest / f"mobile-{lang}.png")


if __name__ == "__main__":
    main()
