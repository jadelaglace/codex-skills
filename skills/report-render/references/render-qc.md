# Rendering QC reference

Use this reference when a run needs a repeatable evidence record.

## Run record

Record:

```text
input: path or stable artifact id
input_hash: optional content hash
mode: long | paged
profile: named local profile or none
viewport: width × height CSS pixels
scale: device scale factor
renderer: browser/tool identity and version
outputs: exact PNG paths and dimensions
checks: pass/warn/fail/skipped/unavailable with evidence
```

## Conservative checks

- Long output height should match the measured content height within the
  renderer's known tolerance.
- Paged output must have contiguous numbering and no unexpected empty page.
- A blank or nearly blank horizontal band is a layout defect unless the
  template explicitly declares it.
- Text and tables must remain inside the intended content width; clipping at
  the right or bottom edge is a failure.
- Missing fonts or images are reported as defects, not silently substituted in
  the evidence record.

If a check requires a visual model or OCR service that is not configured,
mark it `unavailable` and keep the local geometric checks.
