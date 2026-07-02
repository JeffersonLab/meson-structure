from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, TYPE_CHECKING

import numpy as np
import awkward as ak
import uproot
import math

from config import CONST
from physics import ToyParams, toy_norm, toy_shape_x

if TYPE_CHECKING:
    from config import PhysicsConstants


# =============================================================================
# Files helpers
# =============================================================================

def iter_reco_files(beam: str, nfiles: int, root_base_dir: Path, suffix: str) -> Iterable[Path]:
    """
    Yield existing non-empty ROOT files following your naming convention.
    """
    for i in range(1, nfiles + 1):
        fpath = root_base_dir / f"k_lambda_{beam}_5000evt_{i:03d}_{suffix}.root"
        if not fpath.exists() or fpath.stat().st_size == 0:
            continue
        yield fpath


# =============================================================================
# ROOT readers
# =============================================================================

def read_lambda_eicrecon(
    beam: str,
    nfiles: int,
    root_base_dir: Path,
    suffix: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Read reconstructed Lambda from ReconstructedFarForwardLambdas.
    Returns: E [GeV], cos(theta), sin(phi)
    """
    e_branch = "ReconstructedFarForwardLambdas.energy"
    px_branch = "ReconstructedFarForwardLambdas.momentum.x"
    py_branch = "ReconstructedFarForwardLambdas.momentum.y"
    pz_branch = "ReconstructedFarForwardLambdas.momentum.z"

    E_list: list[np.ndarray] = []
    cos_list: list[np.ndarray] = []
    sinphi_list: list[np.ndarray] = []

    for fpath in iter_reco_files(beam, nfiles, root_base_dir, suffix):
        try:
            with uproot.open(fpath) as f:
                tree = f["events"]
                arr = tree.arrays([e_branch, px_branch, py_branch, pz_branch], how=dict)

                E = ak.to_numpy(ak.flatten(arr[e_branch]))
                px = ak.to_numpy(ak.flatten(arr[px_branch]))
                py = ak.to_numpy(ak.flatten(arr[py_branch]))
                pz = ak.to_numpy(ak.flatten(arr[pz_branch]))

                if E.size == 0:
                    continue

                p = np.sqrt(px * px + py * py + pz * pz)
                m = p > 1e-12
                if not np.any(m):
                    continue

                E = E[m]
                px = px[m]
                py = py[m]
                pz = pz[m]
                p = p[m]

                cos_theta = pz / p
                phi = np.arctan2(py, px)
                sin_phi = np.sin(phi)

                E_list.append(E)
                cos_list.append(cos_theta)
                sinphi_list.append(sin_phi)

        except Exception as e:
            print(f"[read_lambda_eicrecon] Warning {fpath.name}: {e}")

    E_out = np.concatenate(E_list) if E_list else np.array([], dtype=np.float64)
    cos_out = np.concatenate(cos_list) if cos_list else np.array([], dtype=np.float64)
    sinphi_out = np.concatenate(sinphi_list) if sinphi_list else np.array([], dtype=np.float64)
    return E_out, cos_out, sinphi_out


def read_lambda_geant4(
    beam: str,
    nfiles: int,
    root_base_dir: Path,
    suffix: str,
    c: "PhysicsConstants" = CONST,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Read truth Lambda from MCParticles.
    Returns: E [GeV], cos(theta), sin(phi)
    """
    branches = [
        "MCParticles.PDG",
        "MCParticles.momentum.x",
        "MCParticles.momentum.y",
        "MCParticles.momentum.z",
    ]

    E_list: list[np.ndarray] = []
    cos_list: list[np.ndarray] = []
    sinphi_list: list[np.ndarray] = []

    for fpath in iter_reco_files(beam, nfiles, root_base_dir, suffix):
        try:
            with uproot.open(fpath) as f:
                tree = f["events"]
                arr = tree.arrays(branches, how=dict)

                pdg = arr["MCParticles.PDG"]
                px = arr["MCParticles.momentum.x"]
                py = arr["MCParticles.momentum.y"]
                pz = arr["MCParticles.momentum.z"]

                p2 = px * px + py * py + pz * pz
                p = np.sqrt(p2)

                mask = (pdg == c.pid_lambda) & (p > 1e-12)
                if not ak.any(mask):
                    continue

                px = px[mask]
                py = py[mask]
                pz = pz[mask]
                p = p[mask]

                cos_theta = pz / p
                phi = np.arctan2(py, px)
                sin_phi = np.sin(phi)
                E = np.sqrt(p * p + (c.m_lambda_gev ** 2))

                E_list.append(ak.to_numpy(ak.flatten(E)))
                cos_list.append(ak.to_numpy(ak.flatten(cos_theta)))
                sinphi_list.append(ak.to_numpy(ak.flatten(sin_phi)))

        except Exception as e:
            print(f"[read_lambda_geant4] Warning {fpath.name}: {e}")

    E_out = np.concatenate(E_list) if E_list else np.array([], dtype=np.float64)
    cos_out = np.concatenate(cos_list) if cos_list else np.array([], dtype=np.float64)
    sinphi_out = np.concatenate(sinphi_list) if sinphi_list else np.array([], dtype=np.float64)
    return E_out, cos_out, sinphi_out


# =============================================================================
# Afterburner reader (HepMC3 ASCII)
# =============================================================================

def read_lambda_afterburner(
    beam: str,
    nfiles: int,
    pattern: str,
    pid: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Read Lambda from HepMC v3 afterburner file.
    Returns: E [GeV], cos(theta), sin(phi)
    """
    E_list: list[np.ndarray] = []
    cos_list: list[np.ndarray] = []
    sinphi_list: list[np.ndarray] = []

    for i in range(1, nfiles + 1):
        hepmc_path = Path(pattern.format(beam=beam, idx=i))
        if not hepmc_path.exists():
            continue

        E, px, py, pz = [], [], [], []
        with hepmc_path.open("r") as f:
            for line in f:
                if not line.startswith("P "):
                    continue
                parts = line.split()
                try:
                    if int(parts[3]) != pid:
                        continue
                    px.append(float(parts[4]))
                    py.append(float(parts[5]))
                    pz.append(float(parts[6]))
                    E.append(float(parts[7]))
                except (ValueError, IndexError):
                    continue

        if not E:
            continue

        E = np.asarray(E, dtype=np.float64)
        px = np.asarray(px, dtype=np.float64)
        py = np.asarray(py, dtype=np.float64)
        pz = np.asarray(pz, dtype=np.float64)

        p = np.sqrt(px * px + py * py + pz * pz)
        m = p > 1e-12
        if not np.any(m):
            continue

        pxm, pym, pzm, pm = px[m], py[m], pz[m], p[m]
        cos_theta = pzm / pm
        sin_phi = np.sin(np.arctan2(pym, pxm))

        E_list.append(E[m])
        cos_list.append(cos_theta)
        sinphi_list.append(sin_phi)

    E_all = np.concatenate(E_list) if E_list else np.array([], dtype=np.float64)
    cos_all = np.concatenate(cos_list) if cos_list else np.array([], dtype=np.float64)
    sinphi_all = np.concatenate(sinphi_list) if sinphi_list else np.array([], dtype=np.float64)
    return E_all, cos_all, sinphi_all


# =============================================================================
# LHAPDF helpers (kaon toy × pion evolution)
# =============================================================================

try:
    import lhapdf  # type: ignore
except Exception:
    lhapdf = None


def is_lhapdf_available() -> bool:
    return lhapdf is not None


def ensure_lhapdf_set_installed(setname: str) -> None:
    if lhapdf is None:
        raise RuntimeError("python lhapdf is not available in this environment.")
    installed = set(lhapdf.availablePDFSets())
    if setname not in installed:
        raise RuntimeError(
            f"Pion PDF set '{setname}' is not installed in LHAPDF_DATA_PATH={os.environ.get('LHAPDF_DATA_PATH')}\n"
            f"Install it e.g.:\n"
            f"  lhapdf install --pdfdir {os.environ.get('LHAPDF_DATA_PATH')} {setname}\n"
        )


def pion_light_quark_sum(pdf, x: float, Q: float) -> float:
    """
    Using (u+ubar + d+dbar) as a proxy for meson evolution.
    LHAPDF returns x*f, so divide by x to get f.
    """
    if x <= 0.0:
        return 0.0
    u = pdf.xfxQ(2, x, Q) / x
    ub = pdf.xfxQ(-2, x, Q) / x
    d = pdf.xfxQ(1, x, Q) / x
    db = pdf.xfxQ(-1, x, Q) / x
    return (u + ub + d + db)


def make_pdf_kaon_toy_times_pion_evolution(
    p: ToyParams,
    pion_set: str,
    member: int = 0,
) -> Callable[[int, float, float], float]:
    """
    q_K(pid,x,Q2) = q_K^toy(pid,x,Q0) * R_pi(x,Q2)
    where R_pi is derived from pion PDFs.
    K+ content: u and sbar only (valence-only toy).
    """
    if lhapdf is None:
        raise RuntimeError("python lhapdf is not available in this environment.")
    ensure_lhapdf_set_installed(pion_set)

    pion_pdf = lhapdf.mkPDF(pion_set, member)
    norm = toy_norm(p.a, p.b)
    Q0 = float(np.sqrt(p.Q0))

    def pdf_kaon(pid: int, x: float, Q2: float) -> float:
        base = toy_shape_x(x, p.a, p.b, norm)

        Q = float(np.sqrt(Q2))
        num = pion_light_quark_sum(pion_pdf, x, Q)
        den = pion_light_quark_sum(pion_pdf, x, Q0)

        R = 1.0 if den <= 0.0 else (num / den)
        val = base * R

        if pid == 2:   # u
            return val
        if pid == -3:  # sbar
            return val
        return 0.0

    return pdf_kaon


# =============================================================================
# Grids
# =============================================================================

@dataclass(frozen=True)
class Grid:
    x_edges: np.ndarray
    q2_edges: np.ndarray
    x_cent: np.ndarray
    q2_cent: np.ndarray
    Xc: np.ndarray
    Q2c: np.ndarray


def make_log_grid(
    x_min: float,
    x_max: float,
    q2_min: float,
    q2_max: float,
    nx: int,
    nq2: int,
) -> Grid:
    x_edges = np.logspace(np.log10(x_min), np.log10(x_max), nx + 1)
    q2_edges = np.logspace(np.log10(q2_min), np.log10(q2_max), nq2 + 1)
    x_cent = 0.5 * (x_edges[:-1] + x_edges[1:])
    q2_cent = 0.5 * (q2_edges[:-1] + q2_edges[1:])
    Xc, Q2c = np.meshgrid(x_cent, q2_cent, indexing="xy")
    return Grid(x_edges, q2_edges, x_cent, q2_cent, Xc, Q2c)


def make_lin_grid(
    x_min: float,
    x_max: float,
    q2_min: float,
    q2_max: float,
    nx: int,
    nq2: int,
) -> Grid:
    x_edges = np.linspace(x_min, x_max, nx + 1)
    q2_edges = np.linspace(q2_min, q2_max, nq2 + 1)
    x_cent = 0.5 * (x_edges[:-1] + x_edges[1:])
    q2_cent = 0.5 * (q2_edges[:-1] + q2_edges[1:])
    Xc, Q2c = np.meshgrid(x_cent, q2_cent, indexing="xy")
    return Grid(x_edges, q2_edges, x_cent, q2_cent, Xc, Q2c)


def compute_F2_grid(grid: Grid, f2_point: Callable[[float, float], float]) -> np.ndarray:
    """
    f2_point(x, Q2) -> F2
    """
    F2 = np.empty_like(grid.Xc, dtype=np.float64)
    for i in range(grid.Q2c.shape[0]):
        for j in range(grid.Xc.shape[1]):
            x = float(grid.Xc[i, j])
            Q2 = float(grid.Q2c[i, j])
            F2[i, j] = f2_point(x, Q2)
    return F2