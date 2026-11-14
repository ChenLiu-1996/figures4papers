"""EXP-QA: learning and retention across 6 medical tasks.

Raw scores copied from main_initial.tex (2026-11-10), Table exp_qa_raw.
Rows are training stages; columns are evaluation tasks. Seed 1; MACL N=10,
total lambda=1 (equally split for MACL-both); replay K=500 per previous task.
All scores are accuracy percentages.

Standalone script: the manuscript is not read at runtime.
Produces four PNGs: exp_qa_learning_curves.png,
exp_qa_comparison.png, exp_qa_ablation.png, and
exp_qa_ablation_SFTRL.png. The fourth output compares training schedules
using Table exp_qa_sft_then_rl_raw (copied 2026-11-13); its three configurations
all use MACL-prev with Llama-3.1-8B-Instruct.
"""

from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator
import numpy as np


TASKS = ['PubMedQA', 'MedMCQA', 'MedQA', 'HeadQA', 'MedXpertQA', 'MedBullets']
STAGE_LABELS = ['PubMedQA', 'MedMCQA', 'MedQA', 'HeadQA', 'MedXpertQA', 'MedBullets']
TASK_METRICS = ['Accuracy (%)', 'Accuracy (%)', 'Accuracy (%)', 'Accuracy (%)', 'Accuracy (%)', 'Accuracy (%)']
METHOD_STYLES = {
    'Sequential SFT': {'color': '#DADADA', 'linestyle': '--', 'marker': 'o'},
    'Replay': {'color': '#C4E8BD', 'linestyle': '-', 'marker': 's'},
    'KD-LoRA': {'color': '#F3CEC7', 'linestyle': '-', 'marker': '^'},
    'SPG': {'color': '#DFC2E0', 'linestyle': '-', 'marker': 'v'},
    'SAPT': {'color': '#B5DFE2', 'linestyle': '-', 'marker': 'D'},
    'MACL-curr': {'color': '#B7CAE2', 'linestyle': '--', 'marker': '^'},
    'MACL-prev': {'color': '#0F4D92', 'linestyle': '-', 'marker': 'o'},
    'MACL-both': {'color': '#6F94BE', 'linestyle': '-.', 'marker': 's'},
}

# Display names keep the data keys aligned with the manuscript tables.
METHOD_LABELS = {
    'MACL-prev': 'MACL',
    'MACL-curr': 'MACL (current)',
    'MACL-both': 'MACL (current + previous)',
    'MACL-prev (interleaved)': 'MACL (5-epoch interleaved SFT/RL)',
    'MACL-prev (SFT → RL, 1 epoch)': 'MACL-sequential (5-epoch SFT + 1-epoch RL)',
    'MACL-prev (SFT → RL, 2 epochs)': 'MACL-sequential (5-epoch SFT + 2-epoch RL)',
}

REFERENCE_STYLES = {
    'Zero-shot': {'color': '#000000', 'linestyle': (0, (8, 4))},
    'Specialist': {'color': '#B22222', 'linestyle': (0, (8, 4))},
    'Multitask mixed': {'color': '#C65D00', 'linestyle': '-'},
}

MAIN_METHODS = ['Sequential SFT', 'Replay', 'KD-LoRA', 'SPG', 'SAPT', 'MACL-prev']
ABLATION_METHODS = ['SAPT', 'MACL-curr', 'MACL-both', 'MACL-prev']

# Static references, in TASKS order.
REFERENCE_SCORES = {
    'Zero-shot': np.array([75.1, 48.0, 57.97, 60.88, 13.06, 48.39]),
    'Specialist': np.array([78.8, 56.51, 59.47, 64.76, 30.41, 46.77]),
    'Multitask mixed': np.array([78.3, 53.91, 58.37, 64.52, 28.78, 48.39]),
}

