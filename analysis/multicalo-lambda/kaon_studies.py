from __future__ import annotations

from pathlib import Path
import numpy as np
import awkward as ak
import uproot
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import LogLocator, NullFormatter, FixedLocator, LogFormatterMathtext, FixedFormatter

import uproot

from plotting import (
    apply_mpl_style, 
    ensure_outdir, savefig, 
    get_color, get_style, 
    plot_relerr_map
)

from physics import (
    KaonModelParams,
    proton_kinematics_for_beam, 
    xk_from_xb_xl, 
    F2_from_pdf_func,
    ToyParams, 
    KaonModelParams, 
    toy_norm, 
    toy_shape_x
) 

from uq import (
    efficiency_from_counts,
    expected_yields_nb,
    relerr_combined,
    migration_probability_xk_given_xb_q2,
    project_xbq2_to_xkq2,
    projected_efficiency_from_migration,
)

from kaon_models import (
    EvalConfig,
    make_kaon_pdf_func,
    make_f2k_jam_replica,
    make_f2k_jam_mean,
    get_all_jam_replica_ids,
    evaluate_f2k_for_jam_replicas,
    evaluate_f2k_component_for_jam_replicas,
)

from config import (
    PhysicsConstants, 
    CONST,
    setup_lhapdf_env,
    get_pion_pdfset,
    get_pion_pdfmember,
)
from utils import (
        is_lhapdf_available,
        make_pdf_kaon_toy_times_pion_evolution,
)

# event generator cross-section

def build_sigma_map_xb_q2(
    beam: str,
    base_dir: str | Path,
    xb_range=(0.0, 1.0),
    xb_bins=10,
    q2_range=(1.0, 500.0),
    q2_bins=10,
    chunk=2_000_000,
    do_savefig: bool = True,
    fig_dir: str | Path = "./outputs",
    plot_density: bool = True,
    log_Q2: bool = True,
    log_x: bool = False,
):
    Ee_str, Ep_str = beam.lower().split("x")
    Ee, Ep = float(Ee_str), float(Ep_str)

    fname = f"k_lambda_crossing_0.000-{Ee:.1f}on{Ep:.1f}_x0.0001-1.0000_q1.0-500.0.root"
    fpath = Path(base_dir) / fname
    if not fpath.exists():
        raise FileNotFoundError(fpath)

    if log_x:
        if xb_range[0] <= 0 or xb_range[1] <= 0:
            raise ValueError("xb_range must be strictly positive when log_x=True")
    if log_Q2:
        if q2_range[0] <= 0 or q2_range[1] <= 0:
            raise ValueError("q2_range must be strictly positive when log_Q2=True")

    if log_x:
        xb_edges = np.logspace(np.log10(xb_range[0]), np.log10(xb_range[1]), xb_bins + 1)
    else:
        xb_edges = np.linspace(xb_range[0], xb_range[1], xb_bins + 1)

    if log_Q2:
        q2_edges = np.logspace(np.log10(q2_range[0]), np.log10(q2_range[1]), q2_bins + 1)
    else:
        q2_edges = np.linspace(q2_range[0], q2_range[1], q2_bins + 1)

    sumw_map = np.zeros((xb_bins, q2_bins), dtype=np.float64)
    Ngen_map = np.zeros((xb_bins, q2_bins), dtype=np.float64)

    with uproot.open(fpath) as f:
        meta = f["Meta"]
        evnts = f["Evnts"]
        process = f["Process"]
        n_use = min(meta.num_entries, evnts.num_entries)

        mc0 = meta["MC"].array(entry_start=0, entry_stop=1, library="np")
        Ngen_declared = int(mc0["nEvts"][0])

        for start in range(0, n_use, chunk):
            stop = min(start + chunk, n_use)

            jac = meta["Jacob"].array(entry_start=start, entry_stop=stop, library="np")
            mc = meta["MC"].array(entry_start=start, entry_stop=stop, library="np")
            inv = evnts["invts"].array(entry_start=start, entry_stop=stop, library="np")
            xdis = process["xsec_tagged_dis"].array(entry_start=start, entry_stop=stop, library="np")
            kint = process["k_int"].array(entry_start=start, entry_stop=stop, library="np")

            w = mc["PhSpFct"] * jac * xdis * kint # nb
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

    if do_savefig:
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
        if log_x:
            ax.set_xscale("log")
        if log_Q2:
            ax.set_yscale("log")
        ax.set_title(title)
        fig.tight_layout()
        savefig(fig, outpath, dpi=200)

    print('CHECK. Sigma tot =', sigma_tot_nb, 'nb')

    return sigma_map_nb, Ngen_map, sigma_tot_nb

