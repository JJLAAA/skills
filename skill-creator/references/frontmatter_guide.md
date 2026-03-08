# Frontmatter Guide

Complete reference for YAML frontmatter fields in SKILL.md.

## Required Fields

### `name`

The skill's unique identifier. This is how the skill is referenced internally.

**Rules:**
- Hyphen-case only: lowercase letters, digits, and hyphens (`[a-z0-9-]+`)
- No leading, trailing, or consecutive hyphens
- Must exactly match the skill's directory name
- Must not contain reserved words: "claude", "anthropic"
- Maximum 40 characters recommended

**Examples:**
- `pdf-editor` — good
- `big-query` — good
- `My_Skill` — bad (uppercase, underscores)
- `claude-helper` — bad (reserved word)

### `description`

The primary trigger signal that determines when Claude activates the skill. This is the most important field for skill discoverability.

**Rules:**
- Maximum 1024 characters
- No angle brackets (`<` or `>`)
- Minimum 50 characters recommended for adequate trigger coverage
- Use third-person voice: "This skill should be used when..." not "Use this skill when..."

**Formula:** `[What it does] + [When to use it] + [Key capabilities]`

**Example:**
```yaml
description: >-
  Comprehensive PDF manipulation toolkit for extracting text and tables,
  creating new PDFs, merging/splitting documents, and handling forms.
  When Claude needs to fill in a PDF form or programmatically process,
  generate, or analyze PDF documents at scale.
```

## Optional Fields

### `license`

License information for the skill.

```yaml
license: Complete terms in LICENSE.txt
```

### `allowed-tools`

Restrict which tools the skill can use. If omitted, all available tools are allowed.

```yaml
allowed-tools:
  - Bash
  - Read
  - Write
```

### `compatibility`

Describe environment requirements or constraints. Maximum 500 characters.

```yaml
compatibility: Requires Python 3.9+ and the PyPDF2 library.
```

### `metadata`

Arbitrary key-value pairs for organizational purposes. Not used for triggering.

```yaml
metadata:
  author: Your Name
  version: "1.0"
  category: document-processing
```

## Constraints Summary

| Field | Limit |
|-------|-------|
| `name` | `[a-z0-9-]+`, no reserved words, must match directory |
| `description` | 1024 chars max, no `<` or `>`, 50+ chars recommended |
| `compatibility` | 500 chars max |
| File name | Must be exactly `SKILL.md` (case-sensitive) |
| Directory | Must not contain `README.md` |

## Complete Frontmatter Examples

### Simple (minimal)

```yaml
---
name: code-reviewer
description: This skill should be used when reviewing pull requests or code changes. It provides structured code review workflows with checklist-based analysis.
---
```

### Medium (with optional fields)

```yaml
---
name: data-pipeline
description: >-
  Orchestrates ETL data pipelines using Python and SQL. This skill should be
  used when building, debugging, or optimizing data transformation workflows
  that involve multiple data sources and destinations.
license: MIT
compatibility: Requires Python 3.10+ with pandas and sqlalchemy installed.
---
```

### Full (all fields)

```yaml
---
name: brand-guidelines
description: >-
  Enforces company brand standards across all generated content including
  documents, presentations, and web assets. This skill should be used when
  creating any customer-facing material that must comply with brand identity
  rules covering colors, typography, logos, and tone of voice.
license: Complete terms in LICENSE.txt
compatibility: Requires access to assets/ directory for brand templates.
allowed-tools:
  - Bash
  - Read
  - Write
metadata:
  author: Design Team
  version: "2.1"
  category: brand-compliance
---
```
