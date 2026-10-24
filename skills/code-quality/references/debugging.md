# Debugging

When a defect survives one careful reading of the code, work these four steps in
order. Skipping ahead to a hypothesis is what makes debugging expensive; each step
below exists because a plausible-looking shortcut produced a wrong answer.

## 1. Classify The Symptom Before Naming A Cause

State what is actually observed: nothing rendered, rendered but invisible,
rendered but stale, rendered but wrong. These are different failures.

Wrong: "the scene is black, so the lighting is broken." An empty canvas means
nothing was drawn — geometry, camera, or load order — and lighting cannot be the
first suspect. Classify first, write the classification down, then hypothesize.

## 2. Make The Probe Faithful

A probe is evidence only if it exercises the same path, inputs, and environment as
the failing case. Otherwise it proves the probe.

Wrong: a probe that renders a toy scene passes every check while the real asset
still shows nothing. That green result was never about the failing path.

## 3. Bisect With A Variation Matrix

List the dimensions that can differ — input, asset, runtime version, feature flag,
data shape, environment. Switch one at a time and record which switch moves the
symptom.

Wrong: changing the asset and the renderer in the same round. When the symptom
disappears you have learned nothing about which change did it.

## 4. Verify The Measurement Before Trusting It

Some reads are undefined for the thing being read, and an undefined read looks
exactly like a defect.

Wrong: reading pixels back from the default framebuffer returns undefined content.
Two rounds of "everything is black" were measurement garbage, not a rendering
failure. Prefer a measurement with a known-good control: if the instrument cannot
report a passing case, it cannot report a failing one either.
