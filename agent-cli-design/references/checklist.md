# Agent-Friendly CLI Checklist

Use this checklist to audit an existing CLI or verify a new design.
Each item maps to one of the 14 principles in `10-principles.md`.

---

## Quick Audit Checklist

### Structure & Discovery
- [ ] **P1** Commands use noun-verb hierarchy (e.g., `tool resource action`), not flat verb-noun
- [ ] **P1** Running `tool --help` reveals a navigable tree of nouns, not a flat list of commands
- [ ] **P1** The same verb (list, create, delete, get) means the same thing across all nouns

### Parameter Design
- [ ] **P2** Every parameter has a long form (`--verbose`, not just `-v`)
- [ ] **P2** Short forms exist only as optional aliases, never as the only option
- [ ] **P2** Parameter names are self-describing (`--dry-run`, `--if-not-exists`, `--output-format`)
- [ ] **P7** Enum parameters use `type=Choice(["a","b","c"])`, not free-text strings
- [ ] **P7** There's a `--yes` / `--no-interactive` flag to skip all confirmation prompts

### Output
- [ ] **P3** Data goes to stdout, status/logs/warnings go to stderr — never mixed
- [ ] **P3** `--format json|table|csv` (or similar) is supported
- [ ] **P4** In non-TTY environments, output defaults to JSON (no `--json` flag required)
- [ ] **P4** No ANSI color codes, spinners, or progress bars in non-TTY mode
- [ ] **P3** Output schema is documented and treated as a versioned API contract

### Safety & Reliability
- [ ] **P5** Every command with side effects supports `--dry-run`
- [ ] **P5** `--dry-run` output is structured JSON showing what would change (not just "dry-run mode")
- [ ] **P8** Destructive/create commands support `--if-not-exists` or `ensure` variant
- [ ] **P8** Key operations support `--idempotency-key` for safe retries

### Error Handling
- [ ] **P6** Exit codes are documented with specific meanings (not just 0=success, 1=failure)
- [ ] **P6** Exit codes are stable across versions (treated as API contract)
- [ ] **P9** Error output is structured JSON with `error`, `message`, `suggestion`, `retryable` fields
- [ ] **P9** Error messages include specific fix instructions, not just symptom descriptions

### Discoverability
- [ ] **P7** `schema` command (or `--schema`) outputs machine-readable command/parameter definitions
- [ ] **P10** `--help` starts with 2-3 usage examples
- [ ] **P10** `--help` labels parameters as `<required>` or `<optional, default: X>`
- [ ] **P10** `--help` shows enum values inline (`--format json|table|csv`)
- [ ] **P10** `--help` stays under 50 lines per command

### Input Validation
- [ ] **P7** URL parameters reject dangerous protocols (`javascript:`, `file:`, `data:`)
- [ ] **P7** URL parameters reject embedded credentials
- [ ] **P7** Output path parameters reject writes to sensitive directories (`.ssh/`, `.gnupg/`, etc.)

### Skill Pairing (P11)
- [ ] **P11** A companion Skill file exists alongside the CLI binary
- [ ] **P11** Skill is split by domain (one Skill per business area, not one giant Skill)
- [ ] **P11** A shared base Skill handles auth, identity, and security rules
- [ ] **P11** Each Skill includes a Quick Reference table and Workflows section
- [ ] **P11** Skill parameters document where to get required IDs (e.g., "get `--chat-id` from: ...")
- [ ] **P11** Commands have been tested with real agents; success rate is the quality gate

### Three-Layer Abstraction (P12)
- [ ] **P12** Shortcut commands (`+prefix` or similar) exist for the 80% high-frequency cases
- [ ] **P12** API commands (noun-verb, auto-generated from metadata) cover the 15% case
- [ ] **P12** Raw API escape hatch exists for full endpoint coverage
- [ ] **P12** Shortcuts encode smart defaults and opinionated output (table, concise params)
- [ ] **P12** Agents are guided to try shortcuts first, fall back to API commands, then raw
- [ ] **P12** When a Shortcut fails due to unsupported flag, error `hint` names the Layer 2 command
- [ ] **P12** `schema <command>` returns machine-readable parameter definitions for Layer 2 commands
- [ ] **P12** When a Layer 2 command doesn't exist, error `hint` provides the raw API path

