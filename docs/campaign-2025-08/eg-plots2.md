# EIC Event Generator Kinematics

<script setup>
import { ref, computed } from 'vue'

// Available energy configurations
const energyConfigs = [
  { label: '10×100 GeV', value: '10x100', electron: 10, proton: 100 },
  { label: '10×130 GeV', value: '10x130', electron: 10, proton: 130 },
  { label: '18×275 GeV', value: '18x275', electron: 18, proton: 275 },
  { label: '5×41 GeV', value: '5x41', electron: 5, proton: 41 }
]

// Selected energy
const selectedEnergy = ref('10x100')

// Get current config
const currentConfig = computed(() => 
  energyConfigs.find(c => c.value === selectedEnergy.value)
)

// Base path for images
const imagePath = computed(() => 
  `/analysis/campaign-2025-07/eg-kinematics/${selectedEnergy.value}`
)

// Helper function to get full image path
const img = (filename) => `${imagePath.value}/${filename}.png`
</script>

<style scoped>
.energy-selector {
  background: var(--vp-c-bg-soft);
  padding: 16px;
  border-radius: 8px;
  margin: 20px 0;
}

.energy-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.energy-btn {
  padding: 10px 20px;
  border: 2px solid var(--vp-c-brand);
  background: var(--vp-c-bg);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
  font-size: 14px;
}

