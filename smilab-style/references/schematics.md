# Schematic, architecture and teaser figures

For figures drawn in draw.io / PowerPoint / Keynote / Figma. Colors: [design-rules.md](design-rules.md#tonal-pairs-smilab_styletones).

## Shape vocabulary

| Shape | Meaning | Ref |
|---|---|---|
| Rounded rectangle (small radius, ~4–6 px) | processing block / module | all |
| Trapezoid | encoder or head (narrows/widens dimension) | #08, #09, #12, #23, #29 |
| Tall thin rectangle, rotated label | layer (LayerNorm, FFN, DiT block) | #02, #04, #19 |
| Dashed rectangle | text input, latent state, legend, group (`×L Blocks`) | #02, #06, #09, #31 |
| Circle with ⊕ ⊗ ⊙ ⊖ | add / multiply / element-wise ops | #02, #04, #12, #31 |
| Offset stacked cards | multiple items: T frames, slices, batches | #12, #13, #21, #26 |
| Row of small squares | token sequence | #06, #20, #21 |
| Cylinder | database | #25 |

## Lines and arrows
- Gray `#666666`, 0.75–1 pt, small filled heads. Black only for emphasis.
- **Orthogonal (Manhattan) routing.** Diagonals only for conceptual links (#08, #12).
- At crossings draw a **line hop** (#02, #04).
- Solid = data flow; **dashed = feedback / iteration / inference-only / conceptual** (#04, #12, #28).
- Colored arrows only when they carry that color's concept (#07 forward/backward, #08, #31).
- Bundle branches on a shared x or y coordinate (#04 β/γ/α, #26 five arrows from $l_+$).

## Layout
- One reading direction: left→right (pipelines) or bottom→top (LLM stacks, #06, #21).
- Split large figures into 2–3 panels, separated by a vertical dashed line (#07, #08, #24) or a thin solid line (#03, #17), or enclose each panel in a tinted rounded box with a bold title at top-left (#13, #18, #19, #26).
- Zoom-ins: colored frame + curved arrow to a detail panel in the same color (#04 S5 → (b), #15 red zoom).
- Same-type blocks: identical width/height, equal gaps; snap to a grid.
- Legend in an empty corner, inside a thin gray (dashed) frame (#07, #09, #13).
- Subtle shadow allowed (offset 1–2 px, ≤ 20 % opacity) — never heavier than the references.

## Emphasis
- New modules: tone color + 🔥; reused pretrained parts: gray or tone + ❄.
- Standard parts (Projection, Tokenizer, LLM) in gray so the novelty stands out (#06, #21).
- Mirror the paper's notation on every arrow / tensor label.

## Teaser (Figure 1) template
1. **Prior work ✗ vs ours ✓** side by side (#08, #20, #22, #28, #32), split by a dashed divider.
2. A concrete input example (real image, caption, audio).
3. Numeric comparison boxes at the bottom/right; ours **bold with a thicker border**; human score with ≈ (#08, #22).
4. Sparse icons/emoji (👤, 🎬, 😊/☹) for instant reading (#22, #25, #33).

## Export
- Export vector PDF (fonts embedded). Insert at final column width so text is 8–10 pt.
- Embedded photos: ≥ 300 dpi at print size, thin gray border (`#9A9A9A`, 0.5 pt).
