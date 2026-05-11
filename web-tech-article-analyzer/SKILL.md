---
name: web-tech-article-analyzer
description: Analyze web technical articles, URLs, blog posts, and article lists with a 7-layer framework. Handles single articles, RSS/batch workflows, Reddit, X/Twitter, arxiv, GitHub, technical blogs, and tap-backed sources including Simon Willison, Claude, Anthropic Engineering, and Baoyu. Outputs Chinese analysis with English technical terms preserved. Use when the user provides or asks to browse/analyze technical article content, URLs, or supported blogs, even without saying "deep analysis."
---

# Web Tech Article Analyzer

## Overview

This skill specializes in efficiently deconstructing web-based technical content and performing deep analysis of articles using a **7-layer analytical framework**. It intelligently routes to different processing modes based on input type:

- **Single Article Mode**: Fetch, analyze, and output detailed analysis directly to the console (no file creation)
- **RSS/Batch Mode**: Parse RSS feeds, analyze multiple articles in parallel, and save each analysis to a local markdown file with a generated README index

For single articles, choose the reading strategy by content size and fidelity needs:

- **Short Article Direct Mode**: For short, simple articles that fit comfortably in context, read the complete content directly. This preserves completeness and avoids search-induced blind spots.
- **Indexed Long Article Mode**: For medium/long articles or noisy pages, use context-mode as a local full-text index, then perform structured multi-query retrieval, exact spot checks, and coverage validation.

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
- User wants to browse or analyze Simon Willison's blog articles (simonwillison.net)
- User wants to browse or analyze Claude blog articles (claude.com/blog)
- User wants to browse or analyze Anthropic engineering blog articles (anthropic.com/engineering)
- User wants to browse or analyze Baoyu blog articles (baoyu.io)
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
   - Detect domain: `x.com` or `twitter.com` → **X Tweet Mode**
   - Detect domain: `reddit.com` (including mobile/legacy domains) → **Reddit Mode**
   - Detect domain: `simonwillison.net` → **Simon Willison Mode**
   - Detect domain: `claude.com` → **Claude Blog Mode**
   - Detect domain: `anthropic.com/engineering` → **Anthropic Engineering Mode**
   - Detect domain: `baoyu.io` → **Baoyu Mode**
   - Other domains → **Technical Article Mode**
   - Call appropriate tools:
     - X Tweet Mode: Run `tap x tweet --url {url}` via Bash — do NOT use chrome-devtools or context-mode
     - Reddit Mode: Run `tap reddit thread --url {url}` via Bash — do NOT use chrome-devtools or context-mode
     - Simon Willison Mode: Run `tap simonwillison post --url {url}` via Bash — do NOT use chrome-devtools or context-mode
     - Claude Blog Mode: Run `tap claude post --url {url}` via Bash — do NOT use chrome-devtools or context-mode
     - Anthropic Engineering Mode: Run `tap anthropic article --url {url}` via Bash — do NOT use chrome-devtools or context-mode
     - Baoyu Mode: Run `tap baoyu article --url {url}` via Bash — do NOT use chrome-devtools or context-mode
     - Technical Article Mode: Use webReader first for clean extraction, but if any login/anti-scraping block appears, immediately switch to chrome-devtools

2. **When input is direct content:**
   - Check for Reddit features: "upvote", "comment thread", "u/" prefix → **Reddit Mode**
   - No features → **Technical Article Mode**

3. **Exception handling:**
   - 404/empty content → Return: `ERROR: Content fetch failed [URL]`
   - Login-gated / anti-scraping blocked content (e.g., 401/403, captcha/challenge page, "sign in to continue") → immediately use chrome-devtools and do NOT try other fetch methods (does not apply to X/Twitter, Reddit, Simon Willison, Claude Blog, Anthropic Engineering, or Baoyu — use tap CLI only)
   - Non-technical content (news/video/shopping) → Return: `ERROR: Only technical content supported [type]`

### X Tweet Mode

