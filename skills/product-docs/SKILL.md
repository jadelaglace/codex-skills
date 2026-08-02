---
name: product-docs
description: Maintain product and system documentation, authority, traceability, and delivery governance across discovery, definition, delivery, real-use recovery, closure, and operations. Use when defining or revising requirements, PRDs, acceptance criteria, design specifications, architecture, development process, status, test traceability, ownership, or human/Agent responsibilities. Preserve user intent, isolate external advice, map the repository's existing authority chain, propagate only real consequences, and use risk-based batch validation.
---

# Product Docs

Keep user intent, product behavior, acceptance, design, implementation boundaries,
delivery status, and evidence distinct. Start from the outcome the user values,
then maintain the smallest coherent document chain that can govern delivery.

## Establish Authority And Mode

Before editing:

1. Read the repository's local instructions and discover its current authority
   documents. Do not assume filenames or numbering.
2. Identify the current lifecycle mode: discovery, definition, delivery,
   real-use/recovery, closure, or operations.
3. Identify which decisions belong to the user and which work is delegated to
   Agents.
4. Read the highest affected authority document before its downstream
   interpretations.
5. Treat the latest direct user statement as higher authority than older
   requirements. Treat external research, advisors, and AI conversations as
   reference material unless the user explicitly adopts a conclusion.

Lifecycle mode changes delivery emphasis, not product truth. A mature product in
closure should not be pushed back into broad architecture discovery because a
local implementation choice is imperfect.

## Protect User Intent

Treat the repository's requirements authority as the durable interpreted record
of what the user actually wants:

- Preserve distinctive priorities, examples, tensions, and open questions when
  they carry meaning.
- Make the current interpreted body readable and current. Do not leave obsolete
  debate in the main requirements merely because it once occurred.
- Do not replace a concrete desire with a cleaner but narrower abstraction.
- Keep implementation phases, file inventories, algorithms, framework choices,
  and transient task status out of requirements unless they are genuine product
  constraints.
- Resolve conflicts in favor of the latest explicit user intent. Leave genuinely
  unresolved choices unresolved.

If the authority chain keeps raw user wording, use it as recovery evidence, not
as a second interpreted requirements document:

- Preserve exact wording inside selected quotations.
- Select excerpts that carry decisions, values, examples, corrections, or
  unresolved tension; a full transcript is not required.
- Do not silently rewrite, translate, or attribute an Agent/AI summary to the
  user.
- Curate existing low-signal tone, repetition, or superseded debate only when
  the user authorizes that cleanup. Do not erase unique decision evidence.
- Keep enough date/source context to distinguish direct user wording from
  external material and later interpretation.

Read `references/intent-preservation.md` before accepting a new or substantially
rewritten requirements authority.

## Isolate External Inputs

Keep these categories explicit:

```text
direct user intent and value judgement
existing product authority
external research, advisor, or AI suggestion
implementation candidate
adopted decision
```

External material can suggest questions, options, risks, tools, models, or
processes. It does not become user intent, a requirement, or an architecture
decision through paraphrase or proximity. Record it as reference until the user
or the repository's authorized decision process adopts it.

When several sources conflict, use this default order unless the repository
defines a stricter one:

```text
latest direct user instruction
-> current product authority
-> accepted decision record
-> external reference
-> implementation convenience
```

## Map The Existing Document Chain

Read `references/document-chain.md` before creating, moving, or reorganizing
authority documents. Map the repository's files to equivalent roles rather than
forcing a numbered template.

A common chain is:

```text
requirements / intent
  -> product behavior or PRD
  -> observable acceptance
  -> design specification when an interface exists
  -> architecture and ownership
  -> delivery process and live status
  -> verification cases and evidence
  -> implementation
```

Update the highest affected role first, then propagate only actual semantic
consequences. A reviewed downstream document may remain unchanged when its
contract did not change; record that conclusion instead of mechanically editing
the whole chain. Local instructions and working notes are not product authority
unless the repository explicitly says otherwise.

## Divide Human And Agent Responsibility

Unless the user specifies another model, keep human authority over:

- requirements and priority;
- success criteria and final acceptance;
- value judgments and scope tradeoffs;
- irreversible choices with material product, security, legal, financial, or
  data-authority consequences.

Agents should own the routine delivery burden:

- maintain affected downstream documents and live status;
- research and compare implementation options;
- make reversible technical choices within established boundaries;
- implement, review, test, and gather evidence;
- report progress and gaps in the user's outcome language.

