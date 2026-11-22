"""smilab-style: SMILab layer on top of the scientific-figure-making base skill.

Implements the base contract (scientific-figure-making/references/api.md:
PALETTE, DEFAULT_COLORS, FigureStyle, apply_publication_style, create_subplots,
finalize_figure) and applies ONLY the overrides decided for SMILab:

  override 1  fonts: Times + STIX math for paper figures (base: Helvetica/Arial)
  override 2  size: draw at print size, 7-9 pt (base: 45x12 in canvas, 16-24 pt)
  override 3  bars: values inside bars (vertical), same-hue thin edges, framed
              legend with square patches, significance stars (base: values above,
              black thick edges, frameless legend)

Everything else is inherited from the base: blue #0F4D92 = proposed method,
blue/green/red/neutral palette family, top/right spines off, dpi 300 (600 for
dense bars), svg.fonttype none, hatching for print safety, tightened y-limits.
Additions (schematic tones, icons, direction arrows, ...) are new helpers below.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Patch

# ---------------------------------------------------------------------------
# Inherited from the base (unchanged)
# ---------------------------------------------------------------------------

PALETTE = {
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "green_1": "#DDF3DE", "green_2": "#AADCA9", "green_3": "#8BCF8B",
    "red_1": "#F6CFCB", "red_2": "#E9A6A1", "red_strong": "#B64342",
    "neutral": "#CFCECE", "highlight": "#FFD700",
    "teal": "#42949E", "violet": "#9A4D8E",
}
DEFAULT_COLORS = [PALETTE[k] for k in ("blue_main", "green_3", "red_strong", "teal", "violet",
                                       "neutral")]

OURS = PALETTE["blue_main"]  # base rule: blue = proposed / key method

# Pastel baseline colors used by the base author's own figures (figure_MACL).
# Blue hues are reserved for the proposed method and its variants.
METHOD_CYCLE: list[str] = [
    "#DADADA",  # neutral gray
    "#C4E8BD",  # green
    "#F3CEC7",  # red / pink
    "#DFC2E0",  # violet
    "#B5DFE2",  # teal
    "#F5E1B0",  # sand (added for >5 baselines)
    "#E9A6A1",  # red_2
    "#AADCA9",  # green_2
]
# Proposed-method variants (ablations): lighter blues, as in figure_MACL.
OURS_VARIANTS: list[str] = ["#B7CAE2", "#6F94BE", "#3775BA"]

# Saturated variants for thin marks (lines / markers), still within the base family.
LINE_CYCLE: list[str] = ["#767676", "#5BAF5B", "#B64342", "#9A4D8E", "#42949E", "#C68A1D"]
OURS_LINE = OURS

# ---------------------------------------------------------------------------
# Additions
# ---------------------------------------------------------------------------

# Tonal pairs for schematic blocks and panel backgrounds: (light fill, edge).
# Color = concept (A2C, MLLM, ...); the proposed output/emphasis uses "blue".
TONES: dict[str, tuple[str, str]] = {
    "blue": ("#E3ECF7", "#3775BA"),
    "green": ("#E8F5E8", "#6DBA6D"),
    "red": ("#FBE6E4", "#D27C76"),
    "purple": ("#EFE4F0", "#9A4D8E"),
    "teal": ("#E2F1F2", "#42949E"),
    "yellow": ("#FFF6DA", "#D9AE3A"),
    "gray": ("#F2F2F2", "#9A9A9A"),
}

GRAY_TEXT = "#555555"
GRID = "#E6E6E6"
ARROW = "#666666"
SIG_TEXT = "#333333"
GOOD = "#4CAF50"  # check mark
BAD = "#D9443A"  # cross mark


def darken(color: str, factor: float = 0.75) -> tuple[float, float, float]:
    """Same hue, darker: edges of pastel fills (override 3)."""
    r, g, b = to_rgb(color)
    return (r * factor, g * factor, b * factor)


def text_color_on(color: str) -> str:
    """Black on light fills, white on dark fills (e.g. values inside blue_main bars)."""
    r, g, b = to_rgb(color)
    return "white" if 0.299 * r + 0.587 * g + 0.114 * b < 0.5 else "#222222"


def method_colors(methods: Sequence[str], ours: str | Iterable[str] | None = None,
                  variants: Iterable[str] = (), cycle: Sequence[str] = METHOD_CYCLE,
                  ours_color: str = OURS) -> dict[str, str]:
    """Fixed method -> color map. Build it ONCE per paper and reuse it in every figure.
    `ours` gets blue_main; `variants` (ablations of ours) get lighter blues."""
    ours_set = {ours} if isinstance(ours, str) else set(ours or [])
    var = list(variants)
    out, i = {}, 0
    for m in methods:
        if m in ours_set:
            out[m] = ours_color
        elif m in var:
            out[m] = OURS_VARIANTS[var.index(m) % len(OURS_VARIANTS)]
        else:
            out[m] = cycle[i % len(cycle)]
            i += 1
    return out


# ---------------------------------------------------------------------------
# Style (base contract + overrides 1-3)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class FigureStyle:
    """Base FigureStyle with SMILab defaults (print size, Times)."""
    font_size: float = 8.0          # override 2: printed size (base: 16-24)
    axes_linewidth: float = 0.8     # override 2 (base: 2-3, for a shrunk canvas)
    use_tex: bool = False
    mode: str = "paper"             # override 1: "paper" = Times+STIX, "teaser" = sans
    font_family: tuple[str, ...] = ("Times New Roman", "Times", "STIXGeneral", "DejaVu Serif")


def apply_publication_style(style: FigureStyle | None = None) -> None:
    style = style or FigureStyle()
    paper = style.mode == "paper"
    mpl.rcParams.update({
        # inherited
        "axes.spines.top": False,
        "axes.spines.right": False,
        "svg.fonttype": "none",
        "savefig.dpi": 300,
        "text.usetex": style.use_tex,
        # override 1: fonts
        "font.family": "serif" if paper else "sans-serif",
        "font.serif": list(style.font_family),
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],  # base stack
        "mathtext.fontset": "stix" if paper else "stixsans",
        # override 2: print-size typography and strokes
        "font.size": style.font_size,
        "axes.titlesize": style.font_size + 1,
        "axes.labelsize": style.font_size + 1,
        "xtick.labelsize": style.font_size,
        "ytick.labelsize": style.font_size,
        "legend.fontsize": style.font_size,
        "axes.linewidth": style.axes_linewidth,
        "axes.edgecolor": "#333333",
        "xtick.major.width": style.axes_linewidth,
        "ytick.major.width": style.axes_linewidth,
        "xtick.major.size": 3,
        "ytick.major.size": 3,
        "lines.linewidth": 1.8,
        "errorbar.capsize": 2.5,
        # override 3: framed legend with square patches, light y-grid
        "legend.frameon": True,
        "legend.edgecolor": "#BBBBBB",
        "legend.fancybox": False,
        "legend.framealpha": 1.0,
        "legend.handlelength": 1.2,
        "legend.handleheight": 0.8,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        # export
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.03,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


def apply_style(mode: str = "paper", font_size: float = 8.0) -> None:
    """Shorthand: apply_publication_style(FigureStyle(mode=mode, font_size=font_size))."""
    if mode not in ("paper", "teaser"):
        raise ValueError("mode must be 'paper' or 'teaser'")
    apply_publication_style(FigureStyle(font_size=font_size, mode=mode))


COLUMN = 3.3  # in, single column (IEEE/ICASSP ~3.39, NeurIPS full width ~5.5)
DOUBLE = 7.0  # in, double column


def create_subplots(nrows: int = 1, ncols: int = 1, figsize=None, **kwargs):
    """Base contract; figsize defaults to print width (override 2)."""
    figsize = figsize or (DOUBLE if ncols > 2 else COLUMN, 1.9 * nrows)
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, squeeze=False, **kwargs)
    return fig, axes.ravel()


def finalize_figure(fig, out_path: str | Path, formats: Sequence[str] | None = None,
                    dpi: int = 300, close: bool = False, pad: float = 0.03, **kwargs) -> list[Path]:
    """Base contract. Default formats: pdf (paper) + png (preview)."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if formats is None:
        formats = [out_path.suffix[1:]] if out_path.suffix else ["pdf", "png"]
    paths = []
    for f in formats:
        p = out_path.with_suffix("." + f)
        fig.savefig(p, dpi=dpi, pad_inches=pad, **kwargs)
        paths.append(p)
    if close:
        plt.close(fig)
    return paths


