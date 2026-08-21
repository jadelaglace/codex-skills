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
| Active plan/progress | Current goal, bounded next-start queue, route-changing stage conclusions, terminal, next action, recovery entry | Product authority, usage history, permanent completed-task archive |

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
   or execution order in the primary active plan/progress control. If it changes
   the running route, update the current item; otherwise insert it at the top of
   a bounded next-start queue without silently replacing the running task.
3. Split one input across both roles when it genuinely contains product intent
   and a general execution obligation; link both captures to one source.
4. Capture only enough source/time context to recover the input. Do not decide
   its status, rewrite it, or promote it to requirements before analysis.
5. When the repository supports stable capture identities, give the recovery
   entry one and reference the same identity from its active-plan item. Keep the
   recovery status, fast index, and whether an active obligation still exists
   consistent at terminal.

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

Keep only one current active item. A small next-start queue may exist, but not a
competing backlog. Give queued items only the source, goal, known conclusion,
next action, and recovery entry needed to resume; add the full terminal and
temporary subplan when an item becomes current. If a new input changes the
current route, update the current item instead of hiding the change in the
queue. Stage conclusions do not become user intent merely because they are in
the plan; promote them only after user adoption or the repository's authorized
decision process.

Give every queued item an explicit promotion policy. An auto-promote item may
advance only after a valid current-item terminal. A held, paused, or
`requires-explicit-resume` item cannot advance until the named user or authority
condition occurs. If all remaining items are held, the current slot may be
explicitly empty; do not fill it merely to avoid an empty active marker.

## Size And Structure

Use size as a maintenance signal, not a deletion command:

- Optimize the active plan for one-screen/fast recovery. Keep stable lifecycle
  policy in its governing authority and completed history in status/evidence or
  version history. Use both line and character/byte bounds appropriate to the
  repository so long lines cannot evade the hot-path limit.
- Order a next-start queue by explicit user priority; otherwise put the newest
  captured general obligation first. Keep it bounded. At terminal, select only
  the first item whose promotion policy currently permits advancement.
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
3. If the task created a recovery entry, annotate it with capture source/time,
   a few retrieval phrases, status such as `active`, `superseded`, `resolved`,
   or `recovery-only`, and replacement/resolution links. Do not create a
   recovery entry solely to satisfy terminal maintenance, and do not edit an
   existing quote.
4. Delete a successful temporary active item/subplan when no obligation or
   required evidence remains. Promote only a queue item whose policy permits
   it. If all remaining items require explicit resume or other new authority,
   keep them queued and mark the current slot explicitly empty.
5. Retain and terminally mark failed, blocked, interrupted, follow-up, audit,
   recovery, or handoff state. Record reason and next authority/decision.

Never delete unique direct wording, an adopted decision, current usage,
acceptance, failure recovery, or handoff evidence because an execution ended.
Never delete a temporary anchor before its durable consequences are promoted.

## Reading And Recovery

Apply this section at every full recovery boundary: a new session, context loss
or compaction, Agent/task handoff or interruption that may lose control/context,
a long pause with uncertain execution state, or an explicit `continue`,
`resume`, or equivalent instruction. Such an instruction authorizes
continuation of the governing goal; it does not authorize choosing the most
recently visible subtopic or checkpoint as a new goal.

An ordinary synchronous tool, command, or API failure with a clear result does
not require full recovery while the current turn, context, and governing task
identity remain intact. Handle or retry it locally. If a stateful operation has
an ambiguous outcome, reconcile the affected external state first; rerun the
full hook only when control/context or governing-task identity may also have
been lost.

Use an environment goal/task-state API when one exists. Do not infer the
governing goal or terminal state from a compacted summary, last message, tool
checkpoint, or most recent file touched when authoritative state is available.
Repositories that rely on a deep active-plan authority should expose a compact,
explicitly bounded root-level operational hook naming this order and linking
that authority. Validate the order inside the bounded block (Goal/task-state API
before Active Plan), including a mutation that reverses it. The hook is not a
second plan or lifecycle authority and must not copy its detailed contract.

### Recovery Hook Checker Pattern

Use marker-bounded checks rather than whole-file or exact-newline assumptions:

1. Extract the bounded hook block; fail when its markers are missing or repeated.
2. Normalize LF and CRLF for comparison inside the block.
3. Require the goal/task-state API marker and the active-plan link, in that
   order, within the same block.
4. Distinguish full recovery from ordinary synchronous failures with intact
   context; do not make every failed command restart recovery.
5. Mutate the order and local-failure boundary in isolated copies and assert
   that the checker rejects each defect.
6. Treat a missing hook as not-applicable only when recovery safety is outside
   the task scope; otherwise report it as an initialization gap.

Normal resume order:

```text
environment-level thread/task goal, when available -> shallow recovery hook ->
authoritative current active item -> authority index -> current intent ->
requirements -> only the downstream authorities needed
```

When the goal is missing or terminal, the active marker is empty, and the live
conversation contains an explicit new request, stop recovery after the active
plan. Do not read history, usage, verbatim evidence, or the full authority chain
just to reconfirm that no old task is active; continue with only the authorities
the new request needs.

Treat missing compacted, handed-off, interrupted, or checkpoint detail as
unknown. It cannot reopen a terminal item, demote the current goal, or promote
another item. Before the first state mutation after recovery, reconcile the
external goal and active plan. If they conflict, preserve both states while
resolving the conflict from the latest explicit user instruction or governing
authority; ask the user when that evidence cannot resolve it.

