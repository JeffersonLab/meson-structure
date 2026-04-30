#!/usr/bin/env python3
"""ROOT-macro analyses over edm4hep files.

Runs both `mcpart_lambda.cxx` and `acceptance.cxx` ROOT macros against the
`*.edm4hep.root` files for one energy. Expected to run inside a container
that has ROOT + edm4hep/edm4eic dictionaries.

Run standalone (inside container):
    python runner.py --energy 10x100 \
        --edm4hep-dir /path/to/dd4hep/10x100 \
        --outdir /tmp/test --n-events 5000
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Sequence, Union

runner_dir = Path(__file__).resolve().parent

MacroArg = Union[str, int, float]


def format_macro_arg(value: MacroArg) -> str:
    """Format one argument for a ROOT macro call.

    Strings are JSON-encoded (proper quoting + escaping of \" and \\).
    ints and floats are emitted as numeric literals.
    """
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, str):
        return json.dumps(value)
    raise TypeError(f"unsupported macro arg type: {type(value).__name__}")


def run_macro(macro: str, args: Sequence[MacroArg], cwd: Path) -> None:
    arg_str = ", ".join(format_macro_arg(a) for a in args)
    invocation = f"{macro}({arg_str})"
    cmd = ["root", "-x", "-l", "-b", "-q", invocation]
    print(f"[runner] {' '.join(cmd)}", flush=True)
    proc = subprocess.run(cmd, cwd=str(cwd))
    if proc.returncode != 0:
        sys.exit(proc.returncode)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--energy", required=True)
    parser.add_argument("--edm4hep-dir", type=Path, required=True,
                        help="Dir with *.edm4hep.root for this energy.")
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--n-events", type=int, default=5000)
    parser.add_argument("--only", default="all",
                        choices=["all", "mcpart_lambda", "acceptance"])
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    pattern = str(args.edm4hep_dir / "*.edm4hep.root")

    if args.only in ("all", "mcpart_lambda"):
        run_macro("mcpart_lambda.cxx",
                  [pattern, str(args.outdir / "mcpart_lambda"), args.n_events],
                  cwd=runner_dir)
    if args.only in ("all", "acceptance"):
        run_macro("acceptance.cxx",
                  [pattern, str(args.outdir / "acceptance"), args.n_events],
                  cwd=runner_dir)


if __name__ == "__main__":
    main()
