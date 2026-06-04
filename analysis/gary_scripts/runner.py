#!/usr/bin/env python3
"""Gary Penman's RAD/ePIC KLambda processing, wired into the launcher.

Runs the ROOT macro `ProcessMCMatchedKLambda.C` over the reconstructed
`*.edm4eic.root` files for one energy, producing a RAD output tree
(`MCMatched_KLambda_<energy>.root`) in the output directory.

The macro is built on the RAD / epic-rad header-only frameworks, added to
this repo as git submodules:
    deps/rad        (https://github.com/Garypenman/rad      @ v1.0.0)
    deps/epic-rad   (https://github.com/Garypenman/epic-rad @ v1.0.0)
Both `include/` dirs are prepended to ROOT_INCLUDE_PATH so the macro's
`#include "ePICReaction.h"` etc. resolve at run time.

Expected to run inside a container with ROOT + edm4eic/edm4hep/podio
dictionaries (e.g. eicdev/eic-full). meta.yaml sets use_container: true.

Run standalone (inside container):
    python runner.py --energy 18x275 \
        --reco-dir /path/to/reco/18x275 \
        --outdir /tmp/test --max-files 2

Stdlib-only at import time so it also runs inside the campaign container.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

runner_dir = Path(__file__).resolve().parent
repo_root = runner_dir.parents[1]  # analysis/gary_scripts -> <repo root>

RAD_INCLUDE = repo_root / "deps" / "rad" / "include"
EPICRAD_INCLUDE = repo_root / "deps" / "epic-rad" / "include"

MACRO = "ProcessMCMatchedKLambda.C"


def build_root_include_path(env: dict[str, str]) -> str:
    """Prepend the RAD + epic-rad include dirs to ROOT_INCLUDE_PATH."""
    parts = [str(RAD_INCLUDE), str(EPICRAD_INCLUDE)]
    existing = env.get("ROOT_INCLUDE_PATH", "")
    if existing:
        parts.append(existing)
    return os.pathsep.join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--energy", required=True,
                        help="Beam energy tag, e.g. 18x275 (output naming).")
    parser.add_argument("--reco-dir", type=Path, required=True,
                        help="Directory with reconstructed *.edm4eic.root files.")
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--glob", dest="glob_pattern", default="*.edm4eic.root",
                        help="Glob for reco files inside --reco-dir.")
    parser.add_argument("--max-files", type=int, default=None,
                        help="Limit number of input files (debug).")
    args = parser.parse_args()

    if not RAD_INCLUDE.is_dir() or not EPICRAD_INCLUDE.is_dir():
        sys.exit(
            "RAD headers not found. Initialise the submodules:\n"
            "    git submodule update --init deps/rad deps/epic-rad\n"
            f"  expected: {RAD_INCLUDE}\n            {EPICRAD_INCLUDE}"
        )

    args.outdir.mkdir(parents=True, exist_ok=True)

    files = sorted(str(f) for f in args.reco_dir.glob(args.glob_pattern))
    if not files:
        sys.exit(f"no reco files matching {args.glob_pattern!r} in {args.reco_dir}")
    if args.max_files is not None:
        files = files[: args.max_files]

    outfile = args.outdir / f"MCMatched_KLambda_{args.energy}.root"

    # Build the ROOT macro invocation: ProcessMCMatchedKLambda.C({"f1",...}, "out")
    vec_literal = "{" + ", ".join(json.dumps(f) for f in files) + "}"
    invocation = f'{MACRO}({vec_literal}, {json.dumps(str(outfile))})'

    env = dict(os.environ)
    env["ROOT_INCLUDE_PATH"] = build_root_include_path(env)

    cmd = ["root", "-x", "-l", "-b", "-q", invocation]
    print(f"[runner] energy={args.energy}  files={len(files)}  out={outfile}", flush=True)
    print(f"[runner] ROOT_INCLUDE_PATH={env['ROOT_INCLUDE_PATH']}", flush=True)
    print(f"[runner] cwd={runner_dir}", flush=True)
    print(f"[runner] root -x -l -b -q '{invocation[:120]}{'...' if len(invocation) > 120 else ''}'",
          flush=True)
    proc = subprocess.run(cmd, cwd=str(runner_dir), env=env)
    if proc.returncode != 0:
        sys.exit(proc.returncode)


if __name__ == "__main__":
    main()
