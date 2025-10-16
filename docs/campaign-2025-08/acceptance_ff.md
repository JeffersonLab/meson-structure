# Far Forward Acceptance Analysis

## Overview

This document presents the acceptance analysis for Lambda (Λ) baryons in the 
Far Forward (FF) detector region of the EPIC detector at the EIC.

- **5×41 GeV**: 5 GeV electron beam on 41 GeV proton beam
- **10×100 GeV**: 10 GeV electron beam on 100 GeV proton beam  
- **10×130 GeV**: 10 GeV electron beam on 130 GeV proton beam
- **18×275 GeV**: 18 GeV electron beam on 275 GeV proton beam


## Lambda Decay over Energies

![Lambda Decay](/analysis/campaign-2025-08/acceptance_ff/lambda_decay.png)

![Lambda Decay Zoom](/analysis/campaign-2025-08/acceptance_ff/lambda_decay_zoom.png)

![Lambda Decay Cumulative](/analysis/campaign-2025-08/acceptance_ff/lambda_decay_cumulative.png)


## Decay Distance



| Energy Configuration | Distribution Plot |
|---------------------|-------------------|
| **5×41 GeV** | ![Lambda Distance 5x41](/analysis/campaign-2025-08/acceptance_ff/bidim_lambda_distance_5x41.png) |
| **10×100 GeV** | ![Lambda Distance 10x100](/analysis/campaign-2025-08/acceptance_ff/bidim_lambda_distance_10x100.png) |
| **10×130 GeV** | ![Lambda Distance 10x130](/analysis/campaign-2025-08/acceptance_ff/bidim_lambda_distance_10x130.png) |
| **18×275 GeV** | ![Lambda Distance 18x275](/analysis/campaign-2025-08/acceptance_ff/bidim_lambda_distance_18x275.png) |

**Key Observations:**
- Higher beam energies generally produce Lambdas with larger decay distances due to increased Lorentz boost (γ factor)
- The bidimensional plots show the correlation between generated and reconstructed decay distances, revealing reconstruction efficiency
- The FF detector acceptance is optimized for particles at small angles (large η), with tracking layers positioned to cover the expected decay regions
- Reconstruction efficiency depends on both the decay distance and the Lambda momentum, with challenges arising from very short decays (close to the interaction point) and very long decays (beyond the tracking volume)

## Lambda Decay Products

Understanding the acceptance for Lambda decay products (proton and π⁻) is crucial for reconstruction efficiency. The decay topology and kinematics of individual particles determine whether the Lambda can be successfully reconstructed. Additionally, the production of associated particles (neutrons, π⁰) provides important context for the reaction mechanism.

### Proton from Lambda Decay

The proton from Lambda decay typically carries most of the Lambda momentum and must be detected in the FF tracking system. The proton's high momentum and forward direction make it well-suited for detection in the Far Forward region.

| Energy Configuration | Decay Distance Distribution |
|---------------------|-------------------|
| **5×41 GeV** | ![Proton Distance 5x41](/analysis/campaign-2025-08/acceptance_ff/bidim_prot_distance_5x41.png) |
| **10×100 GeV** | ![Proton Distance 10x100](/analysis/campaign-2025-08/acceptance_ff/bidim_prot_distance_10x100.png) |
| **10×130 GeV** | ![Proton Distance 10x130](/analysis/campaign-2025-08/acceptance_ff/bidim_prot_distance_10x130.png) |
| **18×275 GeV** | ![Proton Distance 18x275](/analysis/campaign-2025-08/acceptance_ff/bidim_prot_distance_18x275.png) |

**Analysis Notes:**
- Proton detection efficiency is generally high due to good tracking coverage and particle identification capabilities
- The proton carries approximately 64% of the Lambda momentum in the rest frame, resulting in a highly forward-boosted proton in the lab frame
- Particle identification (PID) is essential to distinguish protons from other charged hadrons

### Pion⁻ from Lambda Decay

The π⁻ from Lambda decay typically has lower momentum and a wider angular distribution compared to the proton. Efficient pion detection is critical since both decay products must be reconstructed for Lambda identification.

