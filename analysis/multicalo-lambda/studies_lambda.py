from __future__ import annotations

from pathlib import Path
import numpy as np
import awkward as ak
import matplotlib.pyplot as plt
import matplotlib as mpl

from config import PhysicsConstants, Paths, DEFAULT_CONST, DEFAULT_PATHS
from utils import read_lambda_geant4, read_lambda_eicrecon, read_lambda_afterburner, iter_reco_files
from physics import direct_energy_window, E_to_L, L_to_E, proton_kinematics_for_beam, xk_from_xb_xl
from plotting import apply_mpl_style, ensure_outdir, savefig


def plot_lambda_spectra(
    beam: str,
    xmax: float,
    nfiles: int,
    bins: int,
    root_base_dir: Path,
    suffix: str,
    outdir: Path,
    afterburner_pattern: str,
    c: PhysicsConstants = DEFAULT_CONST,
    logy: bool = True,
) -> Path:
    apply_mpl_style()
    outdir = ensure_outdir(outdir)

    E_geant4, _, _ = read_lambda_geant4(beam, nfiles=nfiles, root_base_dir=root_base_dir, suffix=suffix, c=c)
    E_reco, _, _ = read_lambda_eicrecon(beam, nfiles=nfiles, root_base_dir=root_base_dir, suffix=suffix)
    E_after, _, _ = read_lambda_afterburner(beam, nfiles=nfiles, pattern=afterburner_pattern, pid=c.pid_lambda)

    # label Geant4 count in direct window
    try:
        Emin, Emax = direct_energy_window(beam)
        E_geant4_direct = E_geant4[(E_geant4 >= Emin) & (E_geant4 <= Emax)]
        n_geant4_label = int(E_geant4_direct.size)
    except Exception:
        n_geant4_label = int(E_geant4.size)

    fig, ax = plt.subplots(figsize=(5, 5))

    if E_reco.size:
        ax.hist(
            E_reco, bins=bins, range=(0, xmax),
            histtype="step", linewidth=2.0,
            label=f"Reco ({E_reco.size:.1e})",
        )
    if E_geant4.size:
        ax.hist(
            E_geant4, bins=bins, range=(0, xmax),
            histtype="step",
            label=rf"Geant4 ({n_geant4_label:.1e})",
        )
    if E_after.size:
        ax.hist(
            E_after, bins=bins, range=(0, xmax),
            histtype="step", linestyle="--",
            label="Afterburner",
        )

    ax.set_xlabel("Energy (GeV)")
    ax.set_ylabel("Counts")
    ax.set_title(rf"$\Lambda$-spectrum at {beam}")
    ax.legend(frameon=False, loc="upper right")
    if logy:
        ax.set_yscale("log")
    fig.tight_layout()

    out = outdir / f"spectrum_{beam}_{suffix}.png"
    return savefig(fig, out, dpi=300)


def plot_angle_distrib(
    nfiles: int,
    bins: int,
    root_base_dir: Path,
    suffix: str,
    outdir: Path,
    afterburner_pattern: str,
    energies: tuple[str, ...] = ("5x41", "10x100", "18x275"),
    c: PhysicsConstants = DEFAULT_CONST,
) -> Path:
    apply_mpl_style()
    outdir = ensure_outdir(outdir)

    fig, axes = plt.subplots(3, 2, figsize=(10, 7.5), sharex=False, sharey=False)

    for row, beam in enumerate(energies):
        _, cos_true, sinphi_true = read_lambda_geant4(beam=beam, nfiles=nfiles, root_base_dir=root_base_dir, suffix=suffix, c=c)
        _, cos_reco, sinphi_reco = read_lambda_eicrecon(beam=beam, nfiles=nfiles, root_base_dir=root_base_dir, suffix=suffix)
        _, cos_after, sinphi_after = read_lambda_afterburner(beam=beam, nfiles=nfiles, pattern=afterburner_pattern, pid=c.pid_lambda)

        ax = axes[row, 0]
        if cos_true.size:
            ax.hist(cos_true, bins=bins, range=(-1, 1), histtype="step", label="Geant4")
        if cos_reco.size:
            ax.hist(cos_reco, bins=bins, range=(-1, 1), histtype="step", linewidth=2.5, label="Reco")
        if cos_after.size:
            ax.hist(cos_after, bins=bins, range=(-1, 1), histtype="step", linestyle="--", label="Afterburner")
        ax.set_xlabel(r"$\cos\theta_\Lambda$")
        ax.set_ylabel("Counts")
        ax.set_yscale("log")
        ax.set_title(beam)
        ax.legend(frameon=False)

        ax = axes[row, 1]
        if sinphi_true.size:
            ax.hist(sinphi_true, bins=bins, range=(-1, 1), histtype="step", label="Geant4")
        if sinphi_reco.size:
            ax.hist(sinphi_reco, bins=bins, range=(-1, 1), histtype="step", linewidth=2.5, label="Reco")
        if sinphi_after.size:
            ax.hist(sinphi_after, bins=bins, range=(-1, 1), histtype="step", linestyle="--", label="Afterburner")
        ax.set_xlabel(r"$\sin\phi_\Lambda$")
        ax.set_ylabel("Counts")
        ax.set_yscale("log")
        ax.set_title(beam)
        ax.legend(frameon=False)

    fig.tight_layout()
    out = outdir / f"angledistrib_lambda_cos_sinphi_{suffix}.png"
    return savefig(fig, out, dpi=300)


