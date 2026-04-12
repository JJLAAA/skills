# CLI Build Workflow

When building a complete agent-friendly CLI from source material (API docs, OpenAPI spec,
curl examples, SDK, web app, admin tool, or local script), follow this workflow.

This is the operational companion to the design principles in `10-principles.md`. Use the
principles to judge quality; use this workflow to get there.

---

## 1. Command Surface Design

Sketch the command surface in chat **before coding**. Include the binary name, discovery
commands, resolve commands, read commands, write commands, raw escape hatch, auth/config
approach, and PATH install method.

Build toward this surface:

- `tool-name --help` shows every major capability.
- `tool-name --json doctor` verifies config, auth, version, endpoint reachability, and
  missing setup.
- `tool-name init ...` stores local config when env-only auth is painful.
- **Discovery** commands find accounts, projects, workspaces, teams, queues, channels,
  repos, dashboards, or other top-level containers.
- **Resolve** commands turn names, URLs, slugs, permalinks, customer input, or build
  links into stable IDs so future commands do not repeat broad searches.
- **Read** commands fetch exact objects and list/search collections. Paginated lists
  support a bounded `--limit`, cursor, offset, or clearly documented default.
- **Write** commands do one named action each: create, update, delete, upload, schedule,
  retry, comment, draft. They accept the narrowest stable resource ID, support
  `--dry-run`, `draft`, or `preview` when the service allows it, and do not hide writes
  inside broad commands such as `fix`, `debug`, or `auto`.
- `--json` returns stable machine-readable output.
- A **raw escape hatch** exists: `request`, `api`, or the nearest honest name.

Do not expose only a generic `request` command. Give agents high-level verbs for the
repeated jobs.

Document the JSON policy in the CLI README: API pass-through versus CLI envelope, success
shape, error shape, and one example per command family. Under `--json`, errors must be
machine-readable and must not contain credentials.

---

## 2. Runtime Selection

Before choosing, inspect the user's machine and source material:

```bash
command -v cargo rustc node pnpm npm python3 uv || true
```

Choose the least surprising toolchain:

- **Rust**: durable CLI meant to run from any repo — one fast binary, strong argument
  parsing, good JSON handling, easy install into `~/.local/bin`.
- **TypeScript/Node**: the official SDK, auth helper, browser automation library, or
  existing repo tooling is the reason the CLI can be better.
- **Python**: data science, local file transforms, notebooks, SQLite/CSV/JSON analysis,
  or Python-heavy admin tooling that can still be installed as a durable command.

Do not pick a language that adds setup friction unless it materially improves the CLI.
If the best language is not installed, install the missing toolchain with the user's
approval or fall back to the next-best installed option.

State the choice in one sentence before scaffolding, including the reason and the
installed toolchain found.

---

## 3. Auth and Config

Support the boring paths first, in this precedence order:

1. **Environment variable** using the service's standard name, such as `GITHUB_TOKEN`.
2. **User config** under `~/.<tool-name>/config.toml` or another simple documented path.
3. `--api-key` or a tool-specific token flag only for explicit one-off tests. Prefer
   env/config for normal use because flags can leak into shell history or process
   listings.

Never print full tokens. `doctor --json` should say whether a token is available, the
auth source category (`flag`, `env`, `config`, provider default, or missing), and what
setup step is missing.

If the CLI can run without network or auth, make that explicit in `doctor --json`:
report fixture/offline mode, whether fixture data was found, and whether auth is not
required for that mode.

For internal web apps sourced from browser DevTools, create sanitized endpoint notes
before implementing: resource name, method/path, required headers, auth mechanism, CSRF
behavior, request body, response ID fields, pagination, errors, and one redacted sample
response. Never commit copied cookies, bearer tokens, customer secrets, or full
production payloads.

---

## 4. Build Steps

1. **Read the source** just enough to inventory resources, auth, pagination, IDs,
   media/file flows, rate limits, and dangerous write actions. If the docs expose
   OpenAPI, download or inspect it before naming commands.
2. **Sketch the command list** in chat. Keep names short and shell-friendly.
3. **Scaffold** the CLI with a README or equivalent repo-facing instructions.
4. **Implement** `doctor`, discovery, resolve, read commands, one narrow draft or
   dry-run write path if requested, and the raw escape hatch.
