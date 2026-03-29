---
name: web-tech-article-analyzer
description: This skill should be used when the user provides a URL or technical article content that needs deep analysis using a 7-layer analytical framework. It applies the systematic methodology covering Problem Space, Architecture Design, Implementation, Quality Assurance, Production Engineering, Experience Distillation, and Cross-domain Connections. Intelligently routes between single article mode (console output) and RSS/batch mode (file output). Outputs are in Chinese with English technical terms preserved, featuring structured analysis with metrics, architectural insights, and actionable knowledge extraction.
---

# Web Tech Article Analyzer

## Overview

This skill specializes in efficiently deconstructing web-based technical content and performing deep analysis of articles using a **7-layer analytical framework**. It intelligently routes to different processing modes based on input type:

- **Single Article Mode**: Fetch, analyze, and output detailed analysis directly to the console (no file creation)
- **RSS/Batch Mode**: Parse RSS feeds, analyze multiple articles in parallel, and save each analysis to a local markdown file with a generated README index

All outputs are strictly neutral, data-driven, and structured, with Reddit content integrating community wisdom from comments.

## 7-Layer Analysis Framework

This skill applies a systematic methodology for deconstructing technical articles:

### Layer 1: Problem Space Analysis
- Identify core problem and boundary definition
- Analyze limitations of existing solutions
- Determine problem characteristics (deterministic vs open-ended, static vs dynamic)
- Understand target users and use cases

### Layer 2: Architecture Design
- **Pattern Recognition**: Identify architectural patterns (orchestrator-worker, pipeline, event-driven, etc.)
- **Component Topology**: Map hierarchical relationships, dependency graphs, data flow
- **Key Abstractions**: Extract core concept models and interface designs
- **Trade-off Decisions**: Performance vs complexity, flexibility vs control

### Layer 3: Implementation Techniques
- **Algorithms & Data Structures**: Understand core algorithm choices and rationale
- **Prompt Engineering** (for AI systems):
  - Behavior shaping strategies
  - Context management techniques
  - Error pattern prevention
- **Tool Design Principles**:
  - Granularity choices (coarse vs fine-grained)
  - Composability design
  - Error handling strategies

### Layer 4: Quality Assurance
- **Evaluation Strategy**:
  - Process evaluation vs outcome evaluation
  - Quantitative metrics + qualitative analysis
  - Small-sample rapid validation → large-scale regression testing
- **Observability**:
  - Key metrics definition
  - Tracing granularity choices
  - Privacy protection measures

### Layer 5: Production Engineering
- **Reliability Guarantees**:
  - State management strategies
  - Failure recovery mechanisms
  - Graceful degradation approaches
- **Deployment Strategy**:
  - Gradual rollout, canary deployment
  - Version compatibility handling
  - Rollback mechanisms
- **Performance Optimization**:
  - Bottleneck identification
  - Concurrency and async processing
  - Resource utilization

### Layer 6: Experience Distillation
- **Anti-pattern Library**: Common mistakes and avoidance methods
- **Best Practices**: Reusable design patterns
- **Evolution Path**: Iteration process from prototype to production
- **Future Directions**: Known limitations and improvement opportunities

### Layer 7: Cross-domain Connections
- Comparison with related technologies
- Transferable core ideas
- Applicable boundaries and non-applicable scenarios

This framework ensures comprehensive analysis that extracts actionable knowledge beyond surface-level understanding.

## When to Use This Skill

Use this skill when:
- User provides a URL from technical sites (reddit.com, arxiv.org, github.com, technical blogs, etc.)
- User provides technical article content that needs summarization or analysis
- User wants to extract key insights, metrics, or architectural details from web content
- User needs community feedback analysis from Reddit technical discussions
- User provides a blog homepage URL - automatically performs batch analysis and saves to files

## Processing Workflow

### STEP 0: URL Type Detection & Routing

**Before any analysis, determine the input type and route to appropriate mode:**

