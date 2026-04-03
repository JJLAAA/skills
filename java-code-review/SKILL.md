---
name: java-code-review
description: Structured Java code review workflow focused on finding high-impact defects, regressions, and missing tests in Java pull requests. Use when reviewing Java code changes, preparing PR feedback, auditing risky refactors, or requesting prioritized findings with severity, file and line references, and concrete remediation guidance.
---

# Java Code Review

## Goal

Apply a risk-first review process for Java changes and return actionable findings that prevent production defects.

## Required Review Posture

- Prioritize bug risk, regressions, security, and missing tests over style nits.
- Cite concrete evidence from code paths, control flow, contracts, and edge cases.
- Include file and line references for every finding.
- State assumptions explicitly when project context is missing.

## Review Workflow

1. Map scope and risk.
- Identify modified modules, entry points, persistence boundaries, external calls, and concurrency surfaces.
- Flag changes touching auth, money, data integrity, caching, retries, async execution, or schema changes as high-risk first-pass targets.

2. Validate correctness and business behavior.
- Trace happy path, failure path, and rollback behavior.
- Check boundary conditions: null, empty, overflow, locale/timezone, precision, and idempotency.
- Verify method and API contracts: preconditions, postconditions, and compatibility.

3. Validate reliability and safety.
- Check exception handling, resource closure, transaction boundaries, retry logic, and timeout behavior.
- Check thread safety for shared mutable state, lock ordering, atomicity, and executor usage.
- Check security controls: input validation, authorization checks, secret handling, injection risk.

4. Validate maintainability and design impact.
- Check naming clarity, method cohesion, abstraction boundaries, and duplicated logic.
- Check whether new code increases coupling or hides side effects.

5. Validate test coverage.
- Verify coverage for main path, edge cases, failures, and concurrency-sensitive behavior.
- Flag missing tests for each high or medium risk finding.

6. Produce prioritized findings.
- Report findings ordered by severity.
- Give minimal but complete remediation guidance.
- Avoid speculative findings without code evidence.

## Severity Rubric

- Critical: Likely production outage, data corruption/loss, auth bypass, or major security exposure.
- High: User-visible functional break, integrity bug, race condition, severe reliability issue.
- Medium: Non-trivial maintainability or performance risk that can become defects.
- Low: Minor clarity, consistency, or low-impact improvements.

## Finding Output Format

Use this structure for each issue:

- `[Severity] <short title>`
- `Location:` `<absolute-or-repo path>:<line>`
- `Why it matters:` concrete impact/risk
- `Evidence:` specific condition/path showing the problem
- `Fix:` concise remediation direction
- `Tests:` missing or required tests to prevent regression

If no issues are found, state: `No material findings.` Then list residual risks or untested areas.

## Review Boundaries

- Do not block on style-only observations unless a style issue obscures correctness or reliability.
- Do not claim framework-specific behavior without verifying the actual code path.
- Do not recommend broad refactors unless directly required to remove a concrete defect risk.

## Resources

- Load `references/java-review-checklist.md` for a detailed category checklist.
- Load `references/java-pr-comment-templates.md` for concise, high-signal comment templates.
