"""
Reference Calculation Script for Series 1 Paper 2: Temporal Dissipation
======================================================================
Calculates all physical constants, evaluations, saddle point crossover distances,
and wide binary scales for Paper 2 using the official ChronodynamicModel physics engine.
Outputs results to reference_calculations.json.
"""

import os
import sys
import json
import numpy as np

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if not os.path.exists(os.path.join(REPO_ROOT, "src")):
    REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
for p in [REPO_ROOT, os.path.join(REPO_ROOT, "official")]:
    if os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

from src.models import LatestChronodynamicModel
from src.utils.constants import (
    C_M_S,
    G,
    MPC_TO_M,
    MYR_TO_S,
    GYR_TO_S,
    N_GEOMETRIC,
    H0_DEFAULT,
    MSUN_TO_KG,
)

def verify_paper_2():
    model = LatestChronodynamicModel()
    
    h0 = model.h0
    h0_si = model.h0_si
    t0_s = model.t0_seconds
    t0_gyr = t0_s / GYR_TO_S
    n = model.n
    a0 = model.a0
    
    # Sun-Earth L1 Saddle Point (alpha_saddle = 2.5e-13 s^-2)
    alpha_saddle = 2.5e-13
    delta_x_c = a0 / alpha_saddle # meters
    
    # Wide binary reference scale (M_tot = 1.5 M_sun)
    AU = 1.495978707e11
    M_tot = 1.5 * MSUN_TO_KG
    s_c = np.sqrt(G * M_tot / a0) # meters
    s_c_au = s_c / AU
    v_flat_kms = (G * M_tot * a0)**0.25 / 1000.0

    calcs = {
        "paper": "series_1_paper_2_temporal_dissipation",
        "h0_kms_mpc": h0,
        "h0_si_s_inv": h0_si,
        "t0_seconds": t0_s,
        "t0_gyr": t0_gyr,
        "geometric_n": n,
        "a0_formula": "c * H_0 * n = (3 * c * H_0) / (4 * pi)",
        "a0_ms2": a0,
        "saddle_point": {
            "alpha_saddle_s_minus_2": alpha_saddle,
            "crossover_formula": "a0 / alpha_saddle",
            "delta_x_c_meters": delta_x_c,
            "legacy_mond_delta_x_c_meters": 1.20e-10 / alpha_saddle
        },
        "wide_binaries": {
            "m_tot_solar": 1.5,
            "s_c_meters": s_c,
            "s_c_au": s_c_au,
            "v_flat_kms": v_flat_kms
        }
    }

    out_path = os.path.join(os.path.dirname(__file__), "reference_calculations.json")
    with open(out_path, "w") as f:
        json.dump(calcs, f, indent=2)

    print(f"Paper 2 reference calculations verified and saved to: {out_path}")
    return calcs

if __name__ == "__main__":
    verify_paper_2()