1. **RSS Feed Direct Link Detection**
   - Check URL patterns: `/rss`, `/feed`, `.xml`, `atom.xml`, `feed.xml`
   - Examples:
     - `https://example.com/rss` → **RSS Mode**
     - `https://blog.example.com/feed.xml` → **RSS Mode**
     - `https://example.com/atom.xml` → **RSS Mode**

2. **Blog Homepage Detection**
   - Check if URL points to homepage: `https://example.com/`, `https://blog.example.com/`
   - Use bundled script to detect RSS feed:
     ```bash
     scripts/rss_parser.py detect <html_content> <base_url>
     ```
   - Confidence threshold: ≥0.4 (40%) → **RSS Mode**
   - If no RSS feed detected → **Single Article Mode**

3. **Single Article Detection**
   - URL contains path parameters, slug, or article patterns
   - Examples:
     - `https://blog.example.com/post/my-article` → **Single Article Mode**
     - `https://example.com/articles/2024/01/my-post` → **Single Article Mode**
     - `https://baoyu.io/blog/state-of-ai-in-2026` → **Single Article Mode**

**Routing Decision:**
- **RSS Mode** → Proceed to STEP 4 (Batch Analysis)
- **Single Article Mode** → Proceed to STEP 1 (Single Article Analysis)

---

## MODE A: Single Article Analysis

*Use this mode for individual blog posts, Reddit threads, or direct article URLs. Output is displayed directly in the console without creating files.*

### STEP 1: Source Type Judgment

**Execute source detection before any analysis:**

1. **When input is URL:**
   - Detect domain: `reddit.com` (including mobile/legacy domains) → **Reddit Mode**
   - Other domains → **Technical Article Mode**
   - Call appropriate tools:
     - Reddit Mode: Use chrome-devtools to fetch body + Top 5 comments
     - Technical Article Mode: Use webReader first for clean extraction, but if any login/anti-scraping block appears, immediately switch to chrome-devtools

2. **When input is direct content:**
   - Check for Reddit features: "upvote", "comment thread", "u/" prefix → **Reddit Mode**
   - No features → **Technical Article Mode**

3. **Exception handling:**
   - 404/empty content → Return: `ERROR: Content fetch failed [URL]`
   - Login-gated / anti-scraping blocked content (e.g., 401/403, captcha/challenge page, "sign in to continue") → immediately use chrome-devtools and do NOT try other fetch methods
   - Non-technical content (news/video/shopping) → Return: `ERROR: Only technical content supported [type]`

### STEP 2: Identify Article Type

**Reddit Mode:** Skip type detection, proceed directly to STEP 3 Reddit output format.

**Technical Article Mode:** Determine which of the following types best fits the article. Different types call for different analytical depth and output structure.

| 类型 | 识别特征 | 分析侧重 |
|------|----------|----------|
| **技术观点文** | 提出明确主张、有对比论证、有"我认为"类表述 | SCQA + 论点拆解 + 批判性评价（完整框架） |
| **教程/实操文** | 分步骤指引、有代码示例、偏 how-to | 知识结构梳理 + 前置依赖 + 实操可行性评估 |
| **经验分享文** | 项目复盘、踩坑记录、最佳实践 | 经验提炼 + 可迁移性分析 + 适用条件 |
| **工具介绍文** | 功能介绍、使用方法、与同类对比 | 工具定位 + 优劣势 + 适用场景 |
| **混合类型** | 兼具多种特征 | 以主要特征为主，兼顾次要特征 |

### STEP 3: Two-Pass Deep Reading & Analysis

**All outputs are in Chinese. Preserve English technical terms (e.g., `PagedAttention`, `vLLM`). Output directly to console — DO NOT use Write tool.**

**Two-pass reading is mandatory for all single article analysis. The goal is to avoid shallow first-impression bias — the second pass often reveals nuances, implicit assumptions, and structural logic that the first pass misses.**

#### Pass 1: Initial Read (Quick Comprehension)

Read through the article once to build a mental model:
- What is the author's main claim or goal?
- What is the overall structure and flow?
- Which sections seem most important?
- What questions or uncertainties arise?

Do NOT output anything yet. Internally note your first impressions and any gaps in understanding.

