#!/usr/bin/env python3
"""
EIC Data Analysis Script

Analyzes EIC (Electron-Ion Collision) data by generating matplotlib plots
comparing truth vs reconstructed kinematics.

Usage:
    csv_b2root.py file1.mc_dis.csv file1.reco_dis.csv ... -o /output/directory

The script expects paired CSV files (can be in different directories):
- *mc_dis.csv: Monte Carlo truth data
- *reco_dis.csv: Reconstructed data
Files are paired by base name: foo.mc_dis.csv pairs with foo.reco_dis.csv

Input CSV format (see docs/data-csv.md):
- mc_dis.csv: Truth event-level values (evt, xbj, q2, y_d, w, ...)
- reco_dis.csv: Reconstructed kinematics with method prefixes
  (da_x, da_q2, electron_x, jb_x, etc.)
"""

import argparse
import itertools
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LogNorm


# =============================================================================
# Configuration
# =============================================================================

# Truth column names in mc_dis.csv -> short keys
TRUTH_VAR_MAPPING = {'x': 'xbj', 'q2': 'q2', 'y': 'y_d', 'w': 'w'}
KINEMATIC_VARS = list(TRUTH_VAR_MAPPING.keys())
VAR_LABELS = {'x': r'$x_{bj}$', 'q2': r'$Q^2$', 'y': 'y', 'w': 'W'}

# Analysis parameters
AGREEMENT_THRESHOLD = 0.20
Y_CUT_THRESHOLD = 0.1


# =============================================================================
# File Handling
# =============================================================================

def validate_file_pairs(input_files: list[str]) -> list[tuple[str, str]]:
    """
    Validate input files and pair mc_dis.csv with reco_dis.csv by base name.

    Files are paired by their base name (ignoring directory):
    - foo.mc_dis.csv pairs with foo.reco_dis.csv
    - Files can be in different directories
    """
    mc_files = {}  # base_name -> full_path
    reco_files = {}  # base_name -> full_path
    ignored_files = []

    for f in input_files:
        basename = os.path.basename(f)
        if basename.endswith('.mc_dis.csv'):
            base_name = basename[:-len('.mc_dis.csv')]
            mc_files[base_name] = f
        elif basename.endswith('.reco_dis.csv'):
            base_name = basename[:-len('.reco_dis.csv')]
            reco_files[base_name] = f
        else:
            ignored_files.append(f)

    if ignored_files:
        print(f"Warning: Ignoring {len(ignored_files)} file(s) with unrecognized suffix:")
        for f in ignored_files:
            print(f"  - {os.path.basename(f)}")

    # Find matching pairs
    pairs = []
    mc_only = []
    reco_only = []

    all_bases = set(mc_files.keys()) | set(reco_files.keys())
    for base_name in sorted(all_bases):
        has_mc = base_name in mc_files
        has_reco = base_name in reco_files
        if has_mc and has_reco:
            pairs.append((mc_files[base_name], reco_files[base_name]))
        elif has_mc:
            mc_only.append(mc_files[base_name])
        else:
            reco_only.append(reco_files[base_name])

    # Report errors
    errors = []
    if mc_only:
        errors.append("mc_dis.csv files without matching reco_dis.csv:\n" +
                      "\n".join(f"  - {os.path.basename(f)}" for f in mc_only))
    if reco_only:
        errors.append("reco_dis.csv files without matching mc_dis.csv:\n" +
                      "\n".join(f"  - {os.path.basename(f)}" for f in reco_only))

    if errors:
        raise ValueError("\n".join(errors))

    if not pairs:
        raise ValueError("No valid file pairs found. Please provide matching "
                         "*mc_dis.csv and *reco_dis.csv files.")

    return pairs


# =============================================================================
# Data Loading
# =============================================================================

def load_csv_with_unique_events(filepath: str, key_column: str = 'evt',
                                 offset: int = 0) -> tuple[pd.DataFrame, int]:
    """Load a CSV file and adjust event IDs to be globally unique."""
    try:
        df = pd.read_csv(filepath)
        df.columns = [col.strip().strip(',') for col in df.columns]

        if df.empty:
            return pd.DataFrame(), offset

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
    """Load and concatenate multiple file pairs."""
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
    """Extract reconstruction method names from column prefixes."""
    methods = set()
    for col in reco_df.columns:
        if '_' in col and col != 'evt' and not col.startswith('mc_'):
            methods.add(col.split('_')[0])
    return sorted(methods)


