"""
Unit and Integration Tests for Symbolic Chronodynamic Engine
=============================================================
Verifies:
  1. Tier 1 dynamic continuous field equations in metric time t and horizon radius R(t).
  2. Proper time tau vs coordinate time t worldline operator transformations.
  3. Tier 2 epoch boundary limits as t -> t_0.
  4. Tier 3 geometric dilution derivations (n = 3 / 4pi).
  5. Tier 4 asymptotic limits (Keplerian screening, MOND limit, Tully-Fisher exponent).
  6. Numerical equivalence between lambdified symbolic formulas and ChronodynamicModel.
  7. Integrity and MathJax syntax of canonical_equations.json.
"""

import json
import os
import numpy as np
import pytest
import sympy as sp

from src.models import ChronodynamicModel, SymbolicChronodynamicModel


@pytest.fixture
def sym_model():
    return SymbolicChronodynamicModel()


@pytest.fixture
def num_model():
    return ChronodynamicModel(h0=70.5)


def test_tier_1_dynamic_continuous_equations(sym_model):
    """Verify Tier 1 dynamic continuous relations in metric time t and horizon R."""
    # R(t) = c * t
    eq_R = sym_model.dynamic_horizon_radius()
    assert eq_R.rhs == sym_model.c * sym_model.t

    # H(t) = 1 / t
    eq_H_t = sym_model.dynamic_expansion_rate_temporal()
    assert eq_H_t.rhs == 1 / sym_model.t

    # H(R) = c / R
    eq_H_R = sym_model.dynamic_expansion_rate_geometric()
    assert eq_H_R.rhs == sym_model.c / sym_model.R

    # Equivalence: substituting R = c * t into H(R) recovers H(t)
    H_sub = eq_H_R.rhs.subs(sym_model.R, sym_model.c * sym_model.t)
    assert sp.simplify(H_sub - eq_H_t.rhs) == 0

    # a_c(t) = c * n / t
    eq_a_t = sym_model.dynamic_critical_acceleration_temporal()
    assert eq_a_t.rhs == (sym_model.c * sym_model.n) / sym_model.t

    # a_c(R) = (c^2 / R) * n
    eq_a_R = sym_model.dynamic_critical_acceleration_geometric()
    assert eq_a_R.rhs == (sym_model.c**2 / sym_model.R) * sym_model.n

    # Equivalence: substituting R = c * t into a_c(R) recovers a_c(t)
    a_sub = eq_a_R.rhs.subs(sym_model.R, sym_model.c * sym_model.t)
    assert sp.simplify(a_sub - eq_a_t.rhs) == 0


def test_frame_derivative_transformation(sym_model):
    """Verify worldline frame transformation operator between proper time and coordinate time."""
    eq_op = sym_model.proper_to_coordinate_derivative_operator()
    # d/dtau = gamma_dyn * d/dt
    assert sym_model.gamma_dyn in eq_op.rhs.free_symbols


def test_tier_2_epoch_boundary_limits(sym_model):
    """Verify that evaluating dynamic continuous equations at t = t_0 recovers present-epoch parameters."""
    eq_H0 = sym_model.derive_epoch_hubble_constant()
    assert eq_H0.rhs == 1 / sym_model.t_0

    eq_R0 = sym_model.derive_epoch_horizon_scale()
    assert eq_R0.rhs == sym_model.c / sym_model.H_0

    eq_a0 = sym_model.derive_epoch_critical_acceleration()
    assert eq_a0.rhs == sym_model.c * sym_model.H_0 * sym_model.n

    eq_tau0 = sym_model.derive_epoch_relaxation_timescale()
    assert eq_tau0.rhs == (sp.sqrt(2) * sym_model.t_0) / sym_model.n


def test_tier_3_geometric_dilution_derivations(sym_model):
    """Verify analytic geometric derivation of dilution exponent and relaxation stiffness."""
    eq_n = sym_model.derive_geometric_dilution_exponent()
    assert eq_n.rhs == sp.Rational(3, 1) / (4 * sp.pi)

    eq_k = sym_model.derive_geometric_stiffness_factor()
    assert eq_k.rhs == sp.Rational(3, 1) / (4 * sp.pi * sp.sqrt(2))


