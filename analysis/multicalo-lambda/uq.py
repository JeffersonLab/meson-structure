from __future__ import annotations

import numpy as np

from physics import (
    KaonModelParams, 
    ToyParams, 
    F2_from_pdf_func
)

from config import (
    setup_lhapdf_env,
    get_pion_pdfset,
    get_pion_pdfmember,
)

from kaon_models import (
    make_kaon_pdf_func,
)

def efficiency_from_counts(
    n_reco: np.ndarray,
    n_gen: np.ndarray,
    *,
    clip: bool = True,
) -> np.ndarray:
    """
    eps = n_reco / n_gen with safe handling (eps=0 when n_gen=0).
    """
    eps = np.zeros_like(n_gen, dtype=np.float64)
    m = n_gen > 0
    eps[m] = n_reco[m] / n_gen[m]
    if clip:
        eps = np.clip(eps, 0.0, 1.0)
    return eps


def expected_yields_nb(
    sigma_nb: np.ndarray,
    eps: np.ndarray,
    lumin_fb: float,
) -> np.ndarray:
    """
    Nexp = sigma(nb/bin) * eps * L(nb^-1), with L = lumin_fb * 1e6 (fb^-1 -> nb^-1).
    """
    L_nb_inv = float(lumin_fb) * 1e6
    return sigma_nb * eps * L_nb_inv


def relerr_combined(
    n_exp: np.ndarray,
    eps: np.ndarray,
    n_gen: np.ndarray,
) -> np.ndarray:
    """
    Relative uncertainty [%] combining:
      - Poisson counting on expected data: 1/sqrt(Nexp)
      - Binomial MC stat on eps: sqrt((1-eps)/(eps*Ngen))
      - ...

    Returns an array with NaN where undefined.
    """
    out = np.full_like(n_exp, np.nan, dtype=np.float64)

    okN = n_exp > 0
    ok_eps = (eps > 0) & (n_gen > 0)
    mask = okN & ok_eps
    if not np.any(mask):
        return out

    stat_term = 1.0 / np.sqrt(n_exp[mask])
    relerr_eps = np.sqrt((1.0 - eps[mask]) / (eps[mask] * n_gen[mask]))

    out[mask] = 100.0 * np.sqrt(stat_term**2) #100.0 * np.sqrt(stat_term**2 + relerr_eps**2)

    return out


def migration_probability_xk_given_xb_q2(M: np.ndarray) -> np.ndarray:
    """
    Build P(xK | xB, Q2) from counts M with shape (xK, xB, Q2).
    Normalizes over xK for each (xB,Q2). Where denom=0, leaves P=0.
    """
    denom = np.sum(M, axis=0)  # (xB,Q2)
    P = np.zeros_like(M, dtype=np.float64)
    ok = denom > 0
    P[:, ok] = M[:, ok] / denom[ok]
    return P


def project_xbq2_to_xkq2(
    P_xk_xb_q2: np.ndarray,
    A_xb_q2: np.ndarray,
) -> np.ndarray:
    """
    For each Q2 bin: A_xk(Q2) = P(Q2) @ A_xb(Q2)
    P has shape (xK, xB, Q2), A has shape (xB, Q2).
    Returns shape (xK, Q2).
    """
    xk_bins, xb_bins, q2_bins = P_xk_xb_q2.shape
    out = np.zeros((xk_bins, q2_bins), dtype=np.float64)
    for iQ in range(q2_bins):
        out[:, iQ] = P_xk_xb_q2[:, :, iQ] @ A_xb_q2[:, iQ]
    return out


