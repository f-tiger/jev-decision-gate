#!/usr/bin/env python3
"""Illustrated LLM API / Jev API / our MCP comparison, not a live model benchmark."""
import json
import os
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from jev_decision_gate.triage import triage
from price_scenario import calculate, SNAPSHOT

OUT = ROOT / "docs/assets"
W, H = 900, 760
BG, PANEL, BORDER = "#101923", "#1a2836", "#334554"
TEXT, MUTED, GREEN, AMBER, CYAN = "#f2f5f3", "#b7c6ce", "#d4ff77", "#ffcc7b", "#8bdded"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
CJK = os.environ.get("DEMO_CJK_FONT", "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")


def text(d, x, y, value, size=24, color=TEXT, zh=False, bold=False, mono=False, width=816):
    f = ImageFont.truetype(CJK if zh else MONO if mono else BOLD if bold else FONT, size)
    if d.textlength(value, font=f) > width:
        raise ValueError(f"Text exceeds available width: {value}")
    d.text((x, y), value, font=f, fill=color, anchor="lt")


def box(d, bounds, active=False):
    d.rounded_rectangle(bounds, radius=18, fill="#203124" if active else PANEL,
                        outline=GREEN if active else BORDER, width=3 if active else 2)


def frame(lang, scene, reveal, report, calc, prices):
    zh = lang == "zh-CN"
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    text(d, 42, 29, "JEV DECISION GATE", 23, GREEN, bold=True)
    text(d, 740, 29, "by BPJ", 23, MUTED)
    titles = ["为什么装我们的 MCP？", "模型单价，与工具价值分开看", "把重复开发，变成安装即用", "先免费试跑，再决定是否接入", "给你的 Agent 装上这套工作流"] if zh else [
        "A model API is only the starting point.", "Model pricing and our added value.",
        "Four pieces you do not have to build.", "Try the workflow before paying for calls.",
        "Give your agent the whole workflow."]
    captions = ["同一批 Issue · 三种接法 · 同一分类目标",
        "公开单价 · 100 万输入 token 情景 · " + prices["as_of"],
        "对比裸 API 接入 · 同样功能也可自行开发",
        "本地规则 · 12 个合成案例 · 可复现输出",
        "开源 MIT · MCP / Skill / CLI · Jev 默认关闭"] if zh else [
        "ONE ISSUE BATCH / THREE WAYS TO CONNECT",
        "LIST PRICES / 1M INPUT-TOKEN SCENARIO / " + prices["as_of"],
        "BARE APIs / EQUIVALENT WORKFLOWS CAN BE CUSTOM-BUILT",
        "LOCAL RULES / 12 SYNTHETIC CASES / REPRODUCIBLE OUTPUT",
        "OPEN SOURCE / MCP + SKILL + CLI / JEV OFF BY DEFAULT"]
    text(d, 42, 71, captions[scene], 18 if scene == 1 and not zh else 20, MUTED, zh)
    text(d, 42, 115, titles[scene], 38 if zh else 34, TEXT, zh, bold=True)
    if scene < 3:
        names = ["大模型 API", "直接 Jev", "我们的 MCP"] if zh else ["LLM API", "DIRECT JEV", "OUR MCP"]
        subs = ["Fable 5.1", "TypeSafe Jev", "Jev Decision Gate"]
        for i in range(3):
            x = 42 + 278 * i
            box(d, (x, 182, x + 260, 589), i == 2)
            text(d, x + 18, 204, names[i], 27, GREEN if i == 2 else TEXT, zh, bold=True, width=224)
            text(d, x + 18, 244, subs[i], 19, MUTED, width=224)
        if scene == 0:
            heads = ["模型接口", "判断接口", "现成工作流"] if zh else ["MODEL API", "DECISION API", "WORKFLOW"]
            columns = [["生成文本或 JSON", "自写任务逻辑", "自写检查与评估"],
                       ["输出结构化判断", "自写任务逻辑", "自写检查与评估"],
                       ["6 个现成 MCP 工具", "接入、校验、校准", "不确定的留给复核"]] if zh else [
                       ["Text or JSON", "Build task logic", "Build checks + evals"],
                       ["Typed judgments", "Build task logic", "Build checks + evals"],
                       ["6 MCP tools", "Connect + validate", "Calibrate + review"]]
            for i in range(3):
                text(d, 60 + 278 * i, 303, heads[i], 25, GREEN if i == 2 else CYAN, zh, bold=True, width=224)
                for j, value in enumerate(columns[i]):
                    if reveal >= j:
                        text(d, 60 + 278 * i, 370 + 58 * j, value, 23 if zh else 20,
                             GREEN if i == 2 else TEXT, zh, width=224)
            text(d, 42, 618, "Jev 提供判断；我们的 MCP 提供可直接接入的流程。" if zh else "Jev supplies judgments. Our MCP supplies the workflow.", 26 if zh else 25, TEXT, zh)
            text(d, 42, 658, "类型、模块、信息是否充分 → 接受或复核" if zh else "Kind, module, information → accept or review", 23, MUTED, zh)
        elif scene == 1:
            values = [calc["baseline_input_usd"], calc["jev_input_usd"], calc["jev_input_usd"]]
            for i, value in enumerate(values):
                x = 60 + 278 * i
                charge = "$" + (f"{value:.0f}" if i == 0 else f"{value:.3f}")
                text(d, x, 298, charge, 59 if i == 0 else 47, GREEN if i == 2 else CYAN, bold=True, width=224)
                detail = (["1M 假设输入 token", "模型输入费用"] if i < 2 else ["1M 输入交给 Jev", "+ 宿主模型费用"]) if zh else (
                         ["1M assumed input", "Model input charge"] if i < 2 else ["1M input to Jev", "+ host model cost"])
                for j, line in enumerate(detail):
                    text(d, x, 389 + 34 * j, line, 22 if zh else 20, TEXT, zh, width=224)
                labels = ["仅作为价格参照", "直接调用即享此价", "MCP 本地工具免费"] if zh else ["Price reference only", "Jev's own pricing", "Local MCP is free"]
                if reveal >= 2:
                    text(d, x, 516, labels[i], 21 if zh else 20, GREEN if i == 2 else AMBER, zh, width=224)
            text(d, 42, 611, "相同 Jev 单价，附带完整的 Issue 分流流程。" if zh else "Same Jev price. Ready-made Issue-triage workflow.", 25, GREEN, zh)
            text(d, 42, 649, "相同 Jev 单价；宿主上下文、输出、重试等另计。" if zh else "Same Jev price. Host context, output and retries add cost.", 22, MUTED, zh)
            text(d, 42, 679, "低价 LLM 参照：Haiku 4.5 输入 $1/M；详见价格来源。" if zh else "Lower-cost LLM reference: Haiku 4.5 input $1/M. Sources in README.", 18, MUTED, zh)
        else:
            generic = ["自写批量入口", "自写任务检查", "自写接受 / 复核", "自行设置调用限制"] if zh else ["Build batch entry", "Build task checks", "Build accept/review", "Configure call cap"]
            ours = ["批量 Issue JSON", "任务字段、用量检查", "独立校准 + 复核", "每次调用数量上限"] if zh else ["Batch Issue JSON", "Fields + usage checks", "Calibration + review", "Per-invocation cap"]
            for i in range(3):
                for j, value in enumerate(ours if i == 2 else generic):
                    if reveal >= j:
                        text(d, 60 + 278 * i, 299 + 68 * j, value, 23 if zh else 19,
                             GREEN if i == 2 else MUTED, zh, width=224)
            text(d, 42, 618, "省去重复接入与检查代码，直接开始处理 Issue。" if zh else "Skip repeat integration work. Start triaging Issues.", 25, TEXT, zh)
            text(d, 42, 657, "review 不会自动调用另一个模型，也不会修改 Issue。" if zh else "Review does not call another model or modify Issues.", 23, MUTED, zh)
    elif scene == 3:
        box(d, (42, 183, 858, 337))
        text(d, 64, 204, "示例 MCP 调用 · 实际本地规则输出" if zh else "EXAMPLE MCP REQUEST / ACTUAL LOCAL RULES OUTPUT", 22, MUTED, zh)
        text(d, 64, 247, 'triage_issues(issues_file="issues.json",', 26, GREEN, mono=True)
        text(d, 64, 289, '              provider="rules")', 26, GREEN, mono=True)
        values = [str(report["summary"]["issues"]), f"{sum(r['correct'] for r in report['rows'])}/{report['summary']['issues']}", str(report["summary"]["review"])]
        labels = ["合成案例", "三项全对", "需要人工复核"] if zh else ["SYNTHETIC CASES", "JOINTLY CORRECT", "REQUIRE REVIEW"]
        for i, (value, label) in enumerate(zip(values, labels)):
            x = 42 + 278 * i
            box(d, (x, 364, x + 260, 497), i == 2)
            text(d, x + 19, 389, value, 48, GREEN, bold=True, width=222)
            text(d, x + 19, 458, label, 23 if zh else 19, TEXT, zh, width=222)
        text(d, 42, 534, "后端模型调用 0 次 · 后端 token 0 · 无需密钥" if zh else "0 provider calls / 0 provider tokens / no API key", 28, GREEN, zh)
        text(d, 42, 584, "分类结果与复核建议，一份报告直接查看。" if zh else "See classifications and review decisions in one report.", 25, TEXT, zh)
        text(d, 42, 632, "先看失败案例，再用自己的标注数据做校准。" if zh else "Inspect the misses. Calibrate on your own labeled cases.", 25, TEXT, zh)
        text(d, 42, 673, "Agent 宿主读取工具说明、参数和结果的 token 仍可能计费。" if zh else "Agent-host tokens for tool descriptions, arguments and results may still be billed.", 19 if zh else 18, MUTED, zh)
    else:
        box(d, (42, 190, 858, 365), True)
        text(d, 64, 214, "安装到支持的 Agent" if zh else "INSTALL IN A COMPATIBLE AGENT", 23, MUTED, zh)
        text(d, 64, 264, "npx skills add f-tiger/jev-decision-gate " + chr(92), 27, GREEN, mono=True, width=772)
        text(d, 64, 309, "  --skill jev-decision-gate", 27, GREEN, mono=True, width=772)
        text(d, 42, 405, "或下载 MCPB，接入支持的 MCP 宿主" if zh else "Or download the MCPB for a compatible host", 30, TEXT, zh)
        text(d, 42, 456, "选择 Issue JSON → 先跑规则 → 检查复核结果" if zh else "Choose Issue JSON → run rules → inspect the review queue", 25 if zh else 24, CYAN, zh)
        text(d, 42, 524, "直接获得一套可运行的 Issue 分流流程。" if zh else "Get a working Issue-triage process for your agent.", 30 if zh else 29, GREEN, zh)
        text(d, 42, 585, "Jev 默认关闭；启用后由 TypeSafe 收取模型费用。" if zh else "Jev is off by default. TypeSafe bills enabled model calls.", 24, MUTED, zh)
        text(d, 42, 636, "github.com/f-tiger/jev-decision-gate", 29, TEXT, mono=True)
    d.line((42, 710, 858, 710), fill=BORDER, width=2)
    labels = ["三种接法", "费用", "工具增量", "试跑", "安装"] if zh else ["COMPARE", "COST", "WHY MCP", "TRY IT", "INSTALL"]
    for i, label in enumerate(labels):
        x = 42 + 166 * i
        if i == scene:
            d.rounded_rectangle((x, 708, x + 146, 713), radius=2, fill=GREEN)
        text(d, x, 729, f"{i + 1:02} {label}", 18, GREEN if i == scene else MUTED, zh)
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    issues = json.loads((ROOT / "examples/issues.synthetic.json").read_text())
    report = triage(issues, provider="rules")
    for row, issue in zip(report["rows"], issues):
        row.pop("latency_ms", None)
        row["title"], row["body"] = issue["title"], issue["body"]
    report["provenance"] = "Actual offline rules output on original synthetic fixtures; English inputs; Chinese captions are translations. Not live Jev output or a product UI recording."
    report["fixture"] = "examples/issues.synthetic.json"
    (OUT / "demo-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    prices = json.loads(SNAPSHOT.read_text())
    calc = calculate(prices)
    (OUT / "price-scenario.json").write_text(json.dumps(calc, indent=2) + "\n")
    for lang in ("en", "zh-CN"):
        frames, durations, settled = [], [], []
        for scene in range(5):
            for reveal in range(5):
                im = frame(lang, scene, reveal, report, calc, prices)
                frames.append(im.quantize(colors=96, method=Image.Quantize.MEDIANCUT))
                durations.append(500 if reveal < 4 else 5000)
            settled.append(im)
        path = OUT / f"token-cost-{lang}.gif"
        frames[0].save(path, save_all=True, append_images=frames[1:], duration=durations, loop=0, optimize=True, disposal=1)
        settled[0].save(OUT / f"token-cost-{lang}-poster.png", optimize=True)
        print(f"{path.relative_to(ROOT)}: {path.stat().st_size:,} bytes")
        if qa := os.environ.get("DEMO_QA_DIR"):
            dest = Path(qa)
            dest.mkdir(parents=True, exist_ok=True)
            sheet = Image.new("RGB", (W * 2, H * 3), BG)
            for i, still in enumerate(settled):
                sheet.paste(still, ((i % 2) * W, (i // 2) * H))
                still.save(dest / f"{lang}-scene-{i}.png")
            sheet.save(dest / f"contact-{lang}.png")
            settled[0].resize((390, 329), Image.Resampling.LANCZOS).save(dest / f"mobile-{lang}.png")


if __name__ == "__main__":
    main()
