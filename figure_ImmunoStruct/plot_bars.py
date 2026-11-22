import os
import numpy as np
from matplotlib import pyplot as plt
from raw_data import data_comparison_IEDB, data_ablation_IEDB, data_comparison_Cancer, data_ablation_Cancer


def decode_ablation(data_dict):
    binary_list = data_dict['ablations']
    component_str = data_dict['components']
    decoded_list = []
    for binary_code in binary_list:
        assert len(binary_code) == len(component_str)
        decoded_str = []
        for i, c in enumerate(binary_code):
            if c == '1':
                decoded_str.append(component_str[i])
        decoded_list.append(' + '.join(decoded_str))
    return decoded_list


if __name__ == '__main__':
    plt.rcParams['font.family'] = 'helvetica'
    plt.rcParams['font.size'] = 24
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.linewidth'] = 3
    plt.rcParams['svg.fonttype'] = 'none'

    fig = plt.figure(figsize=(28, 6))

    ax = fig.add_subplot(1, 4, 1)
    ax.bar(range(len(data_comparison_IEDB['mean'])),
           data_comparison_IEDB['mean'][:, 0],
           yerr=data_comparison_IEDB['std'][:, 0],
           capsize=5,
           color=data_comparison_IEDB['colors'],
           label=data_comparison_IEDB['methods'])
    handles, labels = ax.get_legend_handles_labels()
    ax.set_xticks([])
    ax.set_ylim([0.5, 0.9])
    ax.set_ylabel(data_comparison_IEDB['metrics'][0], fontsize=32)

    ax = fig.add_subplot(1, 4, 2)
    ax.bar(range(len(data_comparison_IEDB['mean'])),
           data_comparison_IEDB['mean'][:, 1],
           yerr=data_comparison_IEDB['std'][:, 1],
           capsize=5,
           color=data_comparison_IEDB['colors'])
    ax.set_xticks([])
    ax.set_ylim([0.15, 0.75])
    ax.set_ylabel(data_comparison_IEDB['metrics'][1], fontsize=32)

    ax = fig.add_subplot(1, 4, 3)
    ax.bar(range(len(data_comparison_IEDB['mean'])),
           data_comparison_IEDB['mean'][:, 2],
           yerr=data_comparison_IEDB['std'][:, 2],
           capsize=5,
           color=data_comparison_IEDB['colors'])
    ax.set_xticks([])
    ax.set_ylim([0.18, 0.55])
    ax.set_ylabel(data_comparison_IEDB['metrics'][2], fontsize=32)

    ax = fig.add_subplot(1, 4, 4)
    ax.legend(handles, labels, frameon=False)
    ax.set_axis_off()

    fig.tight_layout(pad=2)

    os.makedirs('./figures/', exist_ok=True)
    fig.savefig('./figures/bars_comparison_IEDB.png', dpi=600)
    plt.close(fig)


    fig = plt.figure(figsize=(24, 8))

    ax = fig.add_subplot(1, 3, 1)
    ax.barh(range(len(data_ablation_IEDB['mean'][:, 0])),
            data_ablation_IEDB['mean'][:, 0],
            xerr=data_ablation_IEDB['std'][:, 0],
            color=[(0.215686, 0.458824, 0.729412, alpha) for alpha in np.linspace(0.2, 1.0, 12)],
            ecolor='k',
            capsize=5,
    )

    ax.set_yticks(range(len(data_ablation_IEDB['ablations'])))
    ax.set_yticklabels(decode_ablation(data_ablation_IEDB))
    ax.set_xlim([0.75, 0.9])
    ax.set_xticks([0.75, 0.8, 0.85, 0.9])
    ax.set_xticklabels([0.75, 0.8, 0.85, 0.9])
    ax.set_xlabel(data_ablation_IEDB['metrics'][0], fontsize=32)

    ax = fig.add_subplot(1, 3, 2)
    ax.barh(range(len(data_ablation_IEDB['mean'][:, 1])),
            data_ablation_IEDB['mean'][:, 1],
            xerr=data_ablation_IEDB['std'][:, 1],
            color=[(0.215686, 0.458824, 0.729412, alpha) for alpha in np.linspace(0.2, 1.0, 12)],
            ecolor='k',
            capsize=5,
    )

    ax.set_yticks([])
    ax.set_xlim([0.4, 0.72])
    ax.set_xticks([0.4, 0.5, 0.6, 0.7])
    ax.set_xticklabels([0.4, 0.5, 0.6, 0.7])
    ax.set_xlabel(data_ablation_IEDB['metrics'][1], fontsize=32)

    ax = fig.add_subplot(1, 3, 3)
    ax.barh(range(len(data_ablation_IEDB['mean'][:, 2])),
            data_ablation_IEDB['mean'][:, 2],
            xerr=data_ablation_IEDB['std'][:, 2],
            color=[(0.215686, 0.458824, 0.729412, alpha) for alpha in np.linspace(0.2, 1.0, 12)],
            ecolor='k',
            capsize=5,
    )

    ax.set_yticks([])
    ax.set_xlim([0.4, 0.55])
    ax.set_xticks([0.4, 0.45, 0.5, 0.55])
    ax.set_xticklabels([0.4, 0.45, 0.5, 0.55])
    ax.set_xlabel(data_ablation_IEDB['metrics'][2], fontsize=32)

    fig.tight_layout(pad=2)
    os.makedirs('./figures/', exist_ok=True)
    fig.savefig('./figures/bars_ablation_IEDB.png', dpi=600)
    plt.close(fig)


    fig = plt.figure(figsize=(28, 6))

    ax = fig.add_subplot(1, 4, 1)
    ax.bar(range(len(data_comparison_Cancer['mean'])),
           data_comparison_Cancer['mean'][:, 0],
           yerr=data_comparison_Cancer['std'][:, 0],
           capsize=5,
           color=data_comparison_Cancer['colors'],
           label=data_comparison_Cancer['methods'])
    handles, labels = ax.get_legend_handles_labels()
    ax.set_xticks([])
    ax.set_ylim([0.5, 0.82])
    ax.set_ylabel(data_comparison_Cancer['metrics'][0], fontsize=32)

    ax = fig.add_subplot(1, 4, 2)
    ax.bar(range(len(data_comparison_Cancer['mean'])),
           data_comparison_Cancer['mean'][:, 1],
           yerr=data_comparison_Cancer['std'][:, 1],
           capsize=5,
           color=data_comparison_Cancer['colors'])
    ax.set_xticks([])
    ax.set_ylim([0.16, 0.52])
    ax.set_ylabel(data_comparison_Cancer['metrics'][1], fontsize=32)

    ax = fig.add_subplot(1, 4, 3)
    ax.bar(range(len(data_comparison_Cancer['mean'])),
           data_comparison_Cancer['mean'][:, 2],
           yerr=data_comparison_Cancer['std'][:, 2],
           capsize=5,
           color=data_comparison_Cancer['colors'])
    ax.set_xticks([])
    ax.set_ylim([0.14, 0.44])
    ax.set_ylabel(data_comparison_Cancer['metrics'][2], fontsize=32)

    ax = fig.add_subplot(1, 4, 4)
    ax.legend(handles, labels, frameon=False)
    ax.set_axis_off()

    fig.tight_layout(pad=2)

    os.makedirs('./figures/', exist_ok=True)
    fig.savefig('./figures/bars_comparison_Cancer.png', dpi=600)
    plt.close(fig)

    fig = plt.figure(figsize=(28, 6))

    items_shown = [6, 4, 0] # transfer + contrastive, transfer, none

    ax = fig.add_subplot(1, 4, 1)
    ax.bar(range(len(items_shown)),
           data_ablation_Cancer['mean'][:, 0][items_shown],
           yerr=data_ablation_Cancer['std'][:, 0][items_shown],
           capsize=5,
           color=[(0.215686, 0.458824, 0.729412, alpha) for alpha in [1.0, 0.7, 0.4]],
           label=['ImmunoStruct', 'No Contrastive Learning',
                  'No Contrastive Learning &\nNo Transfer Learning'])
    handles, labels = ax.get_legend_handles_labels()
    ax.set_xticks([])
    ax.set_ylim([0.68, 0.80])
    ax.set_ylabel(data_ablation_Cancer['metrics'][0], fontsize=32)

    ax = fig.add_subplot(1, 4, 2)
    ax.bar(range(len(items_shown)),
           data_ablation_Cancer['mean'][:, 1][items_shown],
           yerr=data_ablation_Cancer['std'][:, 1][items_shown],
           capsize=5,
           color=[(0.215686, 0.458824, 0.729412, alpha) for alpha in [1.0, 0.7, 0.4]])
    ax.set_xticks([])
    ax.set_ylim([0.30, 0.52])
    ax.set_ylabel(data_ablation_Cancer['metrics'][1], fontsize=32)

    ax = fig.add_subplot(1, 4, 3)
    ax.bar(range(len(items_shown)),
           data_ablation_Cancer['mean'][:, 2][items_shown],
           yerr=data_ablation_Cancer['std'][:, 2][items_shown],
           capsize=5,
           color=[(0.215686, 0.458824, 0.729412, alpha) for alpha in [1.0, 0.7, 0.4]])
    ax.set_xticks([])
    ax.set_ylim([0.29, 0.43])
    ax.set_ylabel(data_ablation_Cancer['metrics'][2], fontsize=32)

    ax = fig.add_subplot(1, 4, 4)
    ax.legend(handles, labels, frameon=False)
    ax.set_axis_off()

    fig.tight_layout(pad=2)
    os.makedirs('./figures/', exist_ok=True)
    fig.savefig('./figures/bars_ablation_Cancer.png', dpi=600)
    plt.close(fig)
