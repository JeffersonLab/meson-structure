"""Lambda particle decay analysis and visualization.

This module provides functions for analyzing Lambda particle decays,
including primary vs secondary lambdas, decay modes, and trajectories.
"""
import argparse
import os
import json
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LogNorm
from aa_helpers import create_plot_with_background

# Global variable to store statistics and output directory
STATS_COLLECTOR = {}
OUTPUT_DIR = None

def convert_to_json_serializable(obj):
    """Convert numpy/pandas types to JSON-serializable Python types.

    Args:
        obj: Object to convert (can be dict, list, or scalar)

    Returns:
        JSON-serializable version of the object
    """
    if isinstance(obj, dict):
        return {key: convert_to_json_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_json_serializable(item) for item in obj]
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return convert_to_json_serializable(obj.tolist())
    else:
        return obj



# ============================================================================
# Data Filtering
# ============================================================================

def filter_decay_modes(df):
    """Filter dataframe into different decay modes.
    
    Args:
        df: Input dataframe
        
    Returns:
        dict: Dictionary containing filtered dataframes
    """
    df_primary = df[df['lam_is_first'] == 1]
    df_secondary = df[df['lam_is_first'] == 0]
    
    # Undecayed lambdas (no proton or neutron)
    df_not_decayed = df[
        (df['lam_is_first'] == 1) &
        (df['prot_id'].isna() & df['neut_id'].isna())
    ]
    
    # Proton + pi- decays
    df_ppim = df_primary[
        df_primary['prot_id'].notna() &
        df_primary['pimin_id'].notna() &
        df_primary['neut_id'].isna() &
        df_primary['pizero_id'].isna()
    ].copy()
    
    # Neutron + pi0 -> gamma gamma decays
    df_npzero = df_primary[
        df_primary['prot_id'].isna() &
        df_primary['pimin_id'].isna() &
        df_primary['neut_id'].notna() &
        df_primary['pizero_id'].notna() &
        df_primary['gamtwo_id'].notna() &
        df_primary['gamone_id'].notna()
    ].copy()
    
    return df_primary, df_secondary, df_not_decayed, df_ppim, df_npzero



# ============================================================================
# Statistics Functions
# ============================================================================

def calculate_percentage(df_all, condition_mask):
    """Calculate percentage of events matching condition.
    
    Args:
        df_all: Full dataframe
        condition_mask: Boolean mask for condition
        
    Returns:
        float: Percentage value
    """
    total = len(df_all)
    if total == 0:
        return 0.0
    percentage = (condition_mask.sum() / total) * 100
    return percentage


def print_decay_statistics(df, title="NO TITLE"):
    """Calculate and print decay statistics.
    
    Args:
        df: Input dataframe
    """
    total = len(df)
    if total == 0:
        print("No data available")
        STATS_COLLECTOR[title] = {"error": "No data available"}
        return

    proton_only =  df['prot_id'].notna() & df['neut_id'].isna()
    neutron_only = df['prot_id'].isna()  & df['neut_id'].notna()
    not_decayed =  df['prot_id'].isna()  & df['neut_id'].isna()
    what =         df['prot_id'].notna() & df['neut_id'].notna()

    p_proton = (proton_only.sum() / total) * 100
    p_neutron = (neutron_only.sum() / total) * 100
    p_not_decayed = (not_decayed.sum() / total) * 100
    p_crap = (what.sum() / total) * 100

    stats = {
        "total_events": int(total),
        "decayed_to_proton_percent": round(float(p_proton), 1),
        "decayed_to_neutron_percent": round(float(p_neutron), 1),
        "not_decayed_percent": round(float(p_not_decayed), 1),
        "both_proton_and_neutron_percent": round(float(p_crap), 1),
        "total_percent": round(float(p_proton + p_neutron + p_not_decayed + p_crap), 1)
    }
    STATS_COLLECTOR[title] = stats

    print()
    print(f"=== {title} ===")
    print(f"Total events:       {total}")
    print(f"Decayed to proton:  {p_proton:.1f}%")
    print(f"Decayed to neutron: {p_neutron:.1f}%")
    print(f"Not decayed:        {p_not_decayed:.1f}%")
    print(f" WHAT?:        {p_crap:.1f}%")
    print(f"total:        {p_proton+p_neutron+p_not_decayed+p_crap:.1f}%")