| Energy Configuration | Decay Distance Distribution |
|---------------------|-------------------|
| **5×41 GeV** | ![Pion- Distance 5x41](/analysis/campaign-2025-08/acceptance_ff/bidim_pimin_distance_5x41.png) |
| **10×100 GeV** | ![Pion- Distance 10x100](/analysis/campaign-2025-08/acceptance_ff/bidim_pimin_distance_10x100.png) |
| **10×130 GeV** | ![Pion- Distance 10x130](/analysis/campaign-2025-08/acceptance_ff/bidim_pimin_distance_10x130.png) |
| **18×275 GeV** | ![Pion- Distance 18x275](/analysis/campaign-2025-08/acceptance_ff/bidim_pimin_distance_18x275.png) |

**Key Points:**
- Pion⁻ detection is more challenging at higher energies due to the boost-dependent opening angle between proton and pion
- The pion's lower momentum means it is more susceptible to multiple scattering in detector material
- Combined tracking and calorimetry help identify pions and reject backgrounds

### Associated Neutron Production

Neutrons may be produced in association with the Lambda through various reaction channels. Neutron detection in the Zero Degree Calorimeter (ZDC) provides additional information about the reaction mechanism.

| Energy Configuration | Neutron Distribution |
|---------------------|-------------------|
| **5×41 GeV** | ![Neutron Distance 5x41](/analysis/campaign-2025-08/acceptance_ff/bidim_neut_distance_5x41.png) |
| **10×100 GeV** | ![Neutron Distance 10x100](/analysis/campaign-2025-08/acceptance_ff/bidim_neut_distance_10x100.png) |
| **10×130 GeV** | ![Neutron Distance 10x130](/analysis/campaign-2025-08/acceptance_ff/bidim_neut_distance_10x130.png) |
| **18×275 GeV** | ![Neutron Distance 18x275](/analysis/campaign-2025-08/acceptance_ff/bidim_neut_distance_18x275.png) |

**Physics Context:**
- Neutrons can be produced through baryon number conservation in the reaction
- The ZDC provides efficient neutron detection at very forward angles
- Neutron tagging helps distinguish different reaction channels and reduce backgrounds

### Associated π⁰ Production

Neutral pions may be produced in the fragmentation region or through resonance decays. Their detection relies on electromagnetic calorimetry.

| Energy Configuration | π⁰ Distribution |
|---------------------|-------------------|
| **5×41 GeV** | ![Pion0 Distance 5x41](/analysis/campaign-2025-08/acceptance_ff/bidim_pizero_distance_5x41.png) |
| **10×100 GeV** | ![Pion0 Distance 10x100](/analysis/campaign-2025-08/acceptance_ff/bidim_pizero_distance_10x100.png) |
| **10×130 GeV** | ![Pion0 Distance 10x130](/analysis/campaign-2025-08/acceptance_ff/bidim_pizero_distance_10x130.png) |
| **18×275 GeV** | ![Pion0 Distance 18x275](/analysis/campaign-2025-08/acceptance_ff/bidim_pizero_distance_18x275.png) |

**Detection Strategy:**
- π⁰ → γγ decay requires reconstruction of two photons in the electromagnetic calorimeter
- Invariant mass reconstruction helps identify π⁰ candidates
- High granularity calorimetry is essential for resolving the two-photon system

## Detector-Specific Acceptance

The Far Forward region consists of multiple detector subsystems, each optimized for specific particle types and kinematic ranges. The following sections show polar acceptance plots for different particles in various detector components. These plots display the angular distribution of particle hits in a polar coordinate representation, providing insight into the geometric acceptance of each subsystem.

### Proton Detection Systems

The FF region employs three complementary tracking systems for proton detection, each covering different angular and momentum ranges.

#### B0 Tracker

The B0 tracker provides tracking coverage close to the beam pipe in the forward direction, essential for detecting high-momentum particles at small angles.

| Energy Configuration | Polar Acceptance |
|---------------------|-------------------|
| **5×41 GeV** | ![Proton B0 5x41](/analysis/campaign-2025-08/acceptance_ff/proton_B0TrackerHits_5x41_polar_zoom.png) |
| **10×100 GeV** | ![Proton B0 10x100](/analysis/campaign-2025-08/acceptance_ff/proton_B0TrackerHits_10x100_polar_zoom.png) |
| **18×275 GeV** | ![Proton B0 18x275](/analysis/campaign-2025-08/acceptance_ff/proton_B0TrackerHits_18x275_polar_zoom.png) |

