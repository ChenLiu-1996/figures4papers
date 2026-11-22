"""smilab-style: matplotlib helpers for SMILab publication figures.

Implements the plot rules in references/design-rules.md:
  * pastel fills with a darker same-hue edge, few hues, fixed method->color map
  * the proposed method is last, red-pink, and bold in legends
  * axis labels carry units and a "better" arrow (↓ / ↑)
  * bar values are written vertically inside the bar; significance stars above
  * light grid, no top/right spines, square legend patches

Usage:
    import smilab_style as sm
    sm.apply_style()                 # paper mode: Times + STIX math
    colors = sm.method_colors(["LCMV", "sLORETA", "Ours"], ours="Ours")
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Patch

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------

# Tonal pairs for schematic blocks and panel backgrounds: (light fill, edge).
TONES: dict[str, tuple[str, str]] = {
    "blue": ("#E8EEFA", "#7A96D6"),
    "yellow": ("#FFF6DA", "#E2BE55"),
    "purple": ("#EDE3F3", "#A77DB8"),
    "orange": ("#F9E3CC", "#E8A36A"),
    "green": ("#E3F1E1", "#7FB77A"),
    "red": ("#FBE4E1", "#E08A82"),
    "gray": ("#F2F2F2", "#9A9A9A"),
}

# Method colors for data plots (pastel, CANDLE-like). Baselines first; OURS is reserved.
METHOD_CYCLE: list[str] = [
    "#A8968A",  # brown
    "#93C08E",  # green
    "#8FA7D6",  # blue
    "#EDD98A",  # yellow
    "#86C1BE",  # teal
    "#B29CC4",  # purple
    "#EFB070",  # orange
    "#C9C9C9",  # gray
]
OURS = "#D9837F"  # red-pink, only for the proposed method

# Saturated variants for line plots, where thin marks need more chroma (ELSA-like).
LINE_CYCLE: list[str] = ["#B5462B", "#E5962F", "#8E3F6E", "#3E8E5E", "#6A5AA8", "#7A7A7A"]
OURS_LINE = "#3F84AA"

GRAY_TEXT = "#555555"
GRID = "#E6E6E6"
ARROW = "#666666"
SIG_TEXT = "#333333"
GOOD = "#4CAF50"  # ✓
BAD = "#D9443A"  # ✗


def darken(color: str, factor: float = 0.75) -> tuple[float, float, float]:
    """Same hue, darker: used for edges of pastel fills."""
    r, g, b = to_rgb(color)
    return (r * factor, g * factor, b * factor)


def method_colors(methods: Sequence[str], ours: str | Iterable[str] | None = None,
                  cycle: Sequence[str] = METHOD_CYCLE, ours_color: str = OURS) -> dict[str, str]:
    """Fixed method -> color map. Build it ONCE per paper and reuse it in every figure."""
    ours_set = {ours} if isinstance(ours, str) else set(ours or [])
    out, i = {}, 0
    for m in methods:
        if m in ours_set:
            out[m] = ours_color
        else:
            out[m] = cycle[i % len(cycle)]
            i += 1
    return out


# ---------------------------------------------------------------------------
# Global style
# ---------------------------------------------------------------------------

def apply_style(mode: str = "paper", font_size: float = 9.0) -> None:
    """mode='paper': Times + STIX math (matches LaTeX body).
    mode='teaser': Helvetica/Arial (schematic-like figures, slides)."""
    if mode == "paper":
        family, serif = "serif", ["Times New Roman", "Times", "STIXGeneral", "DejaVu Serif"]
        mathtext = "stix"
    elif mode == "teaser":
        family, serif = "sans-serif", ["Times New Roman"]
        mathtext = "stixsans"
    else:
        raise ValueError("mode must be 'paper' or 'teaser'")
    mpl.rcParams.update({
        "font.family": family,
        "font.serif": serif,
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "mathtext.fontset": mathtext,
        "font.size": font_size,
        "axes.titlesize": font_size + 1,
        "axes.labelsize": font_size + 1,
        "xtick.labelsize": font_size,
        "ytick.labelsize": font_size,
        "legend.fontsize": font_size,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": "#333333",
        "axes.linewidth": 0.8,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "xtick.major.size": 3,
        "ytick.major.size": 3,
        "legend.frameon": True,
        "legend.edgecolor": "#BBBBBB",
        "legend.fancybox": False,
        "legend.framealpha": 1.0,
        "legend.handlelength": 1.2,
        "legend.handleheight": 0.8,
        "lines.linewidth": 2.0,
        "errorbar.capsize": 2.5,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.03,
        "pdf.fonttype": 42,  # embed TrueType: editable text in Illustrator
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    })


# ---------------------------------------------------------------------------
# Small text helpers
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
    """Legend with square patches; the proposed method is bold. target: Axes or Figure."""
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
                ylabel: str | None = None, show_xticks: bool = False, width: float = 0.78):
    """CANDLE-style bars: one bar per method, value written vertically inside the bar,
    significance stars above the error bar. Put the proposed method LAST in `names`."""
    means = np.asarray(means, float)
    x = np.arange(len(names))
    fc = [colors[n] for n in names]
    ec = [darken(c, 0.85) for c in fc]
    bars = ax.bar(x, means, width=width, color=fc, edgecolor=ec, linewidth=0.6, zorder=2)
    if errs is not None:
        ax.errorbar(x, means, yerr=errs, fmt="none", ecolor="#333333", elinewidth=0.8,
                    capsize=2.5, zorder=3)
    if ylim is not None:
        ax.set_ylim(*ylim)
    lo, hi = ax.get_ylim()
    span = hi - lo
    for xi, m, n in zip(x, means, names):
        ax.text(xi, lo + 0.03 * span, fmt.format(m), rotation=90, ha="center", va="bottom",
                color="#222222", zorder=4, fontsize=mpl.rcParams["font.size"] + 1)
    if pvalues is not None:
        top = means + (np.asarray(errs, float) if errs is not None else 0)
        for xi, t, p in zip(x, top, pvalues):
            s = stars(p)
            if s:
                ax.text(xi, t + 0.005 * span, s, ha="center", va="bottom", color=SIG_TEXT,
                        fontsize=mpl.rcParams["font.size"], fontweight="bold")
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
                  full_idx: int = 0, full_color: str = OURS, base_color: str = "#DCDDE0",
                  best: str = "min", pvalues: Sequence[float | None] | None = None,
                  fmt: str = "{:.1f}", xlim: tuple[float, float] | None = None,
                  xlabel: str | None = None, show_rows: bool = True, gaps: Sequence[int] = ()):
    """CANDLE-style ablation: full model colored, ablations gray, best value bold,
    value written inside the bar near its left end. `gaps` = row indices before which
    an empty row (for a group header) is inserted."""
    values = np.asarray(values, float)
    y, pos = [], 0.0
    for i in range(len(rows)):
        if i in gaps:
            pos += 1.0
        y.append(pos)
        pos += 1.0
    y = np.asarray(y)
    colors = [full_color if i == full_idx else base_color for i in range(len(rows))]
    ax.barh(y, values, height=0.72, color=colors, edgecolor=[darken(c, 0.7) for c in colors],
            linewidth=0.6, zorder=2)
    if errs is not None:
        ax.errorbar(values, y, xerr=errs, fmt="none", ecolor="#222222", elinewidth=0.8,
                    capsize=2.5, zorder=3)
    if xlim is not None:
        ax.set_xlim(*xlim)
    lo, hi = ax.get_xlim()
    best_i = int(np.argmin(values) if best == "min" else np.argmax(values))
    for i, (yi, v) in enumerate(zip(y, values)):
        ax.text(lo + 0.02 * (hi - lo), yi, fmt.format(v), va="center", ha="left",
                fontweight="bold" if i == best_i else "normal",
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
                 lw: float = 2.4, ms: float = 7.0):
    """ELSA-style lines: color AND marker differ per method; ours is a circle drawn on top."""
    xs = np.arange(len(x)) if isinstance(x[0], str) else np.asarray(x)
    k = 0
    for name, ys in series.items():
        if name == ours:
            mk, z = "o", 5
        else:
            mk = (markers or {}).get(name, MARKERS[k % len(MARKERS)])
            k += 1
            z = 3
        ax.plot(xs, ys, color=colors[name], marker=mk, lw=lw, ms=ms, label=name, zorder=z,
                markeredgecolor="white" if name == ours else colors[name], markeredgewidth=0.8)
    if isinstance(x[0], str):
        ax.set_xticks(xs)
        ax.set_xticklabels(x)
    ax.grid(axis="both", color=GRID)


def scatter_direct(ax, points: Mapping[str, tuple[float, float]], colors: Mapping[str, str],
                   markers: Mapping[str, str] | None = None, sizes: Mapping[str, float] | None = None,
                   labels: Mapping[str, str] | None = None, offsets: Mapping[str, tuple[float, float]] | None = None,
                   ours: str | None = None, s: float = 180, alpha: float = 0.75):
    """ABMamba-style scatter: semi-transparent markers with a dark edge, and each point
    labelled directly in its own color (no legend). `offsets` in points."""
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
                     color: str = "#7F7F7F", highlight_color: str = "#E0342B",
                     y: float = -0.09, size: float | None = None) -> None:
    """DISCODE-style x tick labels drawn as rounded badges (white bold text)."""
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
    """Light gray plotting area with dashed y grid (DISCODE-style)."""
    ax.set_facecolor(color)
    ax.grid(axis="y", linestyle="--", color="#AAAAAA", linewidth=0.7)
    for s in ax.spines.values():
        s.set_visible(True)
        s.set_color("#333333")


def tone_box(ax, xy, w, h, tone: str = "gray", text: str | None = None, rotation: float = 0,
             radius: float = 0.02, lw: float = 1.0, dashed: bool = False, **text_kw):
    """Schematic block: light fill + darker same-hue edge (TONES). Axes-data coordinates."""
    fill, edge = TONES[tone]
    box = FancyBboxPatch(xy, w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
                         fc=fill, ec=edge, lw=lw, ls="--" if dashed else "-", zorder=2)
    ax.add_patch(box)
    if text:
        ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center",
                rotation=rotation, zorder=3, **text_kw)
    return box


def save(fig, path: str | Path, formats: Sequence[str] = ("pdf", "png")) -> list[Path]:
    """Save to every format (vector PDF for the paper, PNG for preview)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    out = []
    for f in formats:
        p = path.with_suffix("." + f)
        fig.savefig(p)
        out.append(p)
    return out
