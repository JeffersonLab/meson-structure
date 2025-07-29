
#!/usr/bin/env python3
"""
A comprehensive script to analyze EIC data.
- Generates a full suite of Matplotlib comparison plots.
- Creates data-driven, variable-binned ROOT histograms with a configurable focus
  on the low-end of the x and Q2 spectrum.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import glob
import os
import re
import itertools
import ROOT
 
# --- Paths ---
# Directory where  input CSV files are located
data_base_dir = "/scratch/gregory/allcsv3"
# Base directory where all output plots and files will be saved
base_output_dir = "/home/gregory/sum25/eic/analysis/all_method_plots6"

# --- Analysis Definitions ---
# List of beam energies to process
beam_energies = ['5x41', '10x100', '18x275']
truth_var_mapping = {'x': 'xbj', 'q2': 'q2', 'y': 'y_d', 'w': 'w'}
kinematic_vars = list(truth_var_mapping.keys())
# Pretty labels for plots
var_labels = {'x': r'$x_{bj}$', 'q2': r'$Q^2$', 'y': 'y', 'w': 'W'}

os.makedirs(base_output_dir, exist_ok=True)
print(f"Base output directory set to: {base_output_dir}")

def concat_csvs_unique_event(pattern, key_column='evt'):
    """
    Reads all CSV files matching a glob pattern, concatenates them, and ensures
    event IDs are unique across all files.
    """
    dfs = []
    offset = 0
    files_found = sorted(glob.glob(pattern))
    if not files_found:
        print(f"No files found matching pattern: {pattern}")
        return pd.DataFrame()
    for file in files_found:
        try:
            df = pd.read_csv(file)
            df.columns = [col.strip().strip(',') for col in df.columns]
            if df.empty:
                continue
            if key_column not in df.columns:
                if 'event' in df.columns and key_column == 'evt':
                     df = df.rename(columns={'event': 'evt'})
                else:
                    continue
            df[key_column] = pd.to_numeric(df[key_column], errors="coerce")
            df[key_column] += offset
            max_evt = df[key_column].max()
            if pd.notna(max_evt):
                offset = int(max_evt) + 1
            dfs.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def save_2dhist(x, y, xlabel, ylabel, title, filename, target_dir, bins=100, use_percentiles=True, vmin=1, custom_range=None, text_to_display=None, x_scale='linear', y_scale='linear'):
    """
    Saves a 2D histogram to a file. Supports linear or log axes
    """
    mask = np.isfinite(x) & np.isfinite(y)
    if x_scale == 'log': mask &= (x > 0)
    if y_scale == 'log': mask &= (y > 0)
    if not np.any(mask):
        print(f"Skipping 2D histogram {filename} in {target_dir}: no valid data for specified scale.")
        return
    
    x_filtered, y_filtered = x[mask], y[mask]

    if custom_range:
        data_range = custom_range
    else:
        # Define a local helper for ranges to avoid NameError
        def compute_local_range(arr):
            if not np.any(arr): return (0, 1)
            lo, hi = (np.percentile(arr, [1, 99])) if use_percentiles else (np.nanmin(arr), np.nanmax(arr))
            return (lo, hi) if lo != hi else (lo, lo + 1e-6)
        range_x = compute_local_range(x_filtered)
        range_y = compute_local_range(y_filtered)
        data_range = [range_x, range_y]
    
    plt.figure()
    plt.xscale(x_scale)
    plt.yscale(y_scale)
    plt.hist2d(x_filtered, y_filtered, bins=bins, cmap='viridis', range=data_range, norm=LogNorm(vmin=vmin))
    plt.xlabel(xlabel); plt.ylabel(ylabel)
    plt.colorbar(label="Counts")
    plt.title(title, fontsize=10)
    if text_to_display:
        plt.text(0.05, 0.95, text_to_display, transform=plt.gca().transAxes, fontsize=8,
                 verticalalignment='top', bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.5))
    plt.tight_layout()
    full_path = os.path.join(target_dir, filename)
    plt.savefig(full_path)
    plt.close()

def save_1dhist(data, xlabel, ylabel, title, filename, target_dir, bins=200, plot_range=None, color='steelblue', text_to_display=None):
    """
    Saves a 1D histogram to a file.
    """
    mask = np.isfinite(data)
    if not np.any(mask):
        print(f"Skipping 1D histogram {filename} in {target_dir}: no finite data.")
        return
    plt.figure()
    plt.hist(data[mask], bins=bins, range=plot_range, histtype='stepfilled', color=color)
    plt.xlabel(xlabel); plt.ylabel(ylabel)
    plt.title(title, fontsize=10)
    if text_to_display:
        plt.text(0.05, 0.95, text_to_display, transform=plt.gca().transAxes, fontsize=8,
                 verticalalignment='top', bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.5))
    plt.grid(True)
    plt.tight_layout()
    full_path = os.path.join(target_dir, filename)
    plt.savefig(full_path)
    plt.close()

def create_focused_quantiles(num_bins, focus_strength=1.5):
    """
