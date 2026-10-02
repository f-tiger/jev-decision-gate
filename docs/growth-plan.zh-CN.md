# Jev Decision Gate 传播方案：先让开发者跑起来

研究日期：2026-10-02。结论：**用费用差吸引点击，用可复现任务转化，用现有 Agent 的安装入口留住用户。** GitHub 是试用入口，BPJ 是后续服务入口。当前不要把访问者先导到需要注册的网站。

这份方案根据公开页面、仓库实现入口和实时 GitHub 元数据判断可借鉴做法。没有这些项目的后台流量、获客归因或营收数据，不能证明某种页面设计导致其增长，也不能用累计 Stars 推导增长速度。

## 关联项目和站点到底在怎么传播

下表 Stars / Forks 是 2026-10-02 GitHub API 快照，按 Stars 排序。站点目录内嵌的计数可能滞后；统计的是各项目本身，不能把它们收录的大仓库 Stars 当成目录的 Stars。

| 项目 / 站点 | Stars / Forks | 可观察到的传播与转化设计 | 我们借鉴什么 |
|---|---:|---|---|
| [browser-use/jev-ultrafast](https://github.com/browser-use/jev-ultrafast) | 21,708 / 1,533 | README 用机票查询的具体结果作入口，并给出录像、测量记录、运行命令，另接云服务候补名单 | 首屏展示一个任务及证据。其速度是作者报告，不能移植成我们的成绩；其品牌基础也不是新仓库天然拥有的 |
| [tamaratran/fast-jev-compaction](https://github.com/tamaratran/fast-jev-compaction) | 7,309 / 480 | 聚焦 Claude Code 上下文压缩；npm 与插件两种入口；安装后接入已有流程 | “装上就进入工作流”比算法介绍更直接。它减少上下文内容，与我们当前 Issue 分类的范围不同 |
| [typesafe-ai/skills](https://github.com/typesafe-ai/skills) | 2,523 / 151 | 官方技能与开发文档相连 | 把 Skill 安装作为主入口之一；官方信誉无法靠命名复制 |
| [yibie/awesome-jev](https://github.com/yibie/awesome-jev) | 2,064 / 310 | 分类清单、贡献规则，要求具体实现、可运行证据和 AI 辅助披露 | 优先申请精准收录；一项目一类别，不批量堆条目 |
| [heyjunpenn/awesome-jev](https://github.com/heyjunpenn/awesome-jev) / [jevbest.com](https://jevbest.com/) | 916 / 72 | 搜索、类别、语言、新增项目视图；站点提交入口导向 GitHub 审核 | 准备一段场景描述、源码定位、演示与验证链接，降低审核成本 |
| [logicrw/awesome-jev-projects](https://github.com/logicrw/awesome-jev-projects) / [站点](https://logicrw.github.io/awesome-jev-projects/) | 638 / 56 | 中英文项目解释、“Jev 在这里做什么”、场景分类与 GitHub/Clone 入口 | 每条介绍都讲具体判断；申请 MCP/分类决策对应的单一类别 |
| [kydlikebtc/awesome-jev](https://github.com/kydlikebtc/awesome-jev) | 588 / 17 | 按决策模式索引，附源码证据、日期、兼容性和机器可读数据 | 把模型、版本、输入输出与证据写清，方便人工及自动索引核查 |
| [itsmostafa/system-one-connector](https://github.com/itsmostafa/system-one-connector) | 340 / 39 | 通用多模型 MCP；原 typesafe-mcp 已更名 | 通用连接器已有供给，我们应突出具体可复现的判断任务 |
| [hellogumbo/awesome-jev](https://github.com/hellogumbo/awesome-jev) / [awesomejev.com](https://awesomejev.com/) | 213 / 68 | 可筛选目录、规格、代码样例、提交入口；站点说明来自同一条目数据 | 仓库与站点复用事实，降低信息不一致；先被收录，不再造一个大目录 |

另一种路径是 [jevmodel.org](https://jevmodel.org/jev-github/)：围绕 GitHub、定价、模型对比等搜索意图建页面，通过内链接浏览器试用和付费额度。可借鉴“一个搜索问题 → 一页明确答案 → 试用”，但没有该站营收或流量证据，也不能把它当官方 TypeSafe 服务。搜索起量有时间成本，优先级低于现成开发者分发渠道。

**特别相关的反证：** fast-jev-compaction 明确说明其 token 大小是估算，且多次请求会重复发送状态。因此，即使借鉴热门项目，也要审查“节省”的分母和额外成本。目录数量和累计 Stars 都不等于真实使用。

## 我们的传播主题

主标题：**“每百万输入 token，$10 → $0.042。把简单判断交给 Jev，实际能省多少？”**

第一层用“大模型 API／直接 Jev／我们的 MCP”三栏讲清安装理由：现成的批量入口、检查、校准与复核流程；第二层展示模型单价与工具成本；第三层邀请用户运行自己的案例。Jev 的单价优势同样适用于直接调用，不能归为 MCP 额外节省。保留便宜模型对照和费用测算；三方真实用量及 MCP 额外 token 节省仍待实测。详见 [为什么安装](why-use-mcp.md) 和 [费用口径](token-cost.md)。

当前可以宣传：安装方式、六个 MCP 工具、离线案例、校准/评估机制、公开单价测算。当前不能宣传：实测省 238 倍 token、客户准确率、无人值守自动改 Issue、付费产品已上线。Skill 安装本身也不会自动降低宿主所有请求的 token 用量。

如果反馈显示开发者只关心长日志和上下文费用，下一轮应验证“构建/测试日志压缩后，诊断正确率是否保留”的新案例。先测需求和信息损失，再实现；当前仓库没有上下文压缩能力，不能把其他项目的功能写进宣传。

## 先后次序与本轮状态

| 优先级 | 具体动作 | 为什么 | 当前状态 |
|---|---|---|---|
| P0 | README 首屏中英文三方对比动画；静态图、出处、复现计算和离线试用 | 点击后立即理解安装理由，再检查费用与证据 | 本轮仓库交付 |
| P0 | 一条 Skills 安装命令、MCP 文档、简短反馈表 | 缩短进入现有开发流程的距离 | `--list` 已发现 Skill；不是所有宿主均完成安装测试 |
| P1 | yibie、jevbest、logicrw、awesomejev 四处按规则分别申请收录 | 直接接触正在寻找 Jev 项目的人 | 材料已准备，尚未向第三方提交 |
| P1 | 作者 X 与 TypeSafe 社区允许的展示区：三方对比动画 + 可运行链接 | 技术讨论可围绕证据展开，便于回应问题 | 中英文文案已准备，未发布；先查看社区当时规则 |
| P1 | Skills 生态真实安装与试用反馈 | 安装比点赞更接近价值验证 | 尚不宣称上榜；官方说明排行来自 CLI 安装遥测 |
| P2 | Show HN：可运行工具、实现动机、失败案例，作者现场回答 | 适合开发者反馈，门槛是实质性工作与可试用 | 标题和介绍已准备，未投稿；有修复和实测证据后更有说服力 |
| P2 | 官方 MCP Registry | 长期工具发现入口 | 目前只有本地 stdio；需先解决可分发包和所有权认证，不假称已收录 |
| P3 | BPJ 独立介绍页，围绕成本、安装和使用场景做搜索内容 | 承接长期搜索与具体服务意向 | 本轮未改网站，未改 agi-site |

不要同时到十个社区复制同一句广告。先选择两个最匹配的入口，回应安装问题并更新证据，再扩大。仓库 About、topics、社交预览建议见 [发布素材](launch-kit.md)，这些设置未在本轮自动修改。

## 7 天验证节奏

这是建议执行节奏，不是已创建的定时任务，也不是流量预测。

1. 第 0 天：首屏动画、试用、反馈表可用，记录 GitHub 初始基线和已知内部测试访问。
2. 第 1–2 天：由作者选定并提交精准目录材料；在一个熟悉且允许展示的开发者社区发布，及时回答安装问题。
3. 第 3–4 天：先修复前三个阻碍，再发布一个真实用户允许公开的使用记录；没有记录就公布失败复现，不伪造客户案例。
4. 第 5–7 天：评估成本标题是否带来正确受众；有代表性实测后发布质量—成本—回退完整对比，再考虑第二波传播。

**内部实验门槛（自定，不是行业标准）：** 先争取 200 个有效仓库访问、10 个外部开发者明确跑通、3 人在另一日再次使用。没有足够访问时，优先判断渠道覆盖；达到约 200 个访问却少于 5 个确认跑通，优先修复定位和安装；已有 10 人跑通却无人返回，优先检查持续使用价值，暂停扩大曝光。GitHub 无法精确区分所有“有效访问”，应同时查看来源并排除已知内部测试。

## 度量与营收连接

- GitHub Traffic：访问、独立访客、克隆、来源；[官方可见窗口为过去 14 天](https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository)。克隆不等于安装，机器人与内部检查会影响数据。
- 试用反馈：自愿填写安装结果、宿主、发现渠道及是否再次使用。成功使用人数以可核实反馈计，不从 Star 数推算。
- Skills：官方说明用安装遥测帮助排行；不刷安装。用户可关闭遥测，因此排行不是完整使用统计。
- BPJ：现有 UTM 链接可区分仓库来源的网站访问；不能用网站访问替代工具运行数据。不往 README 插像素追踪开发者。
- 商业信号：至少出现三个团队重复使用并明确提出周期评估、策略历史或团队管理需求，再验证收费。没有询价、付款或留存数据时，不写营收预测。

## 两轮对抗检查

**第一轮，证据和传播可信度：** 238× 是价格而非 token 数；不同模型、缓存和回退改变结论；作者测量与我们的实测分开；目录和社区收录尚未发生；大仓库累计 Stars 不证明其增长由 Jev 引起。

**第二轮，用户转化与产品价值：** 动画不能补足真实效果证据；当前全部复核，未证明节省人工时间；模块标签较窄，若真实仓库不匹配会流失。优先收集真实任务与安装反馈，下一波传播必须增加这些证据。快速曝光是渠道目标，持续使用取决于产品是否解决重复问题。

## 来源与检索范围

仓库 API：`https://api.github.com/repos/{owner}/{repo}`，上表逐个核对；页面与元数据抓取可能不同步，计数以后会变化。

主要页面：[Jev Ultrafast](https://github.com/browser-use/jev-ultrafast)、[fast-jev-compaction](https://github.com/tamaratran/fast-jev-compaction)、[yibie 收录规则](https://github.com/yibie/awesome-jev/blob/main/CONTRIBUTING.md)、[jevbest](https://jevbest.com/)、[Awesome Jev Radar](https://logicrw.github.io/awesome-jev-projects/)、[awesomejev.com](https://awesomejev.com/)、[jevmodel.org 的搜索页](https://jevmodel.org/jev-github/)。

分发规则：[Skills FAQ](https://skills.sh/docs/faq)、[Skills CLI](https://github.com/vercel-labs/skills)、[Show HN](https://news.ycombinator.com/showhn.html)、[MCP Registry 发布](https://modelcontextprotocol.io/registry/quickstart)、[PyPI 包验证](https://modelcontextprotocol.io/registry/package-types)。

仓库内容可被搜索和引用，但 GitHub 的 sitemap/域名验证由 GitHub 控制，本项目不能为 github.com 自行提交 IndexNow。未来 BPJ 页面若上线，再沿用其 SEO/GEO/IndexNow 流程；没有建立新网站或提交索引的声明。
