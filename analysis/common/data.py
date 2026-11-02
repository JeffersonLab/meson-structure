"""Small shared numerical helpers."""
from __future__ import annotations
import numpy as np

def finite(values):
    """Return finite float values from an iterable, array or generator."""
    array = np.asarray(list(values) if not isinstance(values, (list, tuple, np.ndarray)) else values, dtype=float)
    return array[np.isfinite(array)]

def percent_weights(values):
    """Weights with total 100 percent; return None for empty input."""
    size = len(values)
    return np.full(size, 100.0 / size) if size else None
