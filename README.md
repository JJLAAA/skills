# My Skills

这个仓库保存可被 AI agent 调用的 skills。`SKILL.md` 是给 agent 读取的执行规则；本 `README.md` 是给人类看的索引和使用说明。

原则：

- 不把人类说明写进各个 skill 运行目录，避免干扰 agent 读取 `SKILL.md`。
- 仓库级图片和示意图统一放在 `assets/`。
- `SKILL.md` 保持机器可执行、约束明确；README 只做导航和解释。

## Agent Handoff Relay

`handoff` skill 用于让 source agent 和 target agent 通过文件持续接力，而不是让用户做人肉中间层。

![Handoff Agent Relay](assets/handoff-agent-relay-infographic.png)

HTML 源文件：`assets/handoff-agent-relay-infographic.html`

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
| `handoff` | `handoff/` | 生成 agent-to-agent 技术交接文件 | handoff、保存进度、交接、checkpoint |
| `java-code-review` | `java-code-review/` | Java 代码审查，优先发现高风险缺陷 | Java review、PR review、风险审计 |
| `linuxdo-news-analyzer` | `linuxdo-news-analyzer/` | 分析指定日期 linux.do 新闻 | linux.do 今日快讯、分析 linux.do YYYY-MM-DD |
| `openai-weekly-blog` | `openai-weekly-blog/` | 分析 OpenAI 本周 Research/Engineering 博客 | OpenAI blog this week、OpenAI 本周博客 |
| `pdf` | `pdf/` | PDF 提取、生成、合并、拆分、表单处理 | PDF 分析、填表、合并、拆分 |
| `reddit-analyzer` | `reddit-analyzer/` | 筛选 Reddit 高质量技术帖子 | 分析 Reddit、AgentsOfAI 帖子 |
| `skill-creator` | `skill-creator/` | 创建、修改、优化、评测 skills | 创建 skill、优化 skill、skill eval |
| `sync-docs-index` | `sync-docs-index/` | 同步文档目录索引和摘要，整理单篇文章 | 更新索引、同步文档摘要、整理文章 |
| `tap-adapter-author` | `tap-adapter-author/` | 为新站点或命令编写 TAP adapter | 写 TAP adapter、适配新网站 |
| `web-tech-article-analyzer` | `web-tech-article-analyzer/` | 用 7 层框架分析技术文章、URL、博客和帖子 | 分析技术文章、URL、博客、Reddit、X、WeChat |

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

### handoff

**用途：** 生成给下一个 AI agent 的技术交接文件，让 agent 之间通过文件接力。

**适合场景：**

- 保存进度、暂停、切换任务、上下文接近上限。
- 让 Claude Code 和 Codex 等不同 agent 异步协作。
- 将 review findings、实现状态、失败尝试、验证命令沉淀为可执行上下文。

**关键机制：**

- 先明确 `Target reader` 和 `Execution type`。
- handoff 文件自带 `How to read this handoff` 和 `Next Agent's First Action`。
- 继续接力时保留事实和决策，只更新 routing、progress、pending tasks 和 next action。

**示例：**

```text
请生成 handoff。
目标读者：Codex
执行类型：code review
重点 review 当前 diff 的 bug、回归风险和缺失测试。
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

## System Skills

`.system/` 下是系统级 skills，通常不作为日常自定义 skill 修改对象，但这里也列出用途，方便理解。

| Skill | 目录 | 用途 |
|---|---|---|
| `imagegen` | `.system/imagegen/` | 生成或编辑位图资产，如照片、插画、纹理、sprite、mockup |
| `openai-docs` | `.system/openai-docs/` | 查询 OpenAI 官方文档，做模型选择、API 迁移和 prompt 升级 |
| `plugin-creator` | `.system/plugin-creator/` | 创建 Codex plugin 目录、manifest 和 marketplace 条目 |
| `skill-creator` | `.system/skill-creator/` | 创建或更新 Codex skills 的系统指导 |
| `skill-installer` | `.system/skill-installer/` | 从 curated list 或 GitHub repo 安装 skills |

## Repository Layout

```text
.
├── README.md
├── assets/
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
