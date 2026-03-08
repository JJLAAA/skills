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
     - Reddit Mode: Use chrome-devtools or webReader to fetch body + Top 5 comments
     - Technical Article Mode: Use webReader to fetch body only (clean content)

2. **When input is direct content:**
   - Check for Reddit features: "upvote", "comment thread", "u/" prefix → **Reddit Mode**
   - No features → **Technical Article Mode**

3. **Exception handling:**
   - 404/empty content → Return: `ERROR: Content fetch failed [URL]`
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

### STEP 3: Generate Analysis & Console Output

**All outputs are in Chinese. Preserve English technical terms (e.g., `PagedAttention`, `vLLM`). Output directly to console — DO NOT use Write tool.**

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

## 核心论点拆解

### 论点 1：[论点名称]
- **主张**：作者认为...
- **论据**：
  - [列出支撑该论点的具体证据、数据、案例]
- **推理逻辑**：[强/中/弱] — [解释为什么给出这个评价]

### 论点 2：...
（重复上述结构，通常 3-6 个核心论点）

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
2. **区分事实和观点**：明确标注哪些是文章中的事实陈述，哪些是作者的主观判断。
3. **建设性批评**：指出问题时给出具体理由，不要空洞地说"论证不够充分"。
4. **公允**：如果作者的论证确实扎实，就说扎实。不要为了显得"有深度"而强行找茬。
5. **聚焦价值**：行动建议要具体可执行，不要写"可以进一步研究"这种空话。

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

First, confirm the time range with user:
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

Launch subAgents one at a time in FOREGROUND mode to avoid permission issues:

```
# SubAgent Template for Each Group:

Agent(
    subagent_type="general-purpose",
    description="分析第 [start]-[end] 篇文章并导出详细 markdown",
    run_in_background=false,  # FOREGROUND execution to allow permission requests
    prompt="""You are a technical article analyzer. Analyze the following articles and create detailed markdown files for each.

OUTPUT DIRECTORY: /Users/leo/projects/[blog-name]-analysis-[YYYYMMDD]/

ARTICLES TO ANALYZE (Group [X] of [total]):
1. [Article Title]
   URL: [url]
   Target file: [number]-[slug].md

2. [Article Title]
   URL: [url]
   Target file: [number]-[slug].md

[... continue for all articles in this group ...]

CRITICAL INSTRUCTIONS - Use the SAME analysis methodology as Single Article Mode:

For EACH article:

Step 1: Fetch and index article content
- Use ctx_fetch_and_index(url="[article-url]", source="Article: [title]")
- Returns ~3KB preview, full content indexed

Step 2: Extract key information using ctx_search
- ctx_search(queries=["article structure and main points", "technical details and metrics", "author arguments and evidence"], source="Article: [title]", limit=5)

Step 3: Identify article type (SAME as Single Article Mode STEP 2)
Determine which type:
- **技术观点文**: 提出明确主张、有对比论证
- **教程/实操文**: 分步骤指引、有代码示例
- **经验分享文**: 项目复盘、踩坑记录
- **工具介绍文**: 功能介绍、使用方法

Step 4: Generate analysis using type-specific template (SAME as Single Article Mode STEP 3)

For 技术观点文, use this template:
```markdown
## 文章元信息
- 标题：
- 作者：
- 发表时间：
- 原文链接：

## 一句话总结

## SCQA 脉络
- **Situation（情境）**：
- **Complication（冲突）**：
- **Question（问题）**：
- **Answer（答案）**：

## 核心论点拆解
### 论点 1：[论点名称]
- **主张**：
- **论据**：
- **推理逻辑**：[强/中/弱]

## 关键数据与证据

## 批判性评价
### 论证强项
### 论证弱项 / 可商榷之处
### 被忽略的视角

## 适用边界
- **成立条件**：
- **不成立条件**：

## 行动建议
- **可以立即应用的点**：
- **需要进一步验证的点**：

