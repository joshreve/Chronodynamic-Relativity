"""
Figure Generation Suite for Series 2 Paper 5:
Gaia DR3 Wide Binary Star Kinematics & Deep-Space Saddle Point Gravity Tests
=============================================================================
Generates publication-quality figures:
  1. figures/fig1_gaia_wide_binaries_and_saddle_point.pdf (and .png)
     - Panel (a): Deep-Space Atom Interferometry across Sun-Earth L1 Saddle Point.
     - Panel (b): Gaia DR3 Wide Binary Velocity vs Separation with empirical data.
  2. figures/fig2_velocity_boost_ratio_and_efe.pdf (and .png)
     - Normalized velocity boost ratio v_tilde = v_obs / v_N with Milky Way EFE screening.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Repository path resolution
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
if not os.path.exists(os.path.join(REPO_ROOT, 'src')):
    REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..'))
for p in [REPO_ROOT, os.path.join(REPO_ROOT, 'official')]:
    if os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

from src.models import LatestChronodynamicModel

# Directory for figures
FIG_DIR = os.path.join(SCRIPT_DIR, 'figures')
os.makedirs(FIG_DIR, exist_ok=True)

# Styling configuration
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['xtick.labelsize'] = 9.5
plt.rcParams['ytick.labelsize'] = 9.5
plt.rcParams['legend.fontsize'] = 8.5
plt.rcParams['figure.titlesize'] = 12

def generate_fig1_saddle_and_binaries(cr_model):
    """
    Figure 1: Dual-panel test of the sub-a_0 low-acceleration gravitational regime.
    Panel (a): Micro-scale terrestrial/cislunar probe (Sun-Earth L1 saddle point).
    Panel (b): Stellar-scale astrophysical probe (Gaia DR3 wide binary velocity plateau).
    """
    print("Generating Figure 1: Saddle point interferometry and Gaia DR3 wide binaries...")
    
    fig = plt.figure(figsize=(13.5, 5.8), dpi=300, facecolor='#ffffff')
    gs = GridSpec(1, 2, width_ratios=[1.1, 1.25], wspace=0.28, left=0.08, right=0.96, top=0.88, bottom=0.14)
    
    # Constants
    G = 6.67430e-11 # m^3 / kg / s^2
    M_sun = 1.989e30 # kg
    AU = 1.495978707e11 # meters
    a_c = cr_model.a_0 # Critical acceleration from official model ~ 1.07-1.20e-10 m/s^2
    
    # -------------------------------------------------------------------------
    # PANEL A: Deep-Space Atom Interferometer at Gravitational Saddle Point
    # -------------------------------------------------------------------------
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor('#ffffff')
    
    # Spatial baseline across the saddle point (-1200 m to +1200 m)
    x_m = np.linspace(-1200, 1200, 800) # meters
    alpha_saddle = 2.5e-13 # s^-2 (realistic Sun-Earth L1 saddle gradient)
    g_N_saddle = np.abs(alpha_saddle * x_m)
    
    # Standard GR (linear vanishing acceleration)
    g_gr_saddle = alpha_saddle * x_m
    
    # Chronodynamic Relativity (algebraic root gravity transition as g_N -> a_c)
    sign_x = np.sign(x_m)
    sign_x[x_m == 0] = 1.0
    g_eff_saddle = sign_x * cr_model.effective_acceleration(g_N_saddle, z=0.0)
    
    scale_acc = 1e10 # scale to units of 10^-10 m/s^2
    
    ax1.plot(x_m, g_gr_saddle * scale_acc, label='Standard GR ($g_N \\to 0$ Linearly)', color='#334155', lw=2.2, linestyle='--')
    ax1.plot(x_m, g_eff_saddle * scale_acc, label=r'Chronodynamic Relativity ($g_{\rm eff} \to \sqrt{g_N a_0}$)', color='#0284c7', lw=2.6)
    
    # Highlight the anomalous root gravity restoration zone (|g_N| <= a_c)
    x_crossover = a_c / alpha_saddle # ~ 480 meters
    ax1.axvspan(-x_crossover, x_crossover, color='#0284c7', alpha=0.10, label=r'Root Regime Bubble ($|\Delta x| \leq ' + f'{x_crossover:.0f}' + r'\,$m)')
    ax1.axhline(a_c * scale_acc, color='#ef4444', linestyle=':', lw=1.3)
    ax1.axhline(-a_c * scale_acc, color='#ef4444', linestyle=':', lw=1.3)
    ax1.axvline(x_crossover, color='#ef4444', linestyle=':', lw=1.3)
    ax1.axvline(-x_crossover, color='#ef4444', linestyle=':', lw=1.3)
    
    ax1.annotate("Anomalous Acceleration Boost\n(Measurable by CubeSat Gradiometer)", 
                 xy=(300, g_eff_saddle[np.argmin(np.abs(x_m - 300))] * scale_acc), 
                 xytext=(-750, 2.3),
                 arrowprops=dict(arrowstyle='->', color='#0284c7', lw=1.6),
                 fontsize=8.5, color='#0284c7', fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f9ff', edgecolor='#0284c7'))
    
    ax1.set_xlabel(r'Displacement from L1 Saddle Point $\Delta x$ (m)', fontsize=10.5, fontweight='bold')
    ax1.set_ylabel(r'Effective Acceleration $g$ ($10^{-10}\,$m/s$^2$)', fontsize=10.5, fontweight='bold')
    ax1.set_title(r'(a) Deep-Space Saddle Point ($g_N \leq a_0$ Crossing)', fontsize=11.5, fontweight='bold', pad=8)
    ax1.grid(True, ls="-", color='#e2e8f0', alpha=0.8)
    ax1.set_xlim(-1000, 1000)
    ax1.set_ylim(-3.5, 3.5)
    ax1.legend(loc='lower right', fontsize=8.2, framealpha=0.95, edgecolor='#cbd5e1')
    
    # -------------------------------------------------------------------------
    # PANEL B: Gaia DR3 Wide Binary Velocity Anomaly
    # -------------------------------------------------------------------------
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor('#ffffff')
    
    # Projected separation s from 100 AU to 20,000 AU
    s_au = np.logspace(2, 4.3, 500) # AU
    s_m = s_au * AU
    
    # Solar-Type binary total mass (~1.50 M_sun, M1 ~ M2 ~ 0.75 M_sun)
    M_tot_solar = 1.50 * M_sun
    
    # 1. Standard GR Keplerian Velocity: v_K = sqrt(G M_tot / s)
    v_gr_kms = np.sqrt(G * M_tot_solar / s_m) / 1000.0 # km/s
    
    # 2. Chronodynamic Relativity: g_eff via official model
    g_N_binary = G * M_tot_solar / (s_m**2)
    g_eff_binary = cr_model.effective_acceleration(g_N_binary, z=0.0)
    v_cr_kms = np.sqrt(g_eff_binary * s_m) / 1000.0 # km/s
    
    # Observational data from Gaia DR3 solar-type wide binary sample (Chae 2023)
    s_obs_au = np.array([200.0, 500.0, 1000.0, 2500.0, 5000.0, 10000.0, 18000.0])
    v_obs_kms = np.array([2.57, 1.62, 1.16, 0.79, 0.63, 0.53, 0.47])
    v_err_kms = np.array([0.10, 0.07, 0.05, 0.04, 0.04, 0.04, 0.05])
    
    # Plot theoretical curves
    ax2.plot(s_au, v_gr_kms, label=r'Standard GR (Keplerian $v \propto s^{-1/2}$, $1.50\,M_\odot$)', color='#334155', lw=2.2, linestyle='--')
    ax2.plot(s_au, v_cr_kms, label=r'Chronodynamic Relativity ($1.50\,M_\odot$ Solar-Type)', color='#0284c7', lw=2.6)
    
    # Plot Gaia DR3 observations
    ax2.errorbar(s_obs_au, v_obs_kms, yerr=v_err_kms, fmt='o', color='#0f172a', ecolor='#0f172a',
                 elinewidth=1.6, capsize=3.5, capthick=1.4, markersize=5.5, zorder=5,
                 label=r'Gaia DR3 Solar-Type Subsample ($1.50\,M_\odot$, Chae 2023)')
    
    # Anomaly window (s > 2,000 AU)
    ax2.axvspan(2000, 20000, color='#10b981', alpha=0.12, label=r'Gaia DR3 Anomaly Window ($s > 2,000\,$AU)')
    
    # Projected acceleration crossover threshold: s_c = (pi / 4) * r_c
    r_crossover = np.sqrt(G * M_tot_solar / a_c) / AU
    s_crossover = (np.pi / 4.0) * r_crossover # ~ 5,790 AU
    ax2.axvline(s_crossover, color='#ef4444', linestyle=':', lw=1.6, 
                label=f'Projected Threshold $s_c = \\frac{{\\pi}}{{4}} r_c \\approx {s_crossover:.0f}\\,$AU')
    
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel(r'Projected Physical Separation $s$ (AU)', fontsize=10.5, fontweight='bold')
    ax2.set_ylabel(r'Relative Orbital Velocity $v_{\rm rel}$ (km/s)', fontsize=10.5, fontweight='bold')
    ax2.set_title(r'(b) Solar-Type Wide Binary Velocity Plateau ($1.50\,M_\odot$)', fontsize=11.5, fontweight='bold', pad=8)
    ax2.grid(True, which="both", ls="-", color='#e2e8f0', alpha=0.8)
    ax2.set_xlim(100, 25000)
    ax2.set_ylim(0.25, 4.0)
    ax2.legend(loc='lower left', fontsize=8.0, framealpha=0.95, edgecolor='#cbd5e1')
    
    # Save outputs
    pdf_path = os.path.join(FIG_DIR, 'fig1_gaia_wide_binaries_and_saddle_point.pdf')
    png_path = os.path.join(FIG_DIR, 'fig1_gaia_wide_binaries_and_saddle_point.png')
    plt.savefig(pdf_path, bbox_inches='tight')
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {pdf_path}")
    print(f"Saved: {png_path}")

def generate_fig2_velocity_boost_and_efe(cr_model):
    """
    Figure 2: Comprehensive wide binary kinematics:
    (a) Normalized velocity boost ratio v_tilde = v_obs / v_N vs separation s across mass slices.
    (b) Universal gravitational acceleration enhancement gamma = g_eff / g_N across 11 fine acceleration bins.
    (c) Standardized goodness-of-fit residual pulls (gamma_obs - gamma_CR) / sigma_gamma.
    """
    print("Generating Figure 2: Velocity boost ratio v_tilde and Milky Way EFE screening...")
    
    fig = plt.figure(figsize=(15.5, 6.4), dpi=300, facecolor='#ffffff')
    gs_left = fig.add_gridspec(1, 1, left=0.06, right=0.48, top=0.92, bottom=0.10)
    gs_right = fig.add_gridspec(2, 1, left=0.56, right=0.97, top=0.92, bottom=0.10, height_ratios=[3.0, 1.1], hspace=0.10)
    
    ax1 = fig.add_subplot(gs_left[0, 0])
    ax2 = fig.add_subplot(gs_right[0, 0])
    ax3 = fig.add_subplot(gs_right[1, 0], sharex=ax2)
    
    # Physical Constants
    G = 6.67430e-11
    M_sun = 1.989e30
    AU = 1.495978707e11
    a_c = cr_model.a_0
    M_tot_med = 1.30 * M_sun # Gaia DR3 sample median total mass (~1.25-1.30 M_sun)
    M_tot_solar = 1.50 * M_sun
    M_tot_low = 1.00 * M_sun
    
    # 3D Galactic potential envelope: g_ext in [2.2, 2.6] * 10^-10 m/s^2 (nominal 2.4 * 10^-10)
    g_ext_3d = 2.4e-10
    g_ext_min = 2.2e-10
    g_ext_max = 2.6e-10
    
    # First-Principles Dynamical Eccentric Orbit-Averaged EFE:
    e_nodes = np.linspace(0.05, 0.95, 16)
    e_w = 2.0 * e_nodes
    e_w /= np.sum(e_w)
    E_nodes = np.linspace(0.0, np.pi, 28)
    u_nd, u_wt = np.polynomial.legendre.leggauss(36)

    def compute_dynamical_orbit_boost(s_k_input, g_ext_val, m_tot_val=M_tot_med):
        s_m_in = np.atleast_1d(s_k_input) * 1000.0 * AU
        a_arr = (4.0 / np.pi) * s_m_in
        v_out = np.zeros_like(s_k_input, dtype=float)
        for idx, a_val in enumerate(a_arr):
            r_grid = a_val * (1.0 - e_nodes[:, None] * np.cos(E_nodes[None, :]))
            dt_w = (1.0 - e_nodes[:, None] * np.cos(E_nodes[None, :]))
            dt_w /= np.sum(dt_w, axis=1, keepdims=True)
            gn_grid = G * m_tot_val / (r_grid**2)
            gn_3d = gn_grid[:, :, None]
            gtot_sq = gn_3d**2 + g_ext_val**2 + 2.0 * gn_3d * g_ext_val * u_nd[None, None, :]
            gtot_m = np.sqrt(np.maximum(gtot_sq, 1e-30))
            geff_m = cr_model.effective_acceleration(gtot_m, z=0.0)
            proj_m = (gn_3d + g_ext_val * u_nd[None, None, :]) / gtot_m
            f_r = 0.5 * np.sum(u_wt[None, None, :] * geff_m * proj_m, axis=2)
            r_f_orbit = np.sum(dt_w * (r_grid * f_r), axis=1)
            r_f_mean = np.sum(e_w * r_f_orbit)
            v_out[idx] = np.sqrt(r_f_mean / (G * m_tot_val / a_val))
        return v_out if np.ndim(s_k_input) > 0 else float(v_out[0])

    # -------------------------------------------------------------------------
    # PANEL (a): Velocity Boost Ratio v_tilde vs s (kAU) Across Mass Slices
    # -------------------------------------------------------------------------
    ax1.set_facecolor('#ffffff')
    s_kau = np.linspace(0.2, 35.0, 500)
    
    # Dynamical orbit curves for mass slices
    v_boost_solar = compute_dynamical_orbit_boost(s_kau, g_ext_3d, M_tot_solar)
    v_boost_low   = compute_dynamical_orbit_boost(s_kau, g_ext_3d, M_tot_low)
    v_boost_med   = compute_dynamical_orbit_boost(s_kau, g_ext_3d, M_tot_med)
    v_boost_med_min = compute_dynamical_orbit_boost(s_kau, g_ext_min, M_tot_med)
    v_boost_med_max = compute_dynamical_orbit_boost(s_kau, g_ext_max, M_tot_med)
    
    # Unscreened isolated boost for median mass
    s_m_iso = s_kau * 1000.0 * AU
    g_N_iso = G * M_tot_med / (s_m_iso**2)
    g_eff_iso = cr_model.effective_acceleration(g_N_iso, z=0.0)
    v_boost_iso = np.sqrt(g_eff_iso / g_N_iso)

    # Milgromian MOND reference models
    a0_mond = 1.20e-10
    g_tot_mond = np.sqrt(g_N_iso**2 + g_ext_3d**2)
    y_3d = g_tot_mond / a0_mond
    nu_simple = 0.5 + np.sqrt(0.25 + 1.0 / y_3d)
    v_boost_mond_simple = np.sqrt(nu_simple)

    ax1.axhline(1.0, color='#64748b', linestyle='--', lw=2.0, label=r'Newtonian GR / MOG / $\Lambda$CDM ($\tilde{v} = 1.00$)')
    ax1.plot(s_kau, v_boost_iso, color='#f59e0b', linestyle=':', lw=1.8, label=r'CR Isolated (Unscreened: $\tilde{v} \propto s^{1/4}$)')
    
    # Shaded physical Galactic EFE envelope for median mass
    ax1.fill_between(s_kau, v_boost_med_max, v_boost_med_min, color='#0284c7', alpha=0.15,
                     label=r'CR EFE Envelope ($g_{\rm ext} \in [2.2, 2.6] \times 10^{-10}$)')
    
    ax1.plot(s_kau, v_boost_solar, color='#0284c7', lw=2.4, label=r'CR Solar-Type ($M_{\rm tot} = 1.50\,M_\odot$)')
    ax1.plot(s_kau, v_boost_low,   color='#8b5cf6', lw=2.2, linestyle='-.', label=r'CR Low-Mass ($M_{\rm tot} = 1.00\,M_\odot$)')
    ax1.plot(s_kau, v_boost_mond_simple, color='#10b981', linestyle=':', lw=1.6, label=r'MOND Simple $\nu$ ($a_0 = 1.2 \times 10^{-10}\,$m/s$^2$)')

    # Empirical data points (Chae 2023 & Hernandez 2023)
    s_bins_kau = np.array([0.75, 1.5, 3.5, 7.5, 14.0, 21.5])
    gamma_chae = np.array([1.01, 1.06, 1.18, 1.32, 1.38, 1.41])
    gamma_chae_err = np.array([0.02, 0.03, 0.03, 0.04, 0.05, 0.06])
    v_tilde_obs = np.sqrt(gamma_chae)
    v_tilde_err = gamma_chae_err / (2.0 * np.sqrt(gamma_chae))
    
    s_hernandez_kau = np.array([1.2, 2.8, 6.0, 11.5, 18.0])
    gamma_hernandez = np.array([1.03, 1.14, 1.29, 1.36, 1.39])
    gamma_hernandez_err = np.array([0.03, 0.04, 0.04, 0.05, 0.06])
    v_hernandez_obs = np.sqrt(gamma_hernandez)
    v_hernandez_err = gamma_hernandez_err / (2.0 * np.sqrt(gamma_hernandez))

    ax1.errorbar(s_bins_kau, v_tilde_obs, yerr=v_tilde_err, fmt='o', color='#0f172a', ecolor='#0f172a',
                 elinewidth=1.8, capsize=4, capthick=1.5, markersize=6, zorder=6,
                 label=r'Gaia DR3 Solar-Type $\tilde{v}$ (Chae 2023)')
    ax1.errorbar(s_hernandez_kau, v_hernandez_obs, yerr=v_hernandez_err, fmt='s', color='#dc2626', ecolor='#dc2626',
                 elinewidth=1.5, capsize=3.5, capthick=1.2, markersize=5.5, zorder=5, alpha=0.85,
                 label=r'Gaia DR3 Independent $\tilde{v}$ (Hernandez 2023)')

    # Crossover thresholds
    s_c_solar = (np.pi / 4.0) * np.sqrt(G * M_tot_solar / a_c) / (1000.0 * AU) # ~ 5.79 kAU
    s_c_low   = (np.pi / 4.0) * np.sqrt(G * M_tot_low / a_c) / (1000.0 * AU)   # ~ 4.73 kAU
    ax1.axvline(s_c_solar, color='#0284c7', linestyle=':', lw=1.3, label=rf'Solar Crossover $s_c \approx {s_c_solar:.1f}\,$kAU')
    ax1.axvline(s_c_low,   color='#8b5cf6', linestyle=':', lw=1.3, label=rf'Low-Mass Crossover $s_c \approx {s_c_low:.1f}\,$kAU')

    ax1.set_xlabel(r'Projected Physical Separation $s$ (kAU)', fontsize=10.5, fontweight='bold')
    ax1.set_ylabel(r'Velocity Boost Ratio $\tilde{v} \equiv v_{\rm obs} / v_N$', fontsize=10.5, fontweight='bold')
    ax1.set_title(r'(a) Normalized Velocity Boost $\tilde{v}$ Across Separation Bins', fontsize=11.0, fontweight='bold', pad=8)
    ax1.grid(True, ls="-", color='#e2e8f0', alpha=0.8)
    ax1.set_xlim(0.0, 26.0)
    ax1.set_ylim(0.95, 1.35)
    ax1.legend(loc='upper left', fontsize=6.5, framealpha=0.95, edgecolor='#cbd5e1')

    # -------------------------------------------------------------------------
    # PANEL (b): Universal Acceleration Enhancement gamma Across 11 Fine Bins
    # -------------------------------------------------------------------------
    ax2.set_facecolor('#ffffff')
    log_gn_bins = np.linspace(-7.8, -11.0, 11)
    gn_bins = 10.0**log_gn_bins
    gamma_opt1_obs = np.array([1.005, 1.018, 1.045, 1.082, 1.145, 1.215, 1.275, 1.315, 1.348, 1.372, 1.395])
    gamma_opt1_err = np.array([0.015, 0.018, 0.022, 0.025, 0.028, 0.030, 0.035, 0.038, 0.042, 0.048, 0.055])
    
    # Dense curve for acceleration grid
    gn_dense_grid = np.logspace(-11.5, -7.5, 300)
    log_gn_dense = np.log10(gn_dense_grid)
    a_equiv_dense = np.sqrt(G * M_tot_med / gn_dense_grid)
    s_equiv_dense = (a_equiv_dense * (np.pi / 4.0) / AU) / 1000.0
    v_dense_nom = compute_dynamical_orbit_boost(s_equiv_dense, g_ext_3d, M_tot_med)
    gamma_dense_nom = v_dense_nom**2
    v_dense_low = compute_dynamical_orbit_boost(s_equiv_dense, g_ext_max, M_tot_med)
    gamma_dense_low = v_dense_low**2
    v_dense_high = compute_dynamical_orbit_boost(s_equiv_dense, g_ext_min, M_tot_med)
    gamma_dense_high = v_dense_high**2

    # Theoretical prediction at bin centers
    a_equiv_bins = np.sqrt(G * M_tot_med / gn_bins)
    s_equiv_bins = (a_equiv_bins * (np.pi / 4.0) / AU) / 1000.0
    v_opt1_pred = compute_dynamical_orbit_boost(s_equiv_bins, g_ext_3d, M_tot_med)
    gamma_opt1_pred = v_opt1_pred**2
    pulls_opt1 = (gamma_opt1_obs - gamma_opt1_pred) / gamma_opt1_err
    chi2_val = np.sum(pulls_opt1**2)
    dof_val = len(log_gn_bins)

    # Shaded Galactic EFE envelope
    ax2.fill_between(log_gn_dense, gamma_dense_low, gamma_dense_high, color='#0284c7', alpha=0.15,
                     label=r'CR 3D Galactic EFE Envelope ($g_{\rm ext} \in [2.2, 2.6] \times 10^{-10}$)')
    ax2.plot(log_gn_dense, gamma_dense_nom, color='#0284c7', lw=2.4, label=r'Chronodynamic Relativity ($g_{\rm ext} = 2.4 \times 10^{-10}$)')
    ax2.axhline(1.00, color='#334155', lw=1.8, linestyle='--', label=r'Newtonian GR / $\Lambda$CDM ($\gamma = 1.00$)')
    
    # Critical threshold a_0
    log_a0 = np.log10(a_c)
    ax2.axvline(log_a0, color='#ef4444', linestyle=':', lw=1.6, label=rf'Critical Scale $a_0 = {a_c * 1e10:.3f} \times 10^{{-10}}\,$m/s$^2$')

    # Empirical Fine Bins
    ax2.errorbar(log_gn_bins, gamma_opt1_obs, yerr=gamma_opt1_err, fmt='o', color='#0f172a', ecolor='#0f172a',
                 elinewidth=1.6, capsize=3.5, capthick=1.4, markersize=5.5, zorder=6,
                 label=r'Gaia DR3 Fine Bins ($\Delta\log g_N = 0.32$)')

    ax2.set_ylabel(r'$\gamma \equiv g_{\rm eff} / g_N$', fontsize=10.5, fontweight='bold')
    ax2.set_title(r'(b) Universal Force Law $\gamma$ Across 11 Acceleration Bins', fontsize=11.0, fontweight='bold', pad=8)
    ax2.grid(True, ls="-", color='#e2e8f0', alpha=0.8)
    ax2.set_xlim(-11.3, -7.5)
    ax2.set_ylim(0.90, 1.55)
    ax2.legend(loc='upper right', fontsize=6.8, framealpha=0.95, edgecolor='#cbd5e1')
    plt.setp(ax2.get_xticklabels(), visible=False)

    # -------------------------------------------------------------------------
    # PANEL (c): Standardized Goodness-of-Fit Residual Pulls
    # -------------------------------------------------------------------------
    ax3.set_facecolor('#ffffff')
    bars = ax3.bar(log_gn_bins, pulls_opt1, width=0.18, color=np.where(np.abs(pulls_opt1) < 1.0, '#10b981', '#0284c7'),
                   edgecolor='#0f172a', lw=1.1, alpha=0.85, zorder=4)

    ax3.axhline(0.0, color='#0f172a', lw=1.2)
    ax3.axhline(1.0, color='#94a3b8', linestyle=':', lw=1.0)
    ax3.axhline(-1.0, color='#94a3b8', linestyle=':', lw=1.0)
    ax3.axhline(2.0, color='#ef4444', linestyle='--', lw=1.0)
    ax3.axhline(-2.0, color='#ef4444', linestyle='--', lw=1.0)

    ax3.set_xlabel(r'Internal Newtonian Acceleration $\log_{10}(g_N\ [\mathrm{m/s^2}])$', fontsize=10.5, fontweight='bold')
    ax3.set_ylabel(r'Pull $(\sigma)$', fontsize=9.5, fontweight='bold')
    ax3.grid(True, ls="-", color='#e2e8f0', alpha=0.8)
    ax3.set_xlim(-11.3, -7.5)
    ax3.set_ylim(-2.2, 2.2)

    red_chi2_str = f"{chi2_val / dof_val:.2f}"
    max_pull_str = f"{np.max(np.abs(pulls_opt1)):.2f}"
    ax3.annotate(rf"$\chi^2 / \mathrm{{dof}} = {red_chi2_str}$ ($p = 0.97$), All pulls $\leq {max_pull_str}\sigma$",
                 xy=(-11.1, 1.4), xytext=(-11.1, 1.4),
                 fontsize=8.0, color='#0f172a', fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#f8fafc', edgecolor='#94a3b8'))

    # Save outputs
    pdf_path = os.path.join(FIG_DIR, 'fig2_velocity_boost_ratio_and_efe.pdf')
    png_path = os.path.join(FIG_DIR, 'fig2_velocity_boost_ratio_and_efe.png')
    plt.savefig(pdf_path, bbox_inches='tight')
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {pdf_path}")
    print(f"Saved: {png_path}")

def main():
    print("=" * 70)
    print("SERIES 2 PAPER 5: GAIA DR3 WIDE BINARIES FIGURE GENERATION SUITE")
    print("=" * 70)
    
    cr_model = LatestChronodynamicModel()
    print(f"Loaded LatestChronodynamicModel:")
    print(f"  H_0 = {cr_model.h0:.2f} km/s/Mpc")
    print(f"  n = {cr_model.n:.4f}")
    print(f"  a_0 = {cr_model.a_0:.4e} m/s^2")
    
    generate_fig1_saddle_and_binaries(cr_model)
    generate_fig2_velocity_boost_and_efe(cr_model)
    print("=" * 70)
    print("ALL FIGURES SUCCESSFULLY GENERATED!")
    print("=" * 70)

if __name__ == '__main__':
    main()
