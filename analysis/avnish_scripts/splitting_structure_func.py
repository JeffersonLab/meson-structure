#! /usr/bin/env python

import lhapdf
import numpy as np
from scipy.integrate import quad


################################ Pion Structure function definitions start #########################################

class pion_structure_function:

    def __init__(self):
        self.JAM21PionPDFnlo = lhapdf.getPDFSet("JAM21PionPDFnlo").mkPDF(0)
        self.JAM21PionPDFnlo_pT = lhapdf.getPDFSet("JAM21PionPDFnlo_pT").mkPDF(0)
        self.JAM21PionPDFnlonll_cosine = lhapdf.getPDFSet("JAM21PionPDFnlonll_cosine").mkPDF(0)
        self.JAM21PionPDFnlonll_double_Mellin = lhapdf.getPDFSet("JAM21PionPDFnlonll_double_Mellin").mkPDF(0)
        self.JAM21PionPDFnlonll_expansion = lhapdf.getPDFSet("JAM21PionPDFnlonll_expansion").mkPDF(0)

    def F2pi_nlo(self, x, Q2):
        e_u2 = (2/3)**2
        e_d2 = (1/3)**2
        u = self.JAM21PionPDFnlo.xfxQ2(2, x, Q2)
        ubar = self.JAM21PionPDFnlo.xfxQ2(-2, x, Q2)
        d = self.JAM21PionPDFnlo.xfxQ2(1, x, Q2)
        dbar = self.JAM21PionPDFnlo.xfxQ2(-1, x, Q2)
        F2_pion = x * (e_u2 * (u + ubar) + e_d2 * (d + dbar))
        # print("F2^π(x=%.2f, Q²=%.2f GeV²) = %.5f" % (i, Q2, F2_pion))
        return F2_pion

    def F2pi_nlo_pT(self, x, Q2):
        e_u2 = (2/3)**2
        e_d2 = (1/3)**2
        u = self.JAM21PionPDFnlo.xfxQ2(2, x, Q2)
        ubar = self.JAM21PionPDFnlo.xfxQ2(-2, x, Q2)
        d = self.JAM21PionPDFnlo.xfxQ2(1, x, Q2)
        dbar = self.JAM21PionPDFnlo.xfxQ2(-1, x, Q2)
        F2_pion = x * (e_u2 * (u + ubar) + e_d2 * (d + dbar))
        # print("F2^π(x=%.2f, Q²=%.2f GeV²) = %.5f" % (x, Q2, F2_pion))
        return F2_pion

    def F2pi_nlonll_cosine(self, x, Q2):
        e_u2 = (2/3)**2
        e_d2 = (1/3)**2
        u = self.JAM21PionPDFnlo.xfxQ2(2, x, Q2)
        ubar = self.JAM21PionPDFnlo.xfxQ2(-2, x, Q2)
        d = self.JAM21PionPDFnlo.xfxQ2(1, x, Q2)
        dbar = self.JAM21PionPDFnlo.xfxQ2(-1, x, Q2)
        F2_pion = x * (e_u2 * (u + ubar) + e_d2 * (d + dbar))
        # print("F2^π(x=%.2f, Q²=%.2f GeV²) = %.5f" % (x, Q2, F2_pion))
        return F2_pion

    def F2pi_nlonll_double_Mellin(self, x, Q2):
        e_u2 = (2/3)**2
        e_d2 = (1/3)**2
        u = self.JAM21PionPDFnlo.xfxQ2(2, x, Q2)
        ubar = self.JAM21PionPDFnlo.xfxQ2(-2, x, Q2)
        d = self.JAM21PionPDFnlo.xfxQ2(1, x, Q2)
        dbar = self.JAM21PionPDFnlo.xfxQ2(-1, x, Q2)
        F2_pion = x * (e_u2 * (u + ubar) + e_d2 * (d + dbar))
        # print("F2^π(x=%.2f, Q²=%.2f GeV²) = %.5f" % (x, Q2, F2_pion))
        return F2_pion

    def F2pi_nlonll_expansion(self, x, Q2): 
        e_u2 = (2/3)**2
        e_d2 = (1/3)**2
        u = self.JAM21PionPDFnlo.xfxQ2(2, x, Q2)
        ubar = self.JAM21PionPDFnlo.xfxQ2(-2, x, Q2)
        d = self.JAM21PionPDFnlo.xfxQ2(1, x, Q2)
        dbar = self.JAM21PionPDFnlo.xfxQ2(-1, x, Q2)
        F2_pion = x * (e_u2 * (u + ubar) + e_d2 * (d + dbar))
        # print("F2^π(x=%.2f, Q²=%.2f GeV²) = %.5f" % (x, Q2, F2_pion))
        return F2_pion

