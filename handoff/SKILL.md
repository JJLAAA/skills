---
name: handoff
description: This skill should be used when the user requests to save progress, pause work, create a handoff document, or says "保存进度", "handoff", "暂停", "checkpoint", "交接". It enables zero-loss context transfer across AI agent sessions by creating a structured handoff document written FOR THE NEXT AI AGENT (not for humans). Use this at session end, when approaching context limits, or before switching tasks. The handoff preserves executable context - specific file paths, function names, decision rationale, failed approaches, and priority-ordered next steps.
---

# Handoff - AI Agent Context Transfer

## Core Principle

**This is NOT a user summary - it's a technical handoff TO THE NEXT AI AGENT.**

The next agent cannot access this conversation. It only sees your handoff document. Your goal: enable it to continue work immediately without repeating your analysis, mistakes, or wasted effort.

---

## When to Trigger

**User keywords:**
- "保存进度" / "save progress" / "handoff" / "暂停" / "checkpoint" / "交接"

**Proactive triggers:**
- Context approaching limit
- Session ending
- Complex multi-session task
- Before task switching

---

## Workflow

### Step 1: Determine File Location

Generate filename: `./{YYMMDD}-handoff.md` (e.g., `./260314-handoff.md`)

Use current directory unless user specifies otherwise.

### Step 2: Gather Executable Context

Collect SPECIFIC, ACTIONABLE information:

- **Concrete identifiers**: File paths, class names, function names, variable names, API endpoints
- **Decision rationale**: WHY certain approaches were chosen
- **Failed attempts**: What was tried and WHY it didn't work
- **Assumptions made**: What was assumed to be true
- **Verification status**: What has been tested/confirmed

### Step 3: Write Handoff Document

Write to `./{YYMMDD}-handoff.md` using the structure below.

### Step 4: Confirm

Tell user: "Handoff saved to `{filename}` - next agent can continue from here."

---

## Handoff Document Structure

```markdown
# AI Agent Handoff - {YYMMDD}

> **Target Audience:** Next AI Agent (cannot access current context)
> **Goal:** Enable immediate continuation without repeating analysis or mistakes

---

## 1. Current Task Objective

**What problem are we solving:**
[Specific problem description]

**Expected output:**
[Concrete deliverables with acceptance criteria]

**Completion criteria:**
[How to know when done]

---

## 2. Current Progress

**Completed:**
- [Specific action taken] - resulted in [concrete outcome]
- [Another completed item] - file: `path/to/file.ts:123`

**In progress:**
- [Current work item] - status: [percentage or milestone]
- Files being modified: `path/to/file1.ts`, `path/to/file2.ts`

---

## 3. Critical Context

**User requirements:**
- [Explicit requirement 1]
- [Explicit requirement 2]

**Key constraints:**
- [Technical constraint] - reason: [why it matters]
- [Business constraint] - impact: [what it affects]

**Important decisions made:**
- **Decision:** [What was decided]
  - **Rationale:** [Why this approach]
  - **Alternatives considered:** [What else was evaluated]
  - **Trade-offs:** [What we're giving up]

**Assumptions:**
- [Assumption 1] - needs verification: [yes/no]
- [Assumption 2] - confirmed by: [evidence]

---

## 4. Key Findings

**Technical discoveries:**
- [Finding 1] - location: `file.ts:line_number`
- [Pattern observed] - affects: [what components]

**Root causes identified:**
- [Problem] → [Root cause] → [Evidence: file/log/test]

**Critical insights:**
- [Insight that changes approach]
- [Non-obvious relationship between components]

---

## 5. Failed Approaches (DO NOT RETRY)

**Approach 1: [Description]**
- **Why tried:** [Reasoning]
- **Why failed:** [Specific error or limitation]
- **Evidence:** [Error message, test result, file: `path:line`]
- **Lesson:** [What this teaches us]

**Approach 2: [Description]**
- **Why tried:** [Reasoning]
- **Why failed:** [Specific reason]
- **Don't waste time on:** [What to avoid]

---

## 6. Pending Tasks (Priority Order)

**Priority 1 (URGENT):**
- [ ] [Specific task] - blocks: [what depends on this]
  - Files: `path/to/file.ts`
  - Function: `functionName()`
  - Expected change: [what needs to happen]

**Priority 2 (HIGH):**
- [ ] [Next task] - depends on: [prerequisite]
  - Location: `path/to/file.ts:line_range`

**Priority 3 (MEDIUM):**
- [ ] [Lower priority task]

---

## 7. Recommended First Steps

**Step 1: Verify current state**
```bash
# Commands to run
git status
git log -1 --oneline
```

**Step 2: Check these files first**
- `path/to/critical/file.ts` - contains: [what to look for]
- `path/to/another/file.ts:123-145` - focus on: [specific section]

**Step 3: Run this to validate**
```bash
# Validation command
npm test path/to/test.spec.ts
```

**Step 4: Start here**
- Open: `path/to/file.ts`
- Locate: `function targetFunction()`
- Modify: [specific change needed]
- Reason: [why this is the right starting point]

---

## 8. Risks & Pitfalls

**Easy to misunderstand:**
- [Concept X] - actually means: [correct interpretation]
- [File Y] - looks like [A] but is actually [B]

**Already verified (don't re-check):**
- ✓ [Thing 1] - confirmed in: `file.ts:line`
- ✓ [Thing 2] - test: `test.spec.ts` passes

**Watch out for:**
- [Gotcha 1] - symptom: [how it manifests] - solution: [how to handle]
- [Edge case] - occurs when: [condition] - handle by: [approach]

**Don't go down these paths:**
- ❌ [Approach X] - already tried, failed because: [reason]
- ❌ [Direction Y] - looks promising but: [why it won't work]

---

## 9. File Inventory

**Modified files:**
- `path/to/file1.ts` - changes: [what was changed] - status: [committed/uncommitted]
- `path/to/file2.ts` - changes: [what was changed] - status: [committed/uncommitted]

**New files created:**
- `path/to/new/file.ts` - purpose: [why it exists]

**Files to review:**
- `path/to/important/file.ts` - contains: [relevant info]

---

## 10. Git Status

**Branch:** `branch-name`
**Latest commit:** `abc123def` - message: "commit message"
**Uncommitted changes:** [yes/no]
**Unpushed commits:** [yes/no]

---

## 11. Environment & Dependencies

**Runtime:**
- Node version: [version]
- Package manager: [npm/yarn/pnpm]

**Key dependencies:**
- [package-name@version] - used for: [purpose]

**Environment variables needed:**
- `VAR_NAME` - purpose: [what it controls]

---

## 12. Next Agent's First Action

**Immediate next step:**

1. Read file: `path/to/file.ts:line_range`
2. Verify assumption: [what to check]
3. If [condition], then [action A], else [action B]
4. Expected outcome: [what should happen]

**Why start here:**
[Explanation of why this is the optimal starting point based on current state]

---

## Session Metadata

- **Created:** {YYYY-MM-DD HH:MM}
- **Context tokens used:** [approximate]
- **Session duration:** [time spent]
- **Handoff reason:** [why session ended]
```

