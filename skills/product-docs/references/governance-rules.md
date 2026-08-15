# Architecture, Data, Route, And Delivery Governance

Apply only the sections relevant to the product and its current lifecycle mode.

## Decision Authority

Keep human authority over requirements, priorities, success criteria,
decisions about whether observed progress is sufficient, product-scope
completion, acceptance, and materially irreversible product, security, legal,
financial, or data-authority choices. Agents handle reversible technical
decisions, implementation, review, verification, evidence, and evidence-backed
measurement, reporting, and status maintenance within those boundaries.
Maintaining observed progress does not confer product completion or acceptance.

Do not make routine architecture review a permanent human approval gate.
Escalate when a decision materially changes the authority above, creates a
security or recovery risk, or blocks acceptance.

## Ownership And Writers

For each meaningful data class, name one authority and its permitted writers.
Possible classes include:

```text
source or raw evidence
processed derivatives
canonical records
published outputs or snapshots
runtime state
credentials and local configuration
```

Do not allow an adapter, consumer, model, or presentation layer to write
canonical records without an explicit contract. Keep the authoritative writer
and its readback/verification path identifiable. Treat external and model-
produced inputs as untrusted until the owning boundary validates them.

## Storage, Provenance, And Recovery

Use version control when records are reviewable, reasonably sized, and benefit
from diff, history, synchronization, and rollback. Use external storage when
data is large, binary, high-churn, private, secret, operational, cached,
indexed, logged, or transient.

For transformations where traceability matters, retain the applicable subset:

```text
stable input identity and source reference
input integrity evidence
attachment or dependency references
processor identity and version
processing steps, status, and limitations
output identity and integrity evidence
```

Preserve source evidence according to its authority policy. Keep derivatives
reproducible where feasible. Deleting or rebuilding derivatives, indexes, views,
or outputs must not delete or alter authoritative inputs, human judgments, or
relationships. Protect important external data with suitable backup, retention,
integrity checking, and isolated recovery evidence. Restore from a consistent
snapshot into a separate root before claiming recovery; do not automatically
switch or overwrite the active root. Quarantine or clearly mark
incomplete, failed, restricted, or provenance-free results rather than silently
promoting them.

## Route Evidence And Availability

When importing data or integrating providers, record the route's evidence level,
authorization requirement, normal path, fallback, limitations, and next probe.

Track these axes independently when they affect a decision:

```text
route evidence maturity
runtime capability status
authorized user scope
per-object execution result
usage completion and acceptance
```

Use the repository's evidence scale when it has one. Reaching the highest
evidence level does not automatically enable a route at runtime. For one
runtime observation, use mutually exclusive capability states: `enabled` means
the capability is present, intentionally on, and has no known route-level
blocker; `disabled` means it is present but intentionally off; `absent` means it
is not present; `unavailable` means it is present and not intentionally off,
but a route-level operational dependency or external condition currently
prevents use. `not-yet-probed` belongs to evidence maturity and makes no runtime
claim. Do not use `unavailable` for a subject's authorization or an object's
execution result. `inaccessible` belongs to authorized scope or a per-object
execution result and must identify the blocked subject or object; do not
promote it to a global runtime status without route-level evidence. User
deferrals, run denominators, object results, and usage completion belong to
scope, execution, or status records rather than the route registry.

- A search result, repository name, placeholder, fixture, locator-only record,
  or plausible tool name is not real route evidence.
- A fallback or manual recovery path does not prove the normal path.
- Keep evidence maturity, runtime status, authorization, and object results in
  their respective axes instead of treating any one as successful capability.
- Do not enable a route merely because an adapter or interface exists.
- Reconcile any documented runtime mirror against the real command, API,
  provider, or registry rather than letting documentation certify itself.
- Preserve the user-visible reason and actionable gap for a failed or
  unavailable route.

Prefer:

```text
proven existing capability
-> thin invocation or normalization
-> narrow implementation for a demonstrated gap
-> manual fallback when normal routes are unavailable
```

## State, Retry, And Idempotency

For repeated or per-item operations, retain object-level status and reason.
Successful items must survive local failures, cancellation, and retry of other
items. Retry only the affected item or run. Re-collecting unchanged input should
record the observation without manufacturing a new revision, asset, or fact.
Changed input may append a traceable revision; inaccessible, removed, skipped,
and non-retryable failures must remain visible.

## Boundary Decisions And Progressive Hardening

Create a repository, service, protocol, module boundary, or formal handoff only
when a real lifecycle, deployment, access, ownership, release, scale, security,
or consumer boundary requires it. Do not create boundaries solely to mirror
conceptual layers or a generic template. Do not introduce an abstraction before
there is a concrete working caller that justifies it.

Keep implementation modules small, explicitly owned, and replaceable where the
cost is reasonable. Prototype volatile behavior behind narrow contracts, then
harden only after real use stabilizes behavior and the added safety or
performance benefit is demonstrated. Language, framework, library, algorithm,
and file layout should follow product constraints, ecosystem evidence, target
platform, team capability, and measured behavior; this reference does not set a
universal language default.

## Delivery Cadence And Gates

Within a clear scope, batch related work to reveal common patterns and then
converge. Use immediate targeted checks for high-risk changes, shared contracts,
and failures. Run broader gates at deliberate batch checkpoints and before
merge, release, or acceptance.

Keep engineering gates separate from product AC/TC and user acceptance. A gate
may prove ownership, compilation, migration, or integrity without proving the
user workflow. Increase checkpoint frequency when blast radius or failure
signals rise; decrease it when work is repetitive, reversible, and protected by
cheap local checks.

For closure audits, map every requested outcome to its authority and evidence
before accepting a broad green gate. A checker proves only the rules and inputs
it covers; query the live runtime or system of record for live claims. Where a
checker guards important authority or fail-closed behavior, use a targeted
mutation or negative test to confirm that a deliberate defect is rejected.
