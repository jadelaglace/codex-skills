# Standards And Visual Verification

Use the medium's applicable requirements, not a universal visual style.

## Make Standards Implementable

| Area | Specify when applicable | Inspect on actual output |
| --- | --- | --- |
| Principles | Audience/task, information priority, tone, density | Important content remains discoverable and its meaning intact |
| Color | Semantic roles, real values/tokens, state meaning and contrast | Text/background contrast and status are understandable beyond color alone |
| Typography | Fonts/fallbacks, sizes, weights, line height, hierarchy | Actual font render, mixed scripts, long titles, small text and line breaks |
| Spacing/layout | Scale, grid, padding, alignment, content widths and breakpoints | Crowding, overflow, clipping, page breaks and responsive changes |
| Components | Anatomy, behavior, data limits, valid/empty/loading/error/disabled states | Rendered states and actionable feedback match real capability |
| Navigation/copy | Labels, reading order, actions, provenance/evidence links | Users can find the next action and evidence; link targets actually resolve |
| Imagery/diagrams | Role, aspect ratio, crop, labels, captions and source | Relevant legible content and safe crops; diagrams retain meaningful relations |
| Motion/accessibility | Focus order, keyboard, names, contrast, reduced motion as required | Relevant behavior and accessibility measurements, not screenshot guesses |

Values and thresholds come from adopted project/platform/accessibility
requirements. For example, when WCAG AA is the adopted target, measure its
applicable contrast and interaction criteria; do not claim conformance from
visual impression alone. Identify the standard version and tested scope.

Templates define required content, optional slots, limits and allowed variations.
Use representative real-shaped content, including long titles, empty values,
multilingual text, dense data, and images where those can occur. Decorative
placeholders are not evidence that the real content fits. Do not expose internal
build/storage mechanics to users unless those details help them decide or act.

## Match Verification To The Medium

| Medium | Actual evidence | Limits to state |
| --- | --- | --- |
| Web/app | Render at relevant sizes/states, plus interaction and keyboard checks where in scope | A static image cannot prove focus order, live behavior, or backend readiness |
| Document/PDF | Native/document render and target export, relevant pages and breaks | A source file or one preview cannot prove all pages or correct export |
| Slides | Rendered relevant slides plus target presentation/export conditions | Source shapes do not prove font fit, crop, or final presentation readability |
| Diagram/image/template | Intended-size render with actual labels/content and relevant variations | A moodboard or one empty template does not prove instantiated output quality |

Choose tools available in the environment. Use a suitable artifact Skill if it
exists and applies; missing tools are a reported verification limit, not reason
to fabricate screenshots or install unrelated dependencies without scope.

## Self-Check And Refinement Record

Use a compact record in the existing artifact/design evidence:

```text
Artifact/version, standard/template version, content identity
Page/view/state, render size/environment
Check and expected behavior -> observation -> evidence
Defect impact and owner -> repair -> re-render/re-inspection result
Unverified checks, exceptions, final visual scope and return destination
```

Reject a visual pass for required clipped/missing content, unreadable required
labels, inaccessible required controls, misleading success/status, broken
required navigation, or required cases that were not inspected. A chosen visual
direction can remain accepted while one implementation fails; repair the
implementation instead of silently weakening the standard.

Verify content and provenance alongside appearance. Generated reading views
must preserve required source/evidence access and meaningful status. A count of
notes/pages or a machine checker may prove a structural condition, not readable
navigation, intact media, or actual visual quality. These distinctions reflect
Babata's package-to-live and rendered learning-view experience, not a fixed
Obsidian layout or a mandated number of media/learning sections.

When a visual defect comes from an upstream data/interface constraint, report
the dependency and return it to architecture or product with evidence. Do not
hide the issue through truncation, fake success text, or removal of required
content. Return separate visual and behavioral conclusions after refinement.