For `x.com` or `twitter.com` URLs, fetch content exclusively via the `tap` CLI:

```bash
tap x tweet --url {url}
```

- Run this as a Bash command; the output is the tweet/thread content.
- Do NOT fall back to chrome-devtools, webReader, or context-mode for X URLs.
- After fetching, analyze the content using the Technical Article Mode output templates (or Reddit Mode Output if the thread resembles a community discussion), applying the same 7-layer framework as appropriate.

### Simon Willison Mode

For `simonwillison.net` URLs or when user wants to browse Simon Willison's blog, use the `tap` CLI exclusively.

**Workflow:**

1. **List articles** — Run `tap simonwillison articles` via Bash to get the article list
2. **Present list and wait for user selection** — Display the article list with numbered entries, ask user which articles to analyze (same pattern as RSS Mode STEP 4.5)
3. **Fetch selected article content** — For each selected article, run:
   ```bash
   tap simonwillison post --url {url}
   ```
4. **Analyze** — Use Technical Article Mode output templates (A/B/C/D) with the same 7-layer framework

**Rules:**
- Do NOT use chrome-devtools, webReader, or context-mode for Simon Willison content — `tap` CLI handles everything
- Do NOT start analysis until user confirms which articles they want to analyze
- Output directly to console for single article; use Write tool for batch analysis (same as RSS Mode)

### Claude Blog Mode

For `claude.com` URLs or when user wants to browse Claude's official blog, use the `tap` CLI exclusively.

**Workflow:**

1. **List articles** — Run `tap claude articles` via Bash to get the article list
2. **Present list and wait for user selection** — Display the article list with numbered entries, ask user which articles to analyze (same pattern as RSS Mode STEP 4.5)
3. **Fetch selected article content** — For each selected article, run:
   ```bash
   tap claude post --url {url}
   ```
4. **Analyze** — Use Technical Article Mode output templates (A/B/C/D) with the same 7-layer framework

**Rules:**
- Do NOT use chrome-devtools, webReader, or context-mode for Claude blog content — `tap` CLI handles everything
- Do NOT start analysis until user confirms which articles they want to analyze
- Output directly to console for single article; use Write tool for batch analysis (same as RSS Mode)

### Anthropic Engineering Mode

For `anthropic.com/engineering` URLs or when user wants to browse Anthropic engineering blog, use the `tap` CLI exclusively.

**Workflow:**

1. **List articles** — Run `tap anthropic articles` via Bash to get the article list
2. **Present list and wait for user selection** — Display the article list with numbered entries, ask user which articles to analyze (same pattern as RSS Mode STEP 4.5)
3. **Fetch selected article content** — For each selected article, run:
   ```bash
   tap anthropic article --url {url}
   ```
4. **Analyze** — Use Technical Article Mode output templates (A/B/C/D) with the same 7-layer framework

**Rules:**
- Do NOT use chrome-devtools, webReader, or context-mode for Anthropic engineering content — `tap` CLI handles everything
- Do NOT start analysis until user confirms which articles they want to analyze
- Output directly to console for single article; use Write tool for batch analysis (same as RSS Mode)

### Baoyu Mode

For `baoyu.io` URLs or when user wants to browse Baoyu's blog, use the `tap` CLI exclusively.

**Workflow:**

1. **List articles** — Run `tap baoyu articles` via Bash to get the article list
2. **Present list and wait for user selection** — Display the article list with numbered entries, ask user which articles to analyze (same pattern as RSS Mode STEP 4.5)
3. **Fetch selected article content** — For each selected article, run:
   ```bash
   tap baoyu article --url {url}
   ```
4. **Analyze** — Use Technical Article Mode output templates (A/B/C/D) with the same 7-layer framework

**Rules:**
- Do NOT use chrome-devtools, webReader, or context-mode for Baoyu content — `tap` CLI handles everything
- Do NOT start analysis until user confirms which articles they want to analyze
- Output directly to console for single article; use Write tool for batch analysis (same as RSS Mode)

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

