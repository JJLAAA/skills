---
name: linuxdo-news-analyzer
description: >-
  专门分析 linux.do 社区今日新闻的工具。通过 Discourse JSON API 获取带时间戳的帖子列表，
  按北京时间（UTC+8）过滤当天新闻，逐篇读取详情页并输出结构化概述。
  当用户说"分析 linux.do 今天的新闻"、"linux.do 今日快讯"或类似请求时使用。
metadata:
  author: leo
  version: "2.6"
  category: news
---

# linuxdo-news-analyzer

## Overview

专门用于分析 linux.do 社区今日新闻的 skill。核心设计原则：

- **北京时间日期过滤**：使用 Discourse JSON API 的 `created_at` 字段，按北京时间（UTC+8）判断"今天"，避免遗漏北京时间凌晨发布的帖子
- **逐篇读取详情**：每篇新闻都访问其详情 API，提取楼主正文，不只依赖列表页标题
- **结构化输出**：按分类整理，附北京时间、浏览量、回复数，最后给出今日总结
- **Token 优化**：列表页一次获取所有信息，详情页批量抓取，避免重复导航开销

## When to Use This Skill

用户说以下内容时触发：
- "分析 linux.do 今天的新闻"
- "linux.do 今日快讯"
- "看看 linux.do 前沿快讯"
- `/linuxdo-news-analyzer`

## Workflow

### STEP 1: 获取今日新闻列表（北京时间）

使用 chrome-devtools 工具打开列表页：

```
new_page("https://linux.do/c/news/34.json")
```

**关键：按北京时间过滤**

北京时间 = UTC+8，所以北京时间今天的帖子对应的 UTC 时间范围是：
- 北京时间 00:00 = UTC 前一天 16:00
- 北京时间 23:59 = UTC 当天 15:59

然后使用 evaluate_script 提取并过滤今日新闻：

```js
() => {
  const raw = document.body.innerText;
  const data = JSON.parse(raw);

  // 北京时间今天00:00对应的UTC时间（使用当前日期）
  const todayStartUTC = new Date('2026-03-08T00:00:00.000+08:00').toISOString();

  // 过滤今日帖子
  const topics = data.topic_list.topics
    .filter(t => t.created_at >= todayStartUTC)
    .map(t => ({
      id: t.id,
      title: t.title,
      created_at: t.created_at,
      posts_count: t.posts_count,
      views: t.views
    }))
    .sort((a, b) => new Date(a.created_at) - new Date(b.created_at));

  return { count: topics.length, topics };
}
```

> ⚠️ 记得将日期 '2026-03-08' 替换为当前日期

> ⚠️ 必须用 `created_at` 过滤，不能用 `bumped_at`（后者会包含有新回复的旧帖）
> ⚠️ 必须按北京时间过滤，不能直接用 UTC 日期字符串匹配，否则会漏掉北京时间凌晨（UTC前一天下午）发布的帖子

### ⏹️ 空列表检查

**如果 STEP 1 返回空列表**，直接输出以下内容并结束任务：

```
📢 今日（{YYYY-MM-DD}）linux.do 前沿快讯版块尚无新帖发布，请稍后再试。
```

**不要**显示昨天或其他时间的帖子作为备选。

### STEP 2: 批量抓取详情

使用 chrome-devtools 批量打开详情页。对于每个帖子：

1. 使用 `new_page` 或 `navigate_page` 打开详情页：
```
https://linux.do/t/topic/{id}.json
```

2. 使用 `evaluate_script` 提取数据：

```js
() => {
  const data = JSON.parse(document.body.innerText);
  const post = data.post_stream?.posts?.[0];

  if (!post) {
    return { error: 'no post', id: data.id };
  }

  const cooked = post.cooked || '';
  const text = cooked.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
  const summary = text.substring(0, 200);

  // 计算内容质量分
  let score = Math.min(text.length, 500);
  score += (cooked.match(/https?:\/\/[^\s"<>]+/g) || []).length * 50;
  score += (cooked.match(/\d+\.\d+|GPT-\d|Claude[\s-]?\d/gi) || []).length * 30;
  score += (text.match(/支持|包含|提供|可以|能够/g) || []).length * 10;

  return {
    id: data.id,
    title: data.title,
    created_at: data.created_at,
    summary,
    views: data.views,
    posts_count: data.posts_count,
    content_score: score
  };
}
```

**优化建议：**
- 可以在后台打开多个页面（使用 `background: true`）
- 避免打开过多页面导致浏览器卡顿
- 建议分批处理，每批5-8个页面

#### 重定向检测

如果返回的 `data.id` 与请求的 `topic.id` 不同，说明帖子已被重定向合并，需标记并去重：

```js
const isRedirected = data.id !== topicId;
```

### STEP 3: 智能去重与分类

