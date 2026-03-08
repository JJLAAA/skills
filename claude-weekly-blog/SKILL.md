---
name: claude-weekly-blog
description: Analyzes Claude blog posts from claude.com/blog for the current week. Triggers when users ask about "Claude blog this week", "Claude weekly articles", "latest Claude posts", "Claude 本周博客", or want to see what Claude published recently. Filters posts by Beijing time (UTC+8) for the current week (last Sunday to this Saturday), provides 20-30 character summaries in Chinese, and includes original links.
---

# Claude Weekly Blog Analyzer

Fetch and analyze Claude blog posts from https://claude.com/blog for the current week.

## When to use this skill

Use this skill when the user asks about:
- Claude blog posts this week
- Latest Claude articles or updates
- What Claude published recently
- Claude 本周博客 / 这周的博客

## Week definition

**Current week** = Last Sunday 00:00 to this Saturday 23:59 in Beijing time (UTC+8).

Calculate the date range based on today's date before fetching.

## Workflow

1. **Calculate week boundaries**
   - Determine today's date
   - Find last Sunday (start of week)
   - Find this Saturday (end of week)
   - Convert to Beijing time (UTC+8)

2. **Fetch blog page**
   - Use WebFetch to get https://claude.com/blog
   - Extract all posts with: title, publication date, URL, brief description

3. **Filter by date**
   - Parse publication dates
   - Keep only posts published within the current week range
   - If no posts match, report "本周暂无新文章发布"

4. **Generate summaries**
   - For each post, read the full article by fetching its URL
   - Write a 20-30 character Chinese summary focusing on:
     - Technical details if the post is technical
     - Application scenarios if the post is about use cases
     - Follow the emphasis of the original content
   - Keep summaries concise and informative

5. **Output format**

```
Claude 博客本周文章汇总（北京时间 YYYY-MM-DD 至 YYYY-MM-DD）

[If posts found:]
**1. [Article Title]**
- 发布日期：YYYY年MM月DD日
- 概述：[20-30字中文概述]
- 链接：https://claude.com/blog/[article-slug]

**2. [Article Title]**
...

[If no posts found:]
本周（北京时间 YYYY-MM-DD 至 YYYY-MM-DD）暂无新文章发布。
```

## Important notes

- Always calculate the week range dynamically based on current date
- Use Beijing time (UTC+8) for all date comparisons
- If a post's date is ambiguous or missing, exclude it from results
- Summaries must be in Chinese, 20-30 characters
- Do not show recent articles if none match the current week
- Include the full URL for each article