from __future__ import annotations

from pathlib import Path
import numpy as np
import awkward as ak
import uproot
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from .plotting import apply_mpl_style, ensure_outdir, savefig
from .physics import proton_kinematics_for_beam, xk_from_xb_xl
from .config import PhysicsConstants, DEFAULT_CONST


def build_sigma_map_xb_q2(
    beam: str,
    base_dir: str | Path,
    xb_range=(0.0, 1.0),
    xb_bins=10,
    q2_range=(1.0, 500.0),
    q2_bins=10,
    chunk=2_000_000,
    savefig: bool = True,
    fig_dir: str | Path = "./outputs",
    plot_density: bool = True,
):
    Ee_str, Ep_str = beam.lower().split("x")
    Ee, Ep = float(Ee_str), float(Ep_str)

    fname = f"k_lambda_crossing_0.000-{Ee:.1f}on{Ep:.1f}_x0.0001-1.0000_q1.0-500.0.root"
    fpath = Path(base_dir) / fname
    if not fpath.exists():
        raise FileNotFoundError(fpath)

    xb_edges = np.linspace(xb_range[0], xb_range[1], xb_bins + 1)
    q2_edges = np.logspace(np.log10(q2_range[0]), np.log10(q2_range[1]), q2_bins + 1)

    sumw_map = np.zeros((xb_bins, q2_bins), dtype=np.float64)
    Ngen_map = np.zeros((xb_bins, q2_bins), dtype=np.float64)

    with uproot.open(fpath) as f:
        meta = f["Meta"]
        evnts = f["Evnts"]
        n_use = min(meta.num_entries, evnts.num_entries)

        mc0 = meta["MC"].array(entry_start=0, entry_stop=1, library="np")
        Ngen_declared = int(mc0["nEvts"][0])

        for start in range(0, n_use, chunk):
            stop = min(start + chunk, n_use)

            jac = meta["Jacob"].array(entry_start=start, entry_stop=stop, library="np")
            mc = meta["MC"].array(entry_start=start, entry_stop=stop, library="np")
            inv = evnts["invts"].array(entry_start=start, entry_stop=stop, library="np")

            w = mc["PhSpFct"] * jac  # nb
            xb = inv["xBj"]
            q2 = inv["Q2"]

            ok = np.isfinite(w) & np.isfinite(xb) & np.isfinite(q2) & (q2 > 0)
            if not np.any(ok):
                continue

            w = w[ok]
            xb = xb[ok]
            q2 = q2[ok]

            sumw_map += np.histogram2d(xb, q2, bins=(xb_edges, q2_edges), weights=w)[0]
            Ngen_map += np.histogram2d(xb, q2, bins=(xb_edges, q2_edges))[0]

    sigma_map_nb = sumw_map / float(Ngen_declared)
    sigma_tot_nb = float(sumw_map.sum()) / float(Ngen_declared)

    if savefig:
        apply_mpl_style()
        outdir = ensure_outdir(fig_dir)
        outpath = outdir / f"sigma_xb_q2_{beam}.png"

        if plot_density:
            dx = np.diff(xb_edges)[:, None]
            dQ2 = np.diff(q2_edges)[None, :]
            z = sigma_map_nb / (dx * dQ2)
            cbar_label = r"$d\sigma/(dx_B\,dQ^2)$ [nb/GeV$^2$]"
            title = rf"Sullivan $d\sigma/(dx_B dQ^2)$ — {beam}"
        else:
            z = sigma_map_nb
            cbar_label = r"$\sigma$ [nb]"
            title = rf"Sullivan $\sigma(x_B,Q^2)$ — {beam}"

        pos = z[z > 0]
        norm = LogNorm(vmin=float(pos.min()), vmax=float(pos.max())) if pos.size else None

        fig, ax = plt.subplots(figsize=(6, 5))
        m = ax.pcolormesh(xb_edges, q2_edges, z.T, shading="auto", norm=norm, cmap="coolwarm")
        cb = fig.colorbar(m, ax=ax)
        cb.set_label(cbar_label)
        ax.set_xlabel(r"$x_B$")
        ax.set_ylabel(r"$Q^2$ [GeV$^2$]")
        ax.set_yscale("log")
        ax.set_title(title)
        fig.tight_layout()
        savefig(fig, outpath, dpi=200)

    return sigma_map_nb, Ngen_map, sigma_tot_nb