################################ Pion Structure function definitions end #########################################

################################ Pion Splitting function definitions start #########################################

class PP2N_SPLITTING:
    
    def __init__(self, model):
        self.mN = 0.938272
        self.mPi = 0.139570
        self.mN2 = self.mN**2
        self.mPi2 = self.mPi**2
        self.model = model

    def get_regulator(self, kT2, xL, par):
        spiN = (kT2 + self.mPi2) / (1 - xL) + (kT2 + self.mN2) / xL
        t = -(kT2 + (1 - xL)**2 * self.mN2) / xL

        # https://arxiv.org/pdf/1512.04459
        # https://arxiv.org/pdf/1804.01965

        if self.model == 's_exp': # s-dep exponential
            reg = np.exp((self.mN2 - spiN) / par**2) 
        elif self.model == 't_exp': # t-dep exponential
            reg = np.exp((t - self.mPi2) / par**2) 
        elif self.model == 't_mon': # t-dep monopole
            reg = ((par**2 - self.mPi2) / (par**2 - t))
        # elif self.model == 'cov dip': # 
        #     reg = ((par**2 - self.mPi2) / (par**2 - t))**4  
        elif self.model == 'Regge': # Regge
            reg = (1 - xL)**(-1 * t) * np.exp((t - self.mPi2) / par**2)
        elif self.model == 'Pauli-Villars': # Pauli-Villars
            reg = np.sqrt(1 - ((t - self.mPi2)**2 / (t - par**2)**2))
        return reg

    def get_fN(self, kT2, xL):
        prefact = 13.7 / (4 * np.pi)
        DpiN = -(kT2 + (1 - xL)**2 * self.mN2 + xL * self.mPi2) / xL
        fppin = prefact * (1 - xL) * (kT2 + self.mN2 * (1 - xL)**2) / (xL**2 * DpiN**2)
        return 2 * fppin  # Factor 2 for charged pion
    
    def integrated_split_func(self, xL, par):
        def integrand(kT2):
            fN = self.get_fN(kT2, xL)
            reg = self.get_regulator(kT2, xL, par)
            return fN * reg * reg  # squared regulator
    
        result, error = quad(integrand, 0, np.inf, limit=100)
        return result


################################ Pion Splitting function definitions end #########################################



################################ Leading Neutron Structure function definitions end #########################################
class LN_structure_function:
    def __init__(self, split_model_name, par):
        self.par = par
        self.split_model = PP2N_SPLITTING(model=split_model_name)

    def _split_func(self, xL):
        return self.split_model.integrated_split_func(xL, self.par)

    def F2LN_nlo(self, x, Q2, xL):
        return 2 * self._split_func(xL) * pion_structure_function.F2pi_nlo(x, Q2)

    def F2LN_nlo_pT(self, x, Q2, xL):
        return 2 * self._split_func(xL) * pion_structure_function.F2pi_nlo_pT(x, Q2)

    def F2LN_nlonll_cosine(self, x, Q2, xL):
        return 2 * self._split_func(xL) * pion_structure_function.F2pi_nlonll_cosine(x, Q2)

    def F2LN_nlonll_double_Mellin(self, x, Q2, xL):
        return 2 * self._split_func(xL) * pion_structure_function.F2pi_nlonll_double_Mellin(x, Q2)

    def F2LN_nlonll_expansion(self, x, Q2, xL):
        return 2 * self._split_func(xL) * pion_structure_function.F2pi_nlonll_expansion(x, Q2)
    
    # usage:
    # # Choose model and parameter for splitting function
    # ln_model = LN_structure_function(split_model_name="Pauli-Villars", par=0.27)

    # # Call desired version
    # x, Q2, xL = 0.3, 4.0, 0.8
    # F2LN_val = ln_model.F2LN_nlo(x, Q2, xL)
    # print(f"F2^LN(x={x}, Q²={Q2}, xL={xL}) = {F2LN_val:.5e}")


################################ Leading Neutron function definitions end #########################################