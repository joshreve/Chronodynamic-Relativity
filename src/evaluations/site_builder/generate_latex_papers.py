import os
import sys
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import quad
import time
# Project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from src.evaluations.site_builder.data_provider import DataProvider
from src.evaluations.site_builder.plot_factory import PlotFactory

def generate_latex_papers():
    print("Generating Academic LaTeX Papers...")
    output_dir = "docs/papers"
    fig_dir = os.path.join(output_dir, "figures")
    os.makedirs(fig_dir, exist_ok=True)
    
    provider = DataProvider()
    
    # -------------------------------------------------------------
    # 1. EXPORT IMAGES (PDF FORMAT FOR LATEX COMPILATION)
    # -------------------------------------------------------------
    print("  * Exporting figures to PDF...")
    
    # Figure 1: Timeline
    h0_lcdm = 67.4
    h0_cr = 70.5
    omega_m = 0.315
    omega_l = 0.685
    omega_r = 9.2e-5
    z_eq = 3500.0
    n = 0.2385
    z_obs_target = 14.32
    
    h0_s_lcdm = h0_lcdm * (1000.0 / 3.08567758e22)
    h0_s_cr = h0_cr * (1000.0 / 3.08567758e22)
    
    def integrand_age_lcdm_a(a):
        return a / np.sqrt(omega_r + omega_m * a + omega_l * a**4)
        
    def get_age_lcdm(z):
        a = 1.0 / (1.0 + z)
        val, _ = quad(integrand_age_lcdm_a, 0.0, a)
        return (val / h0_s_lcdm) / (3.15576e16)
        
    def get_cr_params(z):
        omega_b = 0.049
        omega_r = 9.2e-5
        omega_s = 1.0 - omega_b
        beta_r = 2.0 * omega_r / omega_b
        beta_v = -2.0 * omega_s / omega_b
        val_inside = 1.0 + beta_r * (1.0 + z) + beta_v * (1.0 + z)**-3
        n_eff = n * np.sqrt(np.maximum(val_inside, 1e-5))
        z_exp = (1.0 + z)**(1.0 / (1.0 + n_eff/2.0)) - 1.0
        t_ratio = (1.0 + z_exp)**(n_eff / 2.0)
        t_phys_today = 1.0 / h0_s_cr / 3.15576e16
        t_phys = t_phys_today / (1.0 + z_exp)
        t_local = (t_phys_today / (1.0 - n_eff/2.0)) * (1.0 + z_exp)**(n_eff/2.0 - 1.0)
        return z_exp, t_ratio, t_phys, t_local

    t_lcdm_z14 = get_age_lcdm(z_obs_target)
    z_exp_z14, t_ratio_z14, t_phys_z14, t_local_z14 = get_cr_params(z_obs_target)
    
    dl_lcdm = (1 + z_obs_target) * quad(lambda z: 299792.458 / (h0_lcdm * np.sqrt(omega_r*(1+z)**4 + omega_m*(1+z)**3 + omega_l)), 0.0, z_obs_target)[0]
    da_lcdm = dl_lcdm / (1 + z_obs_target)**2
    
    r_com_cr = (299792.458 / h0_cr) * np.log(1.0 + z_exp_z14)
    dl_cr_raw = (1 + z_obs_target) * r_com_cr
    da_cr = r_com_cr / (1 + z_obs_target)
    
    mu_lcdm = 5.0 * np.log10(dl_lcdm) + 25.0
    mu_cr_eff = 5.0 * np.log10(dl_cr_raw) + 25.0 - 2.5 * np.log10(t_ratio_z14)
    flux_ratio = 10**((mu_lcdm - mu_cr_eff) / 2.5)

    zs = np.linspace(0.0, 20.0, 200)
    ages_lcdm = [get_age_lcdm(z) * 1000.0 for z in zs]
    ages_cr_phys = []
    ages_cr_local = []
    for z in zs:
        _, _, tp, tl = get_cr_params(z)
        ages_cr_phys.append(tp * 1000.0)
        ages_cr_local.append(tl * 1000.0)
        
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=zs, y=ages_lcdm, name='LambdaCDM Age', line=dict(color='#e74c3c', width=2)))
    fig1.add_trace(go.Scatter(x=zs, y=ages_cr_phys, name='Chronodynamic Relativity Physical Age', line=dict(color='#3498db', width=2, dash='dash')))
    fig1.add_trace(go.Scatter(x=zs, y=ages_cr_local, name='Chronodynamic Relativity Local Experienced Time', line=dict(color='#9b59b6', width=3)))
    
    fig1.add_trace(go.Scatter(
        x=[z_obs_target, z_obs_target, z_obs_target],
        y=[t_lcdm_z14*1000.0, t_phys_z14*1000.0, t_local_z14*1000.0],
        mode='markers+text',
        name='JADES-GS-z14-0 Epoch',
        marker=dict(color='black', size=8, symbol='diamond'),
        text=[f"LCDM: {t_lcdm_z14*1000.0:.0f} Myr", f"CR Phys: {t_phys_z14*1000.0:.0f} Myr", f"CR Local: {t_local_z14*1000.0:.0f} Myr"],
        textposition=["bottom right", "bottom right", "top right"]
    ))
    
    fig1.update_layout(
        xaxis_title="Observed Redshift (z)",
        yaxis_title="Time Since Big Bang (Myr)",
        template="plotly_white",
        legend=dict(x=0.55, y=0.9),
        yaxis_type="log",
        margin=dict(l=40, r=40, t=20, b=40)
    )
    
    try:
        fig1.write_image(os.path.join(fig_dir, "paper1_timeline.pdf"))
    except Exception as e:
        print(f"Warning: Failed to write paper1_timeline.pdf: {e}. Writing placeholder.")
        with open(os.path.join(fig_dir, "paper1_timeline.pdf"), "w") as f:
            f.write("% PDF Placeholder")
            
    # Figure 2: Hubble Diagram
    data_expansion = provider.get_cosmic_expansion_data()
    fig2 = PlotFactory.create_hubble_diagram(data_expansion)
    fig2.update_layout(margin=dict(l=40, r=40, t=20, b=40))
    try:
        fig2.write_image(os.path.join(fig_dir, "paper2_hubble_diagram.pdf"))
    except Exception as e:
        print(f"Warning: Failed to write paper2_hubble_diagram.pdf: {e}. Writing placeholder.")
        with open(os.path.join(fig_dir, "paper2_hubble_diagram.pdf"), "w") as f:
            f.write("% PDF Placeholder")
            

    # -------------------------------------------------------------
    # 2. READ LATEX TEMPLATES AND BUILD PAPERS (DYNAMIC PLACEMENT)
    # -------------------------------------------------------------
    print("  * Generating LaTeX files from templates...")
    
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "templates"))
    
    # Paper 1 LaTeX (ApJL Style using AASTeX 7.0.1)
    paper1_template_path = os.path.join(template_dir, "paper1_jades_z14.template.tex")
    with open(paper1_template_path, "r", encoding="utf-8") as f:
        paper1_template = f.read()
        
    paper1_tex = paper1_template\
        .replace("__z_exp_z14__", f"{z_exp_z14:.2f}")\
        .replace("__t_lcdm_z14_myf__", f"{t_lcdm_z14*1000.0:.1f}")\
        .replace("__t_phys_z14_myf__", f"{t_phys_z14*1000.0:.1f}")\
        .replace("__t_phys_ratio__", f"{t_phys_z14/t_lcdm_z14:.2f}")\
        .replace("__t_local_z14_myf__", f"{t_local_z14*1000.0:.1f}")\
        .replace("__t_local_ratio__", f"{t_local_z14/t_lcdm_z14:.2f}")\
        .replace("__t_local_z14_gyr__", f"{t_local_z14:.2f}")\
        .replace("__da_lcdm__", f"{da_lcdm:.1f}")\
        .replace("__da_cr__", f"{da_cr:.1f}")\
        .replace("__t_ratio_z14__", f"{t_ratio_z14:.4f}")\
        .replace("__t_ratio_z14_2f__", f"{t_ratio_z14:.2f}")

    with open(os.path.join(output_dir, "paper1_jades_z14.tex"), "w", encoding='utf-8') as f:
        f.write(paper1_tex)
        
    # Paper 2 LaTeX (PRD Style using RevTeX 4.2)
    paper2_template_path = os.path.join(template_dir, "paper2_pantheon_fit.template.tex")
    with open(paper2_template_path, "r", encoding="utf-8") as f:
        paper2_tex = f.read()

    with open(os.path.join(output_dir, "paper2_pantheon_fit.tex"), "w", encoding='utf-8') as f:
        f.write(paper2_tex)
        
    print("Academic LaTeX papers and figures generated successfully.")


def clean_temporary_files():
    print("Cleaning up LaTeX temporary files...")
    output_dir = "docs/papers"
    temp_extensions = [
        ".aux", ".log", ".fls", ".fdb_latexmk", ".synctex.gz",
        ".out", ".blg", ".bbl", "Notes.bib", ".toc", ".nav", ".snm"
    ]
    if not os.path.exists(output_dir):
        return
    cleaned_count = 0
    for filename in os.listdir(output_dir):
        filepath = os.path.join(output_dir, filename)
        if os.path.isfile(filepath):
            for ext in temp_extensions:
                if filename.endswith(ext):
                    try:
                        os.remove(filepath)
                        cleaned_count += 1
                    except Exception as e:
                        print(f"Error removing {filename}: {e}")
                    break
    print(f"Removed {cleaned_count} temporary files.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true", help="Clean temporary LaTeX files")
    args = parser.parse_args()
    
    if args.clean:
        clean_temporary_files()
    else:
        generate_latex_papers()
        time.sleep(1)
        clean_temporary_files()

