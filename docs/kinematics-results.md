# Kinematics Analysis Results

This page demonstrates how to embed histograms throughout your documentation using the `JsonHistogram` component.

## Overview

The kinematics analysis examines the momentum distributions and angular correlations of particles in the EIC simulation. Below are key distributions from the 10×100 GeV beam configuration.

## Incident Particles

### Proton Beam

The incident proton beam shows the expected narrow momentum distribution centered at 100 GeV:

<JsonHistogram path="/analysis/campaign-2025-07/eg-kinematics/10x100/inc_p_p.json" />

The transverse momentum distribution is very narrow, indicating good beam collimation:

<JsonHistogram path="/analysis/campaign-2025-07/eg-kinematics/10x100/inc_p_pt.json" />

### Electron Beam

The 10 GeV electron beam shows similarly good collimation:

<JsonHistogram path="/analysis/campaign-2025-07/eg-kinematics/10x100/inc_e_p.json" />

Note the negative pz values, as the electron beam travels in the opposite direction:

<JsonHistogram path="/analysis/campaign-2025-07/eg-kinematics/10x100/inc_e_pz.json" />

## Scattered Particles

### Scattered Electron Kinematics

The scattered electron shows a broad momentum distribution:

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0;">
  <JsonHistogram 
    path="/analysis/campaign-2025-07/eg-kinematics/10x100/scat_e_p.json" 
    height="350px"
  />
  <JsonHistogram 
    path="/analysis/campaign-2025-07/eg-kinematics/10x100/scat_e_pt.json" 
    height="350px"
  />
</div>

The angular distributions provide insight into the scattering dynamics:

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0;">
  <JsonHistogram 
    path="/analysis/campaign-2025-07/eg-kinematics/10x100/scat_e_theta.json" 
    height="350px"
  />
  <JsonHistogram 
    path="/analysis/campaign-2025-07/eg-kinematics/10x100/scat_e_phi.json" 
    height="350px"
  />
</div>

### Kaon Production

The kaon momentum spectrum reflects the Sullivan process kinematics:

<JsonHistogram path="/analysis/campaign-2025-07/eg-kinematics/10x100/kaon_p.json" />

The pseudorapidity distribution shows the forward-going nature of the produced kaons:

<JsonHistogram path="/analysis/campaign-2025-07/eg-kinematics/10x100/kaon_eta.json" />

### Lambda Baryon

The Lambda baryon acts as a spectator in the Sullivan process, carrying most of the initial proton momentum:

<JsonHistogram path="/analysis/campaign-2025-07/eg-kinematics/10x100/lambda_p.json" />

The very small angle with the z-axis confirms its forward-going nature:

<JsonHistogram path="/analysis/campaign-2025-07/eg-kinematics/10x100/lambda_angle_z_mrad.json" />

## Summary

These distributions demonstrate the expected kinematics for the Sullivan process at the EIC:
- Well-collimated incident beams
- Broad scattered electron distributions
- Forward-going kaon production
- Lambda baryon as a spectator carrying most of the proton momentum

The `JsonHistogram` component makes it easy to embed these visualizations directly in the documentation, providing interactive exploration of the data alongside the physics interpretation.
