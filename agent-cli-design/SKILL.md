---
name: agent-cli-design
description: |
  Design and implement agent-friendly CLI tools for AI agents and automation. This skill supports auditing existing CLIs, designing new command trees, and implementing features like structured output, dry-run behavior, deterministic exit codes, strict input validation, idempotency, actionable error messages, and non-blocking auth flows. Use it when users ask about LLM/agent CLI best practices, improving tools built with Click/Cobra/Clap/argparse, choosing MCP vs CLI, or creating layered command systems with companion Skill files.
---

# Agent-Friendly CLI Design

AI agents are becoming primary users of CLI tools. They don't click buttons or fill forms — they
run `--help`, parse output, compose commands, and check exit codes. But agents have different
failure modes than humans: they confuse similar-looking flags, get stuck on interactive prompts,
hallucinate parameters, and can't parse unstructured output.

This skill helps you design CLIs that work well for both agents and humans, with agents as the
primary design constraint.

## When to Use This Skill

- **Audit mode**: User has an existing CLI and wants to know what to improve
- **Design mode**: User is designing a new CLI from scratch
- **Implementation mode**: User wants to implement a specific agent-friendly feature
- **Explain mode**: User wants to understand why certain CLI patterns matter for agents

## Workflow

### Step 1: Understand the Context

Before diving in, figure out which mode applies:

1. **Does the user have existing CLI code or a spec?** → Audit mode
2. **Are they starting fresh?** → Design mode
3. **Do they want a specific feature?** → Implementation mode
4. **Are they asking "why"?** → Explain mode

Ask for:
- The CLI's purpose and target domain
- What language/framework they're using (Python/Click, Go/Cobra, Rust/Clap, Node/Commander, etc.)
- Whether agents will be the primary or secondary users
- Any existing code or command structure to review

For framework selection guidance (Go/Rust/Python/Node/Java 对比、选型决策树、CLI vs MCP benchmark 数据),
see `references/cli-framework-selection.md`.

### Step 2: Apply the 13-Principle Framework

Read `references/10-principles.md` for the full framework. Here's the quick map:

| Principle | Key Question |
|-----------|-------------|
| 1. Noun-Verb Structure | Does `--help` reveal a navigable tree, or a flat list? |
| 2. Long Flags First | Can an agent understand every flag without context? |
| 3. Output as Contract | Is stdout/stderr separated? Is JSON output stable across versions? |
| 4. Environment Detection | Does the CLI behave differently in TTY vs pipe? |
| 5. Dry-Run Support | Can agents preview side effects before committing? |
| 6. Exit Code Semantics | Do exit codes distinguish error types, not just success/failure? |
| 7. Hallucination Defense | Are inputs validated? Are enums used instead of free text? |
| 8. Idempotent Design | Can agents safely retry without creating duplicates? |
| 9. Errors as Instructions | Do error messages tell agents exactly how to fix the problem? |
| 10. Help as Brain | Does `--help` start with examples and stay under 50 lines? |
| 11. Skill Pairing | Is there a companion Skill file teaching agents *when* to use which commands? |
| 12. Three-Layer Abstraction | Are there shortcut / API / raw layers for different granularity needs? |
| 13. Agent Auth Patterns | Does OAuth support `--no-wait` + `--device-code` for non-blocking agent flows? |
| 14. Context Budget | Do list commands support `--fields` and pagination to avoid context exhaustion? |
| 15. Stdin Input | Do data-accepting commands support `--stdin` and pipe auto-detection? |

### Step 3: Mode-Specific Output

#### Audit Mode

Run through the checklist in `references/checklist.md` against the user's CLI. For each item:
- **Pass**: Brief confirmation
- **Fail**: Explain the risk with a concrete failure scenario, then show the fix
- **N/A**: Note why it doesn't apply

End with a prioritized fix list: what to fix first (highest agent-failure risk), what can wait.

#### Design Mode

Help the user design their CLI structure top-down:

1. **Identify the nouns** (resources/entities the CLI manages)
2. **Map the verbs** (actions per noun — keep them consistent: `list`, `get`, `create`, `update`, `delete`, `ensure`)
3. **Design the output schema** (what JSON shape does each command return?)
4. **Define exit codes** (what failure modes need distinct codes?)
5. **Write the `--help` text** (examples first, required/optional labeled, enum values listed)

Show a concrete command tree before writing any code.

#### Implementation Mode

Help the user implement a specific agent-friendly feature in their language/framework of choice.
See `references/implementation-patterns.md` for language-agnostic patterns covering each principle.

For concrete design decisions on parameter design, output formats, pagination, and error
envelopes derived from a production CLI (larksuite/cli), see
`references/lark-cli-design-patterns.md`.

Always include:
- The implementation (in the user's language/framework)
- A test showing it works correctly in a pipe/non-TTY context
- A note on what agent failure mode this prevents

#### Explain Mode

Use concrete failure scenarios to explain why the principle matters. The best explanations
connect to real incidents (AWS CLI v2 pager, Kubernetes --export removal, the 693-line
hallucination spiral). See `references/10-principles.md` for the full incident library.

### Step 4: Deliver the Output

**For audits**, use this structure:
```
## Agent-Friendliness Audit: [CLI Name]

### Score: X/12 principles met

### Critical Issues (fix these first)
[Issues that will cause agent failures]

### Improvements (nice to have)
[Issues that reduce reliability but won't break things]

### Already Good
[What's working well]

### Prioritized Fix Plan
1. [Highest impact fix]
2. ...
```

**For design**, produce:
```
## CLI Design: [Tool Name]

### Command Tree
[noun-verb hierarchy]

### Output Schema
[JSON shape for key commands]

### Exit Code Map
[code → meaning → agent response]

### Help Text Template
[--help output for the main command]
```

**For implementation**, produce working code with inline comments explaining the agent-friendly
design choices.

## Key Principles to Internalize

The underlying logic behind all 10 principles is the same: **agents explore deterministically,
fail probabilistically, and retry automatically**. Good CLI design reduces the probability of
each failure mode and makes retries safe.

- Noun-verb structure → deterministic exploration via `--help` tree
- Long flags → lower probability of flag confusion
- Structured output → deterministic parsing
- TTY detection → no interactive prompts blocking agent
- Dry-run → safe exploration before commitment
- Exit codes → deterministic retry/abort decisions
- Input validation → catch hallucinated parameters early
- Idempotency → safe retries
- Error messages → self-correcting agent behavior
- Good help text → lower hallucination rate on first attempt

The goal isn't to make CLIs that only work for agents — it's to make CLIs where the agent-friendly
design also makes them better for humans. Structured output, clear error messages, and good help
text benefit everyone.
