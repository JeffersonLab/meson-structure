import argparse
import os
import matplotlib.pyplot as plt
import scipy as sp 
import numpy as np
import pandas as pd
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable

# column names expected in concatenated DataFrame (true MC values)
PX_MC_COL = "mc_elec_px"
PY_MC_COL = "mc_elec_py"
PZ_MC_COL = "mc_elec_pz"
xbjk_MC_COL = "mc_x"
Q2_MC_COL = "mc_q2"
Y_MC_COL = "mc_y"

# column names expected in concatenated DataFrame (Reconstructed Values) (Electron Method)
PX_COL = "elec_px"
PY_COL = "elec_py"
PZ_COL = "elec_pz"
xbjk_COL = "electron_x"
Q2_COL = "electron_q2"
E_COL = "elec_energy"
Y_COL = "electron_y"

# Double Angle Method
xbjk_DA_COL = "da_x"
Q2_DA_COL = "da_q2"
Y_DA_COL = "da_y"

# E Sigma Method
xbjk_ESIG_COL = "esigma_x"
Q2_ESIG_COL = "esigma_q2"
Y_ESIG_COL = "esigma_y"

# Jaquet-Blondel Method
xbjk_JB_COL = "jb_x"
Q2_JB_COL = "jb_q2"
Y_JB_COL = "jb_y"

# Sigma Method
xbjk_SIG_COL = "sigma_x"
Q2_SIG_COL = "sigma_q2"
Y_SIG_COL = "sigma_y"


