#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


help_txt = """
convert_lambda.py  –  run csv_mcpart_lambda.cxx on every *.edm4eic.root file

Usage:
    python3 convert_lambda.py [directory] [macro]

Arguments (all optional)
    directory : where to search for ROOT files
                default: /volatile/eic/romanov/meson-structure-2025-06/reco

"""


# --- Config ---

if len(sys.argv) < 2:
    print("we need at least directory path")
    print(help_txt)
    exit(1)

indir = Path(sys.argv[1])
macros = [
    "csv_mcpart_lambda.cxx",
    "csv_mcdis.cxx"
]


# --- Find files ---
root_files = sorted(indir.glob("*.edm4eic.root"))
file_count = len(root_files)
if file_count == 0:
    sys.exit(f"[ERROR] No *.edm4eic.root files found in {indir}")

print(f"[INFO] Found {file_count} .edm4eic.root files in {indir}\n")

# ------------------------------------------------------------------ run loop
for idx, f in enumerate(root_files, start=1):
    print(f"[{idx}/{file_count}] processing...")
    for macro in macros:
        macro_base_name = macro.replace("csv_", "").replace(".cxx", "")
        out_file = f.with_name(f.name.replace(".edm4eic.root",  f".{macro_base_name}.csv"))

        print(f"  {macro}  {f.name} → {out_file.name}")
        cmd = [
            "root", "-x", "-l", "-b", "-q",
            f'{macro}("{f}","{out_file}")'
        ]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed on {f.name}: exit code {e.returncode}")
            sys.exit(1)

print(f"\n[OK] Successfully processed {file_count} files. Output CSVs are alongside the ROOT files.")
