# from pathlib import Path
# import os
# import lhapdf


# name = "JAM19FF_kaon_nlo"
# pdf = lhapdf.mkPDF(name, 0)

# print("Set:", name)
# print("x range:", pdf.xMin(), pdf.xMax())
# print("Q2 range:", pdf.q2Min(), pdf.q2Max())
# print("flavors:", pdf.flavors())

# # Try to locate .info file
# datapath = os.environ.get("LHAPDF_DATA_PATH", "")
# candidates = [Path(p) for p in datapath.split(":") if p]
# for base in candidates:
#     info = base / name / f"{name}.info"
#     if info.exists():
#         print("\nINFO FILE:", info)
#         print(info.read_text()[:1200])
#         break
# else:
#     print("\nCould not locate .info file via LHAPDF_DATA_PATH.")


from __future__ import annotations

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from kaon_studies import make_kaon_pdf_func, F2_from_pdf_func
from physics import ToyParams, KaonModelParams
from config import setup_lhapdf_env, get_pion_pdfset, get_pion_pdfmember
setup_lhapdf_env()
pion_set = get_pion_pdfset()
pion_member = get_pion_pdfmember()

# suppose que tu as déjà :
# - build_kaon_model(model_kind, ...)
# - F2_from_pdf_func(pdf_func, x, Q2)
# - apply_mpl_style()

# colorss = ['black', 'darkorange', 'cadetblue', 'darkred']
colorss = ['black', 'blue', 'gold', 'darkgreen']

TOY_MODEL_LABELS = {
    # "toy_baseline": "Baseline",
    # "toy_soft_valence": "Soft valence",
    # "toy_hard_valence": "Hard valence",
    # "toy_sea_enhanced": "Sea enhanced",
    # "toy_su3_breaking": "SU(3) breaking",

    "smrs": "SMRS (ansatz)",
    "grv_grs": "GRV-GRS (ansatz)",
    "jam_grs": "JAM-GRS (ansatz)",
    "dse": "DSE (ansatz)",
}

def plot_toy_models_vs_x(
    Q2: float,
    outpath: str | Path | None = None,
    xmin: float = 1e-3,
    xmax: float = 0.95,
    nx: int = 400,
    logx: bool = True,
):
    """
    Plot F2^K(x,Q2) vs x for the toy models on a single figure.
    """

    # apply_mpl_style()  # décommente si tu veux ton style global

    model_kinds = [
        # "toy_baseline",
        # "toy_hard_valence",
        # "toy_sea_enhanced",
        # "toy_su3_breaking",
        "smrs",
        "grv_grs", 
        "jam_grs", 
        "dse"
    ]

    if logx:
        xgrid = np.logspace(np.log10(xmin), np.log10(xmax), nx)
    else:
        xgrid = np.linspace(xmin, xmax, nx)

    fig, ax = plt.subplots(figsize=(7,5))

    i = 0

    for model_kind in model_kinds:

        # adapte cette ligne à ton builder exact
        pdf_func = make_kaon_pdf_func(
            model=model_kind, toy=ToyParams, kparams=KaonModelParams,
            pion_set=pion_set, pion_member=pion_member, require_lhapdf=True)

        y = np.array([F2_from_pdf_func(pdf_func, x, Q2) for x in xgrid])
        # y_u = np.array([x * (4.0/9.0) * pdf_func(2, x, Q2) for x in xgrid])
        # y_sbar = np.array([x * (1.0/9.0) * pdf_func(-3, x, Q2) for x in xgrid])
        # y_tot = y_u + y_sbar

        ax.plot(
            xgrid,
            y,
            lw=2.2,
            label=TOY_MODEL_LABELS.get(model_kind, model_kind),
            color=colorss[i]
        )

        # ax.plot(
        #     xgrid,
        #     y_sbar,
        #     lw=2.2,
        #     # label=TOY_MODEL_LABELS.get(model_kind, model_kind),
        #     color='gray'
        # )

        # ax.plot(
        #     xgrid,
        #     y_u,
        #     lw=2.2,
        #     # label=TOY_MODEL_LABELS.get(model_kind, model_kind),
        #     color='black'
        # )

        i+=1

    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$F$")
    ax.set_xticks([0,0.5,1])
    # ax.set_title(rf"Toy kaon structure-function models at $Q^2 = {Q2:g}\ \mathrm{{GeV}}^2$")
    ax.legend(frameon=False)

    # if logx:
    #     ax.set_xscale("log")

    # ax.grid(True, alpha=0.3)
    fig.tight_layout()

    if outpath is not None:
        outpath = Path(outpath)
        outpath.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(outpath, dpi=300, bbox_inches="tight")

    return fig, ax

plot_toy_models_vs_x(
    Q2=10.0,
    outpath="outputs/vizu_realmodels.png",
)