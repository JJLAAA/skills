# CLI Args Reference

`args` 定义用户在 `tap <site> <command>` 后可以传入的参数。保持参数少而明确，只暴露用户确实需要调节的选项。

## 基本结构

```js
args: [
  {
    name: 'limit',
    default: 20,
    description: 'Maximum number of items to return.',
  },
  {
    name: 'keyword',
    default: '',
    description: 'Search keyword.',
  },
]
```

## 命名约定

- 使用 camelCase：`limit`、`keyword`、`categoryId`、`pageSize`。
- 数字参数带清晰单位或语义：`pageSize`、`maxPages`、`minScore`。
- 不暴露上游 API 的含糊字段名，如 `ps`、`pn`、`rid`；改成业务名，并在 URL 映射时转换。

## 常用参数

| 参数 | 默认值 | 用途 |
|------|--------|------|
| `limit` | `20` | 最终返回条数，通常 pipeline 最后加 `{ limit: '${{ args.limit }}' }` |
| `keyword` | `''` | 搜索词 |
| `category` | 站点默认分类 | 分类 slug 或名称 |
| `categoryId` | 站点默认 ID | 上游 API 只接受 ID 时使用 |
| `page` | `1` | 单页接口页码 |
| `pageSize` | `20` 或 `50` | 请求每页数量 |
| `maxPages` | `1` 到 `3` | 多页抓取上限，避免无限请求 |

## 设计规则

- `limit` 控制最终输出，不一定等于 API 的 `pageSize`。
- 搜索、分类、时间范围等参数要在 `description` 里说明来源和格式。
- 如果 runtime 支持类型、必填、choices 等扩展，优先使用；不确定时只写 `name`、`default`、`description`，并用验证命令确认。
- 不把 cookie、token、app secret 写成 args；这类值应来自浏览器登录态、环境变量或本地配置。

## URL 映射示例

```js
args: [
  { name: 'keyword', default: '', description: 'Search keyword.' },
  { name: 'pageSize', default: 20, description: 'Items requested per API page.' },
  { name: 'limit', default: 20, description: 'Maximum number of items to return.' },
],
pipeline: [
  { fetch: 'https://api.example.com/search?q=${{ args.keyword }}&size=${{ args.pageSize }}' },
  { select: 'data.items' },
  { map: {
    title: '${{ item.title }}',
    url: '${{ item.url }}',
  }},
  { limit: '${{ args.limit }}' },
]
```