def analyze_primary_vs_secondary_lambdas(df):
    """Analyze and print primary vs secondary lambda statistics.
    
    Args:
        df: Input dataframe
    """
    secondary_events = calculate_percentage(df, df['lam_is_first'] == 0)
    total_events = df['event'].nunique()
    events_with_secondary = df[df['lam_is_first'] == 0]['event'].nunique()
    total_secondary_lambdas = (df['lam_is_first'] == 0).sum()
    
    stats = {
        "total_events": int(total_events),
        "events_with_secondary": int(events_with_secondary),
        "secondary_events_percent": round(float(secondary_events), 1),
        "total_secondary_lambda_particles": int(total_secondary_lambdas)
    }

    if events_with_secondary > 0:
        avg_lambdas = total_secondary_lambdas / events_with_secondary
        stats["average_secondary_lambdas_per_event"] = round(float(avg_lambdas), 2)
    else:
        stats["average_secondary_lambdas_per_event"] = 0

    STATS_COLLECTOR["Primary vs Secondary Lambda Analysis"] = stats

    print("=== Primary vs Secondary Lambda Analysis ===")
    print(f"Total events: {total_events}")
    print(f"Events with secondary lambdas: {events_with_secondary} "
          f"({secondary_events:.1f}%)")
    print(f"Total secondary lambda particles: {total_secondary_lambdas}")

    if events_with_secondary > 0:
        print(f"Average secondary lambdas per event: {avg_lambdas:.2f}")
    else:
        print("No secondary lambdas")


# ============================================================================
# Basic Plotting Functions
# ============================================================================

def plot_point(x_axis, y_axis, xlabel="z [mm]", ylabel="y [mm]", filename=None):
    """Create scatter plot of points.

    Args:
        x_axis: X coordinates
        y_axis: Y coordinates
        xlabel: X-axis label
        ylabel: Y-axis label
        filename: Optional filename to save plot
    """
    fig, ax = create_plot_with_background()
    ax.plot(x_axis, y_axis, marker="o", linestyle="none", alpha=0.3)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True)

    plt.tight_layout()

    if OUTPUT_DIR and filename:
        filepath = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plt_hist2d(x_axis, y_axis, bins=50, bin_size=None,
               xlabel="z [mm]", ylabel="y [mm]", title="Title is missing", filename=None):
    """Create 2D histogram with background.

    Args:
        x_axis: X coordinates
        y_axis: Y coordinates
        bins: Number of bins or [x_bins, y_bins]
        bin_size: Size of bins in mm (overrides bins parameter)
        xlabel: X-axis label
        ylabel: Y-axis label
        title: Plot title
        filename: Optional filename to save plot
    """
    fig, ax = create_plot_with_background()

    original_xlim = ax.get_xlim()
    original_ylim = ax.get_ylim()

    if bin_size is not None:
        x_range = original_xlim[1] - original_xlim[0]
        y_range = original_ylim[1] - original_ylim[0]

        x_bins = max(1, int(x_range / bin_size))
        y_bins = max(1, int(y_range / bin_size))
        bins = [x_bins, y_bins]

        print(f"Bin size: {bin_size}×{bin_size} mm")
        print(f"Number of bins: {x_bins}×{y_bins}")

    h = ax.hist2d(x_axis, y_axis, bins=bins,
                  cmap='viridis', norm=LogNorm())

    ax.set_xlim(original_xlim)
    ax.set_ylim(original_ylim)

    fig.colorbar(h[3], ax=ax, label='Counts', shrink=0.3)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True)
    ax.set_title(title)

    plt.tight_layout()

    if OUTPUT_DIR and filename:
        filepath = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


# ============================================================================
# Specialized Plotting Functions
# ============================================================================