def save(fig, path: str | Path, formats: Sequence[str] = ("pdf", "png")) -> list[Path]:
    return finalize_figure(fig, path, formats=formats)


# ---------------------------------------------------------------------------
# Text helpers (additions)
# ---------------------------------------------------------------------------

def label(name: str, unit: str | None = None, better: str | None = None) -> str:
    """'HD95', 'mm', 'down' -> 'HD95 [mm] ↓'."""
    s = name + (f" [{unit}]" if unit else "")
    if better in ("down", "lower"):
        s += r" $\downarrow$"
    elif better in ("up", "higher"):
        s += r" $\uparrow$"
    return s


def stars(p: float | None) -> str:
    if p is None or np.isnan(p):
        return ""
    return "***" if p < 1e-3 else "**" if p < 1e-2 else "*" if p < 5e-2 else ""


def panel_label(ax, text: str, x: float = -0.12, y: float = 1.04, **kw) -> None:
    """Bold '(a)' at the top-left of an axes."""
    ax.text(x, y, text, transform=ax.transAxes, fontweight="bold",
            fontsize=mpl.rcParams["font.size"] + 2, ha="left", va="bottom", **kw)


def square_legend(target, names: Sequence[str], colors: Mapping[str, str],
                  ours: str | Iterable[str] | None = None, **kw):
    """Framed legend with square patches; the proposed method is bold (override 3)."""
    ours_set = {ours} if isinstance(ours, str) else set(ours or [])
    handles = [Patch(facecolor=colors[n], edgecolor=darken(colors[n], 0.8), linewidth=0.6)
               for n in names]
    leg = target.legend(handles, names, **kw)
    for t in leg.get_texts():
        if t.get_text() in ours_set:
            t.set_fontweight("bold")
    return leg


