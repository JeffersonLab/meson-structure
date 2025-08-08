# EIC Event Generator Kinematics

<script setup>
import { ref, computed } from 'vue'

const energy = ref('10x100')
const path = '/analysis/campaign-2025-07/eg-kinematics'

const energyLabel = computed(() => {
  const labels = {
    '10x100': '10×100 GeV',
    '10x130': '10×130 GeV',
    '18x275': '18×275 GeV',
    '5x41': '5×41 GeV'
  }
  return labels[energy.value]
})
</script>

<div style="margin: 1em 0;">
  <strong>Select beam energy:</strong>
  <select v-model="energy" style="margin-left: 0.5em; padding: 0.3em;">
    <option value="10x100">10×100 GeV</option>
    <option value="10x130">10×130 GeV</option>
    <option value="18x275">18×275 GeV</option>
    <option value="5x41">5×41 GeV</option>
  </select>
</div>

Analysis of generated events for electron-proton collisions at {{ energyLabel }} beam energy configuration.
Generated with the Sullivan process for K⁺Λ production.

---

## Incident Proton

The incident proton beam particles

| px | py | pz |
|:--:|:--:|:--:|
| ![px]({{ `${path}/${energy}/inc_p_px.png` }}) | ![py]({{ `${path}/${energy}/inc_p_py.png` }}) | ![pz]({{ `${path}/${energy}/inc_p_pz.png` }}) |

| pT | p | angular |
|:--:|:--:|:--:|
| ![pT]({{ `${path}/${energy}/inc_p_pt.png` }}) | ![p]({{ `${path}/${energy}/inc_p_p.png` }}) | ![angle]({{ `${path}/${energy}/inc_p_angle_z_mrad.png` }}) |

---

## Incident Electron

The incident electron beam (traveling in -z direction).

### Momentum Components

| px | py |
|:--:|:--:|
| ![px]({{ `${path}/${energy}/inc_e_px.png` }}) | ![py]({{ `${path}/${energy}/inc_e_py.png` }}) |

| pT | pz | p |
|:--:|:--:|:--:|
| ![pT]({{ `${path}/${energy}/inc_e_pt.png` }}) | ![pz]({{ `${path}/${energy}/inc_e_pz.png` }}) | ![p]({{ `${path}/${energy}/inc_e_p.png` }}) |

### Angular Distribution

| Minimal angle with Z-axis |
|:-------------------------:|
| ![angle]({{ `${path}/${energy}/inc_e_angle_z_mrad.png` }}) |

---

## Scattered Electron

The electron after DIS interaction.

### Momentum Distributions

| pT | pz | p |
|:--:|:--:|:--:|
| ![pT]({{ `${path}/${energy}/scat_e_pt.png` }}) | ![pz]({{ `${path}/${energy}/scat_e_pz.png` }}) | ![p]({{ `${path}/${energy}/scat_e_p.png` }}) |

### Angular Distributions

| θ (polar angle) | η (pseudorapidity) |
|:---------------:|:------------------:|
| ![theta]({{ `${path}/${energy}/scat_e_theta.png` }}) | ![eta]({{ `${path}/${energy}/scat_e_eta.png` }}) |

| φ (azimuthal angle) |
|:-------------------:|
| ![phi]({{ `${path}/${energy}/scat_e_phi.png` }}) |

---

## Scattered Kaon

The produced K⁺ meson from the Sullivan process.

### Momentum Distributions

| pT | pz | p |
|:--:|:--:|:--:|
| ![pT]({{ `${path}/${energy}/kaon_pt.png` }}) | ![pz]({{ `${path}/${energy}/kaon_pz.png` }}) | ![p]({{ `${path}/${energy}/kaon_p.png` }}) |

### Angular Distributions

| θ (polar angle) | η (pseudorapidity) |
|:---------------:|:------------------:|
| ![theta]({{ `${path}/${energy}/kaon_theta.png` }}) | ![eta]({{ `${path}/${energy}/kaon_eta.png` }}) |

| φ (azimuthal angle) |
|:-------------------:|
| ![phi]({{ `${path}/${energy}/kaon_phi.png` }}) |

---

## Spectator Lambda

The Λ baryon acting as the spectator in the Sullivan process, carrying most of the initial proton momentum.

### Momentum Components

| px | py |
|:--:|:--:|
| ![px]({{ `${path}/${energy}/lambda_px.png` }}) | ![py]({{ `${path}/${energy}/lambda_py.png` }}) |

| pT | pz | p |
|:--:|:--:|:--:|
| ![pT]({{ `${path}/${energy}/lambda_pt.png` }}) | ![pz]({{ `${path}/${energy}/lambda_pz.png` }}) | ![p]({{ `${path}/${energy}/lambda_p.png` }}) |

### Angular Distribution

| Minimal angle with Z-axis |
|:-------------------------:|
| ![angle]({{ `${path}/${energy}/lambda_angle_z_mrad.png` }}) |

---

## Summary

This analysis shows the kinematic distributions for the Sullivan process e + p → e' + K⁺ + Λ at {{ energyLabel }}:

- **Incident particles**: Show narrow momentum distributions centered around beam energies
- **Scattered electron**: Exhibits broad kinematic range typical of DIS
- **Kaon**: Produced meson with significant transverse momentum
- **Lambda**: Spectator baryon carrying most of the initial proton momentum

The distributions confirm the expected kinematics for meson structure studies at the EIC.