def plot_primary_lambda_decay_z_distribution(df_primary, filename=None):
    """Plot Z coordinate distribution of primary lambda decays.

    Args:
        df_primary: Dataframe with primary lambdas
        filename: Optional filename to save plot
    """
    plt.figure(figsize=(12, 6))
    plt.hist(df_primary['lam_epz'], bins=80, alpha=0.7, edgecolor='black')
    plt.xlabel('Z decay vertex coordinate of Λ⁰ (mm)')
    plt.ylabel('Number of events')
    plt.title('Distribution of Z decay vertex coordinate for primary Λ⁰')
    plt.grid(True, alpha=0.3)

    plt.xlim(0, 45000)
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(5000))
    plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(1000))

    plt.grid(True, which='major', alpha=0.3)
    plt.grid(True, which='minor', alpha=0.1)

    plt.tight_layout()

    if OUTPUT_DIR and filename:
        filepath = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_decay_trajectories(p_pi_minus_decays, filename=None):
    """Plot Lambda -> proton + pi- decay trajectories.

    Args:
        p_pi_minus_decays: Dataframe with proton+pion decays
        filename: Optional filename to save plot
    """
    sample_df = p_pi_minus_decays.iloc[50:200].head(3)
    
    # Lambda trajectory
    lam_start_z = sample_df['lam_vz'].values
    lam_start_x = sample_df['lam_vx'].values
    lam_end_z = sample_df['lam_epz'].values
    lam_end_x = sample_df['lam_epx'].values
    
    # Proton trajectory
    prot_start_z = sample_df['lam_epz'].values
    prot_start_x = sample_df['lam_epx'].values
    prot_end_z = sample_df['prot_epz'].values
    prot_end_x = sample_df['prot_epx'].values
    
    # Pi- trajectory
    pimin_start_z = sample_df['lam_epz'].values
    pimin_start_x = sample_df['lam_epx'].values
    pimin_end_z = sample_df['pimin_epz'].values
    pimin_end_x = sample_df['pimin_epx'].values
    
    # Create line segments
    lam_segments = np.array([
        [[lam_start_z[i], lam_start_x[i]], [lam_end_z[i], lam_end_x[i]]]
        for i in range(len(sample_df))
    ])
    prot_segments = np.array([
        [[prot_start_z[i], prot_start_x[i]], [prot_end_z[i], prot_end_x[i]]]
        for i in range(len(sample_df))
    ])
    pimin_segments = np.array([
        [[pimin_start_z[i], pimin_start_x[i]],
         [pimin_end_z[i], pimin_end_x[i]]]
        for i in range(len(sample_df))
    ])
    
    fig, ax = create_plot_with_background(
        bck_image="eic_center_forward_bw.png"
    )
    
    # Add trajectories
    lam_lines = LineCollection(
        lam_segments, color='red', alpha=0.7, linewidths=2,
        label='Λ⁰ trajectory'
    )
    prot_lines = LineCollection(
        prot_segments, color='blue', alpha=0.7, linewidths=2,
        label='Proton trajectory'
    )
    pimin_lines = LineCollection(
        pimin_segments, color='lime', alpha=0.7, linewidths=2,
        label='π⁻ trajectory'
    )
    
    ax.add_collection(lam_lines)
    ax.add_collection(prot_lines)
    ax.add_collection(pimin_lines)
    
    # Add markers
    ax.scatter(lam_start_z, lam_start_x, color='darkred', s=50,
               marker='o', label='Λ⁰ birth', alpha=1)
    ax.scatter(lam_end_z, lam_end_x, color='red', s=50,
               marker='s', label='Λ⁰ decay', alpha=1)
    ax.scatter(prot_end_z, prot_end_x, color='blue', s=50,
               marker='^', label='Proton detection', alpha=1)
    ax.scatter(pimin_end_z, pimin_end_x, color='lime', s=50,
               marker='v', label='π⁻ detection', alpha=1)
    
    ax.set_xlabel("z [mm]")
    ax.set_ylabel("x [mm]")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_title("Λ⁰ → p + π⁻ decay trajectories")
    
    plt.tight_layout()

    if OUTPUT_DIR and filename:
        filepath = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_neutron_pizero_decay_trajectories(n_pi_zero_decays, filename=None):
    """Plot neutron + pi0 decay trajectories.
    
    Args:
        n_pi_zero_decays: Dataframe with neutron+pizero decays
    """
    sample_df = n_pi_zero_decays.iloc[34:200].head(1)
    
    # Lambda trajectory
    lam_start_z = sample_df['lam_vz'].values
    lam_start_x = sample_df['lam_vx'].values
    lam_end_z = sample_df['lam_epz'].values
    lam_end_x = sample_df['lam_epx'].values

    # Neutron trajectory
    neut_start_z = sample_df['lam_epz'].values
    neut_start_x = sample_df['lam_epx'].values
    neut_end_z = sample_df['neut_epz'].values
    neut_end_x = sample_df['neut_epx'].values

    # Pi0 trajectory
    pizero_start_z = sample_df['lam_epz'].values
    pizero_start_x = sample_df['lam_epx'].values
    pizero_end_z = sample_df['pizero_epz'].values
    pizero_end_x = sample_df['pizero_epx'].values

    # Create line segments
    lam_segments = np.array([
        [[lam_start_z[i], lam_start_x[i]], [lam_end_z[i], lam_end_x[i]]]
        for i in range(len(sample_df))
    ])
    neut_segments = np.array([
        [[neut_start_z[i], neut_start_x[i]],
         [neut_end_z[i], neut_end_x[i]]]
        for i in range(len(sample_df))
    ])
    pizero_segments = np.array([
        [[pizero_start_z[i], pizero_start_x[i]],
         [pizero_end_z[i], pizero_end_x[i]]]
        for i in range(len(sample_df))
    ])

    fig, ax = create_plot_with_background(
        bck_image="eic_center_forward_bw.png"
    )
    
    # Add trajectories
    lam_lines = LineCollection(
        lam_segments, color='red', alpha=0.7, linewidths=2,
        label='Λ⁰ trajectory'
    )
    neut_lines = LineCollection(
        neut_segments, color='blue', alpha=0.7, linewidths=2,
        label='Neutron trajectory'
    )
    pizero_lines = LineCollection(
        pizero_segments, color='lime', alpha=0.7, linewidths=2,
        label='π⁰ trajectory'
    )

    ax.add_collection(lam_lines)
    ax.add_collection(neut_lines)
    ax.add_collection(pizero_lines)

    # Add markers
    ax.scatter(lam_start_z, lam_start_x, color='darkred', s=50,
               marker='o', label='Λ⁰ birth', alpha=1)
    ax.scatter(lam_end_z, lam_end_x, color='red', s=50,
               marker='s', label='Λ⁰ decay', alpha=1)
    ax.scatter(neut_end_z, neut_end_x, color='blue', s=50,
               marker='^', label='Neutron detection', alpha=1)
    ax.scatter(pizero_end_z, pizero_end_x, color='lime', s=50,
               marker='v', label='π⁰ detection', alpha=1)

    ax.set_xlabel("z [mm]")
    ax.set_ylabel("x [mm]")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_title("Neutron + π⁰ decay trajectories")

    plt.tight_layout()

    if OUTPUT_DIR and filename:
        filepath = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_undecayed_primary_lambdas(df, df_not_decayed):
    """Plot undecayed primary lambdas if they exist.
    
    Args:
        df: Full dataframe
        df_not_decayed: Dataframe with undecayed lambdas
    """
    undecayed_primary_percentage = calculate_percentage(
        df, df_not_decayed.index.isin(df.index)
    )

    STATS_COLLECTOR["Undecayed Primary Lambdas"] = {
        "undecayed_primary_lambdas_percent": round(undecayed_primary_percentage, 1)
    }

    print(f"Undecayed primary lambdas: {undecayed_primary_percentage:.1f}%")

    # Fixed logic: plot only if there ARE undecayed lambdas
    if undecayed_primary_percentage > 0:
        plot_point(df_not_decayed['lam_epz'], df_not_decayed['lam_epx'], 
                   filename="undecayed_primary_lambdas.png")


