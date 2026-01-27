#!/usr/bin/env python3
"""
EIC Data Analysis Script

Analyzes EIC (Electron-Ion Collision) data by generating:
- Matplotlib comparison plots (truth vs reconstructed)
- Data-driven, variable-binned ROOT histograms

Usage:
    csv_b2root.py file1.mc_dis.csv file2.mc_dis.csv ... -o /output/directory

The script expects paired CSV files:
- *mc_dis.csv: Monte Carlo truth data
- *reco_dis.csv: Reconstructed data
For each mc_dis.csv file provided, a corresponding reco_dis.csv file must exist.
"""

import argparse
import glob
import itertools
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LogNorm

try:
    import ROOT
    HAS_ROOT = True
except ImportError:
    HAS_ROOT = False
    print("Warning: ROOT not available. ROOT histogram generation will be skipped.")


# =============================================================================
# Configuration
# =============================================================================

@dataclass
class AnalysisConfig:
    """Configuration for analysis parameters."""
    # Variable mappings
    truth_var_mapping: dict = None
    kinematic_vars: list = None
    var_labels: dict = None

    # ROOT histogram parameters
    target_events_per_cell: float = 1000.0
    focus_strength: float = 1.5

    # Agreement threshold for correlation plots
    agreement_threshold: float = 0.20

    # Y-cut regions
    y_cut_threshold: float = 0.1

    def __post_init__(self):
        if self.truth_var_mapping is None:
            self.truth_var_mapping = {'x': 'xbj', 'q2': 'q2', 'y': 'y_d', 'w': 'w'}
        if self.kinematic_vars is None:
            self.kinematic_vars = list(self.truth_var_mapping.keys())
        if self.var_labels is None:
            self.var_labels = {'x': r'$x_{bj}$', 'q2': r'$Q^2$', 'y': 'y', 'w': 'W'}


# =============================================================================
# File Handling
# =============================================================================

def validate_file_pairs(mc_dis_files: list[str]) -> list[tuple[str, str]]:
    """
    Validate that each mc_dis.csv file has a corresponding reco_dis.csv file.

    Args:
        mc_dis_files: List of mc_dis.csv file paths

    Returns:
        List of tuples (mc_dis_path, reco_dis_path)

    Raises:
        FileNotFoundError: If a corresponding reco_dis.csv file is missing
    """
    pairs = []
    missing_files = []

    for mc_file in mc_dis_files:
        # Convert mc_dis.csv -> reco_dis.csv
        reco_file = mc_file.replace('mc_dis.csv', 'reco_dis.csv')

        if not os.path.exists(reco_file):
            missing_files.append(reco_file)
        else:
            pairs.append((mc_file, reco_file))

    if missing_files:
        raise FileNotFoundError(
            f"Missing corresponding reco_dis.csv files:\n"
            + "\n".join(f"  - {f}" for f in missing_files)
        )

    return pairs


def extract_beam_energy(filepath: str) -> Optional[str]:
    """
    Extract beam energy from filename (e.g., '5x41', '10x100', '18x275').

    Args:
        filepath: Path to the file

    Returns:
        Beam energy string or None if not found
    """
    filename = os.path.basename(filepath)
    match = re.search(r'(\d+x\d+)', filename)
    return match.group(1) if match else None


def group_files_by_beam_energy(file_pairs: list[tuple[str, str]]) -> dict[str, list[tuple[str, str]]]:
    """
    Group file pairs by beam energy.

    Args:
        file_pairs: List of (mc_dis, reco_dis) file path tuples

    Returns:
        Dictionary mapping beam energy to list of file pairs
    """
    grouped = {}
    for mc_file, reco_file in file_pairs:
        energy = extract_beam_energy(mc_file)
        if energy is None:
            energy = 'unknown'
        grouped.setdefault(energy, []).append((mc_file, reco_file))
    return grouped


# =============================================================================
# Data Loading
# =============================================================================

