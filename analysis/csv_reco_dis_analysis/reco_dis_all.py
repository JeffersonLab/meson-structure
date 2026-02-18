#!/usr/bin/env python3
"""
Reco DIS CSV Analysis Script

Analyzes all columns of reco_dis.csv files and generates histograms for each column.

Usage:
    reco_dis_all.py file1.csv file2.csv -o output_directory

The script:
1. Loads one or more CSV files with unique event ID handling
2. Creates histograms for all numeric columns
3. Saves plots with zero-based prefix (01_, 02_, etc.)
"""

import argparse
import os
import sys

import hist
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for saving plots
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# =============================================================================
# Column Configuration - defines histogram parameters per column type
# =============================================================================

# Define histogram configurations for different column types
# Format: (bins, low, high, xlabel, use_log_x)
COLUMN_CONFIG = {
    # DIS kinematics - x (Bjorken x)
    'da_x': (100, 0, 1, r'$x_{Bj}$ (DA)', False),
    'esigma_x': (100, 0, 1, r'$x_{Bj}$ (E-Sigma)', False),
    'electron_x': (100, 0, 1, r'$x_{Bj}$ (Electron)', False),
    'jb_x': (100, 0, 1, r'$x_{Bj}$ (JB)', False),
    'ml_x': (100, 0, 1, r'$x_{Bj}$ (ML)', False),
    'sigma_x': (100, 0, 1, r'$x_{Bj}$ (Sigma)', False),
    'mc_x': (100, 0, 1, r'$x_{Bj}$ (MC Truth)', False),

    # DIS kinematics - Q2
    'da_q2': (100, 0, 1000, r'$Q^2$ [GeV$^2$] (DA)', False),
    'esigma_q2': (100, 0, 1000, r'$Q^2$ [GeV$^2$] (E-Sigma)', False),
    'electron_q2': (100, 0, 1000, r'$Q^2$ [GeV$^2$] (Electron)', False),
    'jb_q2': (100, 0, 1000, r'$Q^2$ [GeV$^2$] (JB)', False),
    'ml_q2': (100, 0, 1000, r'$Q^2$ [GeV$^2$] (ML)', False),
    'sigma_q2': (100, 0, 1000, r'$Q^2$ [GeV$^2$] (Sigma)', False),
    'mc_q2': (100, 0, 1000, r'$Q^2$ [GeV$^2$] (MC Truth)', False),

    # DIS kinematics - y (inelasticity)
    'da_y': (100, 0, 1, r'$y$ (DA)', False),
    'esigma_y': (100, 0, 1, r'$y$ (E-Sigma)', False),
    'electron_y': (100, 0, 1, r'$y$ (Electron)', False),
    'jb_y': (100, 0, 1, r'$y$ (JB)', False),
    'ml_y': (100, 0, 1, r'$y$ (ML)', False),
    'sigma_y': (100, 0, 1, r'$y$ (Sigma)', False),
    'mc_y': (100, 0, 1, r'$y$ (MC Truth)', False),

    # DIS kinematics - nu (energy transfer)
    'da_nu': (100, 0, 2000, r'$\nu$ [GeV] (DA)', False),
    'esigma_nu': (100, 0, 2000, r'$\nu$ [GeV] (E-Sigma)', False),
    'electron_nu': (100, 0, 2000, r'$\nu$ [GeV] (Electron)', False),
    'jb_nu': (100, 0, 2000, r'$\nu$ [GeV] (JB)', False),
    'ml_nu': (100, 0, 2000, r'$\nu$ [GeV] (ML)', False),
    'sigma_nu': (100, 0, 2000, r'$\nu$ [GeV] (Sigma)', False),
    'mc_nu': (100, 0, 2000, r'$\nu$ [GeV] (MC Truth)', False),

    # DIS kinematics - W (invariant mass)
    'da_w': (100, 0, 2000, r'$W$ [GeV] (DA)', False),
    'esigma_w': (100, 0, 2000, r'$W$ [GeV] (E-Sigma)', False),
    'electron_w': (100, 0, 2000, r'$W$ [GeV] (Electron)', False),
    'jb_w': (100, 0, 2000, r'$W$ [GeV] (JB)', False),
    'ml_w': (100, 0, 2000, r'$W$ [GeV] (ML)', False),
    'sigma_w': (100, 0, 2000, r'$W$ [GeV] (Sigma)', False),
    'mc_w': (100, 0, 2000, r'$W$ [GeV] (MC Truth)', False),

    # t-values (momentum transfer squared, typically negative)
    'mc_true_t': (100, -5, 0, r'$t$ [GeV$^2$] (MC True)', False),
    'mc_lam_tb_t': (100, -5, 0, r'$t$ [GeV$^2$] (MC $\Lambda$, True Beam)', False),
    'mc_lam_exp_t': (100, -50, 0, r'$t$ [GeV$^2$] (MC $\Lambda$, Exp Beam)', False),
    'ff_lam_tb_t': (100, -5, 0, r'$t$ [GeV$^2$] (FF $\Lambda$, True Beam)', False),
    'ff_lam_exp_t': (100, -50, 0, r'$t$ [GeV$^2$] (FF $\Lambda$, Exp Beam)', False),

    # Scattered electron
    'elec_id': (50, 0, 50, 'Electron ID', False),
    'elec_energy': (100, 0, 50, 'Electron Energy [GeV]', False),
    'elec_px': (100, -20, 20, 'Electron $p_x$ [GeV/c]', False),
    'elec_py': (100, -20, 20, 'Electron $p_y$ [GeV/c]', False),
    'elec_pz': (100, -20, 20, 'Electron $p_z$ [GeV/c]', False),
    'elec_ref_x': (100, -100, 100, 'Electron ref x [mm]', False),
    'elec_ref_y': (100, -100, 100, 'Electron ref y [mm]', False),
    'elec_ref_z': (100, -100, 100, 'Electron ref z [mm]', False),
    'elec_pid_goodness': (100, 0, 1, 'Electron PID Goodness', False),
    'elec_type': (10, 0, 10, 'Electron Type', False),
    'elec_n_clusters': (10, 0, 10, 'Electron N Clusters', False),
    'elec_n_tracks': (10, 0, 10, 'Electron N Tracks', False),
    'elec_n_particles': (10, 0, 10, 'Electron N Particles', False),
    'elec_n_particle_ids': (10, 0, 10, 'Electron N Particle IDs', False),

    # MC scattered electron momentum
    'mc_elec_px': (100, -20, 20, 'MC Electron $p_x$ [GeV/c]', False),
    'mc_elec_py': (100, -20, 20, 'MC Electron $p_y$ [GeV/c]', False),
    'mc_elec_pz': (100, -20, 20, 'MC Electron $p_z$ [GeV/c]', False),

    # MC Lambda momentum
    'mc_lam_px': (100, -20, 20, r'MC $\Lambda$ $p_x$ [GeV/c]', False),
    'mc_lam_py': (100, -20, 20, r'MC $\Lambda$ $p_y$ [GeV/c]', False),
    'mc_lam_pz': (100, 0, 150, r'MC $\Lambda$ $p_z$ [GeV/c]', False),

    # Far-forward Lambda momentum
    'ff_lam_px': (100, -20, 20, r'FF $\Lambda$ $p_x$ [GeV/c]', False),
    'ff_lam_py': (100, -20, 20, r'FF $\Lambda$ $p_y$ [GeV/c]', False),
    'ff_lam_pz': (100, 0, 150, r'FF $\Lambda$ $p_z$ [GeV/c]', False),

    # MC beam proton momentum
    'mc_beam_prot_px': (100, -5, 5, 'MC Beam Proton $p_x$ [GeV/c]', False),
    'mc_beam_prot_py': (100, -5, 5, 'MC Beam Proton $p_y$ [GeV/c]', False),
    'mc_beam_prot_pz': (100, 0, 300, 'MC Beam Proton $p_z$ [GeV/c]', False),

    # MC beam electron momentum
    'mc_beam_elec_px': (100, -1, 1, 'MC Beam Electron $p_x$ [GeV/c]', False),
    'mc_beam_elec_py': (100, -1, 1, 'MC Beam Electron $p_y$ [GeV/c]', False),
    'mc_beam_elec_pz': (100, -20, 0, 'MC Beam Electron $p_z$ [GeV/c]', False),
}