Reconcile three complementary recovery layers. Mandatory read order discovers
state; it does not let an older layer erase facts already visible in a newer
one:

1. **Live conversation layer** — the latest explicit instruction, actual result,
   and completion report. It is the most timely and has the highest action
   priority, but is also most exposed to interruption, compaction reordering, or
   fragments. Verify instruction-instance identity against visible results and
   the other layers.
2. **Goal runtime layer** — short- or medium-term scope and execution state that
   survives sessions and compaction. It usually represents the real direction
   and aligns with one durable active scope, but it may be paused to yield to a
   newer live instruction. Pausing preserves identity and obligations without
   authorizing execution.
3. **Durable document layer** — the same scope's persisted plan, current step,
   terminal state, and hard boundaries. It is most resistant to noise and drift,
   but may lag the live and goal layers by one terminal-writeback window.

### Recovery Selection And Replay Prohibition

First identify instruction or stage instances and exclude those already proved
terminal. Select among the remaining unfinished instances in this closed order:

```text
newest unfinished explicit user instruction established from live conversation at recovery
-> currently started goal
-> current executable instruction in durable documents
-> paused goal
-> compacted recovery context
-> pre-compaction instruction
```

Each step is a fallback, not an invitation to blend states. A lower-ranked
candidate cannot replace, reopen, or delay a higher-ranked one. The last two
steps may locate an instruction but cannot independently prove that it remains
authorized or unfinished; reconcile them with live, goal, or document authority.
If identity or state remains ambiguous, stop and ask rather than execute.

For the same instruction instance, use this increasing completion-evidence
strength:

```text
explicit completion report in live conversation
< goal progress marked completed or otherwise terminal
< durable documents marked terminal or removed by successful terminal cleanup
```

Every level prohibits replay. The stronger levels are increasingly persistent
across compaction and cannot be overridden by older, weaker `in progress`
evidence. Absence from an active document counts only when terminal evidence or
the document's cleanup policy proves successful removal; mere absence is
`unknown`. Reopen only when the user explicitly reissues the instruction as a
new instance or new verifiable evidence invalidates the recorded terminal.

When the live layer contains the corresponding result and explicitly reports
completion while the goal or documents still say `in progress`, and the
difference is fully explained by missing terminal maintenance, classify the
state as **writeback lag**. Perform only the remaining goal/document/evidence
writeback and advance the goal or stage to the state already proved by the
result. Do not rerun the business action, closure, tests, publication, or release.
An older `in progress` document cannot overwrite a completion fact that has
already occurred in the live layer.

When the live layer has no credible new instruction or result, continue from the
started goal and durable current step. A paused goal remains below the durable
current instruction in recovery priority. When durable documents already mark
the instance terminal, or successful terminal maintenance has removed it from
the active plan, do not infer `unfinished` from absence or incomplete context.
Compacted summaries, handoff text, older messages, and tool checkpoints are not
a fourth layer. Use them only to locate and reconcile three-layer evidence; they
cannot independently authorize action or manufacture a new instruction instance.

The queue is not part of goal selection during recovery. Read it only after the
current identity is established and only to preserve future obligations. Never
execute a held or explicit-resume item because it is first, recent, or the only
remaining queue entry.

Permit an active-goal transition only for an explicit user override, a valid
terminal promotion, or an authority-approved replan for a real blocker. Record
the source as a closed enum and pair it with an affirmative evidence sentence
whose prefix matches the enum; reject keyword-only or negated transition text.
Mark a blocked current item blocked before considering a replan. Reopen resolved,
superseded, or closed work only through an explicit user reopen or new verifiable
evidence that invalidates its terminal; retain the old terminal and attribute
the reopen source and impact.

The initial creation of a governing goal is a distinct transition. Record it as
`user-explicit-goal-start` when the user explicitly authorizes the goal, with an
affirmative evidence sentence using that prefix. Do not treat a first visible
message, an Agent suggestion, or a recovered summary as goal authorization.

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
- recovery begins changing state before reconciling an available external goal
  with the current active item;
- a `continue` or `resume` instruction is interpreted as permission to choose
  the latest visible subtopic instead of continuing the governing goal;
- missing compacted context is treated as unfinished work or permission to
  reopen a terminal item;
- a lower-ranked recovery candidate displaces a newer unfinished user
  instruction, a started goal, or the durable current instruction;
- an instruction is replayed after live completion, goal-terminal, or durable
  terminal/cleanup evidence already proves the same instance complete;
- an Agent reopens resolved work merely to re-audit or improve it;
- a current goal is replaced because a blocker exists, without an authorized
  replan;
- analysis continues for a long time without persisting a route-changing
  conclusion;
- current intent contains exact-quote formatting after wording was cleaned;
- recovery evidence is routinely read from the beginning;
- Agent summaries are attributed to the user;
- active plan duplicates requirements, usage, full logs, or every local check;
- active plan duplicates stable lifecycle policy or completed history in the
  mandatory recovery hot path;
- an ordinary synchronous tool failure with intact context restarts full
  recovery;
- completed temporary items accumulate as a shadow backlog;
- the current slot is empty while a next-start queue contains work that is
  currently eligible for automatic promotion;
- a temporary item is deleted before durable consequences or recovery evidence
  are promoted;
- size limits mechanically erase current intent or unique evidence.
