"""EXP-SUB: learning and retention across 12 MedMCQA disciplines.

Raw accuracy (%) copied from main_initial.tex (2026-11-10), Table medmcqa_disciplines.
Rows in each result array are training stages; columns are evaluation disciplines.
Single run: seed 1. MACL uses N=10 and total lambda=1 (equally split for
MACL-both). Replay retains K=500 examples per previous discipline.
The plotting script is standalone and does not read the manuscript at runtime.

Running this file produces three PNG figures:
1. exp_sub_learning_curves.png: per-discipline accuracy across training stages.
2. exp_sub_comparison.png: five aggregate metrics for the main methods.
3. exp_sub_ablation.png: the same metrics for SAPT and the three MACL variants.
"""

from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator
import numpy as np


DISCIPLINES = [
    'Medicine', 'Surgery', 'Pathology', 'Anatomy', 'Pharmacology',
    'Social & Preventive Medicine', 'Microbiology', 'Gynaecology & Obstetrics',
    'Physiology', 'Biochemistry', 'Pediatrics', 'Dental',
]
STAGE_LABELS = [
    'Med', 'Surg', 'Path', 'Anat', 'Pharm', 'SPM',
    'Micro', 'Gyn/Obs', 'Phys', 'Biochem', 'Ped', 'Dental',
]
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

# Static references, in DISCIPLINES order.
REFERENCE_SCORES = {
    'Zero-shot': np.array([49.15, 46.88, 54.3, 48.72, 60.08, 37.21, 49.18, 44.64, 49.71, 58.48, 51.28, 44.54]),
    'Specialist': np.array([66.44, 52.85, 67.95, 65.81, 74.49, 55.81, 61.48, 58.48, 61.4, 76.61, 70.51, 52.43]),
    'Multitask mixed': np.array([63.05, 56.1, 66.17, 63.68, 74.9, 53.49, 65.57, 59.82, 64.91, 69.01, 69.66, 49.01]),
}

