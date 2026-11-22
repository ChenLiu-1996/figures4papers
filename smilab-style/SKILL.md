---
name: smilab-style
description: >-
  SMILab house style for paper figures: matplotlib result plots (bars with in-bar
  values and significance stars, ablation h-bars, marker+color line plots,
  directly-labelled scatter) AND rules for schematic / architecture / teaser
  figures drawn in draw.io, PowerPoint, Keynote or Figma. Use when making or
  reviewing any figure for an SMILab paper, or when the user says "smilab style".
  Derived from 33 reference figures in references/images/.
---

# smilab-style

Open files only as needed.

| File | Open when |
|------|-----------|
| [references/design-rules.md](references/design-rules.md) | Always first: the core rules (color, type, emphasis, consistency) |
| [references/schematics.md](references/schematics.md) | Architecture / pipeline / teaser figures (non-matplotlib) |
| [references/api.md](references/api.md) | Writing matplotlib code with `smilab_style.py` |
| [references/gallery.md](references/gallery.md) | Picking a reference image to imitate; what each one teaches |
| [references/style-rules.ja.md](references/style-rules.ja.md) | Japanese original of the rules (reviewed by the user) |
| [examples/demo.py](examples/demo.py) | Runnable examples of every plot helper |

## Ten rules to remember

1. 3–5 hues per figure; **one concept = one color**, fixed across the whole paper.
2. Blocks/bars = **light fill + darker same-hue edge**. No saturated large areas, no 3D, no heavy shadows.
3. **Proposed method**: red-pink `#D9837F`, placed last, **bold** in legends and tables. Baselines muted; generic modules gray.
4. Fonts: Times + STIX math for paper figures; Helvetica for teasers/slides. One family per figure.
5. Math in figures uses the **paper's exact notation** ($\boldsymbol{X}$, $\hat{y}$, $\mathcal{L}$).
6. Axis labels carry **units and a better-direction arrow**: `HD95 [mm] ↓`.
7. Bar values written **vertically inside the bar**; `* / ** / ***` above.
8. Arrows: gray `#666`, thin, orthogonal routing; dashed = feedback / inference-only / conceptual.
9. Pair abstract mechanisms with **real data thumbnails** (spectrograms, frames, brain surfaces).
10. Spell-check every label before export (references contain typos — don't copy them).

## Quick start

```python
import sys; sys.path.insert(0, "smilab-style")
import smilab_style as sm
sm.apply_style("paper")                       # or "teaser"
C = sm.method_colors(METHODS, ours="Ours")    # build once, reuse in every figure
sm.bar_compare(ax, METHODS, means, C, errs=sd, pvalues=p,
               ylabel=sm.label("HD95", "mm", "down"))
sm.save(fig, "figures/result")                # -> .pdf + .png
```

Python: matplotlib ≥ 3.7, numpy. Run headless with `matplotlib.use("Agg")`.
