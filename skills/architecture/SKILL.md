---
name: architecture
description: Design or review software architecture, technology choices, functional units, interfaces, data ownership, non-functional targets, and test strategy; issue implementation contracts and verify returned functional-unit and integration evidence. Use for technical design, architecture review, or acceptance of implemented system boundaries. Product intent and final product acceptance remain upstream; code implementation and visual standards belong to their specialist workflows.
metadata:
  version: "1.0.0"
---

# 架构工程

Translate product goals into implementable, testable system contracts. Close the
loop from technical choices and functional-unit instructions to verification of
returned implementation, then return conclusions and evidence upstream.
A functional unit is a user-relevant capability or system responsibility, not
necessarily a function, package, service, or unit test.

## Establish Scope And Authority

Follow the workspace's instructions and recovery hook before selecting work.
Read only the relevant requirements, product acceptance, adopted architecture,
and applicable design constraints. Use existing document roles and identifiers.
Keep proposals distinct from adopted contracts and runtime availability.

Identify whether the request authorizes analysis, design, review, verification,
or implementation. Analysis/review does not authorize implementation, external
writes, or a new deployment. Work directly when the upstream scope is clear;
ask only about missing decisions that materially change the result. If product
goals are genuinely unclear, return the ambiguity upstream rather than inventing
requirements. Routine reversible technical choices need no new approval.

For direct invocation without product documents, capture the smallest sufficient
goal, observable success conditions, and constraints in the existing planning
artifact; a full PRD is not a prerequisite for a bounded architecture question.

## Design And Issue Contracts

1. Map the affected outcomes to functional units, existing callers, and system
   boundaries. Reuse an adequate architecture; introduce a service, repository,
   protocol, or abstraction only for a demonstrated lifecycle, deployment,
   ownership, security, scale, or consumer need.
2. Check proven existing APIs, exports, maintained tools, and local capabilities
   before designing custom adapters or protocols. Compare viable routes against actual constraints: target platform,
   ecosystem/tool availability, compatibility, cost, performance, security, and
   recovery. Record the chosen option and material tradeoffs at the existing
   architecture authority. Preserve credible alternatives when the decision is
   still open; do not manufacture an option catalogue for a small known fix.
3. For each affected boundary, define responsibilities, allowed dependencies,
   input/output contracts, identities, permitted writers, invariants, error
   semantics, cancellation, and retry rules at the level the risk requires.
   Inspect external results at the owning boundary before admitting them.
4. Define applicable performance, reliability, security, observability, and
   recovery targets with a threshold, measurement
   conditions, and failure criterion. Use project requirements or measured
   constraints; label proposed targets and unresolved thresholds explicitly.
5. Specify verification before implementation: product outcome -> affected
   contract -> case and expected result -> evidence -> return destination.
   Read [verification-and-data.md](references/verification-and-data.md) when
   designing a test matrix, data/recovery boundary, or returned-result gate.
6. Review the design for missing ownership, incompatible interfaces, untested
   failure paths, migration/recovery risk, and divergence from acceptance.
   Issue an implementation scope with contract references, permitted changes,
   applicable design standards, acceptance cases, and blocking conditions.

Keep this handoff in existing documents or task output. A useful small form is:

```text
Outcome and functional-unit scope
Adopted contract/design versions and allowed changes
Inputs, outputs, ownership, invariants, failure/recovery semantics
Cases, expected results, applicable thresholds and evidence required
Known limitations and return destination
```

For implementation within the authorized task, locate and read `code-quality`
when available. Use `design-standards` when visual standards or actual visual
acceptance matter. Skill routing is workflow selection, not authority to create
an agent, message another task, publish, or expand scope. If a specialist is
missing, use available methods and identify any material verification gap.

## Receive And Verify Functional Units

On return, reconcile the delivered scope, build/configuration identity, inputs,
contract versions, changes, review findings, and evidence. Review the actual
implementation at relevant boundaries; a self-reported green result is not
proof. Reuse adequate recorded evidence, rerunning only when it is missing,
stale, mismatched, or insufficient for the claim.

Verify functional-unit behavior and interactions across units, including the
applicable data, error, authorization, and non-functional contracts. Unit tests
can prove code mechanisms; they cannot by themselves prove integration,
external route availability, or a complete user workflow. For a live-path claim,
use a real authorized path or report the unproven dependency. Never treat mocks,
an adapter name, a successful command, or a locator as proof of that path.

Return implementation defects to the implementation work, contract/integration
defects to architecture, visual defects to design, and requirement conflicts to
product. Verify repairs against the affected cases and run the broader gates
required by the impact. Within a frozen usage round, record observed defects
without silently changing the build or contracts; follow the owning process
for promotion to a repair round.

Do not pass a required contract with failed or missing evidence. Keep the failed
or blocked unit explicit while preserving unrelated successes. A limitation
accepted by the authorized decision maker remains visible; it is not a passed
test. Do not merge or release on failed required gates.

## Return Upstream

Return a concise result using the project's existing evidence/status authority:

```text
Scope and implementation/input/contract identity
Functional-unit and integration results: passed / failed / partial / skipped / blocked
Claim -> case -> observed result -> evidence pointer
Architecture Review conclusions and applicable non-functional measurements
Remaining gaps, limitations, responsible layer, next action
```

Report what the implemented system can now do and under which conditions.
Functional acceptance returns to `product-docs` when available; relevant visual
results also return to design. Do not claim whole-product completion or user
acceptance from this layer. Do not create a second product/status authority.