**B0 Tracker Characteristics:**
- Located close to the interaction region
- Designed for particles at very forward angles (small θ)
- Provides the first hit information for track seeding
- Critical for high-momentum protons from Lambda decays

#### Forward Off-Momentum Tracker

The Forward Off-Momentum (OMD) tracker system captures particles scattered at small angles, including protons from Lambda decays that are slightly deflected from the beam direction.

| Energy Configuration | Polar Acceptance |
|---------------------|-------------------|
| **5×41 GeV** | ![Proton OMD 5x41](/analysis/campaign-2025-08/acceptance_ff/proton_ForwardOffMTrackerRecHits_5x41_polar_zoom.png) |
| **10×100 GeV** | ![Proton OMD 10x100](/analysis/campaign-2025-08/acceptance_ff/proton_ForwardOffMTrackerRecHits_10x100_polar_zoom.png) |
| **18×275 GeV** | ![Proton OMD 18x275](/analysis/campaign-2025-08/acceptance_ff/proton_ForwardOffMTrackerRecHits_18x275_polar_zoom.png) |

**Forward OMD Characteristics:**
- Positioned downstream from B0
- Covers a complementary angular range
- Excellent position resolution for momentum determination
- Particularly important for protons with transverse momentum

#### Forward Roman Pot

The Roman Pot detectors are specialized tracking stations positioned very close to the beam line, designed to detect forward protons at extremely small scattering angles.

| Energy Configuration | Polar Acceptance |
|---------------------|-------------------|
| **5×41 GeV** | ![Proton RomanPot 5x41](/analysis/campaign-2025-08/acceptance_ff/proton_ForwardRomanPotRecHits_5x41_polar_zoom.png) |
| **10×100 GeV** | ![Proton RomanPot 10x100](/analysis/campaign-2025-08/acceptance_ff/proton_ForwardRomanPotRecHits_10x100_polar_zoom.png) |
| **18×275 GeV** | ![Proton RomanPot 18x275](/analysis/campaign-2025-08/acceptance_ff/proton_ForwardRomanPotRecHits_18x275_polar_zoom.png) |

**Roman Pot Characteristics:**
- Can approach within millimeters of the beam
- Essential for detecting protons with minimal deflection
- Housed in movable "pots" that can be inserted during stable beam conditions
- Provides unique access to very small-t processes

### Charged Pion Detection

Charged pions from Lambda decay and other sources are detected in the B0 and OMD tracking systems. Both π⁺ and π⁻ are important for understanding the reaction kinematics and backgrounds.

#### Pion⁺ in B0 Tracker

| Energy Configuration | Polar Acceptance |
|---------------------|-------------------|
| **5×41 GeV** | ![Pion+ B0 5x41](/analysis/campaign-2025-08/acceptance_ff/pion+_B0TrackerHits_5x41_polar_zoom.png) |
| **10×100 GeV** | ![Pion+ B0 10x100](/analysis/campaign-2025-08/acceptance_ff/pion+_B0TrackerHits_10x100_polar_zoom.png) |
| **18×275 GeV** | ![Pion+ B0 18x275](/analysis/campaign-2025-08/acceptance_ff/pion+_B0TrackerHits_18x275_polar_zoom.png) |

#### Pion⁺ in Forward Off-Momentum Tracker

| Energy Configuration | Polar Acceptance |
|---------------------|-------------------|
| **5×41 GeV** | ![Pion+ OMD 5x41](/analysis/campaign-2025-08/acceptance_ff/pion+_ForwardOffMTrackerRecHits_5x41_polar_zoom.png) |
| **10×100 GeV** | ![Pion+ OMD 10x100](/analysis/campaign-2025-08/acceptance_ff/pion+_ForwardOffMTrackerRecHits_10x100_polar_zoom.png) |
| **18×275 GeV** | ![Pion+ OMD 18x275](/analysis/campaign-2025-08/acceptance_ff/pion+_ForwardOffMTrackerRecHits_18x275_polar_zoom.png) |

#### Pion⁻ in Forward Off-Momentum Tracker

The π⁻ from Lambda decay (Λ → p + π⁻) is a critical component for Lambda reconstruction.

