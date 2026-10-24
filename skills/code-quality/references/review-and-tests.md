# Review And Test Adequacy

Choose checks from the actual contract and risk. Language-specific rules come
from the repository's adopted tooling and conventions, not a universal style.

## Review Meaningful Implementation Details

| Concern | Inspect | Useful failure evidence when applicable |
| --- | --- | --- |
| Function responsibility | Inputs/outputs, side effects, call sites, coupling and branching | Behavior-level tests of meaningful branches, rather than duplicating statements |
| Types and naming | Identity vs content hash, units, optionality, ownership, mutable aliases | Wrong-unit, missing-value, cross-identity, or aliasing input |
| Request/execution ctx | Deadline propagation, cancellation checks, child work lifetime, cleanup | Cancel/timeout before and during external work and before durable promotion |
| Agent context | Sources, effective decisions, scope isolation, compact recovery pointer | Stale input or recovery cannot authorize unrelated work or replay a terminal task |
| Errors and retries | Error provenance, retryability, bounds/backoff, idempotency, partial success | A transient failure retries only affected work; permanent failure retains cause |
| Resource and concurrency | Files/streams, locks, transactions, task joins, races, ordering | Fault or cancellation closes resources; competing writes cannot violate invariants |
| Data and readiness | Permitted writer, validation, stable identity, revisions, durable bytes | Corrupt/missing asset or failed finalization cannot create ready state |
| Compatibility | Public interfaces, migration, existing consumers and rollback | Old caller/data plus new code remains compatible or an explicit migration is verified |

Recollection deserves tests for unchanged, changed, inaccessible, removed, and
skipped cases when the product supports them. Equal bytes may have multiple
contextual occurrences; deduplication must preserve the adopted relationship
contract. Verify required assets and compound-object pairing, not just the main
body hash. Repeated retry must not create duplicate revisions or success records.

For transaction-like flows, inject failures at meaningful stage/write/finalize/
readback boundaries. Verify durable state as well as the returned error. A mock
return value alone does not prove there are no orphan or falsely ready records.
Tests must stay isolated from live stores unless that real path is authorized.

## Make Assertions Carry Meaning

Map each important case to the contract or invariant it proves. Assert relevant
values, persisted effects, forbidden effects, and explicit failure states;
`does not throw`, exit zero, or a file's presence often proves too little.

For an important validator or fail-closed guard, corrupt the value, remove a
required dependency, or change the identity and confirm rejection. Check the
checker against meaningful defects when a false positive would admit bad data.
Property-based or mutation testing is useful for a demonstrated invariant or
assertion weakness; it is not automatically required for every change.

Unit tests isolate code behavior; contract/integration tests verify boundary
interactions. Real authorized-path evidence validates actual dependencies and
user-observable outputs. Report these levels separately. Artifact completeness
may require duration/streams, final message ranges, all required attachments,
hashes, readable links, or isolated recovery, depending on the actual contract.

Keep the project's coverage threshold and measurement configuration. Report the
denominator and exclusions when making a coverage claim. New targets need a
project-specific rationale; high coverage does not remove the need to inspect
assertions or omitted failure paths. Never generate one test per line merely to
inflate coverage.

## Review And Gate Decisions

Report findings in impact order with location and evidence. A finding should
explain the concrete trigger, violated behavior, consequence, and repair or
needed decision. Avoid treating personal stylistic preference as a correctness
defect. Inspect the entire relevant change, including meaningful function,
variable, data, and case details; a generic “looks good” is not a review result.

Stop the affected promotion for data loss/corruption, authorization or writer
bypass, broken required behavior, false readiness, failed mandatory checks, or
missing evidence for a required gate. Preserve independent successful work.
Return architecture/design/product conflicts to their owning layer rather than
redefining the contract in code. Repaired code needs affected-case verification
and the project-required broader gates before return or promotion.

These checks generalize Babata's asset admission, idempotent recollection,
partial failures, integrity checks, and frozen-round discipline. They do not
mandate Rust, SQLite, numbered data classes, or the project's exact commands.

## Assertion Forms And The Minimum Edge Set

When turning a case into an assertion, three forms cover most of it:

- exit and status: the command or endpoint succeeded, with the expected code;
- value comparison: a measured or returned value against a threshold, with the
  tolerance stated;
- structure: the required keys, fields, or elements exist and the prohibited ones
  do not.

Order the edge set the way failures actually happen: empty input, boundary or
extreme value, failing dependency, then the normal path. Recording a case without
its expected result is not a case; recording a result without the command that
produced it is not evidence.