### STEP 2.5: Context Strategy Selection

**Before deep reading, choose one strategy. Optimize for fidelity first, then context efficiency.**

| Strategy | Use when | Tools | Completeness rule |
|---|---|---|---|
| **Short Article Direct Mode** | Article is short/simple enough to read fully in context, roughly ≤8k Chinese chars / ≤5k English words, or user needs one-off analysis | `webReader`, direct content, or `chrome-devtools` + direct Read | Read the whole article directly. Do not use context-mode because retrieval adds avoidable blind spots. |
| **Standard Indexed Mode** | Medium/long article, many code blocks/tables, noisy HTML, or user will ask follow-ups | `ctx_fetch_and_index` / `ctx_index` + `ctx_search`, with exact direct spot checks for critical fragments | First extract structure, then search by chapter and analysis dimension. Do coverage check before final output. |
| **Strict Indexed Mode** | Important long article, high-fidelity analysis, many numbers/code/configs, or user asks to avoid information loss | Same as Standard Indexed Mode plus chapter-by-chapter fact extraction and conclusion backtrace | Separate facts from interpretation. Every major conclusion must cite source section/fragment. |

**Decision heuristics:**
- If the full article can be read once without crowding the context window, prefer **Short Article Direct Mode**.
- If direct reading would require many large snapshots/segments, prefer **Standard Indexed Mode**.
- If the task is legal/compliance/line-by-line review/full translation/zero-omission extraction, state that context-mode alone is not sufficient; use direct full-text or chapter-by-chapter exact extraction.
- For Reddit pages, follow domain rules first — use `tap reddit thread --url {url}` exclusively. For login-gated pages, use `chrome-devtools`. Choose direct Read for short pages and `ctx_index` for long/noisy snapshots.

**Indexed Mode workflow:**
1. Build index with `ctx_fetch_and_index` for URLs or `ctx_index` for already fetched/local content.
2. Extract article structure first: title, headings, sections, content types (code/table/image/formula/reference).
3. Search by chapters or headings, not only by generic summary prompts.
4. Run multi-perspective queries: problem/motivation, architecture/design, implementation/code, tradeoff/limitation, performance/benchmark, security/risk, testing/validation, conclusion/takeaway.
5. Precisely spot-check code blocks, CLI commands, configs, API params, benchmark numbers, tables, formulas, and strong claims (`must`, `should`, `never`, `only`) with direct extraction when possible.
6. Produce fact notes first, then analysis. Mark unsupported analysis as inference.
7. Run coverage validation against the structure: list unexamined sections, missing code/table/data, and any low-confidence conclusions; search again if gaps matter.

### STEP 3: Two-Pass Deep Reading & Analysis

**All outputs are in Chinese. Preserve English technical terms (e.g., `PagedAttention`, `vLLM`). Output directly to console — DO NOT use Write tool.**

**Two-pass reading is mandatory for all single article analysis. In Direct Mode, both passes operate on complete article content. In Indexed Mode, Pass 1 uses structure + broad retrieval, and Pass 2 uses targeted chapter/dimension retrieval plus exact spot checks. The goal is to avoid shallow first-impression bias — the second pass often reveals nuances, implicit assumptions, and structural logic that the first pass misses.**

#### Pass 1: Initial Read (Quick Comprehension)

Build a mental model:
- What is the author's main claim or goal?
- What is the overall structure and flow?
- Which sections seem most important?
- What questions or uncertainties arise?

Direct Mode: read through the article once.

Indexed Mode: retrieve structure first, then broad chapter summaries. Do not form conclusions from one search result.

Do NOT output anything yet. Internally note your first impressions and any gaps in understanding.

#### Pass 2: Close Read (Deep Analysis)

Re-read the article with focused attention, now that you have the full picture:
- Verify your initial impressions — were they accurate?
- Examine the evidence and reasoning behind each claim
- Look for implicit assumptions the author makes
- Identify what the author chose NOT to say (omissions)
- Check for internal consistency across sections
- Extract all data points, metrics, and specific examples

