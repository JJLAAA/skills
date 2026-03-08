---
name: handoff
description: This skill should be used when the user requests to save progress, pause work, create a handoff document, or says "保存进度", "handoff", "暂停", "checkpoint". It enables zero-loss context transfer across coding sessions by maintaining structured HANDOFF.md and optional CHECKPOINT.md files in the workspace directory. Use this skill at the end of a session or when approaching context limits to preserve work state for the next session.
---

# Handoff

## Overview

Enable zero-loss context transfer across coding sessions by maintaining structured state documents in the workspace. This skill implements a Code Relay-inspired HANDOFF mechanism that saves work progress, allowing the next session to quickly restore full context without information loss.

**Key benefit:** Unlike auto-compression which loses critical details, HANDOFF provides structured, recoverable state snapshots that the next session can use to continue work seamlessly.

---

## When to Use This Skill

**Trigger keywords (any of these):**
- "保存进度" / "save progress"
- "handoff" / "HANDOFF"
- "暂停" / "pause"
- "checkpoint"
- "保存状态" / "save state"
- "交接" / "hand over"

**Proactive triggers:**
- Conversation is approaching context limit
- Complex task that will span multiple sessions
- End of work session
- Before switching to another task

---

## Workflow

### Step 1: Determine Workspace Location

Check for workspace directory in the following order:

1. User-specified workspace path
2. `./workspace/` (current directory)
3. Project root workspace directory
4. Ask user to confirm location

### Step 2: Gather Current State

Before writing HANDOFF, collect:

- **Completed work** — What features/functions are done
- **In-progress work** — What's currently being worked on
- **Next steps** — What to do next
- **Gotchas and pitfalls** — Problems encountered and their solutions
- **Branch status** — Current git branch and commit SHA
- **Files modified** — List of changed files

### Step 3: Write HANDOFF.md

Write to `{workspace}/HANDOFF.md` using the structured format below.

### Step 4: (Optional) Write CHECKPOINT.md

For more detailed state snapshots, also write `{workspace}/CHECKPOINT.md`. Use this when:
- Context is extremely tight
- Complex task with many sub-components
- Need to preserve design decisions and reasoning

### Step 5: Confirm and Report

Confirm to user that handoff is complete, showing the file location and a brief summary.

---

## HANDOFF.md Format

```markdown
# HANDOFF

**Session Date:** YYYY-MM-DD HH:MM
**Branch:** `branch-name` @ `commit-sha`

---

## Completed

- [x] Feature/task 1 — description
- [x] Feature/task 2 — description

## In Progress

- [ ] Task name — brief description of what's being done

## Next Steps

1. First next action
2. Second next action
3. Third next action

## Gotchas & Pitfalls

- **Issue description** — Solution approach
- **Another problem** — How it was resolved

## Files Modified

- `path/to/file1.ts` — changes made
- `path/to/file2.ts` — changes made

## Branch Status

- Current branch: `feature/xxx`
- Latest commit: `abc123...`
- Committed: Yes/No
- Pushed: Yes/No

---

## Notes for Next Session

Any additional context, design decisions, or important notes for continuing the work.
```

---

## CHECKPOINT.md Format (Optional)

More detailed snapshot for complex tasks:

```markdown
# CHECKPOINT

**Created:** YYYY-MM-DD HH:MM
**Branch:** `branch-name` @ `commit-sha`

---

## Task Overview

[Full task description and objectives]

---

## Architecture & Design

[Key architectural decisions, design patterns chosen]

---

## Implementation Progress

### Module 1: Status
- Completed: ...
- Remaining: ...

### Module 2: Status
- Completed: ...
- Remaining: ...

---

## Technical Details

[Database schema changes, API modifications, etc.]

---

## Dependencies & Relationships

[How different components interact]

---

## Testing Status

- Unit tests: ...
- Integration tests: ...
- Manual testing: ...

---

## Open Questions

[Unresolved issues or decisions pending]
```

---

## Session Startup: Reading HANDOFF

When starting a new session:

1. **Check for existing HANDOFF.md** in workspace
2. **If found:** Read and display summary to user
3. **Ask user:** "Continue from previous session? [Y/n]"
4. **If yes:** Use HANDOFF content to restore context and continue work

### Startup Summary Format

```
Found previous HANDOFF (YYYY-MM-DD):

Branch: feature/xxx @ abc123

Completed:
- Feature 1
- Feature 2

In Progress:
- Task being worked on

Next Steps:
1. First next action
2. Second next action

Continue from this session? [Y/n]
```

---

## File Communication Principle

**Critical:** Always write large content to files, not into the conversation.

- HANDOFF/ CHECKPOINT files are the mechanism for state transfer
- Keep conversation minimal — just confirm file was written
- Reference file paths rather than duplicating content

This protects the context window and ensures state is recoverable.

---

## Tips

1. **Be specific** — Include concrete file paths, function names, commit SHAs
2. **Document decisions** — Note why certain approaches were chosen
3. **List failures** — What didn't work is as important as what did
4. **Keep it updated** — Update HANDOFF after significant progress
5. **Delete when done** — Remove HANDOFF/ CHECKPOINT after task completion

---

## Resources

### workspace/
Directory for HANDOFF.md and CHECKPOINT.md files. This directory should exist at the project root or designated workspace location.
