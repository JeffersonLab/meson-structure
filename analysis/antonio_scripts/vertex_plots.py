#!/usr/bin/env python3
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def stats(path_acceptance: Path, outdir: Path):
    """Compute summary stats and write stats CSV to outdir."""
    # columns needed for counting
    pimin_B0_tracker_hits = "pimin_B0TrackerHits"
    prot_RP_hits = "prot_ForwardRomanPotHits"
    cols_for_counts = [pimin_B0_tracker_hits, prot_RP_hits]

    df_small = pd.read_parquet(path_acceptance, columns=cols_for_counts)
    total = len(df_small)

    count_B0_tracker = int((df_small[pimin_B0_tracker_hits] == 1).sum())
    count_RP = int((df_small[prot_RP_hits] == 1).sum())

    fraction_B0_tracker = count_B0_tracker / max(1, total)
    fraction_RP = count_RP / max(1, total)

    mask = (df_small[pimin_B0_tracker_hits] == 1) & (df_small[prot_RP_hits] == 1)
    count_corr = int(mask.sum())
    fraction_corr = count_corr / max(1, total)

    data = [
        {"Detector": "B0TrackerHits",       "Pimin Hits": count_B0_tracker,  "Fraction of Events": fraction_B0_tracker},
        {"Detector": "ForwardRomanPotHits", "Prot Hits": count_RP,           "Fraction of Events": fraction_RP},
        {"Detector": "Correlation",         "Both Hits": count_corr,        "Fraction of Events": fraction_corr},
    ]
    df_stats = pd.DataFrame(data)

    # write to csv in outdir
    outdir.mkdir(parents=True, exist_ok=True)
    stats_path = outdir / "acceptance_stats.csv"
    df_stats.to_csv(stats_path, index=False)
    return df_stats, stats_path

def plot_vtx(path_acceptance: Path, outdir: Path):
    """Create and save 4 hist2d plots for correlated events (pi- in B0 AND proton in RP)."""
    # columns we need (only these will be read)
    cols = [
        "pimin_px", "pimin_py", "pimin_pz", "pimin_vz",
        "prot_px",  "prot_py",  "prot_pz",  "prot_vz",
        "pimin_B0TrackerHits", "prot_ForwardRomanPotHits"
    ]

    df = pd.read_parquet(path_acceptance, columns=cols)

        
    # 3/18/26: Comment out correlation data frame --> will plot vertex information across all events 
    # mask for correlated events  
    detectors = [c for c in df.columns if c.startswith("pimin_")]

    mask = (df[detectors] == 1).any(axis=1)

    df_corr = df[mask]

    # prepare safe extraction (handle empty df_corr)
    if df_corr.empty:
        print(f"  No correlated events found in {path_acceptance.name}; skipping plots.")
        return [], []
    
    # proton kinematics
    prot_px = df_corr["prot_px"].to_numpy()
    prot_py = df_corr["prot_py"].to_numpy()
    prot_pz = df_corr["prot_pz"].to_numpy()
    prot_zvtx = df_corr["prot_vz"].to_numpy()/1000 # convert to m

    prot_p = np.sqrt(prot_px**2 + prot_py**2 + prot_pz**2)
    with np.errstate(invalid="ignore", divide="ignore"):
        prot_theta = np.arccos(np.clip(prot_pz / prot_p, -1.0, 1.0)) * 1000 # convert to mrad

    # pimin kinematics
    pimin_px = df_corr["pimin_px"].to_numpy()
    pimin_py = df_corr["pimin_py"].to_numpy()
    pimin_pz = df_corr["pimin_pz"].to_numpy()
    pimin_zvtx = df_corr["pimin_vz"].to_numpy()/1000 # convert to m

    pimin_p = np.sqrt(pimin_px**2 + pimin_py**2 + pimin_pz**2)
    with np.errstate(invalid="ignore", divide="ignore"):
        pimin_theta = np.arccos(np.clip(pimin_pz / pimin_p, -1.0, 1.0)) * 1000 # convert to mrad

    # Ensure output dir exists
    outdir.mkdir(parents=True, exist_ok=True)

    saved_paths = []

    # helper to make and save hist2d, closing figure each time
    def _save_hist2d(x, y, bins, range, xlabel, ylabel, title, fname):
        fig, ax = plt.subplots(figsize=(6,5))
        h = ax.hist2d(x, y, bins=bins, range = range, cmin=1)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        fig.colorbar(h[3], ax=ax, label="Counts")
        path = outdir / fname
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return path

    # Proton p vs z
    saved_paths.append(_save_hist2d(prot_zvtx, prot_p, bins=(100,100), range = ((0,40), (0,300)),
                                   xlabel=r"$z_{vtx}$ (m)", ylabel=r"p (GeV/c)",
                                   title=r"p vs $z_{vtx}$ (proton)",
                                   fname="prot_p_vs_z.png"))

    # Proton theta vs z
    saved_paths.append(_save_hist2d(prot_zvtx, prot_theta, bins=(100,100), range = ((0,40), (0,100)),
                                   xlabel=r"$z_{vtx}$ (m)", ylabel=r"$\theta$ (mrad)",
                                   title=r"$\theta$ vs $z_{vtx}$ (proton)",
                                   fname="prot_theta_vs_z.png"))

    # Pimin p vs z
    saved_paths.append(_save_hist2d(pimin_zvtx, pimin_p, bins=(100,100), range = ((0,40), (0,100)),
                                   xlabel=r"$z_{vtx}$ (m)", ylabel=r"p (GeV/c)",
                                   title=r"p vs $z_{vtx}$ ($\pi^-$)",
                                   fname="pimin_p_vs_z.png"))

    # Pimin theta vs z
    saved_paths.append(_save_hist2d(pimin_zvtx, pimin_theta, bins=(100,100), range = ((0,40),(0,100)),
                                   xlabel=r"$z_{vtx}$ (m)", ylabel=r"$\theta$ (mrad)",
                                   title=r"$\theta$ vs $z_{vtx}$ ($\pi^-$)",
                                   fname="pimin_theta_vs_z.png"))

    return saved_paths

def main():
    base_dir = Path("/home/ajperillo19/SULI_JLAB_2026")
    beams = ["5x41", "10x100", "10x130", "18x275"]
    out_base = base_dir / "results"

    for beam in beams:
        path_acceptance = base_dir / f"{beam}_acceptance.duckdb.parquet"
        if not path_acceptance.exists():
            print(f"Warning: {path_acceptance} not found, skipping")
            continue

        print(f"Processing beam: {beam}")
        outdir = out_base / beam
        df_stats, stats_path = stats(path_acceptance=path_acceptance, outdir=outdir)
        print(f"  Wrote stats CSV to {stats_path}")

        plot_paths = plot_vtx(path_acceptance=path_acceptance, outdir=outdir)
        for p in plot_paths:
            print(f"  Saved plot: {p}")

if __name__ == "__main__":
    main()