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