def apply_kinematic_cuts(df: pd.DataFrame, reco_methods: list[str]) -> pd.DataFrame:
    """Apply global kinematic cuts (0 <= x, y <= 1 for all methods)."""
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
    """Create and save a 2D histogram plot."""
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

    if custom_range:
        data_range = custom_range
    else:
        data_range = [
            compute_data_range(x_filtered, use_percentiles),
            compute_data_range(y_filtered, use_percentiles)
        ]

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
    """Create and save a 1D histogram plot."""
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
                                  output_dir: str) -> None:
    """Generate truth vs reconstructed kinematic plots."""
    print("\n--- Generating Truth vs Reconstructed Plots ---")

    for var_key in KINEMATIC_VARS:
        truth_col = TRUTH_VAR_MAPPING[var_key]
        if truth_col not in df.columns:
            continue

        for method in reco_methods:
            reco_col = f"{method}_{var_key}"
            if reco_col not in df.columns:
                continue

            var_label = VAR_LABELS[var_key]
            truth_label = f"Truth {var_label}"
            reco_label = f"Reco {var_label} ({method})"
            title = f"Reco {var_label} vs Truth ({method})"

            mask = df[truth_col].notna() & df[reco_col].notna()
            annotation = f"Entries: {mask.sum():,}"

            save_2d_histogram(
                df[truth_col].values, df[reco_col].values,
                truth_label, reco_label, title,
                f"truth_vs_reco_{var_key}_{method}.png",
                output_dir, annotation=annotation
            )

            if var_key == 'x':
                save_2d_histogram(
                    df[truth_col].values, df[reco_col].values,
                    truth_label, reco_label, f"{title} (Log x-axis)",
                    f"truth_vs_reco_logx_{var_key}_{method}.png",
                    output_dir, annotation=annotation, x_scale='log'
                )


def generate_correlation_plots(df: pd.DataFrame, reco_methods: list[str],
                                output_dir: str) -> None:
    """Generate intra-kinematic variable correlation plots."""
    print("\n--- Generating Correlation Plots ---")

    for var1, var2 in itertools.combinations(KINEMATIC_VARS, 2):
        truth_col1 = TRUTH_VAR_MAPPING[var1]
        truth_col2 = TRUTH_VAR_MAPPING[var2]
        label1 = VAR_LABELS[var1]
        label2 = VAR_LABELS[var2]

        # Truth correlations
        if truth_col1 in df.columns and truth_col2 in df.columns:
            mask = df[truth_col1].notna() & df[truth_col2].notna()
            title = f"Truth {label1} vs {label2}"
            annotation = f"Entries: {mask.sum():,}"

            save_2d_histogram(
                df[truth_col1].values, df[truth_col2].values,
                f"Truth {label1}", f"Truth {label2}", title,
                f"truth_{var1}_vs_{var2}.png",
                output_dir, annotation=annotation
            )

            if var1 == 'x':
                save_2d_histogram(
                    df[truth_col1].values, df[truth_col2].values,
                    f"Truth {label1}", f"Truth {label2}", f"{title} (Log x-axis)",
                    f"truth_logx_{var1}_vs_{var2}.png",
                    output_dir, annotation=annotation, x_scale='log'
                )

        # Reco correlations per method
        for method in reco_methods:
            reco_col1 = f"{method}_{var1}"
            reco_col2 = f"{method}_{var2}"

            if reco_col1 not in df.columns or reco_col2 not in df.columns:
                continue

            reco_label1 = f"Reco {label1} ({method})"
            reco_label2 = f"Reco {label2} ({method})"
            title = f"Reco {label1} vs {label2} ({method})"

            mask = df[reco_col1].notna() & df[reco_col2].notna()
            total_events = mask.sum()
            annotation = f"Entries: {total_events:,}"

            # Add agreement statistics for x-Q2 plots
            if {var1, var2} == {'x', 'q2'} and total_events > 0:
                df_agree = df[mask]
                for v in ['x', 'q2']:
                    truth_v = TRUTH_VAR_MAPPING[v]
                    reco_v = f"{method}_{v}"
                    if truth_v in df_agree.columns:
                        res = (df_agree[reco_v] - df_agree[truth_v]) / df_agree[truth_v]
                        agree_count = (abs(res) < AGREEMENT_THRESHOLD).sum()
                        pct = (agree_count / total_events) * 100
                        v_label = 'x' if v == 'x' else 'Q²'
                        annotation += f"\n{v_label} agree (±{AGREEMENT_THRESHOLD:.0%}): {pct:.1f}%"

            save_2d_histogram(
                df[reco_col1].values, df[reco_col2].values,
                reco_label1, reco_label2, title,
                f"reco_{var1}_vs_{var2}_{method}.png",
                output_dir, annotation=annotation
            )

            if var1 == 'x':
                save_2d_histogram(
                    df[reco_col1].values, df[reco_col2].values,
                    reco_label1, reco_label2, f"{title} (Log x-axis)",
                    f"reco_logx_{var1}_vs_{var2}_{method}.png",
                    output_dir, annotation=annotation, x_scale='log'
                )


