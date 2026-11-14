"""EXP-TASK: learning and retention across 5 medical tasks.

Raw scores copied from main_initial.tex (2026-11-10), Table exp_task_raw.
Rows are training stages; columns are evaluation tasks. Seed 1; MACL N=10,
total lambda=1 (equally split for MACL-both); replay K=500 per previous task.
All task scores use a 0--100 scale. Aggregates mix accuracy, ROUGE-L, and
micro-F1 and are descriptive equal-task averages, not a shared metric.

Standalone script: the manuscript is not read at runtime.
Produces three PNGs: exp_task_learning_curves.png,
exp_task_comparison.png, and exp_task_ablation.png.
"""

from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator
import numpy as np


TASKS = ['MedCalc-Bench', 'DischargeMe', 'NoteAid-README', 'MedHallu', 'MIMIC-IV ICD']
STAGE_LABELS = ['MedCalc-Bench', 'DischargeMe', 'NoteAid-README', 'MedHallu', 'MIMIC-IV ICD']
TASK_METRICS = ['Accuracy (%)', 'ROUGE-L (0--100)', 'ROUGE-L (0--100)', 'Accuracy (%)', 'Micro-F1 (0--100)']
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
    'Zero-shot': np.array([5.7, 16.37, 13.89, 78.3, 0.91]),
    'Specialist': np.array([34.7, 30.39, 50.92, 97.3, 62.24]),
    'Multitask mixed': np.array([32.7, 26.99, 50.55, 97.7, 48.79]),
}

# Each method: rows are training stages; columns are evaluation tasks.
RESULTS = {
    'Sequential SFT': np.array([
        [38.1, 2.77, 24.07, 60.9, 0.03],  # After MedCalc-Bench
        [37.1, 30.39, 26.26, 71.4, 0.11],  # After DischargeMe
        [28.7, 14.41, 50.31, 52.0, 0.0],  # After NoteAid-README
        [2.8, 0.01, 0.0, 97.8, 0.0],  # After MedHallu
        [8.2, 0.36, 28.87, 96.7, 62.42],  # After MIMIC-IV ICD
    ]),
    'Replay': np.array([
        [33.1, 1.6, 20.17, 59.6, 0.0],  # After MedCalc-Bench
        [30.7, 28.11, 20.93, 60.7, 0.0],  # After DischargeMe
        [26.4, 25.51, 50.9, 53.3, 0.0],  # After NoteAid-README
        [22.5, 24.69, 46.98, 98.7, 0.0],  # After MedHallu
        [21.7, 24.94, 45.87, 97.5, 44.45],  # After MIMIC-IV ICD
    ]),
    'KD-LoRA': np.array([
        [32.4, 1.28, 23.82, 60.2, 0.04],  # After MedCalc-Bench
        [33.4, 22.23, 23.23, 62.8, 0.0],  # After DischargeMe
        [30.9, 14.07, 44.53, 57.8, 0.07],  # After NoteAid-README
        [11.3, 0.06, 8.5, 96.6, 0.0],  # After MedHallu
        [7.0, 0.13, 10.37, 96.6, 23.95],  # After MIMIC-IV ICD
    ]),
    'SPG': np.array([
        [33.9, 4.15, 21.24, 56.7, 0.11],  # After MedCalc-Bench
        [32.8, 28.24, 9.65, 57.2, 0.0],  # After DischargeMe
        [27.6, 11.53, 49.56, 49.3, 0.08],  # After NoteAid-README
        [2.7, 0.01, 0.0, 98.1, 0.0],  # After MedHallu
        [3.2, 0.56, 30.55, 96.8, 49.65],  # After MIMIC-IV ICD
    ]),
    'SAPT': np.array([
        [26.0, 0.16, 0.2, 26.1, 0.0],  # After MedCalc-Bench
        [21.2, 28.44, 21.24, 49.3, 0.0],  # After DischargeMe
        [18.8, 6.92, 51.9, 50.2, 0.03],  # After NoteAid-README
        [8.9, 22.67, 50.95, 98.3, 0.0],  # After MedHallu
        [24.4, 22.25, 50.02, 94.0, 55.41],  # After MIMIC-IV ICD
    ]),
    'MACL-curr': np.array([
        [27.4, 0.16, 0.2, 22.5, 0.0],  # After MedCalc-Bench
        [20.3, 28.53, 22.05, 50.3, 0.0],  # After DischargeMe
        [20.8, 8.46, 50.12, 52.8, 0.03],  # After NoteAid-README
        [23.9, 26.72, 50.05, 97.9, 0.0],  # After MedHallu
        [24.5, 23.55, 48.31, 97.2, 53.69],  # After MIMIC-IV ICD
    ]),
    'MACL-prev': np.array([
        [26.0, 0.16, 0.2, 26.1, 0.0],  # After MedCalc-Bench
        [19.9, 28.71, 20.26, 52.8, 0.04],  # After DischargeMe
        [22.3, 20.71, 51.55, 49.9, 0.0],  # After NoteAid-README
        [24.2, 27.34, 50.48, 98.2, 0.04],  # After MedHallu
        [23.8, 25.24, 50.16, 98.0, 53.66],  # After MIMIC-IV ICD
    ]),
    'MACL-both': np.array([
        [28.7, 0.12, 0.05, 33.0, 0.0],  # After MedCalc-Bench
        [23.6, 28.23, 21.39, 39.4, 0.0],  # After DischargeMe
        [19.8, 18.98, 50.55, 49.9, 0.0],  # After NoteAid-README
        [26.8, 27.02, 49.8, 97.6, 0.0],  # After MedHallu
        [24.3, 24.47, 50.03, 93.9, 53.36],  # After MIMIC-IV ICD
    ]),
}