# Each method: rows are training stages; columns are evaluation tasks.
RESULTS = {
    'Sequential SFT': np.array([
        [78.7, 50.56, 49.25, 57.98, 13.27, 38.71],  # After PubMedQA
        [78.4, 54.91, 55.38, 64.56, 15.71, 45.16],  # After MedMCQA
        [70.9, 42.22, 53.02, 51.67, 17.14, 41.94],  # After MedQA
        [70.6, 41.62, 45.33, 52.21, 13.27, 37.1],  # After HeadQA
        [48.3, 31.82, 31.34, 40.85, 24.49, 35.48],  # After MedXpertQA
        [62.0, 35.17, 38.88, 42.77, 21.43, 30.65],  # After MedBullets
    ]),
    'Replay': np.array([
        [78.2, 50.97, 52.63, 59.58, 14.69, 38.71],  # After PubMedQA
        [78.3, 55.13, 52.95, 63.66, 17.35, 40.32],  # After MedMCQA
        [76.3, 48.29, 55.38, 59.04, 18.98, 38.71],  # After MedQA
        [75.9, 44.51, 49.49, 55.35, 14.29, 38.71],  # After HeadQA
        [74.8, 43.41, 46.5, 55.51, 21.63, 46.77],  # After MedXpertQA
        [71.7, 43.77, 48.39, 54.21, 21.02, 41.94],  # After MedBullets
    ]),
    'KD-LoRA': np.array([
        [77.9, 47.43, 46.35, 52.53, 12.04, 35.48],  # After PubMedQA
        [78.5, 56.66, 56.48, 64.41, 16.73, 41.94],  # After MedMCQA
        [78.1, 50.42, 56.56, 60.68, 20.82, 43.55],  # After MedQA
        [75.3, 48.1, 51.3, 60.29, 17.96, 38.71],  # After HeadQA
        [69.2, 42.6, 49.1, 54.8, 26.12, 43.55],  # After MedXpertQA
        [65.1, 43.68, 47.05, 53.7, 21.84, 38.71],  # After MedBullets
    ]),
    'SPG': np.array([
        [75.7, 45.59, 43.28, 51.94, 11.84, 33.87],  # After PubMedQA
        [77.2, 54.84, 54.75, 65.39, 16.33, 45.16],  # After MedMCQA
        [71.2, 41.88, 52.32, 55.74, 23.06, 45.16],  # After MedQA
        [67.1, 42.31, 47.37, 54.02, 15.51, 32.26],  # After HeadQA
        [42.2, 31.87, 36.14, 40.49, 23.67, 43.55],  # After MedXpertQA
        [58.2, 35.36, 40.14, 43.04, 16.73, 37.1],  # After MedBullets
    ]),
    'SAPT': np.array([
        [76.6, 50.06, 53.1, 55.7, 13.67, 33.87],  # After PubMedQA
        [77.7, 57.57, 57.5, 65.11, 13.67, 33.87],  # After MedMCQA
        [76.1, 55.8, 60.09, 66.25, 16.94, 46.77],  # After MedQA
        [78.0, 56.39, 59.86, 66.84, 14.49, 45.16],  # After HeadQA
        [67.5, 52.16, 48.78, 60.53, 26.53, 43.55],  # After MedXpertQA
        [76.6, 56.94, 59.54, 66.21, 19.18, 38.71],  # After MedBullets
    ]),
    'MACL-curr': np.array([
        [77.5, 46.28, 51.37, 55.78, 13.27, 38.71],  # After PubMedQA
        [77.5, 55.7, 56.09, 65.43, 13.06, 37.1],  # After MedMCQA
        [78.4, 54.98, 62.37, 64.95, 15.92, 50.0],  # After MedQA
        [78.2, 56.18, 62.29, 67.23, 16.12, 41.94],  # After HeadQA
        [70.1, 51.8, 48.86, 60.25, 26.33, 46.77],  # After MedXpertQA
        [75.1, 55.53, 58.92, 64.99, 17.14, 38.71],  # After MedBullets
    ]),
    'MACL-prev': np.array([
        [76.6, 49.92, 53.73, 55.66, 13.47, 33.87],  # After PubMedQA
        [78.7, 57.3, 56.79, 65.39, 14.08, 38.71],  # After MedMCQA
        [78.5, 56.68, 60.41, 65.54, 15.31, 46.77],  # After MedQA
        [78.1, 55.65, 60.49, 66.33, 14.08, 40.32],  # After HeadQA
        [77.3, 54.34, 49.25, 61.19, 25.1, 45.16],  # After MedXpertQA
        [78.4, 56.06, 58.92, 65.97, 18.37, 41.94],  # After MedBullets
    ]),
    'MACL-both': np.array([
        [77.3, 48.15, 52.24, 56.45, 13.47, 41.94],  # After PubMedQA
        [77.6, 55.75, 55.3, 65.31, 13.88, 37.1],  # After MedMCQA
        [78.1, 56.61, 60.09, 66.33, 16.94, 46.77],  # After MedQA
        [79.2, 55.39, 59.07, 67.11, 16.33, 46.77],  # After HeadQA
        [75.4, 50.78, 47.29, 59.04, 26.73, 35.48],  # After MedXpertQA
        [78.4, 55.37, 57.42, 65.35, 20.82, 43.55],  # After MedBullets
    ]),
}


