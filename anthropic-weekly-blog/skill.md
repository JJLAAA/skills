# Anthropic Weekly Blog Analyzer

Analyzes Anthropic engineering blog posts from the current week and generates detailed technical analysis reports.

## Workflow

1. **Filter this week's posts** from https://www.anthropic.com/engineering (Sunday to today)
2. **Exit early** if no posts found
3. **Create parallel tasks** using TaskCreate for each article
4. **Analyze each article** using web-tech-article-analyzer skill
5. **Compile results** into a single markdown file with independent analyses

## Output

Single markdown file: `anthropic-weekly-YYYY-MM-DD.md` containing all article analyses.

## Trigger Phrases

- "分析本周 Anthropic 博客"
- "Anthropic weekly blog"
- "本周 Anthropic 工程博客"

## Gotchas

⚠️ **必须严格筛选发布时间为本周的文章**

1. **Featured ≠ 本周发布**: 博客首页的 Featured 文章只是置顶，可能发布于几周甚至几个月前。必须检查每篇文章的具体发布日期（格式如 "Mar 06, 2026"），而不是依据 Featured 标签判断。

2. **没有就是没有**: 如果本周（周日至今天）没有新文章，直接输出"本周无新文章"，**不要分析过期文章**。这浪费 token 且误导用户。

3. **日期判断标准**:
   - 本周 = 周日 00:00 至今天 23:59（北京时间或当地时区）
   - 文章日期格式通常为 "Mar 06, 2026" 或 "January 21, 2026"
   - 只统计明确标注发布日期的文章

4. **典型错误案例**: 看到 Featured 文章就假设是本周发布，结果浪费大量 token 分析了一篇两周前的文章。
