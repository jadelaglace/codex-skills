# Codex Skills

Personal Codex skills maintained by `jadelaglace`.

<!-- workspace-recovery:start -->
## Workspace recovery

1. At a new session, compaction, or interrupted-task recovery, read any available goal/task-state record first; otherwise use the current plan.
2. Then read the [current plan](docs/skill-replication-plan.md) and reconcile its current item with the latest user instruction and Goal state.
3. Preserve completed instruction instances; held follow-ups need their explicit resume condition. An ordinary synchronous command failure with intact context is handled locally, not as a full recovery.

This block is a shallow entry point; the linked plan owns current progress.
<!-- workspace-recovery:end -->

## Skills

- `product-docs` (`1.0.4`): maintain product intent, acceptance, architecture, delivery status, and evidence without turning documentation governance into unnecessary ceremony.
- `handoff-context` (`1.0.2`): create concise, evidence-backed stage handoffs, with bounded multi-Agent write-conflict protection, that a new conversation can use to continue safely without replaying terminal work.
- `architecture` (`1.1.0`): define technical contracts and verify functional-unit and integration evidence.
- `code-quality` (`1.1.0`): implement and review code against adopted contracts, tests, and quality gates.
- `design-standards` (`1.1.0`): create reusable design standards and verify actual rendered outputs.
- `report-render` (`1.0.0`): render existing HTML reports to long or paginated PNGs and record visual QC without changing report facts.
- `research-report` (`1.1.0`): orchestrate traceable research from question and evidence through Markdown, adversarial review, rendered delivery, and archival.

Working-tree caveat (2026-10-31): the `handoff-context` 1.0.2 entry and the
uncommitted product-docs recovery edits belong to the halted #16 experiment,
not the accepted published baseline. Published handoff-context remains 1.0.1;
no rollback or continuation is implied. The [1028 hardening plan](docs/skill-absorption-1028-plan.md)
is a proposal, not an implemented release.

The screenshot-derived replication boundary and current validation status are recorded in
[`docs/skill-replication-plan.md`](docs/skill-replication-plan.md). The two skills are
portable workflow contracts; no source screenshot credentials, private endpoints, or
project-specific scripts are included. They do not bundle renderer scripts or HTML
templates, and their end-to-end research/rendering paths have not yet been proven.

For the whole workspace, see the [conversation history, rules, and pitfalls](docs/workspace-history-and-rules.md).
Detailed source, installation, and validation evidence is in
[`docs/replication-evidence.md`](docs/replication-evidence.md). These records do not
replace each Skill's own contract or authorize queued work.

Skill versions are independent from repository release versions. Each Skill's
`metadata.version` records that Skill's own public contract version. Repository
publication tags use the date-based form `repo-YYYY.MM.DD` with a same-day
revision suffix when needed; this publication is `repo-2026.10.25.3`. This identifies the coordinated contents of
the repository and must not be interpreted as a Skill version. Historical
numeric tags such as `1.0.0`–`1.0.2` are retained for compatibility and are not
reused for new publications.

The initial commit preserves the pre-optimization baseline of `product-docs`.

No repository-wide license is granted unless one is added explicitly later.
