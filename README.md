# My Skills

这个仓库保存可被 AI agent 调用的 skills。`SKILL.md` 是给 agent 读取的执行规则；本 `README.md` 是给人类看的索引和使用说明。

原则：

- 不把人类说明写进各个 skill 运行目录，避免干扰 agent 读取 `SKILL.md`。
- 仓库级图片和示意图统一放在 `assets/`。
- `SKILL.md` 保持机器可执行、约束明确；README 只做导航和解释。

## Skill Index

| Skill | 目录 | 主要用途 | 常见触发 |
|---|---|---|---|
| `agent-cli-design` | `agent-cli-design/` | 设计、审计、实现 agent 友好的 CLI | CLI 设计、Click/Cobra/Clap/argparse、MCP vs CLI |
| `aihot` | `aihot/` | 查询和整理 AI HOT 中文 AI 资讯 | AI 日报、AI HOT、今天 AI 圈有什么 |
| `anthropic-weekly-blog` | `anthropic-weekly-blog/` | 分析本周 Anthropic Engineering 博客 | Anthropic weekly blog、本周 Anthropic 工程博客 |
| `claude-weekly-blog` | `claude-weekly-blog/` | 分析本周 Claude 博客文章 | Claude blog this week、Claude 本周博客 |
| `deep-research` | `deep-research/` | 多轮搜索、反思、证据交叉验证的深度研究 | research、调查、综合分析、带引用报告 |
| `diagram-viz` | `diagram/` | 生成 draw.io 图表或 HTML 信息图 | 画图、流程图、架构图、信息图、可视化 |
| `github-repo-analyzer` | `github-repo-analyzer/` | 分析 GitHub 仓库功能、技术栈和架构 | 给出 GitHub repo URL 并要求分析 |
| `goal-ready-coach` | `goal-ready-coach/` | 把模糊任务收敛为可自主执行的 Goal Contract | Goal Ready、转成 Goal、创建 Goal 前先澄清、小步快跑、把需求问清楚 |
| `handoff` | `handoff/` | 保存或加载 agent-to-agent 技术交接文件 | 保存进度、恢复进度、继续上次、load handoff、checkpoint |
| `java-code-review` | `java-code-review/` | Java 代码审查，优先发现高风险缺陷 | Java review、PR review、风险审计 |
| `linuxdo-news-analyzer` | `linuxdo-news-analyzer/` | 分析指定日期 linux.do 新闻 | linux.do 今日快讯、分析 linux.do YYYY-MM-DD |
| `openai-weekly-blog` | `openai-weekly-blog/` | 分析 OpenAI 本周 Research/Engineering 博客 | OpenAI blog this week、OpenAI 本周博客 |
| `pdf` | `pdf/` | PDF 提取、生成、合并、拆分、表单处理 | PDF 分析、填表、合并、拆分 |
| `reddit-analyzer` | `reddit-analyzer/` | 筛选 Reddit 高质量技术帖子 | 分析 Reddit、AgentsOfAI 帖子 |
| `skill-creator` | `skill-creator/` | 创建、修改、优化、评测 skills | 创建 skill、优化 skill、skill eval |
| `sync-docs-index` | `sync-docs-index/` | 同步文档目录索引和摘要，整理单篇文章 | 更新索引、同步文档摘要、整理文章 |
| `tap-adapter-author` | `tap-adapter-author/` | 为新站点或命令编写 TAP adapter | 写 TAP adapter、适配新网站 |
| `web-tech-article-analyzer` | `web-tech-article-analyzer/` | 用 7 层框架分析技术文章、URL、博客和帖子 | 分析技术文章、URL、博客、Reddit、X、WeChat |
| `wiki-index-audit` | `wiki-index-audit/` | 审计 Markdown Wiki 关键认知召回层，检查腐化和召回质量 | 审计关键认知索引、检查 Wiki 腐化、知识库定期健检 |

## Skills

### agent-cli-design