## 延伸思考
```

For 教程/实操文:
```markdown
## 文章元信息
## 一句话总结
## 知识结构
- **目标**：
- **前置知识**：
- **核心步骤**：
- **关键产出**：
## 技术要点
## 实操可行性评估
## 行动建议
```

For 经验分享文:
```markdown
## 文章元信息
## 一句话总结
## 背景与上下文
## 核心经验提炼
### 经验 1：
- **内容**：
- **支撑案例**：
- **可迁移性**：
## 批判性评价
## 行动建议
```

For 工具介绍文:
```markdown
## 文章元信息
## 一句话总结
## 工具概览
## 优劣势分析
## 适用场景
## 同类对比
## 行动建议
```

Step 5: Export to markdown file
- Write(file_path="[OUTPUT_DIRECTORY]/[target-file]", content="[complete analysis]")

Step 6: Move to next article

COMPLETION:
After analyzing ALL articles in your group:
1. List all files you created
2. Provide a 2-3 sentence summary of key themes

Start with the first article!
"""
)
```

**Step 5.3: Wait for each subAgent to complete**
- SubAgents run in foreground (sequential execution)
- Each completes before the next starts
- Retrieve results after each completion

**Step 5.4: Consolidate and verify**
- Verify all markdown files were created
- Check that each file contains complete analysis
- Create README.md index file with complete article listing

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
- ⚠️ **Each markdown file must be COMPLETE** with all required sections
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
- Same 5-section structure as console output

### Individual Article File Template

Each article analysis file MUST follow this exact structure:

```markdown
# [Article Title]

## 📌 Content Overview

- **标题**: [Cleaned accurate title]
- **技术领域**: [e.g., LLM 推理/编译器优化/分布式系统]
- **内容类型**: [Reddit 帖子/技术文章] + [源语言→输出语言]
- **发布日期**: [Date]
- **原文链接**: [URL]

## 📑 Detailed Outline

### Core Sections (X%)

- **一级标题**: Summary with technical details
  - 🔥 **二级标题**: [Key Solution] + **Quantitative Metrics** (e.g., "延迟↓42%", "吞吐量↑3x")
  - **二级标题**: Supporting evidence summary

[Continue with all major sections...]

## 💎 Core Summary

[100±10 words in Chinese, preserving English technical terms]

Example: 🔥 [突破性技术] 通过[方法]达成[指标]，解决[场景]瓶颈。

## ⚙️ Deep Analysis

Apply the 7-Layer Framework to extract structured insights:

### 🎯 Layer 1: Problem Space
- **核心问题**: [Problem definition]
- **现有方案局限**: [Limitations]
- **目标场景**: [Use cases]

### 🏗️ Layer 2: Architecture Design
- **架构模式**: [Pattern name]
- **核心组件**: [Key components]
- **设计权衡**: [Trade-offs]

### 🔧 Layer 3: Implementation
- **[Tech Name]** | 位置 [Section%]
  [Principle + Metrics]

  Example: **PagedAttention** | 位置 [35-50%]
  通过虚拟内存分页管理KV cache，显存利用率提升至95%+

### 📊 Layer 4: Quality Assurance
- **评估方法**: [Evaluation approach]
- **关键指标**: [Metrics with values]

### 🚀 Layer 5: Production Engineering
- **可靠性保障**: [Reliability mechanisms]
- **部署策略**: [Deployment approach]

### 💡 Layer 6: Experience Distillation
- **最佳实践**: [Best practices]
- **反模式**: [Anti-patterns]

### 🔗 Layer 7: Cross-domain Connections
- **相关技术对比**: [Comparisons]
- **适用边界**: [When to use]

*Note: Only include layers with substantial content. Skip layers lacking information.*

## 🌟 Unique Value

[Location] [Tech Name]: [Breakthrough point] + **Verification Data**

Only include this section if there are genuine breakthrough innovations.

**原文标签**: #tag1 #tag2
**生成时间**: [timestamp]
**分析工具**: web-tech-article-analyzer
```

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
2. **Location marking**:
   - Sections: Use percentage ranges ([25-40%])
   - Reddit comments: Mark `[评论区: Top N]`
