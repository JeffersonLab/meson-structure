"""Configuration and constants for the neutral Lambda reconstruction analysis.

All user-adjustable analysis settings are defined here.
"""
from __future__ import annotations
import numpy as np

# Input ROOT files are provided through CLI; no user-specific absolute paths.
DEFAULT_RECO = None
DEFAULT_GENERATOR = None
DETECTORS = {
    'ZDC_HCal': 'ReconstructedHcalFarForwardZDCNeutrals',
    'B0_ECal': 'ReconstructedB0EcalNeutrals',
    'LFHCAL': 'ReconstructedLFHCALNeutrals',
}
Q2_EDGES = np.array([4., 10., 20., 40., 80., 160., 320., 640.])
XB_EDGES = np.geomspace(1e-4, 1., 25)
# Incident proton in the ePIC laboratory frame (same frame as EICrecon ROOT).
# The magnitude is 25 mrad; verify the SIGN from your geometry / MC truth.
# Set -25.0 if the hadron beam points toward negative x.
PROTON_E = 275.0
PROTON_MASS = 0.9382720813
PROTON_CROSSING_ANGLE_MRAD = -25.0
PROTON_CROSSING_PLANE = 'xz'
PROTON_P = np.sqrt(PROTON_E**2 - PROTON_MASS**2)
PROTON_ANGLE_RAD = PROTON_CROSSING_ANGLE_MRAD * 1e-3
PROTON_PX = PROTON_P * np.sin(PROTON_ANGLE_RAD)
PROTON_PY = 0.0
PROTON_PZ = PROTON_P * np.cos(PROTON_ANGLE_RAD)
PROTON_DIRECTION = np.array([PROTON_PX, PROTON_PY, PROTON_PZ]) / PROTON_P

# =====================================================================
# SELECTION CUTS
# =====================================================================
TMAX = 2.      # maximum -t [GeV^2], or None to disable
XL_MAX = 1.1    # maximum xL, or None to disable
MLSIGMA = 3.0   # Gaussian Lambda mass window; None disables mass cut
MPSIGMA = 3.0   # Gaussian pi0 mass window; None disables mass cut

# Optional selection windows (None disables either bound).
# theta_gg uses the ACTUAL two reconstructed Lambda photon daughters, not
# the event-wise best pi0 pair used in the legacy pi0 mass selection.
THETA_GG_MIN_MRAD = None
THETA_GG_MAX_MRAD = 30
THETA_LAMBDA_MIN_MRAD = None
THETA_LAMBDA_MAX_MRAD = None
# z is a mass-constrained photon-pointing HYPOTHESIS, NOT a fitted Lambda vertex.
# Only computed if photon referencePoints are physical calorimeter hit positions.
Z_LAMBDA_MIN_M = 4
Z_LAMBDA_MAX_M = 40
# For the mass-constrained pointing hypothesis only:
Z_VERTEX_SCAN_MIN_M = 0.0
Z_VERTEX_SCAN_MAX_M = 30.0
Z_VERTEX_GRID_STEPS = 61


# MC decay vertex in EDM4hep is expressed in mm.
# Only MC endpoint is used (do not mislabel calorimeter referencePoint as decay vertex).
VERTEX_MM_TO_M = 1.e-3

M_LAMBDA = 1.115683
FIT_MASS_LOW = 1.085
FIT_MASS_HIGH = 1.145
M_PI0 = 0.1349768
FIT_PI0_LOW = 0.065
FIT_PI0_HIGH = 0.205
MIN_FIT_ENTRIES = 12

# =====================================================================
# PLOT STYLE
# =====================================================================
COLOR_MC = "#5B6573"
COLOR_NO_BACKGROUND = "#1F4E79"
COLOR_WITH_BACKGROUND = "#C55A11"
COLOR_COMMON_LAMBDA = "#2E8B57"
COLOR_AUXILIARY = "#5B6573"

PLOT_COMMON_RECO_LAMBDAS = False
LABEL_COMMON_RECO_LAMBDAS = r"Common reconstructed $\Lambda$ ($N_{11}$)"

