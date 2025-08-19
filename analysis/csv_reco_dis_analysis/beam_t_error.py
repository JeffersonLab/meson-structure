#!/usr/bin/env python3
"""
Script: beam_t_error.py

Analysis of beam angles and their correlation with t-value errors.
Creates histograms for beam proton angles, Lambda angles, and t-value correlations.

Usage:
    python beam_t_error.py --outdir output_dir file1.csv file2.csv
    python beam_t_error.py -e 10000 data/*.csv

Dependencies:
    pip install pandas numpy matplotlib hist mplhep
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import hist
from hist import Hist
from hist.axis import Regular as Axis

import json_fix
import json
import argparse
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

json.fallback_table[np.ndarray] = lambda array: array.tolist()

# Optional: Use HEP styling
try:
    import mplhep as hep
    plt.style.use(hep.style.ROOT)
except ImportError:
    print("Note: mplhep not installed, using default matplotlib style")


###############################################################################
# Constants
###############################################################################

# Particle masses in GeV
PROTON_MASS = 0.938272
LAMBDA_MASS = 1.115683
ELECTRON_MASS = 0.000511

# Crossing angles from AfterburnerConfig (same as in csv_reco_dis.cxx)
CROSSING_ANGLE_HOR = 25e-3    # 25 mrad in X
CROSSING_ANGLE_VER = 100e-6    # 100 microrad in Y


###############################################################################
# Helper Functions
###############################################################################

def create_lorentz_vector(px, py, pz, mass):
    """Create 4-momentum from 3-momentum and mass"""
    energy = np.sqrt(px**2 + py**2 + pz**2 + mass**2)
    return np.array([energy, px, py, pz])


def calculate_angle_between_vectors(v1, v2):
    """Calculate angle between two 3-vectors in radians"""
    # v1 and v2 should be shape (N, 3) or (3,)
    if len(v1.shape) == 1:
        v1 = v1.reshape(1, -1)
    if len(v2.shape) == 1:
        v2 = v2.reshape(1, -1)
    
    # Normalize vectors
    v1_norm = v1 / np.linalg.norm(v1, axis=1, keepdims=True)
    v2_norm = v2 / np.linalg.norm(v2, axis=1, keepdims=True)
    
    # Calculate angle
    cos_angle = np.sum(v1_norm * v2_norm, axis=1)
    # Clamp to avoid numerical errors
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    angle = np.arccos(cos_angle)
    
    return angle


def calculate_t(p1_vec4, p2_vec4):
    """Calculate Mandelstam t from two four-vectors
    t = (p1 - p2)^2 = (E1-E2)^2 - (p1-p2)^2
    """
    q_vec4 = p1_vec4 - p2_vec4
    # Four-vector inner product with metric (+,-,-,-)
    t = q_vec4[0]**2 - q_vec4[1]**2 - q_vec4[2]**2 - q_vec4[3]**2
    return t


def create_beam_vector_with_angle(momentum, angle_hor, angle_ver=100e-6):
    """Create a beam vector with specified crossing angles
    
    Args:
        momentum: magnitude of momentum in GeV
        angle_hor: horizontal crossing angle in radians
        angle_ver: vertical crossing angle in radians (default 100 μrad)
    
    Returns:
        3-vector of momentum
    """
    px = momentum * np.sin(angle_hor)
    py = momentum * np.sin(angle_ver) * np.cos(angle_hor)
    pz = momentum * np.cos(angle_hor) * np.cos(angle_ver)
    return np.array([px, py, pz])


def get_exp_beam_vector(true_beam_momentum, beam_mode=275.0):
    """
    Calculate the experimental beam vector with crossing angles.
    Mirrors the logic from csv_reco_dis.cxx calculate_approx_beam()
    
    Args:
        true_beam_momentum: magnitude of true beam momentum
        beam_mode: assumed beam momentum mode (41, 100, 130, or 275 GeV)
    
    Returns:
        3-vector of experimental beam momentum
    """
    # Apply crossing angles to get experimental beam
    px = beam_mode * np.sin(CROSSING_ANGLE_HOR)
    py = beam_mode * np.sin(CROSSING_ANGLE_VER) * np.cos(CROSSING_ANGLE_HOR)
    pz = beam_mode * np.cos(CROSSING_ANGLE_HOR) * np.cos(CROSSING_ANGLE_VER)
    
    return np.array([px, py, pz])


def detect_beam_mode(beam_pz):
    """Detect beam mode from proton pz"""
    beam_modes = [41.0, 100.0, 130.0, 275.0]
    beam_momentum = np.abs(beam_pz)  # Approximate, since pz dominates
    
    for mode in beam_modes:
        if np.abs(beam_momentum - mode) < 10:
            return mode
    
    # Default to 275 GeV if not detected
    return 275.0


###############################################################################
# Data Loading
###############################################################################

def concat_csvs_with_unique_events(files):
    """Load and concatenate CSV files with globally unique event IDs"""
    dfs = []
    offset = 0

    for file in files:
        print(f"  Reading: {file}")
        if str(file).endswith('.zip'):
            df = pd.read_csv(file, compression='zip')
        else:
            df = pd.read_csv(file)
        
        df['evt'] = df['evt'] + offset
        offset = df['evt'].max() + 1
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


###############################################################################
# Histogram Creation
###############################################################################

def create_histograms():
    """Create all histograms with predefined binning"""
    hists = {}
    
    # 1D Histograms for angles (in milliradians)
    
    # 1. Angle between beam proton and z axis
    hists['beam_z_angle'] = Hist(Axis(100, 0, 30, name="beam_z_angle", label=r"Angle(beam, z-axis) [mrad]"))
    
    # 2. Angle between beam proton and z axis - 0.25 mrad (should center around 0)
    hists['beam_z_angle_corrected'] = Hist(
        Axis(100, -5, 5, name="beam_z_angle_corrected", 
             label=r"Angle(beam, z-axis) - 25 mrad [mrad]")
    )
    
    # 3. Angle between experimental beam (rotated 275 GeV) and real MC beam
    hists['exp_mc_beam_angle'] = Hist(
        Axis(100, 0, 10, name="exp_mc_beam_angle", 
             label=r"Angle(exp beam, MC beam) [mrad]")
    )
    
    # 4. Angle between Lambda and z axis
    hists['lambda_z_angle'] = Hist(Axis(100, 0, 100, name="lambda_z_angle", label=r"Angle($\Lambda$, z-axis) [mrad]"))
    
    # 5. Angle between beam proton and Lambda
    hists['beam_lambda_angle'] = Hist(Axis(100, 0, 5, name="beam_lambda_angle", label=r"Angle(beam, $\Lambda$) [mrad]"))
    
    # New: Lambda pt and pz 1D histograms
    hists['lambda_pt'] = Hist(
        Axis(100, 0, 20, name="lambda_pt", label=r"$\Lambda$ $p_T$ [GeV]")
    )
    
    hists['lambda_pz'] = Hist(
        Axis(100, 0, 300, name="lambda_pz", label=r"$\Lambda$ $p_z$ [GeV]")
    )
    
    # 2D Histograms
    
    # 6. Difference in t-values vs angle between exp beam and MC beam
    # Y-axis: (mc_lam_exp_t - mc_true_t)
    # X-axis: angle between experimental beam and MC beam
    hists['t_diff_vs_exp_mc_angle'] = Hist(
        Axis(50, 0, 10, name="exp_mc_angle", 
             label=r"Angle(exp beam, MC beam) [mrad]"),
        Axis(50, -5, 5, name="t_diff", 
             label=r"$t_{\Lambda,exp} - t_{MC,true}$ [GeV$^2$]")
    )
    
    # Additional useful 2D histograms
    
    # 7. Lambda angle vs beam angle
    hists['lambda_angle_vs_beam_angle'] = Hist(
        Axis(50, 0, 30, name="beam_z_angle", 
             label=r"Angle(beam, z-axis) [mrad]"),
        Axis(50, 0, 100, name="lambda_z_angle", 
             label=r"Angle($\Lambda$, z-axis) [mrad]")
    )
    
    # 8. t difference vs Lambda angle
    hists['t_diff_vs_lambda_angle'] = Hist(
        Axis(50, 0, 100, name="lambda_z_angle", 
             label=r"Angle($\Lambda$, z-axis) [mrad]"),
        Axis(50, -5, 5, name="t_diff", 
             label=r"$t_{\Lambda,exp} - t_{MC,true}$ [GeV$^2$]")
    )
    
    # 9. New: t error vs beam error scatter plot
    # This will be a 2D histogram showing correlation between beam angle error and t error
    hists['t_error_vs_beam_error'] = Hist(
        Axis(50, -2, 2, name="beam_angle_error", 
             label=r"Beam angle error [mrad]"),
        Axis(50, -2, 2, name="t_error", 
             label=r"$t$ error [GeV$^2$]")
    )
    
    return hists


###############################################################################
# Calculate Angles and Fill Histograms
###############################################################################

def calculate_angles_and_fill(hists, df):
    """Calculate angles from momentum vectors and fill histograms"""
    
    print("\nCalculating angles and filling histograms...")
    
    # Clean data - remove rows with missing momentum components
    beam_mask = (df['mc_beam_prot_px'].notna() & 
                 df['mc_beam_prot_py'].notna() & 
                 df['mc_beam_prot_pz'].notna())
    
    lambda_mask = (df['mc_lam_px'].notna() & 
                   df['mc_lam_py'].notna() & 
                   df['mc_lam_pz'].notna())
    
    # Get beam proton momentum vectors
    beam_px = df.loc[beam_mask, 'mc_beam_prot_px'].values
    beam_py = df.loc[beam_mask, 'mc_beam_prot_py'].values
    beam_pz = df.loc[beam_mask, 'mc_beam_prot_pz'].values
    beam_vectors = np.column_stack([beam_px, beam_py, beam_pz])
    
    # Z-axis vector
    z_axis = np.array([0, 0, 1])
    
    # 1. Calculate angle between beam proton and z-axis
    if len(beam_vectors) > 0:
        beam_z_angles = calculate_angle_between_vectors(beam_vectors, z_axis)
        beam_z_angles_mrad = beam_z_angles * 1000  # Convert to milliradians
        hists['beam_z_angle'].fill(beam_z_angles_mrad)
        print(f"  Filled beam_z_angle: {len(beam_z_angles_mrad)} entries")
        
        # 2. Angle between beam and z-axis minus 25 mrad
        beam_z_angles_corrected = beam_z_angles_mrad - 25.0
        hists['beam_z_angle_corrected'].fill(beam_z_angles_corrected)
        print(f"  Filled beam_z_angle_corrected: {len(beam_z_angles_corrected)} entries")
    
    # 3. Angle between experimental beam and MC beam
    if len(beam_vectors) > 0:
        # Detect beam mode from average beam momentum
        avg_beam_pz = np.mean(np.abs(beam_pz))
        beam_mode = detect_beam_mode(avg_beam_pz)
        print(f"  Detected beam mode: {beam_mode} GeV")
        
        # Get experimental beam vector for each event
        exp_beam_angles = []
        for i in range(len(beam_vectors)):
            mc_beam = beam_vectors[i]
            exp_beam = get_exp_beam_vector(np.linalg.norm(mc_beam), beam_mode)
            angle = calculate_angle_between_vectors(mc_beam, exp_beam)[0]
            exp_beam_angles.append(angle * 1000)  # Convert to mrad
        
        exp_beam_angles = np.array(exp_beam_angles)
        hists['exp_mc_beam_angle'].fill(exp_beam_angles)
        print(f"  Filled exp_mc_beam_angle: {len(exp_beam_angles)} entries")
    
    # 4. Angle between Lambda and z-axis, plus pt and pz
    if lambda_mask.sum() > 0:
        lambda_px = df.loc[lambda_mask, 'mc_lam_px'].values
        lambda_py = df.loc[lambda_mask, 'mc_lam_py'].values
        lambda_pz = df.loc[lambda_mask, 'mc_lam_pz'].values
        lambda_vectors = np.column_stack([lambda_px, lambda_py, lambda_pz])
        
        # Calculate and fill Lambda z-angle
        lambda_z_angles = calculate_angle_between_vectors(lambda_vectors, z_axis)
        lambda_z_angles_mrad = lambda_z_angles * 1000  # Convert to milliradians
        hists['lambda_z_angle'].fill(lambda_z_angles_mrad)
        print(f"  Filled lambda_z_angle: {len(lambda_z_angles_mrad)} entries")
        
        # Calculate and fill Lambda pt
        lambda_pt = np.sqrt(lambda_px**2 + lambda_py**2)
        hists['lambda_pt'].fill(lambda_pt)
        print(f"  Filled lambda_pt: {len(lambda_pt)} entries")
        
        # Fill Lambda pz
        hists['lambda_pz'].fill(np.abs(lambda_pz))
        print(f"  Filled lambda_pz: {len(lambda_pz)} entries")
    
    # 5. Angle between beam proton and Lambda
    combined_mask = beam_mask & lambda_mask
    if combined_mask.sum() > 0:
        beam_px = df.loc[combined_mask, 'mc_beam_prot_px'].values
        beam_py = df.loc[combined_mask, 'mc_beam_prot_py'].values
        beam_pz = df.loc[combined_mask, 'mc_beam_prot_pz'].values
        beam_vectors = np.column_stack([beam_px, beam_py, beam_pz])
        
        lambda_px = df.loc[combined_mask, 'mc_lam_px'].values
        lambda_py = df.loc[combined_mask, 'mc_lam_py'].values
        lambda_pz = df.loc[combined_mask, 'mc_lam_pz'].values
        lambda_vectors = np.column_stack([lambda_px, lambda_py, lambda_pz])
        
        beam_lambda_angles = []
        for i in range(len(beam_vectors)):
            angle = calculate_angle_between_vectors(beam_vectors[i], lambda_vectors[i])[0]
            beam_lambda_angles.append(angle * 1000)  # Convert to mrad
        
        beam_lambda_angles = np.array(beam_lambda_angles)
        hists['beam_lambda_angle'].fill(beam_lambda_angles)
        print(f"  Filled beam_lambda_angle: {len(beam_lambda_angles)} entries")
    
    # 6. 2D: t difference vs experimental beam angle
    t_mask = (combined_mask & 
              df['mc_lam_exp_t'].notna() & 
              df['mc_true_t'].notna())
    
    if t_mask.sum() > 0:
        # Calculate t difference (note: t values are already negative in CSV)
        t_diff = df.loc[t_mask, 'mc_lam_exp_t'].values - df.loc[t_mask, 'mc_true_t'].values
        
        # Calculate experimental beam angles for these events
        beam_px = df.loc[t_mask, 'mc_beam_prot_px'].values
        beam_py = df.loc[t_mask, 'mc_beam_prot_py'].values
        beam_pz = df.loc[t_mask, 'mc_beam_prot_pz'].values
        beam_vectors = np.column_stack([beam_px, beam_py, beam_pz])
        
        exp_mc_angles = []
        for i in range(len(beam_vectors)):
            mc_beam = beam_vectors[i]
            exp_beam = get_exp_beam_vector(np.linalg.norm(mc_beam), beam_mode)
            angle = calculate_angle_between_vectors(mc_beam, exp_beam)[0]
            exp_mc_angles.append(angle * 1000)  # Convert to mrad
        
        hists['t_diff_vs_exp_mc_angle'].fill(
            exp_mc_angle=exp_mc_angles,
            t_diff=t_diff
        )
        print(f"  Filled t_diff_vs_exp_mc_angle: {len(t_diff)} entries")
    
    # 7. 2D: Lambda angle vs beam angle
    if combined_mask.sum() > 0:
        beam_px = df.loc[combined_mask, 'mc_beam_prot_px'].values
        beam_py = df.loc[combined_mask, 'mc_beam_prot_py'].values
        beam_pz = df.loc[combined_mask, 'mc_beam_prot_pz'].values
        beam_vectors = np.column_stack([beam_px, beam_py, beam_pz])
        
        lambda_px = df.loc[combined_mask, 'mc_lam_px'].values
        lambda_py = df.loc[combined_mask, 'mc_lam_py'].values
        lambda_pz = df.loc[combined_mask, 'mc_lam_pz'].values
        lambda_vectors = np.column_stack([lambda_px, lambda_py, lambda_pz])
        
        beam_z_angles = calculate_angle_between_vectors(beam_vectors, z_axis) * 1000
        lambda_z_angles = calculate_angle_between_vectors(lambda_vectors, z_axis) * 1000
        
        hists['lambda_angle_vs_beam_angle'].fill(
            beam_z_angle=beam_z_angles,
            lambda_z_angle=lambda_z_angles
        )
        print(f"  Filled lambda_angle_vs_beam_angle: {len(beam_z_angles)} entries")
    
    # 8. 2D: t difference vs Lambda angle
    if t_mask.sum() > 0:
        t_diff = df.loc[t_mask, 'mc_lam_exp_t'].values - df.loc[t_mask, 'mc_true_t'].values
        
        lambda_px = df.loc[t_mask, 'mc_lam_px'].values
        lambda_py = df.loc[t_mask, 'mc_lam_py'].values
        lambda_pz = df.loc[t_mask, 'mc_lam_pz'].values
        lambda_vectors = np.column_stack([lambda_px, lambda_py, lambda_pz])
        
        lambda_z_angles = calculate_angle_between_vectors(lambda_vectors, z_axis) * 1000
        
        hists['t_diff_vs_lambda_angle'].fill(
            lambda_z_angle=lambda_z_angles,
            t_diff=t_diff
        )
        print(f"  Filled t_diff_vs_lambda_angle: {len(t_diff)} entries")
    
    # 9. 2D: t error vs beam angle error
    if t_mask.sum() > 0:
        # Calculate beam angle error (difference from nominal 25 mrad)
        beam_px = df.loc[t_mask, 'mc_beam_prot_px'].values
        beam_py = df.loc[t_mask, 'mc_beam_prot_py'].values
        beam_pz = df.loc[t_mask, 'mc_beam_prot_pz'].values
        beam_vectors = np.column_stack([beam_px, beam_py, beam_pz])
        
        beam_z_angles = calculate_angle_between_vectors(beam_vectors, z_axis) * 1000
        beam_angle_error = beam_z_angles - 25.0  # Error from nominal 25 mrad
        
        # t error (difference between experimental and true)
        t_error = df.loc[t_mask, 'mc_lam_exp_t'].values - df.loc[t_mask, 'mc_true_t'].values
        
        hists['t_error_vs_beam_error'].fill(
            beam_angle_error=beam_angle_error,
            t_error=t_error
        )
        print(f"  Filled t_error_vs_beam_error: {len(t_error)} entries")


###############################################################################
# Plotting Functions
###############################################################################

def plot_1d_histogram(hist_1d, output_path):
    """Plot a simple 1D histogram"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Use hist's built-in plotting
    hist_1d.plot1d(ax=ax)
    
    # Add statistics to the plot
    values = hist_1d.values()
    edges = hist_1d.axes[0].edges
    centers = (edges[:-1] + edges[1:]) / 2
    
    if values.sum() > 0:
        mean = np.average(centers, weights=values)
        variance = np.average((centers - mean)**2, weights=values)
        std = np.sqrt(variance)
        
        # Add statistics box
        stats_text = f'Entries: {int(values.sum())}\n'
        stats_text += f'Mean: {mean:.3f}\n'
        stats_text += f'Std: {std:.3f}'
        
        ax.text(0.05, 0.95, stats_text, transform=ax.transAxes,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                fontsize=10)
    
    # Set labels
    if hist_1d.axes[0].label:
        ax.set_xlabel(hist_1d.axes[0].label)
    else:
        ax.set_xlabel(hist_1d.axes[0].name)
    ax.set_ylabel('Counts')
    ax.set_title(f'{hist_1d.axes[0].name} Distribution')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {output_path}")


