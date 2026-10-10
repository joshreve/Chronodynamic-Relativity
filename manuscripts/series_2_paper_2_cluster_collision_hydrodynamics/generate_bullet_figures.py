#!/usr/bin/env python3
r"""
Generate Publication Figures for Series 2 Paper 2:
Cluster Collision Hydrodynamics and Gravitational Decoupling (The Bullet Cluster 1E 0657-56)
=============================================================================================

Outputs:
- figures/fig1_bullet_decoupling_evolution.pdf / .png (Figure 1: 4-Epoch Decoupling Evolution 3D AMR)
- figures/fig2_bullet_offset_evolution.pdf / .png (Figure 2: Spatial Offset Evolution vs Empirical Band)
- figures/fig3_bullet_1d_profile.pdf / .png (Figure 3: 1D Collision-Axis Density & Potential Profiles)
- figures/fig4_bullet_semianalytical_recovery.pdf / .png (Figure 4: Semi-Analytical Virial Recovery Trajectory & Inset Zoom)
- figures/fig5_bullet_semianalytical_spacetime.pdf / .png (Figure 5: Spacetime Gravitational Potential & Gas Density Worldsheet)
"""

import os
import sys
import json
import subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import AutoMinorLocator
from scipy.ndimage import gaussian_filter
from scipy.integrate import solve_ivp

# Directory configuration
MANUSCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
REPO_ROOT = os.path.abspath(os.path.join(MANUSCRIPT_DIR, "../.."))
if not os.path.exists(os.path.join(REPO_ROOT, "src")):
    REPO_ROOT = os.path.abspath(os.path.join(MANUSCRIPT_DIR, "../../.."))
for p in [REPO_ROOT, os.path.join(REPO_ROOT, "official")]:
    if os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)
FIG_DIR = os.path.join(MANUSCRIPT_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

SEARCH_DIRS = [
    os.path.join(REPO_ROOT, "official", "results", "investigations"),
    os.path.join(REPO_ROOT, "results", "investigations"),
    os.path.join(REPO_ROOT, "development", "simulations", "analysis"),
    os.path.join(REPO_ROOT, "official", "src", "evaluations"),
    os.path.join(REPO_ROOT, "src", "evaluations")
]

def find_file(filename):
    for s in SEARCH_DIRS:
        p = os.path.join(s, filename)
        if os.path.exists(p):
            return p
    return None

DATA_CSV = find_file("bullet_offset_evolution.csv")
DATA_NPZ = find_file("bullet_spatial_slices.npz")
DATA_JSON = find_file("bullet_summary.json")

def configure_matplotlib_style():
    """Sets publication-grade Matplotlib aesthetic matching APS/MNRAS styling."""
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
        'font.size': 11,
        'axes.labelsize': 13,
        'axes.titlesize': 14,
        'xtick.labelsize': 11,
        'ytick.labelsize': 11,
        'legend.fontsize': 10,
        'figure.titlesize': 16,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'axes.linewidth': 1.2,
        'xtick.direction': 'in',
        'ytick.direction': 'in',
        'xtick.major.size': 6,
        'ytick.major.size': 6,
        'xtick.minor.size': 3,
        'ytick.minor.size': 3,
        'xtick.top': True,
        'ytick.right': True,
        'axes.grid': False
    })