# Each method: (12 training stages, 12 evaluation disciplines).
RESULTS = {
    'Sequential SFT': np.array([
        [63.73, 52.57, 66.17, 55.56, 69.14, 53.49, 63.11, 56.25, 61.99, 67.25, 69.23, 48.56],  # After Medicine
        [61.02, 52.57, 64.39, 51.28, 68.31, 48.84, 58.2, 54.91, 57.89, 65.5, 61.11, 46.05],  # After Surgery
        [57.29, 50.95, 65.88, 50.85, 68.31, 42.64, 61.48, 48.21, 54.39, 62.57, 57.69, 46.97],  # After Pathology
        [60.34, 52.85, 66.47, 63.25, 65.84, 44.96, 59.02, 53.57, 56.14, 61.99, 57.26, 45.68],  # After Anatomy
        [55.25, 47.97, 64.99, 55.98, 73.66, 47.29, 53.28, 50.89, 55.56, 60.23, 50.0, 44.84],  # After Pharmacology
        [53.56, 45.53, 60.53, 52.14, 67.08, 50.39, 55.74, 50.89, 57.89, 61.99, 47.86, 43.47],  # After SPM
        [47.8, 47.43, 62.91, 54.7, 67.08, 52.71, 56.56, 45.54, 55.56, 57.89, 51.28, 42.26],  # After Microbiology
        [51.19, 44.99, 58.16, 54.27, 65.84, 51.16, 59.02, 55.8, 53.22, 54.97, 52.99, 45.45],  # After Gyn/Obs
        [50.85, 47.15, 57.57, 51.28, 65.43, 48.06, 57.38, 52.68, 59.06, 61.99, 50.43, 43.47],  # After Physiology
        [50.51, 49.86, 56.97, 50.0, 67.49, 41.09, 49.18, 53.12, 53.8, 67.25, 47.44, 43.93],  # After Biochemistry
        [56.61, 47.43, 57.86, 49.57, 63.79, 44.96, 52.46, 52.68, 51.46, 66.67, 59.83, 44.08],  # After Pediatrics
        [48.81, 47.15, 60.53, 47.01, 62.14, 44.96, 48.36, 49.55, 55.56, 58.48, 49.15, 48.33],  # After Dental
    ]),
    'Replay': np.array([
        [66.78, 55.01, 65.58, 55.13, 71.6, 50.39, 68.85, 57.14, 57.31, 70.76, 66.24, 49.92],  # After Medicine
        [60.34, 51.49, 61.13, 52.14, 67.49, 48.84, 61.48, 50.45, 57.89, 64.33, 58.55, 46.13],  # After Surgery
        [61.36, 53.66, 67.36, 50.85, 67.49, 47.29, 60.66, 52.68, 53.22, 68.42, 57.26, 45.9],  # After Pathology
        [58.98, 51.49, 65.58, 62.82, 64.2, 44.19, 53.28, 43.75, 54.97, 64.33, 58.12, 44.16],  # After Anatomy
        [56.27, 50.14, 61.42, 55.13, 74.07, 49.61, 51.64, 53.12, 53.22, 63.74, 50.85, 45.3],  # After Pharmacology
        [54.24, 48.24, 61.13, 49.15, 62.96, 52.71, 45.9, 50.89, 56.14, 57.89, 50.0, 45.3],  # After SPM
        [52.88, 47.97, 59.05, 54.27, 61.73, 51.94, 61.48, 45.09, 52.63, 56.14, 54.27, 45.98],  # After Microbiology
        [49.83, 44.44, 55.49, 50.85, 57.2, 44.19, 54.92, 56.7, 49.12, 59.65, 52.56, 44.46],  # After Gyn/Obs
        [50.17, 44.72, 59.94, 52.14, 58.02, 41.09, 58.2, 53.57, 60.23, 63.74, 51.28, 42.41],  # After Physiology
        [52.88, 46.34, 56.68, 48.72, 58.85, 45.74, 50.0, 52.23, 53.22, 74.85, 53.85, 44.46],  # After Biochemistry
        [53.22, 44.44, 54.9, 48.29, 62.96, 51.94, 54.1, 46.43, 56.14, 66.08, 62.39, 42.94],  # After Pediatrics
        [47.46, 47.7, 56.97, 51.71, 60.49, 49.61, 50.82, 50.89, 55.56, 65.5, 55.98, 46.74],  # After Dental
    ]),
    'KD-LoRA': np.array([
        [66.44, 50.68, 62.31, 54.27, 72.02, 52.71, 61.48, 55.36, 60.23, 70.18, 65.38, 48.41],  # After Medicine
        [62.37, 54.2, 62.61, 60.26, 71.19, 53.49, 62.3, 51.34, 56.73, 66.08, 67.95, 50.61],  # After Surgery
        [63.05, 52.85, 67.06, 52.99, 70.37, 51.94, 56.56, 53.57, 53.8, 67.84, 63.68, 49.54],  # After Pathology
        [62.37, 52.57, 69.44, 62.82, 67.08, 49.61, 60.66, 51.34, 54.97, 64.33, 59.4, 48.71],  # After Anatomy
        [58.98, 51.49, 67.36, 59.4, 72.43, 50.39, 60.66, 54.91, 57.31, 64.91, 60.26, 49.92],  # After Pharmacology
        [56.61, 52.85, 65.88, 55.98, 68.72, 55.04, 57.38, 52.68, 59.65, 67.25, 55.98, 48.1],  # After SPM
        [58.64, 48.51, 63.2, 53.85, 66.67, 50.39, 58.2, 50.0, 52.05, 63.16, 54.27, 46.81],  # After Microbiology
        [53.9, 47.15, 64.39, 51.28, 66.26, 46.51, 59.84, 62.05, 51.46, 61.4, 55.56, 46.89],  # After Gyn/Obs
        [53.9, 48.24, 62.31, 50.85, 65.43, 48.06, 60.66, 56.25, 57.31, 59.65, 53.85, 45.52],  # After Physiology
        [54.24, 52.03, 59.35, 53.42, 67.08, 52.71, 56.56, 51.34, 55.56, 70.18, 52.99, 44.61],  # After Biochemistry
        [53.56, 48.24, 62.61, 52.99, 66.26, 46.51, 54.1, 51.79, 52.63, 65.5, 59.83, 47.04],  # After Pediatrics
        [53.22, 50.14, 62.31, 52.99, 59.26, 46.51, 54.1, 47.32, 53.22, 60.23, 51.71, 49.62],  # After Dental
    ]),
    'SPG': np.array([
        [64.07, 53.39, 67.36, 58.55, 71.19, 53.49, 66.39, 53.12, 54.39, 72.51, 65.38, 50.0],  # After Medicine
        [61.36, 52.03, 64.69, 52.14, 67.9, 51.94, 58.2, 50.45, 57.89, 63.74, 61.97, 47.42],  # After Surgery
        [59.32, 52.57, 70.33, 52.14, 65.43, 46.51, 56.56, 42.86, 54.39, 68.42, 58.12, 45.37],  # After Pathology
        [58.64, 48.24, 61.72, 62.82, 65.02, 43.41, 51.64, 47.77, 55.56, 57.89, 54.27, 44.84],  # After Anatomy
        [56.95, 49.59, 58.16, 57.26, 72.02, 44.96, 55.74, 46.88, 52.63, 53.22, 50.43, 42.79],  # After Pharmacology
        [53.22, 41.73, 55.49, 52.14, 65.02, 51.94, 57.38, 47.32, 54.39, 53.22, 50.43, 43.25],  # After SPM
        [48.81, 42.28, 57.27, 53.42, 61.73, 48.84, 65.57, 44.2, 56.14, 54.97, 50.85, 42.87],  # After Microbiology
        [49.83, 43.63, 55.79, 46.15, 60.49, 48.06, 59.84, 55.8, 47.95, 54.97, 45.73, 42.64],  # After Gyn/Obs
        [51.19, 43.63, 55.79, 47.86, 58.85, 51.16, 53.28, 51.79, 62.57, 56.14, 48.72, 39.15],  # After Physiology
        [49.49, 45.8, 55.49, 43.16, 60.91, 49.61, 54.1, 45.98, 52.63, 67.84, 49.15, 42.41],  # After Biochemistry
        [54.58, 44.44, 53.12, 44.44, 58.85, 44.19, 48.36, 50.45, 50.29, 59.65, 57.26, 39.68],  # After Pediatrics
        [48.81, 42.82, 52.82, 52.14, 49.79, 46.51, 48.36, 47.32, 55.56, 60.23, 47.01, 45.22],  # After Dental
    ]),
    'SAPT': np.array([
        [61.69, 55.28, 65.28, 54.27, 68.31, 51.94, 59.84, 52.68, 59.06, 67.84, 62.82, 46.59],  # After Medicine
        [56.95, 58.81, 66.17, 55.56, 70.78, 52.71, 62.3, 55.8, 59.06, 63.74, 62.39, 47.5],  # After Surgery
        [63.73, 56.1, 66.77, 57.69, 71.6, 52.71, 66.39, 59.38, 59.65, 64.33, 63.25, 48.1],  # After Pathology
        [58.98, 55.28, 63.8, 64.53, 67.9, 57.36, 65.57, 58.48, 61.99, 71.35, 62.82, 47.95],  # After Anatomy
        [62.03, 56.64, 67.95, 63.68, 73.25, 51.94, 67.21, 53.57, 60.82, 69.01, 66.67, 49.39],  # After Pharmacology
        [63.39, 56.64, 65.88, 57.69, 72.02, 53.49, 63.11, 53.12, 59.06, 69.59, 63.68, 47.57],  # After SPM
        [59.66, 56.91, 67.06, 54.27, 63.37, 55.81, 61.48, 59.38, 61.99, 66.08, 61.11, 46.43],  # After Microbiology
        [64.07, 57.99, 67.06, 61.11, 71.19, 55.04, 63.11, 59.38, 60.23, 68.42, 64.96, 48.1],  # After Gyn/Obs
        [63.05, 54.74, 67.66, 58.97, 71.19, 51.94, 61.48, 56.7, 62.57, 69.59, 65.81, 49.85],  # After Physiology
        [64.75, 56.64, 69.14, 63.68, 74.9, 52.71, 67.21, 58.48, 60.82, 70.76, 65.81, 50.38],  # After Biochemistry
        [60.0, 54.74, 63.5, 59.4, 72.84, 51.94, 64.75, 58.48, 60.82, 66.67, 67.09, 48.03],  # After Pediatrics
        [62.37, 56.64, 66.77, 64.53, 72.43, 53.49, 67.21, 58.04, 60.23, 68.42, 69.66, 50.76],  # After Dental
    ]),
    'MACL-curr': np.array([
        [61.69, 54.47, 65.88, 54.27, 64.61, 48.06, 59.02, 57.14, 56.73, 66.08, 61.11, 46.05],  # After Medicine
        [62.03, 55.28, 65.88, 55.13, 64.61, 48.06, 57.38, 58.04, 57.31, 67.84, 61.11, 45.9],  # After Surgery
        [62.37, 50.68, 69.44, 56.41, 70.37, 51.94, 63.11, 54.91, 59.65, 67.84, 64.53, 46.97],  # After Pathology
        [62.03, 54.47, 66.17, 61.54, 69.55, 48.06, 63.11, 55.8, 61.4, 72.51, 64.1, 49.39],  # After Anatomy
        [61.69, 55.83, 64.09, 57.26, 71.6, 47.29, 67.21, 57.59, 59.65, 66.08, 63.68, 48.25],  # After Pharmacology
        [59.32, 55.56, 63.5, 58.12, 74.49, 51.16, 63.93, 58.93, 58.48, 69.01, 62.39, 51.29],  # After SPM
        [63.39, 55.83, 66.17, 61.54, 69.55, 55.81, 61.48, 58.04, 58.48, 71.93, 65.38, 48.48],  # After Microbiology
        [65.42, 57.99, 67.36, 60.26, 72.02, 50.39, 63.11, 59.82, 64.33, 69.01, 68.8, 50.15],  # After Gyn/Obs
        [62.71, 55.01, 69.73, 61.54, 70.78, 51.94, 63.93, 55.36, 60.23, 69.59, 67.09, 49.92],  # After Physiology
        [63.39, 55.56, 68.84, 61.54, 72.02, 49.61, 64.75, 56.7, 58.48, 70.76, 65.38, 50.53],  # After Biochemistry
        [62.71, 55.83, 69.14, 59.83, 73.25, 49.61, 64.75, 61.61, 61.99, 70.18, 66.24, 49.17],  # After Pediatrics
        [65.08, 54.2, 69.44, 64.1, 74.9, 55.81, 65.57, 60.27, 60.23, 74.85, 65.81, 51.21],  # After Dental
    ]),
    'MACL-prev': np.array([
        [61.69, 55.28, 64.99, 54.27, 68.31, 51.16, 59.84, 52.68, 59.65, 67.84, 62.82, 46.51],  # After Medicine
        [61.36, 59.08, 64.69, 56.41, 69.55, 51.16, 62.3, 56.25, 60.82, 62.57, 61.97, 47.72],  # After Surgery
        [63.05, 55.83, 65.58, 56.84, 74.9, 50.39, 69.67, 55.8, 59.06, 67.84, 64.96, 48.25],  # After Pathology
        [61.69, 55.56, 68.84, 66.67, 69.96, 48.84, 64.75, 57.14, 61.99, 69.59, 64.96, 49.39],  # After Anatomy
        [62.71, 57.45, 67.06, 58.55, 72.43, 51.16, 64.75, 54.02, 58.48, 66.67, 64.1, 49.24],  # After Pharmacology
        [59.32, 55.56, 65.88, 58.97, 72.43, 50.39, 62.3, 52.68, 60.82, 71.35, 60.26, 46.89],  # After SPM
        [62.37, 54.47, 66.47, 60.26, 69.55, 52.71, 61.48, 54.02, 60.23, 65.5, 65.81, 49.54],  # After Microbiology
        [63.39, 58.27, 67.36, 60.68, 72.84, 55.81, 60.66, 57.59, 60.82, 67.25, 67.09, 48.56],  # After Gyn/Obs
        [65.42, 56.1, 68.55, 61.97, 71.19, 47.29, 63.11, 54.02, 61.4, 70.18, 66.67, 51.21],  # After Physiology
        [60.34, 57.45, 69.44, 61.97, 74.49, 51.16, 60.66, 53.12, 62.57, 73.1, 63.68, 49.24],  # After Biochemistry
        [63.73, 58.54, 67.06, 61.54, 72.43, 51.94, 62.3, 58.93, 60.82, 69.59, 64.96, 50.99],  # After Pediatrics
        [63.05, 58.81, 66.47, 64.53, 74.9, 58.14, 64.75, 60.71, 63.16, 69.59, 67.09, 51.37],  # After Dental
    ]),
    'MACL-both': np.array([
        [59.32, 52.3, 65.28, 54.7, 65.43, 53.49, 59.02, 57.59, 59.06, 66.08, 59.4, 46.66],  # After Medicine
        [61.02, 55.56, 64.39, 56.41, 72.43, 51.94, 59.84, 58.04, 59.65, 63.74, 63.25, 46.97],  # After Surgery
        [63.39, 56.64, 63.5, 62.82, 70.78, 49.61, 63.93, 56.25, 59.06, 69.01, 64.53, 46.97],  # After Pathology
        [59.32, 55.01, 64.69, 62.82, 68.72, 55.04, 63.11, 55.8, 59.65, 70.76, 64.53, 48.94],  # After Anatomy
        [61.36, 57.72, 64.39, 57.26, 75.72, 52.71, 65.57, 55.36, 59.06, 71.35, 67.52, 49.01],  # After Pharmacology
        [58.31, 55.01, 63.2, 57.26, 72.84, 55.04, 57.38, 51.34, 57.89, 69.01, 59.4, 47.57],  # After SPM
        [64.41, 56.91, 66.17, 60.68, 71.6, 58.91, 65.57, 56.7, 59.65, 66.67, 65.81, 48.48],  # After Microbiology
        [65.76, 58.81, 67.36, 64.1, 73.66, 50.39, 68.03, 58.93, 59.06, 71.93, 66.24, 50.91],  # After Gyn/Obs
        [62.71, 54.74, 68.55, 61.11, 72.43, 51.94, 64.75, 56.7, 63.16, 70.76, 67.95, 50.38],  # After Physiology
        [62.03, 57.72, 67.66, 63.25, 73.25, 55.81, 59.02, 54.91, 62.57, 73.68, 62.82, 47.72],  # After Biochemistry
        [64.07, 56.37, 64.39, 60.26, 74.49, 51.16, 65.57, 58.48, 61.4, 66.08, 67.52, 50.91],  # After Pediatrics
        [64.41, 57.72, 70.03, 67.52, 74.07, 54.26, 68.03, 58.04, 57.89, 73.1, 65.81, 51.59],  # After Dental
    ]),
}


