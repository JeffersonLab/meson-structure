from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal
import math
import numpy as np

from config import (
    setup_lhapdf_env,
    get_pion_pdfset,
    get_pion_pdfmember,
    GRID_DEFAULTS,
)
from plotting import (
    apply_mpl_style, 
    plot_F2_map
)
from physics import (
    ToyParams, 
    KaonModelParams, 
    F2_from_pdf_func, 
    toy_norm, 
    toy_shape_x
)
from utils import (
    Grid,
    is_lhapdf_available,
    make_pdf_kaon_toy_times_pion_evolution,
    make_lin_grid,
    make_log_grid,
    compute_F2_grid,
)

# global

GridKind = Literal["lin", "log"]

ModelKind = Literal[ 
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

JAM_REPLICA_MODELS: dict[str, int] = {
    "jam25_rep165": 165,
    "jam25_rep390": 390,
    "jam25_rep400": 400,
}

# configuration call

@dataclass(frozen=True)
class EvalConfig:
    grid_kind: GridKind = "lin"
    grid_overrides: dict[str, float | int] | None = None

    model: ModelKind = "toy_baseline"
    toy: ToyParams = ToyParams(a=0.5, b=1.5, Q0=0.5)
    kparams: KaonModelParams = KaonModelParams()

    prefix: str | None = None


def build_grid(kind: GridKind = "lin", overrides: dict[str, float | int] | None = None) -> Grid:
    params = dict(GRID_DEFAULTS)
    if overrides:
        params.update(overrides)

    if kind == "log":
        return make_log_grid(**params)
    if kind == "lin":
        return make_lin_grid(**params)
    raise ValueError(f"Unknown grid kind: {kind}")


# model builders

PdfFunc = Callable[[int, float, float], float]

def _make_toy_valence_pdf(toy: ToyParams) -> PdfFunc:
    """
    Simplistic K+ valence-only PDF at Q0:
    u(x) ~ sbar(x) ~ x^a (1-x)^b normalized to 1
    """
    a, b = toy.a, toy.b
    norm = toy_norm(a, b)

    def pdf(pid: int, x: float, Q2: float) -> float:
        if pid in (2, -3):   # u, sbar
            return toy_shape_x(x, a, b, norm)
        return 0.0

    return pdf

def _make_pdf_from_lhapdf(setname: str, member: int = 0) -> PdfFunc:
    import lhapdf
    pdfset = lhapdf.mkPDF(setname, member)

    def pdf(pid: int, x: float, Q2: float) -> float:
        if x <= 0.0 or x >= 1.0 or Q2 <= 0.0:
            return 0.0
        return pdfset.xfxQ2(pid, x, Q2) / x

    return pdf

# theoretical model (DSE)

def make_pdf_kaon_cosmao22(
    setname: str = "CoSMAO22Kaon",
    member: int = 0,
) -> PdfFunc:
    """
    CoSMAO22 K+ PDFs from LHAPDF.

    LHAPDF set:
      CoSMAO22Kaon, ID 9950, Particle 321 = K+

    Returns f(x,Q2), not x*f(x,Q2).
    """
    return _make_pdf_from_lhapdf(setname, member)


def _get_pion_uval(pdf_pi: PdfFunc, pion_set: str, x: float, Q2: float) -> float:
    u_pi = pdf_pi(2, x, Q2)
    ubar_pi = pdf_pi(-2, x, Q2)

    if pion_set == "GRVPI0":
        return max(u_pi, 0.0)
    else:
        return max(u_pi - ubar_pi, 0.0)


# JAM model

F2KComponent = Literal["total", "valence", "sea", "gluon"]
JAM_F2K_FLAVS = [21, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
_JAM_PDFS_CACHE: dict[str, list] = {}

def _get_jam_pdfset(setname: str = "JAM25kaon_nlonll_F2K"):
    setup_lhapdf_env()
    import lhapdf

    if setname not in _JAM_PDFS_CACHE:
        _JAM_PDFS_CACHE[setname] = lhapdf.mkPDFs(setname)

    return _JAM_PDFS_CACHE[setname]


def get_n_jam_replicas(setname: str = "JAM25kaon_nlonll_F2K") -> int:
    return len(_get_jam_pdfset(setname))


def make_f2k_jam_replica(replica: int, setname: str = "JAM25kaon_nlonll_F2K"):
    JAM_F2K_FLAVS = [21, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
    pdfs = _get_jam_pdfset(setname)

    if replica < 0 or replica >= len(pdfs):
        raise ValueError(
            f"Replica index {replica} out of range for set {setname} "
            f"(available: 0..{len(pdfs)-1})"
        )

    grid = pdfs[replica]

    def f2k(x: float, Q2: float) -> float:
        if x <= 0.0 or x >= 1.0 or Q2 <= 0.0:
            return np.nan

        vals = np.array([grid.xfxQ2(f, x, Q2) for f in JAM_F2K_FLAVS], dtype=float)
        if not np.all(np.isfinite(vals)):
            return np.nan

        return float(np.sum(vals))

    return f2k


def get_all_jam_replica_ids(setname: str = "JAM25kaon_nlonll_F2K") -> list[int]:
    return list(range(get_n_jam_replicas(setname)))


def evaluate_f2k_for_jam_replicas(
    replica_ids: list[int],
    x_arr: np.ndarray,
    q2_arr: np.ndarray,
    setname: str = "JAM25kaon_nlonll_F2K",
) -> np.ndarray:
    pdfs = _get_jam_pdfset(setname)
    JAM_F2K_FLAVS = [21, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5]

    x_arr = np.asarray(x_arr, dtype=float)
    q2_arr = np.asarray(q2_arr, dtype=float)

    out = np.full((len(replica_ids), len(x_arr), len(q2_arr)), np.nan, dtype=float)

    for irep, rep in enumerate(replica_ids):
        if rep < 0 or rep >= len(pdfs):
            raise ValueError(
                f"Replica index {rep} out of range for set {setname} "
                f"(available: 0..{len(pdfs)-1})"
            )

        grid = pdfs[rep]

        for j, q2 in enumerate(q2_arr):
            for i, x in enumerate(x_arr):
                if x <= 0.0 or x >= 1.0 or q2 <= 0.0:
                    continue

                vals = np.array([grid.xfxQ2(f, x, q2) for f in JAM_F2K_FLAVS], dtype=float)
                if np.all(np.isfinite(vals)):
                    out[irep, i, j] = float(np.sum(vals))

    return out


def is_jam_replica_model(model: str) -> bool:
    return model in JAM_REPLICA_MODELS or model == "jam25_mean"


def get_jam_f2k_flavor_values(grid, x: float, Q2: float) -> dict[str, float]:
    """
    Return LHAPDF-style F2K flavor contributions for a JAM replica grid.

    Important:
    These are not PDFs q(x,Q2), but flavor contributions to F2K.
    """
    pid_to_name = {
        21: "g",
        -5: "bb",
        -4: "cb",
        -3: "sb",
        -2: "ub",
        -1: "db",
         1: "d",
         2: "u",
         3: "s",
         4: "c",
         5: "b",
    }

    vals = {}
    for pid, name in pid_to_name.items():
        vals[name] = float(grid.xfxQ2(pid, x, Q2))

    return vals

def compute_jam_f2k_component(
    flav: dict[str, float],
    component: F2KComponent = "total",
) -> float:
    """
    Compute total, valence, sea, or gluon contribution to F2K
    from JAM LHAPDF-style flavor contributions.

    For K-:
      valence = (s - sb) + (ub - u)
      sea     = 2*u + d + db + 2*sb + (c + cb + b + bb)
      gluon   = g
    """

    if component == "total":
        return sum(flav.values())

    if component == "valence":
        return (flav["s"] - flav["sb"]) + (flav["ub"] - flav["u"])

    if component == "sea":
        return (
            2.0 * flav["u"]
            + flav["d"]
            + flav["db"]
            + 2.0 * flav["sb"]
            + flav["c"]
            + flav["cb"]
            + flav["b"]
            + flav["bb"]
        )

    if component == "gluon":
        return flav["g"]

    raise ValueError(
        f"Unknown component '{component}'. "
        "Use 'total', 'valence', 'sea', or 'gluon'."
    )


def make_f2k_jam_replica_component(
    replica: int,
    component: F2KComponent = "total",
    setname: str = "JAM25kaon_nlonll_F2K",
):
    pdfs = _get_jam_pdfset(setname)

    if replica < 0 or replica >= len(pdfs):
        raise ValueError(
            f"Replica index {replica} out of range for set {setname} "
            f"(available: 0..{len(pdfs)-1})"
        )

    grid = pdfs[replica]

    def f2k_component(x: float, Q2: float) -> float:
        if x <= 0.0 or x >= 1.0 or Q2 <= 0.0:
            return np.nan

        flav = get_jam_f2k_flavor_values(grid, x, Q2)

        if not np.all(np.isfinite(list(flav.values()))):
            return np.nan

        return float(compute_jam_f2k_component(flav, component))

    return f2k_component


def evaluate_f2k_component_for_jam_replicas(
    replica_ids: list[int],
    x_arr: np.ndarray,
    q2_arr: np.ndarray,
    component: F2KComponent = "total",
    setname: str = "JAM25kaon_nlonll_F2K",
) -> np.ndarray:
    pdfs = _get_jam_pdfset(setname)

    x_arr = np.asarray(x_arr, dtype=float)
    q2_arr = np.asarray(q2_arr, dtype=float)

    out = np.full((len(replica_ids), len(x_arr), len(q2_arr)), np.nan, dtype=float)

    for irep, rep in enumerate(replica_ids):
        if rep < 0 or rep >= len(pdfs):
            raise ValueError(
                f"Replica index {rep} out of range for set {setname} "
                f"(available: 0..{len(pdfs)-1})"
            )

        grid = pdfs[rep]

        for j, q2 in enumerate(q2_arr):
            for i, x in enumerate(x_arr):
                if x <= 0.0 or x >= 1.0 or q2 <= 0.0:
                    continue

                flav = get_jam_f2k_flavor_values(grid, x, q2)

                if np.all(np.isfinite(list(flav.values()))):
                    out[irep, i, j] = compute_jam_f2k_component(
                        flav,
                        component=component,
                    )

    return out


def make_f2k_jam_mean(setname: str = "JAM25kaon_nlonll_F2K"):
    pdfs = _get_jam_pdfset(setname)

    def f2k_mean(x: float, Q2: float) -> float:
        if x <= 0.0 or x >= 1.0 or Q2 <= 0.0:
            return np.nan

        vals = []

        for grid in pdfs:
            flavs = np.array([grid.xfxQ2(f, x, Q2) for f in JAM_F2K_FLAVS], dtype=float)
            if np.all(np.isfinite(flavs)):
                vals.append(np.sum(flavs))

        if len(vals) == 0:
            return np.nan

        return float(np.mean(vals))

    return f2k_mean

# make structure function

def make_kaon_pdf_func(
    model: ModelKind,
    toy: ToyParams,
    kparams: KaonModelParams,
    *,
    pion_set: str,
    pion_member: int,
    require_lhapdf: bool = True,
) -> PdfFunc:
    """
    Build a kaon PDF model as a function pdf(pid, x, Q2) -> f(x,Q2).
    """

    # theorerical models

    if model == "cosmao22":
        return make_pdf_kaon_cosmao22(
            setname="CoSMAO22Kaon",
            member=0,
        )

    # toy models 

    a = toy.a
    b = toy.b

    if model == "toy_soft_valence":
        b = toy.b + float(kparams.db_soft_valence)

    elif model == "toy_hard_valence":
        b = toy.b + float(kparams.db_hard_valence)
        b = max(b, 0.05)

    elif model in ("toy_baseline", "toy_su3_breaking", "toy_sea_enhanced"):
        pass

    else:
        raise ValueError(
            f"Unknown model: {model}. "
            "Use: toy_baseline, toy_soft_valence, toy_hard_valence, "
            "toy_sea_enhanced or toy_su3_breaking."
        )

    toy_eff = ToyParams(a=a, b=b, Q0=toy.Q0)

    # pdf

    if require_lhapdf:
        pdf_base = make_pdf_kaon_toy_times_pion_evolution(
            toy_eff,
            pion_set=pion_set,
            member=pion_member,
        )
    else:
        pdf_base = _make_toy_valence_pdf(toy_eff)

    # pdf toy models 

    if model in ("toy_baseline", "toy_soft_valence", "toy_hard_valence"):
        return pdf_base

    if model == "toy_su3_breaking":
        a_u, b_u = toy_eff.a, toy_eff.b
        norm_u = toy_norm(a_u, b_u)

        a_s = a_u + float(kparams.da_sbar_su3_break)
        b_s = b_u + float(kparams.db_sbar_su3_break)
        b_s = max(b_s, 0.05)
        norm_s = toy_norm(a_s, b_s)

        def pdf_su3(pid: int, x: float, Q2: float) -> float:
            base = pdf_base(pid, x, Q2)

            if pid != -3:
                return base

            u0 = toy_shape_x(x, a_u, b_u, norm_u)
            s0 = toy_shape_x(x, a_s, b_s, norm_s)

            if u0 <= 0.0:
                return 0.0

            return base * (s0 / u0)

        return pdf_su3

    if model == "toy_sea_enhanced":
        sea_norm = toy_norm(kparams.sea_a, kparams.sea_b)

        def pdf_with_sea(pid: int, x: float, Q2: float) -> float:
            base = pdf_base(pid, x, Q2)
            sea = float(kparams.sea_amp) * toy_shape_x(
                x, kparams.sea_a, kparams.sea_b, sea_norm
            )

            if pid in (1, -1, 2, -2, 3, -3):
                return base + sea

            return base

        return pdf_with_sea

    raise ValueError(f"Unhandled model: {model}")
    

# compute structure function

def compute_F2_kaon_model(
    grid: Grid,
    model: ModelKind,
    toy: ToyParams,
    kparams: KaonModelParams,
    pion_set: str,
    pion_member: int,
) -> np.ndarray:

    # Direct F2K LHAPDF grids (JAM replicas)

    if model == "jam25_mean":
        f2k = make_f2k_jam_mean(setname="JAM25kaon_nlonll_F2K")

        return compute_F2_grid(
            grid,
            f2_point=lambda x, Q2: f2k(x, Q2),
        )

    if is_jam_replica_model(model):
        replica = JAM_REPLICA_MODELS[model]
        f2k = make_f2k_jam_replica(replica, setname="JAM25kaon_nlonll_F2K")

        return compute_F2_grid(
            grid,
            f2_point=lambda x, Q2: f2k(x, Q2),
        )

    # Standard PDF-based models

    pdf = make_kaon_pdf_func(
        model=model,
        toy=toy,
        kparams=kparams,
        pion_set=pion_set,
        pion_member=pion_member,
        require_lhapdf=True,
    )

    return compute_F2_grid(
        grid,
        f2_point=lambda x, Q2: F2_from_pdf_func(pdf, x, Q2),
    )

# high level structure function

def evaluate_and_plot_F2K(cfg: EvalConfig = EvalConfig()) -> str | None:
    """
    High-level entry point called by run.py.
    Returns output path as string, or None if skipped/failure.
    """
    setup_lhapdf_env()
    apply_mpl_style()

    if not is_lhapdf_available():
        print("WARNING: python lhapdf not available -> skipping plot.")
        return None

    pion_set = get_pion_pdfset()
    pion_member = get_pion_pdfmember()

    grid = build_grid(cfg.grid_kind, cfg.grid_overrides)

    try:
        F2 = compute_F2_kaon_model(
            grid=grid,
            model=cfg.model,
            toy=cfg.toy,
            kparams=cfg.kparams,
            pion_set=pion_set,
            pion_member=pion_member,
        )
    except Exception as e:
        print(f"WARNING: Cannot build/compute kaon model '{cfg.model}': {e}")
        return None

    prefix = cfg.prefix or f"F2K_{cfg.model}_times_{pion_set}"

    toy = cfg.toy
    k = cfg.kparams

    # legends

    title = {
        "toy_baseline":
            fr"Model $\mathbf{{toy\_baseline}}$: $u=s \propto x^a(1-x)^b$"
            "\n"
            fr"$a={toy.a:.2f},\; b={toy.b:.2f}$",

        "toy_soft_valence":
            fr"Model $\mathbf{{toy\_soft\_valence}}$: $u=s \propto x^a(1-x)^{{b+\Delta b}}$"
            "\n"
            fr"$a={toy.a:.2f},\; b={toy.b:.2f},\; \Delta b={k.db_soft_valence:+.2f}$",

        "toy_hard_valence":
            fr"Model $\mathbf{{toy\_hard\_valence}}$: $u=s \propto x^a(1-x)^{{b+\Delta b}}$"
            "\n"
            fr"$a={toy.a:.2f},\; b={toy.b:.2f},\; \Delta b={k.db_hard_valence:+.2f}$",

        "toy_sea_enhanced":
            fr"Model $\mathbf{{toy\_sea\_enhanced}}$: $u=s \propto x^a(1-x)^b + A_s x^{{a_s}}(1-x)^{{b_s}}$"
            "\n"
            fr"$a={toy.a:.2f},\; b={toy.b:.2f},\; A_{{sea}}={k.sea_amp:.3f},\; a_s={k.sea_a:.2f},\; b_s={k.sea_b:.2f}$",

        "toy_su3_breaking":
            fr"Model $\mathbf{{toy\_su3\_breaking}}$: $u \propto x^a(1-x)^b \neq s \propto x^{{a'}}(1-x)^{{b'}} $"
            "\n"
            fr"$a={toy.a:.2f},\; b={toy.b:.2f},\; a'=a+{k.da_sbar_su3_break:.2f},\; b'=b{k.db_sbar_su3_break:.2f}$",

        "jam25_rep165":
            r"Replica 165 (JAM)",

        "jam25_rep390":
            r"Replica 390 (JAM)",

        "jam25_rep400":
            r"Replica 400 (JAM)",

        "jam25_mean":
            r"Replica mean (JAM)",

        "cosmao22":
            fr"CoSMAO22 (Dyson-Schwinger)",

    }[cfg.model]

    # colorbar title

    if is_jam_replica_model(cfg.model):
        cbarlabel = r"$F_2^{K}(x,Q^2)$"
    else:
        cbarlabel = r"$F_2^K(x,Q^2) \approx x \left[ \frac{4}{9} u(x) + \frac{1}{9} s(x) \right] \times R_{\pi,\mathrm{LHAPDF}}(Q^2)$"
        
    out = plot_F2_map(
        prefix=prefix,
        grid=grid,
        F2=F2,
        title=title,
        cbar_label=cbarlabel,
        xscale='lin',
        q2scale='lin'
    )

    return str(out)