---

## Writing Guidelines

**Be specific, not generic:**
- ❌ "Fix the authentication bug"
- ✅ "Fix JWT token expiration in `src/auth/middleware.ts:45` - tokens expire after 1 hour instead of 24 hours"

**Include evidence:**
- ❌ "The API is slow"
- ✅ "GET /api/users takes 3.2s (measured via `curl -w '%{time_total}'`) - caused by N+1 query in `UserController.ts:89`"

**Document WHY, not just WHAT:**
- ❌ "Used Redis for caching"
- ✅ "Used Redis for caching because in-memory cache doesn't persist across container restarts (requirement from user: 'cache must survive deployments')"

**Mark verification status:**
- ✓ Confirmed: [evidence]
- ⚠️ Assumed: [needs verification]
- ❌ Disproven: [evidence]

---

## Anti-Patterns (Avoid These)

❌ **Vague descriptions:** "The code needs improvement"
✅ **Specific:** "Function `processData()` in `utils.ts:234` has O(n²) complexity - refactor to use Map for O(n)"

❌ **Missing context:** "Changed the config"
✅ **Full context:** "Changed `timeout` in `config/api.ts:12` from 5000ms to 30000ms because external API (user requirement: 'must support slow 3rd party API') takes 15-20s to respond"

❌ **No rationale:** "Decided to use PostgreSQL"
✅ **With rationale:** "Decided to use PostgreSQL over MongoDB because user needs ACID transactions for payment processing (explicit requirement: 'payments must be atomic')"

---

## Session Startup: Reading Previous Handoff

When starting a new session:

1. Check for `*-handoff.md` files in current directory
2. If found, read the most recent one
3. Display brief summary to user:

```
Found handoff from {date}:

Task: {brief objective}
Progress: {completion percentage}
Next step: {priority 1 task}

Continue from here? [Y/n]
```

4. If user confirms, use handoff content to restore full context
5. Start with "Recommended First Steps" section

---

## Tips for Maximum Effectiveness

1. **Assume zero context** - next agent sees ONLY your handoff
2. **Prioritize executable info** - file paths > abstract concepts
3. **Document the "why"** - decisions without rationale are useless
4. **Mark dead ends** - save next agent from repeating failures
5. **Be brutally specific** - "line 45" not "somewhere in the file"
6. **Include commands** - exact bash/npm commands to run
7. **Update incrementally** - refresh handoff after major progress
8. **Delete when done** - remove handoff after task completion

---

## Example: Good vs Bad Handoff

**❌ Bad (vague, no context):**
```
Working on user authentication. Made some progress.
Need to fix the login bug. Check the auth files.
```

**✅ Good (specific, executable):**
```
Task: Implement JWT refresh token rotation (user requirement: "tokens must auto-refresh")

Progress:
- ✓ Added refreshToken field to User model (`models/User.ts:23`)
- ✓ Created POST /auth/refresh endpoint (`routes/auth.ts:67`)
- ⚠️ In progress: Token rotation logic in `middleware/auth.ts:89-120`

Failed approach:
- Tried storing refresh tokens in Redis - failed because Redis instance
  resets on deploy (confirmed with DevOps). Don't retry this.

Next step:
1. Open `middleware/auth.ts:89`
2. Replace Redis call with database query: `User.findOne({refreshToken})`
3. Test with: `npm test -- auth.refresh.spec.ts`
4. Expected: Test "should rotate refresh token" passes

Why start here: Token rotation is blocking login flow (Priority 1).
Database approach confirmed working in staging environment.
```