def projected_efficiency_from_migration(
    M: np.ndarray,
    P_xk_xb_q2: np.ndarray,
    n_gen_xb_q2: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Build effective projected quantities:
      - Ngen_xK_Q2 = P @ Ngen_xB_Q2
      - Nreco_xK_Q2 = sum_xB M  (counts already in xK,Q2)
      - eps_xK_Q2 = Nreco_xK_Q2 / Ngen_xK_Q2
    """
    n_gen_xK_Q2 = project_xbq2_to_xkq2(P_xk_xb_q2, n_gen_xb_q2)
    n_reco_xK_Q2 = np.sum(M, axis=1)  # (xK,Q2)
    eps_xK_Q2 = efficiency_from_counts(n_reco_xK_Q2, n_gen_xK_Q2, clip=True)
    return eps_xK_Q2, n_gen_xK_Q2, n_reco_xK_Q2


def _compute_toy_F2_map_xK_Q2(
    *,
    model: str,
    toy: ToyParams,
    kparams: KaonModelParams,
    xK_cent: np.ndarray,
    Q2_cent: np.ndarray,
) -> np.ndarray:
    """
    Compute F2^K(xK, Q2) on the bin-center grid for a given toy model.

    Returns
    -------
    F2 : np.ndarray
        Array of shape (len(xK_cent), len(Q2_cent)).
    """
    setup_lhapdf_env()
    pion_set = get_pion_pdfset()
    pion_member = get_pion_pdfmember()

    pdf = make_kaon_pdf_func(
        model=model,
        toy=toy,
        kparams=kparams,
        pion_set=pion_set,
        pion_member=pion_member,
        require_lhapdf=True,
    )

    F2 = np.empty((len(xK_cent), len(Q2_cent)), dtype=np.float64)

    for ix, x in enumerate(xK_cent):
        for iQ, Q2 in enumerate(Q2_cent):
            F2[ix, iQ] = float(F2_from_pdf_func(pdf, float(x), float(Q2)))

    return F2


def compute_local_fischer(
    *,
    a0: float,
    b0: float,
    relerr_xK_Q2: np.ndarray,
    xK_range: tuple[float, float] = (0, 1),
    xK_bins: int = 10,
    Q2_range: tuple[float, float] = (1, 500),
    Q2_bins: int = 10,
    model: str = "toy_baseline",
    kparams: KaonModelParams = KaonModelParams(),
    da: float = 1e-2,
    db: float = 1e-2,
    log_Q2_centers: bool = True,
    eps: float = 1e-15,
) -> dict:
    """
    Compute the local Fisher matrix for the toy-model parameters (a, b),
    using F2^K(xK, Q2) as observable and relerr_xK_Q2 as projected relative
    uncertainty map.

    Parameters
    ----------
    a0, b0
        Fiducial toy-model parameters where the Fisher matrix is evaluated.

    relerr_xK_Q2
        Relative uncertainty map in percent, shape (xK_bins, Q2_bins).

    xK_edges, Q2_edges
        Bin edges used to define the observable grid.

    model
        Kaon model name passed to make_kaon_pdf_func. For your first study,
        this should typically stay "toy_baseline".

    da, db
        Finite-difference steps for numerical derivatives.

    log_Q2_centers
        If True, use geometric bin centers for Q2, which is the natural choice
        when Q2 bins are logarithmic.

    eps
        Numerical floor to avoid divisions by zero.

    Returns
    -------
    dict with keys:
        "F"         : Fisher matrix, shape (2,2)
        "Cov"       : inverse Fisher matrix if invertible, else None
        "sigma_map" : absolute sigma_ij used in the calculation
        "F2_0"      : central F2 map
        "dF_da"     : numerical derivative wrt a
        "dF_db"     : numerical derivative wrt b
        "xK_cent"   : xK bin centers
        "Q2_cent"   : Q2 bin centers
        "mask"      : boolean mask of bins effectively used
    """

    xK_edges = np.linspace(xK_range[0], xK_range[1], xK_bins + 1)

    if log_Q2_centers:
        Q2_edges = np.logspace(np.log10(Q2_range[0]), np.log10(Q2_range[1]), Q2_bins + 1)
    else:
        Q2_edges = np.linspace(Q2_range[0], Q2_range[1], Q2_bins + 1)

    relerr_xK_Q2 = np.asarray(relerr_xK_Q2, dtype=np.float64)
    xK_edges = np.asarray(xK_edges, dtype=np.float64)
    Q2_edges = np.asarray(Q2_edges, dtype=np.float64)

    xK_cent = 0.5 * (xK_edges[:-1] + xK_edges[1:])

    if log_Q2_centers:
        Q2_cent = np.sqrt(Q2_edges[:-1] * Q2_edges[1:])
    else:
        Q2_cent = 0.5 * (Q2_edges[:-1] + Q2_edges[1:])

    if relerr_xK_Q2.shape != (xK_cent.size, Q2_cent.size):
        raise ValueError(
            f"relerr_xK_Q2 has shape {relerr_xK_Q2.shape}, expected {(xK_cent.size, Q2_cent.size)}"
        )

    # --- Central model
    toy_0 = ToyParams(a=a0, b=b0)
    F2_0 = _compute_toy_F2_map_xK_Q2(
        model=model,
        toy=toy_0,
        kparams=kparams,
        xK_cent=xK_cent,
        Q2_cent=Q2_cent,
    )

    # --- Shifted models for finite differences
    toy_ap = ToyParams(a=a0 + da, b=b0)
    toy_am = ToyParams(a=a0 - da, b=b0)
    toy_bp = ToyParams(a=a0, b=b0 + db)
    toy_bm = ToyParams(a=a0, b=b0 - db)

    F2_ap = _compute_toy_F2_map_xK_Q2(
        model=model,
        toy=toy_ap,
        kparams=kparams,
        xK_cent=xK_cent,
        Q2_cent=Q2_cent,
    )
    F2_am = _compute_toy_F2_map_xK_Q2(
        model=model,
        toy=toy_am,
        kparams=kparams,
        xK_cent=xK_cent,
        Q2_cent=Q2_cent,
    )
    F2_bp = _compute_toy_F2_map_xK_Q2(
        model=model,
        toy=toy_bp,
        kparams=kparams,
        xK_cent=xK_cent,
        Q2_cent=Q2_cent,
    )
    F2_bm = _compute_toy_F2_map_xK_Q2(
        model=model,
        toy=toy_bm,
        kparams=kparams,
        xK_cent=xK_cent,
        Q2_cent=Q2_cent,
    )

    # --- Numerical derivatives
    dF_da = (F2_ap - F2_am) / (2.0 * da)
    dF_db = (F2_bp - F2_bm) / (2.0 * db)

    # --- Absolute sigma map from relative errors
    rel = relerr_xK_Q2 / 100.0
    Fref = F2_0
    sigma_map = rel * Fref

    # --- Valid bins mask
    mask = (
        np.isfinite(F2_0)
        & np.isfinite(dF_da)
        & np.isfinite(dF_db)
        & np.isfinite(sigma_map)
        & np.isfinite(rel)
        & (sigma_map > 0.0)
        & (rel > 0.0)
    )

    if not np.any(mask):
        raise RuntimeError("No valid bins available to compute the local Fisher matrix.")

    w = np.zeros_like(F2_0, dtype=np.float64)
    w[mask] = 1.0 / np.maximum(sigma_map[mask] ** 2, eps)

    F_aa = np.sum(w[mask] * dF_da[mask] * dF_da[mask])
    F_ab = np.sum(w[mask] * dF_da[mask] * dF_db[mask])
    F_bb = np.sum(w[mask] * dF_db[mask] * dF_db[mask])

    F = np.array(
        [
            [F_aa, F_ab],
            [F_ab, F_bb],
        ],
        dtype=np.float64,
    )

    try:
        Cov = np.linalg.inv(F)
    except np.linalg.LinAlgError:
        Cov = None

    return {
        "F": F,
        "Cov": Cov,
        "sigma_map": sigma_map,
        "F2_0": F2_0,
        "dF_da": dF_da,
        "dF_db": dF_db,
        "xK_cent": xK_cent,
        "Q2_cent": Q2_cent,
        "mask": mask,
    }

def compute_local_fischer_maps(
    *,
    a0: float,
    b0: float,
    relerr_xK_Q2: np.ndarray,
    xK_range: tuple[float, float] = (0, 1),
    xK_bins: int = 10,
    Q2_range: tuple[float, float] = (1, 500),
    Q2_bins: int = 10,
    model: str = "toy_baseline",
    kparams: KaonModelParams = KaonModelParams(),
    da: float = 1e-2,
    db: float = 1e-2,
    log_Q2_centers: bool = True,
    eps: float = 1e-15,
) -> dict:
    """
    Compute the bin-by-bin Fisher information density maps associated with the
    local Fisher matrix in parameter space (a, b).

    For each bin (xK, Q2), define
        f_aa = (1/sigma^2) * (dF/da)^2
        f_ab = (1/sigma^2) * (dF/da) * (dF/db)
        f_bb = (1/sigma^2) * (dF/db)^2

    so that the total Fisher matrix is obtained by summing over bins:
        F_aa = sum f_aa
        F_ab = sum f_ab
        F_bb = sum f_bb

    Returns
    -------
    dict with keys:
        "F"          : total Fisher matrix, shape (2, 2)
        "Cov"        : inverse Fisher matrix if invertible, else None
        "maps"       : array of shape (2, 2, xK_bins, Q2_bins)
        "info_aa"    : Fisher density map for aa, shape (xK_bins, Q2_bins)
        "info_ab"    : Fisher density map for ab, shape (xK_bins, Q2_bins)
        "info_ba"    : same as info_ab
        "info_bb"    : Fisher density map for bb, shape (xK_bins, Q2_bins)
        "sigma_map"  : absolute uncertainty map
        "F2_0"       : central F2 map
        "dF_da"      : derivative wrt a
        "dF_db"      : derivative wrt b
        "xK_cent"    : xK bin centers
        "Q2_cent"    : Q2 bin centers
        "mask"       : boolean validity mask
    """
    res = compute_local_fischer(
        a0=a0,
        b0=b0,
        relerr_xK_Q2=relerr_xK_Q2,
        xK_range=xK_range,
        xK_bins=xK_bins,
        Q2_range=Q2_range,
        Q2_bins=Q2_bins,
        model=model,
        kparams=kparams,
        da=da,
        db=db,
        log_Q2_centers=log_Q2_centers,
        eps=eps,
    )

    sigma_map = res["sigma_map"]
    dF_da = res["dF_da"]
    dF_db = res["dF_db"]
    mask = res["mask"]

    w = np.zeros_like(sigma_map, dtype=np.float64)
    w[mask] = 1.0 / np.maximum(sigma_map[mask] ** 2, eps)

    info_aa = np.full_like(sigma_map, np.nan)
    info_ab = np.full_like(sigma_map, np.nan)
    info_bb = np.full_like(sigma_map, np.nan)

    info_aa[mask] = w[mask] * dF_da[mask] * dF_da[mask]
    info_ab[mask] = w[mask] * dF_da[mask] * dF_db[mask]
    info_bb[mask] = w[mask] * dF_db[mask] * dF_db[mask]

    maps = np.zeros((2, 2) + sigma_map.shape, dtype=np.float64)
    maps[0, 0] = info_aa
    maps[0, 1] = info_ab
    maps[1, 0] = info_ab
    maps[1, 1] = info_bb

    return {
        "F": res["F"],
        "Cov": res["Cov"],
        "maps": maps,
        "info_aa": info_aa,
        "info_ab": info_ab,
        "info_ba": info_ab,
        "info_bb": info_bb,
        "sigma_map": sigma_map,
        "F2_0": res["F2_0"],
        "dF_da": dF_da,
        "dF_db": dF_db,
        "xK_cent": res["xK_cent"],
        "Q2_cent": res["Q2_cent"],
        "mask": mask,
    }