#### Pass 2: Close Read (Deep Analysis)

Re-read the article with focused attention, now that you have the full picture:
- Verify your initial impressions — were they accurate?
- Examine the evidence and reasoning behind each claim
- Look for implicit assumptions the author makes
- Identify what the author chose NOT to say (omissions)
- Check for internal consistency across sections
- Extract all data points, metrics, and specific examples

Only after completing both passes, generate the final output below.

---

#### Reddit Mode Output

For Reddit threads, extract the main post and community discussion:

- Core content from body, with location mark (e.g., [正文 15-30%])
- Top 5 comments sorted by upvotes:
  - Mainstream consensus (≥3 similar high-upvote viewpoints)
  - Key controversies (opposing views + evidence)
  - Empirical verifications (cite `@username (upvotes↑)` + data)

---

#### Technical Article Mode: Type-Specific Output

Select the template that matches the article type identified in STEP 2.

**A. 技术观点文（完整批判性分析）**

```markdown
## 文章元信息
- 标题：
- 作者：
- 发表时间： | 更新时间：
- 浏览量：
- 所属圈子/专题：

## 一句话总结
用一句话概括文章的核心主张和结论。不要泛泛而谈，要抓住作者真正想说的那个判断。

## SCQA 脉络
- **Situation（情境）**：作者描述了什么背景/现状？
- **Complication（冲突）**：这个现状中出现了什么矛盾/问题/反直觉的事实？
- **Question（问题）**：由此引出的核心问题是什么？
- **Answer（答案）**：作者给出的回答/方案是什么？

## 观点全景

**⚠️ 完整性原则：必须输出作者在文章中表达的所有观点，不得因"次要"而省略。读者依赖此分析作为原文的忠实映射，遗漏任何观点都会造成信息损失。**

### 核心论点（详细分析）

针对文章中分量最重、论证最充分的 2-4 个主要论点，进行完整拆解：

### 论点 1：[论点名称]
- **主张**：作者认为...
- **论据**：
  - [列出支撑该论点的具体证据、数据、案例]
- **推理逻辑**：[强/中/弱] — [解释为什么给出这个评价]

### 论点 2：...
（重复上述结构）

### 次要观点（完整列出）

以下为作者在文章中提及但着墨较少的观点、建议、顺带提到的判断或注脚式结论。**不要因为它们"不重要"就跳过**——作者选择写下它们是有原因的：

- **[观点标题]**：[作者原意的简洁转述，1-2 句]
- **[观点标题]**：[作者原意的简洁转述，1-2 句]
- ...（穷举，不设上限）

> 判断标准：只要作者在正文中明确表达了一个立场、判断或建议，就应列入此处，哪怕只有一句话。

## 关键数据与证据
以表格或列表形式汇总文章中出现的所有关键数据点（数字、对比、实验结果等），方便读者快速回顾。

## 批判性评价

### 论证强项
- [列出论证有力的地方及原因]

### 论证弱项 / 可商榷之处
- [列出论证薄弱或值得质疑的地方]
注意：不要为了"平衡"而强行找茬。如果论证确实扎实，就如实说。

### 被忽略的视角
- [作者没有考虑到但值得讨论的角度]

## 适用边界
- **成立条件**：该文观点在什么前提下成立？
- **不成立条件**：什么场景下结论可能不适用？

## 社区反馈
如果文章有评论区，则从评论区提取有价值的观点，包括：
- 支持/补充作者观点的评论
- 提出不同意见或质疑的评论
- 作者的回复中包含的额外信息
（如果评论区没有实质内容，可省略此节）

## 行动建议
- **可以立即应用的点**：读完这篇文章，有哪些东西可以直接拿来用？
- **需要进一步验证的点**：哪些结论还需要在自己的场景中验证？

## 延伸思考
基于这篇文章的观点，提出 2-3 个值得进一步探讨的问题。这些问题应该是文章引发但未深入讨论的方向。
```

**B. 教程/实操文**

