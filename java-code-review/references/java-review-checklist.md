# Java Review Checklist

Use this checklist after scoping changes. Apply only relevant sections.

## 1. Correctness and Domain Rules

- Verify domain invariants are preserved across all branches.
- Verify conversion/rounding rules for money, units, and timestamps.
- Verify behavior for empty collections, null values, and invalid IDs.
- Verify pagination, sorting, and filtering logic for off-by-one issues.

## 2. Nullability and Type Safety

- Verify `Optional` is not used as a field/parameter anti-pattern unless intentional.
- Verify nullable inputs are guarded before dereference.
- Verify generic types are explicit where raw types could hide ClassCast issues.

## 3. Exceptions and Error Semantics

- Verify exceptions preserve root cause and actionable context.
- Verify code does not swallow exceptions silently.
- Verify checked vs unchecked exception choices match caller recovery expectations.
- Verify retries do not mask non-retryable errors.

## 4. Concurrency and Async

- Verify shared mutable state is synchronized or avoided.
- Verify lock acquisition order is consistent.
- Verify async tasks propagate cancellation/interruption appropriately.
- Verify executor sizes and queue policies cannot deadlock critical paths.

## 5. Resource and Lifecycle Management

- Verify streams/files/sockets are closed with try-with-resources.
- Verify DB connections and cursors are not leaked on failure paths.
- Verify thread pools and schedulers have clear ownership and shutdown behavior.

## 6. Persistence and Transactions

- Verify transaction boundaries align with consistency requirements.
- Verify isolation and locking behavior for update/read races.
- Verify ORM mappings and fetch strategies avoid N+1 hot paths.
- Verify migration or schema assumptions are explicit.

## 7. Security and Privacy

- Verify authorization checks happen server-side and before state changes.
- Verify untrusted input is validated and encoded where needed.
- Verify SQL/JPQL/native queries are parameterized.
- Verify logs avoid secrets, tokens, and sensitive PII.

## 8. Performance and Scalability

- Verify algorithmic complexity on expected data sizes.
- Verify expensive operations are not inside hot loops.
- Verify object churn, boxing, and stream overuse in critical paths.
- Verify caching and invalidation behavior is correct under concurrency.

## 9. API and Design Quality

- Verify public API changes preserve compatibility expectations.
- Verify method names and return semantics are unambiguous.
- Verify side effects are explicit, especially across service boundaries.
- Verify duplicated logic is not introduced across modules.

## 10. Test Quality

- Verify tests cover success, failure, and boundary cases.
- Verify at least one regression test for each high-risk fix.
- Verify assertions check behavior, not only interaction counts.
- Verify test fixtures are deterministic and isolated.