def get_default_config(column_name):
    """Get default histogram configuration for unknown columns."""
    return (100, None, None, column_name, False)


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


def load_multiple_csvs(file_list: list[str], key_column: str = 'evt') -> pd.DataFrame:
    """Load and concatenate multiple CSV files with unique event IDs."""
    dfs = []
    offset = 0

    for filepath in sorted(file_list):
        print(f"  Loading: {os.path.basename(filepath)}")
        df, offset = load_csv_with_unique_events(filepath, key_column, offset)
        if not df.empty:
            dfs.append(df)

    if not dfs:
        return pd.DataFrame()

    combined = pd.concat(dfs, ignore_index=True)
    print(f"  Total events loaded: {len(combined)}")
    return combined


# =============================================================================
# Histogram Creation
# =============================================================================

def create_histogram(column_name: str, data: np.ndarray) -> hist.Hist:
    """Create a histogram for the given column data."""
    # Get configuration
    if column_name in COLUMN_CONFIG:
        bins, low, high, label, use_log = COLUMN_CONFIG[column_name]
    else:
        bins, low, high, label, use_log = get_default_config(column_name)

    # If no range specified, compute from data
    if low is None or high is None:
        valid_data = data[np.isfinite(data)]
        if len(valid_data) == 0:
            return None
        low = np.percentile(valid_data, 1)
        high = np.percentile(valid_data, 99)
        if low == high:
            low = low - 1
            high = high + 1

    # Create histogram
    h = hist.Hist(hist.axis.Regular(bins, low, high, name=column_name, label=label))
    return h


