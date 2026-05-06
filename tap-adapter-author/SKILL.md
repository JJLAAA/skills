---
name: tap-adapter-author
description: Use when writing a TAP adapter for a new site or command. Guides from reconnaissance through pipeline assembly, installation, and verification.
allowed-tools: Bash, Read, Write, Edit
---

# tap-adapter-author

你是给 TAP 写适配器的 agent。目标：**从零到 `tap <site> <command>` 输出正确数据的完整闭环**。

TAP 适配器是纯声明式的——没有自定义函数，只有 pipeline 步骤。

---

## 顶层决策树

```
START
  │
  ▼
用户想抓什么数据 / 哪个站点？
  │
  ▼
判断获取模式（→ references/patterns.md）
  │
  ├─ Pattern A: 公开 JSON API         → 直接 fetch
  ├─ Pattern B: 需要登录态的 API      → navigate + browserFetch
  ├─ Pattern C: 多请求 list-detail    → as + from + foreach
  ├─ Pattern D: XHR/fetch 请求被隐藏  → intercept
  └─ Pattern E: 数据在页面 DOM 里     → navigate + evaluate(DOM)
  │
  ▼
验证 API 端点可访问（curl / fetch 测试）
  │
  ▼
解码字段结构
  │
  ▼
设计 args + output.fields schema
  │
  ▼
组装 pipeline（→ references/patterns.md 模板）
  │
  ▼
向用户确认 schema 后安装到 ~/.tap/adapters/<site>/<command>.js
  │
  ▼
运行 tap <site> <command> 验证
  │
  ▼
DONE
```

---

## Runbook

```
[ ] 1. 明确目标
       [ ] 站点域名是什么？
       [ ] 想抓什么数据（列表 / 单条 / 排行）？
       [ ] 用户需要哪些参数（limit / keyword / category）？

[ ] 2. 侦察获取模式
       [ ] 在浏览器打开目标页面，打开 DevTools → Network 过滤 XHR/Fetch
       [ ] 观察：请求是否有 JSON 响应？URL 是否可以直接 curl？
       [ ] 判定 Pattern（A / B / C / D / E），见 references/patterns.md
       ✋ 向用户汇报：Pattern 判断结果 + API 端点 URL，等待确认后再继续

[ ] 3. 验证端点
       [ ] Pattern A：直接 curl 或 fetch 验证
       [ ] Pattern B：需要浏览器 cookie → 检查是否需要先登录
       [ ] Pattern C：确认列表接口和详情接口，优先用 as/from/foreach 表达
       [ ] Pattern D：在 Network Tab 找到被拦截的请求 URL
       [ ] Pattern E：确认数据在 DOM 里可用 document.querySelector 取到
       [ ] 确认：响应 200 + 非 HTML + 含目标数据

[ ] 4. 解码字段
       [ ] 找到 API 响应中目标字段的路径（可能有嵌套，如 data.list[0].title）
       [ ] 列出所有可用字段和类型（不要预先筛选，让用户选）
       [ ] 对比页面可见值确认字段映射正确（数量级 / 单位 / 格式）
       [ ] 为候选字段记录 raw path、示例值、观察到的类型、页面含义和不确定点
       ✋ 向用户汇报：列出全部候选字段 + 每个字段的示例值和含义判断，询问用户需要哪些字段

[ ] 5. 设计接口
       [ ] site / command 命名通过 Naming Contract（见下方），先定公共接口再定 schema
       [ ] description：一句话说明该 adapter 返回什么数据、来自哪个站点/范围
       [ ] args：用户可配的参数，命名和默认值见 references/args.md
       [ ] output.fields：按用户确认的字段声明 schema
       [ ] 每个字段必须有 type 和 description，可选 format / unit / nullable / source / examples
       [ ] 命名用 camelCase，单位清晰（如 viewCount 不是 play）
       [ ] columns：如需 table 输出，按 schema 字段顺序排列
       [ ] 通过“必要字段完整性门禁”（见下方 Required Adapter Contract）
       ✋ 向用户汇报：展示 description / args / output.fields / columns / pipeline 草稿，等待最终确认后再写文件

[ ] 6. 组装 pipeline
       [ ] 按 Pattern 选对应模板（references/patterns.md）
       [ ] 用 select 步骤提取嵌套路径（如 data.list）
       [ ] 多请求场景优先只用 as / from / foreach 三个概念，避免把请求逻辑塞进 evaluate 字符串
       [ ] map 步骤映射字段，用 ${{ }} 表达式
       [ ] map 输出 key 必须覆盖 output.fields 中声明的字段
       [ ] 不允许 map 产出未声明字段；未声明字段会被 runtime 丢弃，说明 schema 设计没对齐
       [ ] 末尾加 limit: '${{ args.limit }}'

[ ] 7. 安装适配器
       [ ] mkdir -p ~/.tap/adapters/<site>/
       [ ] 写入 ~/.tap/adapters/<site>/<command>.js

[ ] 8. 验证
       [ ] 运行 tap <site> <command>
       [ ] 确认 JSON 是 { meta, schema, items } envelope
       [ ] 确认 schema.properties 与 output.fields 一致
       [ ] 确认 items 只包含 schema 声明字段
       [ ] 检查行数、字段值是否与页面一致
       [ ] 如有 limit 参数，测试 tap <site> <command> --limit 5
```

