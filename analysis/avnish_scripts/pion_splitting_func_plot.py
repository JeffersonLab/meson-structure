#!/usr/bin/env python3
from scipy.integrate import simpson
import numpy as np
import matplotlib.pyplot as plt
from splitting_structure_func import PP2N_SPLITTING

# ---------------------------------------------------------------------------
# 1. settings
# ---------------------------------------------------------------------------
xL     = np.arange(0.0001, 1.0, 0.001)      # avoid xL = 0 singularities
xL_bar = 1.0 - xL                           # convenient axis label 1-x_L

# models = { # https://arxiv.org/pdf/1512.04459
#     "t-mon (cov mon)":   ("t_mon",   0.68, "#f0be08"),
#     "t-exp (cov exp)":   ("t_exp",   0.85,  "#ed0707"),
#     "s-exp (IMF exp)":   ("s_exp",   1.33,  "#2ca02c"),
#     "Pauli-Villars":     ("Pauli-Villars", 0.27, "#0f0fc5"),
#     "Regge":             ("Regge",     1.32,  "#9467bd"),
# }

models = { # https://arxiv.org/pdf/1804.01965
    "t-mon (cov mon)":   ("t_mon",   0.52, "#f0be08"),
    "t-exp (cov exp)":   ("t_exp",   0.58,  "#ed0707"),
    "s-exp (IMF exp)":   ("s_exp", 1.31  ,  "#2ca02c"),
    "Pauli-Villars":     ("Pauli-Villars", 0.25, "#0f0fc5"),
    "Regge":             ("Regge",     0.78,  "#9467bd"),
}

# ---------------------------------------------------------------------------
# 2. compute, normalise, store curves
# ---------------------------------------------------------------------------
curves = {}
for label, (model_name, par, colour) in models.items():
    splitter = PP2N_SPLITTING(model=model_name)
    fpi_vals = np.array([splitter.integrated_split_func(xL=xl, par=par) for xl in xL])

    # normalise each curve so ∫ f(xL) dxL = 0.1
    area = simpson(fpi_vals, xL)
    fpi_vals *= 0.1 / area

    curves[label] = (fpi_vals, colour)

# ---------------------------------------------------------------------------
# 3. plot
# ---------------------------------------------------------------------------
plt.figure(figsize=(7,5))
for label, (fpi_vals, colour) in curves.items():
    plt.plot(xL_bar, fpi_vals, label=label, color=colour)

# plt.ylim(0, 0.3)
plt.xlim(0, 1.0)
plt.xlabel(r"$\bar{x_L}$")
plt.ylabel(r"normalised $f_\pi(\bar{x_L})$ (area = 0.1)")
plt.title(r"$\pi$N splitting functions (various regulators)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
