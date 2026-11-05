<script setup>
import { reactive, ref, onMounted, onBeforeUnmount, nextTick } from 'vue'

// Only the five intentionally exposed physics settings are editable.
const choices = reactive({
  energy: 'uniform',
  angle: 'uniform',
  detectors: 'both',
  clustering: 30,
  samples: 10000,
})

// Values inherited from the Python model. These geometric assumptions are proxies,
// not DD4hep detector acceptance. Both calorimeters use the chosen cluster distance.
const BASE = Object.freeze({
  energyMinGeV: 130, energyMaxGeV: 275,
  cosMin: 0.99954, cosMax: 0.99981,
  fixedEnergyGeV: 275, fixedThetaMrad: 25,
  azimuth: 'fixed-negative-x', seed: 24010,
  zdcZM: 36, zdcAxisMrad: -25,
  zdcGeometry: 'circle', zdcRadiusMm: 150,
  zdcWidthMm: 650, zdcHeightMm: 600,
  b0ZM: 6.4, b0MinMrad: 5.5, b0MaxMrad: 18,
})

const isRunning = ref(false)
const error = ref('')
const result = ref(null)
const activeSelection = ref(null)
const chartEl = ref(null)
let worker = null
let chart = null
let echarts = null
let resizeObserver = null
let runCounter = 0
let pending = null

function selectionToSimulation(sel) {
  const params = {
    ...BASE,
    samples: Number(sel.samples),
    zdcMergeMm: Number(sel.clustering),
    b0MergeMm: Number(sel.clustering),
  }
  // Keep energy and theta independently selectable: 4 combinations are supported.
  if (sel.energy === 'fixed') {
    params.energyMinGeV = 275
    params.energyMaxGeV = 275
  }
  if (sel.angle === 'fixed') {
    params.cosMin = Math.cos(25e-3)
    params.cosMax = params.cosMin
  }
  // The physics kernel's 'fixed' mode fixes both E and theta.
  // For mixed settings use 'sampled' with one degenerate uniform distribution.
  const mode = sel.energy === 'fixed' && sel.angle === 'fixed' ? 'fixed' : 'sampled'
  return { mode, params }
}

function getSelectedCurves(data, sel) {
  return {
    fractions: sel.detectors === 'zdc' ? data.fractionsZdc : data.fractionsBoth,
    gamma: sel.detectors === 'zdc' ? data.curves.gammaZdc : data.curves.gammaBoth,
    full: sel.detectors === 'zdc' ? data.curves.fullZdc : data.curves.fullBoth,
    fullPct: sel.detectors === 'zdc' ? data.summary.fullZdcPct : data.summary.fullBothPct,
  }
}

function buildChartOption(data, sel) {
  const {fractions, gamma, full} = getSelectedCurves(data, sel)
  const fill = (name, field, color) => ({
    name, type:'line', stack:'acceptance', step:'middle', showSymbol:false,
    silent:true, animation:false, data:fractions.map(p => [p.z, p[field]]),
    lineStyle:{width:0}, areaStyle:{color,opacity:.90}, itemStyle:{color}, z:1,
  })
  const line = (name, values, color, style, width=2.4) => ({
    name, type:'line', yAxisIndex:1, showSymbol:false, animation:false,
    data:values, lineStyle:{color,width,type:style}, itemStyle:{color}, z:12,
  })
  return {
    animation:false,
    backgroundColor:'#ffffff',
    textStyle:{fontFamily:'Georgia, STIXGeneral, serif', color:'#30343b'},
    grid:{left:68,right:80,top:25,bottom:65},
    tooltip:{trigger:'axis',axisPointer:{type:'cross'},confine:true,
      formatter(items) {
        if (!items?.length) return ''
        const z = items[0].axisValue
        return `<strong>z = ${Number(z).toFixed(2)} m</strong><br/>` +
          items.map(x => `${x.marker} ${x.seriesName}: ${Number(x.value?.[1] ?? x.value).toFixed(2)}${x.seriesIndex < 3 ? '' : ' %'}`).join('<br/>')
      }},
    xAxis:{type:'value', min:0, max:BASE.zdcZM, name:'Lambda decay position z [m]',
      nameLocation:'middle',nameGap:35,axisLabel:{fontSize:12},splitLine:{show:false}},
    yAxis:[
      {type:'value',min:0,max:1,interval:.2,name:'Fraction at fixed decay position',
       nameLocation:'middle',nameGap:49,nameTextStyle:{fontSize:12},axisLabel:{fontSize:12},splitLine:{lineStyle:{opacity:.12}}},
      {type:'value',min:0,max:40,interval:10,name:'Cumulative probability [%]',
       nameLocation:'middle',nameGap:48,nameTextStyle:{fontSize:12},axisLabel:{fontSize:12},splitLine:{show:false}},
    ],
    series:[
      fill('Both γ accepted and separable','good','#259f86'),
      fill('Both γ accepted but merged','merged','#786ea8'),
      fill('At least one γ lost','lost','#df8662'),
      line('Neutral decay, cumulative',data.curves.neutral,'#17212d','solid',2.4),
      line('Neutron in ZDC, cumulative',data.curves.neutron,'#2466a0','dotted',2.5),
      line('Full n + γ + γ, cumulative',full,'#17212d',[9,4,2,4],3),
    ],
  }
}

