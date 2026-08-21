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

## Persist New Governing Input First

When new user input changes, corrects, questions, or governs ongoing work,
persist it before searching backward, analyzing, editing implementation, or
continuing an older plan. Classify it first so `docs-first` does not pollute the
wrong authority:

- Put product-specific intent, value judgments, corrections, and genuinely open
  product questions append-first and verbatim in the repository's recovery
  evidence when that role exists. Do not clean, summarize, or promote them first.
- Put an interpreted current product decision in requirements only after it is
  actually decided; do not promote a question or an Agent recommendation.
- Put cross-project working agreements, process corrections, and general
  follow-up obligations in the primary plan or progress control, not in product
  requirements or product wording evidence. If the input changes the running
  route, update the current item; otherwise insert it at the top of a bounded
  next-start queue without silently displacing the running task. Propagate it to
  an applicable shared Skill or process authority when the user requests reuse.
- Put run facts and concrete completion state only in live status or evidence.

For an empty or newly initialized repository, use the optional
`references/greenfield-init.md` route to choose the smallest authority chain
before generating documents. Keep this route conditional; an established
repository keeps its existing chain.

After any required recovery reconciliation, make the capture the first completed
task action, not a promise to document later.
At every full recovery boundary—new session, context loss or compaction,
Agent/task handoff or interruption that may lose control/context, a long pause
with uncertain execution state, or an explicit user instruction such as
`continue`, `resume`, or `pick this back up`—first call an available
goal/task-state API. An ordinary synchronous tool, command, or API failure that
returns a clear result while the current turn and governing task remain intact
is not a full recovery boundary; handle or retry it locally. For an ambiguous
stateful failure, reconcile the affected external state and rerun the full hook
only when control/context or task identity may also have been lost. Then
immediately follow the repository's shallow recovery hook to its authoritative
active plan/progress control and reconcile the single current item before
reading the general authority index, current intent, older history, or queue. Treat a
continue/resume instruction as authorization to continue the governing goal,
not to select the most recently visible subtopic. Missing summary, checkpoint,
or tool-state detail is `unknown`, not evidence that work is unfinished or
authorization to change state. Preserve the current active goal and terminal
states by default. A next-start item marked held, paused, or
`requires-explicit-resume` remains queued after the current item reaches
terminal; promote it only when its declared authority condition is satisfied.
Read verbatim recovery evidence only
when the normal chain cannot resolve serious drift, conflict, blockage, or an
audit/recovery question. If no durable progress control exists, update the
smallest existing planning/status artifact; do not create a competing authority
merely to remember the instruction.

Keep the active plan as a compact dynamic hot path, not a copy of stable
lifecycle policy or completed history. When the goal is missing/terminal, the
active marker is empty, and live conversation contains an explicit new request,
finish recovery there and read only the authorities that request actually needs.

Reconcile three recovery layers: live conversation, goal runtime state, and
durable documents. The live layer is newest but most vulnerable to compaction
damage; the goal layer carries the short- or medium-term scope across sessions
and may pause; documents preserve the same scope's durable state and hard
boundaries but may lag one terminal writeback.

Before selecting work, exclude instruction instances already proved terminal.
Then select unfinished work in this closed order:

```text
newest unfinished user instruction established from live conversation at recovery
-> started goal
-> current executable instruction in durable documents
-> paused goal
-> compacted recovery context
-> pre-compaction instruction
```

A lower-ranked candidate cannot displace a higher-ranked one. Compacted context
and pre-compaction instructions are locating evidence only until reconciled with
live, goal, or document authority; stop rather than infer authorization when
their identity or state cannot be verified.

Treat completion evidence as an increasingly durable replay prohibition:

```text
explicit completion report in live conversation
< goal progress marked terminal
< durable documents marked terminal or removed by successful terminal cleanup
```

Every level forbids rerunning the same instruction instance unless the user
explicitly reissues it as a new instruction or new verifiable evidence
invalidates its terminal. A later level cannot be weakened by an older `in
progress` message or compacted summary. When live evidence proves completion but
goal or documents lag, perform only the missing terminal writeback and
goal/stage completion; do not rerun the work, tests, publication, release, or closure. Read
`references/intent-plan-lifecycle.md` for reconciliation cases.

Change the current active goal only after an explicit user override, a valid
terminal that promotes the agreed next item, or an authority-approved replan for
a real blocker. A blocker alone marks the current item blocked; it does not
authorize replacing it. Do not reopen `resolved`, `superseded`, or `closed` work
because context is incomplete, an Agent wants to re-audit it, or the result can
still be improved. Reopen only on an explicit user instruction or new verifiable
evidence that invalidates the terminal, and preserve the prior terminal plus the
reopen source and impact. After each user-numbered subtask or declared stage
terminal, update the active item before starting the next one.

Record each active-goal transition with a closed type enum such as
`user-explicit-goal-start`,
`user-explicit-goal-override`, `legal-terminal-auto-promote`, or
`authority-approved-blocker-replan`, plus an affirmative evidence sentence
whose prefix matches that type. Reject keyword-only or negated transition text.

