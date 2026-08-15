---
name: product-docs
description: Maintain product and system documentation, authority, traceability, and delivery governance across discovery, definition, delivery, real-use recovery, closure, and operations. Use when defining or revising requirements, PRDs, acceptance criteria, design specifications, architecture, development process, status, test traceability, ownership, or human/Agent responsibilities. Preserve user intent, isolate external advice, map the existing authority chain, research real routes when relevant, keep multi-axis progress and evidence honest, propagate only real consequences, and use risk-based validation.
---

# Product Docs

Keep user intent, product behavior, acceptance, design, implementation
boundaries, delivery status, and evidence distinct. Start from the outcome the
user values, then maintain the smallest coherent document chain that can govern
delivery. Use this priority when deciding what to read and what to report:

```text
direct user intent and current requirements
-> plan and actual progress
-> acceptance criteria and completion evidence
-> stable architecture direction
-> local design and implementation detail
```

Do not let downstream technical detail displace the user's purpose, current
position, or definition of success.

## Establish Authority And Mode

Before assessing, reporting, or editing:

1. Read local instructions and discover the repository's authority index or
   equivalent documents. Do not assume filenames, numbering, or one file per
   role.
2. Identify the lifecycle mode: discovery, definition, delivery,
   real-use/recovery, closure, or operations.
3. Classify the request by its highest affected role: intent/requirements,
   product behavior, plan/progress, acceptance/evidence, architecture, design,
   or verification.
4. Identify which decisions belong to the user and which routine work belongs
   to Agents.
5. Read the highest affected authority before its downstream interpretations.
6. Start with the smallest source set that can answer the request. Expand only
   when a real semantic dependency appears.

Use this routing guide:

| Task | Start with | Expand only when needed |
| --- | --- | --- |
| Change intent or requirements | Latest direct wording and current requirements | Product behavior and acceptance |
| Update plan or progress | Primary live status and relevant acceptance | Verification or real-use evidence |
| Judge completion | Acceptance criteria and completion evidence | Requirements and verification cases |
| Research an external route | Requirements, acceptance, and route authority | Official source, tool evidence, fallback |
| Change architecture direction | Requirements, acceptance, and current architecture | Governance, research, and implementation |
| Repair local wording | Target section and its direct authority | Downstream roles only if meaning changed |
| Create or reorganize documents | Authority index and neighboring roles | Full chain only when boundaries change |

Lifecycle mode changes delivery emphasis, not product truth. A mature product in
closure or recovery should not be pushed back into broad architecture discovery
because a local implementation choice is imperfect.

When sources conflict, use this order unless the repository defines a stricter
one:

```text
latest direct user instruction
-> current product authority
-> explicitly adopted decision
-> external reference
-> implementation convenience
```

## Protect User Intent And External Boundaries

Keep these categories visibly distinct:

```text
direct user wording and value judgment
current interpreted requirements
external research, advisor, or AI suggestion
implementation candidate
explicitly adopted decision
```

- Treat the latest direct user instruction as higher authority than older
  requirements. Preserve genuinely open choices as open.
- Keep requirements readable and current. Do not turn them into a transcript,
  sprint plan, architecture inventory, or technology argument.
- Preserve concrete priorities, examples, corrections, and unresolved tension
  when removing them would narrow what the user wants.
- If raw wording is retained, select exact attributable excerpts that preserve
  decisions, values, examples, or corrections. Raw evidence detects drift; it
  is not a second current requirements authority.
- Do not silently rewrite, translate, or attribute an Agent or AI summary to
  the user. Keep enough date and source context to distinguish direct wording,
  external material, and later interpretation.
- Keep external material labeled until the user or an authorized decision
  process adopts it. An external language, framework, model, or workflow
  recommendation is not a product decision by proximity.

Read `references/intent-preservation.md` before accepting a new or substantially
rewritten requirements authority.

## Map And Shape The Document Chain

Map existing files to roles rather than forcing a numbered template. A common
direction is:

