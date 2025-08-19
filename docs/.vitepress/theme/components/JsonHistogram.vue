<template>
  <div class="json-histogram">
    <div v-if="loading" class="loading">Loading histogram...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div v-if="showStats && histogramData" class="stats">
        <span class="stat-item">
          <strong>Entries:</strong> {{ histogramData.stats.entries.toLocaleString() }}
        </span>
        <span class="stat-item">
          <strong>Mean:</strong> {{ histogramData.stats.mean.toFixed(3) }}
        </span>
        <span class="stat-item">
          <strong>Std Dev:</strong> {{ histogramData.stats.std.toFixed(3) }}
        </span>
      </div>
      <div ref="chartContainer" class="chart-container" :style="{ height: height }"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import { withBase } from 'vitepress'

// Props
const props = defineProps<{
  path: string
  height?: string
  showStats?: boolean
  title?: string
}>()

// Default values
const height = props.height || '400px'
const showStats = props.showStats !== false

// Refs
const chartContainer = ref<HTMLElement>()
const histogramData = ref<any>(null)
const loading = ref(true)
const error = ref('')
let chartInstance: echarts.ECharts | null = null

// Load histogram data
async function loadHistogram() {
  loading.value = true
  error.value = ''

  try {
    const url = withBase(props.path)
    const response = await fetch(url)
    
    if (!response.ok) {
      throw new Error(`Failed to load histogram: ${response.statusText}`)
    }

    const data = await response.json()
    histogramData.value = data
    
    // Wait for next tick to ensure container is ready
    await new Promise(resolve => setTimeout(resolve, 0))
    
    if (chartContainer.value && !chartInstance) {
      const isDark = document.documentElement.classList.contains('dark')
      chartInstance = echarts.init(chartContainer.value, isDark ? 'dark' : undefined)
    }
    
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
  if (!chartInstance) return

  // Create bar data from bins
  const barData = histData.bins.centers.map((center: number, i: number) => 
    [center, histData.bins.counts[i]]
  )

  const option: echarts.EChartsOption = {
    title: {
      text: props.title || histData.title,
      left: 'center',
      top: 10,
      textStyle: {
        fontSize: 14,
        fontWeight: 'normal'
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
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: histData.x_label,
      nameLocation: 'middle',
      nameGap: 25,
      axisLabel: {
        formatter: (value: number) => value.toFixed(2)
      }
    },
    yAxis: {
      type: 'value',
      name: 'Counts',
      nameLocation: 'middle',
      nameGap: 45
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
  loadHistogram()
  window.addEventListener('resize', handleResize)
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
      if (histogramData.value) {
        updateChart(histogramData.value)
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

// Watch for path changes
watch(() => props.path, () => {
  loadHistogram()
})
</script>

<style scoped>
.json-histogram {
  margin: 1.5rem 0;
}

.stats {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding: 0.75rem;
  background-color: var(--vp-c-bg-soft);
  border-radius: 6px;
  font-size: 13px;
}

.stat-item {
  padding: 0.25rem 0.5rem;
  background-color: var(--vp-c-bg);
  border-radius: 4px;
  border: 1px solid var(--vp-c-divider);
}

.chart-container {
  width: 100%;
  background-color: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  padding: 0.5rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: var(--vp-c-text-2);
}

.error {
  text-align: center;
  padding: 1rem;
  color: var(--vp-c-danger);
  background-color: var(--vp-c-danger-soft);
  border-radius: 6px;
}

/* Dark mode adjustments */
.dark .chart-container {
  background-color: var(--vp-c-bg-elv);
}

/* Responsive design */
@media (max-width: 768px) {
  .chart-container {
    padding: 0.25rem;
  }
  
  .stats {
    font-size: 12px;
  }
}
</style>