⚠️ **关键要求：此步骤不可跳过！即使 subAgent 已返回数据，也必须执行去重逻辑。**

#### 去重规则（基于内容质量）

对于相似主题的帖子（如"美团AI浏览器"相关），**必须在抓取详情后比较内容质量**，而非仅看浏览量：

**去重步骤：**

1. **分组**：按标题语义相似性直接分组
   - 清理标题：去掉日期、【】等前缀
   - 对所有标题进行语义相似性判断，将描述同一事件的标题归为一组
   - 判断标准：两个标题是否在讨论同一个新闻事件（如"林俊旸卸任千问"和"通义千问负责人离职"属于同一事件）

2. **抓取后比较**：对每组相似帖子，抓取详情后比较以下指标：
   - **摘要长度**：正文长度更长通常信息更丰富
   - **信息密度**：包含具体数据（数字、版本号、链接、人名）的优先
   - **完整性**：有实际内容 vs 仅有图片/一句话

3. **选择规则**（优先级从高到低）：
   - 有实质文字内容 > 仅有图片
   - 包含具体数据（版本号、URL、数字）> 纯描述性文字
   - 正文长度更长 > 更短
   - 内容质量分更高 > 更低
   - 浏览量更高 > 更低（作为最后参考）

**示例判断：**
- "美团也加入AI浏览器大战了！现在所有功能免费使用！" - 包含产品名、功能描述、模型列表、下载链接 → **内容更丰富**
- "美团AI浏览器" - 仅有标题式描述，信息量少 → **去重时舍弃**

**真实案例（2026-03-04）：**
以下三条新闻核心实体完全一致（林俊旸、千问、卸任），必须去重：
- 1684976: "林俊旸发推称将卸任千问负责人" (content_score: 1050)
- 1685057: "通义千问Qwen核心负责人卸任" (content_score: 1090) ← **保留此条**
- 1685082: "Qwen核心负责人林俊旸非自愿离职" (content_score: 970)

**实现方式：**
在 Task 批量抓取时，为每个帖子计算内容质量分：
```js
function calculateContentScore(post) {
  const summary = post.cooked.replace(/<[^>]+>/g, ' ').trim();
  let score = 0;
  // 基础长度分
  score += Math.min(summary.length, 500);
  // 包含URL加分
  score += (summary.match(/https?:\/\/[^\s]+/g) || []).length * 50;
  // 包含版本号/数字加分
  score += (summary.match(/\d+\.\d+|GPT-\d|Claude[\s-]?\d/i) || []).length * 30;
  // 包含具体功能描述加分
  score += (summary.match(/支持|包含|提供|可以|能够/g) || []).length * 10;
  return score;
}
```

**执行去重的正确流程：**
```
1. subAgent 返回所有文章数据（含 content_score）
2. 主对话按标题语义相似性分组，识别重复主题
3. 对每组重复主题，按 content_score 降序排序
4. 保留每组中 content_score 最高的文章
5. 输出去重后的结果
```

⚠️ **常见错误：过度信任 subAgent 输出**
- ❌ 错误做法：subAgent 返回数据后直接输出，跳过去重
- ✅ 正确做法：即使 subAgent 已计算 content_score，主对话仍需执行实体提取和去重逻辑

#### 分类规则

| 分类 | emoji | 关键词示例 |
|------|-------|-----------|
| 地缘政治 | 🌏 | 战争、领袖、制裁、外交、空袭 |
| AI / 科技 | 🤖 | AI、模型、OpenAI、Anthropic、Claude、Grok、Qwen、GPT |
| 商业动态 | 💰 | 收入、财报、融资、收购、市值 |
| 安全漏洞 | 🔐 | 漏洞、入侵、CVE、修复、黑客 |
| 产品发布 | 📱 | 发布、上线、更新、新款、推出 |
| 政策法规 | 🏛️ | 禁止、法案、监管、政策、封锁 |
| 奇闻趣事 | 😄 | 慢慢讯、奇葩、搞笑、意外 |
| 其他 | 🌍 | 不属于以上分类 |

### STEP 4: 输出结构化分析

直接在对话中输出，不创建文件。

#### 时间格式

- 显示**北京时间**（CST）：`new Date(created_at).toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai', hour: '2-digit', minute: '2-digit' })`
- 格式：`HH:MM CST`

#### 输出模板

```markdown
# 今日前沿快讯详情概述 - {YYYY-MM-DD}（北京时间）

---

## {emoji} {分类名}（N条）

**{序号}. {标题}** `{HH:MM CST}` | 浏览 {views} | 回复 {posts_count}
> {100字以内概述，保留关键事实：人名、数字、机构名}
> 🔗 [原帖链接](https://linux.do/t/topic/{id})

---

## 💎 今日总结

{3-5句话，提炼今日主要主题和关键洞察}
```

## Token 优化总结

