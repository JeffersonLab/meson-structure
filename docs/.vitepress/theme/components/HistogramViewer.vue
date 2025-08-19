<template>
  <div class="histogram-viewer">
    <div class="controls">
      <label for="histogram-select">Select Histogram:</label>
      <select id="histogram-select" v-model="selectedHistogram" @change="loadHistogram">
        <option value="">-- Select a histogram --</option>
        <optgroup v-for="(histograms, particle) in groupedHistograms" :key="particle" :label="particleNames[particle]">
          <option v-for="histogram in histograms" :key="histogram.file" :value="histogram.file">
            {{ histogram.variable }}
          </option>
        </optgroup>
      </select>
    </div>

    <div v-if="currentHistogram" class="stats">
      <span class="stat-item">
        <strong>Entries:</strong> {{ currentHistogram.stats.entries.toLocaleString() }}
      </span>
      <span class="stat-item">
        <strong>Mean:</strong> {{ currentHistogram.stats.mean.toFixed(3) }}
      </span>
      <span class="stat-item">
        <strong>Std Dev:</strong> {{ currentHistogram.stats.std.toFixed(3) }}
      </span>
    </div>

    <div ref="chartContainer" class="chart-container"></div>

    <div v-if="loading" class="loading">Loading histogram...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import * as echarts from 'echarts'
import { withBase } from 'vitepress'

// Props
const props = defineProps<{
  basePath: string
  energy?: string
}>()

// Refs
const chartContainer = ref<HTMLElement>()
const selectedHistogram = ref('')
const currentHistogram = ref<any>(null)
const loading = ref(false)
const error = ref('')
let chartInstance: echarts.ECharts | null = null

// Particle display names
const particleNames = {
  'inc_p': 'Incident Proton',
  'inc_e': 'Incident Electron',
  'scat_e': 'Scattered Electron',
  'kaon': 'Kaon',
  'lambda': 'Lambda'
}

// Available histograms configuration
const availableHistograms = [
  // Incident Proton
  { particle: 'inc_p', variable: 'pt', file: 'inc_p_pt.json' },
  { particle: 'inc_p', variable: 'px', file: 'inc_p_px.json' },
  { particle: 'inc_p', variable: 'py', file: 'inc_p_py.json' },
  { particle: 'inc_p', variable: 'pz', file: 'inc_p_pz.json' },
  { particle: 'inc_p', variable: 'p', file: 'inc_p_p.json' },
  { particle: 'inc_p', variable: 'angle_z_mrad', file: 'inc_p_angle_z_mrad.json' },
  
  // Incident Electron
  { particle: 'inc_e', variable: 'pt', file: 'inc_e_pt.json' },
  { particle: 'inc_e', variable: 'px', file: 'inc_e_px.json' },
  { particle: 'inc_e', variable: 'py', file: 'inc_e_py.json' },
  { particle: 'inc_e', variable: 'pz', file: 'inc_e_pz.json' },
  { particle: 'inc_e', variable: 'p', file: 'inc_e_p.json' },
  { particle: 'inc_e', variable: 'angle_z_mrad', file: 'inc_e_angle_z_mrad.json' },
  
  // Scattered Electron
  { particle: 'scat_e', variable: 'pt', file: 'scat_e_pt.json' },
  { particle: 'scat_e', variable: 'pz', file: 'scat_e_pz.json' },
  { particle: 'scat_e', variable: 'p', file: 'scat_e_p.json' },
  { particle: 'scat_e', variable: 'theta', file: 'scat_e_theta.json' },
  { particle: 'scat_e', variable: 'phi', file: 'scat_e_phi.json' },
  { particle: 'scat_e', variable: 'eta', file: 'scat_e_eta.json' },
  
  // Kaon
  { particle: 'kaon', variable: 'pt', file: 'kaon_pt.json' },
  { particle: 'kaon', variable: 'pz', file: 'kaon_pz.json' },
  { particle: 'kaon', variable: 'p', file: 'kaon_p.json' },
  { particle: 'kaon', variable: 'theta', file: 'kaon_theta.json' },
  { particle: 'kaon', variable: 'phi', file: 'kaon_phi.json' },
  { particle: 'kaon', variable: 'eta', file: 'kaon_eta.json' },
  
  // Lambda
  { particle: 'lambda', variable: 'pt', file: 'lambda_pt.json' },
  { particle: 'lambda', variable: 'px', file: 'lambda_px.json' },
  { particle: 'lambda', variable: 'py', file: 'lambda_py.json' },
  { particle: 'lambda', variable: 'pz', file: 'lambda_pz.json' },
  { particle: 'lambda', variable: 'p', file: 'lambda_p.json' },
  { particle: 'lambda', variable: 'angle_z_mrad', file: 'lambda_angle_z_mrad.json' }
]

