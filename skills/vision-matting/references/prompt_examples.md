# Layering prompts

The decomposition model is prompt-driven: it draws the layer boundary where the
prompt says it is. Vague prompts produce merged layers, so write the prompt like
a scene description with an explicit foreground/background assignment.

## Template

Single subject:

```
<detailed background description> 是背景，<detailed subject description> 是前景
```

Two or more layers, near to far:

```
最前方的<layer 1>是前景1，中间的<layer 2>是前景2，远处的<layer 3>是背景
```

English works too, but keep the assignment explicit:

```
a red ceramic mug on a white desk is the foreground; a plain white studio
backdrop with a soft gradient is the background
```

## Rules that change the result

1. **Enumerate every foreground element.** Anything not named is treated as
   background and disappears with it.
2. **Describe colour, material, position and count** — "the silver SUV facing
   left, four visible wheels" beats "the car".
3. **Say what to keep.** For a product shot, add "及其在地面上的阴影" (and its
   shadow on the floor) when the shadow must survive.
4. **Order by depth**, nearest first; the layer count must match the description.
5. **Name the edge quality** when the material is hard: "轮廓边缘清晰" reduces
   soft, ragged boundaries.
6. **Keep one intention per run.** Changing background text and layer count in
   the same edit makes a failure hard to attribute.

## Pre-submit checklist

- [ ] every foreground element appears before the foreground marker
- [ ] background description is specific (colour, surface, gradient)
- [ ] shadow/reflection ownership stated explicitly
- [ ] number of described layers equals `--layers`
- [ ] seed recorded, so a good result can be reproduced

## Known limits

- A shadow that the model assigns to the background layer cannot be recovered by
  re-prompting in most cases. Use `shadow-extract` + `merge-over` instead of
  retrying with longer prompts.
- A layer with no described content comes back empty. That is a prompt/layer
  count mismatch, not a server fault.