# relative errors computation

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
    log_x: bool = False,
    tmax: float | None = None,
    lumin_fb: float = 1.0,
    vmax_percent: float | None = None,
    c: PhysicsConstants = CONST,
    kinmethod: str = "Truth",
):
    """
    Fully consistent version.

    Strategy
    --------
    1) Build sigma_gen(xB_truth, Q2_truth) from generator.
    2) Build eps(xB_truth, Q2_truth) from reco sample, binned in truth kinematics:
           eps = Nreco_lambda(truth bins) / Ngen_evt(truth bins)
    3) Build expected reconstructed yields in truth bins:
           Nexp_truth = sigma_gen * eps * L
    4) Build a 4D response:
           P(xK_reco, Q2_reco | xB_truth, Q2_truth)
    5) Project Nexp_truth to a fully reconstructed map:
           Nexp_reco(xK_reco, Q2_reco)
    6) Compute Poisson relative uncertainty:
           relerr = 100 / sqrt(Nexp_reco)

    Notes
    -----
    - The output xK-Q2 map is now fully reconstructed:
          (xK_reco, Q2_reco)
      and no longer mixes xK_reco with Q2_truth.
    - The MC uncertainty on projected efficiency is intentionally NOT used here,
      because the previous projected_efficiency_from_migration construction was
      not formally consistent in reco space.
    """

    def _response_probability_xkq2reco_given_xbq2truth(R: np.ndarray) -> np.ndarray:
        """
        Build P(xK_reco, Q2_reco | xB_truth, Q2_truth)
        from raw counts R with shape:
            (xK_bins, Q2_bins, xB_bins, Q2_bins)
        """
        denom = np.sum(R, axis=(0, 1))  # shape: (xB_bins, Q2_bins)
        P = np.zeros_like(R, dtype=np.float64)
        for ixB in range(R.shape[2]):
            for iQ in range(R.shape[3]):
                if denom[ixB, iQ] > 0:
                    P[:, :, ixB, iQ] = R[:, :, ixB, iQ] / denom[ixB, iQ]
        return P

    def _project_xbq2truth_to_xkq2reco(
        P: np.ndarray,
        A_truth: np.ndarray,
    ) -> np.ndarray:
        """
        Project A_truth(xB_truth, Q2_truth) to reco space using
        P(xK_reco, Q2_reco | xB_truth, Q2_truth).

        P shape      : (xK_bins, Q2_bins, xB_bins, Q2_bins)
        A_truth shape: (xB_bins, Q2_bins)
        Returns      : (xK_bins, Q2_bins)
        """
        return np.einsum("kqij,ij->kq", P, A_truth)

    apply_mpl_style()
    outdir = ensure_outdir(outdir)

    if log_x:
        if xB_range[0] <= 0 or xK_range[0] <= 0:
            raise ValueError("xB_range and xK_range must be strictly positive when log_x=True")
        xB_edges = np.logspace(np.log10(xB_range[0]), np.log10(xB_range[1]), xB_bins + 1)
        xK_edges = np.logspace(np.log10(xK_range[0]), np.log10(xK_range[1]), xK_bins + 1)
    else:
        xB_edges = np.linspace(xB_range[0], xB_range[1], xB_bins + 1)
        xK_edges = np.linspace(xK_range[0], xK_range[1], xK_bins + 1)

    if log_Q2:
        if Q2_range[0] <= 0:
            raise ValueError("Q2_range must be strictly positive when log_Q2=True")
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
        do_savefig=True,
        log_Q2=log_Q2,
        log_x=log_x,
    )

    if kinmethod not in ("Truth", "Electron", "JB", "Sigma", "DA", "ML"):
        raise ValueError(
            f"Invalid kinmethod: {kinmethod}. Choose Truth, Electron, JB, Sigma, DA, or ML."
        )

    # truth kinematics

    xB_truth_branch = "InclusiveKinematicsTruth.x"
    Q2_truth_branch = "InclusiveKinematicsTruth.Q2"

    # reconstructed kinematics

    xB_reco_branch = f"InclusiveKinematics{kinmethod}.x"
    Q2_reco_branch = f"InclusiveKinematics{kinmethod}.Q2"

    # reconstructed lambdas

    lamE_branch = "ReconstructedFarForwardLambdas.energy"
    lampx_branch = "ReconstructedFarForwardLambdas.momentum.x"
    lampy_branch = "ReconstructedFarForwardLambdas.momentum.y"
    lampz_branch = "ReconstructedFarForwardLambdas.momentum.z"

    pk = proton_kinematics_for_beam(beam, c=c)
    nhat = pk["nhat"]
    pplus_p = float(pk["pplus_p"])
    ppx, ppy, ppz, ppE = float(pk["ppx"]), float(pk["ppy"]), float(pk["ppz"]), float(pk["ppE"])

    # truth-space quantities

    Ngen_evt = np.zeros((xB_bins, Q2_bins), dtype=np.float64)
    Nreco_lam = np.zeros((xB_bins, Q2_bins), dtype=np.float64)

    # phase-space matrix

    R = np.zeros((xK_bins, Q2_bins, xB_bins, Q2_bins), dtype=np.float64)

    for i in range(1, nfiles + 1):
        fpath = root_base_dir / f"k_lambda_{beam}_5000evt_{i:03d}_{suffix}.root"
        if not fpath.exists():
            continue

        try:
            with uproot.open(fpath) as f:
                tree = f["events"]

                # event-level truth kinematics

                xB_evt_truth = ak.to_numpy(
                    ak.flatten(tree[xB_truth_branch].array(library="ak"))
                )
                Q2_evt_truth = ak.to_numpy(
                    ak.flatten(tree[Q2_truth_branch].array(library="ak"))
                )

                # event-level reconstructed kinematics

                xB_evt_reco = ak.to_numpy(
                    ak.flatten(tree[xB_reco_branch].array(library="ak"))
                )
                Q2_evt_reco = ak.to_numpy(
                    ak.flatten(tree[Q2_reco_branch].array(library="ak"))
                )

                n_evt = min(
                    len(xB_evt_truth), len(Q2_evt_truth),
                    len(xB_evt_reco), len(Q2_evt_reco)
                )
                if n_evt == 0:
                    continue

                xB_evt_truth = xB_evt_truth[:n_evt]
                Q2_evt_truth = Q2_evt_truth[:n_evt]
                xB_evt_reco = xB_evt_reco[:n_evt]
                Q2_evt_reco = Q2_evt_reco[:n_evt]

                # truth event count: denominator of efficiency

                Ngen_evt += np.histogram2d(
                    xB_evt_truth, Q2_evt_truth, bins=(xB_edges, Q2_edges)
                )[0]

                # reconstructed lambdas

                lamE_j = tree[lamE_branch].array(library="ak")[:n_evt]
                px_j = tree[lampx_branch].array(library="ak")[:n_evt]
                py_j = tree[lampy_branch].array(library="ak")[:n_evt]
                pz_j = tree[lampz_branch].array(library="ak")[:n_evt]

                # Broadcast truth event kinematics to lambda candidates

                xB_truth_bc, _ = ak.broadcast_arrays(ak.Array(xB_evt_truth), lamE_j)
                Q2_truth_bc, _ = ak.broadcast_arrays(ak.Array(Q2_evt_truth), lamE_j)

                # Broadcast reco event kinematics to lambda candidates

                xB_reco_bc, _ = ak.broadcast_arrays(ak.Array(xB_evt_reco), lamE_j)
                Q2_reco_bc, _ = ak.broadcast_arrays(ak.Array(Q2_evt_reco), lamE_j)

                xB_truth_c = ak.to_numpy(ak.flatten(xB_truth_bc))
                Q2_truth_c = ak.to_numpy(ak.flatten(Q2_truth_bc))
                xB_reco_c = ak.to_numpy(ak.flatten(xB_reco_bc))
                Q2_reco_c = ak.to_numpy(ak.flatten(Q2_reco_bc))

                E_c = ak.to_numpy(ak.flatten(lamE_j))
                px_c = ak.to_numpy(ak.flatten(px_j))
                py_c = ak.to_numpy(ak.flatten(py_j))
                pz_c = ak.to_numpy(ak.flatten(pz_j))

                if xB_truth_c.size == 0:
                    continue

                # Lambda-derived xL from reconstructed 4-vector

                pL_par = px_c * nhat[0] + py_c * nhat[1] + pz_c * nhat[2]
                xL = (E_c + pL_par) / pplus_p

                # Reconstructed xK using selected reconstructed inclusive kinematics

                xK_reco_c = xk_from_xb_xl(xB_reco_c, xL)

                ok = (
                    np.isfinite(xB_truth_c) & np.isfinite(Q2_truth_c) &
                    np.isfinite(xB_reco_c) & np.isfinite(Q2_reco_c) &
                    np.isfinite(xK_reco_c) &
                    (Q2_truth_c > 0.0) & (Q2_reco_c > 0.0)
                )

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

                # efficiency numerator in truth bins

                xB_truth_sel = xB_truth_c[ok]
                Q2_truth_sel = Q2_truth_c[ok]

                Nreco_lam += np.histogram2d(
                    xB_truth_sel,
                    Q2_truth_sel,
                    bins=(xB_edges, Q2_edges),
                )[0]

                # (xB_truth, Q2_truth) -> (xK_reco, Q2_reco)
                
                xK_sel = xK_reco_c[ok]
                Q2_reco_sel = Q2_reco_c[ok]

                ixB_truth = np.searchsorted(xB_edges, xB_truth_sel, side="right") - 1
                iQ_truth = np.searchsorted(Q2_edges, Q2_truth_sel, side="right") - 1
                ixK_reco = np.searchsorted(xK_edges, xK_sel, side="right") - 1
                iQ_reco = np.searchsorted(Q2_edges, Q2_reco_sel, side="right") - 1

                good = (
                    (ixB_truth >= 0) & (ixB_truth < xB_bins) &
                    (iQ_truth >= 0) & (iQ_truth < Q2_bins) &
                    (ixK_reco >= 0) & (ixK_reco < xK_bins) &
                    (iQ_reco >= 0) & (iQ_reco < Q2_bins)
                )

                np.add.at(
                    R,
                    (
                        ixK_reco[good],
                        iQ_reco[good],
                        ixB_truth[good],
                        iQ_truth[good],
                    ),
                    1.0,
                )

        except Exception as e:
            print(f"[plot_relerr_kaon_sf_xK_Q2] Warning {fpath.name}: {e}")

    # Truth-space efficiency and expected yields
    
    eps = efficiency_from_counts(Nreco_lam, Ngen_evt)
    print(
        "CHECK. Nreco_lam =", Nreco_lam.sum(),
        "Ngen_evt =", Ngen_evt.sum(),
        "eps_mean =", np.nanmean(eps),
    )

    Nexp_xB_Q2 = expected_yields_nb(sigma_gen_nb, eps, lumin_fb)

    # truth-space relative uncertainty (for diagnostic only)

    relerr_xB_Q2 = np.full_like(Nexp_xB_Q2, np.nan, dtype=np.float64)
    mask_truth = Nexp_xB_Q2 > 0
    relerr_xB_Q2[mask_truth] = 100.0 / np.sqrt(Nexp_xB_Q2[mask_truth])

    # reconstructed projections 

    P = _response_probability_xkq2reco_given_xbq2truth(R)
    denom_R = np.sum(R, axis=(0, 1))
    populated = denom_R > 0
    if np.any(populated):
        check = np.sum(P, axis=(0, 1))
        max_dev = np.max(np.abs(check[populated] - 1.0))
        print(f"CHECK. max deviation of response normalization = {max_dev:.3e}")

    Nexp_xK_Q2 = _project_xbq2truth_to_xkq2reco(P, Nexp_xB_Q2)

    # final uncertainty map

    relerr_xK_Q2 = np.full_like(Nexp_xK_Q2, np.nan, dtype=np.float64)
    mask_reco = Nexp_xK_Q2 > 0
    relerr_xK_Q2[mask_reco] = 100.0 / np.sqrt(Nexp_xK_Q2[mask_reco])

    q2_tag = "logQ2" if log_Q2 else "linQ2"

    # plotting

    plot_relerr_map(
        relerr_xB_Q2,
        xB_edges,
        Q2_edges,
        xlabel=r"$x_B^{\rm truth}$",
        ylabel=r"$Q^{2,\,\rm truth}\ (\mathrm{GeV}^2)$",
        cbarlabel=r"Relative uncertainty on $F_2^K$ (%)",
        title=rf"{beam}, $\mathcal{{L}}$={lumin_fb:g} fb$^{{-1}}$, truth normalization",
        outpath=outdir / f"relerr_xBtruth_Q2truth_{beam}_{tag}_L{lumin_fb:g}fb_{q2_tag}_kin{kinmethod}.png",
        log_y=log_Q2,
        log_x=log_x,
        log_z=False,
        vmax_percent=vmax_percent,
    )

    plot_relerr_map(
        relerr_xK_Q2,
        xK_edges,
        Q2_edges,
        xlabel=rf"$x_K^{{\rm reco}} \simeq x_B^{{{kinmethod}}}/(1-x_\Lambda)$",
        ylabel=rf"$Q^{{2,\,\rm reco}}_{{{kinmethod}}}\ (\mathrm{{GeV}}^2)$",
        cbarlabel=r"Relative uncertainty on $F_2^K$ (%)",
        title=rf"{beam}, $\mathcal{{L}}$={lumin_fb:g} fb$^{{-1}}$, {kinmethod} kinematics",
        outpath=outdir / f"relerr_xKreco_Q2reco_{beam}_{tag}_L{lumin_fb:g}fb_{q2_tag}_kin{kinmethod}.png",
        log_y=log_Q2,
        log_x=log_x,
        log_z=False,
        vmax_percent=vmax_percent,
    )

    return relerr_xB_Q2, relerr_xK_Q2, dict(
        eps_truth=eps,
        Ngen_evt_truth=Ngen_evt,
        Nreco_lam_truth=Nreco_lam,
        Nexp_xB_Q2_truth=Nexp_xB_Q2,
        Nexp_xK_Q2_reco=Nexp_xK_Q2,
        sigma_gen_nb=sigma_gen_nb,
        sigma_tot_nb=sigma_tot_nb,
        response_counts=R,
        response_prob=P,
        kinmethod=kinmethod,
    )