```markdown
## 文章元信息
（同上）

## 一句话总结

## 知识结构
- **目标**：这篇教程教你做什么？
- **前置知识**：需要哪些基础？
- **核心步骤**：列出关键步骤概要（不复制全文，提炼骨架）
- **关键产出**：跟着做完之后你会得到什么？

## 技术要点
列出教程中的关键技术点、配置项、易错点。

## 实操可行性评估
- **完整性**：步骤是否完整？有无遗漏？
- **准确性**：技术细节是否正确？（基于你的知识判断）
- **时效性**：涉及的工具/API 版本是否过时？

## 社区反馈
（同上）

## 行动建议
```

**C. 经验分享文**

```markdown
## 文章元信息
（同上）

## 一句话总结

## 背景与上下文
作者在什么项目/场景下积累了这些经验？

## 核心经验提炼
### 经验 1：[名称]
- **内容**：...
- **支撑案例**：...
- **可迁移性**：[高/中/低] — 在其他场景是否适用？需要什么条件？

### 经验 2：...

## 批判性评价
- 哪些经验具有普遍性？
- 哪些可能受限于作者的特定上下文？

## 社区反馈
（同上）

## 行动建议
```

**D. 工具介绍文**

```markdown
## 文章元信息
（同上）

## 一句话总结

## 工具概览
- **定位**：解决什么问题？
- **核心特性**：
- **技术栈**：

## 优劣势分析
| 维度 | 评价 | 说明 |
|------|------|------|
| ... | ... | ... |

## 适用场景
- 适合：...
- 不适合：...

## 同类对比
（如果文章中有对比，提炼出来；如果没有，基于你的知识补充）

## 社区反馈
（同上）

## 行动建议
```

---

#### Analysis Principles

These apply to all technical article types:

1. **先理解再评价**：确保准确理解作者的意图后再做评价。不要歪曲或简化作者的论点。
2. **观点完整性**：分析的首要职责是忠实呈现作者的完整思想图谱。核心论点要深度拆解，次要观点也必须列出——哪怕只是作者的一句断言、一个建议、一个顺带提及的判断，都不应被丢弃。读者依赖这份分析作为原文的替代，任何遗漏都是信息失真。
3. **区分事实和观点**：明确标注哪些是文章中的事实陈述，哪些是作者的主观判断。
4. **建设性批评**：指出问题时给出具体理由，不要空洞地说"论证不够充分"。
5. **公允**：如果作者的论证确实扎实，就说扎实。不要为了显得"有深度"而强行找茬。
6. **聚焦价值**：行动建议要具体可执行，不要写"可以进一步研究"这种空话。

**⚠️ IMPORTANT for Single Article Mode:**
- Output the analysis directly to console (use text response)
- DO NOT use Write tool to create files
- DO NOT save any markdown files locally
- Display complete analysis in the conversation

---

## MODE B: RSS/Batch Analysis

*Use this mode for RSS feeds, blog homepages, or when multiple articles need to be analyzed. Results are saved to local markdown files with a generated index.*

### STEP 4: RSS Feed Detection & Parsing

**When RSS Mode is triggered in STEP 0:**

1. **Create output directory**:
   ```bash
   mkdir -p /Users/leo/projects/[blog-name]-analysis-[YYYYMMDD]/
   ```

2. **Fetch and parse RSS feed using ctx_execute**:
   ```python
   ctx_execute(
       language="python",
       code="""
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import json

# Fetch RSS feed
import urllib.request
response = urllib.request.urlopen('[RSS_URL]')
xml_content = response.read()

# Parse feed
tree = ET.fromstring(xml_content)
ns = {'atom': 'http://www.w3.org/2005/Atom'}

# Extract articles from past 7 days
cutoff_date = datetime.now() - timedelta(days=7)
articles = []

for entry in tree.findall('.//atom:entry', ns) or tree.findall('.//item'):
    title = entry.find('atom:title', ns) or entry.find('title')
    link = entry.find('atom:link', ns) or entry.find('link')
    date = entry.find('atom:published', ns) or entry.find('pubDate')

    if title is not None and link is not None and date is not None:
        pub_date = datetime.fromisoformat(date.text.replace('Z', '+00:00'))
        if pub_date >= cutoff_date:
            articles.append({
                'title': title.text,
                'url': link.get('href') if link.get('href') else link.text,
                'date': date.text
            })

# Output summary only
print(f"Found {len(articles)} articles from past 7 days")
print(json.dumps(articles, ensure_ascii=False))
       """,
       intent="Parse RSS feed and filter to past 7 days"
   )
   ```