def apply_plot_style():
    """Shared typography and axes styling for both figures."""
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
def plot_exp_sub(output_dir=None, methods=None, show_multitask_mixed=True):
    """Save a 2 x 6 grid; optionally select methods or add Multitask mixed.

    The vertical line marks training on the panel's discipline. Points to its
    left evaluate transfer before training; points to its right show retention.
    Each panel uses limits rounded outward to multiples of 10. Zero-shot is a horizontal
    reference, rather than an additional training stage.
    """
    methods = list(MAIN_METHODS) if methods is None else list(methods)
    if not methods or any(method not in RESULTS for method in methods):
        raise ValueError('Select at least one method from RESULTS.')

    apply_plot_style()

    fig, axes = plt.subplots(2, 6, figsize=(45, 15), sharex=True, sharey=False)
    stages = np.arange(1, len(DISCIPLINES) + 1)
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
        title = DISCIPLINES[task_idx]
        ax.set_title(title, fontsize=32, pad=14)
        ax.set_xlim(0.65, 12.35)
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
        if task_idx % 6 == 0:
            ax.set_ylabel('Accuracy (%)', fontsize=32, labelpad=12)
        if task_idx // 6 == 1:
            ax.set_xlabel('Training stage', fontsize=32, labelpad=16)

    handles = [Line2D([0], [0], label=METHOD_LABELS.get(method, method), linewidth=5,
                      markersize=14, **METHOD_STYLES[method]) for method in methods]
    handles.extend(Line2D([0], [0], label=name, linewidth=5, **style)
                   for name, style in references.items())
    fig.legend(handles=handles, loc='lower center', bbox_to_anchor=(0.5, 0.005),
               ncols=len(handles), fontsize=32, columnspacing=1.2, handlelength=2.5)
    fig.tight_layout(pad=2, rect=(0, 0.06, 1, 1))
    return [save_png(fig, output_dir, 'exp_sub_learning_curves.png')]


