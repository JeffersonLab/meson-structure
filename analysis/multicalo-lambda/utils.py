from __future__ import annotations
from pathlib import Path
from typing import Iterable
import numpy as np
import awkward as ak
import uproot
from config import PhysicsConstants, Paths, DEFAULT_CONST, DEFAULT_PATHS


# Reco Lambda collection has been renamed across campaigns. Try the historical
# name first, then the current one.
_RECO_LAMBDA_NAMES = ("ReconstructedFarForwardLambdas", "ReconstructedLambdas")


def resolve_lambda_prefix(tree) -> str:
    """Return the reco-Lambda collection name that actually exists in `tree`."""
    keys = list(tree.keys())
    for name in _RECO_LAMBDA_NAMES:
        if any(k == name or k.startswith(name + ".") for k in keys):
            return name
    return _RECO_LAMBDA_NAMES[-1]


def iter_reco_files(beam: str, nfiles: int, root_base_dir: Path, suffix: str) -> Iterable[Path]:
    root_base_dir = Path(root_base_dir)

    # Legacy naming: k_lambda_{beam}_5000evt_{NNN}_{suffix}.root
    legacy = [
        root_base_dir / f"k_lambda_{beam}_5000evt_{i:03d}_{suffix}.root"
        for i in range(1, nfiles + 1)
    ]
    legacy = [p for p in legacy if p.exists() and p.stat().st_size > 0]
    if legacy:
        yield from legacy
        return

    # Fallback: campaign-agnostic discovery of the reco ROOT files that live in
    # this directory (e.g. msf_ev1000_NNNN.edm4eic.root). Take the first nfiles.
    if not root_base_dir.is_dir():
        return
    found = sorted(p for p in root_base_dir.glob("*.root") if p.stat().st_size > 0)
    yield from found[:nfiles]


def read_lambda_eicrecon(
    beam: str,
    nfiles: int,
    root_base_dir: Path,
    suffix: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Returns: E [GeV], cos(theta), sin(phi)
    """
    E_list: list[np.ndarray] = []
    cos_list: list[np.ndarray] = []
    sinphi_list: list[np.ndarray] = []

    for fpath in iter_reco_files(beam, nfiles, root_base_dir, suffix):
        try:
            with uproot.open(fpath) as f:
                tree = f["events"]
                prefix = resolve_lambda_prefix(tree)
                e_branch = f"{prefix}.energy"
                px_branch = f"{prefix}.momentum.x"
                py_branch = f"{prefix}.momentum.y"
                pz_branch = f"{prefix}.momentum.z"
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
    c: PhysicsConstants = DEFAULT_CONST,
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
                E = np.sqrt(p * p + (c.m_lambda_gev**2))

                E_list.append(ak.to_numpy(ak.flatten(E)))
                cos_list.append(ak.to_numpy(ak.flatten(cos_theta)))
                sinphi_list.append(ak.to_numpy(ak.flatten(sin_phi)))

        except Exception as e:
            print(f"[read_lambda_geant4] Warning {fpath.name}: {e}")

    E_out = np.concatenate(E_list) if E_list else np.array([], dtype=np.float64)
    cos_out = np.concatenate(cos_list) if cos_list else np.array([], dtype=np.float64)
    sinphi_out = np.concatenate(sinphi_list) if sinphi_list else np.array([], dtype=np.float64)
    return E_out, cos_out, sinphi_out


def read_lambda_afterburner(
    beam: str,
    nfiles: int,
    pattern: str,
    pid: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
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