Indexed Mode: run targeted searches for each important heading and each analysis dimension. Exact-check all critical code/data/config fragments before finalizing.

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

### STEP 4.5: Present Article List & Wait for User Selection

**After parsing the RSS feed, display the article list and wait for user to select before starting any analysis.**

1. **Display numbered list** of all articles found (titles only, no analysis yet):

```
找到过去 7 天的文章 {N} 篇（{start_date} 至 {end_date}）：

1. [Article Title 1] — [Date]
2. [Article Title 2] — [Date]
3. [Article Title 3] — [Date]
...

请告诉我你想深入分析哪几篇？可以回复编号（如"1 3 5"），也可以说"全部"。
```

2. **Wait for user response** — do NOT proceed to analysis until the user selects articles.

3. **Parse user selection**:
   - "全部" / "all" / no specific numbers → analyze all listed articles
   - Specific numbers (e.g., "1 3 5") → analyze only those articles
   - Range (e.g., "1-3") → analyze articles 1, 2, 3

4. **Confirm selection before proceeding**:
```
好的，将分析以下 {M} 篇文章：
- [Selected Title 1]
- [Selected Title 2]
...
```

### STEP 5: Sequential Batch Analysis with SubAgents

**Execute batch analysis using Agent tool, on the user-selected articles only.**

**Step 5.1: Divide selected articles into groups**

Take the user-selected subset and divide into groups:
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
3. **Context strategy first**: Choose Direct Mode for short/simple articles; choose Standard/Strict Indexed Mode for medium/long articles
4. **Type-specific template**: Use the matching output template from STEP 3
5. **No Write tool**: Do NOT create any markdown files

### RSS/Batch Mode
1. **Selection-gated batch processing**: For RSS feeds/blog homepages, list articles from the past 7 days and wait for user selection
2. **Sequential execution**: Use 2-3 subAgents running in FOREGROUND mode (not parallel)
3. **Context-efficient**: SubAgents use ctx_fetch_and_index + ctx_search to avoid context pollution
4. **File output**: Create individual markdown files + README.md index
5. **Complete analysis**: Each article gets FULL detailed analysis, not summaries
6. **Confirmation required**: Do not analyze RSS articles until the user selects articles in STEP 4.5

