/**
 * Browser-side, dependency-free port of the semi-analytic Python Lambda model.
 * Geometry is an illustrative planar proxy (not full ePIC DD4hep / beamline).
 * Units: GeV, metres, milliradians, millimetres.
 */
export const MASS_LAMBDA = 1.115683;
export const MASS_N = 0.9395654205;
export const MASS_PI = 0.1349768;
export const BR_NEUTRAL = 0.358 * 0.98823;
const CT = 299792458 * 2.632e-10;

function rngFactory(seed) {
  let s = (seed >>> 0);
  return () => {
    s = (s + 0x6D2B79F5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t ^= t + Math.imul(t ^ (t >>> 7), 61 | t);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function isotropic(rnd) {
  const u = 2 * rnd() - 1;
  const a = 2 * Math.PI * rnd();
  const v = Math.sqrt(Math.max(0, 1 - u * u));
  return [v * Math.cos(a), v * Math.sin(a), u];
}
function boost(E, p, b) {
  const b2 = b[0] ** 2 + b[1] ** 2 + b[2] ** 2;
  const gamma = 1 / Math.sqrt(1 - b2);
  const bp = b[0] * p[0] + b[1] * p[1] + b[2] * p[2];
  const factor = ((gamma - 1) * bp / Math.max(b2, 1e-30)) + gamma * E;
  return [gamma * (E + bp), [p[0] + factor * b[0], p[1] + factor * b[1], p[2] + factor * b[2]]];
}
function unit(p) {
  const v = Math.hypot(...p);
  return p.map(x => x / v);
}
function hit(origin, dir, z, offsetXmm) {
  if (z <= origin[2] || dir[2] <= 1e-12) return null;
  const s = (z - origin[2]) / dir[2];
  return [(origin[0] + s * dir[0]) * 1000 - offsetXmm,
          (origin[1] + s * dir[1]) * 1000];
}
function inZdc(point, a) {
  if (!point) return false;
  const [x, y] = point;
  return a.zdcGeometry === 'rectangle'
    ? Math.abs(x) <= a.zdcWidthMm / 2 && Math.abs(y) <= a.zdcHeightMm / 2
    : Math.hypot(x, y) <= a.zdcRadiusMm;
}
function inB0(point, a) {
  if (!point) return false;
  const r = Math.hypot(...point);
  return r >= a.b0ZM * a.b0MinMrad && r <= a.b0ZM * a.b0MaxMrad;
}
function separate(p, q, threshold) {
  return Math.hypot(p[0] - q[0], p[1] - q[1]) >= threshold;
}
function freshBins(n) { return new Float64Array(n); }
function binIndex(z, limit, bins) {
  return Math.min(bins - 1, Math.max(0, Math.floor(z / limit * bins)));
}
function add(bin, z, limit) { bin[binIndex(z, limit, bin.length)]++; }

export function validate(params) {
  const a = params;
  const numbers = Object.values(a).filter(x => typeof x === 'number');
  if (numbers.some(x => !Number.isFinite(x))) throw new Error('All numeric inputs must be finite.');
  if (!(a.samples >= 100 && a.samples <= 100000 && Number.isInteger(a.samples))) throw new Error('Samples must be an integer between 100 and 100,000.');
  if (!(a.energyMinGeV > MASS_LAMBDA && a.energyMaxGeV >= a.energyMinGeV)) throw new Error('Invalid sampled energy interval.');
  if (!(a.fixedEnergyGeV > MASS_LAMBDA)) throw new Error('Fixed Lambda energy must exceed its rest mass.');
  if (!(a.cosMin > 0 && a.cosMin <= a.cosMax && a.cosMax <= 1)) throw new Error('Invalid cos(theta) interval.');
  if (!(a.fixedThetaMrad >= 0 && a.fixedThetaMrad <= 1000)) throw new Error('Invalid fixed angle.');
  if (!(a.zdcZM > a.b0ZM && a.b0ZM > 0)) throw new Error('B0 must be upstream of the ZDC.');
  if (!(a.b0MinMrad >= 0 && a.b0MaxMrad > a.b0MinMrad)) throw new Error('Invalid B0 angular acceptance.');
  if (!(a.zdcRadiusMm > 0 && a.zdcWidthMm > 0 && a.zdcHeightMm > 0)) throw new Error('ZDC dimensions must be positive.');
  if (!(a.zdcMergeMm >= 0 && a.b0MergeMm >= 0)) throw new Error('Merging thresholds must be non-negative.');
  if (!['circle', 'rectangle'].includes(a.zdcGeometry)) throw new Error('Invalid ZDC geometry.');
  if (!['fixed-negative-x', 'uniform'].includes(a.azimuth)) throw new Error('Invalid azimuth model.');
}

export function simulate(a, mode, seed) {
  validate(a);
  if (!['sampled', 'fixed'].includes(mode)) throw new Error(`Unknown mode: ${mode}`);
  const rnd = rngFactory(seed);
  const n = a.samples;
  const bins = 45;
  const curvesN = 301;
  const zMax = a.zdcZM;
  const h = {
    neutral: freshBins(bins),
    neutron: freshBins(bins),
    gammaZdc: freshBins(bins),
    gammaBoth: freshBins(bins),
    fullZdc: freshBins(bins),
    fullBoth: freshBins(bins),
    total: freshBins(bins),
    zdcGood: freshBins(bins),
    zdcMerge: freshBins(bins),
    zdcLost: freshBins(bins),
    bothGood: freshBins(bins),
    bothMerge: freshBins(bins),
    bothLost: freshBins(bins),
  };
  const zscale = new Float64Array(n);
  const timestamps = { neutron: [], gammaZdc: [], gammaBoth: [], fullZdc: [], fullBoth: [] };
  const q = Math.sqrt((MASS_LAMBDA**2 - (MASS_N + MASS_PI)**2) *
                      (MASS_LAMBDA**2 - (MASS_N - MASS_PI)**2)) / (2 * MASS_LAMBDA);
  const pionRestE = Math.hypot(q, MASS_PI);
  const neutronRestE = Math.hypot(q, MASS_N);
  const zdcOffset = zMax * Math.tan(a.zdcAxisMrad * 1e-3) * 1000;
  const b0Offset = a.b0ZM * Math.tan(a.zdcAxisMrad * 1e-3) * 1000;
  let b0b0 = 0, b0zdc = 0, zdczdc = 0;

  for (let i = 0; i < n; i++) {
    const E = mode === 'fixed' ? a.fixedEnergyGeV : a.energyMinGeV + rnd() * (a.energyMaxGeV - a.energyMinGeV);
    const mu = mode === 'fixed' ? Math.cos(a.fixedThetaMrad * 1e-3) : a.cosMin + rnd() * (a.cosMax - a.cosMin);
    const theta = Math.acos(mu);
    const phi = a.azimuth === 'uniform' ? rnd() * 2 * Math.PI : Math.PI;
    const lambdaDir = [Math.sin(theta) * Math.cos(phi), Math.sin(theta) * Math.sin(phi), mu];
    const p = Math.sqrt(E * E - MASS_LAMBDA * MASS_LAMBDA);
    const beta = lambdaDir.map(v => v * p / E);
    const meanFlight = p / MASS_LAMBDA * CT;
    const decayFlight = -Math.log(Math.max(1e-15, 1 - rnd())) * meanFlight;
    const origin = lambdaDir.map(v => v * decayFlight);
    const z = origin[2];
    zscale[i] = meanFlight * mu;
    if (z >= zMax) continue;

    const uPi = isotropic(rnd);
    const [Epi, pPi] = boost(pionRestE, uPi.map(v => q * v), beta);
    const [, pNeutron] = boost(neutronRestE, uPi.map(v => -q * v), beta);
    const neutron = inZdc(hit(origin, unit(pNeutron), zMax, zdcOffset), a);

    const uPhoton = isotropic(rnd);
    const piBeta = pPi.map(v => v / Epi);
    const [, pGamma1] = boost(MASS_PI / 2, uPhoton.map(v => MASS_PI / 2 * v), piBeta);
    const [, pGamma2] = boost(MASS_PI / 2, uPhoton.map(v => -MASS_PI / 2 * v), piBeta);
    const g1 = unit(pGamma1), g2 = unit(pGamma2);

    const z1pos = hit(origin, g1, zMax, zdcOffset), z2pos = hit(origin, g2, zMax, zdcOffset);
    const z1 = inZdc(z1pos, a), z2 = inZdc(z2pos, a);
    const zdcBoth = z1 && z2;
    const zdcResolved = zdcBoth && separate(z1pos, z2pos, a.zdcMergeMm);
    const zdcMerged = zdcBoth && !zdcResolved;

    const b1pos = hit(origin, g1, a.b0ZM, b0Offset), b2pos = hit(origin, g2, a.b0ZM, b0Offset);
    const b1 = inB0(b1pos, a), b2 = inB0(b2pos, a);
    const zz1 = z1 && !b1, zz2 = z2 && !b2;
    const sameZ = zz1 && zz2, sameB = b1 && b2;
    const mixed = (b1 && zz2) || (zz1 && b2);
    const zResolved = sameZ && separate(z1pos, z2pos, a.zdcMergeMm);
    const bResolved = sameB && separate(b1pos, b2pos, a.b0MergeMm);
    const bothDetected = (b1 || zz1) && (b2 || zz2);
    const combinedResolved = zResolved || bResolved || mixed;
    const combinedMerged = bothDetected && !combinedResolved;
    if (bResolved) b0b0++;
    if (zResolved) zdczdc++;
    if (mixed) b0zdc++;

    add(h.total, z, zMax);
    if (neutron) timestamps.neutron.push(z);
    if (zdcResolved) timestamps.gammaZdc.push(z);
    if (combinedResolved) timestamps.gammaBoth.push(z);
    if (zdcResolved && neutron) timestamps.fullZdc.push(z);
    if (combinedResolved && neutron) timestamps.fullBoth.push(z);

    add(zdcResolved ? h.zdcGood : zdcMerged ? h.zdcMerge : h.zdcLost, z, zMax);
    add(combinedResolved ? h.bothGood : combinedMerged ? h.bothMerge : h.bothLost, z, zMax);
  }
  const zBins = Array.from({length: bins}, (_, j) => zMax * (j + 0.5) / bins);
  function fractions(g, m, l) {
    return zBins.map((z, j) => ({
      z,
      good: h.total[j] ? g[j] / h.total[j] : 0,
      merged: h.total[j] ? m[j] / h.total[j] : 0,
      lost: h.total[j] ? l[j] / h.total[j] : 0,
      count: h.total[j],
    }));
  }
  function cumulative(timestampsForCategory) {
    timestampsForCategory.sort((a, b) => a - b);
    let cursor = 0;
    return Array.from({length: curvesN}, (_, j) => {
      const z = zMax * j / (curvesN - 1);
      while (cursor < timestampsForCategory.length && timestampsForCategory[cursor] <= z) cursor++;
      return [z, 100 * BR_NEUTRAL * cursor / n];
    });
  }
  const neutral = Array.from({length: curvesN}, (_, j) => {
    const z = zMax * j / (curvesN - 1);
    let p = 0;
    for (let i = 0; i < n; i++) p += 1 - Math.exp(-z / zscale[i]);
    return [z, 100 * BR_NEUTRAL * p / n];
  });
  const curves = {
    neutral,
    neutron: cumulative(timestamps.neutron),
    gammaZdc: cumulative(timestamps.gammaZdc),
    gammaBoth: cumulative(timestamps.gammaBoth),
    fullZdc: cumulative(timestamps.fullZdc),
    fullBoth: cumulative(timestamps.fullBoth),
  };
  const last = key => curves[key][curvesN - 1][1];
  return {
    mode,
    fractionsZdc: fractions(h.zdcGood, h.zdcMerge, h.zdcLost),
    fractionsBoth: fractions(h.bothGood, h.bothMerge, h.bothLost),
    curves,
    summary: {
      neutralPct: last('neutral'), neutronPct: last('neutron'),
      gammaZdcPct: last('gammaZdc'), gammaBothPct: last('gammaBoth'),
      fullZdcPct: last('fullZdc'), fullBothPct: last('fullBoth'),
      n, b0b0, b0zdc, zdczdc,
    },
  };
}