def plot_primary_vs_secondary_decay_points(df_primary, df_secondary, filename=None):
    """Plot primary vs secondary lambda decay points.

    Args:
        df_primary: Primary lambdas dataframe
        df_secondary: Secondary lambdas dataframe
        filename: Optional filename to save plot
    """
    fig, ax = create_plot_with_background()

    ax.scatter(df_primary['lam_epz'], df_primary['lam_epx'],
               color='red', marker="o", s=20, alpha=0.5,
               label='Primary Λ⁰')

    ax.scatter(df_secondary['lam_epz'], df_secondary['lam_epx'],
               color='blue', marker="s", s=20, alpha=0.5,
               label='Secondary Λ⁰')

    ax.set_xlabel("z [mm]")
    ax.set_ylabel("x [mm]")
    ax.set_title("Primary vs Secondary Λ⁰ decay points")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()

    if OUTPUT_DIR and filename:
        filepath = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_primary_vs_secondary_birth_points(df_primary, df_secondary, filename=None):
    """Plot primary vs secondary lambda birth points.

    Args:
        df_primary: Primary lambdas dataframe
        df_secondary: Secondary lambdas dataframe
        filename: Optional filename to save plot
    """
    fig, ax = create_plot_with_background()

    ax.scatter(df_secondary['lam_vz'], df_secondary['lam_vx'],
               color='blue', marker="s", s=20, alpha=0.5,
               label='Secondary Λ⁰')

    ax.scatter(df_primary['lam_vz'], df_primary['lam_vx'],
               color='red', marker="o", s=20, alpha=0.5,
               label='Primary Λ⁰')

    ax.set_xlabel("z [mm]")
    ax.set_ylabel("x [mm]")
    ax.set_title("Primary vs Secondary Λ⁰ birth points")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()

    if OUTPUT_DIR and filename:
        filepath = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