def load_csv_with_unique_events(filepath: str, key_column: str = 'evt',
                                 offset: int = 0) -> tuple[pd.DataFrame, int]:
    """
    Load a CSV file and adjust event IDs to be globally unique.

    Args:
        filepath: Path to CSV file
        key_column: Column name for event ID
        offset: Starting offset for event IDs

    Returns:
        Tuple of (DataFrame, new_offset)
    """
    try:
        df = pd.read_csv(filepath)
        df.columns = [col.strip().strip(',') for col in df.columns]

        if df.empty:
            return pd.DataFrame(), offset

        # Handle column naming variations
        if key_column not in df.columns:
            if 'event' in df.columns and key_column == 'evt':
                df = df.rename(columns={'event': 'evt'})
            else:
                print(f"Warning: Key column '{key_column}' not found in {filepath}")
                return pd.DataFrame(), offset

        df[key_column] = pd.to_numeric(df[key_column], errors="coerce")
        df[key_column] += offset

        max_evt = df[key_column].max()
        new_offset = int(max_evt) + 1 if pd.notna(max_evt) else offset

        return df, new_offset

    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return pd.DataFrame(), offset


def load_file_pairs(file_pairs: list[tuple[str, str]],
                    key_column: str = 'evt') -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load and concatenate multiple file pairs.

    Args:
        file_pairs: List of (mc_dis, reco_dis) file path tuples
        key_column: Column name for event ID

    Returns:
        Tuple of (mc_dis_df, reco_df)
    """
    mc_dfs = []
    reco_dfs = []
    mc_offset = 0
    reco_offset = 0

    for mc_file, reco_file in sorted(file_pairs):
        mc_df, mc_offset = load_csv_with_unique_events(mc_file, key_column, mc_offset)
        reco_df, reco_offset = load_csv_with_unique_events(reco_file, key_column, reco_offset)

        if not mc_df.empty:
            mc_dfs.append(mc_df)
        if not reco_df.empty:
            reco_dfs.append(reco_df)

    mc_combined = pd.concat(mc_dfs, ignore_index=True) if mc_dfs else pd.DataFrame()
    reco_combined = pd.concat(reco_dfs, ignore_index=True) if reco_dfs else pd.DataFrame()

    return mc_combined, reco_combined


def extract_reco_methods(reco_df: pd.DataFrame) -> list[str]:
    """
    Extract reconstruction method names from column prefixes.

    Args:
        reco_df: Reconstructed data DataFrame

    Returns:
        Sorted list of method names
    """
    methods = set()
    for col in reco_df.columns:
        if '_' in col and col != 'evt' and not col.startswith('mc_'):
            methods.add(col.split('_')[0])
    return sorted(methods)


def apply_kinematic_cuts(df: pd.DataFrame, reco_methods: list[str]) -> pd.DataFrame:
    """
    Apply global kinematic cuts (0 <= x, y <= 1 for all methods).

    Args:
        df: Merged DataFrame
        reco_methods: List of reconstruction method names

    Returns:
        Filtered DataFrame
    """
    mask = pd.Series(True, index=df.index)

    for method in reco_methods:
        for var in ['x', 'y']:
            col = f"{method}_{var}"
            if col in df.columns:
                mask &= (df[col] >= 0) & (df[col] <= 1)

    return df[mask].copy()


# =============================================================================
# Plotting Utilities
# =============================================================================

def compute_data_range(arr: np.ndarray, use_percentiles: bool = True) -> tuple[float, float]:
    """Compute data range for histograms."""
    if not np.any(arr):
        return (0, 1)
    if use_percentiles:
        lo, hi = np.percentile(arr, [1, 99])
    else:
        lo, hi = np.nanmin(arr), np.nanmax(arr)
    return (lo, hi) if lo != hi else (lo, lo + 1e-6)


def save_2d_histogram(x: np.ndarray, y: np.ndarray, xlabel: str, ylabel: str,
                      title: str, filename: str, output_dir: str,
                      bins: int = 100, use_percentiles: bool = True,
                      vmin: float = 1, custom_range: list = None,
                      annotation: str = None, x_scale: str = 'linear',
                      y_scale: str = 'linear') -> None:
    """
    Create and save a 2D histogram plot.

    Args:
        x, y: Data arrays
        xlabel, ylabel: Axis labels
        title: Plot title
        filename: Output filename
        output_dir: Output directory
        bins: Number of bins
        use_percentiles: Whether to use percentile-based ranges
        vmin: Minimum count for color scale
        custom_range: Custom [[xmin, xmax], [ymin, ymax]] range
        annotation: Text annotation for the plot
        x_scale, y_scale: 'linear' or 'log'
    """
    # Create mask for valid data
    mask = np.isfinite(x) & np.isfinite(y)
    if x_scale == 'log':
        mask &= (x > 0)
    if y_scale == 'log':
        mask &= (y > 0)

    if not np.any(mask):
        print(f"Skipping {filename}: no valid data for specified scale.")
        return

    x_filtered = x[mask]
    y_filtered = y[mask]

    # Determine data range
    if custom_range:
        data_range = custom_range
    else:
        data_range = [
            compute_data_range(x_filtered, use_percentiles),
            compute_data_range(y_filtered, use_percentiles)
        ]

    # Create plot
    plt.figure()
    plt.xscale(x_scale)
    plt.yscale(y_scale)
    plt.hist2d(x_filtered, y_filtered, bins=bins, cmap='viridis',
               range=data_range, norm=LogNorm(vmin=vmin))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.colorbar(label="Counts")
    plt.title(title, fontsize=10)

    if annotation:
        plt.text(0.05, 0.95, annotation, transform=plt.gca().transAxes, fontsize=8,
                 verticalalignment='top',
                 bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.5))

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()


def save_1d_histogram(data: np.ndarray, xlabel: str, ylabel: str,
                      title: str, filename: str, output_dir: str,
                      bins: int = 200, plot_range: tuple = None,
                      color: str = 'steelblue', annotation: str = None) -> None:
    """
    Create and save a 1D histogram plot.

    Args:
        data: Data array
        xlabel, ylabel: Axis labels
        title: Plot title
        filename: Output filename
        output_dir: Output directory
        bins: Number of bins
        plot_range: (min, max) range for histogram
        color: Histogram color
        annotation: Text annotation for the plot
    """
    mask = np.isfinite(data)
    if not np.any(mask):
        print(f"Skipping {filename}: no finite data.")
        return

    plt.figure()
    plt.hist(data[mask], bins=bins, range=plot_range, histtype='stepfilled', color=color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title, fontsize=10)

    if annotation:
        plt.text(0.05, 0.95, annotation, transform=plt.gca().transAxes, fontsize=8,
                 verticalalignment='top',
                 bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.5))

    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()


# =============================================================================
# Plot Generation Functions
# =============================================================================

def generate_truth_vs_reco_plots(df: pd.DataFrame, reco_methods: list[str],
                                  config: AnalysisConfig, beam_energy: str,
                                  output_dir: str) -> None:
    """Generate truth vs reconstructed kinematic plots."""
    print("\n--- Generating Truth vs Reconstructed Plots ---")

    for var_key in config.kinematic_vars:
        truth_col = config.truth_var_mapping[var_key]
        if truth_col not in df.columns:
            continue

        for method in reco_methods:
            reco_col = f"{method}_{var_key}"
            if reco_col not in df.columns:
                continue

            method_dir = os.path.join(output_dir, method)
            os.makedirs(method_dir, exist_ok=True)

            var_label = config.var_labels[var_key]
            truth_label = f"Truth {var_label}"
            reco_label = f"Reco {var_label} ({method})"
            title = f"{beam_energy}: {reco_label} vs {truth_label}"

            mask = df[truth_col].notna() & df[reco_col].notna()
            annotation = f"Entries: {mask.sum():,}"

            save_2d_histogram(
                df[truth_col].values, df[reco_col].values,
                truth_label, reco_label, title,
                f"truth_vs_reco_{var_key}_{method}.png",
                method_dir, annotation=annotation
            )

            # Log x-axis version for x variable
            if var_key == 'x':
                save_2d_histogram(
                    df[truth_col].values, df[reco_col].values,
                    truth_label, reco_label, f"{title} (Log x-axis)",
                    f"truth_vs_reco_logx_{var_key}_{method}.png",
                    method_dir, annotation=annotation, x_scale='log'
                )


def generate_correlation_plots(df: pd.DataFrame, reco_methods: list[str],
                                config: AnalysisConfig, beam_energy: str,
                                output_dir: str) -> None:
    """Generate intra-kinematic variable correlation plots."""
    print("\n--- Generating Correlation Plots ---")

    truth_dir = os.path.join(output_dir, "truth")
    os.makedirs(truth_dir, exist_ok=True)

    for var1, var2 in itertools.combinations(config.kinematic_vars, 2):
        truth_col1 = config.truth_var_mapping[var1]
        truth_col2 = config.truth_var_mapping[var2]
        label1 = config.var_labels[var1]
        label2 = config.var_labels[var2]

        # Truth correlations
        if truth_col1 in df.columns and truth_col2 in df.columns:
            mask = df[truth_col1].notna() & df[truth_col2].notna()
            title = f"{beam_energy}: Truth {label1} vs {label2}"
            annotation = f"Entries: {mask.sum():,}"

            save_2d_histogram(
                df[truth_col1].values, df[truth_col2].values,
                f"Truth {label1}", f"Truth {label2}", title,
                f"truth_{var1}_vs_{var2}.png",
                truth_dir, annotation=annotation
            )

            if var1 == 'x':
                save_2d_histogram(
                    df[truth_col1].values, df[truth_col2].values,
                    f"Truth {label1}", f"Truth {label2}", f"{title} (Log x-axis)",
                    f"truth_logx_{var1}_vs_{var2}.png",
                    truth_dir, annotation=annotation, x_scale='log'
                )

        # Reco correlations per method
        for method in reco_methods:
            reco_col1 = f"{method}_{var1}"
            reco_col2 = f"{method}_{var2}"

            if reco_col1 not in df.columns or reco_col2 not in df.columns:
                continue

            method_dir = os.path.join(output_dir, method)
            os.makedirs(method_dir, exist_ok=True)

            reco_label1 = f"Reco {label1} ({method})"
            reco_label2 = f"Reco {label2} ({method})"
            title = f"{beam_energy}: Reco {label1} vs {label2} ({method})"

            mask = df[reco_col1].notna() & df[reco_col2].notna()
            total_events = mask.sum()
            annotation = f"Entries: {total_events:,}"

            # Add agreement statistics for x-Q2 plots
            if {var1, var2} == {'x', 'q2'} and total_events > 0:
                df_agree = df[mask]
                for v in ['x', 'q2']:
                    truth_v = config.truth_var_mapping[v]
                    reco_v = f"{method}_{v}"
                    if truth_v in df_agree.columns:
                        res = (df_agree[reco_v] - df_agree[truth_v]) / df_agree[truth_v]
                        agree_count = (abs(res) < config.agreement_threshold).sum()
                        pct = (agree_count / total_events) * 100
                        v_label = 'x' if v == 'x' else 'Q\u00b2'
                        annotation += f"\n{v_label} agree (\u00b1{config.agreement_threshold:.0%}): {pct:.1f}%"

            save_2d_histogram(
                df[reco_col1].values, df[reco_col2].values,
                reco_label1, reco_label2, title,
                f"reco_{var1}_vs_{var2}_{method}.png",
                method_dir, annotation=annotation
            )

            if var1 == 'x':
                save_2d_histogram(
                    df[reco_col1].values, df[reco_col2].values,
                    reco_label1, reco_label2, f"{title} (Log x-axis)",
                    f"reco_logx_{var1}_vs_{var2}_{method}.png",
                    method_dir, annotation=annotation, x_scale='log'
                )


def generate_resolution_plots(df: pd.DataFrame, reco_methods: list[str],
                               config: AnalysisConfig, beam_energy: str,
                               output_dir: str) -> None:
    """Generate resolution histograms (1D and 2D)."""
    print("\n--- Generating Resolution Plots ---")

    for var_key in config.kinematic_vars:
        truth_col = config.truth_var_mapping[var_key]
        if truth_col not in df.columns:
            continue

        for method in reco_methods:
            reco_col = f"{method}_{var_key}"
            if reco_col not in df.columns:
                continue

            method_dir = os.path.join(output_dir, method)
            os.makedirs(method_dir, exist_ok=True)

            # Compute resolution
            mask = (np.isfinite(df[truth_col]) &
                    np.isfinite(df[reco_col]) &
                    (df[truth_col] != 0))

            if not mask.any():
                continue

            truth_vals = df.loc[mask, truth_col]
            reco_vals = df.loc[mask, reco_col]
            resolution = (reco_vals - truth_vals) / truth_vals

            var_label = config.var_labels[var_key]
            truth_label = f"Truth {var_label}"
            reco_label = f"Reco {var_label}"
            res_label = f"({reco_label} - {truth_label}) / {truth_label}"

            # 1D resolution histogram
            save_1d_histogram(
                resolution.values, res_label, "Counts",
                f"{beam_energy}: {res_label} ({method})",
                f"{var_key}_resolution_hist_{method}.png",
                method_dir, plot_range=(-1, 1),
                annotation=f"Entries: {len(resolution):,}"
            )

            # 2D resolution vs truth
            save_2d_histogram(
                truth_vals.values, resolution.values,
                truth_label, res_label,
                f"{beam_energy}: Resolution vs Truth ({method})",
                f"{var_key}_res_vs_truth_{method}.png",
                method_dir, annotation=f"Entries: {len(resolution):,}"
            )

            if var_key == 'x':
                save_2d_histogram(
                    truth_vals.values, resolution.values,
                    truth_label, res_label,
                    f"{beam_energy}: Resolution vs Truth ({method}) (Log x-axis)",
                    f"{var_key}_res_vs_truth_logx_{method}.png",
                    method_dir, annotation=f"Entries: {len(resolution):,}",
                    x_scale='log'
                )


def generate_y_cut_plots(df: pd.DataFrame, reco_methods: list[str],
                          config: AnalysisConfig, beam_energy: str,
                          output_dir: str) -> None:
    """Generate resolution plots with y-cuts."""
    print("\n--- Generating Y-Cut Resolution Plots ---")

    y_cut_dir = os.path.join(output_dir, "y_cut_resolution_plots")
    os.makedirs(y_cut_dir, exist_ok=True)

    y_regions = {
        'low_y': {'threshold': lambda y: y <= config.y_cut_threshold,
                  'label': f'y <= {config.y_cut_threshold}'},
        'high_y': {'threshold': lambda y: y > config.y_cut_threshold,
                   'label': f'y > {config.y_cut_threshold}'}
    }

    for method in reco_methods:
        reco_y_col = f"{method}_y"
        if reco_y_col not in df.columns:
            continue

        print(f"  Processing y-cut plots for method: {method}")

        # Apply method-specific kinematic cuts
        method_mask = pd.Series(True, index=df.index)
        for var in ['x', 'y']:
            col = f"{method}_{var}"
            if col in df.columns:
                method_mask &= (df[col] >= 0) & (df[col] <= 1)

        for region_name, region_info in y_regions.items():
            region_mask = method_mask & region_info['threshold'](df[reco_y_col])
            df_region = df[region_mask]

            if df_region.empty:
                continue

            for var_key in ['x', 'q2']:
                truth_col = config.truth_var_mapping[var_key]
                reco_col = f"{method}_{var_key}"

                if truth_col not in df_region.columns or reco_col not in df_region.columns:
                    continue

                method_cut_dir = os.path.join(y_cut_dir, method)
                os.makedirs(method_cut_dir, exist_ok=True)

                # Compute resolution
                mask = (np.isfinite(df_region[truth_col]) &
                        np.isfinite(df_region[reco_col]) &
                        (df_region[truth_col] != 0))

                if not mask.any():
                    continue

                truth_vals = df_region.loc[mask, truth_col]
                reco_vals = df_region.loc[mask, reco_col]
                resolution = (reco_vals - truth_vals) / truth_vals

                var_label = config.var_labels[var_key]
                truth_label = f"Truth {var_label}"
                res_label = f"({var_label} Reco - Truth) / Truth"
                title = f"{beam_energy}: {var_label} Resolution vs Truth\n(Cut: {region_info['label']}, Method: {method})"
                annotation = f"Entries: {len(resolution):,}"

                save_2d_histogram(
                    truth_vals.values, resolution.values,
                    truth_label, res_label, title,
                    f"res_vs_truth_{var_key}_{region_name}_{method}.png",
                    method_cut_dir, annotation=annotation
                )

                if var_key == 'x':
                    save_2d_histogram(
                        truth_vals.values, resolution.values,
                        truth_label, res_label, f"{title}\n(Log x-axis)",
                        f"res_vs_truth_logx_{var_key}_{region_name}_{method}.png",
                        method_cut_dir, annotation=annotation, x_scale='log'
                    )


def generate_limited_range_plots(df: pd.DataFrame, reco_methods: list[str],
                                  config: AnalysisConfig, beam_energy: str,
                                  output_dir: str) -> None:
    """Generate plots with limited kinematic ranges."""
    print("\n--- Generating Limited Range Plots ---")

    limited_dir = os.path.join(output_dir, "Limited_plots")
    os.makedirs(limited_dir, exist_ok=True)

    range_limits = {'x': [0, 1], 'q2': [0, 600], 'y': [0, 1]}

    for var_key, limits in range_limits.items():
        truth_col = config.truth_var_mapping[var_key]
        if truth_col not in df.columns:
            continue

        for method in reco_methods:
            reco_col = f"{method}_{var_key}"
            if reco_col not in df.columns:
                continue

            method_dir = os.path.join(limited_dir, method)
            os.makedirs(method_dir, exist_ok=True)

            var_label = config.var_labels[var_key]
            truth_label = f"Truth {var_label}"
            reco_label = f"Reco {var_label} ({method})"
            title = f"{beam_energy}: {reco_label} vs {truth_label} [LIMITED RANGE]"

            mask = ((df[truth_col] >= limits[0]) & (df[truth_col] <= limits[1]) &
                    (df[reco_col] >= limits[0]) & (df[reco_col] <= limits[1]))
            annotation = f"Entries in Range: {mask.sum():,}"

            save_2d_histogram(
                df[truth_col].values, df[reco_col].values,
                truth_label, reco_label, title,
                f"limited_truth_vs_reco_{var_key}_{method}.png",
                method_dir, annotation=annotation,
                custom_range=[limits, limits]
            )


# =============================================================================
# ROOT Histogram Generation
# =============================================================================

def create_focused_quantiles(num_bins: int, focus_strength: float = 1.5) -> np.ndarray:
    """
    Create quantile values with focus on low-end of spectrum.

    Args:
        num_bins: Number of bins
        focus_strength: Higher values = more focus on low end

    Returns:
        Array of quantile values
    """
    linear_space = np.linspace(0.0, 1.0, num_bins + 1)
    return linear_space ** focus_strength


def generate_root_histograms(df: pd.DataFrame, reco_methods: list[str],
                              config: AnalysisConfig, beam_energy: str,
                              output_dir: str) -> None:
    """Generate data-driven ROOT histograms with variable binning."""
    if not HAS_ROOT:
        print("\n--- Skipping ROOT histograms (ROOT not available) ---")
        return

    print("\n--- Generating ROOT Histograms ---")

    root_dir = os.path.join(output_dir, "root_files")
    os.makedirs(root_dir, exist_ok=True)

    truth_x_col = config.truth_var_mapping['x']
    truth_q2_col = config.truth_var_mapping['q2']

    # Calculate binning
    num_events = len(df)
    num_cells_target = num_events / config.target_events_per_cell
    num_bins = max(10, int(np.sqrt(num_cells_target)))

    focused_quantiles = create_focused_quantiles(num_bins, config.focus_strength)

    x_edges = np.unique(df[truth_x_col].dropna().quantile(focused_quantiles).to_numpy())
    q2_edges = np.unique(df[truth_q2_col].dropna().quantile(focused_quantiles).to_numpy())

    if len(x_edges) < 2 or len(q2_edges) < 2:
        print("  Could not determine valid binning. Skipping ROOT histograms.")
        return

    print(f"  Generated {len(x_edges)-1} bins for x and {len(q2_edges)-1} bins for Q2.")

    # Create main ROOT file
    root_path = os.path.join(root_dir, f"{beam_energy}_focused_variable_binned_hists.root")
    root_file = ROOT.TFile(root_path, "RECREATE")
    print(f"  Saving to: {root_path}")

    # Truth histogram
    h_truth = ROOT.TH2D(
        "h_truth_x_q2_focused_bins",
        f"Truth x vs Q2 ({beam_energy});x_bj;Q^2 (GeV^2)",
        len(x_edges) - 1, x_edges,
        len(q2_edges) - 1, q2_edges
    )

    x_vals = df[truth_x_col].to_numpy()
    q2_vals = df[truth_q2_col].to_numpy()
    for i in range(len(x_vals)):
        if np.isfinite(x_vals[i]) and np.isfinite(q2_vals[i]):
            h_truth.Fill(x_vals[i], q2_vals[i])
    h_truth.Write()

    # Reco histograms per method
    for method in reco_methods:
        reco_x_col = f"{method}_x"
        reco_q2_col = f"{method}_q2"

        if reco_x_col not in df.columns or reco_q2_col not in df.columns:
            continue

        h_reco = ROOT.TH2D(
            f"h_reco_{method}_x_q2_focused_bins",
            f"Reco x vs Q2 ({method}, {beam_energy});x_bj;Q^2 (GeV^2)",
            len(x_edges) - 1, x_edges,
            len(q2_edges) - 1, q2_edges
        )

        x_vals = df[reco_x_col].to_numpy()
        q2_vals = df[reco_q2_col].to_numpy()
        for i in range(len(x_vals)):
            if np.isfinite(x_vals[i]) and np.isfinite(q2_vals[i]):
                h_reco.Fill(x_vals[i], q2_vals[i])
        h_reco.Write()

    root_file.Close()


def generate_high_y_root_histograms(df: pd.DataFrame, reco_methods: list[str],
                                     config: AnalysisConfig, beam_energy: str,
                                     output_dir: str) -> None:
    """Generate ROOT histograms for high-y events."""
    if not HAS_ROOT:
        return

    print("\n--- Generating High-y ROOT Histograms (y > 0.1) ---")

    high_y_dir = os.path.join(output_dir, "high_y_root_files")
    os.makedirs(high_y_dir, exist_ok=True)

    truth_x_col = config.truth_var_mapping['x']
    truth_q2_col = config.truth_var_mapping['q2']

    for method in reco_methods:
        reco_y_col = f"{method}_y"
        if reco_y_col not in df.columns:
            continue

        df_high_y = df[df[reco_y_col] > config.y_cut_threshold].copy()

        if df_high_y.empty:
            print(f"  No high-y events for method '{method}'. Skipping.")
            continue

        print(f"  Processing {len(df_high_y)} high-y events for method: {method}")

        # Calculate binning for subset
        num_events = len(df_high_y)
        num_cells_target = num_events / config.target_events_per_cell
        num_bins = max(10, int(np.sqrt(num_cells_target)))

        focused_quantiles = create_focused_quantiles(num_bins, config.focus_strength)

        x_edges = np.unique(df_high_y[truth_x_col].dropna().quantile(focused_quantiles).to_numpy())
        q2_edges = np.unique(df_high_y[truth_q2_col].dropna().quantile(focused_quantiles).to_numpy())

        if len(x_edges) < 2 or len(q2_edges) < 2:
            print(f"    Could not determine valid binning for {method}.")
            continue

        # Create ROOT file
        root_path = os.path.join(high_y_dir, f"{beam_energy}_{method}_high_y.root")
        root_file = ROOT.TFile(root_path, "RECREATE")
        print(f"    Saving to: {root_path}")

        # Truth histogram
        h_truth = ROOT.TH2D(
            "h_truth_x_q2_high_y",
            f"Truth x vs Q2 (y>0.1, {method});x_bj;Q^2",
            len(x_edges) - 1, x_edges,
            len(q2_edges) - 1, q2_edges
        )

        x_vals = df_high_y[truth_x_col].to_numpy()
        q2_vals = df_high_y[truth_q2_col].to_numpy()
        for i in range(len(x_vals)):
            if np.isfinite(x_vals[i]) and np.isfinite(q2_vals[i]):
                h_truth.Fill(x_vals[i], q2_vals[i])
        h_truth.Write()

        # Reco histogram
        reco_x_col = f"{method}_x"
        reco_q2_col = f"{method}_q2"

        h_reco = ROOT.TH2D(
            "h_reco_x_q2_high_y",
            f"Reco x vs Q2 (y>0.1, {method});x_bj;Q^2",
            len(x_edges) - 1, x_edges,
            len(q2_edges) - 1, q2_edges
        )

        x_vals = df_high_y[reco_x_col].to_numpy()
        q2_vals = df_high_y[reco_q2_col].to_numpy()
        for i in range(len(x_vals)):
            if np.isfinite(x_vals[i]) and np.isfinite(q2_vals[i]):
                h_reco.Fill(x_vals[i], q2_vals[i])
        h_reco.Write()

        root_file.Close()


# =============================================================================
# Main Analysis Pipeline
# =============================================================================

def analyze_beam_energy(file_pairs: list[tuple[str, str]], beam_energy: str,
                        output_dir: str, config: AnalysisConfig) -> None:
    """
    Run full analysis pipeline for a single beam energy.

    Args:
        file_pairs: List of (mc_dis, reco_dis) file path tuples
        beam_energy: Beam energy string (e.g., '5x41')
        output_dir: Output directory for this beam energy
        config: Analysis configuration
    """
    print(f"\n{'='*80}")
    print(f"--- Processing Beam Energy: {beam_energy} ---")
    print(f"{'='*80}")

    os.makedirs(output_dir, exist_ok=True)

    # Load data
    print("\n--- Loading CSV Data ---")
    mc_df, reco_df = load_file_pairs(file_pairs)

    if mc_df.empty or reco_df.empty:
        print(f"Skipping {beam_energy}: A required dataframe is empty.")
        return

    # Merge datasets
    merged_df = pd.merge(mc_df, reco_df, on='evt', how='inner')
    if merged_df.empty:
        print(f"Skipping {beam_energy}: Merged DataFrame is empty.")
        return

    print(f"  Loaded {len(merged_df)} merged events")

    # Extract reconstruction methods
    reco_methods = extract_reco_methods(reco_df)
    print(f"  Found reconstruction methods: {reco_methods}")

    # Apply kinematic cuts
    print("\n--- Applying Kinematic Cuts ---")
    initial_rows = len(merged_df)
    merged_df = apply_kinematic_cuts(merged_df, reco_methods)
    print(f"  Kept {len(merged_df)} of {initial_rows} events after cuts.")

    if merged_df.empty:
        print("DataFrame empty after cuts. Skipping all plots.")
        return

    # Generate all plots
    generate_truth_vs_reco_plots(merged_df, reco_methods, config, beam_energy, output_dir)
    generate_correlation_plots(merged_df, reco_methods, config, beam_energy, output_dir)
    generate_resolution_plots(merged_df, reco_methods, config, beam_energy, output_dir)
    generate_y_cut_plots(merged_df, reco_methods, config, beam_energy, output_dir)
    generate_limited_range_plots(merged_df, reco_methods, config, beam_energy, output_dir)
    generate_root_histograms(merged_df, reco_methods, config, beam_energy, output_dir)
    generate_high_y_root_histograms(merged_df, reco_methods, config, beam_energy, output_dir)

    print(f"\nAnalysis for {beam_energy} complete.")


# =============================================================================
# CLI Entry Point
# =============================================================================

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Analyze EIC data: generate plots and ROOT histograms from CSV files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Analyze specific files
    %(prog)s data_5x41.mc_dis.csv data_10x100.mc_dis.csv -o ./output

    # Use glob patterns (shell expansion)
    %(prog)s /data/*mc_dis.csv -o ./analysis_output

Notes:
    - For each *mc_dis.csv file, a corresponding *reco_dis.csv file must exist
    - Files are automatically grouped by beam energy (e.g., 5x41, 10x100, 18x275)
    - Output is organized into subdirectories by beam energy
        """
    )

    parser.add_argument(
        'input_files',
        nargs='+',
        metavar='FILE',
        help='Input mc_dis.csv files. Corresponding reco_dis.csv files must exist.'
    )

    parser.add_argument(
        '-o', '--output',
        required=True,
        metavar='DIR',
        help='Output directory for plots and ROOT files'
    )

    parser.add_argument(
        '--events-per-cell',
        type=float,
        default=1000.0,
        metavar='N',
        help='Target events per ROOT histogram cell (default: 1000)'
    )

    parser.add_argument(
        '--focus-strength',
        type=float,
        default=1.5,
        metavar='F',
        help='Focus strength for variable binning (default: 1.5, higher = more low-end focus)'
    )

    parser.add_argument(
        '--y-cut',
        type=float,
        default=0.1,
        metavar='Y',
        help='Y-cut threshold for high/low y separation (default: 0.1)'
    )

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()

    # Validate input files
    print("Validating input files...")
    try:
        file_pairs = validate_file_pairs(args.input_files)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(file_pairs)} valid file pairs.")

    # Group by beam energy
    grouped = group_files_by_beam_energy(file_pairs)
    print(f"Beam energies to process: {list(grouped.keys())}")

    # Create output directory
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {output_dir}")

    # Create configuration
    config = AnalysisConfig(
        target_events_per_cell=args.events_per_cell,
        focus_strength=args.focus_strength,
        y_cut_threshold=args.y_cut
    )

    # Process each beam energy
    for beam_energy, pairs in grouped.items():
        energy_output_dir = os.path.join(output_dir, beam_energy)
        analyze_beam_energy(pairs, beam_energy, energy_output_dir, config)

    print("\n\nAll processing finished.")


if __name__ == "__main__":
    main()
