# Architecture And Data Governance

Read this reference only when architecture, ownership, storage, provenance,
security, recovery, repository/service topology, or an acceptance-enabling
contract is in scope.

## Keep Architecture At The Right Level

Architecture should explain stable information flow, ownership, permitted
dependencies, data authority, irreversible boundaries, and contracts required
for acceptance. It should not become a live task plan, file inventory, framework
comparison, or record of every reversible implementation choice.

Preserve an established architecture unless evidence shows that it blocks
acceptance, violates an authority boundary, creates material security or
recovery risk, or no longer matches a real lifecycle or deployment boundary.

## Decision Authority

Keep human authority over requirements, priorities, progress judgment, success,
final acceptance, and materially irreversible product, security, legal,
financial, or data-authority choices. Let Agents own reversible architecture and
implementation decisions within those boundaries.

Do not make routine architecture review a permanent human gate. Escalate when a
decision changes the authority above or blocks acceptance.

## Ownership And Writers

For each meaningful data class, identify one authority and its permitted
writers. Relevant classes may include:

```text
source or raw evidence
processed derivatives
canonical records
published outputs or snapshots
runtime state
credentials and local configuration
```

Do not let an adapter, consumer, model, or presentation layer write canonical
records without an explicit contract. Treat external and model-produced inputs
as untrusted until the owning boundary validates them.

## Storage, Provenance, And Recovery

Use version control for reviewable, reasonably sized records that benefit from
diff, history, synchronization, and rollback. Use external storage for large,
binary, high-churn, private, secret, operational, cached, indexed, logged, or
transient data.

For transformations where traceability matters, retain the applicable subset:

```text
stable input identity and source reference
input integrity evidence
attachment or dependency references
processor identity and version
processing status and limitations
output identity and integrity evidence
```

Protect important external data with proportionate backup, retention, integrity
checks, and recovery evidence. Mark incomplete, failed, restricted, or
provenance-free results explicitly instead of promoting them silently.

## Create Boundaries Only For Real Reasons

Create a repository, service, protocol, module boundary, or formal handoff only
when a real lifecycle, deployment, access, ownership, release, scale, security,
or consumer boundary requires it. Do not create boundaries solely to mirror a
conceptual diagram or generic template.

Keep volatile behavior replaceable behind narrow contracts when the cost is
reasonable. Harden it after real use stabilizes behavior and the added safety or
performance benefit is demonstrated.

Treat language, framework, library, algorithm, file layout, and local interface
choices as implementation details unless they materially affect deployment,
ownership, security, recovery, interoperability, long-term maintenance, or an
acceptance-enabling contract. Optimize volatile work for feedback speed and
ecosystem fit; reserve costly hardening for measured performance, safety,
data-authority, or long-lived stable boundaries.