# Training-schedule ablation: Table exp_qa_sft_then_rl_raw in main_initial.tex.
# All configurations use MACL-prev and Llama-3.1-8B-Instruct.
# Rows and columns follow TASKS; the table reports point estimates only.
SCHEDULE_RESULTS = {
    'MACL-prev (interleaved)': np.array([
        [76.6, 49.92, 53.73, 55.66, 13.47, 33.87],  # After PubMedQA
        [78.7, 57.3, 56.79, 65.39, 14.08, 38.71],  # After MedMCQA
        [78.5, 56.68, 60.41, 65.54, 15.31, 46.77],  # After MedQA
        [78.1, 55.65, 60.49, 66.33, 14.08, 40.32],  # After HeadQA
        [77.3, 54.34, 49.25, 61.19, 25.1, 45.16],  # After MedXpertQA
        [78.4, 56.06, 58.92, 65.97, 18.37, 41.94],  # After MedBullets
    ]),
    'MACL-prev (SFT → RL, 1 epoch)': np.array([
        [76.6, 49.03, 50.12, 57.82, 11.22, 35.48],  # After PubMedQA
        [76.8, 55.41, 53.34, 64.56, 13.47, 38.71],  # After MedMCQA
        [76.8, 56.9, 58.21, 66.56, 17.14, 43.55],  # After MedQA
        [77.6, 56.13, 58.52, 67.74, 16.53, 41.94],  # After HeadQA
        [76.5, 52.4, 53.97, 64.56, 27.96, 41.94],  # After MedXpertQA
        [77.6, 57.52, 59.62, 67.86, 17.76, 38.71],  # After MedBullets
    ]),
    'MACL-prev (SFT → RL, 2 epochs)': np.array([
        [76.5, 48.96, 49.57, 57.55, 11.22, 35.48],  # After PubMedQA
        [76.2, 56.16, 56.4, 66.09, 14.08, 37.1],  # After MedMCQA
        [77.7, 56.32, 59.7, 66.95, 16.12, 43.55],  # After MedQA
        [77.7, 55.8, 59.15, 67.42, 18.57, 41.94],  # After HeadQA
        [76.6, 53.65, 52.87, 62.33, 27.55, 41.94],  # After MedXpertQA
        [75.9, 54.32, 58.99, 64.8, 17.96, 41.94],  # After MedBullets
    ]),
}

# Put the default MACL setting last in every ablation panel and legend.
SCHEDULE_METHODS = [
    'MACL-prev (SFT → RL, 1 epoch)',
    'MACL-prev (SFT → RL, 2 epochs)',
    'MACL-prev (interleaved)',
]
SCHEDULE_STYLES = {
    'MACL-prev (interleaved)': {'color': '#0F4D92'},
    'MACL-prev (SFT → RL, 1 epoch)': {'color': '#9BCDBB'},
    'MACL-prev (SFT → RL, 2 epochs)': {'color': '#539E87'},
}