---

## 降级路径

| 卡在 | 现象 | 跳去 |
|------|------|------|
| Step 2 | Network 没有 XHR | 尝试 Pattern E（DOM 提取）|
| Step 3 | curl 返回 403 | 需要 cookie → 改用 Pattern B |
| Step 3 | 返回 HTML | API 路径不对，重新看 Network |
| Step 3 | 返回 `{"data":[]}` 空数组 | 参数不对，检查 Network 请求参数 |
| Step 4 | 字段含义不清楚 | 对比页面排序推断（如排序后看哪列跟着变）|
| Step 5 | schema 含义无法确认 | 停下来询问用户，不要靠模型猜最终含义 |
| Step 6 | 嵌套结构复杂 | 先用 evaluate 在浏览器跑 JS 确认路径，再翻译成 select 步骤 |
| Step 8 | 输出空 | 检查 select 路径是否正确，在浏览器 console 验证 |
| Step 8 | 字段全是 undefined | map 里的 ${{ item.xxx }} 路径写错，检查实际字段名 |

---

## 参考文件

| 文件 | 什么时候翻 |
|------|----------|
| `references/patterns.md` | Step 2-6：判断 Pattern + 完整 pipeline 模板 |
| `references/args.md` | Step 5：参数命名、默认值、description 写法 |
| `references/field-mapping.md` | Step 6：${{ }} 表达式 + Pipeline Step Reference 速查 |
| `references/adapter-template.md` | Step 6-7：完整适配器结构 |

---

## 关键约定

- 适配器只能用 pipeline 声明式步骤，不能写自定义逻辑函数
- 顶层 `description` 必须写一句业务说明，用于 `tap schema` 全局命令发现；不能省略
- `args` 中每个参数都应写 `description`，让 `tap schema <site> <command>` 能指导 Agent 正确调用
- `args` 只暴露用户确实需要调节的选项；不要把上游 `ps`、`pn`、`rid` 这类含糊参数名直接暴露给用户
- `output.fields` 是 JSON 输出契约，必须由用户确认后写入；不要从字段名或样例值静默猜最终 schema
- JSON 输出只包含 `output.fields` 声明的字段；未声明字段会被 runtime 丢弃
- `columns` 只决定表格列顺序，必须与 schema/map 输出字段对齐
- 需要浏览器的适配器（Pattern B/D/E，以及使用 `browserFetch` 的 Pattern C）要求本地 Chrome 以 `--remote-debugging-port=9222` 启动
- 适配器路径：`~/.tap/adapters/<site>/<command>.js`；`site` 和 `command` 是公共 CLI 接口，创建后不要随意改名
- 调试过程中的临时 JSON 文件只落在 `/tmp/`，不要留在项目目录

## Naming Contract

写入新适配器前先确定 `site` 和 `command`。它们会出现在 `tap <site> <command>`、`tap schema <site> <command>`、文档、脚本和其他 agent 调用里，所以要按稳定公共接口设计。

### site 命名

- 使用稳定的小写 slug，只包含小写字母、数字和连字符；不要使用空格、下划线或大小写混合。
- 优先使用站点/产品/组织的品牌名，不带顶级域名：`openai`、`reddit`、`anthropic`。
- 个人站点使用稳定 handle 或域名主体：`simonwillison`。
- 同一实体不要混用多个名字；如果确实有边界，必须在 description 里体现：
  - `anthropic` 表示 `anthropic.com` 公司站内容。
  - `claude` 表示 `claude.com` 产品站内容。
