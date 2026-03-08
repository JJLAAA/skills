---
name: openai-weekly-blog
description: Analyzes OpenAI's weekly blog posts from their RSS feed. Triggers when users ask about "OpenAI blog this week", "OpenAI weekly articles", "latest OpenAI Research/Engineering posts", "OpenAI 本周博客", or want to see what OpenAI published recently. Filters for Research and Engineering categories only, provides 20-30 character summaries in Chinese, and covers the current week (last Sunday to this Saturday, Beijing time).
---

# OpenAI Weekly Blog Analyzer

Fetch and analyze OpenAI's blog posts from the current week, focusing on Research and Engineering articles.

## What this skill does

1. Fetches OpenAI's RSS feed from https://openai.com/news/rss.xml
2. Filters articles published this week (last Sunday 00:00 to this Saturday 23:59, Beijing time UTC+8)
3. Only includes articles with category "Research" or "Engineering"
4. Generates a 20-30 character Chinese summary for each article
5. Outputs formatted list with title, category, publish time, summary, and link

## Time range calculation

The "current week" is defined as:
- Start: Last Sunday at 00:00:00 Beijing time
- End: This Saturday at 23:59:59 Beijing time

Use the current date to calculate these boundaries. For example, if today is Monday March 9, 2026, the week runs from Sunday March 2 to Saturday March 8.

## Implementation approach

1. Run `scripts/fetch_weekly.js` to get this week's articles as JSON
2. For each article, generate a 20-30 character Chinese summary based on the title and description
3. Format and present the results

The script handles RSS fetching, XML parsing, time filtering, and category filtering. It outputs JSON with articles array and week boundaries.

## Output format

Present results in Chinese with this structure:

```
找到本周（3月2日-3月8日，北京时间）OpenAI 的 X 篇 Research/Engineering 文章：

**1. [Article Title]**
   - 分类: Research
   - 发布时间: 2026年3月5日
   - 概述: [20-30 character summary in Chinese]
   - 链接: https://...

**2. [Article Title]**
   ...
```

If no articles found this week, inform the user and optionally show the most recent Research/Engineering articles from previous weeks.

## Example output

```
找到本周（3月2日-3月8日，北京时间）OpenAI 的 2 篇 Research 文章：

**1. Reasoning models struggle to control their chains of thought, and that's good**
   - 分类: Research
   - 发布时间: 2026年3月5日
   - 概述: 介绍推理模型思维链控制研究，探讨控制难度的价值
   - 链接: https://openai.com/index/...

**2. Extending single-minus amplitudes to gravitons**
   - 分类: Research
   - 发布时间: 2026年3月4日
   - 概述: 将单负振幅扩展到引力子的物理学研究预印本
   - 链接: https://openai.com/index/...
```