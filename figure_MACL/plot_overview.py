"""Separate Figure 1 B and D retention panels using the scenario plot styles.

At distance d, average R[k+d,k] - R[k,k] over the T-d available tasks.
The task cohort shrinks with distance; no additional normalization is applied.
"""
from pathlib import Path
import importlib.util
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

SCENARIOS = [('sub', 'Medical subdisciplines'),
             ('qa', 'Medical QA datasets'),
             ('task', 'Heterogeneous medical tasks')]
ALL_METHODS = ['Sequential SFT', 'Replay', 'MACL-prev']


def load_scenarios(directory):
    scenarios = []
    for tag, title in SCENARIOS:
        spec = importlib.util.spec_from_file_location('exp_' + tag, directory / f'plot_exp_{tag}.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        scenarios.append((title, module))
    return scenarios


def retention_curve(matrix):
    scores = np.asarray(matrix, dtype=float)
    n = len(scores)
    if scores.shape != (n, n):
        raise ValueError('Expected a square training-stage by task matrix.')
    return np.array([(np.diag(scores, k=-d) - np.diag(scores)[:n-d]).mean()
                     for d in range(n)])


def plot_panel(scenarios, methods, filename, output_dir=None):
    style_source = scenarios[0][1]
    style_source.apply_plot_style()
    method_styles = {name: dict(style_source.METHOD_STYLES[name]) for name in ALL_METHODS}
    method_styles['Sequential SFT']['color'] = '#666666'
    method_styles['Sequential SFT']['linestyle'] = (0, (6, 3))
    method_styles['Replay']['color'] = '#2E8B57'
    fig, axes = plt.subplots(1, 3, figsize=(27, 10), sharex=False, sharey=False)
    for index, (ax, (title, module)) in enumerate(zip(axes, scenarios)):
        curves = {name: retention_curve(module.RESULTS[name]) for name in ALL_METHODS}
        n = len(curves[ALL_METHODS[0]])
        stages = np.arange(n)
        ax.axhline(0, linewidth=1.8, alpha=0.85, zorder=1,
                   **style_source.REFERENCE_STYLES['Zero-shot'])
        for method in methods:
            scores = module.RESULTS[method]
            for task_index in range(n):
                task_curve = scores[task_index:, task_index] - scores[task_index, task_index]
                ax.plot(np.arange(len(task_curve)), task_curve,
                        color=method_styles[method]['color'],
                        linestyle='-', linewidth=2.2, alpha=0.2,
                        marker=None, zorder=2, label='_nolegend_')
            ax.plot(stages, curves[method], linewidth=5, markersize=14,
                    alpha=1.0, label=method, zorder=3,
                    **method_styles[method])
        ax.set_title(title, fontsize=36, pad=18)
        ax.set_xlim(-0.35, n - 1 + 0.35)
        # Shared display range for all six subplots across panels B and D.
        ax.set_ylim(-50, 10)
        ax.set_yticks(np.arange(-50, 11, 10))
        ax.set_xticks(stages)
        ax.set_xticklabels(stages, fontsize=30)
        ax.tick_params(labelsize=30, length=10, width=2.5)
        if index == 0:
            ax.set_ylabel(r'$\Delta$ Performance', fontsize=40, labelpad=16)
        ax.set_xlabel('Tasks learned', fontsize=40, labelpad=16)
        handles = [Line2D([0], [0], label=('MACL' if method == 'MACL-prev' else method), linewidth=5, markersize=14,
                          alpha=1.0, **method_styles[method]) for method in methods]
        for handle, method in zip(handles, methods):
            if method == 'Sequential SFT':
                handle.set_linestyle((0, (2, 2)))
        ax.legend(handles=handles, loc='lower left', fontsize=30,
                  columnspacing=1.2, handlelength=2.5)
    fig.tight_layout(pad=2, rect=(0, 0, 1, 1))
    return style_source.save_png(fig, output_dir, filename)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parent / 'figures')
    args = parser.parse_args()
    scenarios = load_scenarios(args.data_dir)
    print(plot_panel(scenarios, ALL_METHODS[:2], 'overview_panel_b.png', args.output_dir))
    print(plot_panel(scenarios, ALL_METHODS[2:], 'overview_panel_d.png', args.output_dir))


if __name__ == '__main__':
    main()
