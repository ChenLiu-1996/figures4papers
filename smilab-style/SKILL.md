---
name: smilab-style
description: >-
  SMILab layer on top of the scientific-figure-making skill. Load
  scientific-figure-making first (it is the base); this skill only overrides
  three of its rules (Times fonts, print-size drawing, CANDLE-style bars) and
  adds rules the base does not cover: schematic / architecture / teaser figures,
  direction arrows, significance stars, per-paper color consistency. Use for
  any figure in an SMILab paper or when the user says "smilab style".
---

# smilab-style (extends scientific-figure-making)

**Base first.** Read [../scientific-figure-making/SKILL.md](../scientific-figure-making/SKILL.md) and follow it. Apply this skill as a diff: where it says nothing, the base rule holds.

| File | Open when |
|------|-----------|
| [references/design-rules.md](references/design-rules.md) | Always: what is inherited / overridden / added |
| [references/schematics.md](references/schematics.md) | Architecture, pipeline and teaser figures (base has no rules for these) |
| [references/api.md](references/api.md) | Writing code with `smilab_style.py` (implements the base API + overrides) |
| [references/gallery.md](references/gallery.md) | The 33 reference figures the additions were derived from |
| [references/style-rules.ja.md](references/style-rules.ja.md) | Japanese version (reviewed by the user) |

## Overrides (only these three)

| # | Base rule | SMILab rule |
|---|---|---|
| O1 | Helvetica / Arial | **Times + STIX math** for paper figures; sans only for teasers/slides |
| O2 | Huge canvas (e.g. 45×12 in), 16–24 pt, then shrink | **Draw at print size** (3.3 / 7.0 in), 7–9 pt, 0.8 pt axes |
| O3 | Values above bars, black 1.5–3 pt edges, frameless legend | **Values inside bars (vertical)**, thin same-hue edges, **framed legend with square patches**, light y-grid, significance stars |

## Inherited unchanged (reminder)

Blue `#0F4D92` = proposed method; blue/green/red/neutral palette family; top/right spines off; tightened y-limits; hidden x-ticks when a legend names the methods; alpha/tint-based ablations; hatching for grayscale print; `fill_between` for uncertainty; dpi 300 (600 for dense bars); `svg.fonttype='none'`; multi-panel consistency.

## Additions (headline)

Axis labels with units and ↓/↑ · one method→color map per paper · schematic tones (light fill + same-hue edge) · ❄ frozen / 🔥 trainable · dashed = feedback/inference-only · teaser = prior ✗ vs ours ✓ with score boxes · real data thumbnails · direct labels on scatter · spell-check before export.

## Quick start

```python
import sys; sys.path.insert(0, "smilab-style")
import smilab_style as sm
sm.apply_publication_style(sm.FigureStyle())            # base API, SMILab defaults
C = sm.method_colors(METHODS, ours="Ours", variants=["Ours w/o X"])
sm.bar_compare(ax, METHODS, means, C, errs=sd, pvalues=p, ylabel=sm.label("HD95", "mm", "down"))
sm.finalize_figure(fig, "figures/result")                 # -> .pdf + .png
```
