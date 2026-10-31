# Video / PAG transparency QC

Still-image QC ends at a PNG. Animated transparency (PAG, APNG, WebM with alpha)
adds encoding, playback and frame order, so it needs five layers of checks. A
product that passed four of them has not been verified.

## Five-layer self-check

| Layer | What to do | What it proves |
| --- | --- | --- |
| 1. Pre-encode frames | split alpha and RGB, view them separately, frame by frame at the boundaries | the matte is right before codec loss |
| 2. CV metrics | edge width, oscillation, stray pixels, PSNR >= 43 dB per frame; coverage change > 3% between frames means propagation failed | numerically stable matte |
| 3. Multi-background overlay | composite frames over white, black and a saturated background | no fringes or halos that only one background hides |
| 4. Post-encode re-read | decode the encoded file and repeat layers 1-3 | the encoder did not introduce defects |
| 5. Real playback | render in the target player (for PAG: libpag, driven headlessly) and screenshot it next to the reference asset | what the user will actually see |

Layer 5 is the one that catches "it looked fine in our own decoder". Treat a
frame dump as evidence only when it came from the real player.

## Defect → cause → fix

| Defect | Cause | Fix |
| --- | --- | --- |
| White fringe | key reference kernel too large, or unpremultiplied edges amplifying noise | smaller kernel, push edge colour inward |
| Black fringe | residual despill / contamination | colour inpainting from the interior |
| Soft edge | gaussian widening of the boundary band | supersample 2x then anti-alias down |
| Grey skirt | keying extended into the shadow | soften with a luminance gate (0.30-0.50) |
| Jagged edge | per-pixel noise plus hard edge, no AA | sample AA at 2x, enable animation tuning, crf ~17 |
| Floating noise | H.264 deblocking bleeding into alpha | put alpha to the right of content with a ~12 px pure-black gap, never copy content pixels into it |
| Invisible shadow | constant light grey equal to the background | darker grey plus a contact line, AO-style |
| Watermark residue | small high-contrast island | connected-component removal |
| Coverage jumps | mask propagation drift | re-seed the propagation at the jump, or split the clip |

## Encoder pitfalls

- Encode with `threads=1`; multi-slice NAL units break alpha frame order.
- Emission order and the `Y = (219a >> 8) + 16` mapping must match the PAG
  layout, otherwise alpha is off by a constant.
- Mask sources: a SAM2-style propagation that changes coverage by more than 3%
  between frames has failed; give the subject and props their own boxes and do
  not box the shadow (capture it in post).

## Reporting

Report per layer: what was checked, on which frames, with which numbers, and
what was looked at by eye or by player. "Encoded and played" without a player
screenshot is not layer 5.