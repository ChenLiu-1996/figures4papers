import os
import numpy as np
from matplotlib import pyplot as plt


data_loo = {
    'methods': [
        r'Full CellSpliceNet',
        r'No Sequence',
        r'No Structure',
        r'No ROI',
        r'No Expression',
    ],
    'colors': ['#0F4D92', '#D3D3D3', '#AFE6E6', '#FFE080', '#B4E6B4'],
    'result': np.array([0.88, 0.74, 0.81, 0.81, 0.84]),
}

data_sm = {
    'methods': [
        r'Full CellSpliceNet',
        r'Sequence Only',
        r'Structure Only',
        r'ROI Only',
        r'Expression Only',
    ],
    'colors': ['#0F4D92', '#D3D3D3', '#AFE6E6', '#FFE080', '#B4E6B4'],
    'result': np.array([0.88, 0.67, 0.62, 0.63, 0.32]),
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

    # Show the full model once, then pair each omission with its single modality.
    data_ablation = {
        'methods': [data_loo['methods'][0]],
        'colors': [data_loo['colors'][0]],
        'result': [data_loo['result'][0]],
        'hatches': [''],
    }
    positions = [0]
    for group_index, i in enumerate([1, 3, 2, 4]):
        for data, hatch, offset in [(data_loo, '', 0), (data_sm, '/', 1)]:
            data_ablation['methods'].append(data['methods'][i])
            data_ablation['colors'].append(data['colors'][i])
            data_ablation['result'].append(data['result'][i])
            data_ablation['hatches'].append(hatch)
            positions.append(1.5 + group_index * 2.5 + offset * 1.1)

    fig = plt.figure(figsize=(17, 15))

    ax = fig.add_subplot(1, 1, 1)
    num_methods = len(data_ablation['methods'])
    bars = ax.bar(
        positions,
        data_ablation['result'],
        width=1.05,
        color=data_ablation['colors'],
        label=data_ablation['methods'],
        hatch=data_ablation['hatches'],
        edgecolor=['none' if not hatch else '#555555' for hatch in data_ablation['hatches']],
        linewidth=0,
    )

    for i, (bar, value) in enumerate(zip(bars, data_ablation['result'])):
        textcolor = 'white' if is_dark(data_ablation['colors'][i]) else 'black'
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() - 0.06,
            f'{value:.2f}', ha='center', va='bottom', fontsize=32, color=textcolor)

    # Add horizontal reference line at the first bar
    baseline = data_ablation['result'][0]  # 0.88
    ax.axhline(y=baseline, color=data_ablation['colors'][0], linestyle='--', linewidth=4, alpha=0.7)

    # Add arrows and reduction values for every variant (skip the full model).
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
        ax.text(bar.get_x() + bar.get_width()/2, baseline + 0.005, r'$-$'+f'{reduction:.2f}',
                ha='center', va='bottom', fontsize=24, color='red')

    ax.set_ylabel('Spearman correlation', fontsize=48, labelpad=12)
    ymax = np.max(data_ablation['result'][:])
    ax.set_ylim([0.0, ymax + 0.3])
    ax.set_yticks([0.0, 0.25, 0.50, 0.75, 1.0])
    ax.tick_params(axis='y', labelsize=36, length=10, width=2)
    ax.set_xticks([])

    ax.legend(loc='upper center', fontsize=30, frameon=False, ncol=3,
              handlelength=1.5, columnspacing=1.0, handletextpad=0.6)

    fig.tight_layout(pad=2)

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')
    os.makedirs(output_dir, exist_ok=True)
    fig.savefig(os.path.join(output_dir, 'ablation.png'), dpi=300)
    plt.close(fig)
