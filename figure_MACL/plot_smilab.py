"""Redraw every figure_MACL figure in smilab-style.

Data and metric definitions are imported from the original plot_exp_*.py
scripts (nothing is copied), so numbers stay identical to figures/.

Run:  python figure_MACL/plot_smilab.py
Out:  figure_MACL/figures_smilab/*.{pdf,png}

Style decisions (see smilab-style/references/design-rules.md):
  * one method -> color map for all 11 figures; MACL = red-pink, placed last, bold
  * static references (Zero-shot / Specialist / Multitask mixed) are gray lines,
    so color is reserved for methods
  * bar values written vertically inside bars; direction arrows on y labels
  * Times + STIX math, sized at print width (7.0 in double column)
"""

import importlib.util
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "smilab-style"))
import smilab_style as sm  # noqa: E402

OUT = HERE / "figures_smilab"
WIDTH = 7.0  # in, double-column

# ---------------------------------------------------------------------------
# One color map for the whole paper
# ---------------------------------------------------------------------------
LABELS = {"MACL-prev": "MACL", "MACL-curr": "MACL (current)", "MACL-both": "MACL (current + previous)",
          "MACL-prev (interleaved)": "MACL (interleaved)",
          "MACL-prev (SFT → RL, 1 epoch)": "SFT → RL (1 epoch)",
          "MACL-prev (SFT → RL, 2 epochs)": "SFT → RL (2 epochs)"}
OURS_KEYS = {"MACL-prev", "MACL-prev (interleaved)"}
COLORS = {
    "Sequential SFT": "#C9C9C9",
    "Replay": sm.METHOD_CYCLE[1],   # green
    "KD-LoRA": sm.METHOD_CYCLE[6],  # orange
    "SPG": sm.METHOD_CYCLE[5],      # purple
    "SAPT": sm.METHOD_CYCLE[4],     # teal
    "MACL-prev": sm.OURS,
    # ablation variants: lighter tints of the ours hue (same family, less emphasis)
    "MACL-curr": "#F3CFCC",
    "MACL-both": "#E9AAA6",
    "MACL-prev (interleaved)": sm.OURS,
    "MACL-prev (SFT → RL, 1 epoch)": "#F3CFCC",
    "MACL-prev (SFT → RL, 2 epochs)": "#E9AAA6",
}
MARKERS = {"Sequential SFT": "o", "Replay": "s", "KD-LoRA": "^", "SPG": "v", "SAPT": "D", "MACL-prev": "o"}
REFS = {  # gray, distinguished by dash pattern
    "Zero-shot": dict(color="#9A9A9A", linestyle=(0, (1.5, 1.5)), linewidth=1.1),
    "Specialist": dict(color="#444444", linestyle=(0, (4, 2)), linewidth=1.1),
    "Multitask mixed": dict(color="#777777", linestyle=(0, (6, 1.5, 1.5, 1.5)), linewidth=1.1),
}


def name(key):
    return LABELS.get(key, key)


def load(tag):
    spec = importlib.util.spec_from_file_location(f"exp_{tag}", HERE / f"plot_exp_{tag}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.ITEMS = getattr(mod, "TASKS", None) or mod.DISCIPLINES
    return mod


def legend_handles(methods, refs=REFS, line=False):
    hs = []
    for m in methods:
        c = COLORS[m]
        if line:
            hs.append(Line2D([0], [0], color=sm.darken(c, 0.9), marker=MARKERS.get(m, "o"), ms=4,
                             lw=2.2 if m in OURS_KEYS else 1.3, label=name(m)))
        else:
            hs.append(Patch(facecolor=c, edgecolor=sm.darken(c, 0.85), linewidth=0.6, label=name(m)))
    hs += [Line2D([0], [0], label=r, **s) for r, s in refs.items()]
    return hs


def top_legend(fig, handles, y=1.0, ncol=None):
    leg = fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, y),
                     ncol=ncol or len(handles), handlelength=1.8, columnspacing=1.0,
                     borderpad=0.35, handletextpad=0.5)
    for t in leg.get_texts():
        if t.get_text() in {name(k) for k in OURS_KEYS}:
            t.set_fontweight("bold")
    return leg


# ---------------------------------------------------------------------------
# Learning curves
# ---------------------------------------------------------------------------

