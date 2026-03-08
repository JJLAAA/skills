# Troubleshooting

Common issues encountered when creating, testing, or deploying skills.

## Upload / Packaging Failures

**Symptom:** `package_skill.py` reports validation errors.

**Common causes:**
- Missing or malformed YAML frontmatter (must start with `---`)
- `name` field doesn't match directory name
- `description` contains angle brackets or exceeds 1024 characters
- `SKILL.md` has wrong casing (e.g., `Skill.md`, `skill.md`)
- A `README.md` exists in the skill root directory

**Fix:** Run `quick_validate.py <skill-dir>` to see specific errors and warnings, then address each one.

## Skill Does Not Trigger

**Symptom:** The skill exists but Claude doesn't activate it when expected.

**Common causes:**
- `description` is too vague or too short (aim for 50+ characters)
- Missing key trigger phrases or domain keywords in description
- Description uses first/second person instead of third person

**Fix:** Rewrite the description using the formula: `[What it does] + [When to use it] + [Key capabilities]`. Include specific terms users would mention.

## Skill Over-Triggers

**Symptom:** The skill activates on unrelated requests.

**Common causes:**
- Description is too broad or generic
- Trigger keywords overlap with common terms

**Fix:** Narrow the description scope. Add specificity about when the skill should NOT be used if needed.

## MCP Connection Issues

**Symptom:** Skill instructions reference MCP tools that fail or are unavailable.

**Common causes:**
- MCP server not configured in the user's environment
- Tool names in SKILL.md don't match actual MCP tool names
- Server requires authentication that isn't set up

**Fix:** Document MCP server requirements in the `compatibility` frontmatter field. Include setup instructions in SKILL.md or a references file.

## Instructions Not Being Followed

**Symptom:** Claude ignores or partially follows SKILL.md instructions.

**Common causes:**
- Instructions are too long or buried in dense text
- Conflicting instructions within the skill
- SKILL.md exceeds recommended 5k word limit, causing important details to be lost

**Fix:** Restructure SKILL.md to put critical instructions first. Move detailed reference material to `references/` files. Use clear headings and bullet points.