async function redraw() {
  if (!result.value || !activeSelection.value) return
  await nextTick()
  if (!chartEl.value) return
  if (!echarts) echarts = await import('echarts')
  if (!chart) chart = echarts.init(chartEl.value, null, {renderer:'canvas'})
  chart.setOption(buildChartOption(result.value, activeSelection.value), {notMerge:true})
  chart.resize()
}

function run() {
  if (isRunning.value) return
  error.value = ''
  isRunning.value = true
  pending = {...choices}
  const {params,mode} = selectionToSimulation(pending)
  const runId = ++runCounter
  if (!worker) {
    worker = new Worker(new URL('./lambdaWorker.js', import.meta.url), {type:'module'})
    worker.onmessage = async ({data}) => {
      if (data.runId !== runCounter) return
      isRunning.value = false
      if (!data.ok) {error.value = data.error; return}
      result.value = data.result
      activeSelection.value = {...pending}
      try {await redraw()} catch (e) {error.value = `Plot error: ${e.message}`}
    }
    worker.onerror = (event) => {
      error.value = `Monte Carlo worker failed: ${event.message}`
      isRunning.value = false
    }
  }
  worker.postMessage({params,mode,runId})
}

function download(name, data, mime) {
  const blob = new Blob([data], {type:mime})
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = name
  document.body.appendChild(link)
  link.click()
  link.remove()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}

function saveCSV() {
  if (!result.value || !activeSelection.value) return
  const r = result.value
  const {gamma,full} = getSelectedCurves(r,activeSelection.value)
  const header = 'z_m,neutral_percent,neutron_percent,two_gamma_percent,full_n_gamma_gamma_percent'
  const lines = r.curves.neutral.map((point,i) =>
    [point[0],point[1],r.curves.neutron[i][1],gamma[i][1],full[i][1]].join(','))
  download('lambda_acceptance.csv',[header,...lines].join('\n'),'text/csv;charset=utf-8')
}

