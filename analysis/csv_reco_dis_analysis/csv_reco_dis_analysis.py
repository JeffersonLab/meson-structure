#!/usr/bin/env python3
"""
Analysis script for CSV files created by csv_reco_dis.cxx
Creates histograms for all columns and saves them in hist/boost-histogram JSON format
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import argparse
from pathlib import Path
import hist
from hist import Hist
import warnings
warnings.filterwarnings('ignore')


def concat_csvs_with_unique_events(files):
    """Load and concatenate CSV files with globally unique event IDs"""
    dfs = []
    offset = 0

    for file in files:
        print(f"Reading: {file}")
        # Handle both compressed and uncompressed files
        if str(file).endswith('.zip'):
            df = pd.read_csv(file, compression='zip')
        else:
            df = pd.read_csv(file)
        
        # Make event IDs globally unique
        df['evt'] = df['evt'] + offset
        offset = df['evt'].max() + 1
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


def determine_histogram_bins(data, column_name):
    """Determine appropriate binning for histogram based on data distribution"""
    # Remove NaN values
    clean_data = data[~np.isnan(data)]
    
    if len(clean_data) == 0:
        return 50, 0, 1
    
    # For event numbers
    if column_name == 'evt':
        return int(min(100, len(clean_data) / 100)), clean_data.min(), clean_data.max()
    
    # For integer-like columns
    if column_name.endswith('_id') or column_name.endswith('_type'):
        unique_vals = len(np.unique(clean_data))
        if unique_vals < 50:
            return unique_vals, clean_data.min() - 0.5, clean_data.max() + 0.5
    
    # For momentum and energy variables
    if any(x in column_name for x in ['_px', '_py', '_pz', '_energy', '_q2', '_w', '_nu', '_x', '_y', '_t']):
        # Use percentiles to handle outliers
        q01 = np.percentile(clean_data, 1)
        q99 = np.percentile(clean_data, 99)
        
        if column_name.endswith('_q2') or column_name.endswith('_w'):
            bins = 100
        elif column_name.endswith('_t'):
            bins = 80
        else:
            bins = 75
            
        return bins, q01, q99
    
    # Default binning
    q05 = np.percentile(clean_data, 5)
    q95 = np.percentile(clean_data, 95)
    return 50, q05, q95


def create_histogram(data, column_name, output_dir):
    """Create histogram using hist library and save plot + JSON"""
    # Remove NaN values
    clean_data = data[~np.isnan(data)]
    
    if len(clean_data) == 0:
        print(f"  Skipping {column_name}: all NaN values")
        return None
    
    # Determine binning
    n_bins, x_min, x_max = determine_histogram_bins(clean_data, column_name)
    
    # Handle edge case where min == max
    if x_min == x_max:
        x_min -= 0.5
        x_max += 0.5
    
    # Create histogram using hist library
    h = Hist(
        hist.axis.Regular(n_bins, x_min, x_max, name=column_name, label=column_name)
    )
    
    # Fill histogram
    h.fill(clean_data)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    h.plot(ax=ax)
    
    # Customize plot
    ax.set_xlabel(column_name)
    ax.set_ylabel('Counts')
    ax.set_title(f'Distribution of {column_name}')
    
    # Add statistics to plot
    stats_text = f'Entries: {len(clean_data)}\n'
    stats_text += f'Mean: {np.mean(clean_data):.3f}\n'
    stats_text += f'Std: {np.std(clean_data):.3f}'
    ax.text(0.7, 0.95, stats_text, transform=ax.transAxes, 
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Save plot
    plot_path = output_dir / f"{column_name}.png"
    plt.savefig(plot_path, dpi=100, bbox_inches='tight')
    plt.close()
    
    # Save histogram to JSON in hist format
    json_path = output_dir / f"{column_name}.json"
    
    # Create JSON representation compatible with hist/boost-histogram
    hist_json = {
        "axes": [{
            "class": "Regular",
            "bins": n_bins,
            "lower": float(x_min),
            "upper": float(x_max),
            "name": column_name,
            "label": column_name
        }],
        "storage": {
            "class": "Double",
            "values": h.values().tolist()
        },
        "metadata": {
            "column": column_name,
            "entries": int(len(clean_data)),
            "mean": float(np.mean(clean_data)),
            "std": float(np.std(clean_data)),
            "min": float(np.min(clean_data)),
            "max": float(np.max(clean_data))
        }
    }
    
    with open(json_path, 'w') as f:
        json.dump(hist_json, f, indent=2)
    
    return h


def create_2d_histogram(df, col1, col2, output_dir):
    """Create 2D histogram for correlation plots"""
    # Remove rows where either column has NaN
    mask = ~(df[col1].isna() | df[col2].isna())
    clean_data = df[mask]
    
    if len(clean_data) == 0:
        return None
    
    # Create 2D histogram
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Determine bins
    n_bins_1, x_min_1, x_max_1 = determine_histogram_bins(clean_data[col1].values, col1)
    n_bins_2, x_min_2, x_max_2 = determine_histogram_bins(clean_data[col2].values, col2)
    
    # Create the 2D histogram
    h, xedges, yedges, im = ax.hist2d(
        clean_data[col1], clean_data[col2],
        bins=[min(n_bins_1, 100), min(n_bins_2, 100)],
        range=[[x_min_1, x_max_1], [x_min_2, x_max_2]],
        cmap='viridis'
    )
    
    plt.colorbar(im, ax=ax)
    ax.set_xlabel(col1)
    ax.set_ylabel(col2)
    ax.set_title(f'{col1} vs {col2}')
    
    # Save plot
    plot_path = output_dir / f"{col1}_vs_{col2}.png"
    plt.savefig(plot_path, dpi=100, bbox_inches='tight')
    plt.close()


def main():
    parser = argparse.ArgumentParser(description='Analyze CSV files from csv_reco_dis.cxx')
    parser.add_argument('-o', '--outdir', type=str, default='histograms',
                        help='Directory where to save histogram plots and json files')
    parser.add_argument('-e', '--events', type=int, default=None,
                        help='Number of events to process (process all if not provided)')
    parser.add_argument('files', nargs='+', help='Input CSV files')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.outdir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories for different types of plots
    (output_dir / '1d_histograms').mkdir(exist_ok=True)
    (output_dir / '2d_correlations').mkdir(exist_ok=True)
    
    print("=" * 60)
    print("CSV Reco DIS Analysis")
    print("=" * 60)
    
    # Load and concatenate CSV files
    print("\nLoading CSV files...")
    df = concat_csvs_with_unique_events([Path(f) for f in args.files])
    
    # Limit events if requested
    if args.events is not None:
        print(f"Limiting to {args.events} events")
        df = df.head(args.events)
    
    print(f"Total events loaded: {len(df)}")
    print(f"Columns found: {len(df.columns)}")
    
    # Process each column
    print("\nCreating 1D histograms...")
    print("-" * 40)
    
    processed_columns = []
    for col in df.columns:
        print(f"Processing: {col}")
        h = create_histogram(df[col].values, col, output_dir / '1d_histograms')
        if h is not None:
            processed_columns.append(col)
    
    print(f"\nProcessed {len(processed_columns)} columns successfully")
    
    # Create some important 2D correlation plots
    print("\nCreating 2D correlation plots...")
    print("-" * 40)
    
    # Define interesting correlations to plot
    correlations = [
        # Compare reconstruction methods with MC truth
        ('mc_q2', 'da_q2'),
        ('mc_q2', 'electron_q2'),
        ('mc_q2', 'jb_q2'),
        ('mc_x', 'da_x'),
        ('mc_x', 'electron_x'),
        ('mc_y', 'da_y'),
        ('mc_y', 'electron_y'),
        ('mc_w', 'da_w'),
        # Lambda t-values
        ('mc_lam_tb_t', 'ff_lam_tb_t'),
        ('mc_lam_exp_t', 'ff_lam_exp_t'),
        # Electron momentum
        ('elec_px', 'mc_elec_px'),
        ('elec_py', 'mc_elec_py'),
        ('elec_pz', 'mc_elec_pz'),
        # Lambda momentum
        ('mc_lam_px', 'ff_lam_px'),
        ('mc_lam_py', 'ff_lam_py'),
        ('mc_lam_pz', 'ff_lam_pz'),
    ]
    
    for col1, col2 in correlations:
        if col1 in df.columns and col2 in df.columns:
            print(f"Creating: {col1} vs {col2}")
            create_2d_histogram(df, col1, col2, output_dir / '2d_correlations')
    
    # Create summary JSON with all column information
    summary = {
        "total_events": len(df),
        "columns": {},
        "missing_data": {}
    }
    
    for col in df.columns:
        col_data = df[col]
        n_valid = col_data.notna().sum()
        n_missing = col_data.isna().sum()
        
        if n_valid > 0:
            summary["columns"][col] = {
                "valid_entries": int(n_valid),
                "missing_entries": int(n_missing),
                "missing_fraction": float(n_missing / len(df)),
                "mean": float(col_data.mean()) if n_valid > 0 else None,
                "std": float(col_data.std()) if n_valid > 0 else None,
                "min": float(col_data.min()) if n_valid > 0 else None,
                "max": float(col_data.max()) if n_valid > 0 else None
            }
    
    summary_path = output_dir / "analysis_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print(f"Output directory: {output_dir}")
    print(f"  - 1D histograms: {output_dir / '1d_histograms'}")
    print(f"  - 2D correlations: {output_dir / '2d_correlations'}")
    print(f"  - Summary: {summary_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
