# Design rules: base + SMILab diff

Base = [scientific-figure-making](../../scientific-figure-making/SKILL.md) ([design-theory](../../scientific-figure-making/references/design-theory.md), [common-patterns](../../scientific-figure-making/references/common-patterns.md)).
This file lists only what SMILab **overrides** or **adds**. `#NN` = [gallery](gallery.md) image.

## 1. Inherited (no change)

| Base rule | Note for SMILab |
|---|---|
| Blue `#0F4D92` = proposed / key method; greens = improvements; reds = baselines/contrasts; neutrals = background | Kept. Variants of the proposed method use lighter blues `#B7CAE2`, `#6F94BE` |
| Palette family only (no unrelated colors) | Kept. Pastel baselines come from the same family (`METHOD_CYCLE`) |
| Top/right spines off | Kept |
| Tightened y-limits (`min − margin` … `max + margin`) | Kept; the lower limit must stay visible on the axis |
| Hide x-ticks when the legend names the methods | Kept |
| Alpha/tint-based ablations, hatching for grayscale print | Kept |
| `fill_between` for uncertainty; 2–4 main curves per axis | Kept |
| dpi 300 (600 dense bars), `svg.fonttype='none'` | Kept; PDF also embeds TrueType (`pdf.fonttype=42`) |
| Dedicated legend panel for big legends | Kept as an option; default is one shared legend row (see A3) |
| Multi-panel consistency | Kept and extended to the whole paper (A1) |

## 2. Overrides

### O1 Fonts
- Base: Helvetica/Arial.
- SMILab: **Times New Roman + STIX math** for figures placed in a LaTeX paper, so figure text matches the body (#01–05, #12–17). Sans (base stack) only for teasers/slides (`mode="teaser"`). One family per figure.
- Math uses the paper's notation: bold-italic vectors ($\boldsymbol{X}$), calligraphic sets, upright subscripts ($\boldsymbol{x}_\mathrm{txt}$).

### O2 Size
- Base: very large canvases (45×12 in, 16–24 pt, 2–3 pt axes) shrunk in LaTeX.
- SMILab: **draw at print size** — single column ≈ 3.3 in, double ≈ 7.0 in; text 7–9 pt (≥ 6 pt), axes 0.8 pt. Printed sizes are then known and equal across figures. The base's wide left-to-right composition is kept, just at real width.

### O3 Bars and legends
- Base: values above bars in large type, black thick edges, frameless legend.
- SMILab (CANDLE-style, #14–16):
  - value written **vertically inside the bar** near its bottom (white on dark fills), leaving the space above for error bars and stars;
  - **thin edges of the same hue** (85 % brightness) instead of black;
  - **framed legend** (thin gray edge) with **square patches**, proposed method **bold**;
  - **light y-grid** `#E6E6E6`;
  - significance `*` p<.05, `**` p<.01, `***` p<.001 above the error bar.

## 3. Additions (not in the base)

### A1 Per-paper consistency
One method→color map for the whole paper (`method_colors`), reused by every figure (#14–17). Same for module→tone in schematics, and for icons.

### A2 Axis labels
`name [unit] ↓/↑` (`label()`), e.g. `HD95 [mm] ↓`. Direction lives on the axis label, not in the title.

### A3 Legends and labels
- Proposed method placed last and bold.
- Multi-panel: one shared legend row on top (#10) or one column at the right (#14).
- Scatter: label points directly in their own color instead of a legend (#05); marker = method, edge style = dataset.
- Lines: vary color **and** marker; proposed drawn on top, slightly thicker.

### A4 Ablation h-bars (#17)
Full model in blue, variants in light blue (inherited tint rule); bold group headers; numbered rows `(b-i) w/o fθ`; best value bold per column; stars at the right; solid divider between task groups.

### A5 Schematic colors
Tonal pairs (light fill + darker same-hue edge) from the base family — see `TONES` and [schematics.md](schematics.md). Color = concept; the proposed output/emphasis uses the blue tone (consistent with the base). Gradients only for "mixture of two states".

### A6 Icons and marks
✗ red / ✓ green; ❄ frozen / 🔥 trainable at a block's top-left; 👤 human reference.

### A7 Teaser (Figure 1)
Prior ✗ vs ours ✓, a concrete example, score boxes with ours bold + thick border and ≈ human (#08, #22). Details in [schematics.md](schematics.md).

### A8 Don'ts
Saturated large fills, 3D, heavy shadows, >5 meaningless hues, notation that differs from the paper, typos (references contain "Hierachical" #07, "Attentnion" #26, "Sculp" #12 — spell-check).