function savePNG() {
  if (!chart) return

  // The on-page legend, title and parameter label are HTML elements OUTSIDE
  // ECharts, so chart.getDataURL() alone cannot include them.
  // Create a second canvas solely for export; leave the page untouched.
  const scale = 2
  const plot = chart.getRenderedCanvas({ pixelRatio: scale, backgroundColor: '#ffffff' })
  const w = plot.width / scale
  const compact = w < 650
  const pad = 26
  const title = 'Λ geometric acceptance'
  const subtitle = resultLabel(activeSelection.value)

  const entries = [
    { label: 'Both γ separable', kind: 'fill', color: '#259f86' },
    { label: 'γ merged', kind: 'fill', color: '#786ea8' },
    { label: 'γ lost', kind: 'fill', color: '#df8662' },
    { label: 'Neutral decay', kind: 'line', color: '#17212d' },
    { label: 'Neutron in ZDC', kind: 'dot', color: '#2466a0' },
    { label: 'Full n+γ+γ', kind: 'dashdot', color: '#17212d' },
  ]

  const canvas = document.createElement('canvas')
  const cols = compact ? 1 : 3
  const rows = Math.ceil(entries.length / cols)
  // Header + parameter label + legend, then the untouched ECharts canvas.
  const headerH = 93 + rows * 25 + 15
  canvas.width = plot.width
  canvas.height = Math.round(plot.height + scale * headerH)
  const ctx = canvas.getContext('2d')
  ctx.scale(scale, scale)
  ctx.fillStyle = '#ffffff'
  ctx.fillRect(0, 0, w, canvas.height / scale)
  ctx.textBaseline = 'middle'
  ctx.textAlign = 'left'

  ctx.fillStyle = '#30343b'
  ctx.font = 'bold 17px Georgia, serif'
  ctx.fillText(title, pad, 26)

  ctx.font = '12px Georgia, serif'
  ctx.fillStyle = '#5e6470'
  // Avoid clipping long parameter labels when the viewport is narrow.
  const maxW = w - 2 * pad
  const words = subtitle.split(/\s+/)
  const lines = []
  let line = ''
  for (const word of words) {
    const test = line ? `${line} ${word}` : word
    if (ctx.measureText(test).width > maxW && line) {
      lines.push(line)
      line = word
    } else {
      line = test
    }
  }
  if (line) lines.push(line)
  lines.slice(0, 3).forEach((str, i) => ctx.fillText(str, pad, 50 + 16 * i))

  const legendTop = Math.max(81, 55 + 16 * Math.min(lines.length, 3))
  const legendCols = compact ? 1 : 3
  const legendRows = Math.ceil(entries.length / legendCols)
  const calculatedHeaderH = legendTop + legendRows * 25 + 14
  // Adjust canvas height to the true wrapped-label/legend height.
  if (calculatedHeaderH !== headerH) {
    // Canvas resize clears its state. Re-render instead of stretching pixels.
    const tmp = document.createElement('canvas')
    tmp.width = canvas.width
    tmp.height = Math.round(scale * calculatedHeaderH + plot.height)
    const c2 = tmp.getContext('2d')
    c2.drawImage(canvas, 0, 0)
    canvas.width = tmp.width
    canvas.height = tmp.height
    const cc = canvas.getContext('2d')
    cc.drawImage(tmp, 0, 0)
  }
  const c = canvas.getContext('2d')
  c.setTransform(scale, 0, 0, scale, 0, 0)
  c.textBaseline = 'middle'
  c.textAlign = 'left'
  c.font = '12px Georgia, serif'
  c.fillStyle = '#30343b'

  const colW = (w - 2 * pad) / legendCols
  entries.forEach((item, i) => {
    const col = i % legendCols
    const row = Math.floor(i / legendCols)
    const x = pad + col * colW
    const y = legendTop + row * 25
    c.save()
    if (item.kind === 'fill') {
      c.fillStyle = item.color
      c.fillRect(x, y - 5, 16, 10)
    } else {
      c.strokeStyle = item.color
      c.lineWidth = 2.5
      c.setLineDash(item.kind === 'dot' ? [2, 4] : item.kind === 'dashdot' ? [9, 4, 2, 4] : [])
      c.beginPath()
      c.moveTo(x, y)
      c.lineTo(x + 20, y)
      c.stroke()
    }
    c.restore()
    c.fillStyle = '#30343b'
    c.fillText(item.label, x + 25, y)
  })

  c.setTransform(1, 0, 0, 1, 0, 0)
  c.drawImage(plot, 0, Math.round(scale * calculatedHeaderH))

  const a = document.createElement('a')
  a.href = canvas.toDataURL('image/png')
  a.download = 'lambda_acceptance.png'
  a.click()
}


function resultLabel(sel) {
  if (!sel) return ''
  const energy = sel.energy === 'fixed' ? 'E = 275 GeV' : 'E ~ U(130, 275) GeV'
  const angle = sel.angle === 'fixed' ? 'θ = 25 mrad' : 'cos θ ~ U(0.99954, 0.99981)'
  const detector = sel.detectors === 'zdc' ? 'ZDC only' : 'ZDC + B0'
  return `${energy} · ${angle} · ${detector} · d = ${sel.clustering} mm`
}

onMounted(() => {
  resizeObserver = new ResizeObserver(() => chart?.resize())
  if (chartEl.value) resizeObserver.observe(chartEl.value)
  run()
})
onBeforeUnmount(() => {
  worker?.terminate()
  resizeObserver?.disconnect()
  chart?.dispose()
  chart = null
})
</script>

