import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re
import os
import zipfile
import sys

# Read command-line arguments
# Usage: python script.py [filtering] [setting] [segments]
# Example: python script.py True 5x41 all
filtering = sys.argv[1].lower() == "true"
setting = sys.argv[2]
segments = sys.argv[3]

if segments.lower() != "all":
    segments = segments.split(",")

# Path to your kaon data
base_dir = "/home/ubuntu/meson-structure/data/csv_files_kaon/kaon_all/meson-strcutrue-2025-06-05-csv"

def extract_and_combine_csvs(base_dir, setting, segments="all"):
    pattern = re.compile(rf"k_lambda_{setting}_5000evt_(\d{{3}})\.reco_dis\.csv\.zip")
    combined_df = pd.DataFrame()
    files = sorted(os.listdir(base_dir))
    for file in files:
        match = pattern.match(file)
        if match:
            segment = match.group(1)
            if segments != "all" and segment not in segments:
                continue
            zip_path = os.path.join(base_dir, file)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                csv_name = zip_ref.namelist()[0]
                with zip_ref.open(csv_name) as f:
                    try:
                        df = pd.read_csv(f)
                        if df.empty or df.columns.size == 0:
                            print(f"[WARN] Skipping empty file inside {file}")
                            continue
                        combined_df = pd.concat([combined_df, df], ignore_index=True)
                    except pd.errors.EmptyDataError:
                        print(f"[ERROR] Empty CSV inside {file}, skipping...")
                        continue
    return combined_df

unfiltered_df = extract_and_combine_csvs(base_dir, setting, segments=segments)

# Variables and methods
variables = ["x", "q2", "y", "nu", "w"]
methods = {
    "da": "Double angle",
    "esigma": "Electron",
    "jb": "Jacquet-Blondel",
    "ml": "Machine Learning",
    "sigma": "Sigma",
    "mc": "Monte Carlo"
}

output_img_dir = f"plots/kaon_analysis_images_{'filtered' if filtering else 'unfiltered'}_{setting}"
os.makedirs(output_img_dir, exist_ok=True)

img_page_counter = 0
metrics_summary = {}

