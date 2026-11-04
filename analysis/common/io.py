"""Shared tabular output helpers. Detector-specific ROOT schemas stay local."""
from __future__ import annotations
import csv
from pathlib import Path
from collections.abc import Iterable, Mapping, Sequence

def write_csv_rows(path: str | Path, rows: Iterable[Mapping], columns: Sequence[str]) -> None:
    """Write dictionaries to CSV, creating parent directories if necessary."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)
