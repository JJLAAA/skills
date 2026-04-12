---
name: agent-cli-design
description: |
  Design and build agent-friendly CLI tools for AI agents and automation. Three modes: Audit (evaluate existing CLI against agent-friendly checklist), Design (plan command tree, output schema, exit codes), Build (implement a complete CLI or specific features from source material or requirements). Covers structured output, dry-run, exit codes, input validation, idempotency, actionable errors, non-blocking auth, companion skill creation, and more. Use it when users ask about agent CLI best practices, improving tools built with Click/Cobra/Clap/argparse, choosing MCP vs CLI, or building a new CLI.
---

# Agent-Friendly CLI Design

AI agents are becoming primary users of CLI tools. They don't click buttons or fill forms — they
run `--help`, parse output, compose commands, and check exit codes. But agents have different
failure modes than humans: they confuse similar-looking flags, get stuck on interactive prompts,
hallucinate parameters, and can't parse unstructured output.

This skill helps you design CLIs that work well for both agents and humans, with agents as the
primary design constraint.

## Modes

Two independent entry points. They can be used alone or composed:

- **Audit**: User has an existing CLI, wants to evaluate and improve it
- **Build**: User wants a working CLI built — always starts with a design phase requiring user approval before any code is written

Compositions:
- Audit → Build (audit identifies issues, build implements fixes)

## Workflow

### Step 1: Determine the Entry Point

Ask what the user has and what they want:

- **Has an existing CLI?** → Audit
- **Wants to build a CLI (new or adding features)?** → Build (always starts with a design phase)
- **Has an existing CLI and wants to add a specific feature?** → Build (with audit context)

Ask for:
- The CLI's purpose and target domain
- What language/framework they're using (Python/Click, Go/Cobra, Rust/Clap, Node/Commander, etc.)
- Whether agents will be the primary or secondary users
- Any existing code or command structure to review

For framework selection guidance (Go/Rust/Python/Node/Java 对比、选型决策树、CLI vs MCP benchmark 数据),
see `references/cli-framework-selection.md`.

### Step 2: Apply the Principle Framework

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

#### Build Mode

Build always starts with a design phase before any code is written.

**Phase 1 — Design (required, blocking)**

Apply the 15-principle framework (Step 2) to drive design decisions. For each principle, ask whether it affects the API surface — if yes, resolve it in the design before proceeding.

1. **Identify the nouns** (resources/entities the CLI manages)
2. **Map the verbs** (actions per noun — keep them consistent: `list`, `get`, `create`, `update`, `delete`, `ensure`)
3. **Design the output schema** (what JSON shape does each command return? Apply P3 Output as Contract)
4. **Define exit codes** (what failure modes need distinct codes? Apply P6 Exit Code Semantics)
5. **Write the `--help` text** (examples first, required/optional labeled, enum values listed. Apply P10 Help as Brain)
6. **Resolve principle-driven design questions** — work through each principle that affects the API surface:
   - P5 Dry-Run: which commands need `--dry-run`? What does the preview output look like?
   - P8 Idempotency: which commands are safe to retry? Do any need `--ensure` semantics?
   - P12 Three-Layer Abstraction: are shortcut / API / raw layers needed?
   - P13 Agent Auth: does any command involve OAuth? Design `--no-wait` + `--device-code` flow now.
   - P14 Context Budget: which list commands need `--fields` and pagination?
   - P15 Stdin Input: which data-accepting commands need `--stdin` and pipe auto-detection?
   - P7 Hallucination Defense: where should enums replace free text? What inputs need early validation?
   - P11 Skill Pairing: outline the companion Skill file structure now (fill content in Phase 2)

Present the initial design as a concrete command tree and schema, then **iterate with the user** — surface tradeoffs, rename commands, add or remove verbs, adjust the JSON schema, and resolve open principle questions through clarification. Only proceed to Phase 2 after the user explicitly approves the final design.

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

### Principle Decisions
[resolved design choices per applicable principle]
```

**[CHECKPOINT] Present the design above. Iterate with the user until the design is approved. This is the design freeze point — no design decisions should be made in Phase 2.**

---

**Phase 2 — Build (starts only after design is approved)**

Follow the workflow in `references/build-workflow.md`:
1. Runtime selection (Rust / TypeScript / Python based on user machine and source material)
2. Auth and config (env var → config file → flag precedence, `doctor --json` reporting)
3. Build steps (scaffold → implement → install → smoke test → test)
4. Per-language tech stack defaults (crates, libraries, install targets)
5. Companion skill creation (9-element ordered guide + template)

**Feature implementation**: When the user wants a specific agent-friendly feature added to an
existing CLI, see `references/implementation-patterns.md` for language-agnostic patterns covering
each principle. For concrete design decisions from a production CLI (larksuite/cli), see
`references/lark-cli-design-patterns.md`. Always include:
- The implementation (in the user's language/framework)
- A test showing it works correctly in a pipe/non-TTY context
- A note on what agent failure mode this prevents

Apply the principle framework from Step 2 throughout. Use the checklist in
`references/checklist.md` to verify the result before delivery.

### Step 4: Deliver the Output

**For audits**, use this structure:
```
## Agent-Friendliness Audit: [CLI Name]

### Score: X/16 principles met

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

**For build**, Phase 1 produces the design document (command tree, output schema, exit code map, help template) and waits for approval. Phase 2 produces the full CLI following `references/build-workflow.md`, including:
installed binary on PATH, working `--help` and `--json doctor`, at least one fixture or
read-only smoke test, and a companion skill file. Verify with the checklist in
`references/checklist.md` before delivery.

For feature implementations, produce working code with inline comments explaining the
agent-friendly design choices.

## Key Principles to Internalize

The underlying logic behind all principles is the same: **agents explore deterministically,
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