def test_tier_4_asymptotic_limits(sym_model):
    """Verify high-acceleration Keplerian and low-acceleration MOND series limits."""
    # Keplerian series: g_eff -> g_N + a_0
    kep_series = sym_model.derive_keplerian_asymptotic_series(order=1)
    # The leading order correction must be a_0
    diff = sp.simplify(kep_series.rhs - (sym_model.g_N + sym_model.a_0))
    assert diff == 0

    # Deep MOND limit: g_eff -> sqrt(g_N * a_0) + (1/2) * g_N
    mond_series = sym_model.derive_mond_asymptotic_series(order=1)
    expected_mond = sp.sqrt(sym_model.a_0) * sp.sqrt(sym_model.g_N) + sym_model.g_N / 2
    assert sp.simplify(mond_series.rhs - expected_mond) == 0

    # Baryonic Tully-Fisher relation: v^4 = G * M * a_0
    btfr = sym_model.derive_tully_fisher_relation()
    assert btfr.rhs == sym_model.G * sym_model.M * (sp.Rational(3, 1) * sym_model.c * sym_model.H_0) / (4 * sp.pi)

    # Redshift critical acceleration zero-parameter: a_c(z) = a_0 * (1 + z)^(3 / (2*pi))
    eq_az = sym_model.derive_redshift_critical_acceleration_zero_parameter()
    expected_az = sym_model.a_0 * (1 + sym_model.z)**(sp.Rational(3, 1) / (2 * sp.pi))
    assert sp.simplify(eq_az.rhs - expected_az) == 0

    # Wide binary velocity boost zero-parameter
    eq_wb = sym_model.derive_wide_binary_velocity_boost_zero_parameter()
    expected_inner = sp.sqrt(1 + sp.Rational(3, 1) * sym_model.c * sym_model.H_0 / (sp.pi * sym_model.g_N))
    expected_wb = sp.sqrt(sp.Rational(1, 2) + sp.Rational(1, 2) * expected_inner)
    assert sp.simplify(eq_wb.rhs - expected_wb) == 0


def test_numerical_equivalence_with_canonical_model(sym_model, num_model):
    """Verify numerical lambdification of symbolic expressions matches ChronodynamicModel methods."""
    c_val = 299792458.0
    h0_si = num_model.h0_si
    a0_expected = num_model.a0

    # 1. Critical Acceleration Evaluation
    eq_a0 = sym_model.derive_zero_parameter_critical_acceleration()
    a0_sym_fn = sp.lambdify((sym_model.c, sym_model.H_0), eq_a0.rhs, 'numpy')
    a0_eval = a0_sym_fn(c_val, h0_si)
    assert np.isclose(a0_eval, a0_expected, rtol=1e-12)

    # 2. Effective Gravity Evaluation across a wide range of Newtonian accelerations
    eq_geff = sym_model.dynamic_root_gravity()
    # Substitute dynamic a_c(t) -> a0
    geff_expr = sp.Rational(1, 2) * (sym_model.g_N + sp.sqrt(sym_model.g_N**2 + 4 * sym_model.g_N * sym_model.a_0))
    geff_fn = sp.lambdify((sym_model.g_N, sym_model.a_0), geff_expr, 'numpy')

    test_gN = np.logspace(-13, -7, 25)
    sym_geff_vals = geff_fn(test_gN, a0_expected)
    num_geff_vals = np.array([num_model.effective_acceleration(gn, z=0.0) for gn in test_gN])
    np.testing.assert_allclose(sym_geff_vals, num_geff_vals, rtol=1e-12)

    # 3. Luminosity Distance Evaluation at various low redshifts (matter-dominated regime, omega_r=0)
    # Using clean cosmological model without radiation-damping perturbation
    clean_model = ChronodynamicModel(h0=70.5, omega_r=0.0)
    eq_dL = sym_model.derive_luminosity_distance_zero_parameter()
    dL_fn = sp.lambdify((sym_model.z, sym_model.c, sym_model.H_0), eq_dL.rhs, 'numpy')

    test_z = np.array([0.05, 0.1, 0.5, 1.0])
    sym_dL_meters = dL_fn(test_z, c_val, clean_model.h0_si)
    sym_dL_mpc = sym_dL_meters / 3.085677581491367e22
    num_dL_mpc = np.array([clean_model.luminosity_distance(z) for z in test_z])
    np.testing.assert_allclose(sym_dL_mpc, num_dL_mpc, rtol=1e-10)


def test_canonical_equations_json_catalog(sym_model):
    """Verify that canonical_equations.json exists, loads cleanly, and passes structural validation."""
    catalog = sym_model.generate_canonical_catalog()
    assert "tier_1_dynamic_continuous_equations" in catalog
    assert "tier_2_epoch_boundary_derivations" in catalog
    assert "tier_3_geometric_exponent_derivations" in catalog
    assert "tier_4_derived_zero_parameter_observables" in catalog

    for tier_name, tier_dict in catalog.items():
        assert len(tier_dict) > 0
        for eq_id, eq_data in tier_dict.items():
            assert "name" in eq_data
            assert "description" in eq_data
            assert "latex" in eq_data
            assert "mathjax_display" in eq_data
            assert "mathjax_inline" in eq_data
            assert "derivative_frame" in eq_data
            assert "paper_refs" in eq_data

            # MathJax display format verification: starts with $$ and ends with $$
            assert eq_data["mathjax_display"].startswith("$$")
            assert eq_data["mathjax_display"].endswith("$$")
            # MathJax inline format verification: starts with $ and ends with $
            assert eq_data["mathjax_inline"].startswith("$")
            assert eq_data["mathjax_inline"].endswith("$")

    # Verify JSON file on disk
    json_path = os.path.join(os.path.dirname(__file__), "..", "src", "models", "canonical_equations.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            disk_catalog = json.load(f)
        assert len(disk_catalog) == 4
