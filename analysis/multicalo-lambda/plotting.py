from __future__ import annotations
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt


def apply_mpl_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["DejaVu Serif"],
            "mathtext.fontset": "dejavuserif",
            "axes.unicode_minus": False,
        }
    )


def ensure_outdir(outdir: str | Path) -> Path:
    p = Path(outdir)
    p.mkdir(parents=True, exist_ok=True)
    return p


def savefig(fig, path: str | Path, dpi: int = 300) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(p, dpi=dpi)
    plt.close(fig)
    return p