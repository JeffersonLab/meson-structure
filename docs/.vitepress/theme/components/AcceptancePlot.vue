<template>
  <div class="acceptance-plot">
    <h3 v-if="title">{{ title }}</h3>
    <p v-if="description" class="description">{{ description }}</p>

    <div class="plot-controls">
      <label :for="'energy-select-' + plotId">Energy Mode:</label>
      <select 
        :id="'energy-select-' + plotId" 
        v-model="localEnergyMode" 
        @change="loadImages"
      >
        <option value="">-- Select energy mode --</option>
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

    <div v-if="currentImages.length > 0" class="images-container">
      <div 
        v-for="(img, index) in currentImages" 
        :key="index" 
        class="image-wrapper"
      >
        <h4 v-if="img.label" class="image-label">{{ img.label }}</h4>
        <img 
          :src="img.src" 
          :alt="img.alt"
          @error="handleImageError"
          class="plot-image"
          data-zoomable
        />
      </div>
    </div>

    <div v-else-if="localEnergyMode" class="no-data">
      No plot available for selected energy mode
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, inject, onMounted } from 'vue'
import { withBase } from 'vitepress'

// Props
const props = defineProps<{
  plotName: string
  title?: string
  description?: string
}>()

// Unique ID for this plot instance
const plotId = Math.random().toString(36).substr(2, 9)

// Inject global energy mode
const globalEnergyMode = inject<any>('globalEnergyMode', ref(''))

// Local energy mode (can be overridden by user)
const localEnergyMode = ref('')

// Current images to display
interface PlotImage {
  src: string
  alt: string
  label?: string
}

const currentImages = ref<PlotImage[]>([])

// Watch global mode changes
watch(globalEnergyMode, (newMode) => {
  if (newMode) {
    localEnergyMode.value = newMode
    loadImages()
  }
})

// Watch local mode changes
watch(localEnergyMode, () => {
  loadImages()
})

// Load images based on selected mode
function loadImages() {
  if (!localEnergyMode.value) {
    currentImages.value = []
    return
  }

  const mode = localEnergyMode.value
  const images: PlotImage[] = []

  if (mode.includes('_vs_')) {
    // Comparison mode: show two plots
    const [energy1, energy2] = mode.split('_vs_')

    images.push({
      src: withBase(`/analysis/campaign-2025-08/acceptance/${energy1}/${props.plotName}`),
      alt: `${props.title || props.plotName} - ${energy1}`,
      label: `${energy1.replace('x', '×')} GeV`
    })

    images.push({
      src: withBase(`/analysis/campaign-2025-08/acceptance/${energy2}/${props.plotName}`),
      alt: `${props.title || props.plotName} - ${energy2}`,
      label: `${energy2.replace('x', '×')} GeV`
    })
  } else {
    // Single energy mode
    images.push({
      src: withBase(`/analysis/campaign-2025-08/acceptance/${mode}/${props.plotName}`),
      alt: `${props.title || props.plotName} - ${mode}`,
      label: undefined
    })
  }

  currentImages.value = images
}

// Handle image loading errors
function handleImageError(event: Event) {
  const img = event.target as HTMLImageElement
  console.warn(`Failed to load image: ${img.src}`)
}

// Initialize on mount
onMounted(() => {
  if (globalEnergyMode.value) {
    localEnergyMode.value = globalEnergyMode.value
    loadImages()
  }
})
</script>

<style scoped>
.acceptance-plot {
  margin: 2rem 0;
  padding: 0.75rem;
  background-color: var(--vp-c-bg-soft);
  border-radius: 8px;
  border: 1px solid var(--vp-c-divider);
}

.acceptance-plot h3 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: var(--vp-c-text-1);
}

.description {
  margin-bottom: 0.75rem;
  color: var(--vp-c-text-2);
  font-size: 14px;
}

.plot-controls {
  margin-bottom: 1rem;
  padding: 0.5rem;
  background-color: var(--vp-c-bg);
  border-radius: 4px;
  border: 1px solid var(--vp-c-divider);
}

.plot-controls label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  font-size: 14px;
}

.plot-controls select {
  width: 100%;
  max-width: 400px;
  padding: 0.5rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 4px;
  background-color: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 14px;
  cursor: pointer;
}

.plot-controls select:hover {
  border-color: var(--vp-c-brand);
}

.plot-controls select:focus {
  outline: none;
  border-color: var(--vp-c-brand);
  box-shadow: 0 0 0 2px var(--vp-c-brand-soft);
}

.images-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.image-wrapper {
  text-align: center;
}

.image-label {
  margin-bottom: 0.5rem;
  font-size: 16px;
  font-weight: 600;
  color: var(--vp-c-brand);
}

.plot-image {
  width: 100%;
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  border: 1px solid var(--vp-c-divider);
  background-color: var(--vp-c-bg);
  cursor: zoom-in;
}

.no-data {
  padding: 2rem;
  text-align: center;
  color: var(--vp-c-text-2);
  font-style: italic;
}

/* Dark mode adjustments */
.dark .acceptance-plot {
  background-color: var(--vp-c-bg-elv);
}

.dark .plot-controls {
  background-color: var(--vp-c-bg-soft);
}

.dark .plot-controls select {
  background-color: var(--vp-c-bg-elv);
}

/* Responsive design */
@media (max-width: 768px) {
  .acceptance-plot {
    padding: 0.5rem;
  }

  .plot-controls {
    padding: 0.5rem;
  }

  .image-label {
    font-size: 14px;
  }
}
</style>
