---
name: report-render
description: Render an existing HTML report into long or paginated PNG images and perform structure and visual-quality checks. Use when a report already has content and needs a reviewable image deliverable; do not use this skill to research, rewrite, or certify report facts.
metadata:
  version: "1.0.0"
---

# Report Render

Turn a content-complete HTML report into a deterministic, reviewable PNG
deliverable. This is a presentation and verification boundary: it may inspect
structure and rendering, but must not alter facts, sources, conclusions, or
research status.

## Inputs and outputs

Require an input HTML file, an explicit output directory, and a selected mode:

- **long**: one vertically scrolling PNG for sharing or quick review;
- **paged**: numbered PNG pages with explicit page-break rules for printing or
  archival review.

Accept optional template/profile, viewport width, target page height, device
scale factor, wait time, prefix/suffix, and image quality. Keep these values
local to the run; never assume a machine-specific path or browser installation.

Report the exact input identity, mode, parameters, output files, and checks.
Use a clean output directory or a collision-safe run directory; do not silently
delete unrelated files.

## Safe rendering workflow

1. Inspect the HTML and referenced local assets. Refuse or explicitly skip
   missing, remote, or restricted assets rather than fabricating them.
2. Select a profile without changing content semantics. A profile may define
   CSS variables, headings, cards, tables, callouts, header/footer, and print
   dimensions. Keep theme changes isolated from the source HTML.
3. Use an available standards-compliant browser renderer. If no renderer is
   available, return `unavailable` with the reason and a manual fallback; do
   not claim a PNG was produced.
4. For long mode, measure CSS height and compare it with renderer/image limits.
   Warn on blank bands, clipping, missing footer, or a suspiciously truncated
   image. If the limit is exceeded or a check fails, recommend paged mode.
5. For paged mode, keep structural units together where possible. Treat
   explicit page breaks, section headings, tables, callouts, and figure blocks
   as boundaries. Do not split a table row or card merely to fill space.
6. Read back generated images and check dimensions, file count, non-empty
   content, footer/page numbering when requested, and representative visual
   regions. A successful command alone is not visual acceptance.

## QC and failure states

Classify each check as `pass`, `warn`, `fail`, `skipped`, or `unavailable`.
At minimum inspect:

- HTML parse and asset loading;
- expected viewport and output dimensions;
- clipping, overflow, blank bands, broken glyphs, and unreadable small text;
- page boundaries, numbering, headers/footers, and table/card integrity;
- output-directory contamination and stale PNG collisions.

Stop before delivery on missing input, untrusted output, content loss,
credential exposure, or a failed required check. A warning may be delivered
only when it is recorded with the affected output and the user can review it.

## Explicit boundary

This skill does not perform web search, source verification, image recognition,
Markdown research, document authoring, PDF conversion, or publication. Call an
appropriate specialist or provide a manual handoff for those tasks. External
browser paths, services, tokens, and scripts belong in local configuration and
must never be copied into this skill or a public repository.
