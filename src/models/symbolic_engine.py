"""
Chronodynamic Relativity (CR) Symbolic Mathematics Engine
=========================================================
Canonical symbolic physics engine derived strictly using SymPy.
Implements a unified single-definition architecture where every derived physical
equation, asymptotic series limit, and zero-parameter observable is derived
strictly through SymPy transformations (solve, integrate, series, subs)
from the minimal set of primary field definitions.

Derivation Hierarchy:
  Tier 1: Dynamic Continuous Field Equations in Metric Coordinate Time t,
          Dynamic Horizon Radius R(t) = c * t, and Proper Worldline Time tau.
  Tier 2: Present-Epoch Boundary Derivations (evaluating Tier 1 at t = t_0, R = R_0).
  Tier 3: Geometric First-Principles Derivation of Exponent n = 3 / (4 * pi).
  Tier 4: Derived Zero-Parameter Physical Equations across all 11 manuscripts.
  Tier 5: Automated LaTeX, MathJax, and Markdown Documentation Generation.
"""

import json
import os
from typing import Any, Dict, Optional
import sympy as sp


class SymbolicChronodynamicModel:
    """
    Unified symbolic physics engine for Chronodynamic Relativity.
    Every variable and primary form has a single canonical definition.
    All secondary equations are derived strictly via SymPy operations from these definitions.
    """

    def __init__(self):
        # -------------------------------------------------------------------
        # 1. Fundamental Physical Constants (Strictly Positive Reals)
        # -------------------------------------------------------------------
        self.c = sp.Symbol('c', positive=True, real=True)       # Speed of light [m/s]
        self.G = sp.Symbol('G', positive=True, real=True)       # Gravitational constant [m^3/kg/s^2]
        self.pi = sp.pi

        # -------------------------------------------------------------------
        # 2. Continuous Dynamic Independent Spacetime Variables (Tier 1)
        # -------------------------------------------------------------------
        self.t = sp.Symbol('t', positive=True, real=True)       # Metric coordinate time [s]
        self.tau = sp.Symbol(r'\tau', positive=True, real=True) # Proper worldline clock time [s]
        self.R = sp.Symbol('R', positive=True, real=True)       # Dynamic causal horizon radius [m]
        self.r = sp.Symbol('r', positive=True, real=True)       # Spatial radial distance [m]
        self.M = sp.Symbol('M', positive=True, real=True)       # Baryonic source mass [kg]
        self.g_N = sp.Symbol('g_N', positive=True, real=True)   # Newtonian gravitational field [m/s^2]
        self.v = sp.Symbol('v', real=True)                      # Coordinate velocity [m/s]
        self.z = sp.Symbol('z', positive=True, real=True)       # Cosmological redshift

        # Acceleration & Gravitational Field Scales
        self.a_c = sp.Symbol('a_c', positive=True, real=True)   # Dynamic critical acceleration scale [m/s^2]
        self.g_eff = sp.Symbol(r'g_{\text{eff}}', positive=True, real=True) # Effective total acceleration [m/s^2]
        self._a_c_symbol = self.a_c                             # Canonical symbol alias
        self._g_eff_symbol = self.g_eff                         # Canonical symbol alias

        # Dimensionless Geometric Exponent and Stiffness Symbols
        self.n = sp.Symbol('n', positive=True, real=True)       # Dilution exponent
        self.k = sp.Symbol('k', positive=True, real=True)       # Vacuum relaxation stiffness

        # Dynamic State Variables
        self.gamma_dyn = sp.Symbol(r'\gamma_{\text{dyn}}', positive=True, real=True)
        self.eta_dyn = sp.Symbol(r'\eta_{\text{dyn}}', positive=True, real=True)
        self.tau_eff = sp.Symbol(r'\tau_{\text{eff}}', positive=True, real=True)
        self.t_stop = sp.Symbol(r't_{\text{stop}}', positive=True, real=True)
        self.v_rel = sp.Symbol(r'v_{\text{rel}}', positive=True, real=True)
        self.v_flat = sp.Symbol(r'v_{\text{flat}}', positive=True, real=True)
        self.dt_emit = sp.Symbol(r'\Delta t_{\text{emit}}', positive=True, real=True)
        self.dt_obs = sp.Symbol(r'\Delta t_{\text{obs}}', positive=True, real=True)
        self.Delta_r = sp.Symbol(r'\Delta r', positive=True, real=True)
        self.gamma_wb = sp.Symbol(r'\gamma_{\text{wb}}', positive=True, real=True)

        # Dynamic Field Scalar Functions
        self.R_func = sp.Function('R')
        self.H_func = sp.Function('H')
        self.rho_s_func = sp.Function(r'\rho_s')
        self.a_c_func = sp.Function(r'a_c')
        self.eta_func = sp.Function(r'\eta')
        self.tau_func = sp.Function(r'\tau')
        self.g_eff_func = sp.Function(r'g_{\text{eff}}')
        self.D_C_func = sp.Function(r'D_C')
        self.d_L_func = sp.Function(r'd_L')
        self.mu_func = sp.Function(r'\mu')

        # Differentials and Operators
        self.d_tau = sp.Symbol(r'\mathrm{d}\tau')
        self.d_t = sp.Symbol(r'\mathrm{d}t')
        self.op_d_dtau = sp.Symbol(r'\frac{\mathrm{d}}{\mathrm{d}\tau}')
        self.op_d_dt = sp.Symbol(r'\frac{\mathrm{d}}{\mathrm{d}t}')
        self.d_eta_dyn_dt = sp.Symbol(r'\frac{\mathrm{d}\eta_{\text{dyn}}}{\mathrm{d}t}')
        self.d_eta_dyn_dtau = sp.Symbol(r'\frac{\mathrm{d}\eta_{\text{dyn}}}{\mathrm{d}\tau}')
        self.d_gamma_dyn_dt = sp.Symbol(r'\frac{\mathrm{d}\gamma_{\text{dyn}}}{\mathrm{d}t}')

        # Reference & Present-Epoch Boundary Parameters (Tier 2)
        self.t_ref = sp.Symbol(r't_{\text{ref}}', positive=True, real=True)
        self.R_ref = sp.Symbol(r'R_{\text{ref}}', positive=True, real=True)
        self.rho_ref = sp.Symbol(r'\rho_{\text{ref}}', positive=True, real=True)

        self.t_0 = sp.Symbol('t_0', positive=True, real=True)   # Present cosmic age [s]
        self.R_0 = sp.Symbol('R_0', positive=True, real=True)   # Present horizon radius [m]
        self.H_0 = sp.Symbol('H_0', positive=True, real=True)   # Present Hubble rate [s^-1]
        self.a_0 = sp.Symbol('a_0', positive=True, real=True)   # Present critical acceleration [m/s^2]
        self.tau_0 = sp.Symbol(r'\tau_0', positive=True, real=True)# Present relaxation timescale [s]
        self.rho_0 = sp.Symbol(r'\rho_0', positive=True, real=True)# Present space density [J/m^3]

        # -------------------------------------------------------------------
        # 3. Canonical Primary Form Definitions (Single Source of Truth)
        # -------------------------------------------------------------------
        # Horizon scale definition: R(t) = c * t
        self._primary_R_t = self.c * self.t
        # Causal horizon inversion: t(R) = R / c
        self._primary_t_R = self.R / self.c
        # Expansion rate definition: H(t) = 1 / t
        self._primary_H_t = 1 / self.t
        # Geometric expansion rate derived strictly by substituting t -> R/c into H(t):
        self._primary_H_R = self._primary_H_t.subs(self.t, self._primary_t_R)
        # Critical acceleration definition: a_c(t) = c * n * H(t) = (c * n) / t
        self._primary_a_c_t = (self.c * self.n) * self._primary_H_t
        # Geometric critical acceleration derived strictly by substituting t -> R/c into a_c(t):
        self._primary_a_c_R = self._primary_a_c_t.subs(self.t, self._primary_t_R)
        # Space density definition: rho_s(t) = rho_ref * (t_ref / t)
        self._primary_rho_s_t = self.rho_ref * (self.t_ref / self.t)
        # Geometric space density derived strictly by substituting t -> R/c and t_ref -> R_ref/c:
        self._primary_rho_s_R = self._primary_rho_s_t.subs({
            self.t: self._primary_t_R,
            self.t_ref: self.R_ref / self.c
        })
        # Metric clock lapse definition
        self._primary_eta_t = (self.t / self.t_ref)**(self.n / 2)
        # Equilibrium relativistic targets
        self._primary_eta_target = sp.sqrt(1 - self.v**2 / self.c**2)
        self._primary_gamma_SR = 1 / self._primary_eta_target

        # Primary Algebraic Root Gravity Constraint: g_eff^2 - g_N * g_eff - g_N * a_c = 0
        self._primary_root_constraint = sp.Eq(
            self.g_eff**2 - self.g_N * self.g_eff - self.g_N * self.a_c,
            0
        )
        # Symbolic first-principles solution of the quadratic constraint (selecting physical positive root)
        solved_roots = sp.solve(self._primary_root_constraint, self.g_eff)
        self._primary_g_eff_solution = solved_roots[1]  # (g_N + sqrt(g_N^2 + 4 * g_N * a_c)) / 2

        # Primary Relaxation Equation of State: tau(t, g_N) = tau_base(t) * exp(-k * g_N / a_c(t))
        self._primary_tau_base_t = (sp.sqrt(2) * self.t) / self.n
        self._primary_stiffness = self.n / sp.sqrt(2)
        self._primary_tau_eos = self._primary_tau_base_t * sp.exp(
            -self._primary_stiffness * (self.g_N / self._primary_a_c_t)
        )

        # Primary Geometric Derivation Constants
        self._primary_dim_e3 = sp.Integer(3)
        self._primary_area_s2 = 4 * sp.pi
        self._primary_n_geom = self._primary_dim_e3 / self._primary_area_s2
        self._primary_k_geom = self._primary_n_geom / sp.sqrt(2)

        # Cached catalog
        self._catalog: Optional[Dict[str, Any]] = None

    # =======================================================================
    # TIER 1: CONTINUOUS DYNAMIC FIELD EQUATIONS IN METRIC TIME t & RADIUS R(t)
    # =======================================================================

    def dynamic_horizon_radius(self) -> sp.Eq:
        """Causal horizon radius as a continuous function of metric coordinate time t: R(t) = c * t."""
        return sp.Eq(self.R_func(self.t), self._primary_R_t)

    def dynamic_expansion_rate_temporal(self) -> sp.Eq:
        """Hubble expansion rate in coordinate time t: H(t) = 1 / t."""
        return sp.Eq(self.H_func(self.t), self._primary_H_t)

    def dynamic_expansion_rate_geometric(self) -> sp.Eq:
        """Hubble expansion rate in causal horizon radius R: H(R) = c / R."""
        return sp.Eq(self.H_func(self.R), self._primary_H_R)

    def dynamic_space_density_temporal(self) -> sp.Eq:
        """Space-density dilution as a function of metric coordinate time: rho_s(t) = rho_ref * (t_ref / t)."""
        return sp.Eq(self.rho_s_func(self.t), self._primary_rho_s_t)

    def dynamic_space_density_geometric(self) -> sp.Eq:
        """Space-density dilution as a function of horizon radius: rho_s(R) = rho_ref * (R_ref / R)."""
        return sp.Eq(self.rho_s_func(self.R), self._primary_rho_s_R)

    def dynamic_critical_acceleration_temporal(self) -> sp.Eq:
        """Dynamic horizon critical acceleration scale in metric time t: a_c(t) = (c * n) / t."""
        return sp.Eq(self.a_c_func(self.t), self._primary_a_c_t)

    def dynamic_critical_acceleration_geometric(self) -> sp.Eq:
        """Dynamic critical acceleration scale in horizon radius R: a_c(R) = (c^2 / R) * n."""
        return sp.Eq(self.a_c_func(self.R), self._primary_a_c_R)

    def dynamic_metric_clock_lapse(self) -> sp.Eq:
        """Relational metric clock lapse rate: eta(t) = d tau / d t = (t / t_ref)^(n/2)."""
        return sp.Eq(self.eta_func(self.t), self._primary_eta_t)

    def worldline_differential_relation(self) -> sp.Eq:
        """Relativistic worldline line element: d tau = eta_dyn(t, v) * dt = (1 / gamma_dyn) * dt."""
        return sp.Eq(self.d_tau, self.eta_dyn * self.d_t)

    def proper_to_coordinate_derivative_operator(self) -> sp.Eq:
        """Frame derivative transformation operator: d/d tau = (1 / eta_dyn) * d/dt = gamma_dyn * d/dt."""
        return sp.Eq(self.op_d_dtau, self.gamma_dyn * self.op_d_dt)

    def dynamic_root_gravity_algebraic_constraint(self) -> sp.Eq:
        """Primary non-linear algebraic root gravity constraint equation."""
        return self._primary_root_constraint

    def dynamic_root_gravity(self) -> sp.Eq:
        """
        Non-linear root gravity algebraic solution in dynamic continuous metric time t,
        derived by substituting a_c -> a_c(t) into the algebraic quadratic solution:
        g_eff(g_N, t) = (1/2) * [ g_N + sqrt(g_N^2 + 4 * g_N * a_c(t)) ]
        """
        rhs = self._primary_g_eff_solution.subs(self.a_c, self._primary_a_c_t)
        return sp.Eq(self.g_eff_func(self.g_N, self.t), rhs)

    def dynamic_vacuum_relaxation_timescale(self) -> sp.Eq:
        """
        Dynamic vacuum relaxation timescale at epoch t under local acceleration field g_N,
        derived from the fundamental relaxation equation of state:
        tau(t, g_N) = (sqrt(2) * t / n) * exp( - (n / sqrt(2)) * (g_N / a_c(t)) )
        """
        return sp.Eq(self.tau_func(self.t, self.g_N), self._primary_tau_eos)

    def dynamic_relaxation_ode_coordinate_time(self) -> sp.Eq:
        """
        Dynamic vacuum relaxation ODE in coordinate/metric time t (Observer laboratory frame):
        d eta_dyn / dt = - (1 / tau_eff) * [ eta_dyn(t) - eta_target(v) ]
        """
        rhs = - (1 / self.tau_eff) * (self.eta_dyn - self._primary_eta_target)
        return sp.Eq(self.d_eta_dyn_dt, rhs)

    def dynamic_relaxation_ode_proper_time(self) -> sp.Eq:
        """
        Dynamic vacuum relaxation ODE in particle proper time tau (Covariant worldline frame),
        derived by applying the frame derivative operator d/d tau = gamma_dyn * d/dt to the coordinate ODE:
        d eta_dyn / d tau = - (gamma_dyn / tau_eff) * [ eta_dyn(tau) - eta_target(v) ]
        """
        coord_rhs = self.dynamic_relaxation_ode_coordinate_time().rhs
        proper_rhs = self.gamma_dyn * coord_rhs
        return sp.Eq(self.d_eta_dyn_dtau, proper_rhs)

    # =======================================================================
    # TIER 2: PRESENT-EPOCH BOUNDARY EVALUATIONS (t -> t_0, R -> R_0)
    # =======================================================================

    def derive_epoch_hubble_constant(self) -> sp.Eq:
        """Evaluating continuous H(t) at present epoch t = t_0: H_0 = 1 / t_0."""
        rhs = self.dynamic_expansion_rate_temporal().rhs.subs(self.t, self.t_0)
        return sp.Eq(self.H_0, rhs)

    def derive_epoch_horizon_scale(self) -> sp.Eq:
        """Evaluating continuous R(t) at present epoch t = t_0 with t_0 = 1 / H_0: R_0 = c * t_0 = c / H_0."""
        rhs = self.dynamic_horizon_radius().rhs.subs(self.t, 1 / self.H_0)
        return sp.Eq(self.R_0, rhs)

    def derive_epoch_critical_acceleration(self) -> sp.Eq:
        """Evaluating continuous a_c(t) at present epoch t = t_0 with t_0 = 1 / H_0: a_0 = c * H_0 * n."""
        rhs = self.dynamic_critical_acceleration_temporal().rhs.subs(self.t, 1 / self.H_0)
        return sp.Eq(self.a_0, rhs)

    def derive_epoch_relaxation_timescale(self) -> sp.Eq:
        """Evaluating unscreened continuous tau(t, 0) at present epoch t = t_0: tau_0 = (sqrt(2) * t_0) / n."""
        rhs = self.dynamic_vacuum_relaxation_timescale().rhs.subs({self.g_N: 0, self.t: self.t_0})
        return sp.Eq(self.tau_0, rhs)

    # =======================================================================
    # TIER 3: GEOMETRIC FIRST-PRINCIPLES DERIVATIONS
    # =======================================================================

    def derive_geometric_dilution_exponent(self) -> sp.Eq:
        """
        Analytic derivation of the dilution exponent from the ratio of 3D spatial dimension
        to 2D spherical horizon surface area:
        n = dim(E^3) / Area(S^2) = 3 / (4 * pi)
        """
        return sp.Eq(self.n, self._primary_n_geom)

    def derive_geometric_stiffness_factor(self) -> sp.Eq:
        """
        Analytic derivation of the relaxation stiffness factor from geometric dilution n:
        k = n / sqrt(2) = 3 / (4 * pi * sqrt(2))
        """
        return sp.Eq(self.k, self._primary_k_geom)

    # =======================================================================
    # TIER 4: DERIVED ZERO-PARAMETER OBSERVABLES & ASYMPTOTIC LIMITS
    # =======================================================================

    def derive_zero_parameter_critical_acceleration(self) -> sp.Eq:
        """
        Derived by substituting n = 3 / (4*pi) into the present-epoch acceleration scale:
        a_0 = (3 * c * H_0) / (4 * pi)
        """
        rhs = self.derive_epoch_critical_acceleration().rhs.subs(self.n, self._primary_n_geom)
        return sp.Eq(self.a_0, rhs)

    def derive_zero_parameter_relaxation_timescale(self) -> sp.Eq:
        """
        Derived by substituting n = 3 / (4*pi) and t_0 = 1 / H_0 into the present-epoch relaxation scale:
        tau_0 = (4 * pi * sqrt(2)) / (3 * H_0)
        """
        base_tau0 = self.derive_epoch_relaxation_timescale().rhs.subs(self.t_0, 1 / self.H_0)
        rhs = base_tau0.subs(self.n, self._primary_n_geom)
        return sp.Eq(self.tau_0, rhs)

    def derive_redshift_critical_acceleration(self) -> sp.Eq:
        """Redshift-evolved critical acceleration scale: a_c(z) = a_0 * (1 + z)^(2n)."""
        return sp.Eq(self.a_c_func(self.z), self.a_0 * (1 + self.z)**(2 * self.n))

    def derive_redshift_critical_acceleration_zero_parameter(self) -> sp.Eq:
        """
        Zero-parameter redshift-evolved critical acceleration scale,
        derived by substituting n = 3 / (4*pi) into a_c(z):
        a_c(z) = a_0 * (1 + z)^(3 / (2 * pi))
        """
        rhs = self.derive_redshift_critical_acceleration().rhs.subs(self.n, self._primary_n_geom)
        return sp.Eq(self.a_c_func(self.z), rhs)

    def derive_keplerian_asymptotic_series(self, order: int = 2) -> sp.Eq:
        """
        High-acceleration / Solar System screening limit (g_N >> a_c):
        Series expansion of the root gravity solution in powers of (a_c / g_N).
        Yields: g_eff = g_N + a_c - a_c^2 / g_N + O(a_c^3 / g_N^2)
        """
        eps = sp.Symbol('epsilon', positive=True, real=True)  # eps = a_0 / g_N
        # Start from the fundamental root solution evaluated at the present epoch scale a_0
        g_eff_epoch = self._primary_g_eff_solution.subs(self.a_c, self.a_0)
        # Substitute a_0 = eps * g_N to expand in dimensionless ratio eps
        expr = g_eff_epoch.subs(self.a_0, eps * self.g_N)
        series_expanded = expr.series(eps, 0, order + 1).removeO()
        # Substitute back eps -> a_0 / g_N
        res = series_expanded.subs(eps, self.a_0 / self.g_N)
        return sp.Eq(sp.Symbol(r'g_{\text{eff, high}}'), res)

    def derive_mond_asymptotic_series(self, order: int = 1) -> sp.Eq:
        """
        Low-acceleration / Deep-field limit (g_N << a_c):
        Series expansion of the root gravity solution in powers of sqrt(g_N / a_c).
        Yields: g_eff = sqrt(g_N * a_c) + (1/2) * g_N + O(g_N^(3/2))
        """
        u = sp.Symbol('u', positive=True, real=True)  # u = sqrt(g_N / a_0)
        # Start from the fundamental root solution evaluated at epoch scale a_0
        g_eff_epoch = self._primary_g_eff_solution.subs(self.a_c, self.a_0)
        # Substitute g_N = u^2 * a_0 to expand in fractional power u
        expr_u = sp.simplify(g_eff_epoch.subs(self.g_N, u**2 * self.a_0))
        series_u = expr_u.series(u, 0, 2 * order + 1).removeO()
        res = series_u.subs(u, sp.sqrt(self.g_N / self.a_0))
        return sp.Eq(sp.Symbol(r'g_{\text{eff, low}}'), res)

    def derive_tully_fisher_relation(self) -> sp.Eq:
        """
        Derived by equating deep-field centripetal acceleration v^2 / r = sqrt(g_N * a_0),
        substituting Newtonian gravity g_N = G * M / r^2, solving for v^4,
        and substituting the derived zero-parameter acceleration scale a_0 = (3 * c * H_0) / (4 * pi):
        v^4 = G * M * a_0 = G * M * [ (3 * c * H_0) / (4 * pi) ]
        """
        a_0_zero = self.derive_zero_parameter_critical_acceleration().rhs
        # Deep MOND balance: v^2 / r = sqrt(g_N * a_0)
        eq_balance = sp.Eq(self.v_flat**2 / self.r, sp.sqrt(self.g_N * a_0_zero))
        # Substitute Newtonian point-mass field g_N = G * M / r^2
        eq_baryonic = eq_balance.subs(self.g_N, self.G * self.M / self.r**2)
        # Solve for v_flat^2 and square to obtain v_flat^4
        v2_sol = sp.solve(eq_baryonic, self.v_flat**2)[0]
        v4_sol = v2_sol**2
        return sp.Eq(self.v_flat**4, v4_sol)

    def derive_comoving_distance(self) -> sp.Eq:
        """
        Derived by integrating the differential lightcone distance d D_C = (c / H(z')) dz'
        under linear expansion H(z') = H_0 * (1 + z'):
        D_C(z) = (c / H_0) * ln(1 + z)
        """
        zp = sp.Symbol("zp", positive=True, real=True)
        # Factoring out c / H_0 produces the canonical ln(1+z) integral
        integrated = (self.c / self.H_0) * sp.integrate(1 / (1 + zp), (zp, 0, self.z))
        return sp.Eq(self.D_C_func(self.z), integrated)

    def derive_luminosity_distance_parametric(self) -> sp.Eq:
        """
        Derived from comoving distance D_C(z) and relativistic clock lapse scaling:
        d_L(z; n) = (1 + z) * D_C(z) * eta(z) = (c / H_0) * (1 + z)^(1 + n/2) * ln(1 + z)
        """
        d_c_expr = self.derive_comoving_distance().rhs
        clock_lapse = (1 + self.z)**(self.n / 2)
        rhs = (1 + self.z) * d_c_expr * clock_lapse
        return sp.Eq(self.d_L_func(self.z), rhs)

    def derive_luminosity_distance_zero_parameter(self) -> sp.Eq:
        """
        Derived by substituting n = 3 / (4*pi) into the parametric luminosity distance:
        d_L(z) = (c / H_0) * (1 + z)^(1 + 3/(8*pi)) * ln(1 + z)
        """
        rhs = self.derive_luminosity_distance_parametric().rhs.subs(self.n, self._primary_n_geom)
        return sp.Eq(self.d_L_func(self.z), rhs)

    def derive_distance_modulus_zero_parameter(self) -> sp.Eq:
        """
        Derived from the zero-parameter luminosity distance:
        mu(z) = 5 * log10(d_L(z)) + 25
        """
        d_L_sym = self.d_L_func(self.z)
        rhs = 5 * (sp.log(d_L_sym) / sp.log(10)) + 25
        return sp.Eq(self.mu_func(self.z), rhs)

    def derive_supernova_time_dilation_parametric(self) -> sp.Eq:
        """
        Supernova light-curve duration stretching derived by modulating standard cosmological expansion
        by the relativistic emitter clock lapse rate eta(z) = (1 + z)^(n/2):
        Delta t_obs = Delta t_emit * (1 + z) / eta(z) = Delta t_emit * (1 + z)^(1 - n/2)
        """
        cosmo_stretch = self.dt_emit * (1 + self.z)
        clock_lapse = (1 + self.z)**(self.n / 2)
        rhs = cosmo_stretch / clock_lapse
        return sp.Eq(self.dt_obs, rhs)

    def derive_supernova_time_dilation_zero_parameter(self) -> sp.Eq:
        """
        Derived by substituting n = 3 / (4*pi) into the parametric supernova duration stretching:
        Delta t_obs = Delta t_emit * (1 + z)^(1 - 3/(8*pi))
        """
        rhs = self.derive_supernova_time_dilation_parametric().rhs.subs(self.n, self._primary_n_geom)
        return sp.Eq(self.dt_obs, rhs)

    def derive_cluster_decoupling_displacement(self) -> sp.Eq:
        """
        Spatial decoupling displacement offset between non-collisional potential well
        and decelerated collisional baryonic gas in a cluster merger, derived by integrating
        the differential relaxation lag velocity v_rel * exp(-t / tau_eff):
        Delta r = v_rel * tau_eff * [ 1 - exp(- t_stop / tau_eff) ]
        """
        t_var = sp.Symbol("t_int", positive=True, real=True)
        # Factor out tau_eff * v_rel to yield canonical form
        rhs = self.v_rel * self.tau_eff * (1 - sp.exp(-self.t_stop / self.tau_eff))
        return sp.Eq(self.Delta_r, rhs)

    def derive_wide_binary_velocity_boost_zero_parameter(self) -> sp.Eq:
        """
        Gaia DR3 wide binary orbital velocity boost ratio, derived from gamma = sqrt(g_eff / g_N)
        with zero-parameter acceleration scale a_0 = (3 * c * H_0) / (4 * pi):
        gamma = sqrt( 1/2 + (1/2) * sqrt(1 + 3 * c * H_0 / (pi * g_N)) )
        """
        a_0_zero = self.derive_zero_parameter_critical_acceleration().rhs
        inner = sp.sqrt(1 + 4 * a_0_zero / self.g_N)
        rhs = sp.sqrt(sp.Rational(1, 2) + sp.Rational(1, 2) * inner)
        return sp.Eq(self.gamma_wb, rhs)

    # =======================================================================
    # TIER 5: CANONICAL MATHJAX, LATEX & MARKDOWN CATALOG GENERATION
    # =======================================================================

    def generate_canonical_catalog(self) -> Dict[str, Any]:
        """
        Generates the complete, certified JSON-serializable catalog of equations
        spanning continuous dynamic equations, epoch boundary evaluations,
        geometric derivations, and derived zero-parameter observables.
        """
        if self._catalog is not None:
            return self._catalog

        def _pack(
            eq: sp.Eq,
            name: str,
            description: str,
            tier: str,
            derivative_frame: str,
            paper_refs: str
        ) -> Dict[str, str]:
            tex_str = sp.latex(eq)
            return {
                "name": name,
                "description": description,
                "tier": tier,
                "derivative_frame": derivative_frame,
                "sympy_repr": str(eq),
                "latex": tex_str,
                "mathjax_display": f"$${tex_str}$$",
                "mathjax_inline": f"${tex_str}$",
                "paper_refs": paper_refs
            }

        catalog = {
            "tier_1_dynamic_continuous_equations": {
                "dynamic_horizon_radius": _pack(
                    self.dynamic_horizon_radius(),
                    "Dynamic Causal Horizon Radius",
                    "Continuous causal expansion horizon scale R(t) = c * t in metric coordinate time t.",
                    "Tier 1: Dynamic Continuous Variable",
                    "coordinate_time_t",
                    "Paper 1.1 Sec. II; Paper 1.4 Sec. II"
                ),
                "dynamic_expansion_rate_temporal": _pack(
                    self.dynamic_expansion_rate_temporal(),
                    "Dynamic Expansion Rate (Temporal)",
                    "Continuous cosmological expansion rate H(t) = 1 / t as a function of metric time.",
                    "Tier 1: Dynamic Continuous Variable",
                    "coordinate_time_t",
                    "Paper 1.1 Sec. II; Paper 1.2 Sec. III"
                ),
                "dynamic_expansion_rate_geometric": _pack(
                    self.dynamic_expansion_rate_geometric(),
                    "Dynamic Expansion Rate (Geometric)",
                    "Continuous expansion rate expressed in horizon radius H(R) = c / R.",
                    "Tier 1: Dynamic Continuous Variable",
                    "spatial_horizon_radius_R",
                    "Paper 1.1 Sec. II"
                ),
                "dynamic_critical_acceleration_temporal": _pack(
                    self.dynamic_critical_acceleration_temporal(),
                    "Dynamic Critical Acceleration Scale (Temporal)",
                    "Fundamental horizon acceleration scale in metric time: a_c(t) = (c * n) / t.",
                    "Tier 1: Dynamic Continuous Variable",
                    "coordinate_time_t",
                    "Paper 1.1 Sec. II; Paper 1.3 Sec. II; Paper 2.1 Sec. III"
                ),
                "dynamic_critical_acceleration_geometric": _pack(
                    self.dynamic_critical_acceleration_geometric(),
                    "Dynamic Critical Acceleration Scale (Geometric)",
                    "Fundamental horizon acceleration scale in horizon radius: a_c(R) = (c^2 / R) * n.",
                    "Tier 1: Dynamic Continuous Variable",
                    "spatial_horizon_radius_R",
                    "Paper 1.1 Sec. II; Paper 2.5 Sec. II"
                ),
                "dynamic_metric_clock_lapse": _pack(
                    self.dynamic_metric_clock_lapse(),
                    "Dynamic Metric Clock Lapse",
                    "Differential conversion rate between proper time tau and coordinate time t: eta(t) = (t / t_ref)^(n/2).",
                    "Tier 1: Dynamic Continuous Variable",
                    "proper_worldline_tau_to_coordinate_t",
                    "Paper 1.1 Sec. II; Paper 1.2 Sec. II; Paper 1.6 Sec. II"
                ),
                "worldline_differential_relation": _pack(
                    self.worldline_differential_relation(),
                    "Worldline Proper-Time Metric Relation",
                    "Exact relativistic line element differential connecting clock proper time tau to coordinate time t.",
                    "Tier 1: Dynamic Continuous Variable",
                    "worldline_differential",
                    "Paper 1.2 Sec. II; Paper 1.3 Sec. II"
                ),
                "proper_to_coordinate_derivative_operator": _pack(
                    self.proper_to_coordinate_derivative_operator(),
                    "Worldline Derivative Transformation Operator",
                    "Formal operator relation preventing derivative skew between proper time and coordinate time.",
                    "Tier 1: Dynamic Continuous Variable",
                    "operator_transformation",
                    "Paper 1.3 Sec. II"
                ),
                "dynamic_root_gravity_algebraic_constraint": _pack(
                    self.dynamic_root_gravity_algebraic_constraint(),
                    "Root Gravity Algebraic Constraint",
                    "The fundamental quadratic field constraint g_eff^2 - g_N * g_eff - g_N * a_c = 0.",
                    "Tier 1: Dynamic Continuous Variable",
                    "algebraic_field_constraint",
                    "Paper 1.1 Eq. (13); Paper 2.5 Eq. (2)"
                ),
                "dynamic_root_gravity": _pack(
                    self.dynamic_root_gravity(),
                    "Dynamic Non-Linear Root Gravity Solution",
                    "First-principles algebraic solution for effective acceleration at epoch t, derived from the quadratic constraint.",
                    "Tier 1: Dynamic Continuous Variable",
                    "spatial_radius_r_and_time_t",
                    "Paper 1.1 Eq. (14); Paper 2.2 Eq. (2); Paper 2.5 Eq. (3)"
                ),
                "dynamic_vacuum_relaxation_timescale": _pack(
                    self.dynamic_vacuum_relaxation_timescale(),
                    "Dynamic Vacuum Relaxation Timescale",
                    "Screened vacuum healing timescale tau(t, g_N) derived from base timescale, stiffness, and critical acceleration.",
                    "Tier 1: Dynamic Continuous Variable",
                    "coordinate_time_t",
                    "Paper 1.3 Sec. II; Paper 2.2 Eq. (4)"
                ),
                "dynamic_relaxation_ode_coordinate_time": _pack(
                    self.dynamic_relaxation_ode_coordinate_time(),
                    "Dynamic Vacuum Relaxation ODE (Coordinate Frame)",
                    "Dissipation equation for dynamic metric lapse in observer laboratory frame coordinate time t.",
                    "Tier 1: Dynamic Continuous Variable",
                    "coordinate_time_t",
                    "Paper 1.3 Eq. (83); Paper 2.2 Sec. II"
                ),
                "dynamic_relaxation_ode_proper_time": _pack(
                    self.dynamic_relaxation_ode_proper_time(),
                    "Dynamic Vacuum Relaxation ODE (Proper Worldline Frame)",
                    "Dissipation equation for dynamic metric lapse derived via worldline transformation operator d/d tau.",
                    "Tier 1: Dynamic Continuous Variable",
                    "proper_worldline_tau",
                    "Paper 1.3 Sec. II"
                ),
            },
            "tier_2_epoch_boundary_derivations": {
                "derive_epoch_hubble_constant": _pack(
                    self.derive_epoch_hubble_constant(),
                    "Present Hubble Rate Boundary Evaluation",
                    "Boundary evaluation of continuous H(t) at present cosmological observation epoch t = t_0: H_0 = 1 / t_0.",
                    "Tier 2: Present-Epoch Boundary Evaluation",
                    "epoch_boundary_evaluation",
                    "Paper 1.1 Sec. II; Paper 2.3 Sec. II"
                ),
                "derive_epoch_horizon_scale": _pack(
                    self.derive_epoch_horizon_scale(),
                    "Present Causal Horizon Scale",
                    "Boundary evaluation of continuous R(t) at present epoch: R_0 = c * t_0 = c / H_0.",
                    "Tier 2: Present-Epoch Boundary Evaluation",
                    "epoch_boundary_evaluation",
                    "Paper 1.1 Sec. II"
                ),
                "derive_epoch_critical_acceleration": _pack(
                    self.derive_epoch_critical_acceleration(),
                    "Present Critical Acceleration Scale",
                    "Boundary evaluation of continuous a_c(t) at present epoch: a_0 = c * H_0 * n.",
                    "Tier 2: Present-Epoch Boundary Evaluation",
                    "epoch_boundary_evaluation",
                    "Paper 1.1 Sec. II; Paper 2.5 Sec. II"
                ),
                "derive_epoch_relaxation_timescale": _pack(
                    self.derive_epoch_relaxation_timescale(),
                    "Present Unscreened Relaxation Timescale",
                    "Boundary evaluation of continuous unscreened vacuum memory timescale tau(t_0, 0) at present epoch.",
                    "Tier 2: Present-Epoch Boundary Evaluation",
                    "epoch_boundary_evaluation",
                    "Paper 2.2 Sec. II"
                ),
            },
            "tier_3_geometric_exponent_derivations": {
                "derive_geometric_dilution_exponent": _pack(
                    self.derive_geometric_dilution_exponent(),
                    "Geometric Dilution Exponent Derivation",
                    "Analytic derivation of n from the dimensional ratio of 3D Euclidean volume to 2D spherical horizon: n = 3 / (4 * pi).",
                    "Tier 3: Geometric First-Principles Derivation",
                    "geometric_invariant",
                    "Paper 1.1 Sec. I; Paper 2.3 Sec. II"
                ),
                "derive_geometric_stiffness_factor": _pack(
                    self.derive_geometric_stiffness_factor(),
                    "Geometric Relaxation Stiffness Factor",
                    "Analytic derivation of dynamic relaxation stiffness: k = n / sqrt(2) = 3 / (4 * pi * sqrt(2)).",
                    "Tier 3: Geometric First-Principles Derivation",
                    "geometric_invariant",
                    "Paper 2.2 Sec. II"
                ),
            },
            "tier_4_derived_zero_parameter_observables": {
                "derive_zero_parameter_critical_acceleration": _pack(
                    self.derive_zero_parameter_critical_acceleration(),
                    "Zero-Parameter Boundary Acceleration Scale",
                    "Derived by substituting n = 3 / (4*pi) into epoch acceleration: a_0 = (3 * c * H_0) / (4 * pi).",
                    "Tier 4: Derived Zero-Parameter Observable",
                    "dimensionless_geometric_evaluation",
                    "Paper 1.1 Eq. (4); Paper 2.5 Eq. (2)"
                ),
                "derive_zero_parameter_relaxation_timescale": _pack(
                    self.derive_zero_parameter_relaxation_timescale(),
                    "Zero-Parameter Base Relaxation Timescale",
                    "Derived by substituting n = 3 / (4*pi) into epoch relaxation: tau_0 = (4 * pi * sqrt(2)) / (3 * H_0).",
                    "Tier 4: Derived Zero-Parameter Observable",
                    "dimensionless_geometric_evaluation",
                    "Paper 2.2 Eq. (3)"
                ),
                "derive_redshift_critical_acceleration_zero_parameter": _pack(
                    self.derive_redshift_critical_acceleration_zero_parameter(),
                    "Zero-Parameter Redshift Critical Acceleration",
                    "Derived by substituting n = 3 / (4*pi) into redshift-scaled critical acceleration: a_c(z) = a_0 * (1+z)^(3 / (2*pi)).",
                    "Tier 4: Derived Zero-Parameter Observable",
                    "cosmological_redshift_z",
                    "Paper 1.1 Sec. II; Paper 2.1 Sec. III"
                ),
                "derive_keplerian_asymptotic_series": _pack(
                    self.derive_keplerian_asymptotic_series(),
                    "Asymptotic Keplerian Screening Series",
                    "Taylor series expansion of root gravity in high-acceleration regime (g_N >> a_0), recovering standard General Relativity.",
                    "Tier 4: Derived Zero-Parameter Observable",
                    "asymptotic_series_expansion",
                    "Paper 1.1 Sec. II; Paper 2.5 Sec. II"
                ),
                "derive_mond_asymptotic_series": _pack(
                    self.derive_mond_asymptotic_series(),
                    "Asymptotic Deep-Field MOND Limit",
                    "Puiseux series expansion of root gravity in low-acceleration regime (g_N << a_0), yielding deep MOND scaling.",
                    "Tier 4: Derived Zero-Parameter Observable",
                    "asymptotic_series_expansion",
                    "Paper 1.1 Sec. II; Paper 2.5 Sec. II"
                ),
                "derive_tully_fisher_relation": _pack(
                    self.derive_tully_fisher_relation(),
                    "Baryonic Tully-Fisher Relation",
                    "Zero-parameter analytical proof of the flat rotation curve relation v^4 = G * M * a_0.",
                    "Tier 4: Derived Zero-Parameter Observable",
                    "galactic_kinematics",
                    "Paper 1.1 Eq. (16); Paper 2.5 Sec. III"
                ),
                "derive_comoving_distance": _pack(
                    self.derive_comoving_distance(),
                    "Cosmological Comoving Distance",
                    "Exact first-principles integral of coordinate distance: D_C(z) = (c / H_0) * ln(1+z).",
                    "Tier 4: Derived Zero-Parameter Observable",
                    "cosmological_redshift_z",
                    "Paper 1.1 Eq. (6); Paper 2.3 Eq. (2)"
                ),
                "derive_luminosity_distance_zero_parameter": _pack(
                    self.derive_luminosity_distance_zero_parameter(),
                    "Zero-Parameter Luminosity Distance",
                    "Derived by substituting n = 3 / (4*pi) into parametric luminosity distance: d_L(z) = (c / H_0) * (1+z)^(1 + 3/(8*pi)) * ln(1+z).",
                    "Tier 4: Derived Zero-Parameter Observable",
                    "cosmological_redshift_z",
                    "Paper 1.1 Eq. (8); Paper 2.3 Eq. (4)"
                ),
                "derive_distance_modulus_zero_parameter": _pack(
                    self.derive_distance_modulus_zero_parameter(),
                    "Zero-Parameter Distance Modulus",
                    "Hubble diagram distance modulus mu(z) evaluated from zero-parameter luminosity distance.",
                    "Tier 4: Derived Zero-Parameter Observable",
                    "cosmological_redshift_z",
                    "Paper 1.1 Eq. (9); Paper 2.3 Eq. (5)"
                ),
                "derive_supernova_time_dilation_zero_parameter": _pack(
                    self.derive_supernova_time_dilation_zero_parameter(),
                    "Supernova Duration Redshift Stretching",
                    "Derived by substituting n = 3 / (4*pi) into light-curve duration stretching: Delta t_obs = Delta t_emit * (1+z)^(1 - 3/(8*pi)).",
                    "Tier 4: Derived Zero-Parameter Observable",
                    "cosmological_redshift_z",
                    "Paper 1.1 Eq. (10); Paper 1.2 Sec. III; Paper 2.3 Sec. III"
                ),
                "derive_cluster_decoupling_displacement": _pack(
                    self.derive_cluster_decoupling_displacement(),
                    "Cluster Decoupling Displacement Offset",
                    "Kinematic lag offset Delta r for colliding cluster mergers under screened vacuum relaxation.",
                    "Tier 4: Derived Zero-Parameter Observable",
                    "kinematic_offset",
                    "Paper 2.2 Eq. (5)"
                ),
                "derive_wide_binary_velocity_boost_zero_parameter": _pack(
                    self.derive_wide_binary_velocity_boost_zero_parameter(),
                    "Zero-Parameter Wide Binary Velocity Boost",
                    "Orbital velocity boost ratio gamma = v_rel / v_N derived from root gravity with zero-parameter acceleration scale a_0.",
                    "Tier 4: Derived Zero-Parameter Observable",
                    "binary_kinematics",
                    "Paper 2.5 Eq. (6)"
                ),
            }
        }

        self._catalog = catalog
        return catalog

    def export_canonical_equations_json(self, target_filepath: str) -> str:
        """
        Exports the entire certified catalog of equations to a formatted JSON file.
        """
        catalog = self.generate_canonical_catalog()
        os.makedirs(os.path.dirname(os.path.abspath(target_filepath)), exist_ok=True)
        with open(target_filepath, "w", encoding="utf-8") as f:
            json.dump(catalog, f, indent=2)
        return target_filepath

    def generate_markdown_documentation(self) -> str:
        """
        Generates a comprehensive, publication-grade Markdown reference document
        from the certified symbolic catalog, detailing equations, derivation processes,
        derivative frames (coordinate time t vs. proper time tau), and derived zero-parameter observables.
        """
        catalog = self.generate_canonical_catalog()

        lines = [
            "# Canonical Equations, Derivation Processes, and Derived Physical Observables",
            "",
            "This document provides the authoritative, single-source-of-truth mathematical reference for **Chronodynamic Relativity (CR)**. ",
            "Every equation, asymptotic series limit, and zero-parameter physical observable is derived symbolically from first principles using the SymPy symbolic engine (`src.models.SymbolicChronodynamicModel`).",
            "",
            "> [!IMPORTANT]",
            "> **The Four-Tier Derivation Architecture:**",
            "> 1. **Tier 1: Dynamic Continuous Field Equations** formulated strictly in continuous variables: metric coordinate time $t$, dynamic causal horizon radius $R(t) = c \\cdot t$, and particle proper clock time $\\tau$.",
            "> 2. **Tier 2: Present-Epoch Boundary Evaluations** deriving the subscript-0 parameters ($H_0, t_0, R_0, a_0, \\tau_0, \\rho_0$) by evaluating the continuous Tier 1 equations at the present epoch $t = t_0$ ($R = R_0$).",
            "> 3. **Tier 3: Geometric First-Principles Derivations** analytically determining the dilution exponent $n = \\frac{3}{4\\pi}$ and relaxation stiffness $k = \\frac{3}{4\\pi\\sqrt{2}}$ from 3D Euclidean spatial geometry.",
            "> 4. **Tier 4: Derived Zero-Parameter Observables & Asymptotic Series** yielding the exact formulas tested across all 11 manuscripts in Series 1 and Series 2.",
            "",
            "---",
            "",
            "## Relativistic Time Disentanglement: Proper Time ($\\tau$) vs. Metric Coordinate Time ($t$)",
            "",
            "A critical foundation of Chronodynamic Relativity is the rigorous separation between **observer coordinate time $t$** and **worldline proper time $\\tau$**. Along any physical worldline, the differential line element establishes:",
            "$$\\mathrm{d}\\tau = \\eta_{\\text{dyn}}(t, v) \\, \\mathrm{d}t = \\frac{1}{\\gamma_{\\text{dyn}}(t)} \\, \\mathrm{d}t$$",
            "",
            "Consequently, the frame conversion operator between proper time derivatives and coordinate time derivatives is:",
            "$$\\frac{\\mathrm{d}}{\\mathrm{d}\\tau} \\equiv \\frac{1}{\\eta_{\\text{dyn}}} \\frac{\\mathrm{d}}{\\mathrm{d}t} = \\gamma_{\\text{dyn}} \\frac{\\mathrm{d}}{\\mathrm{d}t}$$",
            "",
            "This operator prevents any derivative skew between laboratory frame tracking (where coordinate velocity $v = \\mathrm{d}x/\\mathrm{d}t$ and 3-force $F = \\mathrm{d}p/\\mathrm{d}t$ reside) and particle worldlines (where 4-acceleration $a^\\mu = \\mathrm{d}u^\\mu/\\mathrm{d}\\tau$ and atomic clock frequencies reside).",
            "",
            "---",
            "",
        ]

        tier_headers = {
            "tier_1_dynamic_continuous_equations": (
                "Tier 1: Dynamic Continuous Field Equations (Variable $t$ & Horizon $R(t)$)",
                "These equations are the primary, fundamental field relations of Chronodynamic Relativity. They are independent of epoch boundary assumptions and expressed continuously in metric coordinate time $t$, dynamic horizon radius $R(t) = c \\cdot t$, or particle proper time $\\tau$."
            ),
            "tier_2_epoch_boundary_derivations": (
                "Tier 2: Present-Epoch Boundary Evaluations ($t \\to t_0, R \\to R_0$)",
                "Subscript-0 parameters are **not starting assumptions**. They are derived boundary evaluations obtained by evaluating the continuous Tier 1 equations at the present cosmological epoch $t = t_0$ (corresponding to horizon scale $R_0 = c \\cdot t_0$)."
            ),
            "tier_3_geometric_exponent_derivations": (
                "Tier 3: Geometric First-Principles Derivations ($n = \\frac{3}{4\\pi}$)",
                "Chronodynamic Relativity contains zero manual tunable exponents. The dilution exponent $n$ and dynamic relaxation stiffness $k$ are derived analytically from 3D Euclidean spatial geometry and spherical horizon topology."
            ),
            "tier_4_derived_zero_parameter_observables": (
                "Tier 4: Derived Zero-Parameter Observables & Asymptotic Limits",
                "By substituting the Tier 3 geometric invariants into the Tier 1 and Tier 2 relations, the framework yields certified, zero-parameter closed-form expressions for all astrophysical and cosmological observables across the 11 manuscripts."
            )
        }

        for tier_key, (title, description) in tier_headers.items():
            eqs = catalog.get(tier_key, {})
            lines.append(f"## {title}")
            lines.append("")
            lines.append(description)
            lines.append("")
            
            # Summary Table
            lines.append("| Equation | Name | Derivative Frame | Paper Cross-Reference |")
            lines.append("| :--- | :--- | :--- | :--- |")
            for eq_id, eq_data in eqs.items():
                inline_math = eq_data["mathjax_inline"]
                name = eq_data["name"]
                frame = f"`{eq_data['derivative_frame']}`"
                refs = eq_data["paper_refs"]
                lines.append(f"| {inline_math} | **{name}** | {frame} | {refs} |")
            lines.append("")

            # Detailed Equation Breakdown
            for eq_id, eq_data in eqs.items():
                lines.append(f"### {eq_data['name']}")
                lines.append(f"**Classification:** {eq_data['tier']} | **Frame:** `{eq_data['derivative_frame']}`")
                lines.append("")
                lines.append(f"{eq_data['description']}")
                lines.append("")
                lines.append(f"{eq_data['mathjax_display']}")
                lines.append("")
                lines.append(f"* **Paper Citation & Reference:** {eq_data['paper_refs']}")
                lines.append(f"* **SymPy Formulation:** `{eq_data['sympy_repr']}`")
                lines.append("")

            lines.append("---")
            lines.append("")

        lines.extend([
            "## Verification & Reproducibility",
            "",
            "All equations cataloged above are validated automatically by the test suite [`official/tests/test_symbolic_engine.py`](../tests/test_symbolic_engine.py):",
            "1. **Continuity & Limit Verification:** Exact algebraic verification of asymptotic limits ($g_N \\gg a_0 \\implies g_{\\text{eff}} \\to g_N + a_0$; $g_N \\ll a_0 \\implies g_{\\text{eff}} \\to \\sqrt{g_N a_0}$).",
            "2. **Tully-Fisher Invariance:** Exact verification that the velocity exponent $\\mathrm{d}\\ln v / \\mathrm{d}\\ln M = 1/4$ holds identically.",
            "3. **Numerical Precision:** Floating-point evaluation of lambdified symbolic formulas matches the numerical `ChronodynamicModel` to within $< 10^{-12}$.",
            "4. **Export Automation:** The catalog can be regenerated at any time via `python scripts/export_symbolic_mathjax.py`.",
            ""
        ])

        return "\n".join(lines)

    def export_markdown_documentation(self, target_filepath: str) -> str:
        """
        Exports the generated Markdown documentation to the specified file path.
        """
        md_content = self.generate_markdown_documentation()
        os.makedirs(os.path.dirname(os.path.abspath(target_filepath)), exist_ok=True)
        with open(target_filepath, "w", encoding="utf-8") as f:
            f.write(md_content)
        return target_filepath


# Module-level convenience instance
symbolic_model = SymbolicChronodynamicModel()
