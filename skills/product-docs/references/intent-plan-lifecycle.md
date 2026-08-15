# Intent And Active-Plan Lifecycle

Use this reference to design docs-first capture, current-intent curation,
temporary Agent subplans, and terminal maintenance without creating a transcript
or a shadow backlog.

## Contents

- Role model
- First capture
- Stage conclusions
- Size and structure
- Terminal maintenance
- Reading and recovery
- Failure signals

## Role Model

Map the repository's existing files to these roles; do not impose filenames or
create all three when existing authorities already separate them safely.

| Role | Owns | Must not become |
| --- | --- | --- |
| Current intent | Still-effective user intent, lightly curated without changing meaning | Verbatim evidence, requirements, run status |
| Verbatim recovery | Append-first exact user input and indispensable attributed context | Daily entry point, full transcript, Agent-thought dump |
| Active plan/progress | Current goal, route-changing stage conclusions, terminal, next action, recovery entry | Product authority, usage history, permanent completed-task archive |

Requirements remain the current interpreted product authority. Live status and
run evidence remain separate from the active plan. Store a full round terminal
matrix and defect ledger in the repository's evidence/round-ledger authority.
Update live usage/status only with a scope-bound outcome summary and evidence
pointer when that result changes the current user/delivery decision; do not turn
usage into the full execution log. The active plan records the terminal
conclusion and evidence entry, not another copy of either record.

## First Capture

Before backward search, analysis, implementation, or an older plan:

1. Append product-specific intent, correction, value judgment, or open question
   verbatim to recovery evidence when that role exists.
2. Put a cross-project obligation, process correction, bounded read-only task,
   or execution order at the front of the primary active plan/progress control.
3. Split one input across both roles when it genuinely contains product intent
   and a general execution obligation; link both captures to one source.
4. Capture only enough source/time context to recover the input. Do not decide
   its status, rewrite it, or promote it to requirements before analysis.

If the repository has no durable recovery or progress role, use the smallest
existing appropriate artifact. Do not create a parallel authority solely to
remember one instruction.

## Stage Conclusions

Persist an Agent-attributed temporary subplan when any of these occurs:

- analysis changes the remaining route, scope, contract, or risk treatment;
- an execution round reaches its declared terminal and produces a matrix or
  defect ledger;
- a shared blocker, input drift, authorization boundary, or evidence failure
  invalidates downstream work;
- long-running, high-context work or handoff is about to begin.

Do not persist private chain of thought, every tool call, every small hypothesis,
or every targeted check. Use the decision test:

```text
Would losing this conclusion make the next Agent take a different route or
repeat substantial work?
```

An active item should expose, when applicable:

```text
source anchor
user goal
current state
declared terminal
protected or explicitly unchanged boundary
temporary subplan / stage conclusions, attributed to Agent
next action
evidence or recovery entry point
```

At a round terminal, write the complete matrix and defect ledger once to
evidence. Put only the bounded repair conclusion and next fresh-round action in
the active plan. If the terminal changes current delivery status, add a concise
scope/outcome/evidence-pointer update to live status; otherwise leave it
unchanged.

Keep only one primary active item. A small queue may exist, but not a competing
backlog. Stage conclusions do not become user intent merely because they are in
the plan; promote them only after user adoption or the repository's authorized
decision process.

## Size And Structure

Use size as a maintenance signal, not a deletion command:

- Optimize the active plan for one-screen/fast recovery. Around 200 lines is a
  useful review signal; around 250 lines should trigger promotion and cleanup.
- Organize current intent by stable user concern rather than chronology. Around
  80–250 lines is usually scannable; over about 300 lines, audit for history,
  status, implementation detail, or repetition.
- Let verbatim recovery grow when evidence is genuinely unique, but keep a
  compact index of dates/decision clusters, a few retrieval phrases, current
  status, and replacement/resolution links.

Do not rewrite exact quotations while curating current intent. Lightly curated
text must not use quotation formatting or claim verbatim attribution. Preserve
scope words such as `may`, `must`, `prefer`, `only`, `defer`, and `open`.

## Terminal Maintenance

At a successful, failed, blocked, interrupted, or handoff terminal, maintain the
roles once in this order:

1. Promote durable decisions, requirements, architecture, usage facts, run
   evidence, failure context, and unresolved obligations to their authorities.
   Keep complete matrices/defects in evidence and only decision-relevant outcome
   summaries in usage/status.
2. Refresh current intent: retain effective intent and real open tension; remove
   a fully superseded daily-reading copy only when exact evidence remains
   recoverable.
3. Annotate the new recovery entry with capture source/time, a few retrieval
   phrases, status such as `active`, `superseded`, `resolved`, or
   `recovery-only`, and replacement/resolution links. Do not edit the quote.
4. Delete a successful temporary active item/subplan when no obligation or
   required evidence remains. If no item remains, say so explicitly when the
   repository needs a persistent progress file.
5. Retain and terminally mark failed, blocked, interrupted, follow-up, audit,
   recovery, or handoff state. Record reason and next authority/decision.

Never delete unique direct wording, an adopted decision, current usage,
acceptance, failure recovery, or handoff evidence because an execution ended.
Never delete a temporary anchor before its durable consequences are promoted.

## Reading And Recovery

Normal resume order:

```text
authority index -> primary active item -> current intent -> requirements ->
only the downstream authorities needed
```

Escalated recovery order:

```text
normal chain cannot resolve serious drift/conflict/blockage/audit issue ->
recovery index -> matched exact wording and attributed context ->
repair current authority -> resume normal chain
```

Do not reread the entire recovery ledger on every task. More raw does not mean
more current.

## Failure Signals

- latest governing input exists only in chat;
- analysis continues for a long time without persisting a route-changing
  conclusion;
- current intent contains exact-quote formatting after wording was cleaned;
- recovery evidence is routinely read from the beginning;
- Agent summaries are attributed to the user;
- active plan duplicates requirements, usage, full logs, or every local check;
- completed temporary items accumulate as a shadow backlog;
- a temporary item is deleted before durable consequences or recovery evidence
  are promoted;
- size limits mechanically erase current intent or unique evidence.