.energy-btn:hover {
  background: var(--vp-c-brand-soft);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.energy-btn.active {
  background: var(--vp-c-brand);
  color: white;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.config-info {
  margin-top: 12px;
  padding: 12px;
  background: var(--vp-c-bg-alt);
  border-radius: 6px;
  font-size: 0.95em;
}

.plot-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.plot-grid-3 {
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

.plot-item {
  text-align: center;
}

.plot-item img {
  width: 100%;
  height: auto;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.plot-item h4 {
  margin: 10px 0 5px 0;
  font-size: 0.9em;
  color: var(--vp-c-text-2);
}
</style>

<div class="energy-selector">
  <h3>🔄 Select Beam Energy Configuration</h3>
  <div class="energy-buttons">
    <!-- These render as 4 clickable buttons: [10×100 GeV] [10×130 GeV] [18×275 GeV] [5×41 GeV] -->
    <button 
      v-for="config in energyConfigs" 
      :key="config.value"
      :class="['energy-btn', { active: selectedEnergy === config.value }]"
      @click="selectedEnergy = config.value"
    >
      {{ config.label }}
    </button>
  </div>
  <div class="config-info">
    <strong>Currently viewing:</strong> {{ currentConfig.label }} 
    ({{ currentConfig.electron }} GeV electron × {{ currentConfig.proton }} GeV proton)
  </div>
</div>

Analysis of generated events for electron-proton collisions at {{ currentConfig.label }} beam energy configuration.
Generated with the Sullivan process for K⁺Λ production.

---

## Incident Proton

The incident proton beam particles

<div class="plot-grid-3">
  <div class="plot-item">
    <h4>px</h4>
    <img :src="img('inc_p_px')" :alt="`px for ${currentConfig.label}`" />
  </div>
  <div class="plot-item">
    <h4>py</h4>
    <img :src="img('inc_p_py')" :alt="`py for ${currentConfig.label}`" />
  </div>
  <div class="plot-item">
    <h4>pz</h4>
    <img :src="img('inc_p_pz')" :alt="`pz for ${currentConfig.label}`" />
  </div>
</div>

<div class="plot-grid-3">
  <div class="plot-item">
    <h4>pT</h4>
    <img :src="img('inc_p_pt')" :alt="`pT for ${currentConfig.label}`" />
  </div>
  <div class="plot-item">
    <h4>p</h4>
    <img :src="img('inc_p_p')" :alt="`p for ${currentConfig.label}`" />
  </div>
  <div class="plot-item">
    <h4>Angle with Z-axis</h4>
    <img :src="img('inc_p_angle_z_mrad')" :alt="`angle for ${currentConfig.label}`" />
  </div>
</div>

---

## Incident Electron

The incident electron beam with nominal energy of {{ currentConfig.electron }} GeV (traveling in -z direction).

### Momentum Components

<div class="plot-grid">
  <div class="plot-item">
    <h4>px</h4>
    <img :src="img('inc_e_px')" :alt="`px for ${currentConfig.label}`" />
  </div>
  <div class="plot-item">
    <h4>py</h4>
    <img :src="img('inc_e_py')" :alt="`py for ${currentConfig.label}`" />
  </div>
</div>

<div class="plot-grid-3">
  <div class="plot-item">
    <h4>pT</h4>
    <img :src="img('inc_e_pt')" :alt="`pT for ${currentConfig.label}`" />
  </div>
  <div class="plot-item">
    <h4>pz</h4>
    <img :src="img('inc_e_pz')" :alt="`pz for ${currentConfig.label}`" />
  </div>
  <div class="plot-item">
    <h4>p</h4>
    <img :src="img('inc_e_p')" :alt="`p for ${currentConfig.label}`" />
  </div>
</div>

### Angular Distribution

<div class="plot-grid">
  <div class="plot-item">
    <h4>Minimal angle with Z-axis</h4>
    <img :src="img('inc_e_angle_z_mrad')" :alt="`angle for ${currentConfig.label}`" />
  </div>
</div>

---

## Scattered Electron

The electron after DIS interaction.

### Momentum Distributions

<div class="plot-grid-3">
  <div class="plot-item">
    <h4>pT</h4>
    <img :src="img('scat_e_pt')" :alt="`pT for ${currentConfig.label}`" />
  </div>
  <div class="plot-item">
    <h4>pz</h4>
    <img :src="img('scat_e_pz')" :alt="`pz for ${currentConfig.label}`" />
  </div>
  <div class="plot-item">
    <h4>p</h4>
    <img :src="img('scat_e_p')" :alt="`p for ${currentConfig.label}`" />
  </div>
</div>

### Angular Distributions

<div class="plot-grid">
  <div class="plot-item">
    <h4>θ (polar angle)</h4>
    <img :src="img('scat_e_theta')" :alt="`theta for ${currentConfig.label}`" />
  </div>
  <div class="plot-item">
    <h4>η (pseudorapidity)</h4>
    <img :src="img('scat_e_eta')" :alt="`eta for ${currentConfig.label}`" />
  </div>
</div>

<div class="plot-grid">
  <div class="plot-item">
    <h4>φ (azimuthal angle)</h4>
    <img :src="img('scat_e_phi')" :alt="`phi for ${currentConfig.label}`" />
  </div>
</div>

---

## Scattered Kaon

The produced K⁺ meson from the Sullivan process.

### Momentum Distributions

<div class="plot-grid-3">
  <div class="plot-item">
    <h4>pT</h4>
    <img :src="img('kaon_pt')" :alt="`pT for ${currentConfig.label}`" />
  </div>
  <div class="plot-item">
    <h4>pz</h4>
    <img :src="img('kaon_pz')" :alt="`pz for ${currentConfig.label}`" />
  </div>
  <div class="plot-item">
    <h4>p</h4>
    <img :src="img('kaon_p')" :alt="`p for ${currentConfig.label}`" />
  </div>
</div>

### Angular Distributions

<div class="plot-grid">
  <div class="plot-item">
    <h4>θ (polar angle)</h4>
    <img :src="img('kaon_theta')" :alt="`theta for ${currentConfig.label}`" />
  </div>
  <div class="plot-item">
    <h4>η (pseudorapidity)</h4>
    <img :src="img('kaon_eta')" :alt="`eta for ${currentConfig.label}`" />
  </div>
</div>

<div class="plot-grid">
  <div class="plot-item">
    <h4>φ (azimuthal angle)</h4>
    <img :src="img('kaon_phi')" :alt="`phi for ${currentConfig.label}`" />
  </div>
</div>

---

## Spectator Lambda

The Λ baryon acting as the spectator in the Sullivan process, carrying most of the initial proton momentum.

### Momentum Components

<div class="plot-grid">
  <div class="plot-item">
    <h4>px</h4>
    <img :src="img('lambda_px')" :alt="`px for ${currentConfig.label}`" />
  </div>
  <div class="plot-item">
    <h4>py</h4>
    <img :src="img('lambda_py')" :alt="`py for ${currentConfig.label}`" />
  </div>
</div>

<div class="plot-grid-3">
  <div class="plot-item">
    <h4>pT</h4>
    <img :src="img('lambda_pt')" :alt="`pT for ${currentConfig.label}`" />
  </div>
  <div class="plot-item">
    <h4>pz</h4>
    <img :src="img('lambda_pz')" :alt="`pz for ${currentConfig.label}`" />
  </div>
  <div class="plot-item">
    <h4>p</h4>
    <img :src="img('lambda_p')" :alt="`p for ${currentConfig.label}`" />
  </div>
</div>

### Angular Distribution

<div class="plot-grid">
  <div class="plot-item">
    <h4>Minimal angle with Z-axis</h4>
    <img :src="img('lambda_angle_z_mrad')" :alt="`angle for ${currentConfig.label}`" />
  </div>
</div>

---

## Summary

This analysis shows the kinematic distributions for the Sullivan process e + p → e' + K⁺ + Λ at {{ currentConfig.label }}:

- **Incident particles**: Show narrow momentum distributions centered around beam energies
- **Scattered electron**: Exhibits broad kinematic range typical of DIS
- **Kaon**: Produced meson with significant transverse momentum
- **Lambda**: Spectator baryon carrying most of the initial proton momentum (~{{ Math.round(currentConfig.proton * 0.95) }}-{{ currentConfig.proton }} GeV)

The distributions confirm the expected kinematics for meson structure studies at the EIC.