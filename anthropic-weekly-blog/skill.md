# Anthropic Weekly Blog Analyzer

Analyzes Anthropic engineering blog posts from the current week and generates detailed technical analysis reports.

## Workflow

1. **Fetch article list** via `tap anthropic articles` (returns structured JSON with title, summary, date, url)
2. **Filter this week's posts** by date field (Sunday to today)
3. **Exit early** if no posts found
4. **Create parallel tasks** using TaskCreate for each article
5. **Analyze each article** using web-tech-article-analyzer skill
6. **Compile results** into a single markdown file with independent analyses

## Output

Single markdown file: `anthropic-weekly-YYYY-MM-DD.md` containing all article analyses.

## Trigger Phrases

- "分析本周 Anthropic 博客"
- "Anthropic weekly blog"
- "本周 Anthropic 工程博客"

## Gotchas

⚠️ **必须严格筛选发布时间为本周的文章**

1. **Featured ≠ 本周发布**: `tap` 返回的文章按页面顺序排列，Featured 文章可能发布于几周前。必须检查每篇文章的 `date` 字段，而不是依据排列顺序判断。

2. **没有就是没有**: 如果本周（周日至今天）没有新文章，直接输出"本周无新文章"，**不要分析过期文章**。

3. **日期判断标准**:
   - 本周 = 周日 00:00 至今天 23:59
   - `date` 字段格式为 "Mon DD, YYYY"（如 "Apr 23, 2026"）
   - 只统计明确在日期范围内的文章