# high-level plotting : models with attached error

def plot_F2K_xK_slices_with_attached_errors(
    relerr_xK_Q2: np.ndarray,
    Nexp_xK_Q2: np.ndarray,
    xK_edges: np.ndarray,
    Q2_edges: np.ndarray,
    q2_slices: list[tuple[float, float]] | None = None,
    eval_cfg=None,
    outdir: str | Path = "./outputs",
    outname: str = "F2K_xK_slices_with_errors.png",
    title: str | None = None,
    logx: bool = False,
    logy: bool = False,
    ymin: float | None = None,
    ymax: float | None = None,
    xK_range: tuple[float, float] = (0, 1),
    Q2_range: tuple[float, float] = (1, 500),
):
    """
    Build F2K(xK) curves for Q2 slices and attach "artificial" uncertainties:
      dF2 = F2 * relerr(xK,Q2_slice)

    - F2K comes from eval.py model (toy x-shape × pion Q2 evolution).
    - relerr_xK_Q2 is your propagated relative uncertainty map in percent.
    - In each Q2 slice, we compute a yield-weighted average:
        F2_slice(xK)      = sum_i w_i * F2(xK,Q2_i) / sum_i w_i
        (relerr_slice)^2  = sum_i w_i * (relerr_i/100)^2 / sum_i w_i
      with w_i = Nexp_xK_Q2(xK,Q2_i).
    """

    apply_mpl_style()
    outdir = ensure_outdir(outdir)

    if q2_slices is None:
        q2_slices = [(0.0, 100.0), (100.0, 200.0), (200.0, 500.0)]

    if eval_cfg is None:
        eval_cfg = EvalConfig()

    print("[DEBUG] Nexp_xK_Q2: finite frac =", np.isfinite(Nexp_xK_Q2).mean(),
      "min =", np.nanmin(Nexp_xK_Q2), "max =", np.nanmax(Nexp_xK_Q2))
    print("[DEBUG] relerr_xK_Q2: finite frac =", np.isfinite(relerr_xK_Q2).mean(),
        "min% =", np.nanmin(relerr_xK_Q2), "max% =", np.nanmax(relerr_xK_Q2))

    setup_lhapdf_env()
    if not is_lhapdf_available():
        print("WARNING: LHAPDF not available -> cannot compute F2K model for slice plot.")
        return None

    if eval_cfg is None:
        eval_cfg = EvalConfig()

    pion_set = get_pion_pdfset()
    pion_member = get_pion_pdfmember()

    pdf = make_kaon_pdf_func(
        model="toy_baseline",
        toy=eval_cfg.toy,
        kparams=KaonModelParams(),
        pion_set=pion_set,
        pion_member=pion_member,
        require_lhapdf=True,
    )

    def F2_point(x: float, Q2: float) -> float:
        return float(F2_from_pdf_func(pdf, float(x), float(Q2)))

    def F2_on_grid(x_arr: np.ndarray, Q2_arr: np.ndarray) -> np.ndarray:
        """
        Return F2(x_i, Q2_j) as array shape (len(x_arr), len(Q2_arr)).
        """
        x_arr = np.asarray(x_arr, dtype=np.float64)
        Q2_arr = np.asarray(Q2_arr, dtype=np.float64)
        out = np.empty((x_arr.size, Q2_arr.size), dtype=np.float64)
        for j, q2 in enumerate(Q2_arr):
            # evaluate all x for this q2
            out[:, j] = np.fromiter((F2_point(x, q2) for x in x_arr), count=x_arr.size, dtype=np.float64)
        return out

    # slicing 

    xK_cent = 0.5 * (xK_edges[:-1] + xK_edges[1:])
    Q2_cent = 0.5 * (Q2_edges[:-1] + Q2_edges[1:])

    fig, ax = plt.subplots(figsize=(5, 5))

    for islc, (q2min, q2max) in enumerate(q2_slices):

        selQ = (Q2_cent >= q2min) & (Q2_cent < q2max)
        idxQ = np.where(selQ)[0]
        if idxQ.size == 0:
            continue

        F2_x_q = F2_on_grid(xK_cent, Q2_cent[idxQ])
        W = Nexp_xK_Q2[:, idxQ].astype(float)
        good = np.isfinite(F2_x_q) & np.isfinite(W) & (W > 0)
        W_eff  = np.where(good, W, 0.0)
        F2_eff = np.where(good, F2_x_q, 0.0)
        Ntot_slice = np.sum(W_eff, axis=1)
        F2_slice  = np.full_like(xK_cent, np.nan, dtype=float)
        rel_slice = np.full_like(xK_cent, np.nan, dtype=float)
        validx = Ntot_slice > 0
        if np.any(validx):
            F2_slice[validx] = np.sum(W_eff[validx] * F2_eff[validx], axis=1) / Ntot_slice[validx]
            rel_slice[validx] = 1.0 / np.sqrt(Ntot_slice[validx])
        yerr = F2_slice * rel_slice

        # sanity check
        med_rel = np.nanmedian(100 * rel_slice) if np.any(np.isfinite(rel_slice)) else np.nan
        med_ye  = np.nanmedian(yerr) if np.any(np.isfinite(yerr)) else np.nan
        print(f"[DEBUG slice {q2min:g}-{q2max:g}] valid xK frac = {validx.mean():.3f} "
              f"median rel% = {med_rel} median yerr = {med_ye}")

        lab = rf"${q2min:g}<Q^2<{q2max:g}\,\mathrm{{GeV}}^2$"

        okp = np.isfinite(F2_slice) & np.isfinite(yerr) & (yerr > 0)
        if np.any(okp):
            ax.errorbar(
                xK_cent[okp],
                F2_slice[okp],
                yerr=yerr[okp],
                fmt="s-",
                linewidth=1.5,
                markersize=4,
                capsize=2.5,
                label=lab,
            )

    ax.set_xlabel(r"$x_K$")
    ax.set_ylabel(r"$F_2^K(x_K)$ with projected uncertainties")
    ax.set_xlim(xK_range[0], xK_range[1])
    ax.set_ylim(0,1)

    if title is None:
        title = r"$F_2^K(x_K)$ with attached uncertainties from propagated $(x_K,Q^2)$ rel. errors"
    ax.set_title(title)

    if logx:
        ax.set_xscale("log")
    if logy:
        ax.set_yscale("log")

    if ymin is not None or ymax is not None:
        ax.set_ylim(bottom=ymin, top=ymax)

    ax.legend(frameon=False)
    fig.tight_layout()

    outpath = outdir / outname
    savefig(fig, outpath, dpi=200)
    return outpath