def bold_ours_ticklabels(ax, ours: str | Iterable[str], axis: str = "x") -> None:
    ours_set = {ours} if isinstance(ours, str) else set(ours)
    labels = ax.get_xticklabels() if axis == "x" else ax.get_yticklabels()
    for t in labels:
        if t.get_text() in ours_set:
            t.set_fontweight("bold")


# ---------------------------------------------------------------------------
# Plot helpers
# ---------------------------------------------------------------------------

def bar_compare(ax, names: Sequence[str], means: Sequence[float], colors: Mapping[str, str],
                errs: Sequence[float] | None = None, pvalues: Sequence[float | None] | None = None,
                fmt: str = "{:.1f}", ylim: tuple[float, float] | None = None,
                ylabel: str | None = None, show_xticks: bool = False, width: float = 0.78,
                hatches: Mapping[str, str] | None = None):
    """Override 3: one bar per method, value written vertically inside the bar (white
    on dark fills), significance stars above. Inherited: hidden x ticks (legend
    identifies methods), tightened y-limits, optional hatches for grayscale print.
    Put the proposed method LAST."""
    means = np.asarray(means, float)
    x = np.arange(len(names))
    fc = [colors[n] for n in names]
    ec = [darken(c, 0.85) for c in fc]
    bars = ax.bar(x, means, width=width, color=fc, edgecolor=ec, linewidth=0.6, zorder=2)
    if hatches:
        for b, n in zip(bars, names):
            if n in hatches:
                b.set_hatch(hatches[n])
    if errs is not None:
        ax.errorbar(x, means, yerr=errs, fmt="none", ecolor="#333333", elinewidth=0.8,
                    capsize=2.5, zorder=3)
    if ylim is not None:
        ax.set_ylim(*ylim)
    lo, hi = ax.get_ylim()
    span = hi - lo
    fs = mpl.rcParams["font.size"] + 1
    axes_pts = ax.get_position().height * ax.figure.get_figheight() * 72
    top = means + (np.asarray(errs, float) if errs is not None else 0)
    above = np.zeros(len(x))  # extra height used by labels placed above short bars
    for i, (xi, m, c) in enumerate(zip(x, means, fc)):
        txt = fmt.format(m)
        need = (len(txt) * 0.55 * fs + 3) / axes_pts * span  # text length in data units
        if m - lo >= need + 0.03 * span:
            ax.text(xi, lo + 0.03 * span, txt, rotation=90, ha="center", va="bottom",
                    color=text_color_on(c), zorder=4, fontsize=fs)
        else:  # bar too short: write the value above it
            ax.text(xi, top[i] + 0.01 * span, txt, rotation=90, ha="center", va="bottom",
                    color="#222222", zorder=4, fontsize=fs)
            above[i] = need + 0.02 * span
    if pvalues is not None:
        for xi, t, extra, p in zip(x, top, above, pvalues):
            s = stars(p)
            if s:
                ax.text(xi, t + extra + 0.005 * span, s, ha="center", va="bottom",
                        color=SIG_TEXT, fontsize=mpl.rcParams["font.size"], fontweight="bold")
    ax.set_xticks(x)
    if show_xticks:
        ax.set_xticklabels(names, rotation=30, ha="right")
    else:
        ax.set_xticklabels([])
        ax.tick_params(axis="x", length=0)
    if ylabel:
        ax.set_ylabel(ylabel)
    return bars


