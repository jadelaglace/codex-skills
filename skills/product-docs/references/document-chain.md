# Document Authority And Shape

Discover the repository's existing authority chain and map files to roles. Do
not rename, renumber, split, or multiply a working chain merely to match this
reference.

## Authority Roles

| Role | Must answer | Must not silently become |
| --- | --- | --- |
| Raw intent evidence, when used | What did the user directly say and when? | A full transcript, Agent interpretation, or external advice |
| Current requirements | What outcome and constraints govern the product now? | Architecture, task order, or transient status |
| Product behavior or PRD | Who uses it and what observable behavior do they receive? | Code layout or storage internals |
| Acceptance | What observable result proves success or failure? | Test implementation or routine approval ceremony |
| Design specification, when applicable | How does an interface support usable and accessible task completion? | Backend internals or invented interface scope |
| Architecture and ownership | Which lasting boundaries, authorities, contracts, and dependencies enable acceptance? | Phase estimates or product intent invented for convenience |
| Plan and live status | What is the order, current position, next step, risk, and blocker? | New product behavior or a second acceptance authority |
| Verification and evidence | How was each acceptance or engineering claim tested or demonstrated? | Unadopted architecture alternatives or a competing live status |

Repositories may combine roles when their authority, reader, and update cadence
are the same. They may separate them when those boundaries differ.

## Make The Document Contract Discoverable

For each important authority, make these facts easy to find:

```text
purpose and core question
what it owns and does not own
upstream authority
downstream consumers
what kind of change should update it
whether content is current truth, live status, or historical evidence
```

Express the contract through an index, opening paragraph, headings, or links.
Do not repeat a formal template when the boundary is already obvious.

## Split Or Combine Deliberately

Split when at least one durable boundary makes independent reading or updating
safer:

- a different decision authority owns the content;
- a different primary reader needs it;
- it changes at a materially different cadence;
- history or detailed evidence obscures the current decision path;
- one section has become a reusable contract consumed independently.

Keep material together when it shares authority, reader, and cadence, and when
splitting would force the reader to reconstruct one decision across many small
files. Do not use line count alone as a split rule. Use headings, a concise
current-state summary, navigation, and appendices before creating fragments.

Do not merge semantically different roles merely to reduce file count. A large
but well-navigated authority can be better than many tiny documents; a short
file with two competing authorities can still be wrong.

## Keep One Primary Authority Per Fact

- Store live progress in one primary status source.
- Store observable completion criteria in acceptance.
- Store test procedure and results in verification or evidence records.
- Store stable ownership and data boundaries in architecture.
- Reference or summarize these facts elsewhere without creating competing
  editable copies.

A referenced summary may repeat enough context to be useful, but it must make
the primary authority and update direction clear.

## Propagate By Impact

1. Start at the highest role whose meaning changed.
2. Inspect only downstream roles that could be affected.
3. Update a document when its semantics, contract, status, or evidence changed.
4. Record important reviewed-but-unchanged roles in the delivery report.
5. Never manufacture edits solely to prove the chain was visited.

## Keep Traceability Proportional

Use existing identifiers and links where available. Trace product behavior to
requirements, acceptance to behavior, architecture/design to the acceptance
they enable, live status to the applicable acceptance or gate, and evidence to
the claim it proves.

Traceability should expose drift and support decisions. Do not create an
identifier, matrix, or link when it adds ceremony without reducing ambiguity or
verification risk.
