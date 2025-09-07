#!/usr/bin/env python3
# ---------------------------------------------------------------------------
#  Compute pion-exchange splitting functions, pion F2, and LN F2
#  for five regulator models and five JAM21 pion-PDF variants.
# ---------------------------------------------------------------------------

from pathlib import Path
import numpy as np
from scipy.integrate import simpson
import matplotlib.pyplot as plt
import splitting_structure_func as fn 

# ---------------------------------------------------------------------------
# 1. Analysis grid and regulator settings
# ---------------------------------------------------------------------------
xL      = np.arange(0.0001, 1.0, 0.001)      # avoid xL = 0
xL_bar  = 1.0 - xL                           # convenient axis

models = {                                   # regulator  (par, colour)
    "t-mon":          ("t_mon",          0.52, "#f0be08"),
    "t-exp":          ("t_exp",          0.58, "#ed0707"),
    "s-exp":          ("s_exp",          1.31, "#2ca02c"),
    "Pauli-Villars":  ("Pauli-Villars",  0.25, "#0f0fc5"),
    "Regge":          ("Regge",          0.78, "#9467bd"),
}

pion_variants = [                            # PDF tag, plot label
    ("nlo",                 "NLO"),
    ("nlo_pT",              "NLO pT"),
    ("nlonll_cosine",       "cosine"),
    ("nlonll_double_Mellin","double-M"),
    ("nlonll_expansion",    "expansion"),
]

fixed_Q2  = 4.0     # GeV²  (virtuality)
fixed_xbj = 0.30    # proton Bjorken-x
outdir    = Path("outputs_ln"); outdir.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# 2. Containers
# ---------------------------------------------------------------------------
splitting          = {}                 # model -> array
pion_structure     = {}                 # pdf_tag -> array
ln_structure       = {}                 # model -> { pdf_tag -> array }

# ---------------------------------------------------------------------------
# 3. Build pion-PDF interface once
# ---------------------------------------------------------------------------
piF2 = fn.pion_structure_function()     # loads all JAM21 sets

# ---------- compute pion structure functions ----------
for tag, _label in pion_variants:
    vals = []
    for xl in xL:
        xpi = fixed_xbj / (1.0 - xl)        # xπ = x / (1-xL)
        if 0.0 < xpi < 1.0:
            val = getattr(piF2, f"F2pi_{tag}")(xpi, fixed_Q2)
        else:
            val = np.nan                    # out of range
        vals.append(val)
    vals = np.array(vals)
    pion_structure[tag] = vals
    np.save(outdir/f"F2pi_{tag}.npy", vals)

# ---------------------------------------------------------------------------
# 4. Loop over regulator models
# ---------------------------------------------------------------------------
for mod_label, (model_name, par, colour) in models.items():

    # ------- splitting function fπ/p -------
    split = fn.PP2N_SPLITTING(model=model_name)
    fpi_vals = np.array([split.integrated_split_func(xl, par) for xl in xL])

    # normalise each curve to area = 0.1
    area = simpson(fpi_vals, xL)
    fpi_vals *= 0.1 / area
    splitting[mod_label] = fpi_vals
    np.save(outdir/f"fpi_{mod_label}.npy", fpi_vals)

    # ------- leading-neutron structure functions -------
    ln_structure[mod_label] = {}
    for tag, _ in pion_variants:
        ln_vals = 2.0 * fpi_vals * pion_structure[tag]
        ln_structure[mod_label][tag] = ln_vals
        np.save(outdir/f"F2LN_{mod_label}_{tag}.npy", ln_vals)

# ---------------------------------------------------------------------------
# 5. Quick-look plots
# ---------------------------------------------------------------------------
plt.figure(figsize=(6,4))
for mod_label, (_m,_p,c) in models.items():
    plt.plot(xL_bar, splitting[mod_label], color=c, label=mod_label)
plt.xlabel(r"$1-x_L$")
plt.ylabel(r"$f_{\pi/p}(x_L)$  (norm. area = 0.1)")
plt.title("Integrated splitting functions")
plt.grid(alpha=0.3); plt.legend(); plt.tight_layout()
plt.savefig(outdir/"splitting_all.pdf")

plt.figure(figsize=(6,4))
for tag, plab in pion_variants:
    mask = np.isfinite(pion_structure[tag])
    plt.plot(fixed_xbj/(1.0-xL[mask]), pion_structure[tag][mask], label=plab)
plt.xlabel(r"$x_\pi = x/(1-x_L)$")
plt.ylabel(r"$F_2^{\pi}(x_\pi,Q^2)$")
plt.title("Pion structure functions")
plt.grid(alpha=0.3); plt.legend(); plt.tight_layout()
plt.savefig(outdir/"F2pi_all.pdf")

plt.figure(figsize=(6,4))
for mod_label, (_m,_p,c) in models.items():
    plt.plot(xL_bar, ln_structure[mod_label]["nlo"], color=c, label=mod_label)
plt.xlabel(r"$1-x_L$")
plt.ylabel(r"$F_2^{LN}(x=0.3,Q^2=4\,\mathrm{GeV}^2,x_L)$")
plt.title("Leading-neutron F2 (NLO pion PDF)")
plt.grid(alpha=0.3); plt.legend(); plt.tight_layout()
plt.savefig(outdir/"F2LN_all_nlo.pdf")

print(f"Done – data written to {outdir}/ and plots saved.")
