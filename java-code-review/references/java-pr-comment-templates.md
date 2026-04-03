# Java PR Comment Templates

Use concise, evidence-driven language. Replace placeholders.

## Critical / High

- `[High] Missing null guard can trigger runtime failure`
- `Location: <path>:<line>`
- `Why it matters: <impact on users/data/reliability>`
- `Evidence: <failing branch or execution path>`
- `Fix: <specific change>`
- `Tests: add <test-name> for <scenario>`

## Medium

- `[Medium] Transaction boundary may allow partial updates`
- `Location: <path>:<line>`
- `Why it matters: <consistency risk>`
- `Evidence: <sequence showing inconsistency>`
- `Fix: <transaction scope or rollback rule>`
- `Tests: add integration test for <rollback case>`

## Low

- `[Low] Method contract is ambiguous for empty input`
- `Location: <path>:<line>`
- `Why it matters: <future bug risk>`
- `Evidence: <unclear branch or return>`
- `Fix: <clarify contract or rename method>`
- `Tests: add unit test for empty input behavior`

## No Findings

- `No material findings.`
- `Residual risk: <areas not exercised by tests or missing context>`
