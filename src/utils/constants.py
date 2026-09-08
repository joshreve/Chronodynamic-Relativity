"""
Physical and Cosmological Fundamental Constants & Exact Unit Conversions
========================================================================
All constants defined from first principles (CODATA 2022 / IAU / SI definitions).
Zero arbitrary multipliers or phenomenological tuning offsets.
"""

import numpy as np

# ---------------------------------------------------------------------------
# 1. Fundamental Physical Invariants (SI Units)
# ---------------------------------------------------------------------------

# Speed of light in vacuum (exact definition) [m / s]
C_M_S = 299792458.0

# Speed of light in km/s (exact) [km / s]
C_KM_S = 299792.458

# Newtonian Gravitational Constant (CODATA 2022) [m^3 / (kg * s^2)]
G = 6.67430e-11

# Reduced Planck Constant (exact definition) [J * s]
H_BAR = 1.054571817e-34

# ---------------------------------------------------------------------------
# 2. Exact Astronomical & Time Unit Conversions
# ---------------------------------------------------------------------------

# 1 parsec in meters (IAU 2015 resolution B2 exact definition: 1 pc = (180*3600/pi) AU)
PC_TO_M = 3.0856775814913673e16

# 1 kiloparsec in meters [m]
KPC_TO_M = PC_TO_M * 1.0e3  # 3.0856775814913673e19

# 1 Megaparsec in meters [m]
MPC_TO_M = PC_TO_M * 1.0e6  # 3.0856775814913673e22

# 1 Megaparsec in kilometers [km]
MPC_TO_KM = MPC_TO_M * 1.0e-3  # 3.0856775814913673e19

# 1 Julian Year in seconds (IAU definition: 365.25 days of 86,400 SI seconds) [s]
YEAR_TO_S = 365.25 * 86400.0  # 31,557,600.0 s

# 1 Megayear (10^6 years) in seconds [s]
MYR_TO_S = 1.0e6 * YEAR_TO_S  # 3.15576e13 s

# 1 Gigayear (10^9 years) in seconds [s]
GYR_TO_S = 1.0e9 * YEAR_TO_S  # 3.15576e16 s

# Solar Mass (IAU nominal solar mass parameter / G) [kg]
MSUN_TO_KG = 1.98847e30

# ---------------------------------------------------------------------------
# 3. Geometric Theoretical Invariants
# ---------------------------------------------------------------------------

# Geometric Spatial Dilution Exponent: n = dim(R^3) / Area(S^2) = 3 / (4 * pi)
N_GEOMETRIC = 3.0 / (4.0 * np.pi)  # 0.238732414637843

# ---------------------------------------------------------------------------
# 4. Standard Cosmological Reference Constants
# ---------------------------------------------------------------------------

# Reference Hubble Constant [km / s / Mpc]
H0_DEFAULT = 70.50

# Planck 2018 Cosmological Reference Densities (for comparison baselines)
OMEGA_M_DEFAULT = 0.315
OMEGA_L_DEFAULT = 0.685
OMEGA_B_DEFAULT = 0.049
OMEGA_R_DEFAULT = 9.2e-5
OMEGA_K_DEFAULT = 0.0

# Matter-Radiation Equality Redshift
Z_EQ = 3500.0