def apply_plot_style():
    """Shared typography and axes styling for all three figures."""
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
def plot_exp_task(output_dir=None, methods=None, show_multitask_mixed=True):
    """Save a 1 x 5 grid of task-specific learning curves.

    The vertical line marks training on the panel's task. Points to its
    left evaluate transfer before training; points to its right show retention.
    Each panel uses limits rounded outward to multiples of 10. Zero-shot is a horizontal
    reference, rather than an additional training stage.
    """
    methods = list(MAIN_METHODS) if methods is None else list(methods)
    if not methods or any(method not in RESULTS for method in methods):
        raise ValueError('Select at least one method from RESULTS.')

    apply_plot_style()

    fig, axes = plt.subplots(1, 5, figsize=(45, 10), sharex=True, sharey=False)
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
    return [save_png(fig, output_dir, 'exp_task_learning_curves.png')]


def compute_aggregate_metrics(results):
    """Return equally weighted task averages, in percentage points.

    Final accuracy: last row, averaged over all 5 tasks.
    New-task accuracy: diagonal, immediately after learning each task.
    Seen-task accuracy: mean of stage-wise averages over learned tasks.
    Final forgetting: best post-acquisition accuracy minus final accuracy,
    averaged over the first 4 tasks (the final task has no later training).
    The maximum includes the final stage, so forgetting is nonnegative.
    """
    scores = np.asarray(results, dtype=float)
    if scores.shape != (len(TASKS), len(TASKS)):
        raise ValueError('Expected a 5 x 5 training-stage by task matrix.')
    forgetting = [scores[j:, j].max() - scores[-1, j]
                  for j in range(len(TASKS) - 1)]
    return {
        'final_accuracy': scores[-1].mean(),
        'new_task_accuracy': np.diag(scores).mean(),
        'seen_task_accuracy': np.mean([scores[t, :t + 1].mean()
                                       for t in range(len(TASKS))]),
        'final_forgetting': np.mean(forgetting),
    }


def plot_aggregate_bars(selected_methods, filename, output_dir=None):
    """One row of five panels, with equal task weighting and no error bars.

    Rank uses the selected methods plus Zero-shot, Specialist, and Multitask mixed; rank 1 is
    best and ties receive their average rank. Static references use their fixed
    task scores for seen-task and new-task accuracy, not a learning trajectory.
    Forgetting remains nonnegative and excludes the final task.
    """
    apply_plot_style()
    methods = [*selected_methods, *REFERENCE_STYLES]
    metrics = {method: compute_aggregate_metrics(RESULTS[method])
               for method in selected_methods}
    for name in REFERENCE_STYLES:
        fixed_scores = REFERENCE_SCORES[name]
        metrics[name] = {
            'final_accuracy': fixed_scores.mean(),
            'new_task_accuracy': fixed_scores.mean(),
            'seen_task_accuracy': np.mean([fixed_scores[:t + 1].mean()
                                          for t in range(len(TASKS))]),
        }

    final_scores = np.array([RESULTS[name][-1] if name in RESULTS
                             else REFERENCE_SCORES[name] for name in methods])
    for i, name in enumerate(methods):
        # Average tied rank = 1 + number strictly better + half of other ties.
        ranks = (1 + (final_scores > final_scores[i]).sum(axis=0)
                 + 0.5 * ((final_scores == final_scores[i]).sum(axis=0) - 1))
        metrics[name]['final_rank'] = ranks.mean()

    panels = [
        ('final_accuracy', 'Final average performance ' + r'$\uparrow$', 'Performance'),
        ('seen_task_accuracy', 'Average seen-task performance ' + r'$\uparrow$', 'Performance'),
        ('new_task_accuracy', 'Average new-task performance ' + r'$\uparrow$', 'Performance'),
        ('final_rank', 'Final average rank ' + r'$\downarrow$', 'Rank'),
        ('final_forgetting', 'Final average forgetting ' + r'$\downarrow$', r'$\Delta$ Score'),
    ]
    colors = {name: METHOD_STYLES[name]['color'] for name in selected_methods}
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
    handles.extend(Line2D([0], [0], label=name, linewidth=2.5, **style)
                   for name, style in REFERENCE_STYLES.items())
    fig.legend(handles=handles, loc='lower center', bbox_to_anchor=(0.5, 0.01),
               ncols=len(handles), fontsize=32, columnspacing=1.2, handlelength=1.5)
    fig.tight_layout(pad=2, rect=(0, 0.1, 1, 1))
    return save_png(fig, output_dir, filename)


# Figure 2: main-method comparison; ablation variants are excluded.
def plot_aggregate_comparison(output_dir=None):
    return plot_aggregate_bars(MAIN_METHODS, 'exp_task_comparison.png', output_dir)


# Figure 3: reward-branch ablation, with SAPT as the no-MACL baseline.
def plot_ablation(output_dir=None):
    """Rank is computed within this ablation plus the three static references.

    Consequently, rank values are not directly comparable to Figure 2 ranks.
    """
    return plot_aggregate_bars(ABLATION_METHODS, 'exp_task_ablation.png', output_dir)


def main():
    """Generate learning curves, main comparison, and reward ablation (PNG only)."""
    curve_paths = plot_exp_task()
    comparison_path = plot_aggregate_comparison()
    ablation_path = plot_ablation()
    for path in [*curve_paths, comparison_path, ablation_path]:
        print(f'Saved {path}')


if __name__ == '__main__':
    main()
