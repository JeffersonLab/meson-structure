<template>
  <div class="acceptance-viewer">
    <div class="global-controls">
      <label for="energy-mode-select">Display Mode:</label>
      <select id="energy-mode-select" v-model="globalEnergyMode" @change="updateGlobalMode">
        <option value="">-- Select display mode --</option>
        <option value="5x41">5×41</option>
        <option value="10x100">10×100</option>
        <option value="10x130">10×130</option>
        <option value="18x275">18×275</option>
        <option value="5x41_vs_10x100">5×41 vs 10×100</option>
        <option value="5x41_vs_18x275">5×41 vs 18×275</option>
        <option value="10x100_vs_10x130">10×100 vs 10×130</option>
        <option value="10x100_vs_18x275">10×100 vs 18×275</option>
        <option value="10x130_vs_18x275">10×130 vs 18×275</option>
      </select>
    </div>

    <div v-if="globalEnergyMode" class="info-message">
      All plots below will show: <strong>{{ getModeDescription(globalEnergyMode) }}</strong>
    </div>

    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import { ref, provide } from 'vue'

// Global energy mode with default
const globalEnergyMode = ref('5x41_vs_18x275')

// Provide to child components
provide('globalEnergyMode', globalEnergyMode)

// Update event for child components
function updateGlobalMode() {
  // This will trigger reactivity in child components
}

// Get human-readable description
function getModeDescription(mode: string): string {
  const descriptions: Record<string, string> = {
    '5x41': '5×41 GeV',
    '10x100': '10×100 GeV',
    '10x130': '10×130 GeV',
    '18x275': '18×275 GeV',
    '5x41_vs_10x100': '5×41 vs 10×100 GeV',
    '5x41_vs_18x275': '5×41 vs 18×275 GeV',
    '10x100_vs_10x130': '10×100 vs 10×130 GeV',
    '10x100_vs_18x275': '10×100 vs 18×275 GeV',
    '10x130_vs_18x275': '10×130 vs 18×275 GeV'
  }
  return descriptions[mode] || mode
}
</script>

<style scoped>
.acceptance-viewer {
  margin: 2rem 0;
}

.global-controls {
  position: sticky;
  top: var(--vp-nav-height);
  z-index: 10;
  padding: 1rem;
  margin-bottom: 2rem;
  background-color: var(--vp-c-bg-soft);
  border: 2px solid var(--vp-c-brand);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.global-controls label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  font-size: 16px;
  color: var(--vp-c-text-1);
}

.global-controls select {
  width: 100%;
  max-width: 500px;
  padding: 0.75rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 4px;
  background-color: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 15px;
  cursor: pointer;
  transition: all 0.2s;
}

.global-controls select:hover {
  border-color: var(--vp-c-brand);
}

.global-controls select:focus {
  outline: none;
  border-color: var(--vp-c-brand);
  box-shadow: 0 0 0 3px var(--vp-c-brand-soft);
}

.info-message {
  padding: 0.75rem 1rem;
  margin-bottom: 1.5rem;
  background-color: var(--vp-c-brand-soft);
  border-left: 4px solid var(--vp-c-brand);
  border-radius: 4px;
  color: var(--vp-c-text-1);
}

/* Dark mode adjustments */
.dark .global-controls {
  background-color: var(--vp-c-bg-elv);
}

.dark .global-controls select {
  background-color: var(--vp-c-bg-elv);
}

/* Responsive design */
@media (max-width: 768px) {
  .global-controls {
    padding: 0.75rem;
  }

  .global-controls label {
    font-size: 14px;
  }

  .global-controls select {
    font-size: 14px;
  }
}
</style>
