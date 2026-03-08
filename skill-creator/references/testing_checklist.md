# Testing Checklist

Structured testing process for validating skills before and after deployment.

## Pre-Development Checks

- [ ] Skill name follows hyphen-case convention
- [ ] Skill name does not contain reserved words ("claude", "anthropic")
- [ ] Clear understanding of 5+ concrete usage examples
- [ ] Identified which resources (scripts/references/assets) are needed

## During Development Checks

- [ ] SKILL.md frontmatter has valid `name` and `description`
- [ ] Description follows the formula: [What] + [When] + [Capabilities]
- [ ] Description is 50–1024 characters
- [ ] No angle brackets in description
- [ ] SKILL.md body uses imperative/infinitive writing style
- [ ] No residual [TODO] placeholders remain
- [ ] No empty resource directories
- [ ] No README.md in skill root

## Post-Development Checks

- [ ] `quick_validate.py` passes with zero errors
- [ ] `package_skill.py` creates zip successfully
- [ ] All warnings reviewed and addressed (or intentionally accepted)

## Trigger Testing

Test that the skill activates (and doesn't activate) correctly:

### Positive Triggers (5+ required)
- [ ] Direct request using skill's primary function
- [ ] Indirect request implying the skill's domain
- [ ] Request using domain-specific keywords
- [ ] Request with a file type the skill handles
- [ ] Variation in phrasing / different wording

### Negative Triggers (3+ required)
- [ ] Unrelated request in a different domain
- [ ] Request with superficially similar but different intent
- [ ] Ambiguous request that should NOT trigger this skill

## Functional Testing

- [ ] Each core workflow executes end-to-end without errors
- [ ] Scripts run successfully in the target environment
- [ ] References are loaded when needed (not eagerly)
- [ ] Output quality matches expectations
- [ ] Edge cases produce reasonable behavior

## Quality Targets

| Metric | Target |
|--------|--------|
| Trigger accuracy | >= 90% on positive test cases |
| Failed tool calls | Zero failures caused by skill instructions |
| User corrections | None needed for standard workflows |
| Context efficiency | SKILL.md body < 5k words |

## Iteration Signals & Fixes

| Signal | Likely Fix |
|--------|-----------|
| Skill does not trigger | Improve `description` with more trigger phrases |
| Triggers on wrong requests | Narrow `description` scope |
| Produces incorrect output | Update SKILL.md instructions or fix scripts |
| Misses edge cases | Add examples or decision trees |
| Context window too large | Move content to `references/` |
| Scripts fail in some environments | Add `compatibility` field, document dependencies |
