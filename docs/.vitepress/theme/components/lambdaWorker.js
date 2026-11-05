import { simulate } from './lambdaPhysics.mjs';

self.onmessage = (event) => {
  const { params, mode, runId } = event.data;
  try {
    // Exactly one Monte Carlo scenario per click.
    const result = simulate(params, mode, params.seed);
    self.postMessage({ ok: true, result, runId });
  } catch (error) {
    self.postMessage({ ok: false, error: String(error?.message || error), runId });
  }
};
