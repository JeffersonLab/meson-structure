import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import re
import os
import zipfile
import sys

# Read command-line arguments
# Usage: python script.py [filtering] [setting] [segments]
# Example: python script.py True 5x41 all
filtering = sys.argv[1].lower() == "true"  # convert string to boolean
setting = sys.argv[2]                      # e.g., "5x41"
segments = sys.argv[3]                     # e.g., "all" or "001,002"

# Parse segments into list if not "all"
if segments.lower() != "all":
    segments = segments.split(",")

# Set data directory
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

# Define base variable names and reconstruction methods
variables = ["x", "q2", "y", "nu", "w"]
methods = {
    "da": "Double angle",
    "esigma": "Electron",
    "jb": "Jacquet-Blondel",
    "ml": "Machine Learning",
    "sigma": "Sigma",
    "mc": "Monte Carlo"
}

# Create a PDF to save all plots
# pdf_filename = f'kaon_analysis_{setting}.pdf'
# pdf = PdfPages(pdf_filename)


if filtering:
    output_img_dir = f"plots/kaon_analysis_images_filtered_{setting}"
    os.makedirs(output_img_dir, exist_ok=True)

else:
    df = unfiltered_df
    output_img_dir = f"plots/kaon_analysis_images_unfiltered_{setting}"
    os.makedirs(output_img_dir, exist_ok=True)

img_page_counter = 0

metrics_summary = {}

for var in variables:
    ref_col = f"mc_{var}"

    fig_corr, axs_corr = plt.subplots(2, 3, figsize=(18, 10))
    fig_corr.suptitle(f"Correlation with Reference for {var.upper()}", fontsize=16)

    fig_corr_2d, axs_corr_2d = plt.subplots(2, 3, figsize=(18, 10))
    fig_corr_2d.suptitle(f"Correlation with Reference for {var.upper()}", fontsize=16)
    
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

        # Store stats
        mean_resid = residual.mean()
        std_resid = residual.std()
        rmse = np.sqrt((residual ** 2).mean())
        stats_data.append((label, mean_resid, std_resid, rmse))

        # # Residual histogram
        ax_resid = axs_resid[i // 3, i % 3]
        sns.histplot(residual, bins=50, kde=True, ax=ax_resid)
        ax_resid.set_title(f"{label} Residuals")
        ax_resid.set_xlabel("Residual")
        ax_resid.set_ylabel("Count")

        # # Correlation plot (2D histogram)
        ax_corr = axs_corr[i // 3, i % 3]
        sns.histplot(
            x=df[ref_col], y=df[col],
            bins=100, cmap="viridis", cbar=True, ax=ax_corr
        )
        ax_corr.plot([df[ref_col].min(), df[ref_col].max()], 
                [df[ref_col].min(), df[ref_col].max()], 'r--', color='red', linewidth = 0.5)
        ax_corr.set_title(f"{label} (2D Histogram)")
        ax_corr.set_xlabel(f"True {var}")
        ax_corr.set_ylabel(f"Reconstructed {var}")

        # Correlation plot (2D histogram with focused Y range)
        ax_corr_2d = axs_corr_2d[i // 3, i % 3]

        # Compute dynamic Y-limits around the reference values
        # ref_mean = df[ref_col].mean()
        # ref_std = df[ref_col].std()
        # y_min = ref_mean - 3 * ref_std
        # y_max = ref_mean + 3 * ref_std
        y_min = df[ref_col].min() - 0.1*df[ref_col].max()
        y_max = df[ref_col].max() + 0.1*df[ref_col].max()

        # Optionally filter values for plotting (clipping avoids stray outliers in y)
        x_vals = df[ref_col]
        # y_vals = df[col].clip(lower=y_min, upper=y_max)
        y_vals = df[col]

        sns.histplot(
            x=x_vals, y=y_vals,
            bins=100, cmap="viridis", cbar=True, ax=ax_corr_2d
        )

        ax_corr_2d.plot([x_vals.min(), x_vals.max()],
                [x_vals.min(), x_vals.max()], 'r--', color='red', linewidth = 0.5)
        ax_corr_2d.set_title(f"{label} (2D Histogram, Focused)")
        ax_corr_2d.set_xlabel(f"True {var}")
        ax_corr_2d.set_ylabel(f"Reconstructed {var}")
        ax_corr_2d.set_ylim(y_min, y_max)



    # Save plots to PDF
    # pdf.savefig(fig_corr)
    # pdf.savefig(fig_resid)
    # plt.close(fig_corr)
    # plt.close(fig_resid)
    img_corr_path = os.path.join(output_img_dir, f"{img_page_counter:03d}_corr_{var}.png")
    img_corr_2d_path = os.path.join(output_img_dir, f"{img_page_counter:03d}_corr_2d_{var}.png")
    fig_corr.savefig(img_corr_path, dpi=150, bbox_inches='tight')
    fig_corr_2d.savefig(img_corr_2d_path, dpi=150, bbox_inches='tight')
    plt.close(fig_corr)
    plt.close(fig_corr_2d)
    img_page_counter += 1

    # Residuals
    img_resid_path = os.path.join(output_img_dir, f"{img_page_counter:03d}_resid_{var}.png")
    fig_resid.savefig(img_resid_path, dpi=150, bbox_inches='tight')
    plt.close(fig_resid)
    img_page_counter += 1




    # Save metrics
    stats_df = pd.DataFrame(stats_data, columns=["Method", "Mean", "StdDev", "RMSE"])
    stats_df_sorted = stats_df.sort_values("RMSE")

    # Save summary for later
    metrics_summary[var] = stats_df_sorted

    # Plot rankings
    fig_rank, ax_rank = plt.subplots(figsize=(10, 6))
    sns.barplot(x="RMSE", y="Method", data=stats_df_sorted, palette="viridis", ax=ax_rank)
    ax_rank.set_title(f"Method RMSE Ranking for {var.upper()}")
    # pdf.savefig(fig_rank)
    # plt.close(fig_rank)
    img_rank_path = os.path.join(output_img_dir, f"{img_page_counter:03d}_rank_{var}.png")
    fig_rank.savefig(img_rank_path, dpi=150, bbox_inches='tight')
    plt.close(fig_rank)
    img_page_counter += 1

# Create summary page
fig_summary, axs_summary = plt.subplots(2, 3, figsize=(18, 10))
fig_summary.suptitle("Best Methods per Variable Based on RMSE", fontsize=18)

for i, var in enumerate(variables):
    ax = axs_summary[i // 3, i % 3]
    top_method = metrics_summary[var].iloc[1]
    text = f"{var.upper()}:\n{top_method['Method']}\nRMSE = {top_method['RMSE']:.4f}"
    ax.text(0.5, 0.5, text, ha='center', va='center', fontsize=14)
    ax.axis("off")

# pdf.savefig(fig_summary)
# plt.close(fig_summary)

img_summary_path = os.path.join(output_img_dir, f"{img_page_counter:03d}_summary.png")
fig_summary.savefig(img_summary_path, dpi=150, bbox_inches='tight')
plt.close(fig_summary)

# pdf.close()
print(f"All analysis saved to '{output_img_dir}'")