```text
requirements / intent
  -> product behavior or PRD
  -> observable acceptance
  -> interface design when applicable
  -> architecture and ownership
  -> delivery process and live status
  -> verification cases and evidence
  -> implementation
```

For each authority, make its purpose, exclusions, upstream basis, downstream
consumers, and update trigger discoverable through an index, opening, headings,
or links.

- Give each fact one primary authority. Reference or interpret it elsewhere;
  do not maintain competing editable copies.
- Keep one primary source for live plan and progress.
- Keep reusable operating behavior in product authority and concrete execution
  facts in live status or evidence. A preview/dry-run, pilot mode,
  template/profile, or complete processing of an authorized scope can be
  repeatable product behavior; a particular run, denominator, batch, accepted
  instance, or completion claim is not.
- Local instructions and working notes provide operational context unless the
  repository explicitly makes them product authority.
- Put current truth and the reader's next decision before history and detailed
  evidence. Move useful history to a supplement when it obscures the decision
  path.
- Split when authority, primary reader, update cadence, reusable contract, or
  historical evidence creates a durable independent boundary.
- Keep material together when it shares authority, reader, and cadence and must
  be read continuously. Do not split merely because a file is long.
- Keep candidate plans and adopted decisions visibly different. A candidate
  supplement cannot silently become current architecture or requirements.
- Do not let a specialized pilot narrow the general product or Skill authority
  to one dataset, source, customer, course, or other trial instance.
- Do not create a document, layer, identifier, trace matrix, service, or formal
  handoff that cannot prevent meaningful drift or support a real decision.
- Create a design specification only when a user-visible or interactive
  interface exists; do not invent UI scope to fill a template.

Read `references/document-chain.md` before creating, renaming, renumbering,
moving, splitting, combining, or substantially reorganizing authority
documents, and before repairing their navigation.

## Divide Human And Agent Responsibility

Unless the user specifies another model, keep human authority over:

- requirements and priority;
- success criteria, decisions about whether observed progress is sufficient,
  product-scope completion, and final acceptance;
- value judgments and scope tradeoffs;
- irreversible choices with material product, security, legal, financial, or
  data-authority consequences.

Agents should own the routine delivery burden:

- measure, maintain, and report evidence-backed live status and observed
  progress without promoting them to product completion or acceptance;
- research and compare implementation options and existing routes;
- make reversible technical choices within established boundaries;
- implement, review, test, and gather evidence;
- report progress and gaps in the user's outcome language.

Once the user has given a clear authorized scope, let the Agent navigate,
collect, retry, and converge without asking for routine per-item confirmation.
Pause and escalate for permission or semantic judgment, an ambiguous
requirement, an irreversible boundary, a material security/data-authority risk,
or a blocked acceptance decision. Routine architecture review is not a permanent
human gate.

## Work Broadly, Then Converge

Within a clear scope and authority boundary:

1. Establish the batch goal, exit condition, allowed scope, and major risks.
2. Spread across related or repeated work to expose common patterns quickly.
3. Use cheap targeted checks at logical boundaries and immediately after risky
   changes, shared-contract changes, or failures.
4. Converge the batch: resolve common defects, update evidence and status, and
   record remaining gaps.
5. Run broader gates before merge, release, or acceptance, and at a cadence
   appropriate to blast radius and feedback cost.

Do not hard-code a universal check count. Increase checkpoint frequency when
data corruption, security, authority, or shared-contract risk rises; decrease it
for repetitive, reversible work protected by cheap local checks. A status claim
must cite the evidence threshold that permits it; update the claim and its
supporting evidence together or make the evidence link explicit. Do not promote
status merely because code, files, interfaces, or fixtures exist.

## Research Existing Routes When Relevant

When the outcome depends on importing data, integrating providers, or minimizing
custom development, research proven existing routes before designing adapters,
protocols, or handoff formats. Compare official APIs and exports, maintained
tools, attainable content and metadata, authentication, re-collection behavior,
automation suitability, limitations, and fallback.

Read `references/governance-rules.md` before creating or revising a route
registry, classifying route evidence, or judging runtime availability.

