"""
Chronodynamic Relativity (CR) Physics Engine
============================================
Canonical implementation of the covariant scalar-tensor gravity framework.
Strictly derived from first-principles relativistic field equations and 3D Euclidean geometry.
Zero manual phenomenological parameters (k_internal = 0).

Fundamental Theoretical Architecture:
-------------------------------------
1. Dilution Exponent (3D Spherical Horizon Geometry):
   n = dim(R^3) / Area(S^2) = 3 / (4 * pi) ≈ 0.2387324146

2. Cosmic Time and Horizon Radius:
   H_0_SI = (H_0 * 1000 m/s) / (1 Mpc in meters)   [s^-1]
   t_0    = 1 / H_0_SI                             [s]
   R_0    = c * t_0 = c / H_0_SI                   [m]

3. Critical Horizon Boundary Acceleration Scale:
   a_0 = (c^2 / R_0) * n = c * H_0_SI * n = (3 * c * H_0_SI) / (4 * pi)   [m/s^2]

4. Relativistic Metric Clock Lapse:
   eta(z) = (1 + z)^(n / 2)

5. Cosmological Distances:
   D_C(z) = (c / H_0) * ln(1 + z)                               [Mpc]
   d_A(z) = D_C(z) / (1 + z)                                    [Mpc]
   d_L(z) = (1 + z) * D_C(z) * eta(z) = (c / H_0) * (1 + z)^(1 + n/2) * ln(1 + z)   [Mpc]
   mu(z)  = 5 * log10(d_L(z) / 10 pc) = 5 * log10(d_L(z) in Mpc) + 25

6. Non-Linear Algebraic Root Gravity (Galactic Rotation Curves & RAR):
   a_c(z) = a_0 * (1 + z)^(2n)                                  [m/s^2]
   g_eff  = 0.5 * (g_N + sqrt(g_N^2 + 4 * g_N * a_c(z)))        [m/s^2]

7. Dynamic Vacuum Relaxation (Non-Equilibrium Cluster Mergers):
   tau_0  = (sqrt(2) * t_0) / n                                 [s]
   tau(x) = tau_0 * exp(- (n / sqrt(2)) * (g_eff / a_c))        [s]
   dg_actual / dt = (g_target - g_actual) / tau
"""

import numpy as np
from src.models.base import CosmologyModel, GravityModel, PhysicsError
from src.utils.constants import (
    C_M_S,
    C_KM_S,
    G,
    MPC_TO_M,
    MYR_TO_S,
    N_GEOMETRIC,
    H0_DEFAULT,
    OMEGA_B_DEFAULT,
    OMEGA_R_DEFAULT,
)


