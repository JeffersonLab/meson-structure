#!/usr/bin/env python3

import numpy as np


'''
I have provided some parameters for the regulators (written as $\Lambda$ in the note and JAM 2018 PRL). In my code, they are written as “par” in get_regulator. I list below the mean values of my fits to the smallest kT and largest xL bins.

 

IMF exp: 1.532

Cov exp: 0.774

Cov mon: 0.532

Regge: 0.977

Pauli-Villars: 0.551
'''

class PP2LAMBDA_SPLITTING:
    
    def __init__(self, model):
        # Physical constants (manually set)
        self.ML = 1.115683  # Lambda mass [GeV]
        self.mN = 0.938272   # Proton mass [GeV]
        self.mK = 0.493677   # Kaon mass [GeV]

        # Derived quantities
        self.mK2 = self.mK**2
        self.mN2 = self.mN**2
        self.Mbar = self.ML + self.mN
        self.DelM = self.ML - self.mN
        self.model = model

    def get_regulator(self, kT2, xL, par):
        sKL = (kT2 + self.mK2)/(1 - xL) + (kT2 + self.ML**2)/xL
        t = -kT2/xL - (1 - xL)/xL * (self.ML**2 - xL * self.mN2)

        if self.model == 'IMF exp':
            reg = np.exp(2 * (self.mN2 - sKL) / par**2)
        elif self.model == 'cov exp':
            reg = np.exp(2 * (t - self.mK2) / par**2)
        elif self.model == 'cov mon':
            reg = ((par**2 - self.mK2) / (par**2 - t))**2
        elif self.model == 'cov dip':
            reg = ((par**2 - self.mK2) / (par**2 - t))**4
        elif self.model == 'Regge':
            reg = (1 - xL)**(-2 * t) * np.exp(2 * (t - self.mK2) / par**2)
        elif self.model == 'Pauli-Villars':
            reg = 1 - ((t - self.mK2)**2 / (t - par**2)**2)
        return reg

    def get_fL(self, kT2, xL):
        psdc = 0.093
        D = 0.85
        F = 0.41
        CKL2 = ((D + 3 * F)/2.0 / 3**0.5)**2

        prefact = CKL2 * self.Mbar**2 / (4 * np.pi * psdc)**2
        DKY = -(kT2 + (1 - xL) * self.ML**2 + xL * self.mK2 - (1 - xL) * xL * self.mN2) / xL
        fKpL = prefact * (1 - xL) * (kT2 + (self.mN * (1 - xL) + self.DelM)**2) / (xL**2 * DKY**2)

        return fKpL

    def get_theory(self, par, xL, kT):
        sig_tot = 19.9  # mb
        return self.get_fL(kT**2, xL) / np.pi * xL * sig_tot * self.get_regulator(kT**2, xL, par) 
    
    def get_Fk(self, xk, q2): # function to calculate the structure function
        



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

        if self.model == 'IMF exp':
            reg = np.exp(2 * (self.mN2 - spiN) / par**2)
        elif self.model == 'cov exp':
            reg = np.exp(2 * (t - self.mPi2) / par**2)
        elif self.model == 'cov mon':
            reg = ((par**2 - self.mPi2) / (par**2 - t))**2
        elif self.model == 'cov dip':
            reg = ((par**2 - self.mPi2) / (par**2 - t))**4
        elif self.model == 'Regge':
            reg = (1 - xL)**(-2 * t) * np.exp(2 * (t - self.mPi2) / par**2)
        elif self.model == 'Pauli-Villars':
            reg = 1 - ((t - self.mPi2)**2 / (t - par**2)**2)
        return reg

    def get_fN(self, kT2, xL):
        prefact = 13.7 / (4 * np.pi)
        DpiN = -(kT2 + (1 - xL)**2 * self.mN2 + xL * self.mPi2) / xL
        fppin = prefact * (1 - xL) * (kT2 + self.mN2 * (1 - xL)**2) / (xL**2 * DpiN**2)
        return 2 * fppin  # Factor 2 for charged pion

    def get_theory(self, par, xL, kT):
        sig_tot = 23.8  # mb
        return self.get_fN(kT**2, xL) / np.pi * xL * sig_tot * self.get_regulator(kT**2, xL, par)
