"""Beam, detector, selection and plotting settings for pion–neutron analysis."""
from __future__ import annotations
from pathlib import Path
import numpy as np
# ROOT input paths are supplied via CLI.
DEFAULT_SIGNAL = None
DEFAULT_MIXED = None
DEFAULT_OUT=Path('outputs/neutrons/9x275')

# =====================================================================
# PLOT OPTIONS
# =====================================================================
PLOT_HIST_LOG_Y = True    # True: zero-preserving symlog (log-like), continuous stairs
                          # False: linear Y starting at 0
PLOT_MAP_LOG_Y = True     # Q2 axis on 2D efficiency map (independent)
PLOT_FULL_DATA_RANGE = True  # include all finite values in automatic histogram bins
PLOT_Y_HEADROOM = 1.35       # multiplicative log-y headroom (linear uses 15%)

# CANDIDATE SELECTION: None disables a cut bound.
XL_MIN=None
XL_MAX=None
THETA_MIN_MRAD=21
THETA_MAX_MRAD=28
PT_BEAM_MIN_GEV=None
PT_BEAM_MAX_GEV=None
MINUS_T_MIN_GEV2=0.01
MINUS_T_MAX_GEV2=1
ENERGY_MIN_GEV=None
ENERGY_MAX_GEV=400
# Phi is periodic: distance to the beam's lab azimuth (+/-pi), in radians.
# E.g. 0.20 keeps |phi| > pi - 0.20; None disables.
PHI_DISTANCE_TO_PI_MAX_RAD=None
# Optional invariant-mass selections [GeV], all disabled by default.
W_MIN_GEV=None
W_MAX_GEV=40
MX_MIN_GEV=None
MX_MAX_GEV=None
# BEAM AND ELECTRON KINEMATICS (GeV)
# Electron travels approximately along -z for the default 9 x 275 campaign.
ELECTRON_BEAM_ENERGY_GEV=9.0
ELECTRON_MASS_GEV=0.00051099895
# Use a dedicated scattered-electron collection: NEVER guess from arbitrary
# charged-particle candidates or use generator truth for a reconstructed cut.
SCATTERED_ELECTRON_COLLECTION=None  # e.g. 'ScatteredElectrons'; autodetect unique supported collection
ELECTRON_COLLECTION_CANDIDATES=('ScatteredElectrons','ReconstructedScatteredElectrons',
                                'ReconstructedElectrons')
# Optional diagnostic: threshold on dominance of source-zero energy contribution.
# This is a *purity definition*, not a selection on reconstructed observables.
SIGNAL_SOURCE_MIN_FRACTION=0.5
PROTON_ENERGY=275.0
PROTON_MASS=0.9382720813
PROTON_CROSSING_MRAD=-25.0
PROTON_P=np.sqrt(PROTON_ENERGY**2-PROTON_MASS**2)
BEAM_DIR=np.array([np.sin(PROTON_CROSSING_MRAD*1e-3),0.0,
                   np.cos(PROTON_CROSSING_MRAD*1e-3)])
BEAM_MOM=PROTON_P*BEAM_DIR
NEUTRON_MASS=0.9395654205
# DETECTOR COLLECTIONS AND MC ASSOCIATIONS
NEUTRAL_COLLECTION='ReconstructedHcalFarForwardZDCNeutrals'
CLUSTER_COLLECTION='HcalFarForwardZDCClusters'
ASSOC_COLLECTION='HcalFarForwardZDCClusterAssociations'
CHUNK=64  # fewer uproot reads; lower if memory is constrained
BACKGROUND_SAMPLE_EVENTS=150
SOURCES={0:'Sullivan signal',2000:'Synchrotron',3000:'Electron beam-gas',
         4000:'Electron Coulomb',5000:'Electron Touschek',6000:'Proton beam-gas',7000:'DIS-NC'}
# PLOT COLORS AND AXIS LABELS
COLORS={'signal':'#278653','combinatorial':'#626d7c','unclassified':'#c19a48',
        'signal_only':'#24567c','mixed':'#c46b27','truth':'#555d69'}
METRICS={
 'E':r'$E_n$ [GeV]', 'p':r'$|\vec p_n|$ [GeV]',
 'pt_beam':r'$p_{T,n}^{beam}$ [GeV]',
 'theta_mrad':r'$\theta_n$ [mrad, lab $z$]',
 'theta_beam_mrad':r'$\theta_n^{beam}$ [mrad]',
 'phi':r'$\phi_n$ [rad]', 'delta_phi_pi':r'$\pi-|\phi_n|$ [rad]', 'eta':r'$\eta_n$',
 'W':r'$W$ [GeV]', 'MX':r'$M_X$ [GeV]',
 'xL':r'$x_L$', 'minus_t':r'$-t$ [GeV$^2$]',
 'mass':r'$m_n^{reco}$ [GeV]',
 'z_reference_m':r'$z_{reference}$ [m] (NOT decay vertex)',
}
CUTS=[('xL','xL',XL_MIN,XL_MAX),
      ('theta_lab', 'theta_mrad',THETA_MIN_MRAD, THETA_MAX_MRAD),
      ('pt_beam','pt_beam',PT_BEAM_MIN_GEV,PT_BEAM_MAX_GEV),
      ('minus_t','minus_t',MINUS_T_MIN_GEV2,MINUS_T_MAX_GEV2),
      ('energy','E',ENERGY_MIN_GEV,ENERGY_MAX_GEV),
      ('phi_pi','delta_phi_pi',None,PHI_DISTANCE_TO_PI_MAX_RAD),
      ('W','W',W_MIN_GEV,W_MAX_GEV),
      ('MX','MX',MX_MIN_GEV,MX_MAX_GEV)]

# Structure-function uncertainty projections (separate from reconstruction cuts).
PROJECTION_BEAM = '9x275'
PROJECTION_METHODS = ('Truth', 'Electron', 'JB')
PROJECTION_LUMINOSITIES_FB = (0.041,1.0,2.5,10.0,50.0,100.0)
PROJECTION_X_EDGES = np.array([.025,.075,.125,.175,.225,.275,.325,.375,.425,.475,
                               .525,.575,.625,.675,.725,.775,.825,.875,.925,.975,1.0])
PROJECTION_Q2_EDGES = np.array([4.,10.,20.,40.,80.,160.,320.,640.])
PROJECTION_PT_TRUTH_MAX_GEV = 0.8
PROJECTION_MIN_EVENTS = 1.0
PROJECTION_BACKGROUND_MODE = 'none'  # or 'rate_proxy' (exploratory)
PROJECTION_TRUTH_NEUTRON_STATUS = 1
PROJECTION_INCOMING_PROTON_STATUS = 4

# Model-projection figures and external model inputs.
MODEL_PLOT_ENABLED = False  # Enable with --plot-models (LHAPDF required for JAM).
MODEL_PLOT_TYPES = ('DSE', 'JAM')
MODEL_COMPONENTS = ('valence', 'glue')
MODEL_POINT_TO_POINT_SYSTEMATIC = 0.025
MODEL_JAM_SET = 'JAM21PionPDFnlo'
MODEL_JAM_Q2_GEV2 = 5.2 ** 2
MODEL_LHAPDF_PATH = "/work/eic3/users/fraisse/lhapdf"
MODEL_E615_DATA = None  # Optional three-column pion valence reference data.