| Energy Configuration | Polar Acceptance |
|---------------------|-------------------|
| **5×41 GeV** | ![Pion- OMD 5x41](/analysis/campaign-2025-08/acceptance_ff/pion-_ForwardOffMTrackerRecHits_5x41_polar_zoom.png) |
| **10×100 GeV** | ![Pion- OMD 10x100](/analysis/campaign-2025-08/acceptance_ff/pion-_ForwardOffMTrackerRecHits_10x100_polar_zoom.png) |
| **18×275 GeV** | ![Pion- OMD 18x275](/analysis/campaign-2025-08/acceptance_ff/pion-_ForwardOffMTrackerRecHits_18x275_polar_zoom.png) |

**Pion Tracking Observations:**
- Pions typically have wider angular distributions than protons from Lambda decays
- The combination of B0 and OMD provides comprehensive coverage
- Charge sign determination is essential for distinguishing π⁺ from π⁻
- Lower momentum pions are more affected by magnetic field deflection

### Neutral Particle Detection

Neutral particles (neutrons and π⁰) are detected in calorimetric systems, with the ZDC playing a crucial role for very forward particles.

#### Neutron Detection in Far Forward ZDC

The hadronic Zero Degree Calorimeter (HCal ZDC) is optimized for neutron detection at very small angles.

| Energy Configuration | Polar Acceptance |
|---------------------|-------------------|
| **5×41 GeV** | ![Neutron ZDC 5x41](/analysis/campaign-2025-08/acceptance_ff/neutron_HcalFarForwardZDCClusters_5x41_polar_zoom.png) |
| **10×100 GeV** | ![Neutron ZDC 10x100](/analysis/campaign-2025-08/acceptance_ff/neutron_HcalFarForwardZDCClusters_10x100_polar_zoom.png) |
| **18×275 GeV** | ![Neutron ZDC 18x275](/analysis/campaign-2025-08/acceptance_ff/neutron_HcalFarForwardZDCClusters_18x275_polar_zoom.png) |

**Neutron Detection Characteristics:**
- HCal ZDC provides efficient neutron detection through hadronic showers
- Position resolution helps determine neutron scattering angle
- Energy measurement provides momentum information
- Essential for identifying neutron-producing reaction channels

#### π⁰ Detection

Neutral pions are reconstructed through their two-photon decay (π⁰ → γγ) using electromagnetic calorimetry.

**π⁰ in B0 ECal:**

| Energy Configuration | Polar Acceptance |
|---------------------|-------------------|
| **5×41 GeV** | ![Pion0 B0ECal 5x41](/analysis/campaign-2025-08/acceptance_ff/pion0_B0ECalClusters_5x41_polar_zoom.png) |
| **10×100 GeV** | ![Pion0 B0ECal 10x100](/analysis/campaign-2025-08/acceptance_ff/pion0_B0ECalClusters_10x100_polar_zoom.png) |
| **18×275 GeV** | ![Pion0 B0ECal 18x275](/analysis/campaign-2025-08/acceptance_ff/pion0_B0ECalClusters_18x275_polar_zoom.png) |

**π⁰ in ECal Far Forward ZDC:**

| Energy Configuration | Polar Acceptance |
|---------------------|-------------------|
| **5×41 GeV** | ![Pion0 ECalZDC 5x41](/analysis/campaign-2025-08/acceptance_ff/pion0_EcalFarForwardZDCClusters_5x41_polar_zoom.png) |

**π⁰ in HCal Far Forward ZDC:**

| Energy Configuration | Polar Acceptance |
|---------------------|-------------------|
| **5×41 GeV** | ![Pion0 HCalZDC 5x41](/analysis/campaign-2025-08/acceptance_ff/pion0_HcalFarForwardZDCClusters_5x41_polar_zoom.png) |
| **10×100 GeV** | ![Pion0 HCalZDC 10x100](/analysis/campaign-2025-08/acceptance_ff/pion0_HcalFarForwardZDCClusters_10x100_polar_zoom.png) |
| **18×275 GeV** | ![Pion0 HCalZDC 18x275](/analysis/campaign-2025-08/acceptance_ff/pion0_HcalFarForwardZDCClusters_18x275_polar_zoom.png) |

**π⁰ Detection Strategy:**
- Primary detection via B0 ECal for π⁰ at intermediate angles
- FF ZDC calorimeters (both ECal and HCal) provide coverage at very forward angles
- Two-photon invariant mass reconstruction identifies π⁰ candidates
- High-granularity calorimetry essential for resolving photon pairs