5. **Install** the CLI on PATH so `tool-name ...` works outside the source folder.
6. **Smoke test** from another directory or `/tmp`, not only with `cargo run` or
   package-manager wrappers. Run `command -v <tool-name>`, `<tool-name> --help`, and
   `<tool-name> --json doctor`.
7. **Test**: format, typecheck/build, unit tests for request builders, pagination /
   request-body builders, no-auth `doctor`, help output, and at least one fixture,
   dry-run, or live read-only API call.

If a live write is needed for confidence, ask first and make it reversible or
draft-only.

### Source-specific guidance

**Existing script or shell history**: split the working invocation into real phases —
setup, discovery, download/export, transform/index, draft, upload, poll, live write.
Preserve the flags, paths, and environment variables the user already relies on, then
wrap the repeatable phases with stable IDs, bounded JSON, and file outputs.

**Raw escape hatches**: support read-only calls first. Do not run raw non-GET/HEAD
requests against a live service unless the user asked for that specific write.

**Media / artifact / presigned upload flows**: test each phase separately — create
upload, transfer bytes, poll/read processing status, then attach or reference the
resulting ID.

**Fixture-backed prototypes**: keep fixtures in a predictable project path and make the
CLI locate them after installation. Smoke-test from `/tmp` to catch binaries that only
work inside the source folder.

**Log-oriented CLIs**: keep deterministic snippet extraction separate from model
interpretation. Prefer a command that emits filenames, line numbers or byte ranges,
matched rules, and short excerpts.

---

## 5. Per-Language Tech Stack Defaults

### Rust

Use established crates instead of custom parsers:

- `clap` for commands and help
- `reqwest` for HTTP
- `serde` / `serde_json` for payloads
- `toml` for small config files
- `anyhow` for CLI-shaped error context

Add a `Makefile` target such as `make install-local` that builds release and installs
the binary into `~/.local/bin`.

### TypeScript / Node

Keep the CLI installable as a normal command:

- `commander` or `cac` for commands and help
- native `fetch`, the official SDK, or the user's existing HTTP helper for API calls
- `zod` only where external payload validation prevents real breakage
- `package.json` `bin` entry for the installed command
- `tsup`, `tsx`, or `tsc` using the repo's existing convention

Add an install path such as `pnpm install`, `pnpm build`, and `pnpm link --global`, or
a `Makefile` target that installs a small wrapper into `~/.local/bin`.

### Python

Prefer boring standard-library pieces unless the workflow needs more:

- `argparse` for commands and help, or `typer` when subcommands would otherwise get
  messy
- `urllib.request` / `urllib.parse`, `requests`, or `httpx` for HTTP, matching what is
  already installed or already used nearby
- `json`, `csv`, `sqlite3`, `pathlib`, and `subprocess` for local files, exports,
  databases, and existing scripts
- `pyproject.toml` console script or a small executable wrapper for the installed
  command
- `uv` or a virtualenv only when dependencies are actually needed

Add a `Makefile` target such as `make install-local` that installs the command on PATH
and document whether it depends on `uv`, a virtualenv, or only system Python.

---

## 6. Companion Skill Creation

After the CLI works, create a companion skill file that teaches agents how to use it.
The companion skill should be smaller than the CLI README — it teaches the **path**
through the tool, not a tour of every feature.

Write the skill in the order an agent should use the CLI:

1. How to verify the installed command exists
2. Which command to run first
3. How auth is configured
4. Which discovery command finds the common ID
5. The safe read path
6. The intended draft/write path
7. The raw escape hatch
8. What not to do without explicit user approval
9. Three copy-pasteable command examples

Keep API reference details in the CLI docs or a skill reference file. Keep the skill
focused on ordering, safety, and examples agents should actually run.

### Companion Skill Template

```md
Start with:

  tool-name --json doctor
  tool-name --json accounts list

For [common job]:

  tool-name --json ...
  tool-name --json ...

Rules:

  - Prefer installed `tool-name` on PATH
  - Use --json when analyzing output
  - Create drafts by default
  - Do not publish/delete/retry/submit unless the user asked
  - Use `request get ...` only when high-level commands are missing
```

Include JSON shape notes only when the agent needs them to choose the next command.