**CRITICAL: Default behavior is to analyze ONLY articles from the past 7 days. Do not analyze older articles unless user explicitly requests it.**

### STEP 5: Sequential Batch Analysis with SubAgents

**Execute batch analysis using Agent tool:**

**Step 5.1: Confirm article scope and divide into groups**

Auto-confirm the scope before execution:
```
Found {N} articles from past 7 days ({start_date} to {end_date}).
Proceeding with analysis of these {N} articles.

Note: To analyze ALL articles (not just past 7 days), explicitly request it.
```

Then divide the filtered articles into groups:
- For ≤10 articles: Use 2 subAgents (Group 1: 1-N/2, Group 2: N/2+1-N)
- For 11-20 articles: Use 3 subAgents (Group 1: 1-N/3, Group 2: N/3+1-2N/3, Group 3: 2N/3+1-N)
- If odd number: First group gets the extra article

**Step 5.2: Launch subAgents SEQUENTIALLY (foreground execution)**

For each subAgent group, process articles one by one. For **each article**, subAgent MUST:

1. Fetch article content
   - Use `ctx_fetch_and_index` (preferred) or `webReader` only when no interception appears
   - If login-state/anti-scraping interception appears, switch directly to `chrome-devtools` and do NOT try other fetch methods
2. Run source detection + article type detection
   - Follow **Single Article Mode STEP 1 + STEP 2** exactly
3. Perform mandatory two-pass deep reading
   - Follow **Single Article Mode STEP 3** exactly
4. Generate final analysis using **Single Article Mode type-specific template**
   - Reddit URL/content → use **Reddit Mode Output**
   - Technical article → choose one template from:
     - A. 技术观点文
     - B. 教程/实操文
     - C. 经验分享文
     - D. 工具介绍文
5. Write analysis to markdown file
   - Keep the selected single-article template structure intact
   - Do NOT convert to any custom RSS file skeleton

**Step 5.3: Wait for each subAgent to complete**
- SubAgents run in foreground (sequential execution)
- Each completes before the next starts

**Step 5.4: Consolidate and verify completeness**
- Verify every article produced one markdown file
- Verify each file follows one of the single-article templates above
- Verify no file uses deprecated RSS-specific skeleton sections

### STEP 6: Generate Index README

**Create README.md after all subAgents complete:**

```markdown
# [Blog Name] Analysis Report

## 概览
- **文章总数**: N
- **时间范围**: [start] - [end]
- **分析日期**: [timestamp]
- **执行方式**: 2-3 个并发 subAgent
- **导出目录**: /Users/leo/projects/[blog-name]-analysis-[YYYYMMDD]/

## 📁 文件列表

### 1. [Article Title] ([Date])
- **文件**: `01-[slug].md`
- **URL**: [link]
- **核心主题**: [topics]
- **价值密度**: ⭐⭐⭐

[... continue for all articles ...]

## 跨文章主题总结

### 核心主题簇
- [Theme 1]: [description with article references]
- [Theme 2]: [description with article references]

### 技术趋势
- [Trend 1]: [description]
- [Trend 2]: [description]

### 关键洞察
- [Insight 1]: [description]
- [Insight 2]: [description]

*生成时间: [timestamp]*
*分析工具: web-tech-article-analyzer*
```

