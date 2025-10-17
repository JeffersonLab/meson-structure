# Far Forward Acceptance Analysis

## Overview

This document presents the acceptance analysis for Lambda (Λ) baryons in the 
Far Forward (FF) detector region of the EPIC detector at the EIC.

- **5×41 GeV**: 5 GeV electron beam on 41 GeV proton beam
- **10×100 GeV**: 10 GeV electron beam on 100 GeV proton beam  
- **10×130 GeV**: 10 GeV electron beam on 130 GeV proton beam
- **18×275 GeV**: 18 GeV electron beam on 275 GeV proton beam


### Lambda Decay over Energies

![Lambda Decay](/analysis/campaign-2025-08/acceptance_ff/lambda_decay.png)

![Lambda Decay Zoom](/analysis/campaign-2025-08/acceptance_ff/lambda_decay_zoom.png)

![Lambda Decay Cumulative](/analysis/campaign-2025-08/acceptance_ff/lambda_decay_cumulative.png)


### Momentum vs decay distance


| Beam      | Distribution Plot |
|----------------|-------------------|
| **5×41**   | ![Lambda Distance 5x41](/analysis/campaign-2025-08/acceptance_ff/bidim_lambda_distance_5x41.png) |
| **10×100** | ![Lambda Distance 10x100](/analysis/campaign-2025-08/acceptance_ff/bidim_lambda_distance_10x100.png) |
| **10×130** | ![Lambda Distance 10x130](/analysis/campaign-2025-08/acceptance_ff/bidim_lambda_distance_10x130.png) |
| **18×275** | ![Lambda Distance 18x275](/analysis/campaign-2025-08/acceptance_ff/bidim_lambda_distance_18x275.png) |


## Lambda Decay Products

Lambda decay products (proton and π⁻)

### Proton P vs Z endpoint

| Energy Configuration | Decay Distance Distribution |
|---------------------|-------------------|
| **5×41 GeV** | ![Proton Distance 5x41](/analysis/campaign-2025-08/acceptance_ff/bidim_prot_distance_5x41.png) |
| **10×100 GeV** | ![Proton Distance 10x100](/analysis/campaign-2025-08/acceptance_ff/bidim_prot_distance_10x100.png) |
| **10×130 GeV** | ![Proton Distance 10x130](/analysis/campaign-2025-08/acceptance_ff/bidim_prot_distance_10x130.png) |
| **18×275 GeV** | ![Proton Distance 18x275](/analysis/campaign-2025-08/acceptance_ff/bidim_prot_distance_18x275.png) |


### π⁻ P vs Z endpoint

The π⁻ from Lambda decay typically has lower momentum and a wider angular distribution compared to the proton.

| Energy Configuration | Decay Distance Distribution |
|---------------------|-------------------|
| **5×41 GeV** | ![Pion- Distance 5x41](/analysis/campaign-2025-08/acceptance_ff/bidim_pimin_distance_5x41.png) |
| **10×100 GeV** | ![Pion- Distance 10x100](/analysis/campaign-2025-08/acceptance_ff/bidim_pimin_distance_10x100.png) |
| **10×130 GeV** | ![Pion- Distance 10x130](/analysis/campaign-2025-08/acceptance_ff/bidim_pimin_distance_10x130.png) |
| **18×275 GeV** | ![Pion- Distance 18x275](/analysis/campaign-2025-08/acceptance_ff/bidim_pimin_distance_18x275.png) |


### Neutron P vs Z  decay distance


| Energy Configuration | Neutron Distribution |
|---------------------|-------------------|
| **5×41 GeV** | ![Neutron Distance 5x41](/analysis/campaign-2025-08/acceptance_ff/bidim_neut_distance_5x41.png) |
| **10×100 GeV** | ![Neutron Distance 10x100](/analysis/campaign-2025-08/acceptance_ff/bidim_neut_distance_10x100.png) |
| **10×130 GeV** | ![Neutron Distance 10x130](/analysis/campaign-2025-08/acceptance_ff/bidim_neut_distance_10x130.png) |
| **18×275 GeV** | ![Neutron Distance 18x275](/analysis/campaign-2025-08/acceptance_ff/bidim_neut_distance_18x275.png) |