def plot_2d_histogram(hist_2d, output_path):
    """Plot a 2D histogram using hist.plot"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Use hist's built-in plotting
    hist_2d.plot2d(ax=ax, cmap='viridis')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {output_path}")


def beam_rotation_sensitivity_analysis(output_dir, beam_mode=275.0, lambda_momentum=None):
    """Analyze t-value sensitivity to beam angle variations
    
    Fixed Lambda: 25 mrad horizontal, 100 μrad vertical, lambda_momentum GeV (from MC data average)
    Beam: varies from 24 to 26 mrad horizontal, 100 μrad vertical, beam_mode GeV
    
    Args:
        output_dir: Directory for output plots
        beam_mode: Detected beam momentum mode (GeV)
        lambda_momentum: Average Lambda momentum from MC data (GeV)
    """
    print("\nPerforming beam rotation sensitivity analysis...")
    
    # Fixed Lambda parameters
    if lambda_momentum is None:
        lambda_momentum = 200.0  # Default fallback
        print(f"  Warning: Using default Lambda momentum {lambda_momentum} GeV")
    else:
        print(f"  Using average Lambda momentum from MC data: {lambda_momentum:.2f} GeV")
    
    lambda_angle_hor = 25e-3  # 25 mrad
    lambda_angle_ver = 100e-6  # 100 μrad
    
    # Create fixed Lambda vector
    lambda_3vec = create_beam_vector_with_angle(lambda_momentum, lambda_angle_hor, lambda_angle_ver)
    lambda_4vec = create_lorentz_vector(lambda_3vec[0], lambda_3vec[1], lambda_3vec[2], LAMBDA_MASS)
    
    # Beam angle range (24 to 26 mrad)
    beam_angles_mrad = np.linspace(24, 26, 100)
    beam_angles_rad = beam_angles_mrad * 1e-3
    
    t_values = []
    
    for angle in beam_angles_rad:
        # Create beam vector with varying angle
        beam_3vec = create_beam_vector_with_angle(beam_mode, angle, CROSSING_ANGLE_VER)
        beam_4vec = create_lorentz_vector(beam_3vec[0], beam_3vec[1], beam_3vec[2], PROTON_MASS)
        
        # Calculate t
        t = calculate_t(beam_4vec, lambda_4vec)
        t_values.append(t)
    
    t_values = np.array(t_values)
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(beam_angles_mrad, -t_values, 'b-', linewidth=2, label='t-value')
    ax.axvline(x=25.0, color='r', linestyle='--', alpha=0.5, label='Nominal angle (25 mrad)')
    
    # Add reference lines at ±0.5 mrad
    ax.axvline(x=24.5, color='gray', linestyle=':', alpha=0.3)
    ax.axvline(x=25.5, color='gray', linestyle=':', alpha=0.3)
    
    ax.set_xlabel('Beam horizontal angle [mrad]')
    ax.set_ylabel(r'$-t$ [GeV$^2$]')
    ax.set_title(f'T-value Sensitivity to Beam Angle\n(Fixed $\Lambda$: {lambda_momentum:.1f} GeV @ 25 mrad, Beam: {beam_mode} GeV)')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Add text box with sensitivity info
    t_at_25 = -t_values[np.argmin(np.abs(beam_angles_mrad - 25.0))]
    t_at_24 = -t_values[0]
    t_at_26 = -t_values[-1]
    dt_dmrad = (t_at_26 - t_at_24) / 2.0
    
    info_text = f'Lambda: {lambda_momentum:.1f} GeV @ 25 mrad\n'
    info_text += f'At nominal (25 mrad): -t = {t_at_25:.4f} GeV²\n'
    info_text += f'Sensitivity: {dt_dmrad:.4f} GeV²/mrad\n'
    info_text += f'Range (24-26 mrad): {t_at_24:.4f} to {t_at_26:.4f} GeV²'
    
    ax.text(0.05, 0.95, info_text, transform=ax.transAxes,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
            fontsize=10)
    
    plt.tight_layout()
    output_path = output_dir / "beam_rotation_sensitivity.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {output_path}")
    
    # Return data for further analysis if needed
    return beam_angles_mrad, t_values


def plot_angle_comparison(hists, output_dir):
    """Plot multiple angle distributions on the same plot for comparison"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    angle_hists = [
        ('beam_z_angle', 'Beam-Z angle', 'blue'),
        ('lambda_z_angle', 'Lambda-Z angle', 'red'),
        ('beam_lambda_angle', 'Beam-Lambda angle', 'green'),
        ('exp_mc_beam_angle', 'Exp-MC beam angle', 'orange')
    ]
    
    for hist_name, label, color in angle_hists:
        if hist_name in hists and hists[hist_name].sum() > 0:
            h = hists[hist_name]
            
            # Normalize for shape comparison
            h_normalized = h / h.sum()
            
            # Plot using hist's plot method
            h_normalized.plot1d(
                ax=ax,
                label=label,
                color=color,
                linewidth=2,
                alpha=0.8
            )
    
    ax.set_xlabel('Angle [mrad]')
    ax.set_ylabel('Normalized Counts')
    ax.set_title('Angular Distribution Comparison')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_path = output_dir / "angle_comparison.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {output_path}")