# high level plotting : chi2 between models

def plot_discriminant_kaon_sf_xK_Q2(
    *,
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
    vmax: float | None = None,
    modelA: str = "toy_baseline",
    modelB: str = "toy_hard_valence",
    toyA: ToyParams = ToyParams(),
    toyB: ToyParams | None = None,
    kparamsA: KaonModelParams = KaonModelParams(),
    kparamsB: KaonModelParams | None = None,
    sigma_ref: str = "A",  # "A" | "B" | "mean"
):
    """
    Build and plot a per-bin discrimination metric in (xK, Q2):
        chi2_ij = (F2_A - F2_B)^2 / sigma_ij^2

    where sigma_ij is built from the projected relative uncertainty relerr_xK_Q2 [%]
    returned by plot_relerr_kaon_sf_xK_Q2:
        sigma_ij = (relerr_ij/100) * F2_ref_ij
    with F2_ref = F2_A (default), or F2_B, or (F2_A+F2_B)/2.

    Returns: chi2_map, relerr_map, (F2_A, F2_B)
    """
    apply_mpl_style()
    outdir = ensure_outdir(outdir)

    relerr_xB_Q2, relerr_xK_Q2, extra = plot_relerr_kaon_sf_xK_Q2(
        beam=beam,
        nfiles=nfiles,
        root_base_dir=root_base_dir,
        suffix=suffix,
        gen_base_dir=gen_base_dir,
        outdir=outdir,
        tag=tag,
        xB_bins=xB_bins,
        xB_range=xB_range,
        xK_bins=xK_bins,
        xK_range=xK_range,
        Q2_bins=Q2_bins,
        Q2_range=Q2_range,
        log_Q2=log_Q2,
        tmax=tmax,
        lumin_fb=lumin_fb,
    )

    # binning

    xK_edges = np.linspace(xK_range[0], xK_range[1], xK_bins + 1)
    if log_Q2:
        Q2_edges = np.logspace(np.log10(Q2_range[0]), np.log10(Q2_range[1]), Q2_bins + 1)
    else:
        Q2_edges = np.linspace(Q2_range[0], Q2_range[1], Q2_bins + 1)

    xK_cent = 0.5 * (xK_edges[:-1] + xK_edges[1:])
    if log_Q2:
        Q2_cent = np.sqrt(Q2_edges[:-1] * Q2_edges[1:])
    else:
        Q2_cent = 0.5 * (Q2_edges[:-1] + Q2_edges[1:])

    # model pdf

    from config import setup_lhapdf_env, get_pion_pdfset, get_pion_pdfmember
    setup_lhapdf_env()
    pion_set = get_pion_pdfset()
    pion_member = get_pion_pdfmember()

    toyB = toyB or toyA
    kparamsB = kparamsB or kparamsA

    pdfA = make_kaon_pdf_func(
        model=modelA, toy=toyA, kparams=kparamsA,
        pion_set=pion_set, pion_member=pion_member, require_lhapdf=True
    )
    pdfB = make_kaon_pdf_func(
        model=modelB, toy=toyB, kparams=kparamsB,
        pion_set=pion_set, pion_member=pion_member, require_lhapdf=True
    )

    # pdf mapping

    F2A = np.full((xK_bins, Q2_bins), np.nan, dtype=np.float64)
    F2B = np.full((xK_bins, Q2_bins), np.nan, dtype=np.float64)

    for ix, x in enumerate(xK_cent):
        for iQ, Q2 in enumerate(Q2_cent):
            F2A[ix, iQ] = F2_from_pdf_func(pdfA, float(x), float(Q2))
            F2B[ix, iQ] = F2_from_pdf_func(pdfB, float(x), float(Q2))

    # relative error mapping

    rel = relerr_xK_Q2 / 100.0

    if sigma_ref == "A":
        Fref = F2A
    elif sigma_ref == "B":
        Fref = F2B
    elif sigma_ref == "mean":
        Fref = 0.5 * (F2A + F2B)
    else:
        raise ValueError("sigma_ref must be 'A', 'B', or 'mean'")

    sigma = rel * Fref

    # sanity check

    chi2 = np.full_like(F2A, np.nan, dtype=np.float64)
    ok = np.isfinite(F2A) & np.isfinite(F2B) & np.isfinite(sigma) & (sigma > 0) & np.isfinite(rel) & (rel > 0)
    chi2[ok] = (F2A[ok] - F2B[ok])**2 / (sigma[ok]**2)

    # plot chi2 maps

    q2_tag = "logQ2" if log_Q2 else "linQ2"
    title = rf"{beam}, $\mathcal{{L}}$={lumin_fb:g} fb$^{{-1}}$: {modelA} vs {modelB}"

    plot_relerr_map(
        np.sqrt(chi2),
        xK_edges,
        Q2_edges,
        xlabel=r"$x_K$",
        ylabel=r"$Q^2\ (\mathrm{GeV}^2)$",
        cbarlabel=r"Discrimination power $\sqrt{\chi^2}$ with projected uncertainties",
        title=title,
        outpath=outdir / f"chi2_xK_Q2_{beam}_{tag}_{modelA}_vs_{modelB}_L{lumin_fb:g}fb_{q2_tag}.png",
        log_y=log_Q2,
        vmax_percent=vmax,
    )

    return chi2, relerr_xK_Q2, (F2A, F2B)