def process_and_mask(file):
    """
    Return a dict with numeric arrays for px,py,pz and derived kinematics.
    Only events where reconstructed kinematics are present are kept (so MC and reco align).
    """

    # ---------- load data ----------

    suffix = file.lower()
    if ".parquet" or ".parq" in (suffix):
        df = pd.read_parquet(file)
    elif ".feather" in (suffix):
        df = pd.read_feather(file)
    elif ".csv" or ".txt" in (suffix):
        # read only the columns we need (fast & memory friendly)
        df = pd.read_csv(file)
    else:
        raise ValueError(f"Unsupported acceptance file type: {suffix}")
    df = pd.read_parquet(file, engine="pyarrow")
    if df is None or df.empty:
        print("  -> concatenated dataframe empty or None")

    # ---------- coerce important columns to numeric (in-place) ----------
    reco_needed   = [PX_COL, PY_COL, PZ_COL, xbjk_COL, Q2_COL, E_COL, Y_COL]
    mc_needed     = [PX_MC_COL, PY_MC_COL, PZ_MC_COL, xbjk_MC_COL, Q2_MC_COL, Y_MC_COL]
    DA_needed     = [xbjk_DA_COL, Q2_DA_COL, Y_DA_COL]
    ESIGMA_needed = [xbjk_ESIG_COL, Q2_ESIG_COL, Y_ESIG_COL]
    JB_needed     = [xbjk_JB_COL, Q2_JB_COL, Y_JB_COL]
    SIGMA_needed  = [xbjk_SIG_COL, Q2_SIG_COL, Y_SIG_COL]

    df[reco_needed]   = df[reco_needed].apply(pd.to_numeric, errors="coerce")
    df[mc_needed]     = df[mc_needed].apply(pd.to_numeric, errors="coerce")
    df[DA_needed]     = df[DA_needed].apply(pd.to_numeric, errors="coerce")
    df[ESIGMA_needed] = df[ESIGMA_needed].apply(pd.to_numeric, errors="coerce")
    df[JB_needed]     = df[JB_needed].apply(pd.to_numeric, errors="coerce")
    df[SIGMA_needed]  = df[SIGMA_needed].apply(pd.to_numeric, errors="coerce")

    # ---------- build masks ----------
    reco_complete_mask = df[reco_needed].notna().all(axis=1)
    mc_complete_mask   = df[mc_needed].notna().all(axis=1)
    DA_mask            = df[DA_needed].notna().all(axis=1)
    ESIGMA_mask        = df[ESIGMA_needed].notna().all(axis=1)
    JB_mask            = df[JB_needed].notna().all(axis=1)
    SIGMA_mask         = df[SIGMA_needed].notna().all(axis=1)

    matched_mask = reco_complete_mask & mc_complete_mask & DA_mask & ESIGMA_mask & JB_mask & SIGMA_mask

    n_total   = len(df)
    n_reco    = int(reco_complete_mask.sum())
    n_mc      = int(mc_complete_mask.sum())
    n_matched = int(matched_mask.sum())
    print(f"Total events: {n_total}; reco-complete: {n_reco}; mc-complete: {n_mc}; matched: {n_matched}")

    if n_matched == 0:
        print("  -> No matched (reco+mc) events found; returning None")

    df_matched = df.loc[matched_mask].copy()

    # ---------- MC arrays ----------
    px_mc = df_matched[PX_MC_COL].to_numpy()
    py_mc = df_matched[PY_MC_COL].to_numpy()
    pz_mc = df_matched[PZ_MC_COL].to_numpy()
    x_mc  = df_matched[xbjk_MC_COL].to_numpy()
    q2_mc = df_matched[Q2_MC_COL].to_numpy()
    y_mc  = df_matched[Y_MC_COL].to_numpy()

    pt_mc = np.sqrt(px_mc**2 + py_mc**2)
    p_mc  = np.sqrt(px_mc**2 + py_mc**2 + pz_mc**2)
    E_mc  = p_mc.copy()
    with np.errstate(invalid="ignore", divide="ignore"):
        theta_mc = np.arccos(np.clip(pz_mc / p_mc, -1.0, 1.0))
    eta_mc = -np.log(np.tan(theta_mc / 2.0))
    phi_mc = np.arctan2(py_mc, px_mc)

    # ---------- reco arrays ----------
    px = df_matched[PX_COL].to_numpy()
    py = df_matched[PY_COL].to_numpy()
    pz = df_matched[PZ_COL].to_numpy()
    x  = df_matched[xbjk_COL].to_numpy()
    q2 = df_matched[Q2_COL].to_numpy()
    E_reco = df_matched[E_COL].to_numpy()
    y  = df_matched[Y_COL].to_numpy()

    pt = np.sqrt(px**2 + py**2)
    p  = np.sqrt(px**2 + py**2 + pz**2)
    with np.errstate(invalid="ignore", divide="ignore"):
        theta = np.arccos(np.clip(pz / p, -1.0, 1.0))
    eta = -np.log(np.tan(theta / 2.0))
    phi = np.arctan2(py, px)

    # ---------- alternative method arrays ----------
    x_DA     = df_matched[xbjk_DA_COL].to_numpy()
    q2_DA    = df_matched[Q2_DA_COL].to_numpy()
    y_DA     = df_matched[Y_DA_COL].to_numpy()

    x_JB     = df_matched[xbjk_JB_COL].to_numpy()
    q2_JB    = df_matched[Q2_JB_COL].to_numpy()
    y_JB     = df_matched[Y_JB_COL].to_numpy()

    x_SIGMA  = df_matched[xbjk_SIG_COL].to_numpy()
    q2_SIGMA = df_matched[Q2_SIG_COL].to_numpy()
    y_SIGMA  = df_matched[Y_SIG_COL].to_numpy()

    x_ESIGMA  = df_matched[xbjk_ESIG_COL].to_numpy()
    q2_ESIGMA = df_matched[Q2_ESIG_COL].to_numpy()
    y_ESIGMA  = df_matched[Y_ESIG_COL].to_numpy()

    return {
        "n_total": n_total, "n_reco": n_reco, "n_mc": n_mc, "n_matched": n_matched,
        "px_mc": px_mc, "py_mc": py_mc, "pz_mc": pz_mc,
        "pt_mc": pt_mc, "p_mc": p_mc, "theta_mc": theta_mc, "eta_mc": eta_mc, "phi_mc": phi_mc,
        "x_mc": x_mc, "q2_mc": q2_mc, "E_mc": E_mc, "y_mc": y_mc,
        "px": px, "py": py, "pz": pz,
        "pt": pt, "p": p, "theta": theta, "eta": eta, "phi": phi,
        "x": x, "q2": q2, "E_reco": E_reco, "y": y,
        "x_DA": x_DA, "q2_DA": q2_DA, "y_DA": y_DA,
        "x_JB": x_JB, "q2_JB": q2_JB, "y_JB": y_JB,
        "x_SIGMA": x_SIGMA, "q2_SIGMA": q2_SIGMA, "y_SIGMA": y_SIGMA,
        "x_ESIGMA": x_ESIGMA, "q2_ESIGMA": q2_ESIGMA, "y_ESIGMA": y_ESIGMA,
    }


