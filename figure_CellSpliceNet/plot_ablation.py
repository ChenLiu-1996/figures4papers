import os
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import gridspec as gridspec


data_ablation = {
    'methods': [
        r'CellSpliceNet',
        r'No Expression',
        r'No Structure',
        r'No ROI',
        r'No Sequence',
    ],
    'colors': ['#0F4D92', '#B4E6B4', '#AFE6E6', '#FFE080', '#D3D3D3'],
    'result': np.array([0.88, 0.84, 0.82, 0.81, 0.74]),
}

def is_dark(color_in_hex, threshold=128):
    color = color_in_hex.lstrip('#')
    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)

    luminance = 0.299*r + 0.587*g + 0.114*b
    return luminance < threshold


if __name__ == '__main__':
    plt.rcParams['font.family'] = 'helvetica'
    plt.rcParams['font.size'] = 24
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.linewidth'] = 3

    fig = plt.figure(figsize=(13, 13))

    ax = fig.add_subplot(1, 1, 1)
    num_methods = len(data_ablation['methods'])
    bars = ax.bar(
        np.arange(num_methods),
        data_ablation['result'],
        color=data_ablation['colors'],
        label=data_ablation['methods'],
    )

    for i, (bar, value) in enumerate(zip(bars, data_ablation['result'])):
        textcolor = 'white' if is_dark(data_ablation['colors'][i]) else 'black'
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() - 0.08,
            f'{value:.2f}', ha='center', va='bottom', fontsize=32, color=textcolor)

    # Add horizontal reference line at the first bar
    baseline = data_ablation['result'][0]  # 0.88
    ax.axhline(y=baseline, color=data_ablation['colors'][0], linestyle='--', linewidth=4, alpha=0.7)

    # Add arrows and reduction values for bars 2-5 (skip the first bar)
    for i in range(1, num_methods):
        bar = bars[i]
        current_value = data_ablation['result'][i]
        reduction = baseline - current_value

        # Position for the arrow (right side of the bar)
        x_pos = bar.get_x() + bar.get_width()

        # Draw arrow from baseline down to bar top (top to bottom)
        ax.annotate('', xy=(x_pos, current_value), xytext=(x_pos, baseline),
                    arrowprops=dict(arrowstyle='->', color='red', lw=4))

        # Add reduction text near the top (at baseline level)
        ax.text(x_pos - 0.3, baseline + 0.005, r'$-$'+f'{reduction:.2f}',
                ha='left', va='bottom', fontsize=24, color='red')

    ax.set_ylabel('Spearman correlation', fontsize=54, labelpad=12)
    ymax = np.max(data_ablation['result'][:])
    ax.set_ylim([0.0, ymax + 0.5])
    ax.set_yticks([0.0, 0.25, 0.50, 0.75, 1.0])
    ax.tick_params(axis='y', labelsize=36, length=10, width=2)
    ax.set_xticks([])

    ax.legend(bbox_to_anchor=(0.50, 1.08), loc='upper left', fontsize=36, frameon=False)

    fig.tight_layout(pad=2)

    os.makedirs('./figures/', exist_ok=True)
    fig.savefig('./figures/ablation.png', dpi=300)
    plt.close(fig)