# models ratio computation

def plot_F2K_ratio_xK_slices_to_reference(
    relerr_xK_Q2: np.ndarray,
    Nexp_xK_Q2: np.ndarray,
    xK_edges: np.ndarray,
    Q2_edges: np.ndarray,
    ref_model: str,
    models_to_compare: list[str],
    q2_slices: list[tuple[float, float]] | None = None,
    eval_cfg=None,
    outdir: str | Path = "./outputs",
    outname: str = "Discri_ratio_xK_slices.png",
    title: str | None = None,
    logx: bool = False,
    ymin: float | None = None,
    ymax: float | None = None,
    xK_range=(0, 1),
    Q2_range=(1, 500),
):
    """
    Plot F2K(xK) ratios in Q2 slices:
        ratio_model(xK) = F2_model(xK) / F2_ref(xK)

    The reference model appears as a horizontal line at 1.
    The projected experimental relative uncertainty is shown as a band around 1:
        1 ± relerr_slice

    For each Q2 slice, both the ratio and the uncertainty band are built using
    the same yield-weighted averaging as in plot_F2K_xK_slices_with_attached_errors.
    """

    apply_mpl_style()
    outdir = ensure_outdir(outdir)

    if q2_slices is None:
        q2_slices = [(0.0, 100.0), (100.0, 200.0), (200.0, 500.0)]

    if eval_cfg is None:
        eval_cfg = EvalConfig()

    print("[DEBUG] Nexp_xK_Q2: finite frac =", np.isfinite(Nexp_xK_Q2).mean(),
          "min =", np.nanmin(Nexp_xK_Q2), "max =", np.nanmax(Nexp_xK_Q2))
    print("[DEBUG] relerr_xK_Q2: finite frac =", np.isfinite(relerr_xK_Q2).mean(),
          "min% =", np.nanmin(relerr_xK_Q2), "max% =", np.nanmax(relerr_xK_Q2))

    setup_lhapdf_env()
    if not is_lhapdf_available():
        print("WARNING: LHAPDF not available -> cannot compute F2K ratio slice plot.")
        return None

    pion_set = get_pion_pdfset()
    pion_member = get_pion_pdfmember()

    # helpers 

    def _compute_model_map(model_name: str, x_arr: np.ndarray, q2_arr: np.ndarray) -> np.ndarray:
        """
        Return F2(x_i, Q2_j) as array shape (len(x_arr), len(q2_arr)).
        Works for both PDF-based models and direct JAM F2K replicas.
        """
        x_arr = np.asarray(x_arr, dtype=np.float64)
        q2_arr = np.asarray(q2_arr, dtype=np.float64)
        out = np.full((x_arr.size, q2_arr.size), np.nan, dtype=np.float64)

        jam_replica_map = {
            "jam25_rep165": 165,
            "jam25_rep390": 390,
            "jam25_rep400": 400,
        }

        if model_name == "jam25_mean":
            f2k = make_f2k_jam_mean()

            for j, q2 in enumerate(q2_arr):
                for i, x in enumerate(x_arr):
                    out[i, j] = float(f2k(float(x), float(q2)))

            return out

        if model_name in jam_replica_map:
            f2k = make_f2k_jam_replica(jam_replica_map[model_name])

            for j, q2 in enumerate(q2_arr):
                for i, x in enumerate(x_arr):
                    out[i, j] = float(f2k(float(x), float(q2)))

            return out

        pdf = make_kaon_pdf_func(
            model=model_name,
            toy=eval_cfg.toy,
            kparams=KaonModelParams(),
            pion_set=pion_set,
            pion_member=pion_member,
            require_lhapdf=True,
        )

        for j, q2 in enumerate(q2_arr):
            for i, x in enumerate(x_arr):
                out[i, j] = float(F2_from_pdf_func(pdf, float(x), float(q2)))

        return out

    def _weighted_q2_slice(A2d: np.ndarray, W2d: np.ndarray) -> np.ndarray:
        good = np.isfinite(A2d) & np.isfinite(W2d) & (W2d > 0)
        Aeff = np.where(good, A2d, 0.0)
        Weff = np.where(good, W2d, 0.0)
        denom = np.sum(Weff, axis=1)
        out = np.full(A2d.shape[0], np.nan, dtype=float)
        ok = denom > 0
        if np.any(ok):
            out[ok] = np.sum(Weff[ok] * Aeff[ok], axis=1) / denom[ok]
        return out

    all_models = [ref_model] + [m for m in models_to_compare if m != ref_model]

    # binning 

    xK_cent = 0.5 * (xK_edges[:-1] + xK_edges[1:])
    Q2_cent = 0.5 * (Q2_edges[:-1] + Q2_edges[1:])

    # Q2 slice pannel

    nslices = len(q2_slices)
    fig, axes = plt.subplots(
        nslices, 1,
        figsize=(5.0, 5.0 * nslices),
        sharex=True,
        squeeze=False,
    )
    axes = axes[:, 0]

    FONT = 12

    model_colors = {
        "jam25_rep165": "#5E3C99",
        "jam25_rep400": "#B24C7C",
        "jam25_rep390": "#3B5BA9",
        "toy_baseline": "#1F3A5F",
        "toy_soft_valence": "#3B5BA9",
        "toy_hard_valence": "#B24C7C",
        "toy_sea_enhanced": "#5E3C99",
        "toy_su3_breaking": "#2E8B57",
        "cosmao22": "#2E8B57",
    }

    model_markers = {
        "jam25_rep390": "o",
        "jam25_rep400": "s",
        "cosmao22": "^",
    }

    for ax, (q2min, q2max) in zip(axes, q2_slices):
        selQ = (Q2_cent >= q2min) & (Q2_cent < q2max)
        idxQ = np.where(selQ)[0]
        if idxQ.size == 0:
            ax.set_visible(False)
            continue

        W = Nexp_xK_Q2[:, idxQ].astype(float)
        good_rw = np.isfinite(W) & (W > 0)
        W_eff_rw = np.where(good_rw, W, 0.0)
        Ntot_slice = np.sum(W_eff_rw, axis=1)
        rel_slice = np.full_like(xK_cent, np.nan, dtype=float)
        validx_rw = Ntot_slice > 0
        if np.any(validx_rw):
            rel_slice[validx_rw] = 1.0 / np.sqrt(Ntot_slice[validx_rw])

        # reference model slice
        F2_ref_x_q = _compute_model_map(ref_model, xK_cent, Q2_cent[idxQ])
        good_ref = np.isfinite(F2_ref_x_q) & np.isfinite(W) & (W > 0)
        W_eff_ref = np.where(good_ref, W, 0.0)
        F2_ref_eff = np.where(good_ref, F2_ref_x_q, 0.0)
        sumW_ref = np.sum(W_eff_ref, axis=1)

        F2_ref_slice = np.full_like(xK_cent, np.nan, dtype=float)
        validx_ref = sumW_ref > 0

        if np.any(validx_ref):
            F2_ref_slice[validx_ref] = (
                np.sum(W_eff_ref[validx_ref] * F2_ref_eff[validx_ref], axis=1)
                / sumW_ref[validx_ref]
            )

        if ref_model=="jam25_mean":
            replica_ids = get_all_jam_replica_ids("JAM25kaon_nlonll_F2K")

            Frep = evaluate_f2k_for_jam_replicas(
                replica_ids=replica_ids,
                x_arr=xK_cent,
                q2_arr=Q2_cent[idxQ],
                setname="JAM25kaon_nlonll_F2K",
            )

            mean_rep = np.nanmean(Frep, axis=0)
            std_rep = np.nanstd(Frep, axis=0, ddof=1)

            mean_slice = _weighted_q2_slice(mean_rep, W)
            std_slice = _weighted_q2_slice(std_rep, W)

            spread_ratio = np.full_like(xK_cent, np.nan, dtype=float)
            ok_spread = (
                np.isfinite(mean_slice)
                & np.isfinite(std_slice)
                & np.isfinite(F2_ref_slice)
                & (F2_ref_slice > 0)
            )

            spread_ratio[ok_spread] = std_slice[ok_spread] / F2_ref_slice[ok_spread]

            ax.fill_between(
                xK_cent[ok_spread],
                1.0 - spread_ratio[ok_spread],
                1.0 + spread_ratio[ok_spread],
                color="#868E96",
                alpha=0.28,
                linewidth=0.0,
                #label=r"JAM replicas $1\sigma$ spread" if ax is axes[0] else None,
                zorder=0,
            )

        # horizontal reference line
        ax.axhline(
            1.0,
            linestyle="--",
            linewidth=1.5,
            label=f"{ref_model}" if ax is axes[0] else None,
            color='black'
        )

        # compare requested models to reference
        for model_name in models_to_compare:

            F2_mod_x_q = _compute_model_map(model_name, xK_cent, Q2_cent[idxQ])
            good_mod = np.isfinite(F2_mod_x_q) & np.isfinite(W) & (W > 0)
            W_eff_mod = np.where(good_mod, W, 0.0)
            F2_mod_eff = np.where(good_mod, F2_mod_x_q, 0.0)
            sumW_mod = np.sum(W_eff_mod, axis=1)

            F2_mod_slice = np.full_like(xK_cent, np.nan, dtype=float)
            validx_mod = sumW_mod > 0
            if np.any(validx_mod):
                F2_mod_slice[validx_mod] = (
                    np.sum(W_eff_mod[validx_mod] * F2_mod_eff[validx_mod], axis=1)
                    / sumW_mod[validx_mod]
                )

            ratio = np.full_like(xK_cent, np.nan, dtype=float)
            ok_ratio = (
                np.isfinite(F2_mod_slice)
                & np.isfinite(F2_ref_slice)
                & (F2_ref_slice > 0)
            )
            ratio[ok_ratio] = F2_mod_slice[ok_ratio] / F2_ref_slice[ok_ratio]
            
            yerr = ratio * rel_slice
            okp = np.isfinite(ratio) & np.isfinite(yerr) & (yerr >= 0)
            if np.any(okp):
                ax.errorbar(
                    xK_cent[okp],
                    ratio[okp],
                    yerr=yerr[okp],
                    fmt="-" + model_markers.get(model_name, "o"),
                    color=model_colors.get(model_name, "#222222"),
                    ecolor=model_colors.get(model_name, "#222222"),
                    linewidth=2.0 if model_name == "cosmao22" else 1.8,
                    elinewidth=2.0 if model_name == "cosmao22" else 1.8,
                    markersize=6 if model_name == "cosmao22" else 5,
                    capsize=2.5,
                    capthick=1.1,
                    label=(
                        "CoSMAO22 (DSE)" if model_name == "cosmao22"
                        else model_name
                    ),
                )

        ax.set_ylabel("Ratio", fontsize=FONT)
        ax.set_xlim(xK_range[0], xK_range[1])

        if ymin is not None or ymax is not None:
            ax.set_ylim(bottom=ymin, top=ymax)

        ax.legend(
            title=rf"${q2min:g}<Q^2<{q2max:g}\,\mathrm{{GeV}}^2$",
            loc="upper center",
            ncol=1,
            frameon=False,
            fontsize=10,
            title_fontsize=10,
        )

        ax.tick_params(axis="both", which="major", direction="in", length=7, width=1.2, labelsize=FONT)
        ax.tick_params(axis="both", which="minor", direction="in", length=4, width=1.0)
        ax.tick_params(top=False, right=True)

        for spine in ax.spines.values():
            spine.set_linewidth(1.2)

    axes[-1].set_xlabel(r"$x_K$", fontsize=FONT)
    ax.set_xscale("log")
    ax.set_xlim(1e-3, 1.0)
    ax.set_yticks([0.5, 1.0, 1.5, 2.0])
    ax.xaxis.set_major_locator(FixedLocator([1e-3, 1e-2, 1e-1, 1.0]))
    ax.xaxis.set_major_formatter(
        FixedFormatter([r"$10^{-3}$", r"$10^{-2}$", r"$10^{-1}$", r"$1$"])
    )
    ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1))
    ax.xaxis.set_minor_formatter(NullFormatter())

    ax.tick_params(
        axis="x",
        which="major",
        direction="in",
        bottom=True,
        top=False,
        length=7,
        width=1.2,
        labelsize=FONT,
    )

    ax.tick_params(
        axis="x",
        which="minor",
        direction="in",
        bottom=True,
        top=False,
        length=4,
        width=1.0,
    )

    ax.tick_params(
        axis="y",
        which="major",
        direction="in",
        left=True,
        right=True,
        length=7,
        width=1.2,
        labelsize=FONT,
    )

    ax.tick_params(
        axis="y",
        which="minor",
        direction="in",
        left=True,
        right=True,
        length=4,
        width=1.0,
    )

    fig.suptitle(title,fontsize=FONT)

    outpath = outdir / outname
    savefig(fig, outpath, dpi=200)
    return outpath