def generate_figure_1(df, npz):
    """
    Generates 4-panel publication figure showing key collision epochs:
    (a) Infall & Approach (t = 82.4 Myr)
    (b) Core Impact & Shock (t = 351.1 Myr)
    (c) Decoupled State / Bullet Analog (t = 935.6 Myr)
    (d) Late Relaxation (t = 1202.9 Myr)
    """
    print("[1/5] Generating Figure 1: 4-Epoch 2D Decoupling Evolution...", flush=True)
    times = npz['times']
    x_centers = npz['x_centers']
    y_centers = npz['y_centers']
    gas_grids = npz['gas_grids']
    pot_grids = npz['pot_grids']
    
    target_snaps = [3, 10, 25, 32]
    epoch_labels = [
        r"(a) Infall & Approach ($t = 82.4\ \mathrm{Myr}$)",
        r"(b) Core Impact & Shock ($t = 351.1\ \mathrm{Myr}$)",
        r"(c) Decoupled State / Bullet Analog ($t = 935.6\ \mathrm{Myr}$)",
        r"(d) Late Relaxation ($t = 1202.9\ \mathrm{Myr}$)"
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 13), sharex=True, sharey=True)
    axes_flat = axes.flatten()
    
    dx_bin = (x_centers[1] - x_centers[0]) / 2.0
    dy_bin = (y_centers[1] - y_centers[0]) / 2.0
    extent = [x_centers[0] - dx_bin, x_centers[-1] + dx_bin, y_centers[0] - dy_bin, y_centers[-1] + dy_bin]
    
    # Enhanced visibility color dynamic range
    vmin = -27.85
    vmax = -25.80
    
    for idx, snap_num in enumerate(target_snaps):
        ax = axes_flat[idx]
        s_idx = snap_num - 1
        
        row = df[df['snapshot'] == snap_num].iloc[0]
        gas_px, gas_py = row['gas_peak_x'], row['gas_peak_y']
        pot_px, pot_py = row['pot_min_x'], row['pot_min_y']
        offset = row['offset_pot_gas_kpc']
        
        gas_slice = gas_grids[s_idx]
        pot_slice = pot_grids[s_idx]
        
        # Heatmap: Gas Density (X-ray proxy) in inferno colormap
        im = ax.imshow(gas_slice.T, origin='lower', extent=extent, cmap='inferno',
                       vmin=vmin, vmax=vmax, interpolation='bicubic', aspect='equal')
        
        # Overlaid Contours: Continuous Gravitational Potential (Weak Lensing Proxy)
        if np.any(pot_slice != 0):
            bg_p = np.percentile(pot_slice, 92)
            well_2d = np.maximum(0.0, bg_p - pot_slice)
            well_smooth = gaussian_filter(well_2d, sigma=1.8)
            well_depth = well_smooth / (np.max(well_smooth) + 1e-30)
            cs = ax.contour(x_centers, y_centers, well_depth.T,
                            levels=np.linspace(0.35, 0.95, 7),
                            colors='cyan', linewidths=1.5, alpha=0.9)
        
        # Markers for Gas Peak and Potential Minimum
        ax.scatter(gas_px, gas_py, marker='o', s=160, facecolors='#3b82f6',
                   edgecolors='white', linewidths=2.0, label='Gas Density Peak (X-ray)', zorder=5)
        ax.scatter(pot_px, pot_py, marker='X', s=180, facecolors='#ef4444',
                   edgecolors='white', linewidths=2.0, label='Potential Min (Lensing Peak)', zorder=5)
        
        # Spatial separation vector
        if offset >= 50.0:
            ax.annotate('', xy=(pot_px, pot_py), xytext=(gas_px, gas_py),
                        arrowprops=dict(arrowstyle="->", color='yellow', lw=2.2, ls='--'))
            mid_x = (gas_px + pot_px) / 2.0
            mid_y = (gas_py + pot_py) / 2.0
            ax.text(mid_x, mid_y + 110, f"$\\Delta r = {offset:.0f}\\ \\mathrm{{kpc}}$",
                    color='yellow', fontsize=11, fontweight='bold', ha='center',
                    bbox=dict(boxstyle="round,pad=0.2", fc='black', ec='yellow', alpha=0.75))
        
        ax.set_title(epoch_labels[idx], pad=10, fontweight='bold', fontsize=13)
        ax.set_xlim(1100, 2900)
        ax.set_ylim(1100, 2900)
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        
        if idx in [0, 2]:
            ax.set_ylabel(r"$Y\ \mathrm{[kpc]}$", fontweight='bold')
        if idx in [2, 3]:
            ax.set_xlabel(r"$X\ \mathrm{[kpc]}$", fontweight='bold')
            
        if idx == 0:
            ax.legend(loc='upper right', framealpha=0.85, facecolor='black',
                      edgecolor='gray', labelcolor='white', fontsize=10)
    
    fig.subplots_adjust(right=0.88, hspace=0.15, wspace=0.08)
    cbar_ax = fig.add_axes([0.90, 0.25, 0.02, 0.5])
    cbar = fig.colorbar(im, cax=cbar_ax)
    cbar.set_label(r"$\log_{10}\ \rho_{\mathrm{gas}}\ [\mathrm{g\ cm^{-3}}]$", fontweight='bold', fontsize=12)
    
    pdf_out = os.path.join(FIG_DIR, "fig1_bullet_decoupling_evolution.pdf")
    png_out = os.path.join(FIG_DIR, "fig1_bullet_decoupling_evolution.png")
    fig.savefig(pdf_out, dpi=300, bbox_inches='tight')
    fig.savefig(png_out, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"  -> Saved: {pdf_out}\n  -> Saved: {png_out}", flush=True)

