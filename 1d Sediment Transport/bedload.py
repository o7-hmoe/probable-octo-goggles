import numpy as np
from fun import *


class BedCore:
    def __init__(self):
        self.tau_x = np.nan
        self.tau_xcr = 0.047
        self.g = 9.81
        self.s = 2.68
        self.rho_s = 2680.0  # kg/m3 sediment grain density
        self.Se = np.nan  # energy slope (m/m)
        self.D = np.nan  # characteristic grain size
        self.Fr = np.nan  # Froude number
        self.h = np.nan  # water depth (m)
        self.phi = np.nan  # dimensionless bed load
        self.Q = np.nan  # discharge (m3/s)
        self.Rh = np.nan  # hydraulic radius (m)
        self.u = np.nan  # flow velocity (m/s)

    def add_dimensions(self, b):
        try:
            return self.phi * b * np.sqrt((self.s - 1) * self.g * self.D ** 3) * self.rho_s
        except ValueError:
            logging.warning("Non-numeric data. Returning Qb=NaN.")
            return np.nan

    def compute_tau_x(self):
        try:
            return self.Se * self.Rh / ((self.s - 1) * self.D)
        except ValueError:
            logging.warning("Non-numeric data. Returning tau_x=NaN.")
            return np.nan
