# Verification And Data Contracts

Use the applicable sections only. Keep project thresholds and evidence in their
own authority; this reference supplies decision rules, not universal quotas.

## Choose Cases That Prove The Claim

Use an existing case registry or a compact table:

| Claim / contract | Risk or failure | Test level / conditions | Observable expected result | Required gate / evidence |
| --- | --- | --- | --- | --- |
| Functional behavior | Wrong result or missing item | Unit plus functional/integration case as needed | Exact behavior and scope denominator match | Result with build and input identity |
| Cross-boundary contract | Schema, writer, version, or timing mismatch | Contract/integration test at the actual boundary | Valid input accepted; invalid input rejected without false success | Boundary readback and negative evidence |
| External acquisition | Restricted body, expired session, incomplete media | Authorized real-path probe when in scope | Actual body/assets meet the declared completeness conditions | Source/authorization conditions plus artifact measurements |
| Recovery | Missing originals, dangling references, unusable snapshot | Isolated restore/rebuild appropriate to scope | Declared authoritative data and dependencies recover intact | Integrity checks and explicit missing/failed list |

Choose normal, invalid, boundary, timeout/cancellation, retry, concurrency,
authorization, and recovery cases where the contract makes them relevant. Mark
non-applicable cases with a reason; avoid constructing all categories for every
function. Important rejection/integrity gates should have a deliberate invalid
input or fault proving they reject the defect, not merely a positive fixture.

Coverage targets must identify their denominator (lines, branches, critical
paths, contracts, or cases), exclusions, measurement tool, and threshold. Keep
existing mandatory targets. Propose risk-based additions for real gaps; do not
invent a universal percentage or weaken gates to get green. Check assertion
quality separately. Performance/security/recovery targets need similarly clear
conditions and outcomes; unresolved required targets block the relevant claim.

## Data Identity, Writers, And Recovery

For applicable data classes, identify source/raw evidence, canonical records,
human decisions, derivatives, projections, published views, runtime state, and
credentials. Each authoritative class has a named owner and permitted writers.
The physical technology and directory layout remain project-specific.

Where identity and provenance matter, distinguish an external object, its real
content revision, an observation of that object, a byte blob, and each path or
occurrence. Equal bytes need not mean equal contextual objects. Unchanged
recollection must not fabricate a new content revision. Removed or inaccessible
remote content is an observation, not permission to delete retained local data.

For a compound object, define which body and assets are required and how their
pairing, identities, sizes, and integrity are checked. Validate before canonical
admission, then read back durable records and bytes. Stage/commit/finalize/
readback failure must not leave a falsely ready object. Design safe retry,
isolation, and reconciliation for interruptions at these boundaries.

Derived-output cleanup cannot erase authoritative originals, human decisions,
context occurrences, shared references, or successful unrelated results. Define
rebuild inputs and dependencies. For material recovery claims, restore into an
isolated root and verify database compatibility, references, assets, and the
declared integrity scope; do not automatically switch the active root. A sample
proves the sample, not full restore coverage.

## Keep Evidence And State Separate

Keep route maturity, runtime availability, subject authorization, per-object
result, input completeness, processing status, and user acceptance distinct
where these axes matter. A documented or adopted route may still be unavailable.
A local successful fixture does not make a runtime capability enabled.

Define readiness from the actual artifact and owning state, not from process
exit status or remote metadata alone. For example, full-video acceptance needs
the file's measured duration and playable streams; a page showing the full
duration can accompany a downloaded preview. For retained conversations, verify
new identity and complete message/attachment scope while preserving prior local
content. Do not assume the old main conversation ID is still current.

An authorized stop or skip at a processing stage is a valid scoped outcome; it
does not grant permission to advance to the next stage. Preserve successful
items, retry affected items, and expose reasons and retryability.

These rules were informed by Babata's ownership, readback, recollection,
raw-to-view, and isolated-recovery experience. They do not prescribe its storage
classes, languages, sources, historical counts, or product-specific gates.