- 不要把环境、分类、页面类型放进 `site`，例如不要用 `openai-engineering`、`reddit-hot`。

### command 命名

- 使用小写 kebab-case，只包含小写字母、数字和连字符。
- 命令表达“返回的数据集合或稳定入口”，不要混入临时筛选条件。
- 列表型数据优先用复数名词：`articles`、`posts`、`videos`、`topics`。
- 站点原生稳定入口可以用语义名：`hot`、`trending`、`recent`、`search`。
- 分类、时间范围、关键词优先做成 args，而不是 command：
  - 优先：`openai articles --category Engineering`
  - 谨慎：`openai engineering`，只在该分类是长期稳定的一等入口时使用
- 避免把来源和筛选混在 command 里，如 `recent-blog`；更推荐 `articles` 或 `recent`，具体来源写进 description。

### 迁移约束

- 不要为了命名洁癖迁移已有命令；已有命令可能被脚本或 skill 引用。
- 如果必须改名，先保留旧命令作为兼容入口，或在 PR/变更说明里列出明确迁移路径。
- 新建适配器时先搜索现有 `~/.tap/adapters/<site>/`，避免为同一站点创建重复 site。

## Required Adapter Contract

写文件前逐项检查。任何一项缺失，都先修 schema 或向用户确认，不要继续安装。

### 顶层必填

| key | required | 验收标准 |
|-----|----------|----------|
| `description` | yes | 一句话说明业务用途、数据来源和范围；不能只是命令名 |
| `args` | yes | 数组；每个参数都有 `name`、`default`、`description` |
| `output.type` | yes | 当前列表型命令使用 `list` |
| `output.itemName` | yes | 单数业务名，如 `topic`、`video`、`article` |
| `output.fields` | yes | 至少 1 个字段；字段集合就是 JSON 输出契约 |
| `columns` | yes for table-friendly commands | 只包含 `output.fields` 中存在的字段，顺序适合扫描 |
| `pipeline` | yes | 至少包含获取步骤和最终字段映射步骤 |

### 字段必填

每个 `output.fields.<field>` 必须满足：

- `type` 必填，只用 `string` / `integer` / `number` / `boolean` / `array` / `object`
- `description` 必填，说明业务含义，不复述字段名
- `source` 推荐填写 raw path，便于后续维护和排错
- `examples` 推荐填写 1-2 个真实样例，来自侦察结果
- 时间字段必须写 `format`，如 `iso8601`、`unix-seconds`、`date`
- URL 字段必须写 `format: 'url'`
- ID 字段必须写 `format: 'id'`，并说明是哪类 ID
- 有单位的数字必须写 `unit`，如 `views`、`replies`、`seconds`
- 可能缺失的字段必须写 `nullable: true`

### 对齐门禁

写入适配器前，手动核对这三个集合：

```
schemaFields = Object.keys(output.fields)
mapFields    = Object.keys(final map/mapOne output)
columns      = columns
```

必须满足：

- `mapFields` 覆盖全部 `schemaFields`
- `mapFields` 不包含 `schemaFields` 之外的字段
- `columns` 是 `schemaFields` 的子集
- `columns` 不包含重复字段
- `columns` 中优先放 title/url/time/count/status 等用户最常看的字段

如果 pipeline 没有显式 `map`（例如 evaluate 已直接返回最终对象），也必须把 evaluate 返回对象当作 `mapFields` 检查。

## Schema 确认规则

写入适配器前必须向用户展示 adapter schema 确认表，并包含顶层 description：

| adapter description | site | command | uncertainty |
|---------------------|------|---------|-------------|
| Fetch recent articles from example.com. | example | articles | low |

| output field | raw path | type | description | sample | uncertainty |
|--------------|----------|------|-------------|--------|-------------|
| title | data.items[].title | string | Item title. | "..." | low |

确认要求：

- 顶层 `description` 必须说明 adapter 的业务用途，不只复述命令名
- 字段名使用 camelCase，表达业务含义，不照搬含糊的上游字段名
- `type` 使用 `string` / `integer` / `number` / `boolean` / `array` / `object`
- `description` 必须说明业务含义，不只复述字段名
- 有单位的数字必须写 `unit`
- 时间、URL、ID 等格式字段应写 `format`
- 不确定字段必须显式标记并询问用户，不允许静默写入