def apply_plot_style():
    """Shared typography and axes styling for all figures."""
    plt.rcParams.update({
        'font.family': ['Helvetica', 'Arial', 'DejaVu Sans'],
        'font.size': 16,
        'axes.spines.right': False,
        'axes.spines.top': False,
        'axes.linewidth': 2,
        'legend.frameon': False,
    })


def save_png(fig, output_dir, filename):
    """Save beside this script by default, regardless of working directory."""
    directory = (Path(output_dir) if output_dir is not None
                 else Path(__file__).resolve().parent / 'figures')
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / filename
    fig.savefig(path, dpi=300)
    plt.close(fig)
    return path


# Figure 1: task-specific learning and retention curves.
def plot_exp_qa(output_dir=None, methods=None, show_multitask_mixed=True):
    """Save a 1 x 6 grid of task-specific learning curves.

    The vertical line marks training on the panel's task. Points to its
    left evaluate transfer before training; points to its right show retention.
    Each panel uses limits rounded outward to multiples of 10. Zero-shot is a horizontal
    reference, rather than an additional training stage.
    """
    methods = list(MAIN_METHODS) if methods is None else list(methods)
    if not methods or any(method not in RESULTS for method in methods):
        raise ValueError('Select at least one method from RESULTS.')

    apply_plot_style()

    fig, axes = plt.subplots(1, 6, figsize=(45, 10), sharex=True, sharey=False)
    stages = np.arange(1, len(TASKS) + 1)
    references = dict(REFERENCE_STYLES)
    if not show_multitask_mixed:
        references.pop('Multitask mixed')

    for task_idx, ax in enumerate(axes.flat):
        ax.axvline(task_idx + 1, color='#CFCECE', linewidth=2, zorder=0)
        for name, style in references.items():
            ax.axhline(REFERENCE_SCORES[name][task_idx], linewidth=1.8,
                       alpha=0.85, zorder=1, **style)
        for method in methods:
            ax.plot(stages, RESULTS[method][:, task_idx],
                    linewidth=2.2, markersize=8, alpha=1.0,
                    label=METHOD_LABELS.get(method, method), zorder=3, **METHOD_STYLES[method])
        title = TASKS[task_idx]
        ax.set_title(title, fontsize=32, pad=14)
        ax.set_xlim(0.65, len(TASKS) + 0.35)
        panel_values = np.concatenate(
            [RESULTS[method][:, task_idx] for method in methods]
            + [np.atleast_1d(REFERENCE_SCORES[name][task_idx]) for name in references]
        )
        ymin = max(0, 10 * np.floor((panel_values.min() - 1) / 10))
        ymax = min(100, 10 * np.ceil((panel_values.max() + 1) / 10))
        ax.set_ylim(ymin, ymax)
        ax.set_yticks(np.arange(ymin, ymax + 1, 10))
        ax.set_xticks(stages)
        ax.set_xticklabels(STAGE_LABELS, rotation=55, ha='right', fontsize=26)
        ax.tick_params(labelsize=26, length=5, width=1.5)
        ax.set_ylabel(TASK_METRICS[task_idx], fontsize=32, labelpad=12)
        ax.set_xlabel('Training stage', fontsize=32, labelpad=16)

    handles = [Line2D([0], [0], label=METHOD_LABELS.get(method, method), linewidth=5,
                      markersize=14, **METHOD_STYLES[method]) for method in methods]
    handles.extend(Line2D([0], [0], label=name, linewidth=5, **style)
                   for name, style in references.items())
    fig.legend(handles=handles, loc='lower center', bbox_to_anchor=(0.5, 0.005),
               ncols=len(handles), fontsize=32, columnspacing=1.2, handlelength=2.5)
    fig.tight_layout(pad=2, rect=(0, 0.1, 1, 1))
    return [save_png(fig, output_dir, 'exp_qa_learning_curves.png')]