# high level plotting : models discriminating ratio

def plot_ratio_kaon_sf_xK_Q2(
    *,
    beam: str,
    nfiles: int,
    root_base_dir: Path,
    suffix: str,
    gen_base_dir: Path,
    outdir: Path,
    tag: str,
    ref_model: str,
    models_to_compare: list[str],
    q2_slices: list[tuple[float, float]] | None = None,
    xB_bins: int = 20,
    xB_range: tuple[float, float] = (0.0, 1.0),
    xK_bins: int = 20,
    xK_range: tuple[float, float] = (0.0, 1.0),
    Q2_bins: int = 20,
    Q2_range: tuple[float, float] = (1.0, 500.0),
    log_Q2: bool = True,
    tmax: float | None = None,
    lumin_fb: float = 1.0,
    eval_cfg=None,
    outname: str = "Discri_ratio_xK_slices.png",
    title: str | None = None,
    logx: bool = False,
    ymin: float | None = None,
    ymax: float | None = None,
    kinmethod: str = "Truth",
):
    """
    High-level wrapper:
      - compute projected rel. uncertainties and expected yields in (xK,Q2)
      - plot F2K ratios to a reference model in chosen Q2 slices
    """
    apply_mpl_style()
    outdir = ensure_outdir(outdir)

    relerr_xB_Q2, relerr_xK_Q2, extra = plot_relerr_kaon_sf_xK_Q2(
        beam=beam,
        nfiles=nfiles,
        root_base_dir=root_base_dir,
        suffix=suffix,
        gen_base_dir=gen_base_dir,
        outdir=outdir,
        tag=tag,
        xB_bins=xB_bins,
        xB_range=xB_range,
        xK_bins=xK_bins,
        xK_range=xK_range,
        Q2_bins=Q2_bins,
        Q2_range=Q2_range,
        log_x=logx,
        log_Q2=log_Q2,
        tmax=tmax,
        lumin_fb=lumin_fb, 
        vmax_percent=100,
        kinmethod=kinmethod,
    )

    Nexp_xK_Q2 = extra["Nexp_xK_Q2_reco"]

    if logx:
        if xB_range[0] <= 0 or xB_range[1] <= 0:
            raise ValueError("xB_range must be strictly positive when log_x=True")
    if log_Q2:
        if Q2_range[0] <= 0 or Q2_range[1] <= 0:
            raise ValueError("Q2_range must be strictly positive when log_Q2=True")

    if logx:
        xK_edges = np.logspace(np.log10(xK_range[0]), np.log10(xK_range[1]), xK_bins + 1)
    else:
        xK_edges = np.linspace(xK_range[0], xK_range[1], xK_bins + 1)

    if log_Q2:
        Q2_edges = np.logspace(np.log10(Q2_range[0]), np.log10(Q2_range[1]), Q2_bins + 1)
    else:
        Q2_edges = np.linspace(Q2_range[0], Q2_range[1], Q2_bins + 1)

    return plot_F2K_ratio_xK_slices_to_reference(
        relerr_xK_Q2=relerr_xK_Q2,
        Nexp_xK_Q2=Nexp_xK_Q2,
        xK_range=xK_range,
        Q2_range=Q2_range,
        xK_edges=xK_edges,
        Q2_edges=Q2_edges,
        ref_model=ref_model,
        models_to_compare=models_to_compare,
        q2_slices=q2_slices,
        eval_cfg=eval_cfg,
        outdir=outdir,
        outname=outname,
        title=title,
        logx=logx,
        ymin=ymin,
        ymax=ymax,
    )