def fill_histogram(h: hist.Hist, data: np.ndarray) -> int:
    """Fill histogram with data, return count of valid entries."""
    valid_data = data[np.isfinite(data)]
    if len(valid_data) > 0:
        h.fill(valid_data)
    return len(valid_data)


# =============================================================================
# Plotting
# =============================================================================

def plot_histogram(h: hist.Hist, column_name: str, n_entries: int,
                   output_dir: str, prefix: str) -> str:
    """Create and save a histogram plot."""
    # Get configuration for label
    if column_name in COLUMN_CONFIG:
        _, _, _, label, _ = COLUMN_CONFIG[column_name]
    else:
        label = column_name

    fig, ax = plt.subplots(figsize=(10, 6))
    h.plot(ax=ax, color='steelblue', alpha=0.7, histtype='fill')

    ax.set_xlabel(label)
    ax.set_ylabel('Counts')
    ax.set_title(f'{label}')
    ax.grid(True, alpha=0.3)

    # Add statistics box
    stats_text = f'Entries: {n_entries:,}'
    if n_entries > 0:
        # Get histogram data for statistics
        values = h.values()
        edges = h.axes[0].edges
        centers = (edges[:-1] + edges[1:]) / 2
        if np.sum(values) > 0:
            mean = np.average(centers, weights=values)
            variance = np.average((centers - mean)**2, weights=values)
            std = np.sqrt(variance)
            stats_text += f'\nMean: {mean:.4g}\nStd: {std:.4g}'

    ax.text(0.95, 0.95, stats_text, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

    plt.tight_layout()

    # Save plot
    filename = f'{prefix}_{column_name}.png'
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=150)
    plt.close()

    return filepath


# =============================================================================
# Main Analysis
# =============================================================================

def run_analysis(input_files: list[str], output_dir: str) -> None:
    """Run the full analysis pipeline."""
    print(f"\n{'='*60}/n Reco DIS CSV Analysis /n{'='*60}")

    os.makedirs(output_dir, exist_ok=True)

    # Load data
    print("\n--- Loading CSV Data ---")
    df = load_multiple_csvs(input_files)

    if df.empty:
        print("Error: No data loaded.")
        return

    # Get all numeric columns (excluding event ID)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if 'evt' in numeric_cols:
        numeric_cols.remove('evt')

    print(f"\n--- Processing {len(numeric_cols)} columns ---")

    # Process each column
    plot_index = 1
    skipped = []

    for col in numeric_cols:
        data = df[col].values

        # Count valid entries
        n_valid = np.sum(np.isfinite(data))
        if n_valid < 10:
            skipped.append((col, n_valid))
            continue

        # Create histogram
        h = create_histogram(col, data)
        if h is None:
            skipped.append((col, 0))
            continue

        # Fill histogram
        n_entries = fill_histogram(h, data)

        # Create prefix with zero padding
        prefix = f'{plot_index:02d}'

        # Plot and save
        filepath = plot_histogram(h, col, n_entries, output_dir, prefix)
        print(f"  [{prefix}] {col}: {n_entries:,} entries -> {os.path.basename(filepath)}")

        plot_index += 1

    # Report skipped columns
    if skipped:
        print(f"\n--- Skipped {len(skipped)} columns (insufficient data) ---")
        for col, n in skipped:
            print(f"  {col}: {n} valid entries")

    print(f"\n{'='*60}")
    print(f"Analysis complete. {plot_index - 1} plots saved to: {output_dir}")
    print(f"{'='*60}")


# =============================================================================
# CLI Entry Point
# =============================================================================
def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze reco_dis CSV files and generate histograms for all columns.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
    Examples:
        # Single file
        %(prog)s data.reco_dis.csv -o ./plots

        # Multiple files (event IDs are made unique automatically)
        %(prog)s file1.reco_dis.csv file2.reco_dis.csv -o ./plots

        # Use glob patterns (shell expansion)
        %(prog)s /data/*.reco_dis.csv -o ./analysis_output

    Notes:
        - All numeric columns are automatically analyzed
        - Columns with fewer than 10 valid entries are skipped
        - Output files are prefixed with numbers (01_, 02_, etc.)
            """
    )

    parser.add_argument(
        'input_files',
        nargs='+',
        metavar='FILE',
        help='Input CSV files (*.reco_dis.csv)'
    )

    parser.add_argument(
        '-o', '--output',
        required=True,
        metavar='DIR',
        help='Output directory for plot files'
    )


    args = parser.parse_args()

    # Validate input files exist
    for f in args.input_files:
        if not os.path.exists(f):
            print(f"Error: File not found: {f}", file=sys.stderr)
            sys.exit(1)

    # Run analysis
    run_analysis(args.input_files, args.output)


if __name__ == "__main__":
    main()