class ChronodynamicModel(CosmologyModel, GravityModel):
    """
    Canonical Chronodynamic Relativity (CR) Physics Engine.
    
    Unifies cosmic expansion, galactic kinematics, gravitational lensing, and
    temporal vacuum relaxation from a single environmental space-density scalar field.
    All variables and threshold scales are derived directly from first principles.
    """

    def __init__(self, parameters=None, **kwargs):
        self.parameters = {**(parameters or {}), **kwargs}
        
        # 1. Primary Cosmological Boundary Parameter: H_0 [km / s / Mpc]
        self.h0 = float(self.parameters.get('h0', H0_DEFAULT))
        
        # 2. Geometric Dilution Exponent: n = 3 / (4 * pi)
        self.n = float(self.parameters.get('n', N_GEOMETRIC))
        
        # Dynamic State Variables for Non-Equilibrium Simulations
        self.g_actual_prev = None
        self.last_t = None

    # -----------------------------------------------------------------------
    # First-Principles Derived Dimensional Properties
    # -----------------------------------------------------------------------

    @property
    def h0_si(self):
        """Hubble expansion rate converted explicitly to SI units: H_0 [s^-1]."""
        # (H_0 [km/s/Mpc] * 1,000 [m/km]) / (1 Mpc in [m])
        return (self.h0 * 1000.0) / MPC_TO_M

    @property
    def t0_seconds(self):
        """Cosmic coordinate origin time in SI seconds: t_0 = 1 / H_0_SI [s]."""
        return 1.0 / self.h0_si

    @property
    def t0_myr(self):
        """Cosmic coordinate origin time converted explicitly to Megayears: t_0 [Myr]."""
        return self.t0_seconds / MYR_TO_S

    @property
    def r0_meters(self):
        """Cosmic horizon scale in SI meters: R_0 = c * t_0 = c / H_0_SI [m]."""
        return C_M_S * self.t0_seconds

    @property
    def a0(self):
        """
        Fundamental critical acceleration scale derived from the cosmic horizon boundary condition:
        a_0 = (c^2 / R_0) * n = c * H_0_SI * n = (3 * c * H_0_SI) / (4 * pi)   [m / s^2].
        """
        if 'a_0' in self.parameters:
            return float(self.parameters['a_0'])
        elif 'alpha_m' in self.parameters:
            # Backward-compatibility alias
            return float(self.parameters['alpha_m'])
        return C_M_S * self.h0_si * self.n

    @property
    def tau0_seconds(self):
        """
        Unscreened background vacuum relaxation timescale:
        tau_0 = (sqrt(2) / n) * t_0 = sqrt(2) / (H_0_SI * n)   [s].
        """
        return (np.sqrt(2.0) * self.t0_seconds) / self.n

    @property
    def tau0_myr(self):
        """Unscreened background vacuum relaxation timescale in Megayears: tau_0 [Myr]."""
        return self.tau0_seconds / MYR_TO_S

    # -----------------------------------------------------------------------
    # Redshift & Smooth Cosmological Epoch Scaling
    # -----------------------------------------------------------------------

    def get_n_eff(self, z_obs, n=None):
        """
        Effective space density dilution exponent across cosmic epochs.
        Smoothly incorporates radiation density scaling at high redshift.
        """
        if n is None:
            n = self.n
        z_obs = np.atleast_1d(z_obs)
        omega_b = float(self.parameters.get('omega_b', OMEGA_B_DEFAULT))
        omega_r = float(self.parameters.get('omega_r', OMEGA_R_DEFAULT))
        
        # Smooth continuous matter-radiation transition
        term_rad = (2.0 * omega_r / omega_b) * (1.0 + np.maximum(z_obs, 0.0))
        res = n * np.sqrt(1.0 + term_rad)
        return res if len(res) > 1 else res[0]

    def get_z_exp(self, z_obs, n=None):
        """
        Converts observed spectral redshift to physical spatial expansion redshift:
        (1 + z_obs) = (1 + z_exp) * eta(z_exp) = (1 + z_exp)^(1 + n/2)
        => (1 + z_exp) = (1 + z_obs)^(1 / (1 + n/2))
        """
        if n is None:
            n = self.n
        z_obs = np.atleast_1d(z_obs)
        ne = self.get_n_eff(z_obs, n)
        z_exp = (1.0 + z_obs) ** (1.0 / (1.0 + ne / 2.0)) - 1.0
        return z_exp if len(z_exp) > 1 else z_exp[0]

    # -----------------------------------------------------------------------
    # Cosmic Expansion & Distance Engine
    # -----------------------------------------------------------------------

    def hubble_parameter(self, z, **kwargs):
        """
        Physical expansion rate H(z) in km / s / Mpc:
        H(z) = H_0 * (1 + z_exp)
        where (1 + z_exp) = (1 + z_obs)^(1 / (1 + n_eff / 2)).
        """
        params = {**self.parameters, **kwargs}
        h0 = float(params.get('h0', self.h0))
        n = float(params.get('n', self.n))
        z_exp = self.get_z_exp(z, n)
        z_exp_arr = np.atleast_1d(z_exp)
        res = h0 * (1.0 + z_exp_arr)
        return res if len(res) > 1 else res[0]

    def comoving_distance(self, z_obs, z_start=0.0, **kwargs):
        """
        Comoving distance D_C(z) in Mpc:
        D_C(z) = (c / H_0) * ln((1 + z_obs) / (1 + z_start))   [Mpc]
        """
        params = {**self.parameters, **kwargs}
        h0 = float(params.get('h0', self.h0))
        z_start_arr = np.atleast_1d(z_start)
        z_obs_arr = np.atleast_1d(z_obs)
        r_com = (C_KM_S / h0) * np.log((1.0 + z_obs_arr) / (1.0 + z_start_arr))
        return r_com if len(r_com) > 1 else r_com[0]

    def angular_diameter_distance(self, z_obs, z_start=0.0, **kwargs):
        """
        Angular diameter distance d_A(z) in Mpc:
        d_A(z) = D_C(z) / (1 + z_obs)   [Mpc]
        """
        r_com = self.comoving_distance(z_obs, z_start, **kwargs)
        z_obs_arr = np.atleast_1d(z_obs)
        res = r_com / (1.0 + z_obs_arr)
        return res if len(z_obs_arr) > 1 else res[0]

    def luminosity_distance(self, z_obs, **kwargs):
        """
        Physical luminosity distance d_L(z) in Mpc with clock-rate luminosity scaling:
        d_L(z) = (1 + z_obs) * D_C(z) * eta(z) = (c / H_0) * (1 + z_obs)^(1 + n/2) * ln(1 + z_obs)   [Mpc]
        """
        params = {**self.parameters, **kwargs}
        n = float(params.get('n', self.n))
        z_obs_arr = np.atleast_1d(z_obs)
        ne = self.get_n_eff(z_obs_arr, n)
        r_com = self.comoving_distance(z_obs, **kwargs)
        res = ((1.0 + z_obs_arr) ** (1.0 + ne / 2.0)) * r_com
        return res if len(res) > 1 else res[0]

    def luminosity_modulus(self, z_obs, **kwargs):
        """
        Distance Modulus:
        mu(z) = 5 * log10(d_L(z) / 10 pc) = 5 * log10(d_L(z) in Mpc) + 25.0
        """
        dl = np.atleast_1d(self.luminosity_distance(z_obs, **kwargs))
        dl_safe = np.where(dl <= 0, 1e-10, dl)
        mu = 5.0 * np.log10(dl_safe) + 25.0
        return mu if len(mu) > 1 else mu[0]

    def compute_mu(self, z_obs, **kwargs):
        """Standard alias for luminosity modulus."""
        return self.luminosity_modulus(z_obs, **kwargs)

    # -----------------------------------------------------------------------
    # Galactic Kinematics & Gravitational Field Engine
    # -----------------------------------------------------------------------

    def compute_acceleration(self, r, baryonic_mass_profile, z=0.0, dt=0.0, **kwargs):
        """
        Computes total effective acceleration g_eff(r) and local expansion rate.
        
        Formula:
        g_eff = 0.5 * (g_N + sqrt(g_N^2 + 4 * g_N * a_c(z)))   [m / s^2]
        where a_c(z) = a_0 * (1 + z)^(2n)
        """
        r = np.atleast_1d(r)
        r_safe = np.where(r == 0, 1e-10, r)
        params = {**self.parameters, **kwargs}
        n = float(params.get('n', self.n))
        a0 = float(params.get('a_0', self.a0))

        # 1. Baryonic Mass & Base Newtonian Gravitational Acceleration
        if callable(baryonic_mass_profile):
            m_b = baryonic_mass_profile(r)
        else:
            m_b = baryonic_mass_profile

        # g_N = G * M_b / r^2   [m / s^2]
        g_newton = (G * m_b) / (r_safe ** 2)

        # 2. Redshift-Evolved Critical Acceleration Scale: a_c(z) = a_0 * (1 + z)^(2n)
        z_arr = np.atleast_1d(z)
        ne = self.get_n_eff(z_arr, n)
        a_c = a0 * ((1.0 + z_arr) ** (2.0 * ne))

        # 3. Non-Linear Algebraic Root Gravity with External Field Effect (EFE)
        g_ext = float(params.get('g_ext', 0.0))
        if g_ext > 0:
            target = g_newton + g_ext
            X = 0.5 * (target + np.sqrt(target ** 2 + 4.0 * target * a_c))
            g_target = X - g_ext
        else:
            g_target = 0.5 * (g_newton + np.sqrt(g_newton ** 2 + 4.0 * g_newton * a_c))

        # 4. Dynamic Vacuum Relaxation (Non-Equilibrium Cluster Mergers)
        if dt > 0:
            # dt provided in seconds; if dt < 1000, assume input is in Myr and convert explicitly
            dt_s = dt * MYR_TO_S if dt < 1.0e6 else dt
            
            tau_0_s = self.tau0_seconds
            g_val = np.linalg.norm(g_target) if isinstance(g_target, np.ndarray) else g_target
            x = g_val / a0
            k = n / np.sqrt(2.0)
            tau_s = tau_0_s * np.exp(-k * x)

            if self.g_actual_prev is None or tau_s <= dt_s:
                g_actual = g_target
            else:
                g_actual = self.g_actual_prev + (g_target - self.g_actual_prev) * (dt_s / tau_s)
            self.g_actual_prev = g_actual
        else:
            g_actual = g_target

        # 5. Local Environmental Expansion Rate: H_local = H_0 * (1 + z)^(n/2)
        h_local = self.h0 * ((1.0 + z_arr) ** (ne / 2.0))

        return self.validate_result(g_actual), h_local

    def reset_state(self):
        """Reset dynamic relaxation state memory between simulation runs."""
        self.g_actual_prev = None
        self.last_t = None
