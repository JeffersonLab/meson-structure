from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np

from config import CONST, PATHS

from lambda_studies import (
    plot_angle_distrib,
    plot_lambda_spectra,
    plot_efficiencies,
    plot_nlambda_vs_kinematics_all,
)
from kaon_models import (
    evaluate_and_plot_F2K, 
    EvalConfig
) 
from kaon_studies import (
    plot_relerr_kaon_sf_xK_Q2, 
    plot_F2K_xK_slices_with_attached_errors,
    plot_discriminant_kaon_sf_xK_Q2,
    plot_ratio_kaon_sf_xK_Q2,
    plot_jam_reweighting_constraining_power_xK_slices,
    plot_neff_reduction_vs_lumi_by_beam
)
from uq import (
    compute_local_fischer_maps, 
    compute_local_fischer,
)
from plotting import (
    apply_mpl_style, 
    get_color, get_style, 
    plot_fischer_matrix_maps
)

KAON_MODELS = [ 
                # toy models
                "toy_baseline", 
                "toy_soft_valence", 
                "toy_hard_valence", 
                "toy_sea_enhanced", 
                "toy_su3_breaking",
                # JAM models
                "jam25_rep165",
                "jam25_rep390",
                "jam25_rep400",
                "jam25_mean", 
                # theoretical models
                "cosmao22",
            ]


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Multi-calo Lambda / Kaon-SF studies")
    p.add_argument("--inputs", type=Path, default=PATHS.inputs)
    p.add_argument("--outputs", type=Path, default=PATHS.outputs)
    p.add_argument("--suffix", type=str, default="testall_calocalib_verification")
    p.add_argument("--nfiles", type=int, default=1)
    p.add_argument("--bins", type=int, default=10)
    p.add_argument("--beam", type=str, default="5x41", choices=list(CONST.energies))
    p.add_argument("--task", type=str, default="all",
                   choices=["all", 
                            "angles", 
                            "spectra", 
                            "eff", 
                            "kin", 
                            "models", 
                            "relerr", 
                            "discri", 
                            "toymodels", 
                            "replicas"])
    p.add_argument("--with-beta", action="store_true")
    p.add_argument("--tmax", type=float, default=None)
    p.add_argument("--lumin-fb", type=float, default=1.0)
    p.add_argument("--logQ2", action="store_true")
    p.add_argument("--gen-dir", type=Path, default=PATHS.gen_base_dir)
    return p