**CRITICAL REQUIREMENTS for RSS Mode:**
- ⚠️ **Analyze EVERY article** from the past 7 days - do not skip any
- ⚠️ **Each article file MUST follow Single Article Mode template output** (A/B/C/D or Reddit)
- ⚠️ **Do NOT use deprecated RSS custom file skeleton** (`Content Overview/Detailed Outline/Core Summary/Deep Analysis/Unique Value`)
- ⚠️ **Use ctx_fetch_and_index** in subAgents to avoid context pollution
- ⚠️ **Use ctx_search** to extract key information efficiently
- ⚠️ **SubAgents run in FOREGROUND** (run_in_background=false) to allow permission requests
- ⚠️ **Specify exact output file paths** for each article in the subAgent prompt
- ⚠️ **Verify completeness** - ensure each subAgent produced full analyses, not summaries

## Output Format Summary

### Single Article Mode (Console Output)
- Output analysis directly to console
- No file creation
- Detect article type first (技术观点文 / 教程实操文 / 经验分享文 / 工具介绍文)
- Use the type-specific output template from STEP 3
- Display in conversation

### RSS/Batch Mode (File Output)
- Create individual markdown files for each article
- Generate README.md index file
- Save to: `/Users/leo/projects/[blog-name]-analysis-[YYYYMMDD]/`
- **For each article file, use the SAME analysis method and SAME output template as Single Article Mode**
- Do NOT use any RSS-specific custom article skeleton format

### Individual Article File Template (RSS Mode)

In RSS mode, each article file MUST reuse Single Article Mode templates exactly:
- Reddit content → `Reddit Mode Output`
- Technical article → choose one:
  - `A. 技术观点文（完整批判性分析）`
  - `B. 教程/实操文`
  - `C. 经验分享文`
  - `D. 工具介绍文`

⚠️ Deprecated and removed in RSS mode:
- `## 📌 Content Overview`
- `## 📑 Detailed Outline`
- `## 💎 Core Summary`
- `## ⚙️ Deep Analysis`
- `## 🌟 Unique Value`

### README.md Template (Index File - RSS Mode Only)

```markdown
# [Blog Name] Analysis Report

## 概览
- **文章总数**: N
- **时间范围**: [start] - [end] (过去 7 天)
- **分析日期**: [timestamp]
- **原始来源**: [blog URL]
- **RSS Feed**: [feed URL]

## 📁 文件列表

### 1. [Article Title] ([Date])
- **文件**: `01-[slug].md`
- **URL**: [link]
- **核心主题**: [topics]
- **价值密度**: ⭐⭐⭐

### 2. [Article Title] ([Date])
- **文件**: `02-[slug].md`
- **URL**: [link]
- **核心主题**: [topics]
- **价值密度**: ⭐⭐⭐

[... continue for all articles ...]

## 跨文章主题总结

### 核心主题簇
- [Theme 1]: [description]
- [Theme 2]: [description]

### 技术趋势
- [Trend 1]: [description]
- [Trend 2]: [description]

### 关键洞察
- [Insight 1]: [description]
- [Insight 2]: [description]

*生成时间: [timestamp]*
*分析工具: web-tech-article-analyzer*
```

## Execution Guidelines

### Single Article Mode
1. **Console output only**: Display analysis directly in conversation, no file creation
2. **Type detection first**: Identify article type (技术观点文/教程实操文/经验分享文/工具介绍文) before generating analysis
3. **Type-specific template**: Use the matching output template from STEP 3
4. **No Write tool**: Do NOT create any markdown files

### RSS/Batch Mode
1. **Automatic batch processing**: For RSS feeds/blog homepages, automatically analyze all articles from past 7 days
2. **Sequential execution**: Use 2-3 subAgents running in FOREGROUND mode (not parallel)
3. **Context-efficient**: SubAgents use ctx_fetch_and_index + ctx_search to avoid context pollution
4. **File output**: Create individual markdown files + README.md index
5. **Complete analysis**: Each article gets FULL detailed analysis, not summaries
6. **No confirmation needed**: Proceed directly with analysis after detection

### General Guidelines
1. **Judgment first**: Never proceed to analysis without completing STEP 0 (URL type detection)
2. **Interception handling (critical)**:
   - If you hit login-state interception or anti-scraping interception at any point, switch directly to `chrome-devtools` immediately
   - Do NOT retry `webReader`, `curl`, `fetch`, or any other non-browser fetch path after interception is detected