**用途：** 设计和构建 agent 友好的 CLI，覆盖审计、设计和实现三种模式。

**适合场景：**

- 评估现有 CLI 是否适合 AI agent 使用。
- 设计命令树、结构化输出、退出码、dry-run、幂等行为和错误信息。
- 为 Click、Cobra、Clap、argparse 等 CLI 框架做改造建议。

**示例：**

```text
帮我审计这个 CLI 是否适合 agent 使用。
设计一个支持 json 输出和 dry-run 的命令结构。
```

### aihot

**用途：** 从 AI HOT 获取中文 AI 资讯、日报、精选条目和行业动态。

**适合场景：**

- 查询今天或最近的 AI 新闻。
- 了解大模型、产品、论文、行业动态。
- 生成中文 AI 简报。

**示例：**

```text
今天 AI 圈有什么？
看一下 AI HOT 精选。
最近 OpenAI/Anthropic/Google 发布了什么？
```

### anthropic-weekly-blog

**用途：** 获取并分析本周 Anthropic Engineering 博客，生成中文技术报告。

**适合场景：**

- 汇总 Anthropic 本周工程文章。
- 分析每篇文章的技术价值和实现细节。

**示例：**

```text
分析本周 Anthropic 工程博客。
Anthropic weekly blog 有什么新文章？
```

### claude-weekly-blog

**用途：** 分析当前周 Claude 官网博客文章，并按北京时间过滤。

**适合场景：**

- 查看 Claude 本周发布内容。
- 生成 20-30 字中文摘要和原文链接。

**示例：**

```text
Claude 本周博客有哪些？
latest Claude posts
```

### deep-research

**用途：** 执行多轮研究：拆解问题、搜索、评估证据、发现缺口、处理矛盾并生成带引用报告。

**适合场景：**

- 需要多来源交叉验证的研究。
- 需要覆盖时效性、矛盾、深度、视角的综合分析。

**示例：**

```text
对这个主题做 deep research，给出证据和引用。
调查这个技术方向的主要方案、争议和最新进展。
```

### diagram-viz

**用途：** 绘制图表和信息可视化。支持 draw.io 图表和 HTML 信息图。

**适合场景：**

- 流程图、架构图、时序图、ER 图、网络拓扑。
- 分层分色、信息密度高的 HTML 信息图。

**示例：**

```text
画一张这个系统的架构图。
把这个流程做成横向排版的信息图。
```

**注意：** 该 skill 在执行前会先询问使用 `draw.io` 还是 `HTML 信息图` 风格。

### github-repo-analyzer

**用途：** 分析 GitHub 仓库的功能、技术栈、架构和亮点。

**适合场景：**

- 用户提供 GitHub 仓库 URL 并要求理解项目。
- 需要从 README、仓库元数据、官方文档综合生成中文报告。

**示例：**

```text
分析这个 GitHub 仓库：https://github.com/example/project
总结这个 repo 的技术栈和核心功能。
```

### goal-ready-coach

**用途：** 把尚不明确、需要小步推进的任务收敛为一个可交给 Agent 自主执行并客观验收的 Goal Contract，并在使用者显式确认后才创建 Goal。

它维护一份 Readiness Ledger，从已有对话和安全、只读的调查中提取信息，不为 Agent 能自行查证的事实打扰用户。每轮只推进一个影响最大的阻塞项，按 `结果 → 验收 → 范围 → 决策权 → 上下文 → 停止条件` 的优先级排序。六项门槛全部 `READY` 才进入 `GOAL READY`，再输出自包含的 Goal Contract，并通过两阶段提交门禁等待使用者明确确认后才调用 `create_goal`。

![双队列 AI 任务工作流](assets/dual-queue-goal-workflow.svg)

上图说明：探索队列在 `goal-ready-coach` 驱动下逐项消除不确定性，通过 Readiness Gate 后转入 Goal 交付队列；两个队列的并行度都由人的容量（判定容量、验收容量）决定。SVG 源文件：`assets/dual-queue-goal-workflow.svg`

