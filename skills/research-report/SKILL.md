---
name: research-report
description: Orchestrate a traceable research-report project from user question through source collection, evidence and methodology, Markdown drafting, rendered PNG review, and versioned archival. Use when the user needs a research report workflow; it does not itself provide a search provider or certify external facts.
metadata:
  version: "1.1.0"
---

# Research Report

Own the method and project orchestration for a research report. Keep the
research question, evidence, interpretation, rendering, and publication
boundaries explicit so the delivery can be resumed without replaying a hidden
process. Providers and tools are replaceable; the evidence discipline is not.

## Trigger and delivery shape

Start when the user asks to investigate a topic and produce a structured,
reviewable report. Make the smallest useful project workspace and offer three
pause points:

1. **dialogue brief**: question, scope, audience, date boundary, output form,
   and unresolved choices;
2. **report draft**: Markdown with claims, sources, methods, caveats, and an
   evidence register;
3. **rendered delivery**: PNG output reviewed with `report-render`, then an
   archive/version record.

Do not force later stages when the user only asked for a brief or analysis.

## Adversarial review before release

Green calculations and a successful renderer are necessary but do not establish
that a report is review-ready. Before calling a delivery complete, run a fresh
defect-oriented review after the normal checks. Record expected versus observed
behavior, the trigger, impact, affected contract, and the evidence file or code
location. Create or update a tracked defect record in the project's existing
mechanism for every unresolved release-blocking finding; when no such mechanism
exists, keep the finding and its repair status in the run evidence. Close a
finding only after the repair and regression evidence exist.

For reports with interactive or plotted output:

1. Preserve the complete underlying series. If the default view is a zoomed
   focus window, provide an explicit full-horizon view or an equally direct way
   to inspect the whole series; a tiny thumbnail alone must not imply that a
   curve ended.
2. Treat values expressed under different units, bases, dates, or conversion
   regimes as distinct. Check every plotted series and annotation under each
   supported basis, including post-transition paths.
3. Compute axis ranges from every visible series, threshold, annotation, and
   comparison target. A line drawn outside the range is a correctness defect,
   not merely a styling issue.
4. Test the states users can actually select, including no event/no crossover,
   long horizons, boundary values, multiple overlays, and correction
   combinations. Do not substitute one happy-path screenshot for these states.
5. Review representative rendered images by eye for misleading truncation,
   unreadable labels, legend collisions, broken glyphs, clipped tables, blank
   bands, and stale output files. Keep the visual review record alongside the
   render manifest.

For a parameterized model, distinguish the model's main result from comparison
curves. A comparison must not silently inherit the active case's units,
targets, or assumptions unless that inheritance is part of the contract and is
shown in the label.

## Evidence-first workflow

1. Capture the user's question and constraints before searching. Keep direct
   wording, adopted requirements, external advice, and Agent interpretation
   distinct.
2. Establish a bounded source register. For every source preserve locator,
   retrieval time, source identity, relevant excerpt or artifact, scope, and
   credibility state: `trusted`, `provisional`, `rejected`, `unavailable`, or
   `not-yet-checked`.
3. Record competing definitions, dates, samples, and measurement units. When
   sources conflict, show both the conflict and the chosen interpretation;
   never average incompatible figures to make the report look consistent.
4. Mark claims that are direct evidence, inference, assumption, recommendation,
   or unresolved. Never turn a search hit, title, placeholder, or locator into
   verified evidence.
5. Draft a report that can be read without the hidden work log: executive
   conclusion, scope/method, evidence and limitations, analysis, implications,
   references, and an explicit as-of date.
6. Render the Markdown/HTML through an available route. Prefer the independent
   `report-render` skill for PNG generation and QC. If it is unavailable,
   deliver Markdown and record the rendering gap instead of claiming image
   delivery.
7. Archive sources, report Markdown, rendered outputs, and a concise run record
   together. Use a new version or dated record; never overwrite the original
   evidence or silently rewrite a previous conclusion.

## Project layout (portable template)

Use a project-local layout only when it helps the reader:

```text
project/
├── AGENTS.md              # local conventions, if needed
├── process/               # brief, source register, methods, run evidence
├── reports/               # final PNGs and explicitly approved public outputs
├── docs/                  # Markdown report and authority documents
└── package.json           # optional renderer metadata; never required
```

Keep raw source bodies and private provenance outside a public repository unless
the user explicitly authorizes safe publication. Keep credentials in external
configuration. A report may link to a source without embedding its body.

## Boundaries and routing

- Search, web access, API calls, OCR, image recognition, PDF conversion, and
  domain-specific analysis are provider or specialist responsibilities. Probe
  only an authorized, available route and record its actual result.
- HTML structure, templates, viewport choices, PNG generation, and visual QC
  belong to `report-render`; do not duplicate its renderer instructions here.
- Product requirements and acceptance belong to `product-docs`; architecture,
  code, and design standards remain with their specialist skills.
- Publication, Git push, or external sharing requires explicit authorization.

## Completion ledger

Keep these dimensions separate in the final run record:

```text
question captured
sources collected
claims checked
draft complete
render complete
visual QC complete
archive/version recorded
user accepted
```

Use explicit `partial`, `blocked`, `failed`, `skipped`, or `unavailable` states.
Do not call the report complete because a Markdown file, a script, or a PNG
exists. Report the remaining gap and the exact evidence that supports each
closed dimension.