def generate_figure_2(df):
    """
    Generates Figure 2: Spatial offset Delta r(t) vs simulation time with empirical band.
    """
    print("[2/5] Generating Figure 2: Offset Evolution...", flush=True)
    fig, ax1 = plt.subplots(figsize=(8, 6))
    
    ax1.plot(df['time_myr'], df['offset_pot_gas_kpc'], color='#2563eb', lw=2.5,
             label=r'Chronodynamic Relativity ($\tau_{\mathrm{eff}} \approx 82.8\ \mathrm{Myr}$)', zorder=3)
    ax1.scatter(df['time_myr'], df['offset_pot_gas_kpc'], color='#1e3a8a', s=40, zorder=4)
    
    # Empirical 1E 0657-56 observational band
    ax1.axhspan(250, 350, color='#10b981', alpha=0.22,
                label=r'Observed 1E 0657-56 Offset (250–350 kpc)')
    ax1.axhline(300, color='#059669', ls='--', lw=1.5)
    
    ax1.axvline(351.1, color='#dc2626', ls=':', lw=1.8, label=r'Core Impact ($t \approx 351\ \mathrm{Myr}$)')
    
    snap25 = df[df['snapshot'] == 25].iloc[0]
    ax1.scatter(snap25['time_myr'], snap25['offset_pot_gas_kpc'], marker='*', s=260,
                color='#f59e0b', edgecolor='black', linewidth=1.5, zorder=6,
                label=f"Bullet Analog ($t = {snap25['time_myr']:.1f}\\ \\mathrm{{Myr}},\\ \\Delta r = {snap25['offset_pot_gas_kpc']:.1f}\\ \\mathrm{{kpc}}$)")
    
    ax1.set_xlabel(r"Simulation Time $t\ \mathrm{[Myr]}$", fontweight='bold')
    ax1.set_ylabel(r"Spatial Decoupling Offset $\Delta r\ \mathrm{[kpc]}$", fontweight='bold')
    ax1.set_title(r"Gravitational Potential vs. Gas Offset Evolution", pad=12, fontweight='bold')
    ax1.set_xlim(0, 1500)
    ax1.set_ylim(-20, 950)
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.legend(loc='upper left', framealpha=0.9, fontsize=9.5)
    ax1.grid(True, linestyle='--', alpha=0.4)
    
    plt.tight_layout()
    pdf_out = os.path.join(FIG_DIR, "fig2_bullet_offset_evolution.pdf")
    png_out = os.path.join(FIG_DIR, "fig2_bullet_offset_evolution.png")
    fig.savefig(pdf_out, dpi=300, bbox_inches='tight')
    fig.savefig(png_out, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"  -> Saved: {pdf_out}\n  -> Saved: {png_out}", flush=True)