3. **Location marking**:
   - Sections: Use percentage ranges ([25-40%])
   - Reddit comments: Mark `[评论区: Top N]`
4. **Anti-redundancy**:
   - Non-Reddit content: Hide all 💬/✅/⚠️ fields
   - Basic concept sections: 1-line summary only
5. **Termination conditions**:
   - Cannot identify type → `ERROR: Cannot identify content source [input summary]`
   - Insufficient value density (pure discussion) → Output outline + core summary only

## Available Tools

### Single Article Mode
- **mcp__web_reader__webReader**: Primary tool for clean extraction on non-blocked technical articles
- **mcp__chrome-devtools***: Required for Reddit content and mandatory when login/anti-scraping interception is detected
- **WebSearch**: For supplementing context when needed

### RSS/Batch Mode
- **Agent**: For creating sequential subAgents during batch article analysis
  - **Use 2-3 subAgents** for processing article groups
  - **subagent_type**: general-purpose
  - **run_in_background**: false (FOREGROUND execution to allow permission requests)
  - **CRITICAL**: SubAgents must use context-mode MCP tools
- **mcp__context-mode__ctx_execute**: For RSS feed parsing (avoids loading XML into context)
- **mcp__context-mode__ctx_fetch_and_index**: Used by subAgents to fetch and index article content
  - Indexes content into searchable knowledge base
  - Returns only ~3KB preview to context
  - Full content stays in sandbox
- **mcp__context-mode__ctx_search**: Used by subAgents to extract key information
  - Search indexed content with multiple queries
  - Returns only relevant sections
  - Avoids loading full article into context
- **mcp__chrome-devtools***: Mandatory tool for intercepted pages (login-gated or anti-scraping blocked content)
- **Write**: For creating markdown files with article analysis (used by subAgents)

## Tool Selection Strategy

### URL Type Detection (STEP 0)
1. **For RSS feed detection**: Use `scripts/rss_parser.py` to check for RSS feeds in homepage
2. **For URL pattern matching**: Check for `/rss`, `/feed`, `.xml`, `atom.xml` patterns

### Single Article Mode
0. **Check domain rules first**: Read `references/domain-specific-rules.md` — some domains (e.g., reddit.com, linux.do) require specific tools
1. **For Reddit URLs**: Use `chrome-devtools` to navigate and capture full content including comments
2. **For technical articles**: Use `webReader` with markdown format only when no interception appears
3. **If login-state/anti-scraping interception appears** (any domain): immediately switch to `chrome-devtools`; do NOT attempt other fetch methods first
4. **For content already provided**: Skip fetching, proceed directly to analysis

### RSS/Batch Mode
1. **For RSS feed parsing**: Use `scripts/rss_parser.py` to parse feed and extract articles
2. **For article fetching**: subAgents use `webReader`/`ctx_fetch_and_index` only when no interception appears
3. **If interception appears during article fetching**: switch immediately to `chrome-devtools`; do NOT retry other fetch methods
4. **For parallel processing**: Use TaskTool to launch multiple subAgents

## Important Notes

### Single Article Mode Behavior
- ✅ **DO**: Output analysis directly to console
- ✅ **DO**: Detect article type first, then apply the matching template
- ✅ **DO**: Display results in conversation
- ✅ **DO**: Switch directly to `chrome-devtools` when login-state or anti-scraping interception is encountered
- ❌ **DO NOT**: Create any markdown files
- ❌ **DO NOT**: Use Write tool
- ❌ **DO NOT**: Try `webReader`/`curl`/`fetch` retries after interception is detected

### RSS/Batch Mode Behavior
- ✅ **DO**: Automatically analyze ONLY articles from past 7 days (default behavior)
- ✅ **DO**: Confirm article count with user before starting: "Found N articles from past 7 days. Proceeding..."
- ✅ **DO**: Create a separate markdown file for EACH article
- ✅ **DO**: Include FULL detailed analysis in each file
- ✅ **DO**: Generate README.md index file
- ✅ **DO**: Offer to analyze ALL articles if user requests explicitly
- ❌ **DO NOT**: Analyze articles older than 7 days without explicit user request
- ❌ **DO NOT**: Ask for confirmation on article count (auto-confirm with count)
- ❌ **DO NOT**: Create only summary files

