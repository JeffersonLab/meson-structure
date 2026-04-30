#!/usr/bin/env python3
"""Cross-energy comparison of EG kinematics.

`mode: once` analysis — consumes ALL energies in a single run.

Run standalone:
    python runner.py \
        --eg-dir /work/eic/users/romanov/eg-orig-kaon-lambda-2025-08 \
        --outdir /tmp/test
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

runner_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(runner_dir))


def resolve_files(eg_dir: Path, energies: list[str]) -> dict[str, str]:
    found: dict[str, str] = {}
    for e in energies:
        e_num, p_num = e.split("x")
        pattern = f"k_lambda_crossing_*-{e_num}.0on{p_num}.0_*.root"
        matches = sorted(eg_dir.glob(pattern))
        if matches:
            found[e] = str(matches[0])
        else:
            print(f"[runner] WARN: no EG file for {e} in {eg_dir}", file=sys.stderr)
    return found


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eg-dir", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--energies", default="5x41,10x100,10x130,18x275",
                        help="Comma-separated energies to overlay.")
    parser.add_argument("--chunk-size", type=int, default=100_000)
    parser.add_argument("--max-events", type=int, default=None)
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    energies = [e.strip() for e in args.energies.split(",") if e.strip()]
    files = resolve_files(args.eg_dir, energies)
    if not files:
        sys.exit(1)

    import eg_beam_compare_analysis as analysis  # deferred (pulls numpy/uproot)

    hists_by_energy: dict[str, dict] = {}
    for energy, path in files.items():
        print(f"[runner] processing {energy}: {path}", flush=True)
        hists_by_energy[energy] = analysis.process_file(  # type: ignore[name-defined]
            filename=path,
            chunk_size=args.chunk_size,
            max_events=args.max_events,
        )
    analysis.make_all_comparison_plots(hists_by_energy, outdir=str(args.outdir))  # type: ignore[name-defined]
    print(f"[runner] done -> {args.outdir}")


if __name__ == "__main__":
    main()