def learning_curves(mod, tag):
    sm.apply_style("paper", font_size=7)
    methods = mod.MAIN_METHODS
    n = len(mod.ITEMS)
    rows = 1 if n <= 6 else 2
    cols = int(np.ceil(n / rows))
    fig, axes = plt.subplots(rows, cols, figsize=(WIDTH, 1.75 * rows + 0.35), squeeze=False)
    stages = np.arange(1, n + 1)
    metrics = getattr(mod, "TASK_METRICS", ["Accuracy (%)"] * n)
    for j, ax in enumerate(axes.flat):
        ax.axvspan(j + 0.6, j + 1.4, color="#F1F1F1", zorder=0, lw=0)  # "training on this task"
        for r, s in REFS.items():
            ax.axhline(mod.REFERENCE_SCORES[r][j], zorder=1, **s)
        for m in methods:
            ours = m in OURS_KEYS
            ax.plot(stages, mod.RESULTS[m][:, j], color=sm.darken(COLORS[m], 0.9),
                    marker=MARKERS[m], ms=3.2 if ours else 2.4, lw=1.8 if ours else 0.9,
                    zorder=5 if ours else 3, markeredgecolor="white" if ours else "none",
                    markeredgewidth=0.5)
        vals = np.concatenate([mod.RESULTS[m][:, j] for m in methods]
                              + [[mod.REFERENCE_SCORES[r][j]] for r in REFS])
        lo = max(0, 10 * np.floor((vals.min() - 1) / 10))
        hi = min(100, 10 * np.ceil((vals.max() + 1) / 10))
        ax.set_ylim(lo, hi)
        ax.set_xlim(0.5, n + 0.5)
        ax.set_xticks(stages)
        if n > 6:  # 12 names do not fit; numbers + the shaded column identify the stage
                        ax.set_xticklabels([str(k) if k % 2 else "" for k in stages], fontsize=6)
        else:
            ax.set_xticklabels(mod.STAGE_LABELS, rotation=50, ha="right", rotation_mode="anchor",
                               fontsize=6)
        ax.tick_params(axis="x", length=2, pad=1.5)
        ax.grid(axis="both", color=sm.GRID, lw=0.5)
        title = mod.ITEMS[j]
        ax.set_title(title if len(title) < 22 else title.replace(" & ", " &\n"), pad=3,
                     fontsize=7.5)
        metric = metrics[j].replace("(0--100)", "").replace("(%)", "").strip()
        unit = "%" if "%" in metrics[j] else None
        if j % cols == 0 or len(set(metrics)) > 1:
            ax.set_ylabel(sm.label(metric, unit, "up"), labelpad=2)
    fig.supxlabel("Training stage" + (" (1 = " + mod.ITEMS[0] + ", …, " + str(n) + " = "
                  + mod.ITEMS[-1] + ")" if n > 6 else ""), fontsize=8, y=0.0)
    fig.tight_layout(pad=0.3, w_pad=0.5, h_pad=0.6, rect=(0, 0.02, 1, 1))
    top_legend(fig, legend_handles(methods, line=True), y=1.0)
    return sm.save(fig, OUT / f"exp_{tag}_learning_curves")


# ---------------------------------------------------------------------------
# Aggregate bars (comparison / ablation)
# ---------------------------------------------------------------------------

def aggregate(mod, methods, results):
    met = {m: mod.compute_aggregate_metrics(results[m]) for m in methods}
    n = len(mod.ITEMS)
    for r in REFS:
        s = mod.REFERENCE_SCORES[r]
        met[r] = {"final_accuracy": s.mean(), "new_task_accuracy": s.mean(),
                  "seen_task_accuracy": np.mean([s[:t + 1].mean() for t in range(n)])}
    everyone = [*methods, *REFS]
    final = np.array([results[k][-1] if k in results else mod.REFERENCE_SCORES[k] for k in everyone])
    for i, k in enumerate(everyone):  # average tied rank, as in the original scripts
        ranks = 1 + (final > final[i]).sum(0) + 0.5 * ((final == final[i]).sum(0) - 1)
        met[k]["final_rank"] = ranks.mean()
    return met


PANELS = [
    ("final_accuracy", "Final average", "Score", "up"),
    ("seen_task_accuracy", "Seen-task average", "Score", "up"),
    ("new_task_accuracy", "New-task average", "Score", "up"),
    ("final_rank", "Final average rank", "Rank", "down"),
    ("final_forgetting", "Final forgetting", r"$\Delta$ Score", "down"),
]