def compute_aggregate_metrics(results):
    """Return equally weighted task averages, in percentage points.

    Final accuracy: last row, averaged over all 6 tasks.
    New-task accuracy: diagonal, immediately after learning each task.
    Seen-task accuracy: mean of stage-wise averages over learned tasks.
    Final forgetting: best post-acquisition accuracy minus final accuracy,
    averaged over the first 5 tasks (the final task has no later training).
    The maximum includes the final stage, so forgetting is nonnegative.
    """
    scores = np.asarray(results, dtype=float)
    if scores.shape != (len(TASKS), len(TASKS)):
        raise ValueError('Expected a 6 x 6 training-stage by task matrix.')
    forgetting = [scores[j:, j].max() - scores[-1, j]
                  for j in range(len(TASKS) - 1)]
    return {
        'final_accuracy': scores[-1].mean(),
        'new_task_accuracy': np.diag(scores).mean(),
        'seen_task_accuracy': np.mean([scores[t, :t + 1].mean()
                                       for t in range(len(TASKS))]),
        'final_forgetting': np.mean(forgetting),
    }


def plot_aggregate_bars(selected_methods, filename, output_dir=None, *,
                        results=None, method_styles=None,
                        separate_reference_legend=False):
    """One row of five panels, with equal task weighting and no error bars.

    Rank uses the selected methods plus Zero-shot, Specialist, and Multitask mixed; rank 1 is
    best and ties receive their average rank. Static references use their fixed
    task scores for seen-task and new-task accuracy, not a learning trajectory.
    Forgetting remains nonnegative and excludes the final task.
    """
    results = RESULTS if results is None else results
    method_styles = METHOD_STYLES if method_styles is None else method_styles
    apply_plot_style()
    methods = [*selected_methods, *REFERENCE_STYLES]
    metrics = {method: compute_aggregate_metrics(results[method])
               for method in selected_methods}
    for name in REFERENCE_STYLES:
        fixed_scores = REFERENCE_SCORES[name]
        metrics[name] = {
            'final_accuracy': fixed_scores.mean(),
            'new_task_accuracy': fixed_scores.mean(),
            'seen_task_accuracy': np.mean([fixed_scores[:t + 1].mean()
                                          for t in range(len(TASKS))]),
        }

    final_scores = np.array([results[name][-1] if name in results
                             else REFERENCE_SCORES[name] for name in methods])
    for i, name in enumerate(methods):
        # Average tied rank = 1 + number strictly better + half of other ties.
        ranks = (1 + (final_scores > final_scores[i]).sum(axis=0)
                 + 0.5 * ((final_scores == final_scores[i]).sum(axis=0) - 1))
        metrics[name]['final_rank'] = ranks.mean()

    panels = [
        ('final_accuracy', 'Final average performance ' + r'$\uparrow$', 'Accuracy (%)'),
        ('seen_task_accuracy', 'Average seen-task performance ' + r'$\uparrow$', 'Accuracy (%)'),
        ('new_task_accuracy', 'Average new-task performance ' + r'$\uparrow$', 'Accuracy (%)'),
        ('final_rank', 'Final average rank ' + r'$\downarrow$', 'Rank'),
        ('final_forgetting', 'Final average forgetting ' + r'$\downarrow$', r'$\Delta$ Accuracy (%)'),
    ]
    colors = {name: method_styles[name]['color'] for name in selected_methods}
    colors.update({name: style['color'] for name, style in REFERENCE_STYLES.items()})
    fig, axes = plt.subplots(1, 5, figsize=(45, 9))
    for ax, (key, title, ylabel) in zip(axes, panels):
        panel_methods = selected_methods
        values = np.array([metrics[name][key] for name in panel_methods])
        bars = ax.bar(np.arange(len(panel_methods)), values,
                      color=[colors[name] for name in panel_methods],
                      width=0.7, edgecolor='none', linewidth=0)
        limit_values = values
        if key != 'final_forgetting':
            reference_values = [metrics[name][key] for name in REFERENCE_STYLES]
            limit_values = np.concatenate([values, reference_values])
            for name, style in REFERENCE_STYLES.items():
                ax.axhline(metrics[name][key], linewidth=2.5, zorder=3, **style)
        # One label row per panel, clear of every bar and reference line.
        peak = float(limit_values.max())
        if key == 'final_rank':
            label_y = peak + 0.6
            upper = max(len(methods), label_y + 0.8)
            ax.set_ylim(1, upper)
            ax.set_yticks(np.arange(1, len(methods) + 1))
        elif key == 'final_forgetting':
            # Keep a zero baseline, with headroom proportional to forgetting.
            gap = max(0.1, 0.12 * peak)
            label_y = peak + gap
            ticks = MaxNLocator(nbins=5, min_n_ticks=3).tick_values(
                0, label_y + gap)
            ax.set_ylim(0, ticks[-1])
            ax.set_yticks(ticks)
        else:
            gap = max(2.0, 0.08 * peak)
            label_y = peak + gap
            upper = 10 * np.ceil((label_y + gap) / 10)
            ax.set_ylim(0, upper)
            ax.set_yticks(np.arange(0, upper + 1, 10))
        ax.set_xticks([])
        ax.set_title(title, fontsize=32, pad=18)
        ax.set_ylabel(ylabel, fontsize=32, labelpad=12)
        for spine in ax.spines.values():
            spine.set_linewidth(3)
        ax.tick_params(labelsize=26, length=8, width=2)
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, label_y,
                    f'{value:.2f}', ha='center', va='bottom',
                    fontsize=26, zorder=4)

    handles = [Patch(facecolor=colors[name], edgecolor='none', label=METHOD_LABELS.get(name, name))
               for name in selected_methods]
    reference_handles = [Line2D([0], [0], label=name, linewidth=2.5, **style)
                         for name, style in REFERENCE_STYLES.items()]
    if separate_reference_legend:
        # Keep long training-schedule names together above the reference legend.
        fig.legend(handles=handles, loc='lower center', bbox_to_anchor=(0.5, 0.105),
                   ncols=len(handles), fontsize=32, columnspacing=1.2, handlelength=1.5)
        fig.legend(handles=reference_handles, loc='lower center', bbox_to_anchor=(0.5, 0.005),
                   ncols=len(reference_handles), fontsize=32, columnspacing=1.2, handlelength=1.5)
        fig.tight_layout(pad=2, rect=(0, 0.19, 1, 1))
    else:
        handles.extend(reference_handles)
        fig.legend(handles=handles, loc='lower center', bbox_to_anchor=(0.5, 0.01),
                   ncols=len(handles), fontsize=32, columnspacing=1.2, handlelength=1.5)
        fig.tight_layout(pad=2, rect=(0, 0.1, 1, 1))
    return save_png(fig, output_dir, filename)