Use this preference:

```text
proven existing capability
-> thin invocation or normalization
-> narrow implementation for a demonstrated gap
-> manual fallback when normal routes are unavailable
```

Record route evidence and its limitations. Search results, repository names,
placeholder files, fixture envelopes, locator-only records, and plausible tool
names are not real-path evidence. Keep fallback, unavailable, and disabled
capabilities visibly distinct from the normal route. Do not turn the easiest
fixture or fallback into the claimed product workflow. Probe the selected route
when access and safety permit.

## Keep Completion And State Honest

Separate these claims:

```text
intent documented
option or route researched
engineering scaffold present
mechanism tested with fixtures
engineering boundary or gate passed
real authorized path proven
user-visible outcome achieved
accepted and operationally closed
```

Do not collapse independent dimensions such as authorization, input
completeness, registration/readiness, processing, availability, and acceptance
into one `complete` flag. Report the dimensions that matter for the user's
decision.

For repeated or per-item work, preserve explicit `success`, `partial`,
`skipped`, `blocked`, `retryable failed`, `non-retryable failed`, `changed`,
`unchanged`, `inaccessible`, and `removed` outcomes when applicable. Retry only
the affected object, preserve successful work, and make unchanged recollection
idempotent: it must not create a false revision, asset, or fact.

Compilation, file counts, interfaces, or fixture tests cannot by themselves
prove a product workflow or phase complete. Report first what the user can now
do, what evidence supports that claim, what remains, and whether the user has
accepted the result.

Read `references/governance-rules.md` before a closure audit or an
evidence-based claim that a scope is complete.

## Apply Architecture And Data Governance Conditionally

When ownership, storage, provenance, recovery, security, repository/service
topology, or an acceptance-enabling contract is in scope, read
`references/governance-rules.md`.

Architecture should explain stable information flow, ownership, permitted
writers, irreversible transformations, recovery boundaries, and contracts
required for acceptance. Preserve an established architecture unless evidence
shows that it blocks acceptance, violates an authority boundary, creates material
security or recovery risk, or no longer matches a real lifecycle boundary.

For meaningful data classes, identify one authority and its permitted writers.
Keep raw/source evidence, canonical records, processed derivatives, published
outputs, runtime state, and credentials distinct. Preserve source identity,
integrity, processing identity/status, dependencies, and output integrity when
traceability matters. Derived data, indexes, views, and outputs must be
deletable/rebuildable without changing the authoritative source. Quarantine or
clearly mark incomplete, failed, restricted, or provenance-free results.

Create a repository, service, protocol, module boundary, or formal handoff only
when a real lifecycle, deployment, access, ownership, release, scale, security,
or consumer boundary requires it. Keep volatile behavior replaceable behind
narrow contracts and harden it after real use stabilizes the behavior and the
added safety or performance benefit is demonstrated. Language, framework,
library, algorithm, and file layout are implementation choices unless they
materially affect those durable boundaries.

## Change Documents Deliberately And Report Clearly

1. Classify the request as intent, behavior, acceptance, design,
   architecture, delivery/status, or verification work.
2. Update the highest affected authority role first.
3. Preserve selected direct wording only when it materially governs the result.
4. Inspect downstream roles that could be affected; update only changed
   semantics, contracts, status, or evidence.
5. Record important reviewed-but-unchanged roles instead of manufacturing edits.
6. Validate in proportion to authority, blast radius, reversibility, and
   evidence risk. For live or runtime claims, reconcile documentation against
   the real command, API, registry, or system of record. A checker proves only
   the rules it actually covers. Run broader gates before merge, release, or
   acceptance.

Report in this order:

```text
user goal and whether it changed
-> current actual progress
-> evidence, status dimensions, and remaining acceptance gap
-> stable architecture direction and boundary impact
-> changed authorities and important reviewed-but-unchanged roles
-> unresolved decisions and next action
```

Keep the work proportional. A delivery update does not automatically rewrite
requirements or architecture, and a local implementation change does not
automatically change product acceptance.