**适合场景：**

- 需求还没想清楚、想把任务问清楚再开始。
- 模糊输入（如"优化一下""做得更好"）需要收敛为可验收目标。
- 创建 Goal 前需要先把剩余不确定性压到 Agent 授权范围内。

**示例：**

```text
把这个需求转成 Goal。
任务还没想清楚，帮我用小步快跑问清楚。
优化一下后台查询性能，帮我变成 Goal。
```

**注意：** 澄清期间只做只读调查和无副作用验证，不会提前实现 Goal；只有使用者明确表达"确认创建 Goal"等无歧义意图后才会调用 `create_goal`。

### handoff

**用途：** 保存或加载给 AI agent 使用的技术交接文件，让 agent 之间通过文件接力。

`handoff` skill 用于让 source agent 和 target agent 通过文件持续接力，而不是让用户做人肉中间层。它现在有两个模式：Save Mode 用于创建或更新 handoff，Load Mode 用于读取已有 handoff 并继续执行。

![Handoff Agent Relay](assets/handoff-agent-relay-infographic.png)

HTML 源文件：`assets/handoff-agent-relay-infographic.html`

**适合场景：**

- 保存进度、暂停、切换任务、上下文接近上限。
- 读取已有 handoff、恢复进度、继续上次任务。
- 让 Claude Code 和 Codex 等不同 agent 异步协作。
- 将 review findings、实现状态、失败尝试、验证命令沉淀为可执行上下文。

**关键机制：**

- 先判断是 `Save Mode` 还是 `Load Mode`；只有用户意图模糊时才询问。
- Save Mode 会明确 `Source agent`、`Target reader` 和 `Execution type`。
- Load Mode 会先定位 handoff 文件，再读取 `## 0. Handoff Routing` 和 `Next Agent's First Action`。
- handoff 文件自带 `How to read this handoff` 和 `Next Agent's First Action`。
- 继续接力时保留事实和决策，只更新 routing、progress、pending tasks 和 next action。
- 多个 handoff 文件存在时，只有最近修改文件能安全匹配用户意图才自动选择，否则询问文件路径。

**示例：**

Save Mode:

```text
请生成 handoff。
目标读者：Codex
执行类型：code review
重点 review 当前 diff 的 bug、回归风险和缺失测试。
```

Load Mode:

```text
从 260531-handoff.md 继续。
```

### java-code-review

**用途：** 按风险优先的方式审查 Java 代码变更。

**适合场景：**

- Java PR review。
- 审计高风险重构。
- 检查回归、并发、事务、资源释放和测试缺口。

**示例：**

```text
请 review 这组 Java 改动，重点找生产风险。
审查这个 PR 的回归风险和缺失测试。
```

### linuxdo-news-analyzer

**用途：** 通过 linux.do Discourse JSON API 分析指定北京时间日期的社区新闻。

**适合场景：**

- 指定日期的 linux.do 新闻快讯。
- 逐篇读取详情并输出结构化概述。

**示例：**

```text
分析 linux.do 2026-05-30 的新闻。
linux.do 今日快讯 2026-05-30
```

**注意：** 必须显式传入北京时间日期，格式为 `YYYY-MM-DD`。

### openai-weekly-blog

**用途：** 分析 OpenAI 当前周 Research 和 Engineering 博客文章。

**适合场景：**

- 查看 OpenAI 本周技术文章。
- 按指定日期定位某一周。

**示例：**

```text
OpenAI 本周博客有哪些？
OpenAI weekly articles 20260314
```

### pdf

**用途：** PDF 文档处理工具集，包括提取文本和表格、创建 PDF、合并拆分、处理表单。

**适合场景：**

- 分析或生成 PDF。
- 填写 PDF 表单。
- 批量处理 PDF 文档。

**示例：**

```text
提取这个 PDF 的表格。
帮我填写这个 PDF 表单。
把这些 PDF 合并成一个文件。
```

### reddit-analyzer

