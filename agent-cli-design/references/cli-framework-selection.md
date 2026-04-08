# CLI 框架选型参考

来源：《2026 年，是造 CLI 的最好时机》J0hn @ AGI Hunt，2026-04-03

---

## 五大主流框架

| 框架 | 语言 | Stars | 代表项目 | 启动时间 |
|------|------|-------|----------|----------|
| Cobra | Go | 43,500 | kubectl, docker, gh, hugo, terraform, 飞书CLI | — |
| Clap | Rust | 10,000+ | ripgrep, bat, fd, dust | — |
| Typer | Python | 18,300 | — | — |
| Commander.js | Node.js | 28,000 | — | 18ms |
| oclif | Node.js | 9,400 | — | 85ms |
| Picocli | Java | 5,200 | — | ms级（GraalVM） |

---

## 选型决策树

```
需要跨平台单二进制分发？
├── 是，上手简单优先    → Go + Cobra
├── 是，极致性能优先    → Rust + Clap
└── 否
    ├── Python 团队     → Typer
    ├── Node.js 团队    → Commander.js
    ├── 需要插件架构    → oclif
    └── Java 团队       → Picocli

子命令超过 10 个？      → Cobra 或 Clap（子命令树管理能力更强）
长期打磨 + 极致性能？   → Rust + Clap（前期投入大，长期维护体验最好）
```

**默认推荐：Go + Cobra** — 从「造出来」到「分发出去」路径最短。

---

## 各框架详情

### Go：Cobra
- **核心卖点**：子命令树管理，自动生成 `--help`、shell 补全、参数校验
- **PersistentFlags**：定义在父命令上的 flag 自动继承给所有子孙命令（如全局 `--format`）
- **适合**：中大型 CLI，10 个子命令以上
- **缺点**：简单工具偏重；容易导致全局变量；cobra-cli 脚手架基本停更

### Rust：Clap
- **核心卖点**：derive macro（编译期检查）+ builder（运行时动态构建）两种风格
- **适合**：高性能工具、追求极致启动速度和类型安全
- **案例**：Railway 从 Go 重写成 Rust，获得更好类型安全和 UX，但代价是显著团队投入和更长编译时间

### Python：Typer
- **核心卖点**：用类型标注定义参数，框架自动推断类型和生成帮助文本（FastAPI 同作者）
- **适合**：快速原型、数据处理脚本、Python 团队内部工具
- **缺点**：需要 Python 运行时，分发始终是大问题（PyInstaller 打包体验不如原生二进制）

### Node.js：Commander.js
- **核心卖点**：零依赖，启动 18ms，API 干净，文档清晰
- **适合**：Node.js 技术栈团队，不要为了造 CLI 换语言

### Node.js：oclif
- **核心卖点**：TypeScript 优先，自带插件系统和 CLI 脚手架生成器
- **适合**：需要插件架构的企业级工具

### Java：Picocli
- **核心卖点**：支持 GraalVM native image，启动从秒级降到毫秒级；支持 ANSI 彩色输出和 shell 补全
- **适合**：已有 Java 生态、不想换语言的企业团队

---

## 分发方式对比

| 语言 | 分发方式 | 用户体验 |
|------|----------|----------|
| Go / Rust | 单二进制，一行 curl | 最佳，无运行时依赖 |
| Python | pip install 或 PyInstaller | 差，需要运行时或包体积大 |
| Node.js | npm install 或打包 | 中，需要 Node 运行时 |
| Java | JAR 或 GraalVM native | 中，GraalVM 编译后接近原生 |

---

## CLI vs MCP 选型参考

来源：Smithery《MCP vs CLI Is the Wrong Fight》、CircleCI 技术博客

- **用 CLI**：LLM 已有训练先验的本地工具（git、docker、ffmpeg 等）；内循环（速度和 token 效率优先）
- **用 MCP**：零训练数据的远程内部 API；外循环（团队规模和结构化鉴权优先）

**数据支撑**（ScaleKit，75 轮 benchmark，GitHub 官方 MCP vs gh CLI）：
- CLI token 消耗比 MCP 低 **10-32 倍**
- CLI 可靠性 **100%** vs MCP **72%**

---

## AI 辅助开发 CLI 的工作流

喂给 AI 的三样东西：
1. **设计规范**：Agent CLI 设计原则 checklist（noun-verb 结构、长参数优先、JSON 输出、--dry-run 等）
2. **框架知识**：Cobra 核心用法、命令树组装、flag 系统最佳实践
3. **业务需求**：操作哪些资源、支持哪些操作、输入输出格式

效果：从零到 80 分从 1-2 周 → **10 分钟**，全程约 2 小时。剩下 20 分（边界情况、错误信息措辞、退出码语义、架构细节）仍需人工打磨。