# Figure 2: main-method comparison; ablation variants are excluded.
def plot_aggregate_comparison(output_dir=None):
    return plot_aggregate_bars(MAIN_METHODS, 'exp_qa_comparison.png', output_dir)


# Figure 3: reward-branch ablation, with SAPT as the no-MACL baseline.
def plot_ablation(output_dir=None):
    """Rank is computed within this ablation plus the three static references.

    Consequently, rank values are not directly comparable to Figure 2 ranks.
    """
    return plot_aggregate_bars(ABLATION_METHODS, 'exp_qa_ablation.png', output_dir)


# Figure 4: interleaved versus two-stage SFT--RL training.
def plot_sft_rl_ablation(output_dir=None):
    """Compare three MACL-prev schedules using the same five aggregate metrics.

    Rank is computed within these schedules and the three static references.
    No uncertainty bars are inferred from the table's point estimates.
    """
    return plot_aggregate_bars(
        SCHEDULE_METHODS, 'exp_qa_ablation_SFTRL.png', output_dir,
        results=SCHEDULE_RESULTS, method_styles=SCHEDULE_STYLES,
        separate_reference_legend=False,
    )


def main():
    """Generate learning curves, main comparison, and both ablations (PNG only)."""
    curve_paths = plot_exp_qa()
    comparison_path = plot_aggregate_comparison()
    ablation_path = plot_ablation()
    schedule_path = plot_sft_rl_ablation()
    for path in [*curve_paths, comparison_path, ablation_path, schedule_path]:
        print(f'Saved {path}')


if __name__ == '__main__':
    main()