# Plot-only controls. A logarithmic ordinate exposes small populations without
# changing the selection or the underlying histogram normalization.
PLOT_LOG_COUNTS = True  # True: zero-preserving symlog; False: linear
PLOT_FULL_DATA_RANGE = True  # automatic 1D bins include all finite observations
PLOT_Y_HEADROOM = 1.35       # extra space above histogram peaks (log y)
PLOT_AUTO_LOG_X = False
PLOT_AUTO_SYMLOG_X = False
PLOT_LOG_X_DYNAMIC_RANGE = 100.0

BACKGROUND_SOURCES = {
    0: 'Sullivan signal',
    2000: 'Synchrotron radiation',
    3000: 'Electron beam-gas',
    4000: 'Electron Coulomb',
    5000: 'Electron Touschek',
    6000: 'Proton beam-gas',
    7000: 'DIS-NC',
}
BACKGROUND_SAMPLE_MAX = 30000  # maximum plotted particles per source
BACKGROUND_PDG_LABELS = {
    11: 'e-', -11: 'e+', 22: 'gamma', 2112: 'n', -2112: 'anti-n',
    2212: 'p', -2212: 'anti-p', 111: 'pi0', 211: 'pi+',
    -211: 'pi-', 321: 'K+', -321: 'K-', 130: 'K_L',
    310: 'K_S', 3122: 'Lambda', -3122: 'anti-Lambda',
    13: 'mu-', -13: 'mu+',
}


RUN_FAST_BACKGROUND_DIAG = True
BACKGROUND_DIAG_EVENTS = 200  # representative frames, not all frames
BACKGROUND_DIAG_MAX_PARTICLES_PER_SOURCE = 10000
TRUTH_SCAN_EVENTS_PER_CHUNK = 64

PURITY_CHUNK_EVENTS = 12
PURITY_DEBUG_CANDIDATES = 80  # detailed candidate traces; summary covers all candidates
PURITY_DOMINANT_MIN_FRACTION = 0.50
PURITY_SOURCES = {0:'Sullivan signal', 2000:'Synchrotron radiation',
                  3000:'Electron beam-gas', 4000:'Electron Coulomb',
                  5000:'Electron Touschek', 6000:'Proton beam-gas', 7000:'DIS-NC'}
PURITY_ASSOC = {
    'HcalFarForwardZDCClusters': 'HcalFarForwardZDCClusterAssociations',
    'B0ECalClusters': 'B0ECalClusterAssociations',
    'LFHCALClusters': 'LFHCALClusterAssociations',
    'EcalEndcapPClusters': 'EcalEndcapPClusterAssociations',
}

# Structure-function uncertainty projections (separate from reconstruction cuts).
PROJECTION_BEAM = '18x275'
PROJECTION_METHODS = ('Truth', 'Electron', 'JB')
PROJECTION_LUMINOSITIES_FB = (0.041, 1.0, 2.5, 10.0, 50.0, 100.0)
PROJECTION_XB_EDGES = np.geomspace(1e-4, 1.0, 31)
PROJECTION_X_EDGES = np.array([.001,.002,.004,.01,.02,.04,.1,.2,.4,1.])
PROJECTION_Q2_EDGES = np.array([4.,20.,80.,640.])
PROJECTION_TMAX = None  # None disables the projection-specific -t cut.
PROJECTION_MIN_EVENTS = 1.0
PROJECTION_BACKGROUND_MODE = 'none'  # or 'rate_proxy' (exploratory)

# Model-projection figures and external model inputs.
MODEL_PLOT_ENABLED = False  # Enable with --plot-models (LHAPDF required for JAM).
MODEL_PLOT_TYPES = ('DSE', 'JAM')
MODEL_COMPONENTS = ('valence', 'glue')
MODEL_POINT_TO_POINT_SYSTEMATIC = 0.025
MODEL_JAM_SET = 'JAM25kaon_nlonll'
MODEL_JAM_Q2_GEV2 = 5.2 ** 2
MODEL_LHAPDF_PATH = "/work/eic3/users/fraisse/lhapdf"
MODEL_E615_DATA = None  # Optional three-column pion valence reference data.
