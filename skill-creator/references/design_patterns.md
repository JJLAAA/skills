# Design Patterns

Common design patterns for structuring skills effectively.

## 1. Sequential Workflow Orchestration

**When to use:** The skill guides Claude through a multi-step process with a defined order.

**Example use cases:** Document generation, data pipeline execution, deployment workflows.

**SKILL.md skeleton:**
```markdown
## Workflow
### Step 1: Gather Inputs
Collect required parameters from the user...
### Step 2: Process
Run scripts/process.py with the collected inputs...
### Step 3: Validate Output
Check the output against expected criteria...
### Step 4: Deliver
Present results to the user...
```

**Key tips:**
- Include decision points where the workflow may branch
- Reference scripts for deterministic steps
- Keep each step focused on a single responsibility

## 2. Multi-MCP Coordination

**When to use:** The skill coordinates multiple MCP servers to accomplish a task.

**Example use cases:** Fetching data from one API, processing it, then storing results in another system.

**SKILL.md skeleton:**
```markdown
## Available MCP Servers
- `database-server`: Query and update the database
- `notification-server`: Send alerts and notifications

## Workflow
1. Query data using `database-server`
2. Process and transform results
3. Send summary via `notification-server`
```

**Key tips:**
- Document each MCP server's purpose and available tools
- Specify the data flow between servers
- Include fallback behavior if a server is unavailable

## 3. Iterative Refinement

**When to use:** The skill produces output that benefits from multiple rounds of improvement.

**Example use cases:** Content writing, code generation with testing, image editing with feedback.

**SKILL.md skeleton:**
```markdown
## Workflow
### Initial Generation
Produce a first draft based on user requirements...
### Review Cycle
Present output to user, collect feedback...
### Refinement
Apply feedback and regenerate...
### Completion
Confirm final output meets requirements...
```

**Key tips:**
- Define clear quality criteria for "done"
- Limit refinement rounds (suggest a maximum)
- Preserve context between iterations

## 4. Context-Aware Tool Selection

**When to use:** The skill must choose different tools or approaches based on the input context.

**Example use cases:** File format handling (PDF vs DOCX vs image), environment-specific workflows.

**SKILL.md skeleton:**
```markdown
## Decision Tree
### Input Analysis
Determine the input type and context...

### If PDF file → Use PDF workflow
Run scripts/process_pdf.py...

### If DOCX file → Use DOCX workflow
Run scripts/process_docx.py...

### If unknown → Ask user for clarification
```

**Key tips:**
- Use clear decision trees or flowcharts
- Document each branch's prerequisites
- Include a fallback for unrecognized inputs

## 5. Domain Expertise

**When to use:** The skill encodes specialized knowledge that Claude doesn't inherently possess.

**Example use cases:** Company-specific coding standards, proprietary API usage, industry regulations.

**SKILL.md skeleton:**
```markdown
## Domain Knowledge
### Key Concepts
Define domain-specific terms and relationships...

### Rules & Constraints
Business rules that must always be followed...

### Common Patterns
Frequently used patterns with examples...
```

**Key tips:**
- Store detailed reference material in `references/` to keep SKILL.md lean
- Include concrete examples for each rule or pattern
- Document exceptions and edge cases explicitly