After analysis forms a conclusion that changes the remaining route, after a
declared execution terminal, when a shared blocker invalidates downstream work,
or before long/context-heavy work or handoff, update the corresponding active
item with a concise Agent-attributed temporary subplan. Record the conclusion,
next action, protected boundary, and evidence entry point—not private chain of
thought, every command, or every local check. Use this threshold: losing the
update would make the next Agent take a different route or repeat substantial
work.

Treat a plan/progress capture made only to anchor a bounded read-only request as
a temporary execution record, not permanent product history. At the request's
explicit terminal:

1. Promote any durable decision, correction, unresolved obligation, run fact,
   failure, or handoff evidence to its proper authority first.
2. Delete the temporary anchor when the work succeeded, no obligation remains,
   and deleting it loses no evidence needed for audit, recovery, or handoff.
3. Keep and mark it terminal when the primary progress authority intentionally
   preserves history, or when the request failed, was blocked, was interrupted,
   or still has a follow-up obligation. Record the terminal reason.
4. When the progress authority uses a next-start queue, promote only an item
   whose declared policy permits automatic promotion. Keep held, paused, or
   explicit-resume items queued; an empty current slot is correct when every
   remaining item requires new authority.

Never delete direct-wording evidence, an adopted decision, live status, or
completion evidence merely because the task that captured it ended. Do not let
temporary anchors accumulate as a shadow backlog, and do not delete one before
its durable consequences have been promoted.

Read `references/intent-plan-lifecycle.md` before creating or substantially
changing current-intent, verbatim-recovery, active-plan, or progress-control
roles, and before designing their curation, size, status, or terminal cleanup.

Read `references/greenfield-init.md` before initializing an empty repository or
choosing an initial authority chain.

## Establish Authority And Mode

Before assessing, reporting, or editing:

1. Read local instructions and discover the repository's authority index or
   equivalent documents. Do not assume filenames, numbering, or one file per
   role.
2. Check whether root-level local instructions or README expose a mandatory,
   explicitly bounded recovery-hook block to the active-plan authority. When
   recovery safety matters and no shallow hook exists, add the smallest bounded
   link-and-order hook that preserves the deeper document as the sole lifecycle
   authority. Validate that Goal/task-state API occurs before the Active Plan
   link inside the block, and add a mutation that reverses that order.
3. Identify the lifecycle mode: discovery, definition, delivery,
   real-use/recovery, closure, or operations.
4. Classify the request by its highest affected role: intent/requirements,
   product behavior, plan/progress, acceptance/evidence, architecture, design,
   or verification.
5. Identify which decisions belong to the user and which routine work belongs
   to Agents.
6. Read the highest affected authority before its downstream interpretations.
7. Start with the smallest source set that can answer the request. Expand only
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

## Run Coherent Rounds, Then Converge

Use an execution round when repeated or multi-stage delivery would otherwise be
fragmented by per-item checks. Keep narrow, reversible work proportional; do not
add round machinery when one edit and one relevant check already reach the real
terminal.

Before a round, freeze:

- the authorized scope or denominator and input identity;
- the intended terminal, stage sequence, and acceptance matrix;
- the implementation and configuration identity used by the round;
- the small set of risks that invalidate the round immediately.

During the round, treat checkpoints as observations, not automatic repair gates.
Record non-invalidating defects and continue all independent work to explicit
terminal states. Fail fast only when continuing risks data loss or irrecoverable
change, crosses authority or authorization, creates a material security issue,
detects frozen-input drift, or makes downstream evidence untrustworthy. A
fail-closed item, package, or branch does not stop unrelated work unless the
failure is shared and invalidating.

At the declared terminal:

1. Evaluate the whole acceptance matrix once and record every stage and item as
   succeeded, failed, skipped, blocked, or another explicit terminal state.
2. Produce one defect ledger and preserve the actual terminal, evidence, and
   gaps without promoting the round to completion.
3. Cluster defects by root cause, owner, and blast radius; form a bounded repair
   set instead of patching each symptom as it appears.
4. Use targeted checks during repair for fast feedback. These checks prove the
   repair, not the batch, phase, release, or user outcome.
5. After implementation, configuration, input, or acceptance changes, start a
   new round from clean staging and run to the same terminal. Resume an existing
   round only when its frozen state is unchanged.
6. Run broader gates before merge, release, closure, or acceptance at a cadence
   appropriate to blast radius and feedback cost.

Keep checkpoint, repair-test, terminal-gate, and user-acceptance evidence
distinct. Do not hard-code a universal check count. Increase observation
frequency when data corruption, security, authority, or shared-contract risk
rises; decrease it for repetitive, reversible work protected by cheap checks.
A status claim must cite the terminal evidence threshold that permits it; update
the claim and supporting evidence together or link them explicitly. Do not
promote status merely because code, files, interfaces, fixtures, or targeted
tests exist.

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