# high level plotting : constraints JAM replicas

def plot_jam_reweighting_constraining_power_xK_slices(
    *,
    beam: str,
    nfiles: int,
    root_base_dir: Path,
    suffix: str,
    gen_base_dir: Path,
    outdir: Path,
    tag: str,
    q2_slices: list[tuple[float, float]] | None = None,
    xB_bins: int = 20,
    xB_range: tuple[float, float] = (1e-3, 1.0),
    xK_bins: int = 20,
    xK_range: tuple[float, float] = (1e-3, 1.0),
    Q2_bins: int = 20,
    Q2_range: tuple[float, float] = (1e-3, 500.0),
    log_Q2: bool = True,
    logx: bool = True,
    tmax: float | None = None,
    lumin_fb: float | list[float] = 1.0,
    kinmethod: str = "Truth",
    jam_setname: str = "JAM25kaon_nlonll_F2K",
    replica_ids: list[int] | None = None,
    truth_mode: str = "mean",
    component: str = "total",  # "total", "valence", "sea", "gluon"
    outname: str = "jam_reweighting_constraining_power.png",
    title: str | None = None,
):
    apply_mpl_style()
    outdir = ensure_outdir(outdir)

    component_labels = {
        "total": r"$F_2^K$",
        "valence": r"valence contribution to $F_2^K$",
        "sea": r"quark-sea contribution to $F_2^K$",
        "gluon": r"gluon-sea contribution to $F_2^K$",
    }

    if component not in component_labels:
        raise ValueError(
            "component must be 'total', 'valence', 'sea', or 'gluon'."
        )

    ylabel = component_labels[component]

    if outname == "jam_reweighting_constraining_power.png":
        outname = f"jam_reweighting_constraining_power_{component}.png"

    if np.isscalar(lumin_fb):
        lumin_list = [float(lumin_fb)]
    else:
        lumin_list = [float(L) for L in lumin_fb]

    lumin_list = sorted(lumin_list)

    if q2_slices is None:
        q2_slices = [(0.01, 500.0)]

    if logx:
        xK_edges = np.logspace(np.log10(xK_range[0]), np.log10(xK_range[1]), xK_bins + 1)
    else:
        xK_edges = np.linspace(xK_range[0], xK_range[1], xK_bins + 1)

    if log_Q2:
        Q2_edges = np.logspace(np.log10(Q2_range[0]), np.log10(Q2_range[1]), Q2_bins + 1)
    else:
        Q2_edges = np.linspace(Q2_range[0], Q2_range[1], Q2_bins + 1)

    xK_cent = 0.5 * (xK_edges[:-1] + xK_edges[1:])
    Q2_cent = 0.5 * (Q2_edges[:-1] + Q2_edges[1:])

    if replica_ids is None:
        replica_ids = get_all_jam_replica_ids(jam_setname)

    Frep_total = evaluate_f2k_for_jam_replicas(
        replica_ids=replica_ids,
        x_arr=xK_cent,
        q2_arr=Q2_cent,
        setname=jam_setname,
    )

    if component == "total":
        Frep_plot = Frep_total
    else:
        Frep_plot = evaluate_f2k_component_for_jam_replicas(
            replica_ids=replica_ids,
            x_arr=xK_cent,
            q2_arr=Q2_cent,
            component=component,
            setname=jam_setname,
        )

    if truth_mode == "mean":
        F_data = np.nanmean(Frep_total, axis=0)
    elif truth_mode == "median":
        F_data = np.nanmedian(Frep_total, axis=0)
    else:
        raise ValueError("truth_mode must be 'mean' or 'median'")

    mean_prior = np.nanmean(Frep_plot, axis=0)
    std_prior = np.nanstd(Frep_plot, axis=0, ddof=1)

    def weighted_q2_slice(A2d: np.ndarray, W2d: np.ndarray) -> np.ndarray:
        good = np.isfinite(A2d) & np.isfinite(W2d) & (W2d > 0)
        Aeff = np.where(good, A2d, 0.0)
        Weff = np.where(good, W2d, 0.0)
        denom = np.sum(Weff, axis=1)

        out = np.full(A2d.shape[0], np.nan, dtype=float)
        ok = denom > 0
        if np.any(ok):
            out[ok] = np.sum(Weff[ok] * Aeff[ok], axis=1) / denom[ok]
        return out

    post_results = {}

    for L in lumin_list:
        relerr_xB_Q2, relerr_xK_Q2, extra = plot_relerr_kaon_sf_xK_Q2(
            beam=beam,
            nfiles=nfiles,
            root_base_dir=root_base_dir,
            suffix=suffix,
            gen_base_dir=gen_base_dir,
            outdir=outdir,
            tag=tag,
            xB_bins=xB_bins,
            xB_range=xB_range,
            xK_bins=xK_bins,
            xK_range=xK_range,
            Q2_bins=Q2_bins,
            Q2_range=Q2_range,
            log_x=logx,
            log_Q2=log_Q2,
            tmax=tmax,
            lumin_fb=L,
            vmax_percent=100.0,
            kinmethod=kinmethod,
        )

        Nexp_xK_Q2 = extra["Nexp_xK_Q2_reco"]

        sigma = (relerr_xK_Q2 / 100.0) * F_data
        valid = np.isfinite(F_data) & np.isfinite(sigma) & (sigma > 0)

        chi2 = np.full(Frep_total.shape[0], np.nan, dtype=float)
        for k in range(Frep_total.shape[0]):
            ok = valid & np.isfinite(Frep_total[k])
            if np.any(ok):
                chi2[k] = np.sum(((Frep_total[k][ok] - F_data[ok]) / sigma[ok]) ** 2)

        chi2_min = np.nanmin(chi2)
        w = np.exp(-0.5 * (chi2 - chi2_min))
        w[~np.isfinite(w)] = 0.0

        if np.sum(w) <= 0:
            raise RuntimeError(f"All JAM replica weights vanished for L = {L:g} fb^-1.")

        w /= np.sum(w)

        mean_post = np.nansum(w[:, None, None] * Frep_plot, axis=0)
        var_post = np.nansum(
            w[:, None, None] * (Frep_plot - mean_post[None, :, :])**2,
            axis=0,
        )
        std_post = np.sqrt(np.maximum(var_post, 0.0))

        post_results[L] = {
            "relerr_xK_Q2": relerr_xK_Q2,
            "Nexp_xK_Q2": Nexp_xK_Q2,
            "weights": w,
            "chi2": chi2,
            "mean_post": mean_post,
            "std_post": std_post,
        }

    prior_color = "#495057"
    base_colors = [
        "#A5D8FF",
        "#4DABF7",
        "#1C7ED6",
        "#1864AB",
    ]

    post_colors = {
        L: base_colors[i % len(base_colors)]
        for i, L in enumerate(lumin_list)
    }

    nslices = len(q2_slices)
    fig, axes = plt.subplots(
        nslices,
        1,
        figsize=(5, 5 * nslices),
        sharex=True,
        squeeze=False,
    )
    axes = axes[:, 0]

    for ax, (q2min, q2max) in zip(axes, q2_slices):
        idxQ = np.where((Q2_cent >= q2min) & (Q2_cent < q2max))[0]

        if idxQ.size == 0:
            ax.set_visible(False)
            continue

        W_prior = post_results[lumin_list[-1]]["Nexp_xK_Q2"][:, idxQ].astype(float)

        prior_mean_slice = weighted_q2_slice(mean_prior[:, idxQ], W_prior)
        prior_std_slice = weighted_q2_slice(std_prior[:, idxQ], W_prior)

        ok_prior = np.isfinite(prior_mean_slice) & np.isfinite(prior_std_slice)

        if np.any(ok_prior):
            ax.fill_between(
                xK_cent[ok_prior],
                prior_mean_slice[ok_prior] - prior_std_slice[ok_prior],
                prior_mean_slice[ok_prior] + prior_std_slice[ok_prior],
                color=prior_color,
                alpha=0.35,
                linewidth=0.0,
                label="Before EIC",
                zorder=1,
            )

        for iL, L in enumerate(lumin_list):
            res = post_results[L]
            W = res["Nexp_xK_Q2"][:, idxQ].astype(float)

            post_mean_slice = weighted_q2_slice(res["mean_post"][:, idxQ], W)
            post_std_slice = weighted_q2_slice(res["std_post"][:, idxQ], W)

            ok_post = np.isfinite(post_mean_slice) & np.isfinite(post_std_slice)

            if np.any(ok_post):
                ax.fill_between(
                    xK_cent[ok_post],
                    post_mean_slice[ok_post] - post_std_slice[ok_post],
                    post_mean_slice[ok_post] + post_std_slice[ok_post],
                    color=post_colors[L],
                    alpha=0.6,
                    linewidth=0.0,
                    label=rf"After EIC, ${L:g}\,\mathrm{{fb}}^{{-1}}$",
                    zorder=2 + iL,
                )

        ax.set_ylabel(ylabel, fontsize=13)

        ax.set_xlim(xK_range)
        ax.set_ylim(0.0, 1.0)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8])

        if logx:
            ax.set_xscale("log")
            ax.xaxis.set_major_locator(FixedLocator([1e-3, 1e-2, 1e-1, 1.0]))
            ax.xaxis.set_major_formatter(
                FixedFormatter([r"$10^{-3}$", r"$10^{-2}$", r"$10^{-1}$", r"$1$"])
            )
            ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1))
            ax.xaxis.set_minor_formatter(NullFormatter())

        ax.tick_params(
            axis="x",
            which="major",
            direction="in",
            bottom=True,
            top=False,
            length=7,
            width=1.2,
            labelsize=13,
        )
        ax.tick_params(
            axis="x",
            which="minor",
            direction="in",
            bottom=True,
            top=False,
            length=4,
            width=1.0,
        )
        ax.tick_params(
            axis="y",
            which="major",
            direction="in",
            left=True,
            right=True,
            length=7,
            width=1.2,
            labelsize=13,
        )
        ax.tick_params(
            axis="y",
            which="minor",
            direction="in",
            left=True,
            right=True,
            length=4,
            width=1.0,
        )

        for spine in ax.spines.values():
            spine.set_linewidth(1.1)

        ax.legend(
            title=rf"${q2min:g} < Q^2 < {q2max:g}\,\mathrm{{GeV}}^2$",
            loc="upper right",
            frameon=False,
            fontsize=11,
            title_fontsize=11,
        )

    axes[-1].set_xlabel(r"$x_K$", fontsize=13)
    
    if title is not None:
        fig.suptitle(
            title,
            fontsize=13,
            x=0.545,
            y=0.985,
            ha="center",
        )

    fig.subplots_adjust(
        left=0.14,
        right=0.95,
        top=0.86,
        bottom=0.12,
    )

    outpath = outdir / outname
    savefig(fig, outpath, dpi=250)

    return {
        "outpath": outpath,
        "replica_ids": replica_ids,
        "lumin_list": lumin_list,
        "component": component,
        "post_results": post_results,
        "mean_prior": mean_prior,
        "std_prior": std_prior,
        "F_data": F_data,
    }

