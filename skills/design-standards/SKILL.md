---
name: design-standards
description: Develop and apply reusable visual and interaction standards through moodboards, adopted principles, standards libraries, templates, rendered self-checks, refinement, and versioned reuse. Use for design systems, visual guidelines, reusable templates, or visual acceptance of actual interfaces, documents, presentations, and other artifacts. Product goals and final acceptance stay upstream; backend architecture and code verification remain separate.
metadata:
  version: "1.1.0"
---

# 设计规范

Guide implementation with usable design standards, receive actual outputs,
verify them visually, drive refinement, and return evidence upstream. Design is
a specialist part of product work and can also serve a standalone artifact.

## Receive The Goal And Choose The Entry Point

Follow local instructions and recovery rules. Read the intended audience, task,
content, medium, brand/accessibility constraints, acceptance criteria, and
existing adopted standards. Identify analysis, exploration, standard creation,
application, or visual-review scope; review does not authorize redesigning the
product or publishing outputs.

For direct use without a PRD, establish the small set of goal and success
conditions needed for this artifact. Do not invent a software architecture or
UI for a document or poster. Preserve actual content and meaning; decoration
cannot remove evidence, hide limitations, or imply a workflow is available.

Use existing standards/templates when adequate. Start with a moodboard only
when the visual direction is genuinely open. A local repair may start with the
rendered output and a targeted check; it does not require a new design system.

## Explore, Adopt, And Specify

Before collecting references, extract three to five quality words from the actual
requirement and have them confirmed. References gathered before the words are
fixed drift toward whatever looked good that day.

1. When exploring, make reference directions useful for the audience and task:
   mood, hierarchy, density, typography, color, composition, and material/media
   treatment. Label sources and alternatives as exploration; a moodboard is
   not an adopted standard or acceptance evidence.
2. Translate the chosen direction into observable principles and rules, stating
   what is adopted, proposed, or unresolved. For a key visual surface, put two or
   three candidates side by side, each with one sentence on how it differs. The
   user chooses; this layer's job is to make the difference legible, not to decide.
   Write each rule so it can be judged: a value, a range, or a property visible in
   the render. Words that cannot be judged belong in the moodboard, not in the
   standard. Routine reversible design choices
   within the authorized scope can be made by the Agent; material changes to
   audience, content, value judgments, or product acceptance return upstream.
3. Build or extend only the necessary standards library: semantic colors,
   typography, spacing, layout, imagery, and applicable component/interaction
   states, responsive behavior, motion, accessibility, and copy conventions.
   Define real values or constraints with examples, not only adjectives.
4. Turn repeatable structure into templates with fixed rules, variable content,
   supported sizes/states, and boundaries for exceptions. For software, connect
   visual rules to actual tokens/components and their adopted version. For
   documents or slides, use their native styles/layouts where appropriate. For
   generated or rendered output, anchor the brief on real reference images and
   state the prohibitions explicitly: no invented lettering, numerals, logos, or
   watermarks. What is not forbidden will eventually appear.
5. Read [visual-verification.md](references/visual-verification.md) when creating
   standards/templates or reviewing/refining an output. Select relevant visual
   cases and expected results before issuing guidance.
   Read it also for screen-by-screen comparison against a reference, prompt writing,
   magnified text checks, and converging adjustments.
6. Issue standard/template references, accepted version, actual content and
   medium constraints, required states, and visual acceptance checks to the
   implementation. Keep the guidance in the existing design authority or
   artifact, not a competing requirements document.

Design can guide both architecture and code. Return technical feasibility issues
to `architecture` when available; use `code-quality` for authorized software
implementation. Select the appropriate available artifact-production workflow
for other media. Specialist selection alone does not authorize new agents,
other-task messages, generation costs, publication, or expanded scope.

## Receive, Inspect, And Refine

Receive the actual implementation/export, adopted standard version, relevant
content/states/sizes, render environment, and known limitations. Render or open
it with an appropriate available tool and visually inspect the result. Source,
tokens, a DOM tree, a file count, or a successful generator cannot alone prove
visual acceptance. If rendering or inspection is unavailable, distinguish
source-level checks from unverified visual claims and return the limitation.

For an interface, examine the affected desktop/mobile sizes, content extremes,
and states relevant to the contract; test important interactions and keyboard
behavior where authorized and possible. For a document, slide, diagram, or
template, inspect affected pages/slides and the actual intended export medium.
Do not replace a native render with an unrelated mockup and call it accepted.

Lift dark output before judging it. "Everything is black" is treated as
unreadable first, not as a verdict; a brightness check costs less than a redesign.

Check hierarchy, typography, spacing, alignment, overflow, readability, imagery,
navigation/evidence links, and applicable state/accessibility rules. Validate
content completeness and real status meaning as well as appearance. Record
concrete defects by location/state, violated rule or task outcome, and evidence.
Prioritize unusable or misleading outputs before cosmetic refinement.

In an authorized application/refinement task, fix defects within scope or return
them to the implementing layer. Re-render and re-inspect affected outputs after
changes; retain remaining gaps explicitly. In review-only mode, return findings
without edits. Do not invent an arbitrary number of polish passes: stop when
the applicable checks pass, the scope terminal is reached, or a real limitation
prevents further verification.

Visual review enforces the adopted standard; it does not redesign. A failing
output leaves with a difference list against the rule, and the fix returns to the
implementing layer.

Required visual cases must have actual inspected evidence before a visual pass.
Reuse adequate evidence for unchanged unaffected output. A selected screenshot
proves that view; it does not prove all pages, responsive states, interactions,
or user usability. A visually conforming design is not automatically a usable
or finally accepted product.

## Version And Return Upstream

Keep adopted standard/template versions, implementation references, material
exceptions, and change impact discoverable. An exploratory revision does not
silently replace an adopted library. Update affected templates/consumers when
the adopted rule changes; do not recreate every artifact for a local refinement.

Return a concise result to `product-docs` when serving product delivery, or to
the standalone task's owner:

```text
Goal, scope, artifact identity, adopted standard/template version
Guidance issued and actual outputs received
Inspected pages/views/states, render environment, evidence pointers
Visual checks: passed / failed / partial / skipped / blocked
Defects, refinements, re-inspection evidence, unverified behavior and limitations
Remaining upstream decisions or implementation actions
```

Keep product acceptance, visual acceptance, and architecture/code checks
distinct. Close the visual loop on actual artifacts before returning its
conclusion; a delivered standards library or template alone closes only the
standards task, not visual acceptance of an implementation that was never seen.

<!-- 2026-10-24: criteria adapted from a parallel-environment layered skill set;
     project-specific bindings excluded. -->