def compute_aggregate_metrics(results):
    """Return equally weighted discipline averages, in percentage points.

    Final accuracy: last row, averaged over all 12 disciplines.
    New-task accuracy: diagonal, immediately after learning each discipline.
    Seen-task accuracy: mean of stage-wise averages over learned disciplines.
    Final forgetting: best post-acquisition accuracy minus final accuracy,
    averaged over the first 11 disciplines (Dental has no later training).
    The maximum includes the final stage, so forgetting is nonnegative.
    """
    scores = np.asarray(results, dtype=float)
    if scores.shape != (len(DISCIPLINES), len(DISCIPLINES)):
        raise ValueError('Expected a 12 x 12 training-stage by discipline matrix.')
    forgetting = [scores[j:, j].max() - scores[-1, j]
                  for j in range(len(DISCIPLINES) - 1)]
    return {
        'final_accuracy': scores[-1].mean(),
        'new_task_accuracy': np.diag(scores).mean(),
        'seen_task_accuracy': np.mean([scores[t, :t + 1].mean()
                                       for t in range(len(DISCIPLINES))]),
        'final_forgetting': np.mean(forgetting),
    }


def plot_aggregate_bars(selected_methods, filename, output_dir=None):
    """One row of five panels, with equal task weighting and no error bars.

    Rank uses the selected methods plus Zero-shot, Specialist, and Multitask mixed; rank 1 is
    best and ties receive their average rank. Static references use their fixed
    task scores for seen-task and new-task accuracy, not a learning trajectory.
    Forgetting remains nonnegative and excludes the final discipline.
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
                                          for t in range(len(DISCIPLINES))]),
        }

    final_scores = np.array([RESULTS[name][-1] if name in RESULTS
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
    return plot_aggregate_bars(MAIN_METHODS, 'exp_sub_comparison.png', output_dir)


# Figure 3: reward-branch ablation, with SAPT as the no-MACL baseline.
def plot_ablation(output_dir=None):
    """Rank is computed within this ablation plus the three static references.

    Consequently, rank values are not directly comparable to Figure 2 ranks.
    """
    return plot_aggregate_bars(ABLATION_METHODS, 'exp_sub_ablation.png', output_dir)


def main():
    """Generate learning curves, main comparison, and reward ablation (PNG only)."""
    curve_paths = plot_exp_sub()
    comparison_path = plot_aggregate_comparison()
    ablation_path = plot_ablation()
    for path in [*curve_paths, comparison_path, ablation_path]:
        print(f'Saved {path}')


if __name__ == '__main__':
    main()