for var in variables:
    ref_col = f"mc_{var}"

    # fig_corr, axs_corr = plt.subplots(2, 3, figsize=(18, 10))
    # fig_corr.suptitle(f"Correlation (2D Histogram) for {var.upper()}", fontsize=16)

    fig_corr_2d, axs_corr_2d = plt.subplots(2, 3, figsize=(18, 10))
    fig_corr_2d.suptitle(f"Correlation (2D Histogram) for {var.upper()}", fontsize=16)

    fig_resid, axs_resid = plt.subplots(2, 3, figsize=(18, 10))
    fig_resid.suptitle(f"Residuals: Method - Reference for {var.upper()}", fontsize=16)

    stats_data = []

    for i, (prefix, label) in enumerate(methods.items()):
        col = f"{prefix}_{var}"

        if filtering:
            threshold = 1000
            df = unfiltered_df[(unfiltered_df[col] - unfiltered_df[ref_col]).abs() < threshold]
        else:
            df = unfiltered_df

        residual = df[col] - df[ref_col]

        # --- Compute stats ---
        mean_resid = residual.mean()
        std_resid = residual.std()
        rmse = np.sqrt((residual ** 2).mean())
        stats_data.append((label, mean_resid, std_resid, rmse))

        # --- Residuals Histogram ---
        ax_resid = axs_resid[i // 3, i % 3]
        sns.histplot(residual, bins=50, kde=True, ax=ax_resid)
        ax_resid.set_title(f"{label} Residuals")
        ax_resid.set_xlabel("Residual")
        ax_resid.set_ylabel("Count")

        # --- Full 2D Correlation Histogram ---
        # ax_corr = axs_corr[i // 3, i % 3]
        x_vals = df[ref_col]
        y_vals = df[col]

        x_min, x_max = x_vals.min(), x_vals.max()
        # y_min, y_max = y_vals.quantile(0.001), y_vals.quantile(0.999)
        # # y_min, y_max = x_min, x_max

        # sns.histplot(
        #     x=x_vals, y=y_vals,
        #     bins=100,
        #     binrange=[(x_min, x_max), (y_min, y_max)],
        #     cmap="viridis", cbar=True, ax=ax_corr
        # )
        # ax_corr.plot([x_min, x_max], [x_min, x_max], 'r--', linewidth=0.5)
        # ax_corr.set_title(f"{label}")
        # ax_corr.set_xlabel(f"True {var}")
        # ax_corr.set_ylabel(f"Reco {var}")
        # ax_corr.set_ylim(y_min, y_max)

        # --- Focused 2D Correlation ---
        ax_corr_2d = axs_corr_2d[i // 3, i % 3]
        y_focus_min = x_vals.min() - 0.1 * abs(x_vals.min())
        y_focus_max = x_vals.max() + 0.1 * abs(x_vals.max())

        sns.histplot(
            x=x_vals, y=y_vals,
            bins=100,
            binrange=[(x_min, x_max), (y_focus_min, y_focus_max)],
            cmap="viridis", cbar=True, ax=ax_corr_2d
        )
        ax_corr_2d.plot([x_min, x_max], [x_min, x_max], 'r--', linewidth=0.5)
        ax_corr_2d.set_title(f"{label}")
        ax_corr_2d.set_xlabel(f"True {var}")
        ax_corr_2d.set_ylabel(f"Reco {var}")
        ax_corr_2d.set_ylim(y_focus_min, y_focus_max)

    # Save image files
    # fig_corr.savefig(os.path.join(output_img_dir, f"{img_page_counter:03d}_corr_{var}.png"), dpi=150, bbox_inches='tight')
    # plt.close(fig_corr)
    # img_page_counter += 1

    fig_corr_2d.savefig(os.path.join(output_img_dir, f"{img_page_counter:03d}_corr2d_{var}.png"), dpi=150, bbox_inches='tight')
    plt.close(fig_corr_2d)
    img_page_counter += 1

    fig_resid.savefig(os.path.join(output_img_dir, f"{img_page_counter:03d}_resid_{var}.png"), dpi=150, bbox_inches='tight')
    plt.close(fig_resid)
    img_page_counter += 1

    # --- RMSE Ranking Bar Plot ---
    stats_df = pd.DataFrame(stats_data, columns=["Method", "Mean", "StdDev", "RMSE"])
    stats_df_sorted = stats_df.sort_values("RMSE")
    metrics_summary[var] = stats_df_sorted

    fig_rank, ax_rank = plt.subplots(figsize=(10, 6))
    sns.barplot(x="RMSE", y="Method", data=stats_df_sorted, palette="viridis", ax=ax_rank)
    ax_rank.set_title(f"Method RMSE Ranking for {var.upper()}")
    fig_rank.savefig(os.path.join(output_img_dir, f"{img_page_counter:03d}_rank_{var}.png"), dpi=150, bbox_inches='tight')
    plt.close(fig_rank)
    img_page_counter += 1

# --- Q² vs x ---
fig_x_q2, axs_x_q2 = plt.subplots(2, 3, figsize=(18, 10))
fig_x_q2.suptitle("Q² vs x for Each Method", fontsize=16)

for i, (prefix, label) in enumerate(methods.items()):
    col_x = f"{prefix}_x"
    col_q2 = f"{prefix}_q2"

    xbj_vals = df[col_x]
    q2_vals = df[col_q2]

    # Define bin ranges
    xbj_min, xbj_max = 0, 0.2
    q2_min = 0
    q2_max = 100

    # Access correct subplot
    ax_x_q2 = axs_x_q2[i // 3, i % 3]
    
    # Plot 2D histogram
    sns.histplot(
        x=xbj_vals, y=q2_vals,
        bins=50,
        binrange=[(xbj_min, xbj_max), (q2_min, q2_max)],
        cmap="viridis", cbar=True, ax=ax_x_q2
    )

    ax_x_q2.set_title(f"{label}")
    ax_x_q2.set_xlabel("x (Bjorken)")
    ax_x_q2.set_ylabel("Q² (GeV²)")

# Save and close
fig_x_q2.tight_layout(rect=[0, 0.03, 1, 0.95])
fig_x_q2.savefig(os.path.join(output_img_dir, f"{img_page_counter:03d}_x_Q2.png"), dpi=150, bbox_inches='tight')
plt.close(fig_x_q2)
img_page_counter += 1

# --- Summary Image ---
fig_summary, axs_summary = plt.subplots(2, 3, figsize=(18, 10))
fig_summary.suptitle("Best Methods per Variable Based on RMSE", fontsize=18)

for i, var in enumerate(variables):
    ax = axs_summary[i // 3, i % 3]
    top_method = metrics_summary[var].iloc[1]  # 0 may be MC itself
    text = f"{var.upper()}:\n{top_method['Method']}\nRMSE = {top_method['RMSE']:.4f}"
    ax.text(0.5, 0.5, text, ha='center', va='center', fontsize=14)
    ax.axis("off")

fig_summary.savefig(os.path.join(output_img_dir, f"{img_page_counter:03d}_summary.png"), dpi=150, bbox_inches='tight')
plt.close(fig_summary)

print(f"\n✅ All plots saved to: {output_img_dir}")
