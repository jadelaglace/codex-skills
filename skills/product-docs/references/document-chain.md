# Documentation Chain

Discover the repository's existing authority chain and map files to roles. Do
not rename or renumber a working chain merely to match this reference.

## Authority Roles

| Role | Must answer | Must not silently become |
| --- | --- | --- |
| Raw intent evidence, when used | What did the user directly say and when? | A full transcript, Agent interpretation, or external advice |
| Requirements / intent | What outcome and constraints govern the product now? | Architecture, task order, or transient status |
| Product behavior / PRD | Who uses it and what observable behavior do they receive? | Code layout or storage internals |
| Acceptance | What observable result proves success or failure? | Test implementation details or routine approval ceremony |
| Design specification, when applicable | How does the interface support usable and accessible task completion? | Backend internals or invented interface scope |
| Architecture / ownership | Which boundaries, authorities, contracts, and dependencies deliver acceptance? | Phase estimates or product intent invented for convenience |
| Delivery process / live status | What mode, order, responsibility, risk, and evidence govern delivery now? | New product behavior |
| Verification cases / evidence | How is each acceptance claim tested or demonstrated? | Unadopted architecture alternatives |

Repositories may combine roles in one document or use different names. Keep
authority direction explicit even when the files differ.

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

## Impact-Based Propagation

- Start at the highest role whose meaning changed.
- Inspect each downstream role that could be affected.
- Update a document only when its semantics, contract, status, or evidence
  changed.
- Record important reviewed-but-unchanged roles in the delivery report.
- Never manufacture edits solely to demonstrate that the whole chain was
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
- verification evidence identifies the claim it proves.

Traceability should make drift visible. It should not create ceremony that
slows small, semantically unchanged work.
