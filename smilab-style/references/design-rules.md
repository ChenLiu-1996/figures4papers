# Design rules

English version of [style-rules.ja.md](style-rules.ja.md). `#NN` = `images/NN_*.png` (see [gallery.md](gallery.md)).

## Why the references look good

1. **Few, meaningful colors** — 3–5 hues, each bound to one concept across the paper.
2. **Tonal pairs** — light pastel fill + darker edge of the same hue; many colors without noise.
3. **Clear foreground/background** — color, bold and thick borders only for the proposed method / new modules; baselines and standard parts (Projection, Tokenizer, LayerNorm) are gray.
4. **Notation parity** — figure math matches the paper's equations.
5. **Concrete data** — real spectrograms, frames, brain renderings show what goes in and out.
6. **Grid alignment** — same-size blocks, equal spacing, orthogonal arrows, aligned baselines.
7. **Shared visual vocabulary** between schematics and plots (#28–30 digit badges, #12–17 method colors).

## Color

### Tonal pairs (`smilab_style.TONES`)

| Tone | Fill | Edge | Typical use |
|---|---|---|---|
| blue | `#E8EEFA` | `#7A96D6` | inputs / conditions (#01, #26) |
| yellow | `#FFF6DA` | `#E2BE55` | core layer (#02, #21) |
| purple | `#EDE3F3` | `#A77DB8` | proposed block (#04, #06) |
| orange | `#F9E3CC` | `#E8A36A` | sub-module / zoom (#04b, #06, #07) |
| green | `#E3F1E1` | `#7FB77A` | fusion / mixer (#21, #26) |
| red | `#FBE4E1` | `#E08A82` | trainable head / decoder (#01, #23, #29) |
| gray | `#F2F2F2` | `#9A9A9A` | generic components |

Panel backgrounds use the same hues even lighter (≈ alpha 0.15–0.3). Gradients only mean *mixture of two states* (#06, #18).

### Semantics
- Fix **method → color** once per paper (`method_colors`) and reuse it (#14–17 share one map across 4 figures).
- Proposed = warm red-pink `#D9837F` (plots) / saturated blue `#3F84AA` is allowed for line plots (#10). Never reuse the "ours" color for a baseline.
- ✗ red `#D9443A`, ✓ green `#4CAF50`. ❄ = frozen, 🔥 = trainable, placed at the block's top-left.
- Heatmaps: diverging `coolwarm` for signed / relative values (#24); `YlOrRd` for intensity (#12, #14).

### Plot colors
- Bars: pastel (`METHOD_CYCLE`) with an edge at 85 % brightness.
- Lines: more chroma (`LINE_CYCLE`), 2–3 pt, plus markers.
- Saturated bars (#30) only on a light gray `#F5F5F5` plotting area.

## Typography
- Paper figures: **Times New Roman + STIX math** (`apply_style("paper")`). Teasers / slides: **Helvetica** (`"teaser"`). One family per figure.
- Math: bold-italic vectors/matrices ($\boldsymbol{X}$), calligraphic sets ($\mathcal{G}$), upright subscripts ($\boldsymbol{x}_\mathrm{cand}$).
- At most three levels: bold panel title (optionally in the panel's edge color, #04) → regular labels → small annotations (`×24 trials`, `(See Sec. 4)`).
- Panel labels: bold `(a)` at top-left (default). Caption-style `(a) Module Overview` under the panel is allowed for schematics — pick one per paper.
- Text inputs / prompts: italic, in double quotes, inside a dashed box.
- Labels in tall thin blocks are rotated 90°.
- Printed size 8–10 pt; never below 6 pt.

## Plots
- Light grid `#E6E6E6`, no top/right spines, framed legend with thin gray edge and square patches.
- Axis label = `name [unit] ↓/↑` (`sm.label`).
- Proposed method last; bold in legend and tick labels.
- One shared legend for multi-panel figures (top row #10, or right column #14).
- Significance: `*` p<.05, `**` p<.01, `***` p<.001 above bars (or stacked vertically at the right of h-bars, #17).
- Bars: value written vertically inside the bar bottom; black thin error bars with small caps. A truncated y-axis is allowed but the lower limit must be visible on the axis.
- Ablation h-bars: full model colored, others gray `#DCDDE0`, bold group headers, numbered rows `(b-i) w/o fθ`, best value bold per column, solid vertical divider between task groups.
- Lines: vary **color and marker** (◆ ▲ ■ ●); proposed = circle on top.
- Scatter: label points directly in their own color; marker = method, edge style = dataset; alpha ≈ 0.75 with darker edge. Bubble size may encode cost (#33).
- Highlight cells / diagonals with a thick colored frame (#24, #26).

## Consistency (per paper)
1. One method→color table for all figures.
2. One module→tone table shared by schematics and plots.
3. Same font, panel-label position, arrow color, corner radius everywhere.
4. Icons (❄/🔥, ✓/✗) keep one meaning.

## Don'ts
- Saturated large fills, 3D effects, strong drop shadows.
- More than ~5 hues without meaning.
- Notation that differs from the paper.
- Typos (seen in references: "Hierachical" #07, "Attentnion" #26, "Sculp" #12, "descriptivenss" #31).
- Mixing black and gray arrows without a reason.
