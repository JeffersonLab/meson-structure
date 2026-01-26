<template>
  <div class="compare-plot">
    <h3 v-if="title">{{ title }}</h3>
    <p v-if="description" class="description">{{ description }}</p>

    <div class="plot-controls">
      <label :for="'source-select-' + plotId">Select:</label>
      <select
        :id="'source-select-' + plotId"
        v-model="localMode"
        @change="loadImages"
      >
        <option value="">-- Select --</option>
        <optgroup label="Single">
          <option v-for="key in sourceKeys" :key="key" :value="key">
            {{ formatLabel(key) }}
          </option>
        </optgroup>
        <optgroup label="Comparisons">
          <option v-for="comp in comparisons" :key="comp.value" :value="comp.value">
            {{ comp.label }}
          </option>
        </optgroup>
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

    <div v-else-if="localMode" class="no-data">
      No plot available for selected option
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

// Inject sources and global mode from parent
const plotSources = inject<Record<string, string>>('plotSources', {})
const globalSelectedMode = inject<any>('globalSelectedMode', ref(''))

// Extract keys from sources
const sourceKeys = computed(() => Object.keys(plotSources))

// Generate all pairwise comparisons
const comparisons = computed(() => {
  const keys = sourceKeys.value
  const result: { value: string; label: string }[] = []

  for (let i = 0; i < keys.length; i++) {
    for (let j = i + 1; j < keys.length; j++) {
      const key1 = keys[i]
      const key2 = keys[j]
      result.push({
        value: `${key1}_vs_${key2}`,
        label: `${formatLabel(key1)} vs ${formatLabel(key2)}`
      })
    }
  }

  return result
})

// Local mode (synced with global but can be overridden)
const localMode = ref('')

// Current images to display
interface PlotImage {
  src: string
  alt: string
  label?: string
}

const currentImages = ref<PlotImage[]>([])

// Watch global mode changes
watch(globalSelectedMode, (newMode) => {
  if (newMode) {
    localMode.value = newMode
    loadImages()
  }
})

// Watch local mode changes
watch(localMode, () => {
  loadImages()
})

// Format label for display (just return the key as-is)
function formatLabel(key: string): string {
  return key
}

// Build image path from source key
function buildImagePath(key: string): string {
  const basePath = plotSources[key] || ''
  // Ensure path ends with / and combine with plotName
  const normalizedPath = basePath.endsWith('/') ? basePath : basePath + '/'
  return withBase(normalizedPath + props.plotName)
}

// Load images based on selected mode
function loadImages() {
  if (!localMode.value) {
    currentImages.value = []
    return
  }

  const mode = localMode.value
  const images: PlotImage[] = []

  if (mode.includes('_vs_')) {
    // Comparison mode: show two plots
    const [key1, key2] = mode.split('_vs_')

    if (plotSources[key1]) {
      images.push({
        src: buildImagePath(key1),
        alt: `${props.title || props.plotName} - ${key1}`,
        label: formatLabel(key1)
      })
    }

    if (plotSources[key2]) {
      images.push({
        src: buildImagePath(key2),
        alt: `${props.title || props.plotName} - ${key2}`,
        label: formatLabel(key2)
      })
    }
  } else {
    // Single mode
    if (plotSources[mode]) {
      images.push({
        src: buildImagePath(mode),
        alt: `${props.title || props.plotName} - ${mode}`,
        label: undefined
      })
    }
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
  if (globalSelectedMode.value) {
    localMode.value = globalSelectedMode.value
    loadImages()
  }
})
</script>

<style scoped>
.compare-plot {
  margin: 2rem 0;
  padding: 0.75rem;
  background-color: var(--vp-c-bg-soft);
  border-radius: 8px;
  border: 1px solid var(--vp-c-divider);
}

.compare-plot h3 {
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
.dark .compare-plot {
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
  .compare-plot {
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
