# `smilab_style.py` API

Import: `sys.path.insert(0, "smilab-style"); import smilab_style as sm`. Examples: [examples/demo.py](../examples/demo.py).

## Constants
- `TONES[name] -> (fill, edge)` — blue, yellow, purple, orange, green, red, gray.
- `METHOD_CYCLE` — pastel baseline colors for bars; `OURS = "#D9837F"`.
- `LINE_CYCLE` / `OURS_LINE = "#3F84AA"` — saturated variants for line plots.
- `GRID`, `ARROW`, `GOOD`, `BAD`, `GRAY_TEXT`.

## Style
- `apply_style(mode="paper"|"teaser", font_size=9)` — rcParams: fonts (Times+STIX / Helvetica), no top/right spines, light y-grid, framed square legend, TrueType embedding, 300 dpi tight save. Size figures at real print width (single column ≈ 3.3 in, double ≈ 7.0 in) so `font_size` is the printed size.
- `method_colors(methods, ours, cycle=METHOD_CYCLE, ours_color=OURS) -> dict` — build once per paper.
- `darken(color, factor=0.75)` — same-hue darker edge.

## Text
- `label(name, unit=None, better=None)` — `label("HD95", "mm", "down")` → `HD95 [mm] ↓`.
- `stars(p)` — `'***' / '**' / '*' / ''`.
- `panel_label(ax, "(a)", x=-0.12, y=1.04)` — bold, top-left.
- `square_legend(ax_or_fig, names, colors, ours=..., **legend_kw)` — square patches, ours bold.
- `bold_ours_ticklabels(ax, ours, axis="x")`.

## Plots
- `bar_compare(ax, names, means, colors, errs=None, pvalues=None, fmt="{:.1f}", ylim=None, ylabel=None, show_xticks=False)` — in-bar vertical values, stars above. Set `ylim` here (values are placed relative to it).
- `hbar_ablation(ax, rows, values, errs=None, full_idx=0, best="min", pvalues=None, xlim=None, xlabel=None, show_rows=True, gaps=())` — returns row y-positions; `gaps` inserts blank rows for group headers (write headers with `ax.text` at `y[i]-1`). Do **not** use `sharey` (the helper inverts the axis).
- `line_compare(ax, x, series: dict, colors, ours=None, markers=None)` — color+marker per method; string `x` becomes categorical.
- `scatter_direct(ax, points: dict[name -> (x, y)], colors, markers=None, sizes=None, labels=None, offsets=None, ours=None)` — direct colored labels; tune `offsets` (points) to avoid overlaps.
- `badge_ticklabels(ax, labels, highlight=[i])` + `tinted_axes(ax)` — DISCODE-style.
- `tone_box(ax, xy, w, h, tone, text=None, rotation=0, dashed=False)` — schematic block in matplotlib.
- `save(fig, path, formats=("pdf", "png"))`.

## Checklist before export
- [ ] method colors from the paper's single map; ours last and bold
- [ ] axis labels have units and ↓/↑
- [ ] printed text ≥ 6 pt; figure width = column width
- [ ] notation identical to the paper; spell-checked