def main() -> None:

    args = build_parser().parse_args()

    inputs = args.inputs
    outputs = args.outputs
    suffix = args.suffix
    nfiles = args.nfiles
    nbins = args.bins
    beam = args.beam

    after_pattern = PATHS.afterburner_pattern

    # 1) angles

    if args.task in ("angles", "all"):

        out = plot_angle_distrib(
            nfiles=nfiles,
            bins=30,
            root_base_dir=inputs,
            suffix=suffix,
            outdir=outputs,
            afterburner_pattern=after_pattern,
            energies=tuple(CONST.energies),
        )
        print("Saved angular distributions")

    # 2) spectra

    if args.task in ("spectra", "all"):

        for b in CONST.energies:

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
            print(f"Saved Lambda spectra | {b}")

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
        print(f"Saved efficiencies maps")

    # 4) kinematics

    if args.task in ("kin", "all"):

        for b in CONST.energies:

            for kinme in ['Truth', 'Electron', 'JB']:

                plot_nlambda_vs_kinematics_all(
                    beam=b,
                    nfiles=nfiles,
                    root_base_dir=inputs,
                    suffix=suffix,
                    outdir=outputs,
                    tag=suffix,
                    xB_bins=nbins,
                    xB_range=(0, 1),
                    xK_bins=nbins,
                    xK_range=(0, 1),
                    Q2_bins=nbins,
                    Q2_range=(1, 500),
                    log_Q2=False,
                    logz=True,
                    tmax=args.tmax,
                    kinmethod=kinme
                )
                print(f"Saved kinematics maps | {b}")

    # 5) kaon SF evaluation

    if args.task in ("models", "all"):

        for m in KAON_MODELS:

            out_eval = evaluate_and_plot_F2K(EvalConfig(model=m))

            if out_eval:
                print("Saved:", out_eval)

    # 6) relerr kaon SF

    if args.task in ("relerr", "all"):

        for b in CONST.energies:

            for kime in ['Truth', 'Electron', 'JB']:

            # relative error heatmap

                relerr_xB_Q2, relerr_xK_Q2, meta = plot_relerr_kaon_sf_xK_Q2(
                    beam=b,
                    nfiles=nfiles,
                    root_base_dir=inputs,
                    suffix=suffix,
                    gen_base_dir=args.gen_dir,
                    outdir=outputs,
                    tag=suffix,
                    xK_bins=nbins,
                    xK_range=(1e-3, 1.0),
                    Q2_bins=nbins,
                    Q2_range=(1, 100.0),
                    xB_bins=nbins,
                    xB_range=(1e-3, 1.0),
                    lumin_fb=args.lumin_fb,
                    log_Q2=True,#args.logQ2,
                    log_x=True,
                    tmax=args.tmax,
                    vmax_percent=100.0,
                    kinmethod=kime,
                )
                print(f"Saved relative error maps | {b}")

            # fischer matrix and covariance

            # res_fisher = compute_local_fischer_maps(
            #     a0=0.5,
            #     b0=1.5,
            #     relerr_xK_Q2=relerr_xK_Q2,
            #     xK_range=(0, 1),
            #     xK_bins=nbins,
            #     Q2_range=(1, 500),
            #     Q2_bins=nbins,
            #     model="toy_baseline",
            #     da=1e-2,
            #     db=1e-2,
            #     log_Q2_centers=False, #args.logQ2,
            # )

            # plot_fischer_matrix_maps(
            #     info_aa=res_fisher["info_aa"],
            #     info_ab=res_fisher["info_ab"],
            #     info_bb=res_fisher["info_bb"],
            #     xK_range=(0, 1),
            #     xK_bins=nbins,
            #     Q2_range=(1, 500),
            #     Q2_bins=nbins,
            #     log_Q2=False, #args.logQ2,
            #     outdir=outputs,
            #     outname=f"fisher_matrix_maps_{b}_L{args.lumin_fb}fb.png",
            #     title=r"Local Fisher information for toy-model around $\theta=(a,b)=(0.5,1.5)$",
            # )

    # 7) models discrimination heatmaps

    if args.task in ("discri", "all"):

        for b in CONST.energies:

            for modelb in KAON_MODELS:

                chi2, relerr_xK_Q2, (F2A, F2B) = plot_discriminant_kaon_sf_xK_Q2(
                    beam=b,
                    nfiles=nfiles,
                    root_base_dir=inputs,
                    suffix=suffix,
                    gen_base_dir=args.gen_dir,
                    outdir=outputs,
                    tag=suffix,
                    xK_bins=nbins,
                    xK_range=(0.0, 1.0),
                    Q2_bins=nbins,
                    Q2_range=(1.0, 500.0),
                    xB_bins=nbins,
                    xB_range=(0.0, 1.0),
                    lumin_fb=args.lumin_fb,
                    log_Q2=args.logQ2,
                    tmax=args.tmax,
                    modelA="toy_baseline",
                    modelB=modelb,
                    sigma_ref="mean",
                    vmax=3,
                )
                print(f"Saved chi2 map | toy_baseline vs. {modelb} | {b}")

    # 8) toy models study

    if args.task in ("toymodels", "all"):

        for b in CONST.energies:

            for slicing in [(10,100)]:

                for kime in ['Truth', 'Electron', 'JB']:

                    # toy models 
                    plot_ratio_kaon_sf_xK_Q2(
                        beam=b,
                        nfiles=nfiles,
                        root_base_dir=inputs,
                        suffix=suffix,
                        gen_base_dir=args.gen_dir,
                        outdir=outputs,
                        tag=suffix,
                        ref_model="toy_baseline",
                        models_to_compare=[
                            "toy_soft_valence",
                            "toy_hard_valence",
                            "toy_sea_enhanced",
                            "toy_su3_breaking",
                        ],
                        q2_slices=[slicing],
                        xK_bins=nbins,
                        xK_range=(1e-3, 1.0),
                        Q2_bins=nbins,
                        Q2_range=(1e-3, 500.0),
                        xB_bins=nbins,
                        xB_range=(1e-3, 1.0),
                        log_Q2=args.logQ2,
                        logx=True,
                        tmax=args.tmax,
                        lumin_fb=args.lumin_fb,
                        title = f"{b} GeV | {args.lumin_fb} fb$^{{-1}}$ | {kime} kinematics",
                        outname=f"Ratio_toymodels_{b}_{args.lumin_fb}fb_Q2_{slicing}_{kime}.png",
                        ymin=0.,
                        ymax=2.5,
                        kinmethod=kime
                    )
                    print(f"Saved ratio toy models | Q2 {slicing} @ {b} | {kime} kinematicss")

    # 9) literature models (JAM, DSE)

    if args.task in ("replicas", "all"):

        components = ["total", "valence", "sea"]

        component_title = {
            "total": "Total F2K",
            "valence": "Valence F2K",
            "sea": "Quark-sea",
            "gluon": "Gluon-sea",
        }

        for slicing in [(10, 100)]:

            for kime in ["Electron", "JB"]:

                reweighting_results_by_beam = {}

                for b in CONST.energies:

                    # discrimination JAM replicas

                    plot_ratio_kaon_sf_xK_Q2(
                        beam=b,
                        nfiles=nfiles,
                        root_base_dir=inputs,
                        suffix=suffix,
                        gen_base_dir=args.gen_dir,
                        outdir=outputs,
                        tag=suffix,
                        ref_model="jam25_mean",
                        models_to_compare=["jam25_rep400"],
                        q2_slices=[slicing],
                        xK_bins=nbins,
                        xK_range=(1e-3, 1.0),
                        Q2_bins=nbins,
                        Q2_range=(1e-3, 500.0),
                        xB_bins=nbins,
                        xB_range=(1e-3, 1.0),
                        log_Q2=args.logQ2,
                        logx=True,
                        tmax=args.tmax,
                        lumin_fb=args.lumin_fb,
                        title=f"{b} GeV | {args.lumin_fb} fb$^{{-1}}$ | {kime} kinematics",
                        outname=f"Ratio_JAM-JAM_{b}_{args.lumin_fb}fb_Q2_{slicing}_{kime}.png",
                        ymin=0.0,
                        ymax=2.5,
                        kinmethod=kime,
                    )

                    print(f"Saved ratio replicas | Q2 {slicing} @ {b} | {kime} kinematics")

                    # discrimination JAM/DSE

                    plot_ratio_kaon_sf_xK_Q2(
                        beam=b,
                        nfiles=nfiles,
                        root_base_dir=inputs,
                        suffix=suffix,
                        gen_base_dir=args.gen_dir,
                        outdir=outputs,
                        tag=suffix,
                        ref_model="jam25_mean",
                        models_to_compare=["cosmao22"],
                        q2_slices=[slicing],
                        xK_bins=nbins,
                        xK_range=(1e-3, 1.0),
                        Q2_bins=nbins,
                        Q2_range=(1e-3, 500.0),
                        xB_bins=nbins,
                        xB_range=(1e-3, 1.0),
                        log_Q2=args.logQ2,
                        logx=True,
                        tmax=args.tmax,
                        lumin_fb=args.lumin_fb,
                        title=f"{b} GeV | {args.lumin_fb} fb$^{{-1}}$ | {kime} kinematics",
                        outname=f"Ratio_JAM-DSE_{b}_{args.lumin_fb}fb_Q2_{slicing}_{kime}.png",
                        ymin=0.0,
                        ymax=2.5,
                        kinmethod=kime,
                    )

                    print(f"Saved ratio DSE | Q2 {slicing} @ {b} | {kime} kinematics")

                    # constraining power JAM replicas

                    # for comp in components:

                    #     reweighting_res = plot_jam_reweighting_constraining_power_xK_slices(
                    #         beam=b,
                    #         nfiles=nfiles,
                    #         root_base_dir=inputs,
                    #         suffix=suffix,
                    #         gen_base_dir=args.gen_dir,
                    #         outdir=outputs,
                    #         tag=suffix,
                    #         q2_slices=[slicing],
                    #         xK_bins=nbins,
                    #         xK_range=(1e-3, 1.0),
                    #         Q2_bins=nbins,
                    #         Q2_range=(1e-3, 500.0),
                    #         xB_bins=nbins,
                    #         xB_range=(1e-3, 1.0),
                    #         log_Q2=args.logQ2,
                    #         logx=True,
                    #         tmax=args.tmax,
                    #         lumin_fb=[5, 10, 50],
                    #         kinmethod=kime,
                    #         component=comp,
                    #         title=f"{component_title[comp]} | {b} GeV | {kime} kinematics",
                    #         outname=f"Reweighting_replicas_{comp}_{b}_5-10-50fb_Q2_{slicing}_{kime}.png",
                    #     )

                    #     print(f"Saved JAM reweighting | component {comp} | Q2 {slicing} @ {b} | {kime} kinematics")

                    #     if comp == "total":
                    #         reweighting_results_by_beam[b] = reweighting_res

                # plot_neff_reduction_vs_lumi_by_beam(
                #     reweighting_results_by_beam,
                #     outdir=outputs,
                #     title=f"$Q^2$ = {slicing[0]}–{slicing[1]} GeV$^2$ | {kime} kinematics",
                #     outname=f"Neff_reduction_by_beam_5-10-50fb_Q2_{slicing}_{kime}.png",
                # )

                # print(f"Saved replicas reduction | Q2 {slicing} | {kime} kinematics")

# main

if __name__ == "__main__":
    main()