<template>
  <section class="lambda-tool">
    <p class="model-note">Explore the geometric acceptance for Λ → nπ⁰ → nγγ. Adjust five settings and recalculate a single Monte Carlo plot.</p>
    <div class="controls">
      <label class="control-group">
        <span class="heading">Λ energy</span>
        <select v-model="choices.energy">
          <option value="fixed">Monoenergetic — 275 GeV</option>
          <option value="uniform">Uniform 130–275 GeV (realistic)</option>
        </select>
      </label>
      <label class="control-group">
        <span class="heading">Λ angle</span>
        <select v-model="choices.angle">
          <option value="fixed">Mono-angle — 25 mrad</option>
          <option value="uniform">Uniform cos θ 0.99954–0.99981 (realistic)</option>
        </select>
      </label>
      <label class="control-group">
        <span class="heading">Detectors</span>
        <select v-model="choices.detectors">
          <option value="zdc">ZDC only</option>
          <option value="both">ZDC + B0</option>
        </select>
      </label>
      <label class="control-group">
        <span class="heading">Clustering distance</span>
        <select v-model.number="choices.clustering">
          <option :value="15">15 mm</option>
          <option :value="30">30 mm</option>
          <option :value="45">45 mm</option>
        </select>
      </label>
      <label class="control-group">
        <span class="heading">Monte Carlo samples</span>
        <select v-model.number="choices.samples">
          <option :value="10000">10,000 (default)</option>
          <option :value="50000">50,000</option>
          <option :value="100000">100,000</option>
        </select>
      </label>
    </div>

    <div class="actions">
      <button class="run" :disabled="isRunning" @click="run">{{isRunning ? 'Calculating…' : 'Run Monte Carlo'}}</button>
      <button class="secondary" :disabled="!result" @click="saveCSV">Export CSV</button>
      <button class="secondary" :disabled="!result" @click="savePNG">Export PNG</button>
      <span v-if="result && activeSelection" class="status">P(full) = {{getSelectedCurves(result,activeSelection).fullPct.toFixed(2)}}%</span>
    </div>
    <p v-if="error" class="error">{{error}}</p>
    <div class="legend">
      <span><i style="background:#259f86"></i>Both γ separable</span>
      <span><i style="background:#786ea8"></i>γ merged</span>
      <span><i style="background:#df8662"></i>γ lost</span>
      <span><b class="neutral"></b>Neutral decay</span>
      <span><b class="neutron"></b>Neutron in ZDC</span>
      <span><b class="full"></b>Full n+γ+γ</span>
    </div>
    <article class="plot-card">
      <h3>Λ geometric acceptance</h3>
      <p class="plot-label">{{resultLabel(activeSelection) || 'Preparing Monte Carlo…'}}</p>
      <div ref="chartEl" class="chart"></div>
    </article>
    <p class="caveat"><strong>Model limitations:</strong> plane-based ZDC (radius 150 mm, z = 36 m) and B0 (z = 6.4 m, angular annulus 5.5–18 mrad) proxies. No beamline apertures, materials, neutron reconstruction efficiency, or shower simulation. The selected clustering distance applies to both B0 and ZDC. Probabilities include BR(Λ → nπ⁰) × BR(π⁰ → γγ) and correlated neutron–photon geometry.</p>
  </section>
</template>

<style scoped>
.lambda-tool{max-width:1100px;margin:0 auto;padding:0 22px 55px;color:var(--vp-c-text-1);font-size:14px}
.model-note{color:var(--vp-c-text-2);margin:7px 0 22px}
.controls{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.control-group{display:flex;flex-direction:column;gap:10px;padding:13px 14px 15px;border:1px solid var(--vp-c-divider);border-radius:10px;background:var(--vp-c-bg-soft)}
.heading{font-size:13px;font-weight:650;color:var(--vp-c-text-1)}
.control-group select{min-width:0;width:100%;border:1px solid var(--vp-c-divider);background:var(--vp-c-bg);color:var(--vp-c-text-1);border-radius:6px;padding:8px;font-size:12px}
.actions{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:20px 0 15px}
.actions button{border:1px solid var(--vp-c-divider);border-radius:7px;padding:8px 13px;cursor:pointer;font-weight:650}
.actions button.run{background:var(--vp-c-brand-1);color:#fff;border-color:var(--vp-c-brand-1)}
.actions button.secondary{background:var(--vp-c-bg-soft);color:var(--vp-c-text-1)}
.actions button:disabled{opacity:.5;cursor:default}
.status{color:var(--vp-c-brand-1);font-weight:700;margin-left:auto}
.error{color:#b33;padding:8px 0}
.legend{display:flex;justify-content:center;gap:11px 20px;flex-wrap:wrap;margin:16px 0 13px;color:var(--vp-c-text-2);font-size:12px}
.legend span{display:flex;align-items:center;gap:7px}
.legend i{width:15px;height:9px;border-radius:2px;display:inline-block}
.legend b{width:22px;border-top:2.5px solid #17212d;height:1px;display:inline-block}
.legend b.neutron{border-color:#2466a0;border-top-style:dotted}
.legend b.full{border-color:#17212d;border-top-style:dashed}
.plot-card{border:1px solid var(--vp-c-divider);border-radius:12px;padding:18px 15px;min-width:0;background:var(--vp-c-bg)}
.plot-card h3{font-size:16px;font-weight:650;margin:0 0 5px}
.plot-label{font-size:12px;color:var(--vp-c-text-2);margin:0 0 7px}
.chart{height:460px;width:100%}
.caveat{font-size:12px;line-height:1.65;color:var(--vp-c-text-2);margin:22px 0}
@media(max-width:850px){.controls{grid-template-columns:repeat(2,minmax(0,1fr))}.chart{height:390px}}
@media(max-width:600px){.lambda-tool{padding:0 10px 35px}.controls{grid-template-columns:1fr}.chart{height:340px}.status{margin-left:0}}
</style>
