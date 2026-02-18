#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


help_txt = """
runs csv_*.cxx on every *.edm4hep.root file

Usage:
    python3 convert_edm4hep.py [directory]

Arguments (all optional)
    directory : where to search for ROOT files
"""


# --- Config ---

if len(sys.argv) < 2:
    print("Provide directory path as an argument.")
    print(help_txt)
    exit(1)

input_dir = Path(sys.argv[1])
macros = [
    "csv_edm4hep_acceptance_npi0.cxx",
    "csv_edm4hep_acceptance_ppim.cxx",
]


# --- Find files ---
root_files = sorted(input_dir.glob("*.edm4hep.root"))
file_count = len(root_files)
if file_count == 0:
    sys.exit(f"[ERROR] No *.edm4hep.root files found in {input_dir}")

print(f"[INFO] Found {file_count} .edm4hep.root files in {input_dir}\n")

# ------------------------------------------------------------------ run loop
for idx, file_path in enumerate(root_files, start=1):
    print(f"[{idx}/{file_count}] ============================================")
    for macro in macros:
        macro_base_name = macro.replace("csv_", "").replace(".cxx", "")
        out_file = file_path.with_name(file_path.name.replace(".edm4hep.root",  f".{macro_base_name}.csv"))
        if out_file.exists():
            print(f"[SKIP] {out_file.name} already exists, skipping")
            continue

        print(f"|{macro}|  {file_path.name} → {out_file.name}")
        cmd = [
            "root", "-x", "-l", "-b", "-q",
            f'{macro}("{file_path}","{out_file}")'
        ]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed on {file_path.name}: exit code {e.returncode}")
            sys.exit(1)
    print(f"---> Finished converting: {file_path.name}")
print(f"\n[OK] Successfully processed {file_count} files. Output CSVs are alongside the ROOT files.")