###  π⁰ P vs Z

Neutral pions may be produced in the fragmentation region or through resonance decays. Their detection relies on electromagnetic calorimetry.

| Energy Configuration | π⁰ Distribution |
|---------------------|-------------------|
| **5×41 GeV** | ![Pion0 Distance 5x41](/analysis/campaign-2025-08/acceptance_ff/bidim_pizero_distance_5x41.png) |
| **10×100 GeV** | ![Pion0 Distance 10x100](/analysis/campaign-2025-08/acceptance_ff/bidim_pizero_distance_10x100.png) |
| **10×130 GeV** | ![Pion0 Distance 10x130](/analysis/campaign-2025-08/acceptance_ff/bidim_pizero_distance_10x130.png) |
| **18×275 GeV** | ![Pion0 Distance 18x275](/analysis/campaign-2025-08/acceptance_ff/bidim_pizero_distance_18x275.png) |

## Detector-Specific Acceptance

The Far Forward region consists of multiple detector subsystems, each optimized for specific particle types and kinematic ranges. The following sections show polar acceptance plots for different particles in various detector components. These plots display the angular distribution of particle hits in a polar coordinate representation, providing insight into the geometric acceptance of each subsystem.


#### B0 Tracker

The B0 tracker provides tracking coverage close to the beam pipe in the forward direction, essential for detecting high-momentum particles at small angles.

| Energy Configuration | Polar Acceptance |
|---------------------|-------------------|
| **5×41 GeV** | ![Proton B0 5x41](/analysis/campaign-2025-08/acceptance_ff/proton_B0TrackerHits_5x41_polar_zoom.png) |
| **10×100 GeV** | ![Proton B0 10x100](/analysis/campaign-2025-08/acceptance_ff/proton_B0TrackerHits_10x100_polar_zoom.png) |
| **18×275 GeV** | ![Proton B0 18x275](/analysis/campaign-2025-08/acceptance_ff/proton_B0TrackerHits_18x275_polar_zoom.png) |


#### Forward Off-Momentum Tracker

The Forward Off-Momentum (OMD) tracker system captures particles scattered at small angles, including protons from Lambda decays that are slightly deflected from the beam direction.

| Energy Configuration | Polar Acceptance |
|---------------------|-------------------|
| **5×41 GeV** | ![Proton OMD 5x41](/analysis/campaign-2025-08/acceptance_ff/proton_ForwardOffMTrackerRecHits_5x41_polar_zoom.png) |
| **10×100 GeV** | ![Proton OMD 10x100](/analysis/campaign-2025-08/acceptance_ff/proton_ForwardOffMTrackerRecHits_10x100_polar_zoom.png) |
| **18×275 GeV** | ![Proton OMD 18x275](/analysis/campaign-2025-08/acceptance_ff/proton_ForwardOffMTrackerRecHits_18x275_polar_zoom.png) |


#### Forward Roman Pot

The Roman Pot detectors are specialized tracking stations positioned very close to the beam line, designed to detect forward protons at extremely small scattering angles.

| Energy Configuration | Polar Acceptance |
|---------------------|-------------------|
| **5×41 GeV** | ![Proton RomanPot 5x41](/analysis/campaign-2025-08/acceptance_ff/proton_ForwardRomanPotRecHits_5x41_polar_zoom.png) |
| **10×100 GeV** | ![Proton RomanPot 10x100](/analysis/campaign-2025-08/acceptance_ff/proton_ForwardRomanPotRecHits_10x100_polar_zoom.png) |
| **18×275 GeV** | ![Proton RomanPot 18x275](/analysis/campaign-2025-08/acceptance_ff/proton_ForwardRomanPotRecHits_18x275_polar_zoom.png) |


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

