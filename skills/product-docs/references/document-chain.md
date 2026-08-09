# Documentation Chain

Discover the repository's existing authority chain and map files to roles. Do
not rename, renumber, split, or multiply a working chain merely to match this
reference.

## Authority Roles

| Role | Must answer | Must not silently become |
| --- | --- | --- |
| Raw intent evidence, when used | What did the user directly say and when? | A full transcript, Agent interpretation, or external advice |
| Requirements / intent | What outcome and constraints govern the product now? | Architecture, task order, or transient status |
| Product behavior / PRD | Who uses it and what observable behavior do they receive? | Code layout or storage internals |
| Acceptance | What observable result proves success or failure? | Test implementation details or routine approval ceremony |
| Design specification, when applicable | How does the interface support usable and accessible task completion? | Backend internals or invented interface scope |
| Architecture / ownership | Which lasting boundaries, authorities, contracts, and dependencies deliver acceptance? | Phase estimates or product intent invented for convenience |
| Delivery process / live status | What mode, order, current position, risk, blocker, and evidence govern delivery now? | New product behavior or a second acceptance authority |
| Verification cases / evidence | How is each acceptance or engineering claim tested or demonstrated? | Unadopted architecture alternatives or competing live status |

Repositories may combine roles when their authority, reader, and update cadence
are the same. Keep the authority direction explicit even when the files differ.

## Make The Contract Discoverable

For each important authority, make these facts easy to find through an index,
opening paragraph, headings, or links:

```text
purpose and core question
what it owns and does not own
upstream authority
downstream consumers
what kind of change should update it
whether content is current truth, live status, or historical evidence
```

## Typical Direction

```text
requirements / intent
  -> product behavior
  -> acceptance
  -> interface design when applicable
  -> architecture and ownership
  -> delivery process and live status
  -> verification and evidence
  -> implementation
```

## One Primary Authority And Honest Status

- Store current requirements in the requirements authority.
- Store live plan and progress in one primary status source.
- Store observable completion criteria in acceptance.
- Store test procedure and results in verification or evidence records.
- Store stable ownership and data boundaries in architecture.
- Reference or summarize these facts elsewhere without competing editable
  copies, and make the update direction clear.
- Keep independent dimensions such as authorization, completeness, processing,
  readiness, availability, and acceptance separate when they affect a decision.
- Keep candidate proposals, experiments, machine suggestions, and adopted
  decisions visibly distinct.

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
current-state summary, navigation, and supplements before creating fragments.

Do not merge semantically different roles merely to reduce file count. A large
but well-navigated authority can be better than many tiny documents; a short
file with two competing authorities can still be wrong.

## Impact-Based Propagation

1. Start at the highest role whose meaning changed.
2. Inspect only downstream roles that could be affected.
3. Update a document only when its semantics, contract, status, or evidence
   changed.
4. Record important reviewed-but-unchanged roles in the delivery report.
5. Never manufacture edits solely to demonstrate that the whole chain was
   visited.

## Raw Intent Evidence

Raw evidence is optional and can be an appendix, decision log, linked source, or
other durable record. When it exists:

- keep direct user wording distinct from external reference and Agent summaries;
- preserve exact wording within selected excerpts;
- include decisions, values, corrections, examples, and useful unresolved
  tension rather than every conversational turn;
- curate existing noise, repetition, and superseded debate only with user
  authorization;
- keep unique decision evidence recoverable.

The interpreted requirements body remains the current authority. Raw evidence
exists to detect drift and recover intent, not to force obsolete wording back
into the product.

## Interface Design Applicability

Create or maintain a design specification only when a user-visible or
interactive interface exists. Cover the visual system, layout, responsive
behavior, component states, navigation, feedback, motion, accessibility, copy,
and design acceptance evidence at the level the product needs. Do not invent UI
or motion to fill a template.

## Traceability

Use the repository's existing identifiers and links where available. At minimum:

- product behavior traces to requirements;
- acceptance traces to product behavior;
- architecture and design trace to the acceptance they enable;
- delivery status cites the applicable acceptance or gate;
- verification evidence identifies the claim it proves;
- route decisions cite the evidence that makes a route normal, fallback,
  disabled, or unavailable.

Traceability should make drift and false completion visible. Do not create an
identifier, matrix, or link when it adds ceremony without reducing ambiguity or
verification risk.