// Group histograms by particle
const groupedHistograms = computed(() => {
  const groups: Record<string, typeof availableHistograms> = {}
  availableHistograms.forEach(hist => {
    if (!groups[hist.particle]) {
      groups[hist.particle] = []
    }
    groups[hist.particle].push(hist)
  })
  return groups
})

// Load histogram data
async function loadHistogram() {
  if (!selectedHistogram.value) {
    currentHistogram.value = null
    if (chartInstance) {
      chartInstance.clear()
    }
    return
  }

  loading.value = true
  error.value = ''

  try {
    const url = withBase(`${props.basePath}/${selectedHistogram.value}`)
    const response = await fetch(url)
    
    if (!response.ok) {
      throw new Error(`Failed to load histogram: ${response.statusText}`)
    }

    const data = await response.json()
    currentHistogram.value = data
    updateChart(data)
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load histogram'
    console.error('Error loading histogram:', err)
  } finally {
    loading.value = false
  }
}

// Update ECharts
function updateChart(histData: any) {
  if (!chartContainer.value || !chartInstance) return

  // Create bar data from bins
  const barData = histData.bins.centers.map((center: number, i: number) => 
    [center, histData.bins.counts[i]]
  )

  const option: echarts.EChartsOption = {
    title: {
      text: histData.title,
      left: 'center',
      textStyle: {
        fontSize: 16
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        const binCenter = params.data[0]
        const count = params.data[1]
        const binWidth = histData.bins.centers[1] - histData.bins.centers[0]
        const binStart = binCenter - binWidth / 2
        const binEnd = binCenter + binWidth / 2
        
        return `${histData.x_label}<br/>` +
               `Range: [${binStart.toFixed(3)}, ${binEnd.toFixed(3)}]<br/>` +
               `Center: ${binCenter.toFixed(3)}<br/>` +
               `Count: ${count}`
      }
    },
    grid: {
      left: '10%',
      right: '5%',
      bottom: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: histData.x_label,
      nameLocation: 'middle',
      nameGap: 30,
      axisLabel: {
        formatter: (value: number) => value.toFixed(2)
      }
    },
    yAxis: {
      type: 'value',
      name: 'Counts',
      nameLocation: 'middle',
      nameGap: 50
    },
    series: [{
      type: 'bar',
      data: barData,
      itemStyle: {
        color: '#5470c6'
      },
      emphasis: {
        itemStyle: {
          color: '#91cc75'
        }
      }
    }],
    dataZoom: [
      {
        type: 'inside',
        start: 0,
        end: 100
      },
      {
        type: 'slider',
        start: 0,
        end: 100,
        handleSize: '80%',
        bottom: 10
      }
    ]
  }

  chartInstance.setOption(option)
}

// Handle window resize
function handleResize() {
  if (chartInstance) {
    chartInstance.resize()
  }
}

// Lifecycle hooks
onMounted(() => {
  if (chartContainer.value) {
    chartInstance = echarts.init(chartContainer.value)
    window.addEventListener('resize', handleResize)
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (chartInstance) {
    chartInstance.dispose()
  }
})

// Watch for dark mode changes
if (typeof window !== 'undefined') {
  const observer = new MutationObserver(() => {
    if (chartInstance && chartContainer.value) {
      const isDark = document.documentElement.classList.contains('dark')
      chartInstance.dispose()
      chartInstance = echarts.init(chartContainer.value, isDark ? 'dark' : undefined)
      if (currentHistogram.value) {
        updateChart(currentHistogram.value)
      }
    }
  })
  
  onMounted(() => {
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class']
    })
  })
  
  onUnmounted(() => {
    observer.disconnect()
  })
}
</script>

<style scoped>
.histogram-viewer {
  margin: 2rem 0;
}

.controls {
  margin-bottom: 1rem;
}

.controls label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.controls select {
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

.controls select:hover {
  border-color: var(--vp-c-brand);
}

.controls select:focus {
  outline: none;
  border-color: var(--vp-c-brand);
  box-shadow: 0 0 0 2px var(--vp-c-brand-soft);
}

.stats {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background-color: var(--vp-c-bg-soft);
  border-radius: 8px;
  font-size: 14px;
}

.stat-item {
  padding: 0.25rem 0.75rem;
  background-color: var(--vp-c-bg);
  border-radius: 4px;
  border: 1px solid var(--vp-c-divider);
}

.chart-container {
  width: 100%;
  height: 500px;
  background-color: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 1rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: var(--vp-c-text-2);
}

.error {
  text-align: center;
  padding: 2rem;
  color: var(--vp-c-danger);
  background-color: var(--vp-c-danger-soft);
  border-radius: 8px;
  margin-top: 1rem;
}

/* Dark mode adjustments */
.dark .controls select {
  background-color: var(--vp-c-bg-elv);
}

.dark .chart-container {
  background-color: var(--vp-c-bg-elv);
}

/* Responsive design */
@media (max-width: 768px) {
  .chart-container {
    height: 400px;
  }
  
  .stats {
    font-size: 12px;
  }
}
</style>