def hbar_ablation(ax, rows: Sequence[str], values: Sequence[float], errs: Sequence[float] | None = None,
                  full_idx: int = 0, colors: Sequence[str] | None = None,
                  best: str = "min", pvalues: Sequence[float | None] | None = None,
                  fmt: str = "{:.1f}", xlim: tuple[float, float] | None = None,
                  xlabel: str | None = None, show_rows: bool = True, gaps: Sequence[int] = ()):
    """Ablation h-bars. Inherited: full model = blue_main, ablated variants = lighter
    tints of the same blue (base "alpha-based ablation"). Added: best value bold,
    group headers (`gaps` inserts an empty row before those indices), stars."""
    values = np.asarray(values, float)
    y, pos = [], 0.0
    for i in range(len(rows)):
        if i in gaps:
            pos += 1.0
        y.append(pos)
        pos += 1.0
    y = np.asarray(y)
    if colors is None:
        colors = [OURS if i == full_idx else OURS_VARIANTS[0] for i in range(len(rows))]
    ax.barh(y, values, height=0.72, color=colors, edgecolor=[darken(c, 0.8) for c in colors],
            linewidth=0.6, zorder=2)
    if errs is not None:
        ax.errorbar(values, y, xerr=errs, fmt="none", ecolor="#222222", elinewidth=0.8,
                    capsize=2.5, zorder=3)
    if xlim is not None:
        ax.set_xlim(*xlim)
    lo, hi = ax.get_xlim()
    best_i = int(np.argmin(values) if best == "min" else np.argmax(values))
    for i, (yi, v, c) in enumerate(zip(y, values, colors)):
        ax.text(lo + 0.02 * (hi - lo), yi, fmt.format(v), va="center", ha="left",
                fontweight="bold" if i == best_i else "normal", color=text_color_on(c),
                fontsize=mpl.rcParams["font.size"] + 1, zorder=4)
    if pvalues is not None:
        for yi, p in zip(y, pvalues):
            s = stars(p)
            if s:
                ax.text(hi, yi, "\n".join(s), ha="right", va="center", linespacing=0.7,
                        fontweight="bold", color=SIG_TEXT)
    ax.set_yticks(y)
    ax.set_yticklabels(rows if show_rows else [])
    if not show_rows:
        ax.tick_params(axis="y", length=0)
    ax.invert_yaxis()
    ax.grid(axis="x", color=GRID)
    ax.grid(axis="y", visible=False)
    for s in ("left", "top", "right"):
        ax.spines[s].set_visible(False)
    if xlabel:
        ax.set_xlabel(xlabel)
    return y


MARKERS = ["D", "^", "s", "v", "P", "X", "h"]


