# Meson Structure Function Working Group

The **Meson Structure Function Working Group (MSF-WG)** investigates the feasibility of pion and kaon structure-function measurements at the future Electron–Ion Collider (EIC) using the ePIC detector. This repository provides simulation tools and analysis codes developed within the working group.

**Documentation, results, and presentations:** [Meson Structure Working Group website](https://jeffersonlab.github.io/meson-structure/)

## Physics motivation

Understanding the internal structure of hadrons is essential to investigating the emergence of hadronic mass. While proton and neutron structure functions have been extensively studied, experimental information on pion and kaon structure remains limited. Existing measurements rely primarily on Drell–Yan experiments at CERN and Fermilab, and leading-neutron deep-inelastic scattering (DIS) at HERA. The EIC will provide new opportunities to constrain pion and kaon parton distributions over a broad kinematic range.

## Experimental strategy: the Sullivan process

The Sullivan process provides indirect access to meson structure through electron scattering from the virtual meson cloud surrounding the proton. In semi-inclusive DIS, the exchanged virtual photon probes a meson emitted by the proton, while the accompanying baryon is detected in the far-forward region.

Two channels are investigated:

**Pion exchange with forward-neutron tagging**

$$
e + p \rightarrow e' + n + X
$$

**Kaon exchange with forward-$\Lambda$ tagging**

$$
e + p \rightarrow e' + \Lambda^0 + X
$$

The scattered electron (e') and forward baryon are used to reconstruct the kinematic variables: $x_B$, $Q^2$, $x_L$, $t$, etc.

Theoretical studies identify kinematic regions where the Sullivan mechanism can provide a controlled interpretation of meson structure:
- $-t \lesssim 0.6$ $\mathrm{GeV}^2$ for pion exchange, 
- $-t \lesssim 0.9$ $\mathrm{GeV}^2$ for kaon exchange.

## Simulation and analysis workflow

The analysis framework follows five main steps:

1. **Event generator (SURGE)**  
   Generate Sullivan-process events and differential cross sections for the pion–neutron and kaon–$\Lambda$ channels.

2. **Detector simulation (Geant4)**  
   Simulate particle transport and detector response using the ePIC simulation framework.

3. **Event reconstruction (EICrecon)**  
   Reconstruct forward baryons, scattered electrons, and DIS kinematic observables using ePIC detector information.

4. **Uncertainty quantification**  
   Evaluate reconstruction efficiencies, expected event yields, statistical uncertainties, and background contamination.

5. **Structure-function projections**  
   Estimate the impact of future EIC measurements on pion and kaon structure ufor state-of-the-art models and calculations.

## Post-analysis

The repository provides two post-analysis frameworks:

| Channel | Description | Documentation |
|---|---|---|
| **Pion–neutron** | Forward-neutron reconstruction, detector performance, background studies, and pion structure-function projections | [Pion–neutron analysis](analysis/pion-neutron/README.md) |
| **Kaon–Lambda** | Reconstruction of \(\Lambda \to n\pi^0 \to n\gamma\gamma\), detector performance, background studies, and kaon structure-function projections | [Kaon–Lambda analysis](analysis/kaon-lambda/README.md) |

For installation, configuration, and usage instructions, see the corresponding channel README or the [analysis overview](analysis/README.md).

## EIC/ePIC software contributions

The working group contributes to the development and improvement of the ePIC simulation and reconstruction software:

- **Sullivan-process event generator:** [SURGE](https://github.com/JeffersonLab/eic_mesonsf_generator)
- **Multi-calorimeter $\Lambda$ reconstruction**, combining ZDC, B0, and LFHCAL information: [EICrecon PR #2622](https://github.com/eic/EICrecon/pull/2622)
- **HEXPLIT algorithm improvements and fixes:** [PR #2980](https://github.com/eic/EICrecon/pull/2980), [PR #3061](https://github.com/eic/EICrecon/pull/3061)
- **Calorimeter calibration** (EndcapP, LFHCAL, B0): [PR #2622](https://github.com/eic/EICrecon/pull/2622)
- **Clustering for ZDC cartesian tales:** [PR #3064](https://github.com/eic/EICrecon/pull/3064)

## Current status and outlook

**Implemented**

- Sullivan-process event generation for pion and kaon channels using SURGE.
- $\Lambda$ reconstruction through $\Lambda \to n\pi^0 \to n\gamma\gamma$, using ZDC, B0, and LFHCAL information.
- Forward-neutron reconstruction using the ZDC.
- Post-analysis tools for detector performance and event reconstruction.
- Statistical uncertainty projections and comparisons with models (JAM, DSE).
- Exploratory background contamination studies.

**Ongoing and planned developments**

- $\Lambda$ reconstruction through $\Lambda \to p\pi^-$ using B0, RP and OM.
- More realistic time-dependent treatment of signal/background interactions.
- Evaluation of sensitivity to event-generator assumptions.

The ultimate objective is to establish reliable experimental strategies for pion and kaon structure measurements with ePIC, from early EIC operation to design luminosity.