### General Guidelines
1. **Judgment first**: Never proceed to analysis without completing STEP 0 (URL type detection)
2. **Interception handling (critical)**:
   - If you hit login-state interception or anti-scraping interception at any point, switch directly to `chrome-devtools` immediately
   - Do NOT retry `webReader`, `curl`, `fetch`, or any other non-browser fetch path after interception is detected
   - Exception: X/Twitter, Reddit, Simon Willison, Claude Blog, Anthropic Engineering, and Baoyu always use `tap` CLI — never chrome-devtools or context-mode
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
- **tap x tweet --url {url}** (Bash): Exclusive tool for `x.com` / `twitter.com` URLs — do NOT use chrome-devtools or context-mode for X
- **tap reddit thread --url {url}** (Bash): Exclusive tool for `reddit.com` URLs — do NOT use chrome-devtools or context-mode for Reddit
- **tap simonwillison articles** (Bash): List Simon Willison's blog articles — do NOT use chrome-devtools or context-mode
- **tap simonwillison post --url {url}** (Bash): Fetch Simon Willison's blog post content — do NOT use chrome-devtools or context-mode
- **tap claude articles** (Bash): List Claude blog articles — do NOT use chrome-devtools or context-mode
- **tap claude post --url {url}** (Bash): Fetch Claude blog post content — do NOT use chrome-devtools or context-mode
- **tap anthropic articles** (Bash): List Anthropic engineering blog articles — do NOT use chrome-devtools or context-mode
- **tap anthropic article --url {url}** (Bash): Fetch Anthropic engineering blog article content — do NOT use chrome-devtools or context-mode
- **tap baoyu articles** (Bash): List Baoyu blog articles — do NOT use chrome-devtools or context-mode
- **tap baoyu article --url {url}** (Bash): Fetch Baoyu blog article content — do NOT use chrome-devtools or context-mode
- **mcp__web_reader__webReader**: Primary tool for clean extraction on non-blocked technical articles
- **Read**: For reading snapshot files in segments when using chrome-devtools
- **WebSearch**: For supplementing context when needed
- **mcp__context-mode__ctx_fetch_and_index / ctx_index / ctx_search**: Use only for Standard/Strict Indexed Mode when the article is too long/noisy for reliable direct reading

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
1. **For X/Twitter URLs** (`x.com`, `twitter.com`): Run `tap x tweet --url {url}` via Bash. Never use chrome-devtools or context-mode.
2. **For Reddit URLs**: Run `tap reddit thread --url {url}` via Bash. Never use chrome-devtools or context-mode.
3. **For Simon Willison URLs** (`simonwillison.net`) or requests to browse Simon Willison's blog: Run `tap simonwillison articles` to list articles, wait for user selection, then run `tap simonwillison post --url {url}` for each selected article. Never use chrome-devtools or context-mode.
4. **For Claude Blog URLs** (`claude.com`) or requests to browse Claude's blog: Run `tap claude articles` to list articles, wait for user selection, then run `tap claude post --url {url}` for each selected article. Never use chrome-devtools or context-mode.
5. **For Anthropic Engineering URLs** (`anthropic.com/engineering`) or requests to browse Anthropic's engineering blog: Run `tap anthropic articles` to list articles, wait for user selection, then run `tap anthropic article --url {url}` for each selected article. Never use chrome-devtools or context-mode.
6. **For Baoyu URLs** (`baoyu.io`) or requests to browse Baoyu's blog: Run `tap baoyu articles` to list articles, wait for user selection, then run `tap baoyu article --url {url}` for each selected article. Never use chrome-devtools or context-mode.
7. **For technical articles**: Use `webReader` with markdown format only when no interception appears, then choose Direct vs Indexed Mode using STEP 2.5
5. **If login-state/anti-scraping interception appears** (any domain): immediately switch to `chrome-devtools`; do NOT attempt other fetch methods first
4. **For content already provided**: Skip fetching, then choose Direct vs Indexed Mode using STEP 2.5

### When using chrome-devtools in Single Article Mode

**Choose direct Read for short snapshots; index long/noisy snapshots.**

After `take_snapshot`, the output is saved to a file. For short snapshots, read it directly using the Read tool:

```
take_snapshot
  ↓
Read the snapshot file in segments (offset + limit)
  ↓
Perform Two-Pass Deep Reading on the complete content
  ↓
Generate analysis based on full understanding
```

For long/noisy snapshots, use the Indexed Mode pattern:

```
take_snapshot
  ↓
ctx_index(content=<snapshot_text>, source="<article-slug>")
  ↓
ctx_search with structure, chapter, and analysis-dimension queries
  ↓
exact spot checks for code/data/config fragments
  ↓
coverage validation before final analysis
```

**Why prefer direct reading for short articles?**
- Technical article analysis requires understanding the complete structure
- Search-based approaches may miss chapters/sections with unexpected keywords
- "Two-Pass Deep Reading" requires seeing the full content, not search results
- Completeness is more important than token optimization when the article fits comfortably in context

**How to handle large snapshots:**
- Use Read tool with offset and limit parameters
- If the whole snapshot can be read without context pressure, read in segments of 3000-5000 lines until complete
- If it would crowd the context window, index it and follow Standard/Strict Indexed Mode

### RSS/Batch Mode
1. **For RSS feed parsing**: Use `scripts/rss_parser.py` to parse feed and extract articles
2. **For article fetching**: subAgents use `webReader`/`ctx_fetch_and_index` only when no interception appears
3. **If interception appears during article fetching**: switch immediately to `chrome-devtools`; do NOT retry other fetch methods
4. **For parallel processing**: Use TaskTool to launch multiple subAgents