.
    """
    linear_space = np.linspace(0.0, 1.0, num_bins + 1)
    focused_space = linear_space ** focus_strength
    return focused_space


for beam_energy in beam_energies:
    print(f"\n{'='*80}")
    print(f"--- Processing Beam Energy: {beam_energy} ---")
    print(f"{'='*80}")
    current_beam_energy_output_dir = os.path.join(base_output_dir, beam_energy)
    os.makedirs(current_beam_energy_output_dir, exist_ok=True)

    #  Data Loading and Processing
    print("\n--- Loading and processing CSV Data ---")
    mc_dis_df = concat_csvs_unique_event(os.path.join(data_base_dir, f"*{beam_energy}*mc_dis.csv"), key_column='evt')
    reco_df   = concat_csvs_unique_event(os.path.join(data_base_dir, f"*{beam_energy}*reco_dis.csv"), key_column='evt')
    if mc_dis_df.empty or reco_df.empty:
        print(f"Skipping {beam_energy}: A required dataframe is empty.")
        continue
    merged_df = pd.merge(mc_dis_df, reco_df, on='evt', how='inner')
    if merged_df.empty:
        print(f"Skipping {beam_energy}: Merged DataFrame is empty.")
        continue
    
    reco_methods = sorted(list(set([col.split('_')[0] for col in reco_df.columns if '_' in col and col != 'evt' and not col.startswith('mc_')])))
    squared_w_methods = set() # Placeholder for w-squaring logic
    
    # Global Kinematic Cuts
    print("\n--- Applying Global Kinematic Cuts ---")
    initial_rows = len(merged_df)
    total_mask = pd.Series(True, index=merged_df.index)
    for method in reco_methods:
        for var_key in ['x', 'y']:
            reco_col = f"{method}_{var_key}"
            if reco_col in merged_df.columns:
                total_mask &= (merged_df[reco_col] >= 0) & (merged_df[reco_col] <= 1)
    merged_df = merged_df[total_mask].copy()
    print(f"  Kept {len(merged_df)} of {initial_rows} events after cuts.")
    if merged_df.empty:
        print("DataFrame is empty after applying cuts. Skipping all plots for this beam energy.")
        continue

    # --- Matplotlib Plotting Section ---
    truth_plots_dir = os.path.join(current_beam_energy_output_dir, "truth")
    os.makedirs(truth_plots_dir, exist_ok=True)
    
    print("\n--- 1. Generating Standard Truth vs Reconstructed Kinematic Plots ---")
    for var_key in kinematic_vars:
        truth_col = truth_var_mapping[var_key]
        if truth_col not in merged_df.columns: continue
        for method in reco_methods:
            reco_col = f"{method}_{var_key}"
            if reco_col in merged_df.columns:
                current_method_output_dir = os.path.join(current_beam_energy_output_dir, method)
                os.makedirs(current_method_output_dir, exist_ok=True)
                truth_label, reco_val_label = f"Truth {var_labels[var_key]}", f"$W^2$" if var_key == 'w' and method in squared_w_methods else var_labels[var_key]
                reco_label, plot_title = f"Reco {reco_val_label} ({method})", f"{beam_energy}: Reco {reco_val_label} vs Truth {var_labels[var_key]} ({method})"
                plot_mask = merged_df[truth_col].notna() & merged_df[reco_col].notna()
                text = f"Entries: {plot_mask.sum():,}"
                save_2dhist(merged_df[truth_col], merged_df[reco_col], truth_label, reco_label, plot_title, f"truth_vs_reco_{var_key}_{method}.png", target_dir=current_method_output_dir, text_to_display=text)
                if var_key == 'x':
                    logx_title = plot_title + " (Log x-axis)"
                    save_2dhist(merged_df[truth_col], merged_df[reco_col], truth_label, reco_label, logx_title, f"truth_vs_reco_logx_{var_key}_{method}.png", target_dir=current_method_output_dir, text_to_display=text, x_scale='log')

    print("\n--- 2. Generating Intra-Kinematic Variable Correlation Plots ---")
    agreement_threshold = 0.20
    for var1_key, var2_key in itertools.combinations(kinematic_vars, 2):
        truth_col1, truth_col2 = truth_var_mapping[var1_key], truth_var_mapping[var2_key]
        label1, label2 = var_labels[var1_key], var_labels[var2_key]
        if truth_col1 in merged_df.columns and truth_col2 in merged_df.columns:
            title = f"{beam_energy}: Truth {label1} vs {label2}"
            plot_mask = merged_df[truth_col1].notna() & merged_df[truth_col2].notna()
            text = f"Entries: {plot_mask.sum():,}"
            save_2dhist(merged_df[truth_col1], merged_df[truth_col2], f"Truth {label1}", f"Truth {label2}", title, f"truth_{var1_key}_vs_{var2_key}.png", target_dir=truth_plots_dir, text_to_display=text)
            if var1_key == 'x':
                logx_title = title + " (Log x-axis)"
                save_2dhist(merged_df[truth_col1], merged_df[truth_col2], f"Truth {label1}", f"Truth {label2}", logx_title, f"truth_logx_{var1_key}_vs_{var2_key}.png", target_dir=truth_plots_dir, text_to_display=text, x_scale='log')
        for method in reco_methods:
            reco_col1, reco_col2 = f"{method}_{var1_key}", f"{method}_{var2_key}"
            if reco_col1 in merged_df.columns and reco_col2 in merged_df.columns:
                current_method_output_dir = os.path.join(current_beam_energy_output_dir, method)
                os.makedirs(current_method_output_dir, exist_ok=True)
                reco_label1_val, reco_label2_val = (f"$W^2$" if k == 'w' and method in squared_w_methods else var_labels[k] for k in [var1_key, var2_key])
                reco_label1, reco_label2 = f"Reco {reco_label1_val} ({method})", f"Reco {reco_label2_val} ({method})"
                title = f"{beam_energy}: Reco {reco_label1_val} vs {reco_label2_val} ({method})"
                plot_mask = merged_df[reco_col1].notna() & merged_df[reco_col2].notna()
                total_events = plot_mask.sum()
                text_to_display = f"Entries: {total_events:,}"
                if {var1_key, var2_key} == {'x', 'q2'}:
                    df_agree = merged_df[plot_mask]
                    if not df_agree.empty:
                        res_x, res_q2 = ((df_agree[f"{method}_{k}"] - df_agree[truth_var_mapping[k]]) / df_agree[truth_var_mapping[k]] for k in ['x', 'q2'])
                        agree_x_count, agree_q2_count = (abs(res_x) < agreement_threshold).sum(), (abs(res_q2) < agreement_threshold).sum()
                        percent_x = (agree_x_count / total_events) * 100 if total_events > 0 else 0
                        percent_q2 = (agree_q2_count / total_events) * 100 if total_events > 0 else 0
                        text_to_display += f"\nx agree (±{agreement_threshold:.0%}): {percent_x:.1f}%\nQ² agree (±{agreement_threshold:.0%}): {percent_q2:.1f}%"
                save_2dhist(merged_df[reco_col1], merged_df[reco_col2], reco_label1, reco_label2, title, f"reco_{var1_key}_vs_{var2_key}_{method}.png", target_dir=current_method_output_dir, text_to_display=text_to_display)
                if var1_key == 'x':
                    logx_title = title + " (Log x-axis)"
                    save_2dhist(merged_df[reco_col1], merged_df[reco_col2], reco_label1, reco_label2, logx_title, f"reco_logx_{var1_key}_vs_{var2_key}_{method}.png", target_dir=current_method_output_dir, text_to_display=text_to_display, x_scale='log')

    print("\n--- 3. Generating Standard Resolution Histograms (1D & 2D) ---")
    for var_key in kinematic_vars:
        truth_col = truth_var_mapping[var_key]
        if truth_col not in merged_df.columns: continue
        for method in reco_methods:
            reco_col = f"{method}_{var_key}"
            if reco_col in merged_df.columns:
                current_method_output_dir = os.path.join(current_beam_energy_output_dir, method)
                os.makedirs(current_method_output_dir, exist_ok=True)
                valid_mask = np.isfinite(merged_df[truth_col]) & np.isfinite(merged_df[reco_col]) & (merged_df[truth_col] != 0)
                temp_truth, temp_reco = merged_df.loc[valid_mask, truth_col], merged_df.loc[valid_mask, reco_col]
                if temp_truth.empty: continue
                resolution = (temp_reco - temp_truth) / temp_truth
                truth_label_txt = f"Truth {var_labels[var_key]}"
                reco_val_label = f"Reco $W^2$" if var_key == 'w' and method in squared_w_methods else f"Reco {var_labels[var_key]}"
                res_label = f"({reco_val_label} - {truth_label_txt}) / {truth_label_txt}"
                title_1d, title_2d = f"{beam_energy}: {res_label} ({method})", f"{beam_energy}: Resolution vs Truth ({method})"
                text_1d, text_2d = f"Entries: {resolution.notna().sum():,}", f"Entries: {(temp_truth.notna() & resolution.notna()).sum():,}"
                save_1dhist(resolution, res_label, "Counts", title_1d, f"{var_key}_resolution_hist_{method}.png", target_dir=current_method_output_dir, plot_range=(-1, 1), text_to_display=text_1d)
                save_2dhist(temp_truth, resolution, truth_label_txt, res_label, title_2d, f"{var_key}_res_vs_truth_{method}.png", target_dir=current_method_output_dir, text_to_display=text_2d)
                if var_key == 'x':
                    logx_title_2d = title_2d + " (Log x-axis)"
                    save_2dhist(temp_truth, resolution, truth_label_txt, res_label, logx_title_2d, f"{var_key}_res_vs_truth_logx_{method}.png", target_dir=current_method_output_dir, text_to_display=text_2d, x_scale='log')


    print("\n--- 4. Generating Resolution Plots with y-cuts ---")
    y_cut_dir = os.path.join(current_beam_energy_output_dir, "y_cut_resolution_plots")
    os.makedirs(y_cut_dir, exist_ok=True)
    for method in reco_methods:
        reco_y_col = f"{method}_y"
        if reco_y_col not in merged_df.columns: continue
        
        print(f"  Processing y-cut plots for method: {method}")
        method_cut_mask = pd.Series(True, index=merged_df.index)
        for cut_var in ['x', 'y']:
            cut_col = f"{method}_{cut_var}"
            if cut_col in merged_df.columns:
                method_cut_mask &= (merged_df[cut_col] >= 0) & (merged_df[cut_col] <= 1)
        
        y_regions = {'low_y': {'mask': merged_df[reco_y_col] <= 0.1, 'label': 'y <= 0.1'},
                     'high_y': {'mask': merged_df[reco_y_col] > 0.1, 'label': 'y > 0.1'}}
        
        for region_name, region_info in y_regions.items():
            final_mask = method_cut_mask & region_info['mask']
            df_plot = merged_df[final_mask]
            if df_plot.empty: continue
            
            for var_key in ['x', 'q2']:
                truth_col, reco_col = truth_var_mapping[var_key], f"{method}_{var_key}"
                if truth_col in df_plot.columns and reco_col in df_plot.columns:
                    current_method_output_dir = os.path.join(y_cut_dir, method)
                    os.makedirs(current_method_output_dir, exist_ok=True)
                    
                    valid_mask = np.isfinite(df_plot[truth_col]) & np.isfinite(df_plot[reco_col]) & (df_plot[truth_col] != 0)
                    temp_truth, temp_reco = df_plot.loc[valid_mask, truth_col], df_plot.loc[valid_mask, reco_col]
                    if temp_truth.empty: continue
                    
                    resolution = (temp_reco - temp_truth) / temp_truth
                    
                    # --- FIX APPLIED HERE ---
                    # 1. Define var_label first.
                    var_label = var_labels[var_key]
                    # 2. Then use it to define the other labels.
                    truth_label_txt = f"Truth {var_label}"
                    res_label = f"({var_label} Reco - Truth) / Truth"
                    
                    title = f"{beam_energy}: {var_label} Resolution vs Truth\n(Cut: {region_info['label']}, Method: {method})"
                    filename = f"res_vs_truth_{var_key}_{region_name}_{method}.png"
                    text = f"Entries: {(temp_truth.notna() & resolution.notna()).sum():,}"
                    
                    save_2dhist(temp_truth, resolution, truth_label_txt, res_label, title, filename,
                                target_dir=current_method_output_dir, text_to_display=text)
                    
                    if var_key == 'x':
                        logx_title = title + "\n(Log x-axis)"
                        logx_filename = f"res_vs_truth_logx_{var_key}_{region_name}_{method}.png"
                        save_2dhist(temp_truth, resolution, truth_label_txt, res_label, logx_title, logx_filename,
                                    target_dir=current_method_output_dir, text_to_display=text, x_scale='log')

    print("\n--- 5. Generating Limited Range Kinematic Plots ---")
    limited_plots_dir = os.path.join(current_beam_energy_output_dir, "Limited_plots")
    os.makedirs(limited_plots_dir, exist_ok=True)
    limited_plot_defs = {'x': [0, 1], 'q2': [0, 600], 'y': [0, 1]}
    for var_key, limits in limited_plot_defs.items():
        truth_col, reco_col = truth_var_mapping[var_key], f"{method}_{var_key}"
        if truth_col in merged_df.columns:
            for method in reco_methods:
                if reco_col in merged_df.columns:
                    current_method_limited_dir = os.path.join(limited_plots_dir, method)
                    os.makedirs(current_method_limited_dir, exist_ok=True)
                    fixed_range = [[limits[0], limits[1]], [limits[0], limits[1]]]
                    truth_label, reco_val_label = f"Truth {var_labels[var_key]}", f"$W^2$" if var_key == 'w' and method in squared_w_methods else var_labels[var_key]
                    reco_label, plot_title = f"Reco {reco_val_label} ({method})", f"{beam_energy}: Reco {reco_val_label} vs Truth {var_labels[var_key]} [LIMITED RANGE]"
                    plot_mask = (merged_df[truth_col] >= limits[0]) & (merged_df[truth_col] <= limits[1]) & (merged_df[reco_col] >= limits[0]) & (merged_df[reco_col] <= limits[1])
                    text = f"Entries in Range: {plot_mask.sum():,}"
                    save_2dhist(merged_df[truth_col], merged_df[reco_col], truth_label, reco_label, plot_title, f"limited_truth_vs_reco_{var_key}_{method}.png", target_dir=current_method_limited_dir, custom_range=fixed_range, text_to_display=text)

    # --- ROOT Histogram Generation with FOCUSED Variable Bins ---
    print("\n--- 6. Generating and saving data-driven ROOT histograms ---")
    TARGET_EVENTS_PER_CELL = 1000.0
    FOCUS_STRENGTH = 1.5 
    root_output_dir = os.path.join(current_beam_energy_output_dir, "root_files")
    os.makedirs(root_output_dir, exist_ok=True)
    root_file_path = os.path.join(root_output_dir, f"{beam_energy}_focused_variable_binned_hists.root")
    root_file = ROOT.TFile(root_file_path, "RECREATE")
    print(f"  Saving ROOT objects to: {root_file_path}")

    truth_x_col, truth_q2_col = truth_var_mapping['x'], truth_var_mapping['q2']
    num_events, num_cells_target = len(merged_df), len(merged_df) / TARGET_EVENTS_PER_CELL
    num_bins_per_axis = max(10, int(np.sqrt(num_cells_target)))
    focused_quantiles = create_focused_quantiles(num_bins_per_axis, focus_strength=FOCUS_STRENGTH)
    truth_x_edges, truth_q2_edges = np.unique(merged_df[truth_x_col].dropna().quantile(focused_quantiles).to_numpy()), np.unique(merged_df[truth_q2_col].dropna().quantile(focused_quantiles).to_numpy())
    if len(truth_x_edges) < 2 or len(truth_q2_edges) < 2:
        print("  Could not determine valid variable binning. Skipping ROOT histograms.")
    else:
        print(f"  Generated {len(truth_x_edges)-1} bins for x and {len(truth_q2_edges)-1} bins for Q2.")
        h_truth = ROOT.TH2D("h_truth_x_q2_focused_bins", f"Truth x vs Q2 ({beam_energy});x_bj;Q^2 (GeV^2)", len(truth_x_edges) - 1, truth_x_edges, len(truth_q2_edges) - 1, truth_q2_edges)
        x_vals, y_vals = merged_df[truth_x_col].to_numpy(), merged_df[truth_q2_col].to_numpy()
        for i in range(len(x_vals)):
            if np.isfinite(x_vals[i]) and np.isfinite(y_vals[i]):
                h_truth.Fill(x_vals[i], y_vals[i])
        h_truth.Write()
        for method in reco_methods:
            reco_x_col, reco_q2_col = f"{method}_x", f"{method}_q2"
            if reco_x_col in merged_df.columns and reco_q2_col in merged_df.columns:
                h_reco = ROOT.TH2D(f"h_reco_{method}_x_q2_focused_bins", f"Reco x vs Q2 ({method}, {beam_energy});x_bj;Q^2 (GeV^2)", len(truth_x_edges) - 1, truth_x_edges, len(truth_q2_edges) - 1, truth_q2_edges)
                x_vals, y_vals = merged_df[reco_x_col].to_numpy(), merged_df[reco_q2_col].to_numpy()
                for i in range(len(x_vals)):
                    if np.isfinite(x_vals[i]) and np.isfinite(y_vals[i]):
                        h_reco.Fill(x_vals[i], y_vals[i])
                h_reco.Write()
    root_file.Close()
    print("  ROOT file creation complete.")
    
    # --- NEW: Generating ROOT Files for High-y Events ---
    print("\n--- Generating High-y Cut ROOT Files (y > 0.1) with focused histograms ---")
    high_y_root_dir = os.path.join(current_beam_energy_output_dir, "high_y_root_files")
    os.makedirs(high_y_root_dir, exist_ok=True)

    for method in reco_methods:
        reco_y_col = f"{method}_y"
        if reco_y_col not in merged_df.columns:
            continue

        df_high_y = merged_df[merged_df[reco_y_col] > 0.1].copy()

        if df_high_y.empty:
            print(f"\n  No events found for method '{method}' with y > 0.1. Skipping.")
            continue
            
        print(f"\n  Processing {len(df_high_y)} high-y events for method: {method}")
        
        # --- Create ROOT file and calculate binning for this high-y subset ---
        root_file_path = os.path.join(high_y_root_dir, f"{beam_energy}_{method}_high_y.root")
        root_file = ROOT.TFile(root_file_path, "RECREATE")
        print(f"    Saving objects to: {root_file_path}")

        num_events = len(df_high_y)
        num_cells_target = num_events / TARGET_EVENTS_PER_CELL
        num_bins_per_axis = max(10, int(np.sqrt(num_cells_target)))
        focused_quantiles = create_focused_quantiles(num_bins_per_axis, focus_strength=FOCUS_STRENGTH)
        
        truth_x_col, truth_q2_col = truth_var_mapping['x'], truth_var_mapping['q2']
        x_edges = np.unique(df_high_y[truth_x_col].dropna().quantile(focused_quantiles).to_numpy())
        q2_edges = np.unique(df_high_y[truth_q2_col].dropna().quantile(focused_quantiles).to_numpy())
        
        if len(x_edges) < 2 or len(q2_edges) < 2:
            print("    Could not determine valid binning for this subset.")
            root_file.Close()
            continue

        # Create and Fill Truth Histogram for the high-y subset
        h_truth = ROOT.TH2D(f"h_truth_x_q2_high_y", f"Truth x vs Q2 (y>0.1, {method});x_bj;Q^2",
                            len(x_edges)-1, x_edges, len(q2_edges)-1, q2_edges)
        x_vals, y_vals = df_high_y[truth_x_col].to_numpy(), df_high_y[truth_q2_col].to_numpy()
        for i in range(len(x_vals)):
            if np.isfinite(x_vals[i]) and np.isfinite(y_vals[i]):
                h_truth.Fill(x_vals[i], y_vals[i])
        h_truth.Write()

        # Create and Fill Reco Histogram for the high-y subset
        reco_x_col, reco_q2_col = f"{method}_x", f"{method}_q2"
        h_reco = ROOT.TH2D(f"h_reco_x_q2_high_y", f"Reco x vs Q2 (y>0.1, {method});x_bj;Q^2",
                           len(x_edges)-1, x_edges, len(q2_edges)-1, q2_edges)
        x_vals, y_vals = df_high_y[reco_x_col].to_numpy(), df_high_y[reco_q2_col].to_numpy()
        for i in range(len(x_vals)):
            if np.isfinite(x_vals[i]) and np.isfinite(y_vals[i]):
                h_reco.Fill(x_vals[i], y_vals[i])
        h_reco.Write()

        root_file.Close()
        print(f"    Successfully created ROOT file with focused histograms.")
    print(f"\nAnalysis for {beam_energy} complete.")

print("\n\nAll processing finished.")
