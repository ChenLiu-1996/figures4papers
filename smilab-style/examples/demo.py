"""smilab-style demo figures. ALL NUMBERS ARE DUMMY DATA (layout check only).

Run:  python smilab-style/examples/demo.py
Out:  smilab-style/examples/figures/*.{pdf,png}
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import smilab_style as sm  # noqa: E402

OUT = HERE / "figures"
METHODS = ["LCMV", "sLORETA", "wMNE", "eLORETA", "ConvDip", "DeepSIF", "GBF", "Ours"]
COLORS = sm.method_colors(METHODS, ours="Ours")  # one map, reused by every figure


def fig_bars():
    """Ref #14/#16: bars with in-bar values, stars, direction arrows, shared legend."""
    sm.apply_style("paper", font_size=9)
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.3), gridspec_kw={"width_ratios": [1, 1, 1.05]})
    hd = [57.9, 66.1, 70.7, 69.7, 41.0, 45.1, 65.3, 37.3]
    dice = [0.22, 0.24, 0.21, 0.19, 0.33, 0.33, 0.26, 0.48]
    p = [1e-4] * 7 + [None]
    sm.bar_compare(axes[0], METHODS, hd, COLORS, errs=[0.8] * 8, pvalues=p, ylim=(20, 80),
                   ylabel=sm.label("HD95", "mm", "down"))
    sm.bar_compare(axes[1], METHODS, dice, COLORS, errs=[0.006] * 8, pvalues=p, fmt="{:.2f}",
                   ylim=(0.1, 0.5), ylabel=sm.label("Dice score", better="up"))
    thr = np.linspace(0.1, 0.9, 9)
    ax = axes[2]
    for i, m in enumerate(METHODS):
        scale = 0.83 if m == "Ours" else 0.45 + 0.03 * i
        y = scale * np.clip(1 - (thr - 0.1) / (0.8 if m == "Ours" else 0.4 + 0.03 * i), 0, 1) ** 1.6
        ax.plot(thr, y, marker="o", ms=3.5, lw=1.6 if m != "Ours" else 2.2, color=COLORS[m],
                zorder=5 if m == "Ours" else 3)
        if m in ("Ours", "ConvDip"):
            ax.fill_between(thr, y * 0.85, np.minimum(y * 1.15, 1), color=COLORS[m], alpha=0.2, lw=0)
    ax.set_xlabel("IoU threshold")
    ax.set_ylabel(sm.label("F1 score", better="up"))
    ax.set_ylim(0, 1)
    ax.grid(axis="both", color=sm.GRID)
    sm.panel_label(axes[0], "(a)", x=-0.32)
    sm.square_legend(fig, METHODS, COLORS, ours="Ours", loc="center left",
                     bbox_to_anchor=(1.0, 0.55), handlelength=1.4)
    fig.tight_layout(w_pad=1.2)
    sm.save(fig, OUT / "bars_comparison")


def fig_ablation():
    """Ref #17: horizontal ablation bars, full model colored, best bold, group headers."""
    sm.apply_style("paper", font_size=9)
    rows = ["(a) Ours", "(b-i) w/o $f_\\theta$", "(b-ii) w/o $g_\\gamma$",
            "(c-i) w/o denoising loss", "(c-ii) w/o null-space loss"]
    gaps = [1, 3]
    headers = {1: "Architecture ablation", 3: "Loss ablation"}
    fig, axes = plt.subplots(1, 2, figsize=(5.6, 2.4))
    y = sm.hbar_ablation(axes[0], rows, [54.1, 54.3, 60.0, 62.3, 55.2], errs=[1.2, 1.0, 0.9, 1.5, 0.9],
                         pvalues=[None, None, 1e-4, 1e-4, None], xlim=(48, 66), gaps=gaps,
                         xlabel=sm.label("Spatial dispersion", "mm", "down"))
    sm.hbar_ablation(axes[1], rows, [32.9, 34.3, 37.7, 46.0, 34.2], errs=[1.8] * 5,
                     pvalues=[None, None, 0.03, 1e-4, None], xlim=(26, 50), gaps=gaps,
                     show_rows=False, xlabel=sm.label("Peak distance", "mm", "down"))
    for i, h in headers.items():
        axes[0].text(-0.95, y[i] - 1, h, transform=axes[0].get_yaxis_transform(),
                     fontweight="bold", va="center", ha="left")
    fig.suptitle("Intracranial stimulation localization", y=1.0)
    fig.tight_layout(w_pad=0.5)
    sm.save(fig, OUT / "ablation_hbar")


