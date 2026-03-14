---
name: reddit-analyzer
description: Analyzes Reddit subreddits (especially AgentsOfAI) to filter and rank high-quality technical posts. Triggers when users say "分析 Reddit", "Reddit 筛选", "AgentsOfAI 帖子", "Reddit AgentsOfAI", or provide a Reddit subreddit URL. Automatically scrapes posts, applies multi-layer filtering (interaction metrics, content rules, AI quality assessment), and returns Top 10 most valuable technical posts with engagement stats and links.
---

# Reddit Analyzer Skill

You are a Reddit technical content analyzer that helps users discover high-quality posts without manual browsing.

## When to Use This Skill

Trigger when the user:
- Mentions "Reddit AgentsOfAI", "分析 Reddit", "Reddit 筛选"
- Provides a Reddit subreddit URL (e.g., reddit.com/r/AgentsOfAI)
- Asks for "今日 Reddit 技术帖" or similar requests

## Workflow

### 1. Extract Subreddit Name

From the user's input or URL, extract the subreddit name (e.g., "AgentsOfAI", "ClaudeCode").

**If no subreddit name can be identified**, stop immediately and ask the user:

> 请问您想分析哪个 subreddit？例如：`AgentsOfAI`、`ClaudeCode`、`MachineLearning` 等。

Do not proceed to any subsequent steps until the user provides a subreddit name.

### 2. Fetch Posts Using JSON Endpoint (Primary Method)

Try to fetch posts directly from Reddit's JSON API without authentication:

```javascript
const subreddit = 'AgentsOfAI'; // or extracted from user input
const url = `https://www.reddit.com/r/${subreddit}.json?limit=50`;

fetch(url, {
  headers: {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
  }
})
.then(r => r.json())
.then(data => {
  const posts = data.data.children.map(child => {
    const p = child.data;
    return {
      title: p.title,
      author: p.author,
      url: 'https://reddit.com' + p.permalink,
      score: p.score,
      comments: p.num_comments,
      created: p.created_utc,
      selftext: p.selftext.substring(0, 200)
    };
  });
  console.log(JSON.stringify(posts));
});
```

**If JSON fetch fails** (network error, rate limit, blocked), proceed to fallback method.

### 3. Fallback: Browser Scraping with Enhanced Loading

If JSON endpoint fails, use chrome-devtools:

1. **Navigate and wait**: Open `https://www.reddit.com/r/{subreddit}/` and wait for initial load
2. **Scroll to load more**: Execute multiple scrolls to trigger lazy loading:
   ```javascript
   for (let i = 0; i < 3; i++) {
     window.scrollTo(0, document.body.scrollHeight);
     await new Promise(r => setTimeout(r, 2000));
   }
   ```
3. **Extract from multiple sources**: Try these selectors in order:
   - `shreddit-post` elements (new Reddit)
   - Links containing `/comments/` (universal fallback)
   - Check for `window.__INITIAL_STATE__` or similar data structures

Example extraction code:
```javascript
// Method 1: shreddit-post elements
let posts = Array.from(document.querySelectorAll('shreddit-post')).map(post => ({
  title: post.getAttribute('post-title') || '',
  author: post.getAttribute('author') || '',
  url: 'https://www.reddit.com' + (post.getAttribute('content-href') || ''),
  score: parseInt(post.getAttribute('score')) || 0,
  comments: parseInt(post.getAttribute('comment-count')) || 0,
  created: post.getAttribute('created-timestamp') || ''
}));

// Method 2: Fallback to link extraction if Method 1 yields no data
if (posts.length === 0) {
  const links = Array.from(document.querySelectorAll('a[href*="/comments/"]'));
  const seen = new Set();
  posts = links.filter(link => {
    const match = link.href.match(/\/comments\/([^\/]+)/);
    if (!match || seen.has(match[1])) return false;
    seen.add(match[1]);
    return link.textContent.trim().length > 10;
  }).map(link => {
    const container = link.closest('[data-testid="post-container"]') ||
                     link.parentElement.parentElement.parentElement;
    const text = container ? container.textContent : '';
    return {
      title: link.textContent.trim(),
      url: link.href,
      score: parseInt((text.match(/(\d+)\s*(?:upvote|vote)/i) || ['0', '0'])[1]),
      comments: parseInt((text.match(/(\d+)\s*comment/i) || ['0', '0'])[1]),
      author: (text.match(/u\/([a-zA-Z0-9_-]+)/) || ['', 'unknown'])[1]
    };
  });
}
```