3. **Anti-redundancy**:
   - Non-Reddit content: Hide all 💬/✅/⚠️ fields
   - Basic concept sections: 1-line summary only
4. **Termination conditions**:
   - Cannot identify type → `ERROR: Cannot identify content source [input summary]`
   - Insufficient value density (pure discussion) → Output outline + core summary only

## Available Tools

### Single Article Mode
- **mcp__web_reader__webReader**: Primary tool for fetching article content as markdown (use first)
- **mcp__chrome-devtools***: Fallback for webReader, required for Reddit content with comments
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
- **Write**: For creating markdown files with article analysis (used by subAgents)

## Tool Selection Strategy

### URL Type Detection (STEP 0)
1. **For RSS feed detection**: Use `scripts/rss_parser.py` to check for RSS feeds in homepage
2. **For URL pattern matching**: Check for `/rss`, `/feed`, `.xml`, `atom.xml` patterns

### Single Article Mode
1. **For Reddit URLs**: Use `chrome-devtools` to navigate and capture full content including comments
2. **For technical articles**: Use `webReader` with markdown format for clean content extraction
3. **For content already provided**: Skip fetching, proceed directly to analysis

### RSS/Batch Mode
1. **For RSS feed parsing**: Use `scripts/rss_parser.py` to parse feed and extract articles
2. **For article fetching**: subAgents use `webReader` for each article
3. **For parallel processing**: Use TaskTool to launch multiple subAgents

## Important Notes

### Single Article Mode Behavior
- ✅ **DO**: Output analysis directly to console
- ✅ **DO**: Detect article type first, then apply the matching template
- ✅ **DO**: Display results in conversation
- ❌ **DO NOT**: Create any markdown files
- ❌ **DO NOT**: Use Write tool

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
- Complete Detailed Outline with all major sections
- Core Summary of 100±10 words
- Deep Analysis for all key technical points
- Unique Value section (only if applicable)

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

Step 1: Fetch the article content
- Use webReader with url="[article-url]" and return_format="markdown"
- If webReader fails, use chrome-devtools to navigate and take_snapshot

Step 2: Generate complete analysis following this structure:

# [Article Title]

## 📌 Content Overview

- **标题**: [Article title]
- **技术领域**: [e.g., LLM 推理/编译器优化/分布式系统]
- **内容类型**: 技术文章 [EN→ZH]
- **发布日期**: [Date from article]
- **原文链接**: [Article URL]

## 📑 Detailed Outline

### Core Sections

[Break down the article into major sections. For each section:
- Provide a brief summary
- Mark key insights with 🔥
- Include quantitative metrics when available]

[Continue with ALL major sections from the article...]

## 💎 Core Summary

[Write 100±10 words in Chinese that summarize the key insights.
Preserve English technical terms like PagedAttention, vLLM, etc.
Format: 🔥 [突破点] 通过[方法]达成[指标]，解决[场景]问题。]

## ⚙️ Deep Analysis

[For each key technology or concept mentioned:
- **[Tech Name]** | 位置 [Section%]
  [Explain the principle, implementation details, and metrics]

Include 3-5 key technologies with specific details.]

## 🌟 Unique Value

[Only if there are genuine breakthrough innovations:
[Location] [Tech Name]: [Breakthrough point] + **Verification Data**

If no unique value identified, write: 本文未发现突破性创新，但提供了有价值的技术实践和行业观察。]

**原文标签**: #tag1 #tag2 #tag3
**生成时间**: [current timestamp]
**分析工具**: web-tech-article-analyzer

Step 3: Export to markdown file
- Use Write tool with file_path="[OUTPUT_DIRECTORY]/[target-file]"
- Paste the complete analysis content
- Verify the file was created successfully

Step 4: Move to next article
- Process all articles sequentially
- Do not skip any articles

COMPLETION:
After analyzing ALL articles in your group:
1. List all files you created
2. Provide a 2-3 sentence summary of key themes across your articles

Start now with the first article!
```
