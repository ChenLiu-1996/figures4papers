"""Synthetic multi-class classification results for the confusion-matrix demo.

Counts are invented for illustration only; they are not from a real paper.
The "proposed" model is intentionally stronger on the diagonal than the baseline.
"""

CLASS_NAMES = ["Healthy", "Type I", "Type II", "Type III", "Other"]

# Rows = true class, columns = predicted class.
BASELINE_COUNTS = [
    [118, 14, 8, 6, 4],
    [16, 92, 18, 9, 5],
    [9, 21, 84, 17, 9],
    [7, 11, 19, 78, 15],
    [12, 8, 11, 16, 73],
]

PROPOSED_COUNTS = [
    [136, 7, 4, 2, 1],
    [6, 118, 9, 4, 3],
    [3, 8, 121, 7, 5],
    [2, 4, 8, 116, 10],
    [4, 3, 5, 9, 119],
]
