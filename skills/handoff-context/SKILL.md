---
name: handoff-context
description: >
  Create a concise but complete stage handoff that can be pasted into a new conversation so the next Agent can continue safely. Use when the user says “交接”, asks for a阶段性总结上下文, or asks for continuation-ready context. Preserve current authority, evidence, terminal states, unresolved items, and boundaries; do not invent work or restart completed work.
metadata:
  short-description: "Generate continuation-ready handoff context"
  version: "1.0.1"
---

# Handoff Context

When the user says “交接” or asks for a阶段性总结上下文, produce one standalone handoff that can be pasted into a new conversation. The goal is not a diary or a full transcript: it is enough context for the next Agent to understand what is true, what is finished, what is active, what is waiting for the user, and what must not be restarted.

## Required behavior

1. Use the current conversation, task/Goal state, repository or project authority, live status, and concrete evidence available in the current environment. Do not treat an old summary or earlier handoff as stronger than current evidence.
2. Preserve the latest user intent and corrections. Keep user decisions, Agent recommendations, external facts, implementation details, and observed run results distinct.
3. State the current task/Goal state honestly. If the Goal/task-state API returns no result, write `unknown`; do not infer an active task from a missing result.
4. Include the authoritative recovery entry point when one exists, especially the required Goal/task-state check and Active Plan or progress-authority path/marker.
5. Explicitly separate:
   - completed and terminal work;
   - active work and its next safe action;
   - user acceptance or other external confirmation still required;
   - known defects, gaps, or unavailable capabilities;
   - work that must not be auto-recovered or rerun.
6. Preserve identifiers needed for continuation: project/repository, branch, commit, release/version/tag, run/session IDs, paths, package/profile names, and evidence locations. Include only identifiers that are actually known.
7. Do not claim acceptance, publication, payment, testing, device validation, or provider usage unless evidence supports that exact claim. Use `unknown`, `estimated`, `pending_user_acceptance`, `blocked`, or `unavailable` when needed.
8. Do not create a new Goal, Issue, branch, PR, release, or external mutation merely because the user requested a handoff. A handoff is normally read-only.
9. Do not restart completed work, reopen closed phases, or promote queued/held work. Say what explicit user instruction would be needed to start it.
10. End with a clear “new conversation starting point” that tells the next Agent what to check first and what it may or may not do.

## Three-layer recovery model

Treat recovery information as three cooperating layers:

1. **Live conversation:** newest user instruction, corrections, completion reports, and current results. It is the most current layer but the most vulnerable to compaction or context loss.
2. **Goal runtime state:** the started short- or medium-term scope, active item, pause state, and terminal markers that survive a conversation boundary.
3. **Durable documents:** the project or process authority containing the active plan, progress, evidence, and hard boundaries. It may lag one terminal writeback.

The handoff is a transport and locator, not a fourth authority layer. It must not override the current Goal or durable documents, and it cannot by itself authorize a mutation. In a new conversation, first reconcile the current Goal/task state and the active plan or progress authority; use the handoff to locate and interpret them.

When selecting unfinished work after recovery, prefer the newest still-unfinished user instruction, then the started Goal, then the current executable durable-document item, then a paused Goal, then compacted recovery context or pre-compaction instructions. Lower-ranked context is locating evidence only until reconciled with a live authority.

## Prevent replay of terminal work

Treat completion evidence as a replay prohibition, even when a later layer has not yet been updated:

```text
explicit completion report in live conversation
< Goal progress marked terminal
< durable documents marked terminal or successfully cleaned up
```

Every level forbids rerunning the same instruction instance unless the user explicitly issues it again or new verifiable evidence invalidates its terminal. If live evidence says the work is complete but the Goal or documents lag, do only the missing terminal writeback and reconciliation; do not rerun the work, tests, publication, release, or closure. If a read-only task used a temporary progress anchor, mark it terminal or remove it only after its durable consequences and evidence have been preserved.

## Recommended outline (guidance only, not mandatory)

Use this outline when it fits the work. Omit, combine, or reorder sections when a shorter handoff is clearer; it is not a required template.

1. Title and date
2. Recovery rules and current Goal/Active Plan state
3. Repository, workspace, branch, version/tag, and dirty state
4. User goal and governing decisions
5. Current lifecycle mode (for example: usage, development, recovery, acceptance, or closed)
6. Completed results and acceptance evidence
7. Active work, blockers, pending user decisions, and safe next action
8. Defect/gap ledger and honest capability limits
9. Protected boundaries and work that must not be rerun
10. Evidence paths, external systems, and cost/provider notes when relevant
11. Exact instructions for the next conversation

## Writing standard

- Write in the user's language unless the user asks otherwise.
- Prefer compact, information-dense prose and short lists over a transcript.
- Put the outcome and current state before historical detail.
- Keep exact paths and IDs in code formatting so they can be copied.
- Explain important status qualifiers, especially the difference between `accepted`, `published`, `pending_user_acceptance`, `estimated`, `unknown`, `blocked`, and `unavailable`.
- Do not hide important caveats in a footnote or omit them to make the handoff shorter.
- If there is no active work, say so plainly and tell the next Agent to wait for a new explicit instruction.

## Output

Return one self-contained Markdown handoff, ready to paste into a new conversation. A brief note outside the handoff is acceptable only if needed to say that no repository or external state changed. Do not output private chain-of-thought; include decisions, evidence, and actionable continuation guidance instead.