###############################################################################
# Save Histograms in UHI Format
###############################################################################

def save_histogram_uhi(hist_obj, output_path):
    """Save histogram in UHI JSON format"""
    import boost_histogram.serialization as bhs
    
    uhi_dict = bhs.to_uhi(hist_obj)
    
    with open(output_path, 'w') as f:
        json.dump(uhi_dict, f, indent=2)
    
    print(f"  Saved UHI: {output_path}")


###############################################################################
# Main Analysis
###############################################################################

def main():
    parser = argparse.ArgumentParser(description='Beam angle and t-error analysis of CSV files')
    parser.add_argument('-o', '--outdir', type=str, default='beam_t_error_output',
                        help='Directory for output plots and JSON files')
    parser.add_argument('-e', '--events', type=int, default=None,
                        help='Number of events to process')
    parser.add_argument('files', nargs='+', help='Input CSV files')
    
    args = parser.parse_args()
    
    # Create output directories
    output_dir = Path(args.outdir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plots_1d_dir = output_dir / 'plots_1d'
    plots_1d_dir.mkdir(exist_ok=True)
    
    plots_2d_dir = output_dir / 'plots_2d'
    plots_2d_dir.mkdir(exist_ok=True)
    
    json_dir = output_dir / 'histograms_uhi'
    json_dir.mkdir(exist_ok=True)
    
    print("=" * 70)
    print("Beam Angle and T-Error Analysis")
    print("=" * 70)
    
    # Load data
    print("\nLoading CSV files...")
    df = concat_csvs_with_unique_events([Path(f) for f in args.files])
    
    if args.events is not None:
        print(f"Limiting to {args.events} events")
        df = df.head(args.events)
    
    print(f"Total events: {len(df)}")
    
    # Create histograms
    hists = create_histograms()
    
    # Calculate angles and fill histograms
    calculate_angles_and_fill(hists, df)
    
    # Save all histograms in UHI format
    print("\nSaving histograms in UHI format...")
    for name, h in hists.items():
        if h.sum() > 0:  # Only save non-empty histograms
            save_histogram_uhi(h, json_dir / f"{name}.json")
    
    # Create plots
    print("\nCreating plots...")
    
    # Plot 1D histograms
    print("\nCreating 1D histograms...")
    one_d_hists = ['beam_z_angle', 'beam_z_angle_corrected', 'exp_mc_beam_angle', 
                   'lambda_z_angle', 'beam_lambda_angle', 'lambda_pt', 'lambda_pz']
    
    for hist_name in one_d_hists:
        if hist_name in hists and hists[hist_name].sum() > 0:
            plot_1d_histogram(hists[hist_name], 
                            plots_1d_dir / f"{hist_name}.png")
    
    # Plot 2D histograms
    print("\nCreating 2D histograms...")
    two_d_hists = ['t_diff_vs_exp_mc_angle', 'lambda_angle_vs_beam_angle', 
                   't_diff_vs_lambda_angle', 't_error_vs_beam_error']
    
    for hist_name in two_d_hists:
        if hist_name in hists and hists[hist_name].sum() > 0:
            plot_2d_histogram(hists[hist_name],
                            plots_2d_dir / f"{hist_name}.png")
    
    # Create comparison plot
    print("\nCreating comparison plots...")
    plot_angle_comparison(hists, output_dir)
    
    # Perform beam rotation sensitivity analysis
    # Detect beam mode from data if available
    beam_mode = 275.0  # Default
    if 'mc_beam_prot_pz' in df.columns:
        avg_beam_pz = df['mc_beam_prot_pz'].dropna().abs().mean()
        beam_mode = detect_beam_mode(avg_beam_pz)
    
    # Calculate average Lambda momentum from MC data
    lambda_momentum_avg = None
    if all(col in df.columns for col in ['mc_lam_px', 'mc_lam_py', 'mc_lam_pz']):
        lambda_px = df['mc_lam_px'].dropna()
        lambda_py = df['mc_lam_py'].dropna()
        lambda_pz = df['mc_lam_pz'].dropna()
        
        if len(lambda_px) > 0 and len(lambda_py) > 0 and len(lambda_pz) > 0:
            # Calculate momentum magnitude for each Lambda
            lambda_momenta = np.sqrt(lambda_px.values**2 + lambda_py.values**2 + lambda_pz.values**2)
            lambda_momentum_avg = lambda_momenta.mean()
            print(f"\nAverage Lambda momentum from MC data: {lambda_momentum_avg:.2f} GeV")
            print(f"  (std: {lambda_momenta.std():.2f} GeV, min: {lambda_momenta.min():.2f}, max: {lambda_momenta.max():.2f})")
    
    beam_angles, t_values = beam_rotation_sensitivity_analysis(output_dir, beam_mode, lambda_momentum_avg)
    
    # Create summary statistics
    print("\nSummary Statistics:")
    print("-" * 70)
    
    summary = {}
    
    # Angle statistics
    for hist_name in one_d_hists:
        if hist_name in hists and hists[hist_name].sum() > 0:
            h = hists[hist_name]
            values = h.values()
            edges = h.axes[0].edges
            centers = (edges[:-1] + edges[1:]) / 2
            
            if values.sum() > 0:
                mean = np.average(centers, weights=values)
                variance = np.average((centers - mean)**2, weights=values)
                std = np.sqrt(variance)
                
                summary[hist_name] = {
                    'entries': int(values.sum()),
                    'mean': float(mean),
                    'std': float(std),
                    'min': float(centers[values > 0][0]),
                    'max': float(centers[values > 0][-1])
                }
                
                # Choose appropriate units for display
                if hist_name in ['lambda_pt', 'lambda_pz']:
                    units = 'GeV'
                else:
                    units = 'mrad'
                
                print(f"{hist_name:25s}: mean={summary[hist_name]['mean']:7.3f} {units:4s}, "
                      f"std={summary[hist_name]['std']:6.3f} {units:4s}, "
                      f"entries={summary[hist_name]['entries']:6d}")
    
    # t-value difference statistics
    if 't_diff_vs_exp_mc_angle' in hists:
        h = hists['t_diff_vs_exp_mc_angle']
        # Project onto t_diff axis
        t_diff_values = h.project(1).values()
        t_diff_edges = h.axes[1].edges
        t_diff_centers = (t_diff_edges[:-1] + t_diff_edges[1:]) / 2
        
        if t_diff_values.sum() > 0:
            mean = np.average(t_diff_centers, weights=t_diff_values)
            variance = np.average((t_diff_centers - mean)**2, weights=t_diff_values)
            std = np.sqrt(variance)
            
            summary['t_difference'] = {
                'entries': int(t_diff_values.sum()),
                'mean': float(mean),
                'std': float(std)
            }
            
            print(f"\nt_difference (exp-true): mean={mean:7.3f} GeV^2, "
                  f"std={std:6.3f} GeV^2")
    
    # Save summary
    with open(output_dir / 'summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\n" + "=" * 70)
    print("Analysis Complete!")
    print(f"Output directory: {output_dir}")
    print(f"  1D plots: {plots_1d_dir}")
    print(f"  2D plots: {plots_2d_dir}")
    print(f"  UHI histograms: {json_dir}")
    print("=" * 70)


if __name__ == "__main__":
    main()
