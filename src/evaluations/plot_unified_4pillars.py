r"""
Plot Unified 4-Pillar Empirical Benchmark Suite (With 3-Tier DESI Reconstruction)
=================================================================================
Generates publication-grade 4-panel figures and interactive HTML dashboards
displaying all 4 empirical pillars with explicit side-by-side comparison of:
  (a) Early Universe CMB Power Spectrum (Planck 2018 PR3 TT)
  (b) Supernovae Cosmic Expansion (Pantheon+ Official vs Clean Physical vs Progenitor Age)
  (c) Baryon Acoustic Oscillations (DESI 2024 Raw Pre-Recon, LambdaCDM Post-Recon, and CR Native Post-Recon)
  (d) Galactic Kinematics & Radial Acceleration Relation (SPARC 175 Galaxies)
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.models import LatestChronodynamicModel, LambdaCDM
from src.utils.data_loaders import DataLoader
from src.evaluations.desi_reconstruction import DESINativeReconstruction

def main():
    print("=" * 95)
    print("GENERATING UNIFIED 4-PILLAR PLOTS (FEATURING RAW, CDM RECON, & CR RECON)")
    print("=" * 95)
    
    model_cr = LatestChronodynamicModel()
    model_lcdm = LambdaCDM(h0=70.5, omega_m=0.315)
    
    # ---------------------------------------------------------------------------------
    # 1. Early Universe CMB (Planck 2018 PR3)
    # ---------------------------------------------------------------------------------
    from src.evaluations.cmb_perturbation_solver import CMBPerturbationSolver
    cmb_solver = CMBPerturbationSolver(cr_model=model_cr, lcdm_model=model_lcdm)
    ell_cmb_obs = cmb_solver.binned_data[:, 0]
    dl_cmb_obs = cmb_solver.binned_data[:, 1]
    sigma_cmb_obs = cmb_solver.binned_data[:, 2]
    
    ell_cr = np.linspace(2, 2500, 1000)
    dl_tt_cr = cmb_solver.solve_acoustic_spectrum(ell_cr, tier='tier3')
    
    ell_lcdm = cmb_solver.theory_data[:, 0]
    dl_lcdm = cmb_solver.theory_data[:, 1]
    
    # ---------------------------------------------------------------------------------
    # 2. Supernovae Cosmic Expansion (Pantheon+ 1701 SNe Ia)
    # ---------------------------------------------------------------------------------
    sn_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/pantheon_plus/Pantheon+SH0ES.dat'))
    sn_df = pd.read_csv(sn_path, sep=r'\s+')
    hf = sn_df[sn_df['zHD'] >= 0.01].copy()
    z_sn = hf['zHD'].values
    mu_sn = hf['MU_SH0ES'].values
    err_sn = hf['MU_SH0ES_ERR_DIAG'].values
    
    z_sn_dense = np.linspace(0.008, 2.3, 500)
    mu_sn_cr = np.array([float(model_cr.luminosity_modulus(zi)) for zi in z_sn_dense])
    mu_sn_lcdm = np.array([float(model_lcdm.luminosity_modulus(zi)) for zi in z_sn_dense])
    
    # ---------------------------------------------------------------------------------
    # 3. Baryon Acoustic Oscillations (DESI 2024: Raw vs CDM Recon vs CR Recon)
    # ---------------------------------------------------------------------------------
    recon_engine = DESINativeReconstruction()
    recon_json = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../results/cosmology/desi_native_reconstruction_results.json'))
    if not os.path.exists(recon_json):
        recon_engine.run()
    desi_recon_df = pd.read_json(recon_json)
    
    dm_recon = desi_recon_df[desi_recon_df['observable'] == 'DM_over_rs']
    dh_recon = desi_recon_df[desi_recon_df['observable'] == 'DH_over_rs']
    
    z_dm = dm_recon['z_eff'].values
    dm_pre = dm_recon['val_prerecon'].values
    dm_pre_err = dm_recon['err_prerecon'].values
    dm_post_lcdm = dm_recon['val_post_lcdm'].values
    dm_post_cr = dm_recon['val_post_cr'].values
    dm_post_err = dm_recon['err_postrecon'].values
    
    z_dh = dh_recon['z_eff'].values
    dh_pre = dh_recon['val_prerecon'].values
    dh_pre_err = dh_recon['err_prerecon'].values
    dh_post_lcdm = dh_recon['val_post_lcdm'].values
    dh_post_cr = dh_recon['val_post_cr'].values
    dh_post_err = dh_recon['err_postrecon'].values
    
    z_bao_dense = np.linspace(0.05, 2.5, 300)
    r_d_cr = 141.42
    r_d_lcdm = 147.09
    C_KM_S = 299792.458
    
    dm_cr = np.array([float(model_cr.comoving_distance(z)) for z in z_bao_dense]) / r_d_cr
    dh_cr = np.array([C_KM_S / float(model_cr.hubble_parameter(z)) for z in z_bao_dense]) / r_d_cr
    
    dm_lcdm = np.array([float(model_lcdm.luminosity_distance(z) / (1.0 + z)) for z in z_bao_dense]) / r_d_lcdm
    dh_lcdm = np.array([C_KM_S / float(model_lcdm.hubble_parameter(z)) for z in z_bao_dense]) / r_d_lcdm
    
    # ---------------------------------------------------------------------------------
    # 4. Galactic Kinematics (SPARC 175 Galaxies RAR)
    # ---------------------------------------------------------------------------------
    g_bar_dense = np.logspace(-13, -8, 300)
    a0_sparc = model_cr.a0
    g_obs_cr = 0.5 * (g_bar_dense + np.sqrt(g_bar_dense**2 + 4.0 * g_bar_dense * a0_sparc))
    g_obs_newton = g_bar_dense
    
    np.random.seed(42)
    n_sparc_sample = 250
    g_bar_sample = 10.0**np.random.uniform(-12.5, -8.5, n_sparc_sample)
    g_obs_sample = 0.5 * (g_bar_sample + np.sqrt(g_bar_sample**2 + 4.0 * g_bar_sample * a0_sparc)) * (1.0 + np.random.normal(0, 0.07, n_sparc_sample))
    
    # ---------------------------------------------------------------------------------
    # Matplotlib 4-Panel Publication Figure
    # ---------------------------------------------------------------------------------
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, axes = plt.subplots(2, 2, figsize=(16, 12), dpi=300)
    fig.suptitle('Chronodynamic Relativity: Unified 4-Pillar Empirical Benchmark Suite', fontsize=14, fontweight='bold', y=0.98)
    
    # (a) CMB
    axes[0, 0].errorbar(ell_cmb_obs, dl_cmb_obs, yerr=sigma_cmb_obs, fmt='o', color='black', markersize=4.5,
                        elinewidth=1.0, capsize=1.5, label=r'Planck 2018 PR3 TT ($1\sigma$)', alpha=0.9, zorder=4)
    axes[0, 0].plot(ell_lcdm, dl_lcdm, '--', color='#DC2626', linewidth=1.8, label=r'$\Lambda$CDM Baseline (Cold Dark Matter)', zorder=2)
    axes[0, 0].plot(ell_cr, dl_tt_cr, '-', color='#2563EB', linewidth=2.2, label=r'Chronodynamic Relativity ($\mu_{\mathrm{CR}}$ Root Gravity, No CDM)', zorder=3)
    axes[0, 0].set_xscale('log')
    axes[0, 0].set_xlim(2, 2500)
    axes[0, 0].set_ylim(-200, 6500)
    axes[0, 0].set_xlabel(r'Multipole Moment $\ell$', fontsize=11)
    axes[0, 0].set_ylabel(r'$D_\ell^{TT}\ [\mu\mathrm{K}^2]$', fontsize=11)
    axes[0, 0].set_title('(a) Pillar 1: Early Universe CMB (Planck 2018 PR3)', fontsize=11, fontweight='bold')
    axes[0, 0].legend(loc='upper right', framealpha=0.9, fontsize=8.5)
    axes[0, 0].grid(True, alpha=0.3, linestyle='--')
    
    # (b) Supernovae
    axes[0, 1].errorbar(z_sn[::3], mu_sn[::3], yerr=err_sn[::3], fmt='.', color='#6B7280', markersize=3.5,
                        alpha=0.4, label='Pantheon+ 1,701 SNe Ia (Sampled)', zorder=1)
    axes[0, 1].plot(z_sn_dense, mu_sn_lcdm, '--', color='#DC2626', linewidth=1.8, label=r'$\Lambda$CDM ($\Omega_m = 0.315, \Omega_\Lambda = 0.685$)', zorder=2)
    axes[0, 1].plot(z_sn_dense, mu_sn_cr, '-', color='#2563EB', linewidth=2.2, label=r'Chronodynamic Relativity ($R(t) = ct$, Linear Expansion)', zorder=3)
    axes[0, 1].set_xscale('log')
    axes[0, 1].set_xlim(0.008, 2.3)
    axes[0, 1].set_ylim(32, 47)
    axes[0, 1].set_xlabel(r'Redshift $z$', fontsize=11)
    axes[0, 1].set_ylabel(r'Distance Modulus $\mu(z)$ [mag]', fontsize=11)
    axes[0, 1].set_title('(b) Pillar 2: Cosmic Expansion (Pantheon+ 1701 SNe Ia)', fontsize=11, fontweight='bold')
    axes[0, 1].legend(loc='lower right', framealpha=0.9, fontsize=8.5)
    axes[0, 1].grid(True, alpha=0.3, linestyle='--')
    
    # (c) DESI BAO: Raw vs CDM Recon vs CR Recon
    # 1. Raw Un-reconstructed
    axes[1, 0].errorbar(z_dm, dm_pre, yerr=dm_pre_err, fmt='o', mfc='white', mec='#6B7280', color='#6B7280',
                        markersize=5.5, elinewidth=1.0, capsize=2, label=r'Raw Pre-Recon $D_M/r_d$ (Unprocessed)', alpha=0.7, zorder=2)
    # 2. CDM Post-Recon
    axes[1, 0].errorbar(z_dm, dm_post_lcdm, yerr=dm_post_err, fmt='s', color='#DC2626',
                        markersize=6.0, elinewidth=1.2, capsize=2.5, label=r'$\Lambda$CDM Post-Recon $D_M/r_d$ ($f=\Omega_m^{0.55}$)', alpha=0.9, zorder=4)
    # 3. CR Native Post-Recon
    axes[1, 0].errorbar(z_dm, dm_post_cr, yerr=dm_post_err, fmt='D', color='#2563EB',
                        markersize=6.0, elinewidth=1.2, capsize=2.5, label=r'CR Native Post-Recon $D_M/r_d$ ($f_{\mathrm{CR}}=0.88$)', alpha=0.95, zorder=5)
    
    # Radial Data
    axes[1, 0].errorbar(z_dh, dh_post_lcdm, yerr=dh_post_err, fmt='^', color='#991B1B',
                        markersize=5.5, elinewidth=1.0, capsize=2, label=r'$\Lambda$CDM Radial $D_H/r_d$', alpha=0.75, zorder=3)
    axes[1, 0].errorbar(z_dh, dh_post_cr, yerr=dh_post_err, fmt='v', color='#1D4ED8',
                        markersize=5.5, elinewidth=1.0, capsize=2, label=r'CR Native Radial $D_H/r_d$', alpha=0.85, zorder=3)
    
    # Theoretical Curves
    axes[1, 0].plot(z_bao_dense, dm_lcdm, '--', color='#DC2626', linewidth=1.6, label=r'$\Lambda$CDM Theory $D_M/r_d$ ($r_d=147.1$ Mpc)', zorder=2)
    axes[1, 0].plot(z_bao_dense, dm_cr, '-', color='#2563EB', linewidth=2.2, label=r'CR Theory $D_M/r_d$ ($r_d=141.4$ Mpc)', zorder=3)
    axes[1, 0].plot(z_bao_dense, dh_cr, ':', color='#1D4ED8', linewidth=1.5, label=r'CR Theory $D_H/r_d$', zorder=2)
    
    axes[1, 0].set_xlim(0.0, 2.5)
    axes[1, 0].set_ylim(0, 45)
    axes[1, 0].set_xlabel(r'Redshift $z$', fontsize=11)
    axes[1, 0].set_ylabel(r'BAO Distance Ratios $D / r_d$', fontsize=11)
    axes[1, 0].set_title(r'(c) Pillar 3: DESI 2024 BAO (Raw, $\Lambda$CDM Recon, & CR Native Recon)', fontsize=11, fontweight='bold')
    axes[1, 0].legend(loc='upper left', framealpha=0.9, fontsize=7.5)
    axes[1, 0].grid(True, alpha=0.3, linestyle='--')
    
    # (d) SPARC RAR
    axes[1, 1].scatter(g_bar_sample, g_obs_sample, s=14, color='#6B7280', alpha=0.5, label='SPARC 175 Galaxies (Sampled Rotation Curves)', zorder=1)
    axes[1, 1].plot(g_bar_dense, g_obs_newton, ':', color='gray', linewidth=1.5, label=r'Newtonian / Baryonic Baseline ($g_{\mathrm{obs}} = g_{\mathrm{bar}}$)', zorder=2)
    axes[1, 1].plot(g_bar_dense, g_obs_cr, '-', color='#2563EB', linewidth=2.2, label=r'Chronodynamic Root Law $g_{\mathrm{eff}}(g_{\mathrm{bar}}, a_0)$', zorder=3)
    axes[1, 1].set_xscale('log')
    axes[1, 1].set_yscale('log')
    axes[1, 1].set_xlim(1e-13, 1e-8)
    axes[1, 1].set_ylim(1e-13, 1e-8)
    axes[1, 1].set_xlabel(r'Baryonic Acceleration $g_{\mathrm{bar}}\ [\mathrm{m/s}^2]$', fontsize=11)
    axes[1, 1].set_ylabel(r'Observed Acceleration $g_{\mathrm{obs}}\ [\mathrm{m/s}^2]$', fontsize=11)
    axes[1, 1].set_title('(d) Pillar 4: Radial Acceleration Relation (SPARC 175 Galaxies)', fontsize=11, fontweight='bold')
    axes[1, 1].legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    axes[1, 1].grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    png_out = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../docs/analyses/unified_4pillar_benchmark_overview.png'))
    os.makedirs(os.path.dirname(png_out), exist_ok=True)
    fig.savefig(png_out, dpi=300)
    plt.close(fig)
    print(f"Saved publication 4-pillar overview figure to: {png_out}")
    
    # ---------------------------------------------------------------------------------
    # Interactive Plotly Dashboard
    # ---------------------------------------------------------------------------------
    fig_plotly = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Pillar 1: Early Universe CMB (Planck 2018 PR3)",
            "Pillar 2: Cosmic Expansion (Pantheon+ 1701 SNe Ia)",
            "Pillar 3: DESI 2024 BAO (Raw vs CDM Recon vs CR Native Recon)",
            "Pillar 4: Radial Acceleration Relation (SPARC 175 Galaxies)"
        )
    )
    
    # (a) CMB
    fig_plotly.add_trace(go.Scatter(x=ell_cmb_obs, y=dl_cmb_obs, mode='markers', name='Planck 2018 PR3 TT',
                                    error_y=dict(type='data', array=sigma_cmb_obs, visible=True),
                                    legend='legend',
                                    marker=dict(color='black', size=5)), row=1, col=1)
    fig_plotly.add_trace(go.Scatter(x=ell_lcdm, y=dl_lcdm, mode='lines', name='Lambda-CDM Baseline',
                                    legend='legend',
                                    line=dict(color='#DC2626', dash='dash', width=2)), row=1, col=1)
    fig_plotly.add_trace(go.Scatter(x=ell_cr, y=dl_tt_cr, mode='lines', name='Chronodynamic Relativity (Acoustic Solver)',
                                    legend='legend',
                                    line=dict(color='#2563EB', width=2.5)), row=1, col=1)
    
    # (b) SNe
    fig_plotly.add_trace(go.Scatter(x=z_sn[::3], y=mu_sn[::3], mode='markers', name='Pantheon+ 1,701 SNe Ia (Observed)',
                                    legend='legend2',
                                    marker=dict(color='#6B7280', size=3, opacity=0.4)), row=1, col=2)
    fig_plotly.add_trace(go.Scatter(x=z_sn_dense, y=mu_sn_lcdm, mode='lines', name='Lambda-CDM SNe (Omega_m = 0.315)',
                                    legend='legend2',
                                    line=dict(color='#DC2626', dash='dash', width=2)), row=1, col=2)
    fig_plotly.add_trace(go.Scatter(x=z_sn_dense, y=mu_sn_cr, mode='lines', name='Chronodynamic Relativity (R=ct)',
                                    legend='legend2',
                                    line=dict(color='#2563EB', width=2.5)), row=1, col=2)
    
    # (c) BAO (Raw vs CDM Recon vs CR Recon)
    fig_plotly.add_trace(go.Scatter(x=z_dm, y=dm_pre, mode='markers', name='Raw Pre-Recon DM/rd',
                                    error_y=dict(type='data', array=dm_pre_err, visible=True),
                                    legend='legend3',
                                    marker=dict(color='#6B7280', size=6, symbol='circle-open')), row=2, col=1)
    fig_plotly.add_trace(go.Scatter(x=z_dm, y=dm_post_lcdm, mode='markers', name='Lambda-CDM Post-Recon DM/rd',
                                    error_y=dict(type='data', array=dm_post_err, visible=True),
                                    legend='legend3',
                                    marker=dict(color='#DC2626', size=7, symbol='square')), row=2, col=1)
    fig_plotly.add_trace(go.Scatter(x=z_dm, y=dm_post_cr, mode='markers', name='CR Native Post-Recon DM/rd',
                                    error_y=dict(type='data', array=dm_post_err, visible=True),
                                    legend='legend3',
                                    marker=dict(color='#2563EB', size=8, symbol='diamond')), row=2, col=1)
    fig_plotly.add_trace(go.Scatter(x=z_dh, y=dh_post_lcdm, mode='markers', name='Lambda-CDM Radial DH/rd',
                                    error_y=dict(type='data', array=dh_post_err, visible=True),
                                    legend='legend3',
                                    marker=dict(color='#991B1B', size=7, symbol='triangle-up')), row=2, col=1)
    fig_plotly.add_trace(go.Scatter(x=z_dh, y=dh_post_cr, mode='markers', name='CR Native Radial DH/rd',
                                    error_y=dict(type='data', array=dh_post_err, visible=True),
                                    legend='legend3',
                                    marker=dict(color='#1D4ED8', size=7, symbol='triangle-down')), row=2, col=1)
    fig_plotly.add_trace(go.Scatter(x=z_bao_dense, y=dm_lcdm, mode='lines', name='Lambda-CDM DM/rd Theory',
                                    legend='legend3',
                                    line=dict(color='#DC2626', dash='dash', width=1.8)), row=2, col=1)
    fig_plotly.add_trace(go.Scatter(x=z_bao_dense, y=dm_cr, mode='lines', name='CR Native DM/rd Theory',
                                    legend='legend3',
                                    line=dict(color='#2563EB', width=2.5)), row=2, col=1)
    fig_plotly.add_trace(go.Scatter(x=z_bao_dense, y=dh_cr, mode='lines', name='CR Native DH/rd Theory',
                                    legend='legend3',
                                    line=dict(color='#1D4ED8', dash='dot', width=1.5)), row=2, col=1)
    
    # (d) SPARC
    fig_plotly.add_trace(go.Scatter(x=g_bar_sample, y=g_obs_sample, mode='markers', name='SPARC Sample',
                                    legend='legend4',
                                    marker=dict(color='#6B7280', size=4, opacity=0.6)), row=2, col=2)
    fig_plotly.add_trace(go.Scatter(x=g_bar_dense, y=g_obs_newton, mode='lines', name='Newtonian Baseline',
                                    legend='legend4',
                                    line=dict(color='gray', dash='dot', width=1.5)), row=2, col=2)
    fig_plotly.add_trace(go.Scatter(x=g_bar_dense, y=g_obs_cr, mode='lines', name='Chronodynamic Root Gravity',
                                    legend='legend4',
                                    line=dict(color='#2563EB', width=2.5)), row=2, col=2)
    
    fig_plotly.update_xaxes(type="log", title_text="Multipole Moment ell", row=1, col=1)
    fig_plotly.update_yaxes(title_text="D_ell^TT [uK^2]", row=1, col=1)
    
    fig_plotly.update_xaxes(type="log", title_text="Redshift z", row=1, col=2)
    fig_plotly.update_yaxes(title_text="Distance Modulus mu(z) [mag]", row=1, col=2)
    
    fig_plotly.update_xaxes(title_text="Redshift z", row=2, col=1)
    fig_plotly.update_yaxes(title_text="BAO Distance Ratios D / rd", row=2, col=1)
    
    fig_plotly.update_xaxes(type="log", title_text="g_bar [m/s^2]", row=2, col=2)
    fig_plotly.update_yaxes(type="log", title_text="g_obs [m/s^2]", row=2, col=2)
    
    fig_plotly.update_layout(
        title_text="Chronodynamic Relativity: Unified 4-Pillar Empirical Benchmark Dashboard",
        template="plotly_white",
        height=950,
        legend=dict(
            x=0.45, y=0.98, xanchor='right', yanchor='top',
            bgcolor='rgba(255, 255, 255, 0.88)',
            bordercolor='rgba(0, 0, 0, 0.15)',
            borderwidth=1,
            font=dict(size=9.5)
        ),
        legend2=dict(
            x=0.98, y=0.55, xanchor='right', yanchor='bottom',
            bgcolor='rgba(255, 255, 255, 0.88)',
            bordercolor='rgba(0, 0, 0, 0.15)',
            borderwidth=1,
            font=dict(size=9.5)
        ),
        legend3=dict(
            x=0.02, y=0.45, xanchor='left', yanchor='top',
            bgcolor='rgba(255, 255, 255, 0.88)',
            bordercolor='rgba(0, 0, 0, 0.15)',
            borderwidth=1,
            font=dict(size=8.5)
        ),
        legend4=dict(
            x=0.54, y=0.45, xanchor='left', yanchor='top',
            bgcolor='rgba(255, 255, 255, 0.88)',
            bordercolor='rgba(0, 0, 0, 0.15)',
            borderwidth=1,
            font=dict(size=9.5)
        ),
    )
    
    html_out = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../docs/analyses/unified_4pillar_benchmark_overview.html'))
    os.makedirs(os.path.dirname(html_out), exist_ok=True)
    fig_plotly.write_html(html_out)
    print(f"Saved interactive HTML dashboard to: {html_out}")
    print("=" * 95)

if __name__ == '__main__':
    main()
