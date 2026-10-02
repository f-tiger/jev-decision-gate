# Why install Jev Decision Gate?

Install it when you want an existing Issue-triage workflow inside your agent. A model API supplies a prediction; this project supplies the task contract, local batch entry, response validation, independent calibration, held-out evaluation and accept/review recommendations as six MCP tools, a Skill and a CLI.

The comparison below is against **bare model APIs**, not another finished product. Developers can build equivalent functionality on either API. If you already have that workflow, this package may add little value.

| Same task: Issue kind, module and information sufficiency | General LLM API | Direct Jev API | Jev Decision Gate MCP |
|---|---|---|---|
| Underlying prediction | Model response, optionally structured | Typed Jev judgment | Same Jev API, or an optional local rules baseline |
| Task contract and batch entry | Implement for your task | Implement for your task | Included; local Issue JSON, up to 200 records |
| Task fields, model and reported-usage checks | Implement for your task | Implement for your task | Included in the Jev adapter |
| Independent acceptance calibration and held-out evaluation | Implement or integrate | Implement or integrate | Included; inadequate evidence leaves decisions in review |
| Outbound-call controls | Configure in your application | Configure in your application | Jev off by default; startup opt-in and per-invocation call cap |
| Agent integration | Build/integrate tools | Build/integrate tools | Install the Skill or MCPB / stdio server |
| Extra token reduction attributable to this package | No matched live baseline run | No matched live baseline run | **Not measured** |

## Compare costs at the right layer

For the dated 2026-10-02 snapshot and **one hypothetical million input tokens**:

| Layer | LLM API: Fable 5.1 example | Direct Jev 1.13 | Our MCP using Jev 1.13 |
|---|---:|---:|---:|
| Underlying model input charge | $10 | $0.042 | $0.042 to Jev |
| Local package license fee | Depends on application | Depends on application | $0, MIT |
| Additional agent-host model tokens | Depends on application | Depends on application | May be incurred for tool definitions, arguments, results and reasoning; unmeasured |
| Actual total workflow bill | Unmeasured | Unmeasured | Unmeasured |

Jev's unit price is available through direct API calls too. The 238× Fable/Jev input-price ratio is **not an additional saving caused by our MCP**. Haiku 4.5 is a lower-cost reference at $1/M input; cache, output, retries, review and actual token counts can change the result. See [sources and assumptions](token-cost.md).

The package does not compress prompts, secretly route an agent's general chat traffic, or replace the host's reasoning model. A disabled calibrated policy can skip provider inference and recommend review; that trades automation for review and is not a matched-quality savings benchmark. `review` does not automatically call a fallback model.

## What you can verify immediately

The no-key rules demo runs the same local triage engine exposed by MCP. On 12 original synthetic examples, eight match all three expected fields and all 12 require review. It makes zero **backend/provider** model calls and reports zero backend/provider tokens. Using an LLM agent to invoke the tool can still incur agent-host token costs. These numbers are neither Jev accuracy nor a demonstration of infinite savings.

The README animation is an illustrated comparison and invocation example, backed by this runnable output and the MCP interoperability tests. It is not a recording of a live hosted product. Chinese captions are translations of English synthetic inputs.

```bash
npx skills add f-tiger/jev-decision-gate --skill jev-decision-gate
```

[MCP installation](mcp.md) · [Actual rules output](assets/demo-report.json) · [Evaluation method](evaluation.md) · [Verification status](verification.json)

## 中文说明

**安装理由：把 Jev 接入 Issue 分流所需的批量入口、字段与用量检查、独立校准、接受／复核建议和调用限制，变成现成的 MCP／Skill 工作流。** 面向裸 API 的比较不代表大模型或 Jev 无法实现这些功能；开发者可以自行编写同样流程。

直接 Jev 和我们的 MCP 使用相同的 Jev 模型单价。现阶段没有证据证明我们的 MCP 比直接 Jev 再减少了多少 token，也没有真实三方账单对比。Agent 宿主仍可能因为读取工具描述、参数和结果而产生费用。我们应宣传已交付的工作流价值，模型单价优势归于 Jev。