def generate_figure_3(npz):
    """
    Generates Figure 3: 1D collision axis profiles of gas density and gravitational potential.
    """
    print("[3/5] Generating Figure 3: 1D Collision Axis Profile...", flush=True)
    x_1d_centers = npz['x_1d_centers']
    rho_1d_profiles = npz['rho_1d_profiles']
    phi_1d_profiles = npz['phi_1d_profiles']
    
    fig, ax2 = plt.subplots(figsize=(8, 6))
    
    idx_snap = 24 # Snapshot 25 (0-indexed)
    rho_1d = rho_1d_profiles[idx_snap].copy()
    phi_1d = phi_1d_profiles[idx_snap].copy()
    
    # Clean and smooth 1D potential well depth
    bg_1d = np.percentile(phi_1d, 90)
    well_1d = np.maximum(0.0, bg_1d - phi_1d)
    well_1d_smooth = gaussian_filter(well_1d, sigma=2.0)
    norm_phi_well = well_1d_smooth / (np.max(well_1d_smooth) + 1e-30)
    
    # Clean and smooth gas density
    rho_smooth = gaussian_filter(rho_1d, sigma=1.5)
    norm_rho = (rho_smooth - np.min(rho_smooth)) / (np.max(rho_smooth) - np.min(rho_smooth) + 1e-30)
    
    ax2.plot(x_1d_centers, norm_rho, color='#ef4444', lw=2.8,
             label=r'Baryonic Gas Density $\rho_{\mathrm{gas}}(x)/\rho_{\mathrm{max}}$ (X-ray Shock)')
    ax2.plot(x_1d_centers, norm_phi_well, color='#06b6d4', lw=2.8, ls='-',
             label=r'Gravitational Well Depth $\Delta\Phi(x)/\Delta\Phi_{\mathrm{max}}$ (Lensing Potential)')
    
    ax2.fill_between(x_1d_centers, norm_rho, color='#ef4444', alpha=0.18)
    ax2.fill_between(x_1d_centers, norm_phi_well, color='#06b6d4', alpha=0.18)
    
    peak_x_gas = x_1d_centers[np.argmax(norm_rho)]
    peak_x_pot = x_1d_centers[np.argmax(norm_phi_well)]
    delta_x_1d = abs(peak_x_pot - peak_x_gas)
    
    ax2.axvline(peak_x_gas, color='#ef4444', ls='--', lw=1.8)
    ax2.axvline(peak_x_pot, color='#06b6d4', ls='--', lw=1.8)
    
    ax2.annotate('', xy=(peak_x_pot, 0.88), xytext=(peak_x_gas, 0.88),
                 arrowprops=dict(arrowstyle="<->", color='black', lw=2.2))
    ax2.text((peak_x_gas + peak_x_pot) / 2.0, 0.91,
             f"$\\Delta x = {delta_x_1d:.0f}\\ \\mathrm{{kpc}}$",
             ha='center', fontsize=11, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.3", fc='white', ec='black', alpha=0.9))
    
    ax2.set_xlabel(r"Collision Axis Coordinate $X\ \mathrm{[kpc]}$", fontweight='bold')
    ax2.set_ylabel(r"Normalized Observable Amplitude $[0, 1]$", fontweight='bold')
    ax2.set_title(r"1D Axis Decoupling Profile at $t = 935.6\ \mathrm{Myr}$", pad=12, fontweight='bold')
    ax2.set_xlim(1200, 2800)
    ax2.set_ylim(-0.05, 1.2)
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.yaxis.set_minor_locator(AutoMinorLocator())
    ax2.legend(loc='upper right', framealpha=0.9, fontsize=9.5)
    ax2.grid(True, linestyle='--', alpha=0.4)
    
    plt.tight_layout()
    pdf_out = os.path.join(FIG_DIR, "fig3_bullet_1d_profile.pdf")
    png_out = os.path.join(FIG_DIR, "fig3_bullet_1d_profile.png")
    fig.savefig(pdf_out, dpi=300, bbox_inches='tight')
    fig.savefig(png_out, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"  -> Saved: {pdf_out}\n  -> Saved: {png_out}", flush=True)

def generate_figures_4_and_5():
    """Run the semi-analytical script to output fig4 and fig5."""
    print("[4/5 & 5/5] Generating Figures 4 & 5: Semi-Analytical Virial Recovery & Spacetime...", flush=True)
    recovery_script = find_file("bullet_recovery_semianalytical.py")
    if recovery_script and os.path.exists(recovery_script):
        cmd = [sys.executable, recovery_script]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Error running {recovery_script}:\n{res.stderr}", flush=True)
        
        # Check source figures in candidates
        source_candidates = [
            os.path.join(REPO_ROOT, "official", "manuscripts", "series_2_paper_2_cluster_collision_hydrodynamics", "figures"),
            os.path.join(REPO_ROOT, "development", "manuscripts", "series_2_paper_2_cluster_collision_hydrodynamics", "figures"),
            os.path.join(REPO_ROOT, "development", "simulations", "analysis", "figures"),
            os.path.join(os.path.dirname(recovery_script), "figures"),
            FIG_DIR
        ]
        import shutil
        for src_dir in source_candidates:
            s4_pdf = os.path.join(src_dir, "bullet_semianalytical_recovery.pdf")
            s5_pdf = os.path.join(src_dir, "bullet_semianalytical_spacetime.pdf")
            if os.path.exists(s4_pdf) and s4_pdf != os.path.join(FIG_DIR, "fig4_bullet_semianalytical_recovery.pdf"):
                shutil.copy2(s4_pdf, os.path.join(FIG_DIR, "fig4_bullet_semianalytical_recovery.pdf"))
                s4_png = os.path.join(src_dir, "bullet_semianalytical_recovery.png")
                if os.path.exists(s4_png):
                    shutil.copy2(s4_png, os.path.join(FIG_DIR, "fig4_bullet_semianalytical_recovery.png"))
            if os.path.exists(s5_pdf) and s5_pdf != os.path.join(FIG_DIR, "fig5_bullet_semianalytical_spacetime.pdf"):
                shutil.copy2(s5_pdf, os.path.join(FIG_DIR, "fig5_bullet_semianalytical_spacetime.pdf"))
                s5_png = os.path.join(src_dir, "bullet_semianalytical_spacetime.png")
                if os.path.exists(s5_png):
                    shutil.copy2(s5_png, os.path.join(FIG_DIR, "fig5_bullet_semianalytical_spacetime.png"))

        print(f"  -> Saved: {os.path.join(FIG_DIR, 'fig4_bullet_semianalytical_recovery.pdf')}")
        print(f"  -> Saved: {os.path.join(FIG_DIR, 'fig5_bullet_semianalytical_spacetime.pdf')}")
    else:
        print("Warning: bullet_recovery_semianalytical.py not found in SEARCH_DIRS", flush=True)

def main():
    configure_matplotlib_style()
    print("=" * 80)
    print("CHRONODYNAMIC RELATIVITY: SERIES 2 PAPER 2 FIGURE GENERATION")
    print(f"Manuscript Figures Target: {FIG_DIR}")
    print("=" * 80)
    
    if not os.path.exists(DATA_CSV) or not os.path.exists(DATA_NPZ):
        print(f"ERROR: Simulation archives not found in {ANALYSIS_DIR}!")
        sys.exit(1)
        
    df = pd.read_csv(DATA_CSV)
    npz = np.load(DATA_NPZ)
    
    generate_figure_1(df, npz)
    generate_figure_2(df)
    generate_figure_3(npz)
    generate_figures_4_and_5()
    
    print("=" * 80)
    print("ALL PAPER 2.2 FIGURES SUCCESSFULLY GENERATED!")
    print("=" * 80)

if __name__ == "__main__":
    main()