def fig_lines():
    """Ref #10: color+marker per method, one shared legend on top, titles per subplot."""
    sm.apply_style("teaser", font_size=9)
    names = ["CLAPS. MS", "CLAPS. LAION", "CLAPS. Human", "Proposed"]
    cols = sm.method_colors(names, ours="Proposed", cycle=sm.LINE_CYCLE, ours_color=sm.OURS_LINE)
    data = {
        "AudioCaps": [[24, 18, 4], [17, 23, 7], [22, 18, 15.5], [38.7, 31, 30]],
        "MusicCaps": [[24, -17, 20], [15.5, 15.7, 24], [16.5, -17, 12.7], [33.8, 18.3, 23.7]],
        "Clotho": [[11, 32, 2], [11.5, 32, 23], [17, 32, 14.5], [20.8, 33.7, 28]],
    }
    fig, axes = plt.subplots(1, 3, figsize=(6.0, 2.2))
    for ax, (title, ys) in zip(axes, data.items()):
        sm.line_compare(ax, ["1", "2", "3+"], dict(zip(names, ys)), cols, ours="Proposed")
        ax.set_title(title, pad=3)
    axes[0].set_ylabel(r"Kendall's $\tau$ [%]")
    axes[0].set_xlabel("# Acoustic events")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=4, bbox_to_anchor=(0.5, 0.98), handlelength=2.4)
    fig.tight_layout(w_pad=0.6)
    sm.save(fig, OUT / "lines_comparison")


def fig_scatter():
    """Ref #05: direct labels in each point's color; marker shape = method."""
    sm.apply_style("paper", font_size=9)
    names = ["LLaVA-OneVision (7.0B)", "VideoLLaMA3 (2.0B)", "InternVL2.5 (2.2B)",
             "Video-LLaVA (7.0B)", "Ours (3.6B)"]
    cols = sm.method_colors(names, ours="Ours (3.6B)",
                            cycle=["#6F86DC", "#E2B24F", "#E0705A", "#9467BD"], ours_color="#5B4FA0")
    pts = dict(zip(names, [(18, 17.6), (30, 17.4), (31, 19.1), (29, 24.2), (85, 28.6)]))
    mk = dict(zip(names, ["P", "o", "X", "^", "D"]))
    fig, ax = plt.subplots(figsize=(2.9, 2.6))
    sm.scatter_direct(ax, pts, cols, markers=mk, ours="Ours (3.6B)",
                      offsets={names[0]: (2, -16), names[1]: (14, -4), names[2]: (14, 0),
                               names[3]: (12, 6), names[4]: (-12, 0)})
    ax.set_xlim(10, 110)
    ax.set_ylim(14, 31)
    ax.set_xlabel(sm.label("Throughput", "token/s", "up"))
    ax.set_ylabel(sm.label("BLEU4", better="up"))
    fig.tight_layout()
    sm.save(fig, OUT / "scatter_direct_label")


def fig_badges():
    """Ref #30: tinted axes + badge tick labels shared with the schematic."""
    sm.apply_style("paper", font_size=9)
    rng = np.random.default_rng(0)
    fig, axes = plt.subplots(1, 2, figsize=(6.0, 2.0))
    for ax, target in zip(axes, [5, 8]):
        p = np.exp(-0.5 * ((np.arange(10) - target) / 1.6) ** 2) + rng.uniform(0, 0.1, 10)
        p /= p.sum()
        sm.tinted_axes(ax)
        ax.bar(range(10), p, color="#2B2FD9", width=0.8, zorder=2,
               yerr=p * 0.2, error_kw=dict(ecolor="black", elinewidth=1.0, capsize=2))
        sm.badge_ticklabels(ax, [str(i) for i in range(10)], highlight=[target])
        ax.text(0.97, 0.92, f"Raw score : {target}", transform=ax.transAxes, ha="right",
                va="top", color="#1F2BD0", fontweight="bold")
        ax.set_ylim(0, (p * 1.2).max() * 1.25)
    axes[0].set_ylabel("Probability", fontweight="bold")
    fig.tight_layout()
    sm.save(fig, OUT / "badge_bars")


if __name__ == "__main__":
    for f in (fig_bars, fig_ablation, fig_lines, fig_scatter, fig_badges):
        f()
        plt.close("all")
    print("saved to", OUT)
