# `smilab_style.py` API

`smilab_style.py` implements the **base contract** from [scientific-figure-making/references/api.md](../../scientific-figure-making/references/api.md) with the SMILab overrides (O1–O3 in [design-rules.md](design-rules.md)), plus helpers for the additions.
Import: `sys.path.insert(0, "smilab-style"); import smilab_style as sm`. Examples: [examples/demo.py](../examples/demo.py).

## Base contract (same names and meaning as the base)

| Name | SMILab behaviour |
|---|---|
| `PALETTE`, `DEFAULT_COLORS` | Identical to the base |
| `FigureStyle(font_size=8, axes_linewidth=0.8, use_tex=False, mode="paper", font_family=Times…)` | O1/O2 defaults; `mode="teaser"` switches to the base sans stack |
| `apply_publication_style(style=None)` | Base rcParams (spines off, svg text, dpi 300) + O1 fonts + O2 sizes + O3 framed legend / light y-grid |
| `create_subplots(nrows, ncols, figsize=None)` | Returns `(fig, axes_1d)`; default `figsize` is print width (`COLUMN=3.3`, `DOUBLE=7.0` in) |
| `finalize_figure(fig, out_path, formats=None, dpi=300, close=False, pad=0.03)` | Default formats pdf + png |

Shorthands: `apply_style(mode, font_size)`, `save(fig, path)`.

## Colors
- `OURS = PALETTE["blue_main"]` (inherited rule); `OURS_VARIANTS` = lighter blues for ablations.
- `METHOD_CYCLE` — pastel baselines from the base family (as used in `figure_MACL`).
- `LINE_CYCLE`, `OURS_LINE` — saturated versions for thin lines/markers.
- `method_colors(methods, ours=..., variants=[...])` — build once per paper (A1).
- `TONES[name] -> (fill, edge)` — schematic tonal pairs (A5). `darken(c)`, `text_color_on(c)`.

## Text (additions)
- `label(name, unit=None, better="up"|"down")` → `HD95 [mm] ↓` (A2).
- `stars(p)`; `panel_label(ax, "(a)")`; `square_legend(ax_or_fig, names, colors, ours=...)`; `bold_ours_ticklabels(ax, ours)`.

## Plots
- `bar_compare(ax, names, means, colors, errs=None, pvalues=None, fmt, ylim, ylabel, hatches=None)` — O3 bars. Set `ylim` here (in-bar values are placed relative to it).
- `hbar_ablation(ax, rows, values, errs=None, full_idx=0, colors=None, best="min", pvalues=None, xlim, xlabel, show_rows=True, gaps=())` — A4. No `sharey` (the helper inverts the axis).
- `line_compare(ax, x, series, colors, ours=None, markers=None)` — A3 lines.
- `scatter_direct(ax, points, colors, markers=None, sizes=None, labels=None, offsets=None, ours=None)` — A3 direct labels.
- `badge_ticklabels(ax, labels, highlight=[i])`, `tinted_axes(ax)` — shared schematic/plot vocabulary.
- `tone_box(ax, xy, w, h, tone, text=None, rotation=0, dashed=False)` — A5 block.

## Checklist before export
- [ ] base checklist (palette family, spines, y-limits, dpi)
- [ ] one method→color map for the paper; proposed = blue, last, bold
- [ ] axis labels with units and ↓/↑
- [ ] figure width = column width; printed text ≥ 6 pt
- [ ] notation identical to the paper; spell-checked
