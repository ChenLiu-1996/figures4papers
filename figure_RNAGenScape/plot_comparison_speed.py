import os

import numpy as np
import matplotlib.pyplot as plt


# Inference time in milliseconds per sample, with the plotting color.
# (label, samples/ms mean, samples/ms std over 3 datasets, color)
results_inference = [
    ('DiffAb', 0.0544, 0.0032, "#babbc6"),
    ('IgLM', 0.0083, 0.0001, '#ecc4c4'),
    ('NOS-C', 0.000778, 0.000004, '#ecc4e7'),
    ('NOS-D', 0.0124, 0.0002, '#ea84dd'),
    ('PCD', 0.7705, 0.0035, '#c4a8e8'),
    ('EM', 0.3921, 0.1037, '#e8c48a'),
    ('MFM', 1.5581, 0.0082, '#f4aa6d'),
    ('gg-dWJS', 0.2069, 0.0020, '#70cab4'),
    ('MPGD', 0.4019, 0.0086, '#8ab4e8'),
    (r'$\texttt{RNAGenScape}$ \textbf{(ours)}', 0.9518, 0.0025, '#0f4d92'),
]


def plot_speed(output_path='figures/results_comparison_speed.png', show_errorbars=True):
    """Save the inference throughput comparison (samples/ms)."""
    plt.rcParams['text.usetex'] = True
    plt.rcParams['font.family'] = 'helvetica'
    plt.rcParams['font.size'] = 16
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.linewidth'] = 2

    options, speed_values, speed_stds, colors = zip(*results_inference)
    speed_values = np.asarray(speed_values, dtype=float)
    speed_stds = np.asarray(speed_stds, dtype=float)

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(options))
    ax.bar(
        x,
        speed_values,
        yerr=speed_stds if show_errorbars else None,
        color=colors,
        label=options,
        capsize=10,
        error_kw={'elinewidth': 1.5, 'capthick': 1.5, 'ecolor': 'black'},
    )

    ax.set_xlim([-1, len(options)])
    ax.legend(loc='upper left', frameon=False, fontsize=14, ncol=2)
    ax.set_xticks([])
    ax.set_ylabel('Inference Throughput ' + r'$\uparrow$' + '\n(samples / ms)', fontsize=18)
    ax.set_yscale('log')
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(ymin, ymax * 50)

    for i, value in enumerate(speed_values):
        label = f'{value:.3f}' if not show_errorbars else f'{value:.3f}'
        ax.text(i, value * 1.4, label, ha='center', va='bottom', fontsize=14)

    fig.tight_layout(pad=1)
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

if __name__ == '__main__':
    plot_speed()