def plot_relerr_kaon_sf_xK_Q2(
    beam: str,
    nfiles: int,
    root_base_dir: Path,
    suffix: str,
    gen_base_dir: Path,
    outdir: Path,
    tag: str,
    xB_bins: int = 20,
    xB_range: tuple[float, float] = (0.0, 1.0),
    xK_bins: int = 20,
    xK_range: tuple[float, float] = (0.0, 2.0),
    Q2_bins: int = 20,
    Q2_range: tuple[float, float] = (1.0, 500.0),
    log_Q2: bool = True,
    tmax: float | None = None,
    lumin_fb: float = 1.0,
    vmax_percent: float | None = None,
    c: PhysicsConstants = DEFAULT_CONST,
):
    """
    - sigma_gen(xB,Q2) from generator (nb/bin)
    - eps(xB,Q2) from reco sample: Nreco_lambda / Ngen_evt
    - project to (xK,Q2) with migration P(xK|xB,Q2)
    - relerr = 100/sqrt(Nexp) [%], with Nexp = sigma*eps*L
    """
    apply_mpl_style()
    outdir = ensure_outdir(outdir)

    xB_edges = np.linspace(xB_range[0], xB_range[1], xB_bins + 1)
    xK_edges = np.linspace(xK_range[0], xK_range[1], xK_bins + 1)
    if log_Q2:
        Q2_edges = np.logspace(np.log10(Q2_range[0]), np.log10(Q2_range[1]), Q2_bins + 1)
    else:
        Q2_edges = np.linspace(Q2_range[0], Q2_range[1], Q2_bins + 1)

    sigma_gen_nb, _, sigma_tot_nb = build_sigma_map_xb_q2(
        beam=beam,
        base_dir=gen_base_dir,
        xb_range=xB_range,
        xb_bins=xB_bins,
        q2_range=Q2_range,
        q2_bins=Q2_bins,
        chunk=2_000_000,
        savefig=False,
    )

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

    Ngen_evt = np.zeros((xB_bins, Q2_bins), dtype=np.float64)
    Nreco_lam = np.zeros((xB_bins, Q2_bins), dtype=np.float64)
    M = np.zeros((xK_bins, xB_bins, Q2_bins), dtype=np.float64)

    for i in range(1, nfiles + 1):
        fpath = root_base_dir / f"k_lambda_{beam}_5000evt_{i:03d}_{suffix}.root"
        if not fpath.exists():
            continue

        try:
            with uproot.open(fpath) as f:
                tree = f["events"]

                xB_evt = ak.to_numpy(ak.flatten(tree[xB_branch].array(library="ak")))
                Q2_evt = ak.to_numpy(ak.flatten(tree[Q2_branch].array(library="ak")))
                n_evt = min(len(xB_evt), len(Q2_evt))
                if n_evt == 0:
                    continue
                xB_evt = xB_evt[:n_evt]
                Q2_evt = Q2_evt[:n_evt]

                Ngen_evt += np.histogram2d(xB_evt, Q2_evt, bins=(xB_edges, Q2_edges))[0]

                lamE_j = tree[lamE_branch].array(library="ak")[:n_evt]
                px_j = tree[lampx_branch].array(library="ak")[:n_evt]
                py_j = tree[lampy_branch].array(library="ak")[:n_evt]
                pz_j = tree[lampz_branch].array(library="ak")[:n_evt]

                xB_bc, _ = ak.broadcast_arrays(ak.Array(xB_evt), lamE_j)
                Q2_bc, _ = ak.broadcast_arrays(ak.Array(Q2_evt), lamE_j)

                xB_c = ak.to_numpy(ak.flatten(xB_bc))
                Q2_c = ak.to_numpy(ak.flatten(Q2_bc))
                E_c = ak.to_numpy(ak.flatten(lamE_j))
                px_c = ak.to_numpy(ak.flatten(px_j))
                py_c = ak.to_numpy(ak.flatten(py_j))
                pz_c = ak.to_numpy(ak.flatten(pz_j))
                if xB_c.size == 0:
                    continue

                pL_par = px_c * nhat[0] + py_c * nhat[1] + pz_c * nhat[2]
                xL = (E_c + pL_par) / pplus_p
                xK_c = xk_from_xb_xl(xB_c, xL)

                ok = np.isfinite(xB_c) & np.isfinite(Q2_c) & np.isfinite(xK_c) & (Q2_c > 0)

                if tmax is not None:
                    dE = ppE - E_c
                    dpx = ppx - px_c
                    dpy = ppy - py_c
                    dpz = ppz - pz_c
                    t = dE * dE - (dpx * dpx + dpy * dpy + dpz * dpz)
                    tneg = -t
                    ok &= np.isfinite(tneg) & (tneg < tmax)

                if not np.any(ok):
                    continue

                xB_sel = xB_c[ok]
                Q2_sel = Q2_c[ok]
                xK_sel = xK_c[ok]

                Nreco_lam += np.histogram2d(xB_sel, Q2_sel, bins=(xB_edges, Q2_edges))[0]

                ixB = np.searchsorted(xB_edges, xB_sel, side="right") - 1
                iQ = np.searchsorted(Q2_edges, Q2_sel, side="right") - 1
                ixK = np.searchsorted(xK_edges, xK_sel, side="right") - 1
                good = (ixB >= 0) & (ixB < xB_bins) & (iQ >= 0) & (iQ < Q2_bins) & (ixK >= 0) & (ixK < xK_bins)
                np.add.at(M, (ixK[good], ixB[good], iQ[good]), 1.0)

        except Exception as e:
            print(f"[plot_relerr_kaon_sf_xK_Q2] Warning {fpath.name}: {e}")

    eps = np.zeros_like(Ngen_evt, dtype=np.float64)
    m = Ngen_evt > 0
    eps[m] = Nreco_lam[m] / Ngen_evt[m]
    eps = np.clip(eps, 0.0, 1.0)

    L_nb_inv = float(lumin_fb) * 1e6  # fb^-1 -> nb^-1
    Nexp_xB_Q2 = sigma_gen_nb * eps * L_nb_inv

    relerr_xB_Q2 = np.full_like(Nexp_xB_Q2, np.nan, dtype=np.float64)
    okN = Nexp_xB_Q2 > 10
    relerr_xB_Q2[okN] = 100.0 / np.sqrt(Nexp_xB_Q2[okN])

    denom = np.sum(M, axis=0)
    P = np.zeros_like(M, dtype=np.float64)
    ok = denom > 0
    P[:, ok] = M[:, ok] / denom[ok]

    Nexp_xK_Q2 = np.zeros((xK_bins, Q2_bins), dtype=np.float64)
    for iQ in range(Q2_bins):
        Nexp_xK_Q2[:, iQ] = P[:, :, iQ] @ Nexp_xB_Q2[:, iQ]

    relerr_xK_Q2 = np.full_like(Nexp_xK_Q2, np.nan, dtype=np.float64)
    okNk = Nexp_xK_Q2 > 10
    relerr_xK_Q2[okNk] = 100.0 / np.sqrt(Nexp_xK_Q2[okNk])

    print(f"σ_tot(gen) = {sigma_tot_nb:.6g} nb")
    print("Total expected Lambdas (xB,Q2):", float(np.nansum(Nexp_xB_Q2)))
    print("Total expected Lambdas (xK,Q2):", float(np.nansum(Nexp_xK_Q2)))

    extra = "" if tmax is None else rf" ($-t<{tmax}$)"
    q2_tag = "logQ2" if log_Q2 else "linQ2"

    def plot_map(Z, x_edges, y_edges, xlabel, outname):
        fig, ax = plt.subplots(figsize=(6, 5))
        Zm = np.ma.masked_invalid(Z)
        pcm = ax.pcolormesh(x_edges, y_edges, Zm.T, shading="auto", cmap="viridis")
        cb = fig.colorbar(pcm, ax=ax)
        cb.set_label(r"Relative stat. uncertainty $\delta N/N$ [%]" + extra)
        if vmax_percent is not None and np.isfinite(vmax_percent):
            pcm.set_clim(vmin=0.0, vmax=float(vmax_percent))
        ax.set_xlabel(xlabel)
        ax.set_ylabel(r"$Q^2\ (\mathrm{GeV}^2)$")
        if log_Q2:
            ax.set_yscale("log")
        ax.set_title(rf"{beam}, $\mathcal{{L}}$={lumin_fb:g} fb$^{{-1}}$")
        fig.tight_layout()
        savefig(fig, outdir / outname, dpi=300)

    plot_map(
        relerr_xB_Q2, xB_edges, Q2_edges, r"$x_B$",
        f"relerr_xB_Q2_{beam}_{tag}_L{lumin_fb:g}fb_{q2_tag}.png",
    )
    plot_map(
        relerr_xK_Q2, xK_edges, Q2_edges, r"$x_K \simeq x_B/(1-x_\Lambda)$",
        f"relerr_xK_Q2_{beam}_{tag}_L{lumin_fb:g}fb_{q2_tag}.png",
    )

    return relerr_xB_Q2, relerr_xK_Q2, dict(
        eps=eps,
        Nexp_xB_Q2=Nexp_xB_Q2,
        Nexp_xK_Q2=Nexp_xK_Q2,
        sigma_gen_nb=sigma_gen_nb,
        sigma_tot_nb=sigma_tot_nb,
    )