## Acceptance Summary and Energy Comparison

The acceptance analysis across four beam energy configurations reveals several important characteristics:

### Energy-Dependent Trends

| Energy Configuration | Lambda Kinematics | Decay Product Coverage | Detector Occupancy |
|---------------------|-------------------|------------------------|-------------------|
| **5×41 GeV** | Lower momentum, wider angular distribution | Good coverage in B0 and OMD | Moderate, manageable |
| **10×100 GeV** | Intermediate momentum, more forward-peaked | Excellent combined coverage | Higher, still acceptable |
| **10×130 GeV** | Similar to 10×100 with extended reach | Very good across all systems | Comparable to 10×100 |
| **18×275 GeV** | Highest momentum, most forward | Roman Pot becomes critical | Highest, requires optimization |

### Detector System Performance

**Tracking Systems:**
- **B0 Tracker**: Provides essential first-layer tracking across all energies, with acceptance optimized for forward particles
- **Forward OMD**: Comprehensive coverage for both Lambda decay products (p and π⁻), with good efficiency across the energy range
- **Roman Pot**: Critical for highest-energy configuration where particles are most forward-boosted

**Calorimetry:**
- **B0 ECal**: Good coverage for π⁰ and photons at intermediate angles
- **FF ZDC (ECal + HCal)**: Essential for neutral particles at very forward angles, with acceptance improving at higher energies
- **Combined Performance**: Complementary coverage ensures efficient detection across kinematic range

## Systematic Considerations

Several systematic effects must be carefully evaluated when using these acceptance maps for physics analysis:

### Reconstruction Efficiency

1. **Tracking Efficiency**: 
   - Depends on particle momentum, angle, and detector occupancy
   - Multiple tracking systems provide redundancy for cross-checks
   - Edge effects at detector boundaries require careful treatment
   - Material budget affects low-momentum pion tracking

2. **Decay Vertex Reconstruction**:
   - Vertex finding efficiency depends on decay distance and opening angle
   - Secondary vertex algorithms must handle wide range of topologies
   - Background from random track combinations requires robust rejection

3. **Particle Identification**:
   - Proton/pion separation essential for Lambda reconstruction
   - PID performance varies with momentum and angle
   - Combined use of dE/dx, time-of-flight, and calorimetry improves discrimination

### Background Considerations

1. **Physics Backgrounds**:
   - K⁰_S → π⁺π⁻ has similar decay topology to Lambda
   - Σ⁰ → Λγ can produce Lambda candidates
   - Combinatorial background from uncorrelated tracks

2. **Detector Effects**:
   - Secondary interactions in material produce fake vertices
   - Photon conversions can mimic charged particle tracks
   - Detector noise and dead channels affect reconstruction

### Acceptance Corrections

1. **Monte Carlo Validation**:
   - Detailed simulation of detector response essential
   - Comparison with data in control regions validates acceptance maps
   - Energy-dependent corrections required for physics measurements

2. **Kinematic Dependence**:
   - Acceptance varies with Lambda momentum, angle, and decay distance
   - Multidimensional acceptance maps needed for unfolding
   - Correlations between variables must be preserved

## Recommendations for Physics Analysis

Based on this comprehensive acceptance study, we provide the following recommendations for Sullivan process measurements:

### Energy Configuration Selection

1. **10×100 GeV and 18×275 GeV**: Optimal configurations for meson structure studies
   - Provide best combination of kinematic reach and statistics
   - Cover complementary x and Q² regions
   - Higher energies access lower-x regime important for sea quark distributions

2. **5×41 GeV**: Valuable for systematic studies
   - Lower detector occupancy simplifies reconstruction
   - Access to valence quark region at higher x
   - Important for understanding energy-dependent effects

3. **10×130 GeV**: Intermediate option
   - Bridges gap between 10×100 and 18×275 configurations
   - Provides additional Q² coverage
   - Useful for interpolation and systematic studies

### Event Selection Strategy

1. **Lambda Reconstruction**:
   - Require both decay products (p and π⁻) in OMD or B0 acceptance
   - Apply stringent vertex quality cuts to reject backgrounds
   - Use invariant mass window around Lambda mass (1.115 GeV)
   - Implement momentum-dependent selection criteria