def line_compare(ax, x: Sequence, series: Mapping[str, Sequence[float]], colors: Mapping[str, str],
                 ours: str | None = None, markers: Mapping[str, str] | None = None,
                 lw: float = 1.8, ms: float = 5.0):
    """Inherited: 2-4 main curves, width 2-3 (scaled to print). Added: color AND marker
    differ per method; ours is a circle drawn on top."""
    xs = np.arange(len(x)) if isinstance(x[0], str) else np.asarray(x)
    k = 0
    for name, ys in series.items():
        if name == ours:
            mk, z, w = "o", 5, lw * 1.25
        else:
            mk = (markers or {}).get(name, MARKERS[k % len(MARKERS)])
            k += 1
            z, w = 3, lw
        ax.plot(xs, ys, color=colors[name], marker=mk, lw=w, ms=ms, label=name, zorder=z,
                markeredgecolor="white" if name == ours else colors[name], markeredgewidth=0.8)
    if isinstance(x[0], str):
        ax.set_xticks(xs)
        ax.set_xticklabels(x)
    ax.grid(axis="both", color=GRID)


def scatter_direct(ax, points: Mapping[str, tuple[float, float]], colors: Mapping[str, str],
                   markers: Mapping[str, str] | None = None, sizes: Mapping[str, float] | None = None,
                   labels: Mapping[str, str] | None = None, offsets: Mapping[str, tuple[float, float]] | None = None,
                   ours: str | None = None, s: float = 120, alpha: float = 0.75):
    """Added: each point labelled directly in its own color (no legend). Inherited:
    lowered alpha for dense scenes. `offsets` in points."""
    for name, (px, py) in points.items():
        c = colors[name]
        ax.scatter(px, py, s=(sizes or {}).get(name, s), marker=(markers or {}).get(name, "o"),
                   color=c, alpha=alpha, edgecolor=darken(c, 0.6), linewidth=1.0, zorder=3)
        dx, dy = (offsets or {}).get(name, (10, 0))
        ax.annotate((labels or {}).get(name, name), (px, py), xytext=(dx, dy),
                    textcoords="offset points", va="center",
                    ha="left" if dx >= 0 else "right", color=darken(c, 0.8),
                    fontweight="bold" if name == ours else "normal")
    ax.grid(axis="both", color=GRID)


def badge_ticklabels(ax, labels: Sequence[str], highlight: Iterable[int] = (),
                     color: str = "#7F7F7F", highlight_color: str = PALETTE["red_strong"],
                     y: float = -0.09, size: float | None = None) -> None:
    """Added: x tick labels as rounded badges shared with a schematic (DISCODE-style)."""
    hl = set(highlight)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels([])
    ax.tick_params(axis="x", length=0)
    trans = mpl.transforms.blended_transform_factory(ax.transData, ax.transAxes)
    for i, t in enumerate(labels):
        ax.text(i, y, t, transform=trans, ha="center", va="center", color="white",
                fontweight="bold", fontsize=size or mpl.rcParams["font.size"] + 2,
                fontfamily="sans-serif",
                bbox=dict(boxstyle="round,pad=0.22,rounding_size=0.25",
                          fc=highlight_color if i in hl else color, ec="none"))


def tinted_axes(ax, color: str = "#F5F5F5") -> None:
    """Added: light gray plotting area with dashed y grid."""
    ax.set_facecolor(color)
    ax.grid(axis="y", linestyle="--", color="#AAAAAA", linewidth=0.7)
    for s in ax.spines.values():
        s.set_visible(True)
        s.set_color("#333333")


def tone_box(ax, xy, w, h, tone: str = "gray", text: str | None = None, rotation: float = 0,
             radius: float = 0.02, lw: float = 1.0, dashed: bool = False, **text_kw):
    """Added: schematic block, light fill + darker same-hue edge (TONES)."""
    fill, edge = TONES[tone]
    box = FancyBboxPatch(xy, w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
                         fc=fill, ec=edge, lw=lw, ls="--" if dashed else "-", zorder=2)
    ax.add_patch(box)
    if text:
        ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center",
                rotation=rotation, zorder=3, **text_kw)
    return box