| 优化点 | 原方案 | 优化后 | 节省 |
|--------|--------|--------|------|
| 日期过滤 | UTC 日期字符串匹配 | 北京时间换算后过滤 | 避免漏帖 |
| 详情抓取 | 主对话循环 navigate_page | chrome-devtools 批量抓取 | 减少导航开销 |
| 摘要长度 | 300 字符 | 200 字符 | 减少输出开销 |
| 同主题帖子 | 全部抓取后去重 | 列表页去重后再抓取 | 减少请求数 |

## Important Notes

- ✅ 按北京时间（UTC+8）过滤，避免遗漏凌晨发布的帖子
- ✅ 每篇必须读取详情页，不能只用列表标题
- ✅ 概述保留关键事实，不做主观评价
- ✅ 输出直接在对话中展示，不创建 markdown 文件
- ✅ 显示北京时间（CST）而非 UTC 时间
- ✅ **STEP 3 去重逻辑不可跳过**：即使 subAgent 已返回数据，主对话仍需执行核心实体提取和去重
- ✅ 同主题多帖保留内容质量最高的（有实质内容、含具体数据、正文更长）
- ✅ 检测重定向，跳过重复内容
- ❌ 不用 `bumped_at` 作为过滤条件
- ❌ 今日无新帖时，不显示其他日期的帖子作为备选
- ❌ **禁止过度信任工具输出**：不要因为 subAgent 返回了结构化数据就跳过业务逻辑验证
- ❌ **永远不要使用 WebFetch 工具**：linux.do 需要登录态，WebFetch 无法访问，只会超时浪费 token
- ❌ **永远不要使用 bash curl 命令**：linux.do 需要登录态，curl 无法获取内容，只会浪费 token
- ❌ **唯一正确的方式**：使用 chrome-devtools 工具（new_page + evaluate_script），因为浏览器有登录态

## Troubleshooting

- **API 返回空列表**：今日尚无新帖发布，直接输出提示信息并结束任务
- **JSON 解析失败**：linux.do 可能需要登录，尝试截图查看页面状态
- **帖子正文为空**：部分帖子只有图片无文字，标注"（楼主仅附图）"
- **重定向频繁**：多个帖子重定向到同一内容时，说明论坛正在合并帖子，保留最终内容即可
- **时间显示错误**：确保使用 `timeZone: 'Asia/Shanghai'` 转换北京时间
- **WebFetch 或 curl 超时**：这是预期行为，因为 linux.do 需要登录态。必须使用 chrome-devtools 工具

## 更新日志

### v2.6 (2026-03-08)
- **关键说明**：明确禁止使用 WebFetch 和 curl 工具访问 linux.do
- **原因**：linux.do 需要登录态，这两个工具无法访问，只会超时浪费 token
- **唯一正确方式**：使用 chrome-devtools 工具（new_page + evaluate_script）
- 更新 Important Notes 和 Troubleshooting 部分

### v2.5 (2026-03-08)
- **重要修复**：移除 WebFetch 工具（容易超时）
- **重要修复**：移除 bash curl 命令（网络请求无响应）
- 改用 chrome-devtools 工具直接打开 JSON API 页面
- 使用 evaluate_script 提取和处理 JSON 数据
- 优化批量抓取策略：支持后台打开多个页面，分批处理

### v2.4 (2026-03-06)
- **重大优化**：将数据获取方式从 chrome-devtools 改为 WebFetch
- 使用 WebFetch 直接获取 JSON API，无需浏览器渲染
- 配合 context-mode 的 execute 工具处理 JSON 数据
- 显著提升性能，减少 token 消耗

### v2.3 (2026-03-04)
- **优化去重逻辑**：改用语义相似性直接分组，移除程序化实体识别
- 简化分组步骤：直接判断标题是否描述同一事件，而非提取实体后比对
- 提升去重准确性：基于语义理解而非关键词匹配

### v2.2 (2026-03-04)
- **关键修复**：强制执行 STEP 3 去重逻辑，禁止跳过
- 新增核心实体提取方法，识别人名、公司名、产品名
- 新增真实案例说明（林俊旸卸任事件去重示例）
- 新增"常见错误"警告：过度信任 subAgent 输出
- 更新 Important Notes：明确标注去重步骤不可跳过

### v2.1 (2026-03-03)
- 优化去重逻辑：基于内容质量（摘要长度、信息密度、具体数据）而非仅看浏览量
- 提供内容质量评分函数，优先保留信息更丰富的文章

### v2.0 (2026-03-03)
- 修正日期过滤逻辑：按北京时间（UTC+8）判断"今天"
- 优化详情抓取：使用单 Task 批量抓取替代主对话循环
- 更新输出格式：显示北京时间（CST）
- 增加商业动态分类

### v1.2 (2026-03-02)
- 初始版本