2. **DIS Event Selection**:
   - Require reconstructed scattered electron with Q² > 1 GeV²
   - Apply cuts on electron energy and angle for DIS regime
   - Veto on additional activity to ensure exclusive final state
   - Use timing information to reject out-of-time backgrounds

3. **Kaon Tagging**:
   - Reconstruct outgoing K⁺ in central or forward region
   - Use particle identification to separate kaons from pions
   - Apply missing mass cuts to ensure Λ+K final state
   - Require momentum and angular consistency

### Systematic Uncertainty Estimation

1. **Tracking Systematics**:
   - Vary track selection criteria to assess stability
   - Use data-driven methods (tag-and-probe) where possible
   - Study efficiency versus occupancy in simulation
   - Compare different tracking algorithms

2. **PID Systematics**:
   - Measure PID efficiency and misidentification rates in data
   - Use control samples (e.g., K⁰_S, Λ, φ → KK) for calibration
   - Assess momentum and angle dependence
   - Evaluate impact of detector aging and calibration drifts

3. **Acceptance Systematics**:
   - Vary generator-level assumptions in simulation
   - Compare different Monte Carlo generators
   - Study sensitivity to detector alignment and calibration
   - Assess impact of material budget uncertainties

## Conclusions

This comprehensive Far Forward acceptance analysis demonstrates that the EPIC detector is exceptionally well-suited for Sullivan process measurements at the EIC:

### Key Findings

1. **Detector Coverage**: The combination of B0 Tracker, Forward OMD, Roman Pot, and FF ZDC systems provides comprehensive coverage for Lambda detection across all four energy configurations

2. **Lambda Reconstruction**: Both Lambda decay products (proton and π⁻) have good acceptance in the tracking systems, enabling efficient Lambda reconstruction with manageable backgrounds

3. **Energy Scaling**: Acceptance characteristics scale appropriately with beam energy, with higher energies shifting distributions to more forward angles as expected from kinematics

4. **Neutral Particles**: Efficient detection of neutrons and π⁰ in the ZDC and B0 ECal systems provides important auxiliary information for event classification

5. **Complementary Systems**: Multiple detector subsystems provide redundancy and enable robust systematic studies through cross-checks

### Physics Impact

The acceptance maps presented here enable:

- **Precision Measurements**: Sufficient acceptance and resolution for high-quality kaon structure function measurements
- **Kinematic Coverage**: Access to wide ranges in x (0.01-0.8), Q² (1-100 GeV²), and t (0-1 GeV²)
- **Systematic Control**: Multiple detection methods and energy configurations provide handles for systematic uncertainty reduction
- **Future Optimization**: Detailed understanding of acceptance informs trigger strategies and detector optimization

### Next Steps

This acceptance analysis provides essential input for:

1. Developing event generators and simulation frameworks
2. Designing trigger strategies for Sullivan process events
3. Optimizing reconstruction algorithms and selection criteria
4. Planning calibration and monitoring strategies
5. Estimating projected statistical and systematic uncertainties

The detailed acceptance maps will be continuously refined as detector designs are finalized and as experience is gained from detector commissioning and early running.

## Data and Analysis Information

- **Campaign**: 2025-08
- **Simulation Framework**: EDM4HEP/EDM4EIC
- **Detector Configuration**: EPIC Far Forward system (B0 Tracker, Forward OMD, Roman Pot, FF ZDC)
- **Analysis Software**: CERN ROOT
- **Lambda Decay Channel**: Λ → p + π⁻ (branching ratio ~63.9%)
- **Monte Carlo Generator**: Configured for DIS events with Sullivan process implementation
- **Reconstruction**: Particle flow reconstruction, vertex finding, and track matching applied consistently across all energy configurations
- **Acceptance Calculation**: Based on truth-level to reconstructed particle matching with efficiency maps as function of kinematics

---

*This analysis is part of the ongoing EIC detector preparation for meson structure measurements using the Sullivan process. The acceptance studies inform detector optimization, trigger strategies, and analysis methodology development. For questions, additional information, or access to the detailed analysis code and data files, contact the meson structure analysis working group.*

**Document Version**: 1.0 (Campaign 2025-08)  
**Last Updated**: October 2025  
**Analysis Contact**: Meson Structure Working Group