# ============================================================================
# Advanced Trajectory Analysis
# ============================================================================

def plot_particle_trajectory_histogram(
    particle_type, dataframe,
    start_x_col, start_z_col,
    end_x_col, end_z_col,
    grid_x_step=100, grid_z_step=100,
    min_trajectories=10, cmap='viridis',
    particle_name=None, filename=None
):
    """Create histogram of particle trajectories through detector.

    Args:
        particle_type: Type of particle
        dataframe: Dataframe containing particle data
        start_x_col: Column name for start X coordinate
        start_z_col: Column name for start Z coordinate
        end_x_col: Column name for end X coordinate
        end_z_col: Column name for end Z coordinate
        grid_x_step: Grid step size in X direction (mm)
        grid_z_step: Grid step size in Z direction (mm)
        min_trajectories: Minimum trajectories to display cell
        cmap: Colormap name
        particle_name: Display name for particle
        filename: Optional filename to save plot
        
    Returns:
        np.ndarray: Histogram grid
    """
    if particle_name is None:
        particle_name = particle_type
    
    fig, ax = create_plot_with_background()
    grid_z_min, grid_z_max = ax.get_xlim()
    grid_x_min, grid_x_max = ax.get_ylim()
    
    original_xticks = ax.get_xticks()
    original_yticks = ax.get_yticks()
    
    plt.close(fig)
    
    grid_x_bins = int((grid_x_max - grid_x_min) / grid_x_step)
    grid_z_bins = int((grid_z_max - grid_z_min) / grid_z_step)
    
    def get_grid_index(x, z):
        """Convert coordinates to grid indices."""
        x_idx = int((x - grid_x_min) / grid_x_step)
        z_idx = int((z - grid_z_min) / grid_z_step)
        x_idx = max(0, min(grid_x_bins - 1, x_idx))
        z_idx = max(0, min(grid_z_bins - 1, z_idx))
        return (x_idx, z_idx)
    
    def find_intersected_cells_bresenham(start, end):
        """Find grid cells intersected by line using Bresenham algorithm.
        
        Args:
            start: (x, z) start coordinates
            end: (x, z) end coordinates
            
        Returns:
            list: List of (x_idx, z_idx) cell indices
        """
        start_x, start_z = start
        end_x, end_z = end
        
        x0_idx, z0_idx = get_grid_index(start_x, start_z)
        x1_idx, z1_idx = get_grid_index(end_x, end_z)
        
        cells = []
        
        dx = abs(x1_idx - x0_idx)
        dy = abs(z1_idx - z0_idx)
        
        x, z = x0_idx, z0_idx
        
        x_step = 1 if x1_idx > x0_idx else -1
        z_step = 1 if z1_idx > z0_idx else -1
        
        if dx > dy:
            err = dx / 2.0
            while x != x1_idx:
                cells.append((x, z))
                err -= dy
                if err < 0:
                    z += z_step
                    err += dx
                x += x_step
        else:
            err = dy / 2.0
            while z != z1_idx:
                cells.append((x, z))
                err -= dx
                if err < 0:
                    x += x_step
                    err += dy
                z += z_step
        
        cells.append((x1_idx, z1_idx))
        return list(set(cells))
    
    # Initialize histogram grid
    grid_hist = np.zeros((grid_z_bins, grid_x_bins))
    
    # Process each particle trajectory
    for i in range(len(dataframe)):
        particle = dataframe.iloc[i]
        
        start_point = (particle[start_x_col], particle[start_z_col])
        end_point = (particle[end_x_col], particle[end_z_col])
        
        intersected_cells = find_intersected_cells_bresenham(
            start_point, end_point
        )
        
        for x_idx, z_idx in intersected_cells:
            grid_hist[z_idx, x_idx] += 1
    
    # Create plot
    fig, ax = create_plot_with_background()
    ax.grid(False)
    
    x_edges = np.linspace(grid_x_min, grid_x_max, grid_x_bins + 1)
    z_edges = np.linspace(grid_z_min, grid_z_max, grid_z_bins + 1)
    
    # Mask cells below threshold
    grid_hist_masked = np.where(
        grid_hist >= min_trajectories, grid_hist, np.nan
    )
    
    im = ax.pcolormesh(
        z_edges, x_edges, grid_hist_masked.T,
        cmap=cmap, alpha=0.8, shading='auto'
    )
    
    cbar = plt.colorbar(
        im, ax=ax,
        label=(f'Number of {particle_name} trajectories '
               f'(min {min_trajectories})'),
        shrink=0.6, aspect=20, pad=0.02
    )
    cbar.ax.tick_params(labelsize=8)
    
    ax.set_xlabel("z [mm]")
    ax.set_ylabel("x [mm]")
    ax.set_title(
        f"{particle_name.capitalize()} Trajectory Histogram\n"
        f"(Density of {particle_name} paths through detector)"
    )
    ax.set_aspect("equal", adjustable="box")
    
    ax.set_xticks(original_xticks)
    ax.set_yticks(original_yticks)
    
    ax.set_xticks(
        np.arange(grid_z_min, grid_z_max + grid_z_step, grid_z_step),
        minor=True
    )
    ax.set_yticks(
        np.arange(grid_x_min, grid_x_max + grid_x_step, grid_x_step),
        minor=True
    )
    ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.5, which='minor')
    ax.grid(True, alpha=0.4, linestyle='-', linewidth=1, which='major')
    
    plt.tight_layout()

    if OUTPUT_DIR and filename:
        filepath = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()
    
    return grid_hist