**用途：** 分析 Reddit subreddit，筛选高质量技术帖子。

**适合场景：**

- 从 AgentsOfAI 等 subreddit 中筛选有价值内容。
- 按互动指标和内容质量排序 Top 10。

**示例：**

```text
分析 Reddit AgentsOfAI 的高质量帖子。
筛选这个 subreddit 里最值得看的技术讨论。
```

### skill-creator

**用途：** 创建、修改、优化和评测 skills。

**适合场景：**

- 从零创建一个新 skill。
- 优化已有 skill 的触发描述和工作流。
- 运行 eval 或 benchmark 检查 skill 表现。

**示例：**

```text
帮我创建一个用于分析技术播客的 skill。
优化这个 skill 的 description，让它更容易正确触发。
```

### sync-docs-index

**用途：** 同步文档目录索引和摘要，或整理单篇文章。

**适合场景：**

- 文档目录新增或更新后，同步 README 索引。
- 给文章加摘要、任务入口、概念索引和交叉引用。
- 将修订章节合并回正文。

**示例：**

```text
帮我同步一下文档摘要。
新增了文章，需要更新目录索引。
整理这篇文章，把修订整合进去。
```

### tap-adapter-author

**用途：** 从侦察、pipeline 设计、安装到验证，完整编写 TAP adapter。

**适合场景：**

- 为新网站或新命令写 TAP 适配器。
- 需要浏览器侦察、登录状态、网络结构分析。

**示例：**

```text
帮我给这个网站写一个 TAP adapter。
把这个页面的数据做成 tap <site> <command>。
```

### web-tech-article-analyzer

**用途：** 使用 7 层框架分析 Web 技术文章、URL、博客和帖子。

**适合场景：**

- 单篇技术文章深度分析。
- 批量 RSS、Reddit、X/Twitter、WeChat、arxiv、GitHub、技术博客分析。
- 中文输出，保留英文技术术语。

**示例：**

```text
分析这篇技术文章：https://example.com/article
用 7 层框架拆解这组文章。
```

### wiki-index-audit

**用途：** 审计 Markdown LLM Wiki 中 `关键认知索引.md` 这一召回层的质量，覆盖卡片结构、索引膨胀、语义重复、边界模糊、来源失效、跨页面矛盾和真实问题召回命中。

它与 `sync-docs-index` 分工：后者负责文档摘要、README 路由和交叉链接的日常同步；本 Skill 负责低频但更重的语义治理。默认运行 `full` 审计但只生成报告——未经用户确认，不合并、删除卡片，不创建专题页，也不改变知识结构。

**适合场景：**

- 定期（每月、卡片数量达阈值、体积增长超阈值）对关键认知索引做健检。
- 出现漏召回、误召回、来源失效或卡片间矛盾后立即排查。
- 大规模专题整理前后评估召回层质量。

**示例：**

```text
帮我审计一下关键认知索引。
检查一下 Wiki 是否有腐化。
卡片新增较多，跑一次 full 审计。
```

**注意：** 审计和 Automation 运行默认只报告；修复（`fix`）需要用户确认具体变更集，且修复后必须重新运行 full 审计、retrieval eval 和本地 Markdown 链接校验才能更新基线。

## Repository Layout

```text
.
├── README.md
├── assets/
│   ├── dual-queue-goal-workflow.svg
│   ├── handoff-agent-relay-infographic.html
│   └── handoff-agent-relay-infographic.png
├── handoff/
│   └── SKILL.md
├── diagram/
│   └── SKILL.md
└── ...
```

## Maintenance Notes

- 新增 skill 后，在 `Skill Index` 和 `Skills` 两处补充说明。
- 需要展示图示时，将图片或 HTML 源放在 `assets/`，再从 README 引用。
- 不要为了人类说明去改写 `SKILL.md`；`SKILL.md` 应保持 agent 可执行规则。
- 如果某个 skill 有复杂示意图，优先在 README 中嵌入截图，并把源文件放入 `assets/`。