def efficiency_vs_energy(
    beam: str,
    nfiles: int,
    bins: int,
    root_base_dir: Path,
    suffix: str,
    c: PhysicsConstants = DEFAULT_CONST,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    Emin, Emax = direct_energy_window(beam)
    E_truth, _, _ = read_lambda_geant4(beam, nfiles=nfiles, root_base_dir=root_base_dir, suffix=suffix, c=c)
    E_reco, _, _ = read_lambda_eicrecon(beam, nfiles=nfiles, root_base_dir=root_base_dir, suffix=suffix)

    E_truth = E_truth[(E_truth >= Emin) & (E_truth <= Emax)]
    E_reco = E_reco[(E_reco >= Emin) & (E_reco <= Emax)]

    edges = np.linspace(Emin, Emax, bins + 1)
    h_truth, _ = np.histogram(E_truth, bins=edges)
    h_reco, _ = np.histogram(E_reco, bins=edges)

    eps = np.full_like(h_truth, np.nan, dtype=np.float64)
    err = np.full_like(h_truth, np.nan, dtype=np.float64)

    m = h_truth > 0
    eps[m] = h_reco[m] / h_truth[m]
    eps[m] = np.clip(eps[m], 0.0, 1.0)
    err[m] = np.sqrt(eps[m] * (1.0 - eps[m]) / h_truth[m])

    centers = 0.5 * (edges[:-1] + edges[1:])
    return centers, eps, err


def plot_efficiencies(
    nfiles_5x41: int,
    nfiles_10x100: int,
    nfiles_18x275: int,
    bins_5x41: int,
    bins_10x100: int,
    bins_18x275: int,
    root_base_dir: Path,
    suffix_new: str,
    suffix_old: str,
    outdir: Path,
    with_beta: bool,
    tag: str,
    c: PhysicsConstants = DEFAULT_CONST,
) -> Path:
    apply_mpl_style()
    outdir = ensure_outdir(outdir)

    c5, e5, s5 = efficiency_vs_energy("5x41", nfiles_5x41, bins_5x41, root_base_dir, suffix_new, c=c)
    c10, e10, s10 = efficiency_vs_energy("10x100", nfiles_10x100, bins_10x100, root_base_dir, suffix_new, c=c)
    c18, e18, s18 = efficiency_vs_energy("18x275", nfiles_18x275, bins_18x275, root_base_dir, suffix_new, c=c)

    c5o, e5o, s5o = efficiency_vs_energy("5x41", nfiles_5x41, bins_5x41, root_base_dir, suffix_old, c=c)
    c10o, e10o, s10o = efficiency_vs_energy("10x100", nfiles_10x100, bins_10x100, root_base_dir, suffix_old, c=c)
    c18o, e18o, s18o = efficiency_vs_energy("18x275", nfiles_18x275, bins_18x275, root_base_dir, suffix_old, c=c)

    fig, ax = plt.subplots(figsize=(5, 5))

    scale = (100.0 / c.beta) if with_beta else 100.0

    ax.errorbar(c5, scale * e5, yerr=scale * s5, fmt="s", markersize=4, linewidth=1, label="5x41 (new)")
    ax.errorbar(c5o, scale * e5o, yerr=scale * s5o, fmt="x", markersize=4, linewidth=1, label="5x41 (ZDC only)")

    ax.errorbar(c10, scale * e10, yerr=scale * s10, fmt="s", markersize=4, linewidth=1, label="10x100 (new)")
    ax.errorbar(c10o, scale * e10o, yerr=scale * s10o, fmt="x", markersize=4, linewidth=1, label="10x100 (ZDC only)")

    ax.errorbar(c18, scale * e18, yerr=scale * s18, fmt="s", markersize=4, linewidth=1, label="18x275 (new)")
    ax.errorbar(c18o, scale * e18o, yerr=scale * s18o, fmt="x", markersize=4, linewidth=1, label="18x275 (ZDC only)")

    ax.set_xlabel(r"$\Lambda^0$ energy: $E_\Lambda$ (GeV)")
    ax.set_ylabel(r"Reconstruction efficiency $\epsilon(E_\Lambda)$ (%)")

    secax = ax.secondary_xaxis("top", functions=(lambda x: E_to_L(x, c), lambda x: L_to_E(x, c)))
    secax.set_xticks([5, 10, 15, 20])
    secax.set_xlabel(r"Average decay vertex: $\langle z \rangle_\Lambda$ (m)")

    ax.legend(frameon=False)
    fig.tight_layout()

    outname = f"epsilon_vs_energy_{tag}" + ("_beta" if with_beta else "") + ".png"
    return savefig(fig, outdir / outname, dpi=300)


def plot_nlambda_vs_kinematics_all(
    beam: str,
    nfiles: int,
    root_base_dir: Path,
    suffix: str,
    outdir: Path,
    tag: str,
    xB_bins: int,
    xB_range: tuple[float, float],
    xK_bins: int,
    xK_range: tuple[float, float],
    Q2_bins: int,
    Q2_range: tuple[float, float],
    log_Q2: bool,
    logz: bool,
    t_bins: int = 50,
    t_range: tuple[float, float] | None = None,
    tmax: float | None = None,
    c: PhysicsConstants = DEFAULT_CONST,
) -> None:
    apply_mpl_style()
    outdir = ensure_outdir(outdir)

    xB_branch = "InclusiveKinematicsTruth.x"
    Q2_branch = "InclusiveKinematicsTruth.Q2"
    lamE_branch = "ReconstructedFarForwardLambdas.energy"
    lampx_branch = "ReconstructedFarForwardLambdas.momentum.x"
    lampy_branch = "ReconstructedFarForwardLambdas.momentum.y"
    lampz_branch = "ReconstructedFarForwardLambdas.momentum.z"

    pk = proton_kinematics_for_beam(beam, c=c)
    nhat = pk["nhat"]
    pplus_p = float(pk["pplus_p"])
    ppx, ppy, ppz, ppE = float(pk["ppx"]), float(pk["ppy"]), float(pk["ppz"]), float(pk["ppE"])

    xB_evt_all, Q2_evt_all, nlam_evt_all = [], [], []
    xK_cand_all, Q2_cand_all, tneg_cand_all = [], [], []

    for fpath in iter_reco_files(beam, nfiles, root_base_dir, suffix):
        try:
            with uproot.open(fpath) as f:
                tree = f["events"]

                xB_evt = ak.to_numpy(ak.flatten(tree[xB_branch].array(library="ak"))).astype(np.float64)
                Q2_evt = ak.to_numpy(ak.flatten(tree[Q2_branch].array(library="ak"))).astype(np.float64)

                lamE_j = tree[lamE_branch].array(library="ak")
                nlam_evt = ak.to_numpy(ak.num(lamE_j, axis=1)).astype(np.float64)

                nmin = min(len(xB_evt), len(Q2_evt), len(nlam_evt), len(lamE_j))
                if nmin == 0:
                    continue

                xB_evt = xB_evt[:nmin]
                Q2_evt = Q2_evt[:nmin]
                nlam_evt = nlam_evt[:nmin]
                lamE_j = lamE_j[:nmin]

                xB_evt_all.append(xB_evt)
                Q2_evt_all.append(Q2_evt)
                nlam_evt_all.append(nlam_evt)

                lampx = tree[lampx_branch].array(library="ak")[:nmin]
                lampy = tree[lampy_branch].array(library="ak")[:nmin]
                lampz = tree[lampz_branch].array(library="ak")[:nmin]

                xB_bc, _ = ak.broadcast_arrays(ak.Array(xB_evt), lamE_j)
                Q2_bc, _ = ak.broadcast_arrays(ak.Array(Q2_evt), lamE_j)

                xB_c = ak.to_numpy(ak.flatten(xB_bc)).astype(np.float64)
                Q2_c = ak.to_numpy(ak.flatten(Q2_bc)).astype(np.float64)
                E_c = ak.to_numpy(ak.flatten(lamE_j)).astype(np.float64)
                px_c = ak.to_numpy(ak.flatten(lampx)).astype(np.float64)
                py_c = ak.to_numpy(ak.flatten(lampy)).astype(np.float64)
                pz_c = ak.to_numpy(ak.flatten(lampz)).astype(np.float64)

                pL_par = px_c * nhat[0] + py_c * nhat[1] + pz_c * nhat[2]
                xL = (E_c + pL_par) / pplus_p
                xK = xk_from_xb_xl(xB_c, xL)

                dE = ppE - E_c
                dpx = ppx - px_c
                dpy = ppy - py_c
                dpz = ppz - pz_c
                t = dE * dE - (dpx * dpx + dpy * dpy + dpz * dpz)
                tneg = -t

                m = np.isfinite(xK) & np.isfinite(Q2_c) & np.isfinite(tneg)
                if tmax is not None:
                    m &= (tneg < tmax)

                if np.any(m):
                    xK_cand_all.append(xK[m])
                    Q2_cand_all.append(Q2_c[m])
                    tneg_cand_all.append(tneg[m])

        except Exception as e:
            print(f"[plot_nlambda_vs_kinematics_all] Warning {fpath.name}: {e}")

    if not xB_evt_all:
        print("No events found / nothing to plot.")
        return

    xB_evt = np.concatenate(xB_evt_all)
    Q2_evt = np.concatenate(Q2_evt_all)
    nlam_evt = np.concatenate(nlam_evt_all)

    has_cand = len(xK_cand_all) > 0
    if has_cand:
        xK_cand = np.concatenate(xK_cand_all)
        Q2_cand = np.concatenate(Q2_cand_all)
        tneg_cand = np.concatenate(tneg_cand_all) if tneg_cand_all else np.array([], dtype=np.float64)

    def q2_transform(Q2arr: np.ndarray):
        if log_Q2:
            mQ = Q2arr > 0
            return np.log10(Q2arr[mQ]), mQ
        mQ = np.isfinite(Q2arr)
        return Q2arr[mQ], mQ

    xB_edges = np.linspace(xB_range[0], xB_range[1], xB_bins + 1)
    xK_edges = np.linspace(xK_range[0], xK_range[1], xK_bins + 1)

    if log_Q2:
        y_edges = np.linspace(np.log10(Q2_range[0]), np.log10(Q2_range[1]), Q2_bins + 1)
        y_label = r"$\log_{10}(Q^2/\mathrm{GeV}^2)$"
    else:
        y_edges = np.linspace(Q2_range[0], Q2_range[1], Q2_bins + 1)
        y_label = r"$Q^2\ (\mathrm{GeV}^2)$"

    Q2e_plot, me = q2_transform(Q2_evt)
    xBe = xB_evt[me]
    we = nlam_evt[me]
    Hxb, xe, ye = np.histogram2d(xBe, Q2e_plot, bins=[xB_edges, y_edges], weights=we)

    fig, ax = plt.subplots(figsize=(6, 5))
    Z = Hxb.T
    if logz:
        Zm = np.ma.masked_where(Z <= 0, Z)
        pcm = ax.pcolormesh(xe, ye, Zm, shading="auto", norm=mpl.colors.LogNorm(), cmap="coolwarm")
    else:
        pcm = ax.pcolormesh(xe, ye, Z, shading="auto", cmap="coolwarm")
    cbar = fig.colorbar(pcm, ax=ax)
    cbar.set_label(r"Number of reconstructed $\Lambda$ (event weight $n_\Lambda$)")
    ax.set_xlabel(r"$x_B$")
    ax.set_ylabel(y_label)
    ax.set_title(rf"$\Lambda$ yield vs $(x_B,Q^2)$ at {beam}")
    fig.tight_layout()
    savefig(fig, outdir / f"kinematics_xB_Q2_{beam}_{tag}.png", dpi=300)

    if has_cand:
        Q2k_plot, mk = q2_transform(Q2_cand)
        xKk = xK_cand[mk]
        Hxk, xe, ye = np.histogram2d(xKk, Q2k_plot, bins=[xK_edges, y_edges])

        fig, ax = plt.subplots(figsize=(6, 5))
        Z = Hxk.T
        if logz:
            Zm = np.ma.masked_where(Z <= 0, Z)
            pcm = ax.pcolormesh(xe, ye, Zm, shading="auto", norm=mpl.colors.LogNorm(), cmap="coolwarm")
        else:
            pcm = ax.pcolormesh(xe, ye, Z, shading="auto", cmap="coolwarm")
        cbar = fig.colorbar(pcm, ax=ax)
        extra = "" if tmax is None else rf" (cut $-t<{tmax}$)"
        cbar.set_label(r"Number of reconstructed $\Lambda$ candidates" + extra)
        ax.set_xlabel(r"$x_K \approx x_B/(1-x_L)$")
        ax.set_ylabel(y_label)
        ax.set_title(rf"$\Lambda$ candidates vs $(x_K,Q^2)$ at {beam}" + extra)
        fig.tight_layout()
        savefig(fig, outdir / f"kinematics_xK_Q2_{beam}_{tag}.png", dpi=300)