### Quality Requirements
Each article analysis (both modes) must be comprehensive:
- Follow one valid single-article template completely (A/B/C/D or Reddit)
- Preserve required sections for the selected template (do not mix templates arbitrarily)
- Include full argument/evidence extraction instead of brief summaries
- In RSS mode, do NOT use deprecated RSS custom skeleton headings

### File Organization (RSS Mode Only)
```
[blog-name]-analysis-[YYYYMMDD]/
├── README.md (index)
├── 01-[slug].md
├── 02-[slug].md
├── 03-[slug].md
└── ...
```

## Example Output Structure

### Single Article Mode (Console Output)
```
## 文章元信息
- 标题：vLLM: PagedAttention for LLM Serving
- 作者：Woosuk Kwon et al.
- 发表时间：2023-09-12
- 浏览量：N/A
- 所属圈子/专题：LLM Inference

【文章类型识别：技术观点文】

## 一句话总结
vLLM 通过 PagedAttention 将 KV cache 的内存碎片问题降至接近零，从根本上解决了大模型并发推理的显存瓶颈。

## SCQA 脉络
- **Situation**：大模型推理服务需要管理大量并发请求的 KV cache
- **Complication**：传统连续内存分配导致 60-80% 的显存浪费在内部/外部碎片
- **Question**：如何在不改变模型本身的前提下大幅提升显存利用率？
- **Answer**：借鉴操作系统虚拟内存分页思想，将 KV cache 以固定大小的 block 管理

## 核心论点拆解

### 论点 1：KV cache 碎片是吞吐量瓶颈的根本原因
- **主张**：作者认为现有系统的低吞吐量不是算法问题，而是内存管理问题
- **论据**：实测显示传统系统 KV cache 显存利用率仅 20-40%
- **推理逻辑**：强 — 有具体的内存分析数据支撑，问题定位清晰
...
```

### RSS/Batch Mode (File Output)
Same structure as console output, but saved to individual markdown files with README.md index.

---

## SubAgent Prompt Template (For RSS/Batch Mode Only)

When launching subAgents for batch article analysis, use the following template:

```
You are a technical article analyzer working with the web-tech-article-analyzer skill.

Your task is to analyze [N] articles from a blog and create a detailed markdown file for each one.

NOTE: These articles have ALREADY been filtered to include ONLY the past 7 days. This is the default behavior - do not analyze older articles.

OUTPUT DIRECTORY: /Users/leo/projects/[blog-name]-analysis-[YYYYMMDD]/

ARTICLES TO ANALYZE:
1. [Article Title 1]
   URL: [url1]
   Target file: 01-[slug1].md

2. [Article Title 2]
   URL: [url2]
   Target file: 02-[slug2].md

[... continue for all articles in your group ...]

WORKFLOW FOR EACH ARTICLE:

Step 1: Fetch and read content
- Use `ctx_fetch_and_index` + `ctx_search` (preferred) or `webReader` only when no interception appears
- If login-state/anti-scraping interception appears, switch directly to `chrome-devtools` and do NOT try other fetch methods

Step 2: Detect source/type exactly as Single Article Mode
- Run STEP 1 (source detection: Reddit vs Technical Article)
- Run STEP 2 (type detection for technical article)

Step 3: Analyze exactly as Single Article Mode
- Run mandatory Two-Pass Deep Reading
- Output MUST use the exact matching template from Single Article Mode:
  - Reddit → Reddit Mode Output
  - Technical article → one of A/B/C/D templates

Step 4: Write markdown file
- Write to `[OUTPUT_DIRECTORY]/[target-file]`
- Preserve template structure exactly
- Do NOT use deprecated RSS custom skeleton headings

Step 5: Move to next article
- Process all articles sequentially
- Do not skip any article

COMPLETION:
After analyzing ALL articles in your group:
1. List all files you created
2. Briefly summarize cross-article themes in 2-3 sentences
```
