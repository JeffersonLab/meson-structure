<template>
  <div class="compare-viewer">
    <div class="global-controls">
      <label for="source-select">Display Mode:</label>
      <select id="source-select" v-model="selectedMode" @change="onModeChange">
        <option value="">-- Select display mode --</option>
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

    <div v-if="selectedMode" class="info-message">
      All plots below will show: <strong>{{ getModeDescription(selectedMode) }}</strong>
    </div>

    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, provide, onMounted } from 'vue'

// Props - sources is a Record<label, basePath>, defaultMode is optional
const props = defineProps<{
  sources: Record<string, string>
  defaultMode?: string
}>()

// Extract keys from sources
const sourceKeys = computed(() => Object.keys(props.sources))

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

// Check if a mode value is valid (exists in sources or comparisons)
function isValidMode(mode: string): boolean {
  if (!mode) return false
  // Check if it's a single source
  if (sourceKeys.value.includes(mode)) return true
  // Check if it's a valid comparison
  return comparisons.value.some(c => c.value === mode)
}

// Get mode from URL query parameter
function getModeFromUrl(): string | null {
  if (typeof window === 'undefined') return null
  const params = new URLSearchParams(window.location.search)
  return params.get('mode')
}

// Update URL query parameter without page reload
function updateUrlParam(mode: string) {
  if (typeof window === 'undefined') return

  const url = new URL(window.location.href)
  if (mode) {
    url.searchParams.set('mode', mode)
  } else {
    url.searchParams.delete('mode')
  }

  // Update URL without reloading
  window.history.replaceState({}, '', url.toString())
}

// Get default mode (prop > first comparison > first single)
function getDefaultMode(): string {
  // Use defaultMode prop if provided and valid
  if (props.defaultMode && isValidMode(props.defaultMode)) {
    return props.defaultMode
  }
  // Fall back to first comparison or first single
  if (comparisons.value.length > 0) {
    return comparisons.value[0].value
  }
  if (sourceKeys.value.length > 0) {
    return sourceKeys.value[0]
  }
  return ''
}

// Initialize with default mode (will be updated on mount if URL has mode)
const selectedMode = ref(getDefaultMode())

// Provide sources and selected mode to child components
provide('plotSources', props.sources)
provide('globalSelectedMode', selectedMode)

// Handle mode change from dropdown
function onModeChange() {
  updateUrlParam(selectedMode.value)
}

// Format label for display (just return the key as-is)
function formatLabel(key: string): string {
  return key
}

// Get human-readable description for current mode
function getModeDescription(mode: string): string {
  if (mode.includes('_vs_')) {
    const [key1, key2] = mode.split('_vs_')
    return `${formatLabel(key1)} vs ${formatLabel(key2)}`
  }
  return formatLabel(mode)
}

// On mount (client-side only), check URL and sync
onMounted(() => {
  const urlMode = getModeFromUrl()
  if (urlMode && isValidMode(urlMode)) {
    // URL has a valid mode, use it
    selectedMode.value = urlMode
  } else {
    // No URL mode, set it to current selection
    updateUrlParam(selectedMode.value)
  }
})
</script>

<style scoped>
.compare-viewer {
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