### ⚠️ Gotchas (Indexed Mode and RSS/Batch subAgents using chrome-devtools)

**`take_snapshot` can dump the full a11y tree into context — long/noisy snapshots should be indexed immediately.**

This applies to Standard/Strict Indexed Mode and RSS/Batch subAgents when they use `chrome-devtools`. The raw snapshot should not sit in context during analysis when it is too large for direct reading.

**Note**: Short Article Direct Mode should read snapshot content directly using the Read tool instead of using context-mode tools.

**Required pattern whenever `take_snapshot` is called:**
```
take_snapshot
  → ctx_index(content=<snapshot_text>, source="<article-slug>")  # index immediately
  → ctx_search(queries=[                                           # extract only what's needed
      "核心论点 主张",
      "验证流程 架构约束",
      "评论区 社区反馈",
      ...
    ])
  → generate analysis from search results only
```

**Why**: A single article snapshot can be 30-50KB of raw a11y tree text. Leaving it in context while generating analysis doubles or triples token consumption and crowds out reasoning capacity. In RSS/Batch mode with multiple articles, the effect compounds across every subAgent.

**Checklist before proceeding to analysis after any `take_snapshot` call:**
- [ ] `ctx_index` called with the full snapshot content?
- [ ] Analysis driven exclusively via `ctx_search` results?
- [ ] Raw snapshot NOT referenced again after indexing?

## Important Notes

### Single Article Mode Behavior
- ✅ **DO**: Output analysis directly to console
- ✅ **DO**: Detect article type first, then apply the matching template
- ✅ **DO**: Choose Short Article Direct Mode vs Standard/Strict Indexed Mode before deep analysis
- ✅ **DO**: Display results in conversation
- ✅ **DO**: Switch directly to `chrome-devtools` when login-state or anti-scraping interception is encountered
- ✅ **DO**: Read short articles/snapshots directly using Read tool
- ✅ **DO**: Use context-mode indexing for medium/long articles when direct reading would create context pressure
- ✅ **DO**: Perform Two-Pass Deep Reading using the selected strategy
- ❌ **DO NOT**: Create any markdown files
- ❌ **DO NOT**: Use Write tool
- ❌ **DO NOT**: Try `webReader`/`curl`/`fetch` retries after interception is detected
- ❌ **DO NOT**: Use context-mode for short/simple articles where direct full reading is cheaper and more complete

### RSS/Batch Mode Behavior
- ✅ **DO**: Parse RSS and show a **title-only list** first (STEP 4.5), wait for user to select articles
- ✅ **DO**: Only analyze articles the user has explicitly selected
- ✅ **DO**: Create a separate markdown file for EACH selected article
- ✅ **DO**: Include FULL detailed analysis in each file
- ✅ **DO**: Generate README.md index file
- ✅ **DO**: Default time window is past 7 days (unless user requests otherwise)
- ❌ **DO NOT**: Start analysis before user confirms which articles they want
- ❌ **DO NOT**: Analyze articles older than 7 days without explicit user request
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
- For `anthropic.com/engineering` URLs: Run `tap anthropic article --url {url}` via Bash — do NOT use chrome-devtools or context-mode
- For `baoyu.io` URLs: Run `tap baoyu article --url {url}` via Bash — do NOT use chrome-devtools or context-mode
- For other URLs: Use `ctx_fetch_and_index` + `ctx_search` (preferred) or `webReader` only when no interception appears
- If login-state/anti-scraping interception appears, switch directly to `chrome-devtools` and do NOT try other fetch methods

Step 2: Detect source/type exactly as Single Article Mode
- Run STEP 1 (source detection: Reddit vs Technical Article)
- Run STEP 2 (type detection for technical article)

Step 3: Analyze exactly as Single Article Mode
- Choose context strategy first:
  - Short/simple article → direct full reading is acceptable
  - Medium/long/noisy article → use Standard/Strict Indexed Mode with structure extraction, multi-query retrieval, exact spot checks, and coverage validation
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
