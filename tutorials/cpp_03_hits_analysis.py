#!/usr/bin/env python3
"""
Plot tracker hits from CSV file.

Usage:
    python plot_tracker_hits.py <csv_file> <event_number> [-o output_file]

Example:
    python plot_tracker_hits.py acceptance_ppim_trk_hits.csv 0 -o event_0_hits.png
"""

import argparse
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def create_time_vs_z_plot(df: pd.DataFrame, event_num: int, output_file: str):
    """
    Create a scatter plot of trk_hit_time vs trk_hit_pos_z.

    Parameters:
        df: DataFrame with tracker hit data
        event_num: Event number to plot
        output_file: Output file path for the plot
    """
    # Filter data for the specified event
    event_df = df[df['evt'] == event_num].copy()

    if event_df.empty:
        print(f"Error: No data found for event {event_num}")
        print(f"Available events: {sorted(df['evt'].unique())[:20]}...")
        sys.exit(1)

    print(f"Event {event_num}: {len(event_df)} hits")

    # Get unique prt_status values
    status_values = sorted(event_df['prt_status'].unique())
    print(f"prt_status values found: {status_values}")

    # Define color map - status 1 must be red
    # Use a qualitative colormap for other statuses
    base_colors = list(mcolors.TABLEAU_COLORS.values())
    color_map = {}

    color_idx = 0
    for status in status_values:
        if status == 1:
            color_map[status] = 'red'
        else:
            # Skip red-like colors for other statuses
            while color_idx < len(base_colors) and base_colors[color_idx] in ['#d62728', 'red']:
                color_idx += 1
            if color_idx < len(base_colors):
                color_map[status] = base_colors[color_idx]
                color_idx += 1
            else:
                # Fallback to generating colors
                color_map[status] = plt.cm.tab20(len(color_map) / 20)

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot each status group
    for status in status_values:
        status_df = event_df[event_df['prt_status'] == status]
        ax.scatter(
            status_df['trk_hit_time'],
            status_df['trk_hit_pos_z'],
            c=color_map[status],
            label=f'prt_status={status} ({len(status_df)} hits)',
            alpha=0.7,
            s=20,
            edgecolors='none'
        )

    # Configure axes
    ax.set_xlim(0, 2000)
    ax.set_xlabel('t (ns)', fontsize=12)
    ax.set_ylabel('z position (mm)', fontsize=12)
    ax.set_title(f'Tracker Hits: Time vs Z Position (Event {event_num})', fontsize=14)

    # Add grid
    ax.grid(True, linestyle='--', alpha=0.5)

    # Add legend
    ax.legend(loc='best', fontsize=10)

    # Tight layout
    plt.tight_layout()

    # Save figure
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Plot saved to: {output_file}")

    # Also save a version with full time range for reference
    full_range_file = output_file.rsplit('.', 1)
    if len(full_range_file) == 2:
        full_range_file = f"{full_range_file[0]}_full_range.{full_range_file[1]}"
    else:
        full_range_file = f"{output_file}_full_range"

    ax.set_xlim(event_df['trk_hit_time'].min() - 10, event_df['trk_hit_time'].max() + 10)
    ax.set_title(f'Tracker Hits: Time vs Z Position (Event {event_num}) - Full Range', fontsize=14)
    plt.savefig(full_range_file, dpi=150, bbox_inches='tight')
    print(f"Full range plot saved to: {full_range_file}")

    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description='Plot tracker hits from CSV file.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('csv_file', help='Input CSV file with tracker hits')
    parser.add_argument('event', type=int, help='Event number to plot')
    parser.add_argument('-o', '--output', default=None,
                        help='Output file name (default: event_<N>_time_vs_z.png)')

    args = parser.parse_args()

    # Set default output filename
    if args.output is None:
        args.output = f"event_{args.event}_time_vs_z.png"

    # Read CSV file
    print(f"Reading {args.csv_file}...")
    try:
        df = pd.read_csv(args.csv_file)
    except FileNotFoundError:
        print(f"Error: File not found: {args.csv_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    print(f"Loaded {len(df)} rows, {df['evt'].nunique()} unique events")

    # Create plot
    create_time_vs_z_plot(df, args.event, args.output)


if __name__ == '__main__':
    main()