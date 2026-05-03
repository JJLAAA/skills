# Pipeline Steps Reference

本文件只补充会影响 adapter 是否能写对的运行时细节。优先按这里确认参数形态，再回到 `patterns.md` 套模板。

## 通用约定

- 每个 step 接收当前 `data`，输出会成为下一步的 `data`，除非该 step 只写入 `as`。
- 支持 `as` 的 step 会把结果保存到 `state.<name>`；是否同时改变当前 `data` 以 runtime 实际行为为准，后续读取命名结果时显式用 `from`。
- 模板表达式使用 `${{ ... }}`，可读取 `args`、`data`、`state`，在数组上下文可读取 `item` 和 `index`。
- 对不确定的输出形态，先运行 `tap <site> <command> --format json` 验证，不要靠字段名猜。

## Step 参数表

| Step | Params | 常用字段 | 输出 |
|------|--------|----------|------|
| `fetch` | URL 字符串或对象 | `url`, `as`, `method`, `headers`, `body` | JSON 响应 |
| `browserFetch` | 对象 | `url`, `as`, `method`, `headers`, `body`, `credentials` | 浏览器上下文中的 JSON 响应 |
| `navigate` | URL 字符串 | 无 | 通常不改变 `data` |
| `evaluate` | JS 字符串或对象 | `code`, `as` | JS 返回值 |
| `intercept` | 对象 | `capture`, `trigger`, `timeout`, `select`, `as` | 捕获的 JSON；匹配多个请求时可能是数组 |
| `select` | 路径字符串或对象 | `from`, `path`, `as` | 选中的子结构 |
| `map` | 对象 | `select` 加输出字段 | 对象数组 |
| `mapOne` | 对象 | 输出字段 | 单个对象，常用于 `foreach.steps` |
| `foreach` | 对象 | `from`, `as`, `concurrency`, `steps` | 嵌套步骤收集后的数组 |
| `filter` | JS 表达式字符串 | 无 | 过滤后的数组 |
| `sort` | 字段字符串或对象 | `by`, `order` | 排序后的数组 |
| `limit` | 数字或模板字符串 | 无 | 截断后的数组 |

## 参数细节

### fetch / browserFetch

```js
{ fetch: 'https://api.example.com/items?size=${{ args.limit }}' }
{ fetch: {
  url: 'https://api.example.com/search',
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ keyword: '${{ args.keyword }}' }),
  as: 'searchResult',
}}
```

- `fetch` 适合公开 API；`browserFetch` 适合需要 cookie 的 API，通常先 `navigate`。
- `browserFetch.credentials` 默认按浏览器登录态处理；需要明确时写 `credentials: 'include'`。
- POST body 优先保持为上游 API 实际需要的格式，不在 adapter 里重构复杂业务逻辑。

### select

```js
{ select: 'data.items' }
{ select: { from: 'searchResult', path: 'data.items', as: 'items' } }
```

- `path` 使用点号路径，数组下标写成 `0`、`1`。
- 从命名状态读取时使用 `from`，不要假设当前 `data` 仍然是之前的结果。

### foreach

```js
{
  foreach: {
    from: 'items',
    as: 'details',
    concurrency: 5,
    steps: [
      { fetch: { url: 'https://api.example.com/items/${{ item.id }}' } },
      { mapOne: { title: '${{ item.title }}', status: '${{ data.status }}' } },
    ],
  },
}
```

- `item` 是当前遍历项；`data` 是嵌套步骤内的当前结果。
- `concurrency` 用小值开始，避免触发站点限流；常用 `3` 到 `5`。

### intercept

```js
{ intercept: {
  capture: '/api/ranking',
  trigger: 'navigate:https://example.com/ranking',
  timeout: 10,
  select: 'data.list',
}}
```

- `capture` 用 URL 子字符串匹配，越精确越好。
- `trigger` 可用 `navigate:<url>`、`click:<selector>`、`scroll`、`evaluate:<js>`。
- 如果捕获到多个响应，先验证返回结构，再决定是否加 `select` 或后续 `map`。

## 验证要点

- `schema.properties` 必须与 `output.fields` 对齐。
- `items` 只能包含已声明字段。
- `limit`、分页、搜索词等 args 至少各跑一个非默认值。