def aggregate_bars(mod, methods, filename, results=None):
    results = mod.RESULTS if results is None else results
    sm.apply_style("paper", font_size=7)
    met = aggregate(mod, methods, results)
    fig, axes = plt.subplots(1, 5, figsize=(WIDTH, 1.65))
    for ax, (key, title, ylab, better) in zip(axes, PANELS):
        vals = np.array([met[m][key] for m in methods])
        refs = {r: met[r][key] for r in REFS if key in met[r]}
        top = max([*vals, *refs.values()])
        if key == "final_rank":
            ylim = (0, np.ceil(len(methods) + len(REFS)) + 0.5)
        elif key == "final_forgetting":
            ylim = (0, max(1.0, top * 1.25))
        else:
            ylim = (0, 10 * np.ceil(top * 1.12 / 10))
        sm.bar_compare(ax, [name(m) for m in methods], vals,
                       {name(m): COLORS[m] for m in methods}, fmt="{:.1f}", ylim=ylim,
                       ylabel=sm.label(ylab, better=better), width=0.74)
        for r, v in refs.items():
            ax.axhline(v, zorder=4, **REFS[r])
        ax.set_title(title, pad=3, fontsize=7.5)
        ax.yaxis.labelpad = 1.5
    fig.tight_layout(pad=0.3, w_pad=0.6)
    top_legend(fig, legend_handles(methods), y=1.0,
               ncol=len(methods) + 3 if len(methods) + 3 <= 9 else 5)
    return sm.save(fig, OUT / filename)


# ---------------------------------------------------------------------------
# Overview retention panels (Fig. 1 B / D)
# ---------------------------------------------------------------------------

def retention(matrix):
    s = np.asarray(matrix, float)
    n = len(s)
    return np.array([(np.diag(s, k=-d) - np.diag(s)[:n - d]).mean() for d in range(n)])


def overview(mods, methods, filename):
    sm.apply_style("paper", font_size=7)
    titles = {"sub": "Medical subdisciplines", "qa": "Medical QA datasets",
              "task": "Heterogeneous medical tasks"}
    fig, axes = plt.subplots(1, 3, figsize=(WIDTH * 0.62, 1.55), sharey=True)
    for ax, tag in zip(axes, ["sub", "qa", "task"]):
        mod = mods[tag]
        n = len(mod.ITEMS)
        ax.axhline(0, **REFS["Zero-shot"])
        for m in methods:
            c = sm.darken(COLORS[m], 0.9)
            R = mod.RESULTS[m]
            for t in range(n):
                cur = R[t:, t] - R[t, t]
                ax.plot(np.arange(len(cur)), cur, color=c, lw=0.6, alpha=0.25, zorder=2)
            ax.plot(np.arange(n), retention(R), color=c, marker=MARKERS[m], ms=3,
                    lw=1.8 if m in OURS_KEYS else 1.3, zorder=4,
                    markeredgecolor="white", markeredgewidth=0.4)
        lows = [min((md.RESULTS[m][t:, t] - md.RESULTS[m][t, t]).min()
                    for t in range(len(md.ITEMS)))
                for m in ["Sequential SFT", "Replay", "MACL-prev"] for md in mods.values()]
        ax.set_ylim(10 * np.floor(min(lows) / 10) - 2, 10)  # shared by panels B and D
        ax.set_xlim(-0.4, n - 0.6)
        ax.set_xticks(np.arange(0, n, 2 if n > 6 else 1))
        ax.set_title(titles[tag], pad=3, fontsize=7.5)
        ax.grid(axis="both", color=sm.GRID, lw=0.5)
    axes[0].set_ylabel(sm.label(r"$\Delta$ Performance", better="up"))
    fig.supxlabel("Tasks learned", fontsize=7.5, y=0.02)
    fig.tight_layout(pad=0.3, w_pad=0.5)
    top_legend(fig, legend_handles(methods, refs={}, line=True), y=1.0)
    return sm.save(fig, OUT / filename)


def main():
    mods = {t: load(t) for t in ("sub", "qa", "task")}
    paths = []
    for tag, mod in mods.items():
        paths += learning_curves(mod, tag)
        paths += aggregate_bars(mod, mod.MAIN_METHODS, f"exp_{tag}_comparison")
        paths += aggregate_bars(mod, mod.ABLATION_METHODS, f"exp_{tag}_ablation")
    qa = mods["qa"]
    paths += aggregate_bars(qa, qa.SCHEDULE_METHODS, "exp_qa_ablation_SFTRL", results=qa.SCHEDULE_RESULTS)
    paths += overview(mods, ["Sequential SFT", "Replay"], "overview_panel_b")
    paths += overview(mods, ["MACL-prev"], "overview_panel_d")
    for p in paths:
        if p.suffix == ".png":
            print("saved", p.relative_to(HERE.parent))


if __name__ == "__main__":
    main()