# high level plotting : reduction JAM replicas

def plot_neff_reduction_vs_lumi_by_beam(
    results_by_beam: dict,
    *,
    outdir: Path,
    outname: str,
    title: str | None = None,
):
    apply_mpl_style()
    outdir = ensure_outdir(outdir)

    beam_colors = {
        "5x41": "#2B8A3E",
        "10x100": "#1C7ED6",
        "18x275": "#C92A2A",
    }

    beam_markers = {
        "5x41": "o",
        "10x100": "s",
        "18x275": "^",
    }

    fig, ax = plt.subplots(figsize=(5.2,5.2))

    all_reductions = []

    for beam, res in results_by_beam.items():
        replica_ids = res["replica_ids"]
        lumin_list = np.asarray(res["lumin_list"], dtype=float)
        post_results = res["post_results"]

        nrep = len(replica_ids)

        reductions = []

        for L in lumin_list:
            w = np.asarray(post_results[L]["weights"], dtype=float)
            w = w / np.sum(w)

            neff = 1.0 / np.sum(w**2)
            reduction = 100.0 * (1.0 - neff / nrep)

            reductions.append(reduction)

        reductions = np.asarray(reductions)
        all_reductions.extend(reductions[np.isfinite(reductions)])

        ax.plot(
            lumin_list,
            reductions,
            marker=beam_markers.get(beam, "o"),
            markersize=6.5,
            linewidth=2.2,
            color=beam_colors.get(beam, None),
            label=beam,
        )

    ax.set_xlabel(r"Luminosity (fb$^{-1}$)", fontsize=13)
    ax.set_ylabel(r"Replica reduction (%)", fontsize=13)

    ax.set_xscale("log")
    ax.set_xticks([5, 10, 50])
    ax.set_xticklabels([r"$5$", r"$10$", r"$50$"])

    ymin = -2.0
    ymax = max(all_reductions) if len(all_reductions) else 5.0
    ax.set_ylim(ymin, 1.25 * ymax + 1.0)

    # Style ticks
    ax.tick_params(
        axis="both",
        which="major",
        direction="in",
        top=True,
        right=True,
        length=6,
        width=1.1,
        labelsize=12,
    )

    ax.tick_params(
        axis="both",
        which="minor",
        direction="in",
        top=True,
        right=True,
        length=3,
        width=0.9,
    )

    for spine in ax.spines.values():
        spine.set_linewidth(1.1)

    ax.legend(
        frameon=False,
        fontsize=12,
        loc="upper left",
    )

    if title is not None:
        fig.suptitle(title, fontsize=13, y=0.945)

    fig.subplots_adjust(left=0.16, right=0.96, top=0.84, bottom=0.16)

    outpath = outdir / outname
    savefig(fig, outpath, dpi=250)

    return outpath