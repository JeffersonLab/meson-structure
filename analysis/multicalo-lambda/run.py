from __future__ import annotations

import argparse
from pathlib import Path

from config import DEFAULT_CONST, DEFAULT_PATHS
from studies_lambda import (
    plot_angle_distrib,
    plot_lambda_spectra,
    plot_efficiencies,
    plot_nlambda_vs_kinematics_all,
)
from studies_kaon_sf import plot_relerr_kaon_sf_xK_Q2


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Multi-calo Lambda / Kaon-SF studies")
    p.add_argument("--inputs", type=Path, default=DEFAULT_PATHS.inputs)
    p.add_argument("--outputs", type=Path, default=DEFAULT_PATHS.outputs)
    p.add_argument("--suffix", type=str, default="testall_calocalib_verification")
    p.add_argument("--nfiles", type=int, default=1)
    p.add_argument("--bins", type=int, default=50)
    p.add_argument("--beam", type=str, default="5x41", choices=list(DEFAULT_CONST.energies))
    p.add_argument("--task", type=str, default="all",
                   choices=["all", "angles", "spectra", "eff", "kin", "relerr"])
    p.add_argument("--with-beta", action="store_true")
    p.add_argument("--tmax", type=float, default=None)
    p.add_argument("--lumin-fb", type=float, default=1.0)
    p.add_argument("--logQ2", action="store_true")
    p.add_argument("--gen-dir", type=Path, default=DEFAULT_PATHS.gen_base_dir)
    return p


def main() -> None:
    args = build_parser().parse_args()

    inputs = args.inputs
    outputs = args.outputs
    suffix = args.suffix
    nfiles = args.nfiles
    nbins = args.bins
    beam = args.beam

    after_pattern = DEFAULT_PATHS.afterburner_pattern

    # 1) angles
    if args.task in ("angles", "all"):
        out = plot_angle_distrib(
            nfiles=nfiles,
            bins=30,
            root_base_dir=inputs,
            suffix=suffix,
            outdir=outputs,
            afterburner_pattern=after_pattern,
            energies=tuple(DEFAULT_CONST.energies),
        )
        print("Saved:", out)

    # 2) spectra
    if args.task in ("spectra", "all"):
        for b in DEFAULT_CONST.energies:
            xmax = float(b.split("x")[-1]) * 2.0
            out = plot_lambda_spectra(
                beam=b,
                xmax=xmax,
                nfiles=nfiles,
                bins=nbins,
                root_base_dir=inputs,
                suffix=suffix,
                outdir=outputs,
                afterburner_pattern=after_pattern,
                logy=True,
            )
            print("Saved:", out)

    # 3) efficiencies
    if args.task in ("eff", "all"):
        out = plot_efficiencies(
            nfiles_5x41=nfiles,
            nfiles_10x100=nfiles,
            nfiles_18x275=nfiles,
            bins_5x41=10,
            bins_10x100=10,
            bins_18x275=10,
            root_base_dir=inputs,
            suffix_new=suffix,
            suffix_old="testall_calocalib_ZDConly",
            outdir=outputs,
            with_beta=args.with_beta,
            tag=suffix,
        )
        print("Saved:", out)

    # 4) kinematics
    if args.task in ("kin", "all"):
        for b in DEFAULT_CONST.energies:
            plot_nlambda_vs_kinematics_all(
                beam=b,
                nfiles=nfiles,
                root_base_dir=inputs,
                suffix=suffix,
                outdir=outputs,
                tag=suffix,
                xB_bins=nbins,
                xB_range=(0, 2),
                xK_bins=nbins,
                xK_range=(0, 2),
                Q2_bins=nbins,
                Q2_range=(1, 3e3),
                log_Q2=True,
                logz=True,
                tmax=args.tmax,
            )
            print("Saved kinematics for", b)

    # 5) relerr kaon SF
    if args.task in ("relerr", "all"):
        for b in DEFAULT_CONST.energies:
            plot_relerr_kaon_sf_xK_Q2(
                beam=b,
                nfiles=nfiles,
                root_base_dir=inputs,
                suffix=suffix,
                gen_base_dir=args.gen_dir,
                outdir=outputs,
                tag=suffix,
                xK_bins=nbins,
                xK_range=(0, 3.0),
                Q2_bins=nbins,
                Q2_range=(1.0, 550.0),
                xB_bins=nbins,
                xB_range=(0.0, 1.0),
                lumin_fb=args.lumin_fb,
                log_Q2=args.logQ2,
                tmax=args.tmax,
            )
            print("Saved relerr for", b)


if __name__ == "__main__":
    main()