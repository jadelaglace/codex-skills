# Architecture, Data, And Delivery Governance

Apply only the sections relevant to the product and its current lifecycle mode.

## Decision Authority

Keep human authority over requirements, priorities, success, acceptance, and
materially irreversible product, security, legal, financial, or data-authority
choices. Agents handle reversible technical decisions, implementation, review,
verification, evidence, and status maintenance within those boundaries.

Do not make routine architecture review a permanent human approval gate.
Escalate only when the decision materially changes the authority above or blocks
acceptance.

## Ownership Model

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
canonical records without an explicit contract.

## Storage Decision

Use version control when records are reviewable, reasonably sized, and benefit
from diff, history, synchronization, and rollback.

Use external storage when data is large, binary, high-churn, private, secret,
operational, cached, indexed, logged, or transient. Protect important external
data with suitable backup, retention, integrity checking, and recovery evidence.

## Provenance Contract

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
reproducible where feasible. Quarantine or clearly mark incomplete, failed,
restricted, or provenance-free results rather than silently promoting them.

## Boundary Decisions

Create a repository, service, protocol, or formal handoff only when a real
lifecycle, deployment, access, ownership, release, scale, or consumer boundary
requires it. Do not create boundaries solely to mirror conceptual layers or a
generic template.

Keep implementation modules small, explicitly owned, and replaceable where the
cost is reasonable. Prototype volatile behavior behind narrow contracts, then
harden only after real use stabilizes the behavior. Language choice should
follow maturity and evidence: optimize prototypes for feedback speed and
ecosystem fit; reserve costly systems-level hardening for measured performance,
safety, data-authority, or long-lived stable boundaries.

## Delivery Cadence

Within a clear scope, batch related work to reveal common patterns and then
converge. Use immediate targeted checks for high-risk changes, shared contracts,
and failures. Run broader gates at deliberate batch checkpoints and before
merge, release, or acceptance.

The objective is early enough fault detection without imposing a full-suite tax
on every small edit. Increase checkpoint frequency when blast radius or failure
signals rise; decrease it when work is repetitive, reversible, and protected by
cheap local checks.
