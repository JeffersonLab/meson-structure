from __future__ import annotations

from pathlib import Path
from typing import Any, Final

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

from config import PATHS
from utils import Grid

from typing import Literal

# =============================================================================
# Plot style registry
# =============================================================================

Scale = Literal["lin", "log"]

COLORS: Final[dict[str, str]] = {
    "geant4": "orange",
    "reco": "tab:blue",
    "afterburner": "black",
}

STYLES: Final[dict[str, dict[str, Any]]] = {
    "geant4": {"linestyle": "-", "linewidth": 2.0},
    "reco": {"linestyle": "-", "linewidth": 2.5},
    "afterburner": {"linestyle": "--", "linewidth": 2.0},
}


def get_color(which: str) -> str:
    try:
        return COLORS[which]
    except KeyError as e:
        raise KeyError(f"Unknown color key '{which}'. Available: {sorted(COLORS)}") from e


def get_style(which: str) -> dict[str, Any]:
    # styles are optional; unknown keys just return empty style dict
    return dict(STYLES.get(which, {}))


# =============================================================================
# Global Matplotlib style
# =============================================================================

def apply_mpl_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["DejaVu Serif"],
            "mathtext.fontset": "dejavuserif",
            "axes.unicode_minus": False,
        }
    )


# =============================================================================
# File helpers
# =============================================================================

def ensure_outdir(outdir: str | Path) -> Path:
    p = Path(outdir)
    p.mkdir(parents=True, exist_ok=True)
    return p


def savefig(fig: mpl.figure.Figure, path: str | Path, dpi: int = 300) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(p, dpi=dpi)
    plt.close(fig)
    return p


# =============================================================================
# Plots
# =============================================================================

def plot_relerr_map(
    Z: np.ndarray,
    x_edges: np.ndarray,
    y_edges: np.ndarray,
    xlabel: str,
    ylabel: str,
    cbarlabel: str,
    title: str,
    outpath: str | Path,
    *,
    log_y: bool = False,
    log_x: bool = False,
    log_z: bool = False,
    vmax_percent: float | None = None
) -> Path:
    """
    Plot a relative statistical uncertainty map (in percent).
    NOTE: expects Z to be shaped like (nx, ny) and will plot Z.T to match edges.
    """
    fig, ax = plt.subplots(figsize=(6, 5))

    Zm = np.ma.masked_invalid(Z)
    Zm = np.ma.masked_where(Zm < 0, Zm)

    if log_z:
        norm = LogNorm(vmin=np.nanmin(Zm), vmax=np.nanmax(Zm))
        pcm = ax.pcolormesh(x_edges, y_edges, Zm.T, shading="auto", cmap="coolwarm", norm=norm)
        if vmax_percent is not None:
            pcm.set_clim(vmin=1.0, vmax=float(vmax_percent))

    else:
        pcm = ax.pcolormesh(x_edges, y_edges, Zm.T, shading="auto", cmap="coolwarm")
        if vmax_percent is not None:
            pcm.set_clim(vmin=0.0, vmax=float(vmax_percent))

    cb = fig.colorbar(pcm, ax=ax)
    cb.set_label(cbarlabel)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if log_y:
        ax.set_yscale("log")

    if log_x:
        ax.set_xscale("log")

    ax.set_title(title)
    fig.tight_layout()
    return savefig(fig, outpath, dpi=300)


def plot_F2_map(
    prefix: str,
    grid: Grid,
    F2: np.ndarray,
    title: str,
    cbar_label: str,
    *,
    xscale: Scale = "lin",
    q2scale: Scale = "lin",
    dpi: int = 220,
) -> Path:
    """
    Plot F2 on (x, Q2) edges stored in Grid and save into PATHS.outputs.
    """
    fig, ax = plt.subplots(figsize=(6.6, 5.6))

    pcm = ax.pcolormesh(grid.x_edges, grid.q2_edges, F2, shading="auto", cmap="viridis")
    cbar = fig.colorbar(pcm, ax=ax)
    cbar.set_label(cbar_label)

    ax.set_xlabel(r"$x_K$")
    ax.set_ylabel(r"$Q^2$ (GeV$^2$)")
    ax.set_title(title)

    if xscale == "log":
        ax.set_xscale("log")
        ax.set_xlim(0.1,1)

    if q2scale == "log":
        ax.set_yscale("log")

    fig.tight_layout()

    out_png = PATHS.outputs / f"{prefix}.png"
    return savefig(fig, out_png, dpi=dpi)

def plot_fischer_matrix_maps(
    *,
    info_aa: np.ndarray,
    info_ab: np.ndarray,
    info_bb: np.ndarray,
    xK_range: tuple[float, float] = (0.0, 1.0),
    xK_bins: int = 10,
    Q2_range: tuple[float, float] = (1.0, 500.0),
    Q2_bins: int = 10,
    log_Q2: bool = True,
    outdir: str | Path = "./outputs",
    outname: str = "fischer_matrix_maps.png",
    title: str | None = None,
):
    """
    Plot Fisher information density maps arranged as a 2x2 matrix:

        [ f_aa   f_ab ]
        [ f_ba   f_bb ]

    where each element is a map in (xK, Q2).
    """

    apply_mpl_style()
    outdir = ensure_outdir(outdir)

    info_ba = info_ab

    xK_edges = np.linspace(xK_range[0], xK_range[1], xK_bins + 1)

    if log_Q2:
        Q2_edges = np.logspace(np.log10(Q2_range[0]), np.log10(Q2_range[1]), Q2_bins + 1)
    else:
        Q2_edges = np.linspace(Q2_range[0], Q2_range[1], Q2_bins + 1)

    fig, axes = plt.subplots(2, 2, figsize=(9, 8), constrained_layout=True)

    panels = [
        (axes[0,0], info_aa, r"$f_{aa}(x_K,Q^2)$", "viridis"),
        (axes[0,1], info_ab, r"$f_{ab}(x_K,Q^2)$", "viridis"),
        (axes[1,0], info_ba, r"$f_{ba}(x_K,Q^2)$", "viridis"),
        (axes[1,1], info_bb, r"$f_{bb}(x_K,Q^2)$", "viridis"),
    ]

    for ax, z, lab, cmap in panels:

        m = ax.pcolormesh(
            xK_edges,
            Q2_edges,
            z.T,
            shading="auto",
            cmap=cmap,
            vmin=np.nanmin(z),
            vmax=np.nanmax(z),
        )

        cb = fig.colorbar(m, ax=ax)
        cb.set_label("Local Fisher information")

        ax.set_xlabel(r"$x_K$")
        ax.set_ylabel(r"$Q^2$ (GeV$^2$)")
        ax.set_title(lab)

        if log_Q2:
            ax.set_yscale("log")

    if title is not None:
        fig.suptitle(title)

    outpath = Path(outdir) / outname
    savefig(fig, outpath, dpi=200)

    return outpath