def plot_reco_vs_true_all(file,
                          results_dir="results",
                          reco_methods=None,
                          reco_Q2=None,
                          reco_y=None,
                          reco_x=None,
                          nbins_q2=200,
                          nbins_y=100,
                          cmap="viridis",
                          figsize=(14, 18)):

    if reco_methods is None:
        reco_methods = ["Electron Method", "Double Angle", "Jaquet-Blondel", "Sigma", "ESigma"]
    if reco_Q2 is None:
        reco_Q2 = ["q2", "q2_DA", "q2_JB", "q2_SIGMA", "q2_ESIGMA"]
    if reco_y is None:
        reco_y = ["y", "y_DA", "y_JB", "y_SIGMA", "y_ESIGMA"]
    if reco_x is None:
        reco_x = ["x", "x_DA", "x_JB", "x_SIGMA", "x_ESIGMA"]

    df = process_and_mask(file)
    df = pd.DataFrame(df)

    nmethods = len(reco_methods)
    if not (len(reco_Q2) == nmethods == len(reco_y) == len(reco_x)):
        raise ValueError("reco_methods, reco_Q2, reco_y, reco_x must have the same length")

    fig, axes = plt.subplots(nmethods, 3, figsize=figsize, constrained_layout=False)
    fig.subplots_adjust(hspace=0.35, wspace=0.45, right=0.92)

    for i, method in enumerate(reco_methods):
        ax_q2 = axes[i, 0]
        ax_y  = axes[i, 1]
        ax_x  = axes[i, 2]

        q2_col = reco_Q2[i]
        y_col  = reco_y[i]
        x_col  = reco_x[i]

        # ---------- Q2 ----------
        mask_q2 = np.isfinite(df["q2_mc"]) & np.isfinite(df[q2_col]) & (df["q2_mc"] > 0) & (df[q2_col] > 0)
        xq = df.loc[mask_q2, "q2_mc"].to_numpy()
        yq = df.loc[mask_q2, q2_col].to_numpy()

        if len(xq) > 10:
            xedges = np.logspace(np.log10(xq.min()), np.log10(xq.max()), nbins_q2 + 1)
            yedges = np.logspace(np.log10(yq.min()), np.log10(yq.max()), nbins_q2 + 1)
            im_q2 = ax_q2.hist2d(xq, yq, bins=(xedges, yedges), norm=LogNorm(vmin=1), cmin=1, cmap=cmap)
            ax_q2.set_xscale('log'); ax_q2.set_yscale('log')
            ax_q2.set_xlim(10e0, 10e2); ax_q2.set_ylim(10e0, 10e2)
            ax_q2.set_xlabel(r"$Q^2_{true}$ $(\mathrm{GeV}/c)^2$")
            ax_q2.set_ylabel(r"$Q^2_{reco}$ $(\mathrm{GeV}/c)^2$")
            ax_q2.set_title(f"{method} — Q²")
            line_coords = np.logspace(np.log10(min(xedges[0], yedges[0])), np.log10(max(xedges[-1], yedges[-1])), 100)
            ax_q2.plot(line_coords, line_coords, 'r--', linewidth=1.2)
            divider = make_axes_locatable(ax_q2)
            cax = divider.append_axes("right", size="4%", pad=0.06)
            fig.colorbar(im_q2[3], cax=cax).set_label("counts")
        else:
            ax_q2.text(0.5, 0.5, "Insufficient Q2 data", ha='center', va='center')

        # ---------- x ----------
        mask_x = np.isfinite(df["x_mc"]) & np.isfinite(df[x_col]) & (df["x_mc"] > 0) & (df[x_col] > 0)
        xx = df.loc[mask_x, "x_mc"].to_numpy()
        yx = df.loc[mask_x, x_col].to_numpy()

        if len(xx) > 10:
            xedges_x = np.logspace(np.log10(xx.min()), np.log10(xx.max()), nbins_q2 + 1)
            yedges_x = np.logspace(np.log10(yx.min()), np.log10(yx.max()), nbins_q2 + 1)
            im_x = ax_x.hist2d(xx, yx, bins=(xedges_x, yedges_x), norm=LogNorm(vmin=1), cmin=1, cmap=cmap)
            ax_x.set_xscale('log'); ax_x.set_yscale('log')
            ax_x.set_xlim(10e-5, 10e-1); ax_x.set_ylim(10e-5, 10e-1)
            ax_x.set_xlabel(r"$x_{true}$"); ax_x.set_ylabel(r"$x_{reco}$")
            ax_x.set_title(f"{method} — x")
            line_coords = np.logspace(np.log10(min(xedges_x[0], yedges_x[0])), np.log10(max(xedges_x[-1], yedges_x[-1])), 100)
            ax_x.plot(line_coords, line_coords, 'r--', linewidth=1.2)
            divider = make_axes_locatable(ax_x)
            cax = divider.append_axes("right", size="4%", pad=0.06)
            fig.colorbar(im_x[3], cax=cax).set_label("counts")
        else:
            ax_x.text(0.5, 0.5, "Insufficient x data", ha='center', va='center')

        # ---------- y ----------
        mask_y = np.isfinite(df["y_mc"]) & np.isfinite(df[y_col])
        xy = df.loc[mask_y, "y_mc"].to_numpy()
        yy = df.loc[mask_y, y_col].to_numpy()

        if len(xy) > 10:
            im_y = ax_y.hist2d(xy, yy, bins=(nbins_y, nbins_y), range=((0, 1), (0, 1)), norm=LogNorm(vmin=1), cmin=1, cmap=cmap)
            ax_y.set_xlim(0, 1); ax_y.set_ylim(0, 1)
            ax_y.set_xlabel(r"$y_{true}$"); ax_y.set_ylabel(r"$y_{reco}$")
            ax_y.set_title(f"{method} — y")
            ax_y.plot(np.linspace(0, 1, 100), np.linspace(0, 1, 100), 'r--', linewidth=1.0)
            divider = make_axes_locatable(ax_y)
            cax = divider.append_axes("right", size="4%", pad=0.06)
            fig.colorbar(im_y[3], cax=cax).set_label("counts")
        else:
            ax_y.text(0.5, 0.5, "Insufficient y data", ha='center', va='center')

    plt.tight_layout()

    # ---------- save to results directory ----------
    os.makedirs(results_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(file))[0]   # e.g. "18x275_Reco_data"
    out_path = os.path.join(results_dir, f"{stem}_reco_vs_true.png")
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    print(f"Saved: {out_path}")
    plt.close(fig)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Plot reco-vs-true kinematic comparisons for DIS Sullivan process events."
    )
    parser.add_argument(
        "file",
        help="Path to input .parquet data file"
    )
    parser.add_argument(
        "--results-dir", "-o",
        default="results",
        help="Directory to write output into (created if absent). Default: ./results"
    )
    parser.add_argument(
        "--nbins-q2", type=int, default=200,
        help="Number of bins for Q2 and x 2D histograms. Default: 200"
    )
    parser.add_argument(
        "--nbins-y", type=int, default=100,
        help="Number of bins for y 2D histogram. Default: 100"
    )
    parser.add_argument(
        "--cmap", default="viridis",
        help="Matplotlib colormap name. Default: viridis"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    plot_reco_vs_true_all(
        file=args.file,
        results_dir=args.results_dir,
        nbins_q2=args.nbins_q2,
        nbins_y=args.nbins_y,
        cmap=args.cmap,
    )