def generate_resolution_plots(df: pd.DataFrame, reco_methods: list[str],
                               output_dir: str) -> None:
    """Generate resolution histograms (1D and 2D)."""
    print("\n--- Generating Resolution Plots ---")

    for var_key in KINEMATIC_VARS:
        truth_col = TRUTH_VAR_MAPPING[var_key]
        if truth_col not in df.columns:
            continue

        for method in reco_methods:
            reco_col = f"{method}_{var_key}"
            if reco_col not in df.columns:
                continue

            mask = (np.isfinite(df[truth_col]) &
                    np.isfinite(df[reco_col]) &
                    (df[truth_col] != 0))

            if not mask.any():
                continue

            truth_vals = df.loc[mask, truth_col]
            reco_vals = df.loc[mask, reco_col]
            resolution = (reco_vals - truth_vals) / truth_vals

            var_label = VAR_LABELS[var_key]
            truth_label = f"Truth {var_label}"
            reco_label = f"Reco {var_label}"
            res_label = f"({reco_label} - {truth_label}) / {truth_label}"

            # 1D resolution histogram
            save_1d_histogram(
                resolution.values, res_label, "Counts",
                f"{res_label} ({method})",
                f"{var_key}_resolution_hist_{method}.png",
                output_dir, plot_range=(-1, 1),
                annotation=f"Entries: {len(resolution):,}"
            )

            # 2D resolution vs truth
            save_2d_histogram(
                truth_vals.values, resolution.values,
                truth_label, res_label,
                f"Resolution vs Truth ({method})",
                f"{var_key}_res_vs_truth_{method}.png",
                output_dir, annotation=f"Entries: {len(resolution):,}"
            )

            if var_key == 'x':
                save_2d_histogram(
                    truth_vals.values, resolution.values,
                    truth_label, res_label,
                    f"Resolution vs Truth ({method}) (Log x-axis)",
                    f"{var_key}_res_vs_truth_logx_{method}.png",
                    output_dir, annotation=f"Entries: {len(resolution):,}",
                    x_scale='log'
                )


def generate_y_cut_plots(df: pd.DataFrame, reco_methods: list[str],
                          output_dir: str) -> None:
    """Generate resolution plots with y-cuts."""
    print("\n--- Generating Y-Cut Resolution Plots ---")

    y_regions = {
        'low_y': {'threshold': lambda y: y <= Y_CUT_THRESHOLD,
                  'label': f'y <= {Y_CUT_THRESHOLD}'},
        'high_y': {'threshold': lambda y: y > Y_CUT_THRESHOLD,
                   'label': f'y > {Y_CUT_THRESHOLD}'}
    }

    for method in reco_methods:
        reco_y_col = f"{method}_y"
        if reco_y_col not in df.columns:
            continue

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
                truth_col = TRUTH_VAR_MAPPING[var_key]
                reco_col = f"{method}_{var_key}"

                if truth_col not in df_region.columns or reco_col not in df_region.columns:
                    continue

                mask = (np.isfinite(df_region[truth_col]) &
                        np.isfinite(df_region[reco_col]) &
                        (df_region[truth_col] != 0))

                if not mask.any():
                    continue

                truth_vals = df_region.loc[mask, truth_col]
                reco_vals = df_region.loc[mask, reco_col]
                resolution = (reco_vals - truth_vals) / truth_vals

                var_label = VAR_LABELS[var_key]
                truth_label = f"Truth {var_label}"
                res_label = f"({var_label} Reco - Truth) / Truth"
                title = f"{var_label} Resolution vs Truth\n(Cut: {region_info['label']}, {method})"
                annotation = f"Entries: {len(resolution):,}"

                save_2d_histogram(
                    truth_vals.values, resolution.values,
                    truth_label, res_label, title,
                    f"res_vs_truth_{var_key}_{region_name}_{method}.png",
                    output_dir, annotation=annotation
                )

                if var_key == 'x':
                    save_2d_histogram(
                        truth_vals.values, resolution.values,
                        truth_label, res_label, f"{title}\n(Log x-axis)",
                        f"res_vs_truth_logx_{var_key}_{region_name}_{method}.png",
                        output_dir, annotation=annotation, x_scale='log'
                    )