# ============================================================================
# Batch Plot Saving
# ============================================================================

def save_all_plots(decay_modes, output_dir="analysis_results"):
    """Save all analysis plots to directory.
    
    Args:
        decay_modes: Dictionary with filtered dataframes
        output_dir: Base output directory
        
    Returns:
        str: Path to results directory
    """
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = os.path.join(output_dir, f"analysis_{timestamp}")
    os.makedirs(results_dir, exist_ok=True)
    
    def save_plot(func, filename, *args, **kwargs):
        """Helper to save individual plots."""
        try:
            plt.switch_backend('Agg')
            func(*args, **kwargs)
            filepath = os.path.join(results_dir, filename)
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            print(f"✓ Saved: {filename}")
        except Exception as e:
            print(f"✗ Error saving {filename}: {e}")
        finally:
            plt.switch_backend('TkAgg')
    
    df_primary = decay_modes['primary']
    df_secondary = decay_modes['secondary']
    p_pi_minus = decay_modes['p_pi_minus']
    n_pi_zero = decay_modes['n_pi_zero']
    
    # Note: calculate_decayed_statistics prints but doesn't create plot
    # Skipping this in save_all_plots
    
    save_plot(
        plot_primary_vs_secondary_decay_points,
        "01_primary_vs_secondary_decay_points.png",
        df_primary, df_secondary
    )
    
    save_plot(
        plot_primary_vs_secondary_birth_points,
        "02_primary_vs_secondary_birth_points.png",
        df_primary, df_secondary
    )
    
    save_plot(
        plot_primary_lambda_decay_z_distribution,
        "03_primary_lambda_decay_z_distribution.png",
        df_primary
    )
    
    save_plot(
        lambda: plt_hist2d(
            df_primary['lam_epz'], df_primary['lam_epx'],
            title="Λ⁰ decay points distribution"
        ),
        "04_lambda_decay_points.png"
    )
    
    save_plot(
        lambda: plt_hist2d(
            p_pi_minus['lam_epz'], p_pi_minus['lam_epx'],
            title="Λ⁰ → p + π⁻ decay points"
        ),
        "05_proton_pion_decay_points.png"
    )
    
    save_plot(
        plot_decay_trajectories,
        "06_proton_pion_trajectories.png",
        p_pi_minus
    )
    
    save_plot(
        lambda: plt_hist2d(
            p_pi_minus['pimin_epz'], p_pi_minus['pimin_epx'],
            title="π⁻ end points"
        ),
        "07_pion_end_points.png"
    )
    
    save_plot(
        lambda: plt_hist2d(
            n_pi_zero['lam_epz'], n_pi_zero['lam_epx'],
            title="n + π⁰ decay points"
        ),
        "08_neutron_pizero_decay_points.png"
    )
    
    save_plot(
        plot_neutron_pizero_decay_trajectories,
        "09_neutron_pizero_trajectories.png",
        n_pi_zero
    )
    
    save_plot(
        lambda: plt_hist2d(
            n_pi_zero['pizero_epz'], n_pi_zero['pizero_epx'],
            title="π⁰ decay points"
        ),
        "10_pizero_decay_points.png"
    )
    
    save_plot(
        lambda: plt_hist2d(
            n_pi_zero['gamone_epz'], n_pi_zero['gamone_epx'],
            bins=150,
            title="Gamma end points"
        ),
        "11_gamma_end_points.png"
    )
    
    return results_dir


