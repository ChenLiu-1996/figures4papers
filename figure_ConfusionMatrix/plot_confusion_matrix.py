import os

import matplotlib

matplotlib.use("Agg")

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from raw_data import BASELINE_COUNTS, CLASS_NAMES, PROPOSED_COUNTS


# House-style blues from scientific-figure-making/references/design-theory.md
_CMAP = LinearSegmentedColormap.from_list(
    "figures4papers_blue",
    ["#FFFFFF", "#D6E4F2", "#3775BA", "#0F4D92"],
)


def _row_normalize(counts: np.ndarray) -> np.ndarray:
    row_sums = counts.sum(axis=1, keepdims=True)
    row_sums = np.maximum(row_sums, 1)
    return counts / row_sums


def _draw_matrix(ax, matrix, class_names, title, cbar_label, fmt, vmin, vmax):
    im = ax.imshow(matrix, cmap=_CMAP, vmin=vmin, vmax=vmax)
    ax.set_title(title, fontsize=18, pad=10)
    ax.set_xlabel("Predicted", fontsize=16)
    ax.set_ylabel("True", fontsize=16)
    ax.set_xticks(np.arange(len(class_names)))
    ax.set_yticks(np.arange(len(class_names)))
    ax.set_xticklabels(class_names, rotation=30, ha="right")
    ax.set_yticklabels(class_names)
    ax.tick_params(length=0)
    ax.set_xticks(np.arange(len(class_names)) - 0.5, minor=True)
    ax.set_yticks(np.arange(len(class_names)) - 0.5, minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=2)
    ax.tick_params(which="minor", bottom=False, left=False)

    threshold = (vmin + vmax) / 2.0
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = matrix[i, j]
            text = fmt(value)
            ax.text(
                j,
                i,
                text,
                ha="center",
                va="center",
                fontsize=13,
                color="white" if value >= threshold else "#272727",
                fontweight="bold" if i == j else "normal",
            )

    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(cbar_label, fontsize=14)
    cbar.outline.set_linewidth(1.5)
    return im


def plot_counts_and_normalized(out_path: str):
    counts = np.asarray(PROPOSED_COUNTS, dtype=float)
    normalized = _row_normalize(counts)

    plt.rcParams["font.family"] = ["Helvetica", "Arial", "DejaVu Sans", "sans-serif"]
    plt.rcParams["font.size"] = 15
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.linewidth"] = 2
    plt.rcParams["svg.fonttype"] = "none"

    fig = plt.figure(figsize=(13, 5.5))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    _draw_matrix(
        ax1,
        counts,
        CLASS_NAMES,
        title="Proposed model (counts)",
        cbar_label="Count",
        fmt=lambda v: f"{int(round(v))}",
        vmin=0,
        vmax=counts.max(),
    )
    _draw_matrix(
        ax2,
        normalized,
        CLASS_NAMES,
        title="Proposed model (row-normalized)",
        cbar_label="Recall",
        fmt=lambda v: f"{v:.2f}",
        vmin=0.0,
        vmax=1.0,
    )

    fig.tight_layout(pad=2)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    fig.savefig(out_path, dpi=300)
    fig.savefig(out_path.replace(".png", ".pdf"))
    plt.close(fig)


def plot_baseline_vs_proposed(out_path: str):
    baseline = np.asarray(BASELINE_COUNTS, dtype=float)
    proposed = np.asarray(PROPOSED_COUNTS, dtype=float)
    vmax = max(baseline.max(), proposed.max())

    plt.rcParams["font.family"] = ["Helvetica", "Arial", "DejaVu Sans", "sans-serif"]
    plt.rcParams["font.size"] = 15
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.linewidth"] = 2
    plt.rcParams["svg.fonttype"] = "none"

    fig = plt.figure(figsize=(13, 5.5))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    _draw_matrix(
        ax1,
        baseline,
        CLASS_NAMES,
        title="Baseline (counts)",
        cbar_label="Count",
        fmt=lambda v: f"{int(round(v))}",
        vmin=0,
        vmax=vmax,
    )
    _draw_matrix(
        ax2,
        proposed,
        CLASS_NAMES,
        title=r"Proposed (ours)",
        cbar_label="Count",
        fmt=lambda v: f"{int(round(v))}",
        vmin=0,
        vmax=vmax,
    )

    fig.tight_layout(pad=2)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    fig.savefig(out_path, dpi=300)
    fig.savefig(out_path.replace(".png", ".pdf"))
    plt.close(fig)


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "figures")
    plot_counts_and_normalized(os.path.join(out_dir, "confusion_counts_normalized.png"))
    plot_baseline_vs_proposed(os.path.join(out_dir, "confusion_baseline_vs_proposed.png"))
    print(f"Saved figures to {out_dir}")