Architecture review is not a permanent human gate. Escalate when a decision
materially changes requirements, an irreversible boundary, security or data
authority, or the acceptance contract; otherwise decide, document, and proceed.

## Work Broadly, Then Converge

Do not turn documentation discipline into step-by-step hesitation. Within a
clear scope and authority boundary:

1. Establish the batch goal, exit condition, and major risks.
2. Spread across related or repeated work to expose common patterns quickly.
3. Use cheap local checks at meaningful boundaries and immediately after risky
   changes or failures.
4. Converge the batch: resolve common defects, update evidence and status, then
   run the applicable broader gates.
5. Run full checks before merge, release, or acceptance, and at a cadence that
   catches drift without rerunning the entire suite after every small edit.

Do not hard-code a universal check count. Match cadence to blast radius,
feedback cost, task duration, and failure signals. For active day-scale work,
a few deliberate convergence points are often better than one full-suite run
per tiny feature. Known data-corruption, security, authority, or shared-contract
risks still trigger immediate validation.

## Research Existing Routes When Relevant

When the outcome depends on importing data, integrating providers, or minimizing
custom development, research proven existing routes before designing adapters,
protocols, or handoff formats. Compare official APIs and exports, maintained
tools, attainable content and metadata, authentication, re-collection behavior,
automation suitability, limitations, and fallback.

Prefer:

```text
proven existing capability
-> thin invocation or normalization
-> narrow implementation for a demonstrated gap
-> manual fallback when normal routes are unavailable
```

Search results, repository names, placeholder files, and plausible tool names
are not route evidence. Probe the selected route when access and safety permit.
Do not turn the easiest fixture or fallback into the claimed normal workflow.

## Keep Completion Honest

Separate these claims:

```text
intent documented
option or route researched
engineering scaffold present
mechanism tested with fixtures
real authorized path proven
user-visible outcome achieved
accepted and operationally closed
```

Compilation, file counts, interfaces, or fixture tests cannot by themselves
prove a product workflow or phase complete. Report first in concrete outcome
language: what the user can now do, what evidence exists, and what remains.

## Apply Architecture Guidance Conditionally

When ownership, storage, provenance, or repository design is in scope, read
`references/governance-rules.md`. Identify data authorities, permitted writers,
irreversible transformations, runtime state, credentials, and recovery needs.

Local-first, modular-monolith, distributed, hosted, and mixed systems require
different boundaries. Framework and language guidance must follow the product's
actual constraints and existing architecture; no language or topology is the
default of this Skill.

Add a new repository, service, protocol, or formal handoff only when a real
lifecycle, deployment, access, ownership, release, scale, or consumer boundary
proves the need.

### Prefer Replaceable Modules And Progressive Hardening

When the repository has not already fixed another approach, prefer modules that
are small enough to understand, have clear ownership and contracts, and can be
replaced without rewriting the surrounding product. Keep early boundaries
practical: isolate volatility and irreversible state, but do not manufacture a
distributed system or a large abstraction layer merely to claim modularity.

Use implementation maturity to guide language choice:

- Go is a strong default for fast algorithm, worker, CLI, or service prototypes
  that need simple deployment and useful compile-time checks.
- TypeScript is a strong default for interface, interaction, and end-to-end
  product-function prototypes where feedback speed matters most.
- Python is a secondary option when its mature libraries, models, data tooling,
  or provider ecosystem materially shorten the path to evidence.
- Rust is best reserved for narrow measured performance needs, safety-critical
  or data-authority boundaries, and stable components whose behavior and
  contracts are understood well enough to harden.

These are planning defaults, not universal mandates. Existing repository
constraints, target platforms, team capability, ecosystem fit, and measured
behavior can override them. Prototype boundaries should make later replacement
possible; migration or hardening requires evidence that the behavior is useful,
the contract is stable, and the added cost is justified.

## Change Documents Deliberately

Classify the request as intent, behavior, acceptance, interface design,
architecture, delivery/status, or verification work. Then:

1. Update the highest affected authority role.
2. Preserve or append selected direct wording when the repository uses raw
   intent evidence and the new wording materially governs the result.
3. Inspect downstream roles and update only changed semantics.
4. Keep external suggestions labeled until explicitly adopted.
5. Verify in proportion to impact and converge with the batch's broader gates.
6. Report changed authority, unchanged reviewed roles, evidence, and unresolved
   decisions.

Keep the work proportional. A delivery-governance change does not automatically
rewrite product acceptance, architecture, tests, or code.