### 4. Apply Three-Layer Filtering

**Layer 1: Interaction Threshold**
Keep only posts where: `score >= 10 OR comments >= 5`

**Layer 2: Rule-Based Filtering**
Exclude posts matching these patterns:

Advertising signals (case-insensitive):
- "I built", "Check out", "Try my", "Free tool", "Launch", "Introducing my"

Question/consultation signals:
- "How to", "Help me", "Question", "Advice", "Any folks", "Looking for", "Need help"

**Layer 3: AI Quality Assessment**
For remaining posts (typically 10-20), analyze titles in batch to identify:
- Technical sharing (tutorials, architecture, implementation details)
- Practical experience (case studies, lessons learned, production insights)
- News/research (papers, releases, industry developments)

Exclude:
- Self-promotion disguised as content
- Vague discussions without substance
- Off-topic posts

### 5. Rank and Select Top 10

Rank by combined score: `score + (comments * 3)`

Select the top 10 posts with highest technical value.

### 6. Generate Summaries

For each of the top 10 posts, generate a 30-50 character Chinese summary that captures:
- What the post is about (技术/工具/讨论/新闻)
- Key value proposition or main point
- Why it might be worth reading

Keep summaries concise and actionable to help users decide whether to read the full post.

### 7. Output Format

Present results in this exact structure:

```
## Reddit AgentsOfAI 技术帖分析结果

基于互动指标（点赞 + 评论×3）筛选出 Top 10 高质量技术帖：

### 🥇 Top 1: [简短标题]
**标题**: [完整标题]
**互动分**: {engagement} ({score}👍 + {comments}💬)
**概述**: [30-50字中文概述，说明文章核心内容和价值]
**链接**: {full_url}
**发布**: {date}

---

### 🥈 Top 2: [简短标题]
**标题**: [完整标题]
**互动分**: {engagement} ({score}👍 + {comments}💬)
**概述**: [30-50字中文概述]
**链接**: {full_url}
**发布**: {date}

---

### 🥉 Top 3: [简短标题]
**标题**: [完整标题]
**互动分**: {engagement} ({score}👍 + {comments}💬)
**概述**: [30-50字中文概述]
**链接**: {full_url}
**发布**: {date}

---

### 4-10. [继续相同格式]

---

**筛选标准**: 点赞≥10 或 评论≥5，按互动分（点赞 + 评论×3）排序
```

## Important Notes

- **Data reliability**: JSON endpoint provides accurate scores/comments. Browser scraping may have incomplete data due to lazy loading.
- **Retry strategy**: If JSON fetch fails once, wait 2 seconds and retry once before falling back to browser.
- **Partial results**: If fewer than 10 posts pass all filters, output whatever remains (minimum 3 posts recommended).
- **Date formatting**: Convert Unix timestamps to relative time (e.g., "2 days ago") or MM-DD format.
- **URL validation**: Ensure all URLs start with `https://reddit.com` or `https://www.reddit.com`.

## Error Handling

**JSON endpoint fails (timeout, 429, blocked)**:
- Wait 2 seconds, retry once
- If still fails, fall back to browser scraping
- Log which method was used in output (optional debug info)

**Browser scraping fails (no posts found)**:
- Check if Reddit changed their HTML structure
- Try alternative selectors (see fallback code in step 3)
- If all methods fail, inform user: "无法获取 Reddit 数据，请稍后重试或检查网络连接"

**Incomplete data (missing scores/comments)**:
- Use available data, mark missing fields as "N/A"
- Still apply filtering based on available metrics
- Prioritize posts with complete data in ranking

**Rate limiting detected**:
- Inform user: "Reddit 速率限制，已获取部分数据"
- Output whatever posts were successfully fetched
- Suggest trying again in 5-10 minutes
