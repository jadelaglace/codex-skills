---
name: code-quality
description: Implement or review code against adopted product, architecture, and design contracts; manage function and data correctness, naming, context lifecycles, errors, resources, unit tests, static checks, and code review. Use for code implementation, quality review, test gaps, or repair verification. Return code-level evidence upstream; do not replace architecture, visual, or final product acceptance.
metadata:
  version: "1.0.0"
---

# 代码质量

Receive upstream structure and standards, implement the authorized scope, review
and test it, repair demonstrated defects, and return verifiable deliverables.
Code quality includes correctness, maintainability, and effective verification.

## Receive The Contract

Follow local instructions and recovery rules. Identify the requested mode:
implementation, review, analysis, or repair verification. A review/analysis task
returns findings and does not silently implement or rewrite unrelated code.

Read the affected code, project conventions and commands, relevant callers,
architecture/data contracts, product acceptance, and design constraints when
applicable. Preserve user edits. Resolve materially conflicting or absent
contracts with the responsible upstream layer. Use available evidence to make
routine local choices rather than requiring a full document chain for a small
fix. For direct invocation, capture the necessary behavior and scope in an
existing artifact or task output; do not invent a new architecture authority.

Know the delivery boundary before coding:

```text
Requested behavior and permitted change scope
Adopted contract/design versions and input/output invariants
Applicable test cases, required project gates, and return destination
Known limitations and observable failure conditions
```

Skill workflow routing does not authorize agents, other-task messages, releases,
external writes, or wider data processing. Honor frozen usage rounds: an
observed defect is evidence first, not automatic permission to patch the build.

## Implement And Inspect

Keep the change focused and idiomatic to the existing language/framework. Review
each changed function with meaningful logic, its inputs, outputs, side effects,
and affected call sites. Review unchanged code only as needed to assess a real
dependency or impact. Do not document every line or impose a repository-wide
style migration to finish a bounded task.

- Name values and functions for their domain meaning; make units, identities,
  optionality, mutability, and ownership clear. A name such as `complete` needs
  semantics when several independent completion dimensions exist.
- Keep responsibilities and dependencies understandable; split complexity
  when it obscures invariants, error paths, or testing. Do not invent fixed
  function-length limits when the project has none.
- Validate external/untrusted results at the owning boundary. Enforce the
  adopted writer, integrity, and readiness rules; convenient scripts or views
  must not bypass them. Preserve source data and successful unrelated results.
- Carry cancellation, deadline, identity, and resources through the operation's
  scope; prevent orphan work, stale writes, leaks, unbounded retry, and silent
  error conversion. Distinguish execution/request ctx from Agent working context.
- Implement the project's idempotency, versioning, transaction, and recovery
  semantics. Unchanged input, failed finalization, and unavailable dependencies
  must not fabricate revisions or false ready/success states.

Read [review-and-tests.md](references/review-and-tests.md) for substantial
implementation, review of risky paths, or deciding test adequacy. Apply its
relevant checks; it is not a demand to add every test category to every edit.

If the contract cannot be implemented safely as written, return a concrete
conflict and alternatives to architecture, design, or product. Do not silently
relax accepted behavior, data authority, or quality gates.

## Review, Test, Repair

Review the actual diff and relevant surrounding code separately from writing it.
Check behavior, failure handling, boundary ownership, data invariants, and test
assertions. Fresh review reasoning can reveal defects; writing and rereading
code does not constitute independent review. If independent review is required
but unavailable, report that gap instead of asserting it occurred.

Use the project's lint, type, static-analysis, and test commands appropriate to
the change. Required checks remain required. Add meaningful tests for changed
logic, critical invariants, demonstrated regressions, or a real coverage gap;
avoid mirror tests and unnecessary new tests for low-impact reversible edits.
Choose applicable normal, invalid, boundary, timeout/cancellation, retry,
concurrency, and recovery paths. Do not claim code coverage from a test count.

Execute checks when available and authorized; record command, scope, build/input
identity where relevant, and results. Label proposed/unrun cases explicitly.
For environment failures, separate inability to run a gate from a passing gate.
A mocked dependency cannot establish real external authorization or availability.

For a defect, state expected versus observed behavior, trigger, impact, evidence,
and affected contract. Repair authorized defects in a bounded set, verify the
regression and affected boundaries, then run the broader checks required by the
blast radius or project workflow. In review-only mode, return these findings
without edits. Do not weaken assertions, exclude the faulty path, swallow errors,
or declare flaky behavior resolved merely to obtain a green result.

Block code-quality passage on a violated required invariant, failed mandatory
gate, unsupported required evidence, or an unresolved blocking review finding.
Report unrelated pre-existing failures with evidence and their impact; do not
repair them outside scope or hide them. Do not merge/release with required gates
unmet. Keep nonblocking limitations visible in the return.

## Return Implementation Upstream

Use the existing project evidence and status roles. A concise return contains:

```text
Implemented/reviewed scope and code/build/contract identity
Changed behavior and deliverable pointers
Review findings: trigger, expected/actual, severity, fix status
Case/check -> expected result -> observed result -> evidence
Unrun checks, failures, skipped/non-applicable paths, and remaining risks
Responsible upstream layer and next action for each unresolved gap
```

Return implementation and code-level verification to `architecture` when
available. For visual changes, also return the actual rendered output and
relevant states to `design-standards`; screenshots alone do not prove interface
behavior. Product-scope conflicts return to `product-docs`. Invoke these
workflows only when the task needs them and they are available; use project
contracts directly otherwise and identify material evidence gaps.

Code tests and review prove their covered mechanisms. Architecture owns
functional-unit/integration acceptance, design owns applicable visual acceptance,
and product owns overall outcome verification with the user's final acceptance.
Keep those conclusions distinct.
