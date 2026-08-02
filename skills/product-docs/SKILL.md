---
name: product-docs
description: Maintain concise product and system documentation with clear authority, scope, context, progress, acceptance, and architecture boundaries. Use when capturing or revising direct user intent, requirements, PRDs, plans, live status, acceptance criteria, evidence, design specifications, architecture direction, verification traceability, ownership, or human/Agent responsibilities; also use when deciding what documents to read, create, split, combine, or leave unchanged. Prioritize user intent, actual progress, and observable acceptance; load only relevant context, isolate external advice until adopted, and propagate only real semantic consequences.
---

# Product Docs

Maintain the smallest coherent documentation context that can govern delivery.
Use this default priority:

```text
direct user intent and current requirements
-> plan and actual progress
-> acceptance criteria and completion evidence
-> stable architecture direction
-> local design and implementation detail
```

Do not let downstream technical detail displace the user's purpose, current
position, or definition of success.

## Orient And Read Selectively

Before editing:

1. Read local instructions and discover the repository's authority index or
   equivalent documents. Do not assume filenames, numbering, or one file per
   role.
2. Classify the request by its highest affected role: intent/requirements,
   product behavior, plan/progress, acceptance/evidence, architecture, design,
   or verification.
3. Start with the smallest source set that can answer the request. Expand only
   when a real semantic dependency appears.
4. Identify the lifecycle mode. Delivery or closure work should not reopen
   stable product definition or architecture without material cause.

Use this routing guide:

| Task | Start with | Expand only when needed |
| --- | --- | --- |
| Change intent or requirements | Latest direct wording and current requirements | Product behavior and acceptance |
| Update plan or progress | Primary live status and relevant acceptance | Verification or real-use evidence |
| Judge completion | Acceptance criteria and completion evidence | Requirements and verification cases |
| Change architecture direction | Requirements, acceptance, and current architecture | Governance rules, research, and implementation |
| Repair local wording | Target section and its direct authority | Downstream roles only if meaning changed |
| Create or reorganize documents | Authority index and neighboring roles | The full chain only when boundaries change |

Do not load every authority document merely because it exists.

## Preserve Intent And Authority

Keep these categories distinct:

```text
direct user wording and value judgment
current interpreted requirements
external research, advisor, or AI suggestion
implementation candidate
explicitly adopted decision
```

- Treat the latest direct user instruction as higher authority than older
  requirements. Preserve genuinely open choices as open.
- Keep current requirements readable and current; do not turn them into a
  transcript, sprint plan, architecture inventory, or technology argument.
- When raw wording is retained, select exact excerpts that preserve decisions,
  values, examples, corrections, or unresolved tension. Raw evidence helps
  detect drift; it is not a second current requirements authority.
- Keep external material labeled until the user or an authorized decision
  process adopts it.
- Keep human authority over requirements, priorities, progress judgment,
  success criteria, and final acceptance. Let Agents own routine documentation,
  reversible technical decisions, implementation, verification, and evidence
  within those boundaries.

Read `references/intent-preservation.md` before accepting a new or substantially
rewritten requirements authority.

## Shape Documents And Context

Give each authority a clear core question. Make its purpose, exclusions,
upstream basis, downstream consumers, and update trigger discoverable through
its index, opening, headings, or links. Do not require a boilerplate header when
the boundary is already clear.

- Give each fact one primary authority. Other documents should reference or
  interpret it rather than maintain competing copies.
- Put current truth and the reader's next decision before history and detailed
  evidence. Use appendices or supplements when history remains valuable but no
  longer belongs in the main reading path.
- Split documents when authority, primary reader, or update cadence forms a
  durable boundary. Do not split merely because a file is long.
- Keep material together when it shares authority, reader, update cadence, and
  must be read continuously to make the decision correctly.
- Do not combine requirements, live status, acceptance, architecture, and test
  implementation merely to reduce file count.
- Do not create a document, layer, identifier, or trace link that cannot prevent
  meaningful drift or support a real decision.

Read `references/document-chain.md` before creating, moving, splitting,
combining, or substantially reorganizing authority documents.

## Keep Plan, Progress, And Acceptance Honest

Maintain one primary source for live plan and progress. Requirements describe
the outcome and constraints; acceptance defines observable success; plans and
status describe the route and present position; verification records how claims
were tested.

Keep these claims separate:

```text
intent documented
work planned or scaffolded
mechanism tested with fixtures
engineering boundary or gate passed
real authorized path proven
user-visible outcome achieved
accepted and operationally closed
```

Compilation, file counts, interfaces, or fixture tests cannot by themselves
prove a product workflow complete. A local capability passing does not complete
the whole product. Report what the user can now do, what evidence supports that
claim, what remains, and whether the user has accepted the result.

Update status only when the repository's stated evidence threshold is met.
Preserve explicit blocked, partial, deferred, unavailable, and failed outcomes
instead of smoothing them into progress.

## Use Architecture At The Right Level

Treat architecture direction as secondary to intent, progress, and acceptance,
but preserve it when it protects lasting boundaries. Update architecture when a
decision materially changes data authority, permitted writers, module
ownership, irreversible transformation, deployment or access boundaries,
security, recovery, or a contract required for acceptance.

Keep reversible language, library, file-layout, algorithm, and local interface
choices in implementation or task records unless they establish a durable
boundary. Do not reopen stable architecture because a local implementation is
imperfect or an external suggestion is fashionable.

Read `references/governance-rules.md` when architecture, storage, provenance,
security, recovery, repository/service topology, or data ownership is in scope.

## Change And Report Deliberately

1. Update the highest affected authority role first.
2. Preserve selected direct wording only when it materially governs the result.
3. Inspect downstream roles that could be affected.
4. Update only changed semantics, contracts, status, or evidence. Record
   important reviewed-but-unchanged roles instead of manufacturing edits.
5. Validate in proportion to authority, blast radius, reversibility, and
   evidence risk. Run broader gates before merge, release, or acceptance.
6. Report in this order:

```text
whether the user's goal changed
-> current actual progress
-> evidence and remaining acceptance gap
-> whether stable architecture direction changed
-> changed authorities and important reviewed-but-unchanged roles
```

Keep the work proportional. A progress update does not automatically rewrite
requirements or architecture, and a local implementation change does not
automatically change product acceptance.