# ============================================================================
# Main Analysis Function
# ============================================================================

def main():
    """Main entry point for analysis."""
    global OUTPUT_DIR, STATS_COLLECTOR

    parser = argparse.ArgumentParser(description='Process feather tables out of mcpart_lambda.csv files')
    parser.add_argument('files', nargs='+', help='Input Feather file(s) to combine (wildcards supported)')
    parser.add_argument('-o', '--output', default='results', help='Output directory to save files')
    args = parser.parse_args()
    print("Arguments:")
    print(args.files)
    print(args.output)

    # Set up output directory
    OUTPUT_DIR = args.output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    STATS_COLLECTOR = {}

    # Load data
    print("Loading data...")
    df = pd.read_feather(args.files[0])
    print(f"Loaded {len(df)} events")
    
    # Filter decay modes
    print("\nFiltering decay modes...")
    df_primary, df_secondary, df_not_decayed, df_ppim, df_npzero = filter_decay_modes(df)
    
    # Print statistics
    print("\n" + "="*60)
    print("DECAY STATISTICS")
    print("="*60)
    print_decay_statistics(df, "All events")
    print_decay_statistics(df_primary, "Only primary")
    print_decay_statistics(df_secondary, "Only secondary")

    
    print("\n" + "="*60)
    print("PRIMARY VS SECONDARY")
    print("="*60)
    analyze_primary_vs_secondary_lambdas(df)
    
    plot_undecayed_primary_lambdas(df, df_not_decayed)
    
    # Visualization section
    print("\n" + "="*60)
    print("GENERATING PLOTS")
    print("="*60)
    

    # Primary vs Secondary comparisons
    plot_primary_vs_secondary_decay_points(df_primary, df_secondary, 
                                           filename="01_primary_vs_secondary_decay_points.png")
    plot_primary_vs_secondary_birth_points(df_primary, df_secondary,
                                           filename="02_primary_vs_secondary_birth_points.png")

    # Primary lambda analysis
    plot_primary_lambda_decay_z_distribution(df_primary,
                                             filename="03_primary_lambda_decay_z_distribution.png")

    plt_hist2d(
        df_primary['lam_epz'], df_primary['lam_epx'],
        bins=150,
        title="Λ⁰ decay points distribution",
        filename="04_lambda_decay_points.png"
    )

    # Proton + Pi- decay analysis
    plt_hist2d(
        df_ppim['lam_epz'], df_ppim['lam_epx'],
        bins=150,
        title="Λ⁰ → p + π⁻ decay points distribution",
        filename="05_proton_pion_decay_points.png"
    )

    plot_decay_trajectories(df_ppim, filename="06_proton_pion_trajectories.png")

    plt_hist2d(
        df_ppim['pimin_epz'], df_ppim['pimin_epx'],
        bins=150,
        title="π⁻ end points distribution",
        filename="07_pion_end_points.png"
    )

    # Trajectory histograms for proton + pion
    plot_particle_trajectory_histogram(
        particle_type='proton',
        dataframe=df_ppim,
        start_x_col='prot_vx', start_z_col='prot_vz',
        end_x_col='prot_epx', end_z_col='prot_epz',
        grid_x_step=100, grid_z_step=100,
        min_trajectories=10,
        cmap='viridis',
        filename="08_proton_trajectory_histogram.png"
    )

    plot_particle_trajectory_histogram(
        particle_type='pion',
        dataframe=df_ppim,
        start_x_col='pimin_vx', start_z_col='pimin_vz',
        end_x_col='pimin_epx', end_z_col='pimin_epz',
        grid_x_step=100, grid_z_step=100,
        min_trajectories=100,
        cmap='viridis',
        filename="09_pion_trajectory_histogram.png"
    )

    # 2D histogram of proton end points
    plt_hist2d(
        df_ppim['prot_epz'], df_ppim['prot_epx'],
        bins=150,
        title="Proton end points distribution",
        filename="10_proton_end_points.png"
    )

    # Neutron + Pi0 decay analysis
    print("\nNeutron + π⁰ decay analysis...")
    plt_hist2d(
        df_npzero['lam_epz'], df_npzero['lam_epx'],
        bins=150,
        title="n + π⁰ decay points distribution",
        filename="11_neutron_pizero_decay_points.png"
    )

    plot_neutron_pizero_decay_trajectories(df_npzero,
                                           filename="12_neutron_pizero_trajectories.png")

    plt_hist2d(
        df_npzero['pizero_epz'], df_npzero['pizero_epx'],
        bins=150,
        title="π⁰ decay points distribution",
        filename="13_pizero_decay_points.png"
    )

    # 2D histogram of gamma gamma end points
    plt_hist2d(
        df_npzero['gamone_epz'], df_npzero['gamone_epx'],
        bins=150,
        title="Gamma end points distribution",
        filename="14_gamma_end_points.png"
    )

    # 2D histogram of neutron end points
    plt_hist2d(
        df_npzero['neut_epz'], df_npzero['neut_epx'],
        bins=150,
        title="Neutron end points distribution",
        filename="15_neutron_end_points.png"
    )

    # Trajectory histograms for neutron 
    plot_particle_trajectory_histogram(
        particle_type='neut',
        dataframe=df_npzero,
        start_x_col='neut_vx', start_z_col='neut_vz',
        end_x_col='neut_epx', end_z_col='neut_epz',
        grid_x_step=100, grid_z_step=100,
        min_trajectories=10,
        cmap='viridis',
        filename="16_neutron_trajectory_histogram.png"
    )

    # Trajectory histograms for Pi0
    plot_particle_trajectory_histogram(
        particle_type='pizero',
        dataframe=df_npzero,
        start_x_col='pizero_vx', start_z_col='pizero_vz',
        end_x_col='pizero_epx', end_z_col='pizero_epz',
        grid_x_step=300, grid_z_step=300,
        min_trajectories=100,
        cmap='viridis',
        filename="17_pizero_trajectory_histogram.png"
    )

    # Save statistics to JSON
    stats_path = os.path.join(OUTPUT_DIR, "stats.json")
    with open(stats_path, 'w') as f:
        # Convert numpy/pandas types to native Python types for JSON serialization
        json_safe_stats = convert_to_json_serializable(STATS_COLLECTOR)
        json.dump(json_safe_stats, f, indent=2)
    print(f"\n✓ Statistics saved to: {stats_path}")
    print(f"✓ All plots saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