### Agent Auth Patterns (P13)
- [ ] **P13** OAuth flow supports `--no-wait` mode (returns URL immediately, doesn't block)
- [ ] **P13** `--device-code` flag allows resuming a paused auth flow
- [ ] **P13** Tokens are stored in OS-native keychain (not plaintext files or env vars)
- [ ] **P13** Keychain service name is hardcoded (not user-configurable)
- [ ] **P13** `--as user|bot` (or equivalent) supports explicit identity switching
- [ ] **P13** Scope selection supports domain-level (`--domain`), exact (`--scope`), and recommended (`--recommend`) modes

### Stdin Input (P15)
- [ ] **P15** Commands that accept data support `--stdin` flag to read from stdin
- [ ] **P15** Pipeline-oriented commands auto-detect stdin when it's a pipe (not a TTY)
- [ ] **P15** stdin is never read when `sys.stdin.isatty()` is true (avoids blocking humans)
- [ ] **P15** stdout output is clean and pipeable (no status noise mixed in)

### Context Budget (P14)
- [ ] **P14** List commands support `--fields` / `--field-mask` to return only requested fields
- [ ] **P14** List commands paginate by default (`--limit`, `--page-token`); never return unbounded results
- [ ] **P14** Commands that can return >2,000 tokens document this in their `--help` and Skill file
- [ ] **P14** Skill file includes a "Typical output size" column for high-volume commands
- [ ] **P14** NDJSON streaming is supported for commands that return large lists

---

## Scoring Guide

**16 categories, 1 point each** (the sub-items within a category count as 1 point if all pass):

| Score | Assessment |
|-------|-----------|
| 14-16 | Agent-ready. Minor polish only. |
| 11-13 | Good foundation. Fix the failing items before agent deployment. |
| 6-10 | Significant gaps. Agents will encounter frequent failures. |
| 0-5 | Designed for humans only. Major redesign needed for agent use. |

---

## Priority Order for Fixes

When you can't fix everything at once, prioritize in this order:

1. **TTY detection + default JSON output** (P4) — agents get stuck or parse garbage without this
2. **Remove interactive prompts / add `--yes`** (P4) — interactive prompts are hard walls for agents
3. **Structured error messages with `retryable` flag** (P9) — agents can't self-correct without this
4. **Exit code semantics** (P6) — agents need to distinguish "fix params" from "request auth"
5. **Long flags for all parameters** (P2) — reduces flag confusion probability significantly
6. **`--dry-run` for side-effect commands** (P5) — enables safe exploration
7. **Noun-verb structure** (P1) — enables deterministic command discovery
8. **Enum constraints** (P7) — reduces hallucinated parameter values
9. **Idempotent operations** (P8) — makes retries safe
10. **Schema introspection** (P7) — reduces first-attempt hallucination rate
11. **`--help` quality** (P10) — improves first-attempt accuracy
12. **Skill pairing** (P11) — reduces command selection errors
13. **Three-layer abstraction** (P12) — right granularity for every use case
14. **Agent auth patterns** (P13) — non-blocking OAuth for agent workflows
15. **Context budget** (P14) — field masks + pagination prevents context window exhaustion
16. **Output schema versioning** (P3) — prevents downstream breakage on updates

---

## Common Failure Scenarios by Missing Feature

| Missing Feature | Agent Failure Mode |
|----------------|-------------------|
| No TTY detection | Agent gets ANSI codes in output, JSON parsing fails |
| Interactive prompts | Agent hangs indefinitely waiting for y/N |
| Only short flags | Agent uses `-V` (version) instead of `-v` (verbose) |
| No `--dry-run` | Agent executes irreversible action without preview |
| Only exit 0/1 | Agent retries permission errors instead of requesting auth |
| Free-text params | Agent passes hallucinated value, silent failure |
| Vague error messages | Agent retries same wrong approach 20+ times |
| Verb-noun flat structure | Agent can't discover commands without reading all docs |
| Non-idempotent create | Agent retry creates duplicate records |
| No schema introspection | Agent hallucinates parameter names for unfamiliar commands |
| No Skill file | Agent picks wrong command or wrong layer for the task |
| No shortcuts layer | Agent over-engineers simple tasks with raw API calls |
| Blocking OAuth | Agent hangs waiting for browser flow it can't complete |
| No field masks / pagination | Single list command exhausts context window, degrades reasoning |