def generate_limited_range_plots(df: pd.DataFrame, reco_methods: list[str],
                                  output_dir: str) -> None:
    """Generate plots with limited kinematic ranges."""
    print("\n--- Generating Limited Range Plots ---")

    range_limits = {'x': [0, 1], 'q2': [0, 600], 'y': [0, 1]}

    for var_key, limits in range_limits.items():
        truth_col = TRUTH_VAR_MAPPING[var_key]
        if truth_col not in df.columns:
            continue

        for method in reco_methods:
            reco_col = f"{method}_{var_key}"
            if reco_col not in df.columns:
                continue

            var_label = VAR_LABELS[var_key]
            truth_label = f"Truth {var_label}"
            reco_label = f"Reco {var_label} ({method})"
            title = f"{reco_label} vs {truth_label} [LIMITED RANGE]"

            mask = ((df[truth_col] >= limits[0]) & (df[truth_col] <= limits[1]) &
                    (df[reco_col] >= limits[0]) & (df[reco_col] <= limits[1]))
            annotation = f"Entries in Range: {mask.sum():,}"

            save_2d_histogram(
                df[truth_col].values, df[reco_col].values,
                truth_label, reco_label, title,
                f"limited_truth_vs_reco_{var_key}_{method}.png",
                output_dir, annotation=annotation,
                custom_range=[limits, limits]
            )


# =============================================================================
# Main Analysis Pipeline
# =============================================================================

def run_analysis(file_pairs: list[tuple[str, str]], output_dir: str) -> None:
    """Run full analysis pipeline."""
    print(f"\n{'='*60}")
    print(f"Running EIC Data Analysis")
    print(f"{'='*60}")

    os.makedirs(output_dir, exist_ok=True)

    # Load data
    print("\n--- Loading CSV Data ---")
    mc_df, reco_df = load_file_pairs(file_pairs)

    if mc_df.empty or reco_df.empty:
        print("Error: A required dataframe is empty.")
        return

    # Merge datasets
    merged_df = pd.merge(mc_df, reco_df, on='evt', how='inner')
    if merged_df.empty:
        print("Error: Merged DataFrame is empty.")
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
    generate_truth_vs_reco_plots(merged_df, reco_methods, output_dir)
    generate_correlation_plots(merged_df, reco_methods, output_dir)
    generate_resolution_plots(merged_df, reco_methods, output_dir)
    generate_y_cut_plots(merged_df, reco_methods, output_dir)
    generate_limited_range_plots(merged_df, reco_methods, output_dir)

    print(f"\nAnalysis complete. Plots saved to: {output_dir}")


# =============================================================================
# CLI Entry Point
# =============================================================================

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Analyze EIC data: generate comparison plots from CSV files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Provide both mc_dis and reco_dis files
    %(prog)s data.mc_dis.csv data.reco_dis.csv -o ./output

    # Files can be in different directories
    %(prog)s /truth/data.mc_dis.csv /reco/data.reco_dis.csv -o ./output

    # Use glob patterns (shell expansion)
    %(prog)s /data/*.csv -o ./analysis_output

Notes:
    - Files are paired by base name: foo.mc_dis.csv <-> foo.reco_dis.csv
    - Both mc_dis.csv and reco_dis.csv must be provided for each dataset
    - All plots are saved as PNG files in the output directory
        """
    )

    parser.add_argument(
        'input_files',
        nargs='+',
        metavar='FILE',
        help='Input CSV files (*mc_dis.csv and *reco_dis.csv). Paired by base name.'
    )

    parser.add_argument(
        '-o', '--output',
        required=True,
        metavar='DIR',
        help='Output directory for plot files'
    )

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()

    # Validate input files
    print("Validating input files...")
    try:
        file_pairs = validate_file_pairs(args.input_files)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(file_pairs)} valid file pair(s).")

    # Run analysis
    run_analysis(file_pairs, args.output)

    print("\n\nAll processing finished.")


if __name__ == "__main__":
    main()
