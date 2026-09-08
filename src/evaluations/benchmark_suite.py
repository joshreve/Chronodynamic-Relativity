import os
import sys

# Ensure repository root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import numpy as np
import pandas as pd
from src.models.base import PhysicsError

class BenchmarkSuite:
    """
    Automated evaluation pipeline for benchmarking physical models against observational data.
    """
    def __init__(self):
        self.results = {}

    def chi_squared(self, observed, predicted, errors):
        """
        Compute the reduced Chi-Squared statistic.
        """
        observed = np.array(observed)
        predicted = np.array(predicted)
        errors = np.array(errors)
        
        # Apply error floor to prevent division by zero or non-physical errors
        errors = np.maximum(errors, 1e-5)
            
        chi2 = np.sum(((observed - predicted) / errors)**2)
        dof = len(observed)
        
        return chi2 / dof if dof > 0 else 0.0

    def bic(self, chi2, num_params, num_data_points):
        """
        Compute the Bayesian Information Criterion (BIC).
        """
        if num_data_points <= 0:
            return np.inf
        return chi2 + num_params * np.log(num_data_points)

    def distance_modulus(self, dl_mpc):
        """
        Compute distance modulus mu from luminosity distance in Mpc.
        """
        dl_mpc = np.atleast_1d(dl_mpc)
        dl_safe = np.where(dl_mpc <= 0, 1e-10, dl_mpc)
        return 5 * np.log10(dl_safe) + 25

    def evaluate_supernova(self, model, sn_data):
        """
        Evaluate a cosmology model against Type Ia Supernova data.
        """
        z = sn_data['z'].values
        mu_obs = sn_data['mu_obs'].values
        mu_err = sn_data['mu_err'].values
        
        if hasattr(model, 'compute_mu'):
            mu_pred = model.compute_mu(z)
        else:
            dl_pred = model.luminosity_distance(z)
            mu_pred = self.distance_modulus(dl_pred)
        
        red_chi2 = self.chi_squared(mu_obs, mu_pred, mu_err)
        
        return {
            'red_chi2': red_chi2,
            'mu_pred': mu_pred,
            'mu_obs': mu_obs,
            'mu_err': mu_err,
            'z': z
        }

    def simulate_merger_offset(self, v0_kpc_myr, mass_1e14=20.0, n_val=None):
        """
        Simulates the spatial decoupling of the metric potential (field) from collisional gas
        using the zero-parameter Geometric Vacuum Lag (Temporal Viscosity).
        """
        dt = 0.5 # Myr
        t_max = 200.0 # Myr
        times = np.arange(0, t_max, dt)

        # 1. Base relaxation time tau_0 = sqrt(2) / (H0 * n)
        from src.models import LatestChronodynamicModel
        from src.utils.constants import G
        cr_model = LatestChronodynamicModel()
        n_val = cr_model.n if n_val is None else n_val
        a0 = cr_model.a0
        
        # Characteristic cluster relaxation timescale
        h0_inv_myr = (1.0 / cr_model.h0) * 977.8
        tau_0 = np.sqrt(2.0) * h0_inv_myr / n_val
        k_val = n_val / np.sqrt(2.0)

        # 2. Local Gravity Proxy
        # M in 1e14 M_sun, R ~ 1350 kpc (Merger environment boundary)
        m_kg = mass_1e14 * 1e14 * 1.989e30
        r_m = 1350.0 * 3.086e19 # typical interaction radius for ensemble
        g_N = (G * m_kg) / (r_m**2) if mass_1e14 > 0 else 0.0

        # The field's relaxation time dictates how quickly the metric clock can adapt
        # to sudden changes in the mass distribution (like the gas stopping).
        tau_local = tau_0 * np.exp(-k_val * (g_N / a0))

        # Kinematics
        # The gas experiences extreme ram pressure and stops over tau_drag
        tau_drag = 15.0 # Myr
        x_gas = np.zeros_like(times)
        v_gas = np.zeros_like(times)
        v_gas[0] = v0_kpc_myr

        # The field potential is tied to the metric clock.
        # It tries to follow the gas (target), but is lagged by tau_local.
        x_field = np.zeros_like(times)
        v_field = np.zeros_like(times)
        v_field[0] = v0_kpc_myr

        for i in range(1, len(times)):
            # Gas deceleration (ram pressure)
            a_gas = -v_gas[i-1] / tau_drag
            v_gas[i] = v_gas[i-1] + a_gas * dt
            x_gas[i] = x_gas[i-1] + v_gas[i] * dt

            # The target velocity for the potential is where the gas is pulling it
            target_v = v_gas[i]

            # Stateful relaxation: \dot{v}_{actual} = (v_{target} - v_{actual}) / tau
            a_field = (target_v - v_field[i-1]) / tau_local
            v_field[i] = v_field[i-1] + a_field * dt
            x_field[i] = x_field[i-1] + v_field[i] * dt

        # Standard observation point for post-merger clusters is ~150 Myr
        obs_idx = int(150.0 / dt)
        if obs_idx >= len(times): obs_idx = -1

        offset = x_field[obs_idx] - x_gas[obs_idx]
        return offset

    def evaluate_cluster_mergers(self, model, merger_data):
        """
        Evaluate non-linear viscosity model against a dataset of cluster/galactic mergers.
        Uses first-principles stateful geometric relaxation timescale tau.
        """
        n_val = model.parameters.get('n', 0.2385) if hasattr(model, 'parameters') else 0.2385

        v_obs_km_s = merger_data['v_km_s'].values
        offset_obs = merger_data['offset_obs'].values
        offset_err = merger_data['err'].values
        
        # Density-dependence: Local Field Density (Mass in 10^14 M_sun)
        masses = merger_data.get('mass_1e14', np.ones_like(v_obs_km_s) * 20.0).values
        
        v_kpc_myr = v_obs_km_s / 977.8
        
        offset_pred = []
        for v, mass in zip(v_kpc_myr, masses):
            offset_pred.append(self.simulate_merger_offset(v, mass, n_val=n_val))
        
        red_chi2 = self.chi_squared(offset_obs, offset_pred, offset_err)
        
        return {
            'red_chi2': red_chi2,
            'offset_pred': offset_pred,
            'offset_obs': offset_obs,
            'err': offset_err,
            'v_km_s': v_obs_km_s
        }

    def evaluate_strong_lensing(self, model, slacs_data=None):
        """
        Evaluate a gravity model against the SLACS strong lensing dataset.
        Performs a rigorous 3D line-of-sight integration of the deflection angle.
        """
        from scipy.integrate import quad
        from scipy.optimize import minimize

        if slacs_data is None:
            slacs_data = [
                {"name": "J0037", "z_l": 0.1954, "z_s": 0.6322, "obs": 1.47, "m_star": 2.14e11, "sigma": 279},
                {"name": "J0216", "z_l": 0.332,  "z_s": 0.521,  "obs": 1.15, "m_star": 1.70e11, "sigma": 332},
                {"name": "J0737", "z_l": 0.322,  "z_s": 0.581,  "obs": 1.03, "m_star": 1.50e11, "sigma": 310},
                {"name": "J0912", "z_l": 0.1642, "z_s": 0.3239, "obs": 1.63, "m_star": 2.51e11, "sigma": 313},
                {"name": "J0946", "z_l": 0.2220, "z_s": 0.6090, "obs": 1.43, "m_star": 2.19e11, "sigma": 284},
                {"name": "J0956", "z_l": 0.240,  "z_s": 0.470,  "obs": 1.32, "m_star": 2.05e11, "sigma": 298},
                {"name": "J1205", "z_l": 0.2150, "z_s": 0.4808, "obs": 1.24, "m_star": 1.78e11, "sigma": 235},
                {"name": "J1627", "z_l": 0.2076, "z_s": 0.5241, "obs": 1.21, "m_star": 1.91e11, "sigma": 275},
                {"name": "J2300", "z_l": 0.228,  "z_s": 0.463,  "obs": 1.24, "m_star": 1.85e11, "sigma": 279}
            ]

        c = 299792458.0
        pc_to_m = 3.086e16

        # Use v8 dilution power for distances
        n_val = model.parameters.get('n', 0.2385) if hasattr(model, 'parameters') else 0.2385

        results = []
        for lens in slacs_data:
            m_kg = lens['m_star'] * 1.989e30
            z_l, z_s = lens['z_l'], lens['z_s']

            # 1. Cosmological Distances
            # model must support angular_diameter_distance
            d_l = model.angular_diameter_distance(z_l) * 1e6 * pc_to_m
            d_s = model.angular_diameter_distance(z_s) * 1e6 * pc_to_m
            d_ls = model.angular_diameter_distance(z_s, z_start=z_l) * 1e6 * pc_to_m

            # 2. Temporal Mass Correction
            z_exp_l = model.get_z_exp(z_l, n_val)
            t_ratio = (1 + z_exp_l)**(n_val/2.0)
            m_true = m_kg / t_ratio

            # Jaffe Profile: M(r) = M_total * r / (r + r_s)
            r_scale = 5.0 * pc_to_m * 1000.0 # 5 kpc

            def get_enclosed_mass(r): return m_true * (r / (r + r_scale))

            def objective(theta_arcsec):
                theta_val = float(theta_arcsec[0]) if hasattr(theta_arcsec, '__len__') else float(theta_arcsec)
                r_rad = (theta_val / 3600.0) * (np.pi / 180.0)
                b = r_rad * d_l

                def integrand(z_val):
                    r = np.sqrt(b**2 + z_val**2)
                    m_enc = get_enclosed_mass(r)
                    res_g = model.compute_acceleration(r, m_enc, z=z_l)
                    g = float(np.atleast_1d(res_g[0])[0])
                    # Relativistic Doubling Factor (Isotropic Metric)
                    return g * (b / r) * 2.0

                integral, _ = quad(integrand, 0, 1000 * b, limit=50)
                alpha_def = (4.0 / (c**2)) * integral
                return abs(theta_val - alpha_def * (d_ls / d_s) * 206265.0)

            res = minimize(objective, [1.0], method='Nelder-Mead', tol=1e-3)
            theta_pred = res.x[0]

            # SIS Reference
            sigma_m_s = lens['sigma'] * 1000.0
            theta_sis = 4.0 * np.pi * (sigma_m_s**2 / c**2) * (d_ls / d_s) * 206265.0

            results.append({
                'name': lens['name'],
                'obs': lens['obs'],
                'pred': theta_pred,
                'sis': theta_sis
            })

        df = pd.DataFrame(results)
        red_chi2 = self.chi_squared(df['obs'], df['pred'], [0.1]*len(df)) # 0.1 arcsec error estimate

        return {
            'red_chi2': red_chi2,
            'data': df,
            'names': df['name'].tolist(),
            'obs': df['obs'].tolist(),
            'v8': df['pred'].tolist(),
            'sis': df['sis'].tolist()
        }

    def evaluate_rotation_curve(self, model, galaxy_data, z=0, optimize_ups=True):
        """
        [Legacy 1D Model]
        Evaluate a gravity model against a SPARC galaxy rotation curve using 1D thin-disk logic.
        """
        from scipy.optimize import minimize_scalar
        from src.utils.constants import G
        
        r = galaxy_data['r'].values
        v_obs = galaxy_data['v_obs'].values
        v_err = galaxy_data['v_err'].values
        
        n = model.parameters.get('n', 0.0) if hasattr(model, 'parameters') else 0.0
        z_exp = (1 + z)**(1.0 / (1.0 + n/2.0)) - 1.0 if z > 0 else 0.0
        t_ratio = (1 + z_exp)**(n/2.0)
        
        kpc_to_m = 3.086e19; km_s_to_m_s = 1000.0
        r_m = r * kpc_to_m
        
        def compute_v_pred(ups_base):
            Ups_d = ups_base / t_ratio
            Ups_b = (ups_base * 1.4) / t_ratio
            
            v_b_sq = (np.sign(galaxy_data['v_gas']) * galaxy_data['v_gas']**2 + 
                      Ups_d * galaxy_data['v_disk']**2 + 
                      Ups_b * galaxy_data['v_bulge']**2)
            v_baryon = np.sqrt(np.maximum(v_b_sq, 1e-10))
            
            v_b_m_s = v_baryon * km_s_to_m_s
            m_baryon = (v_b_m_s**2 * r_m) / G
            
            h_local = np.zeros_like(r)
            try:
                res = model.compute_acceleration(r_m, m_baryon, z=z)
                g_pred_m_s2, h_local = res if isinstance(res, tuple) else (res, np.zeros_like(r))
            except (TypeError, ValueError):
                g_pred_m_s2 = model.compute_acceleration(r_m, m_baryon)
                
            v_orbital_m_s = np.sqrt(np.maximum(g_pred_m_s2 * r_m, 0))
            v_orbital_km_s = v_orbital_m_s / km_s_to_m_s
            v_exp_km_s = (h_local / 1000.0) * r
            v_total_km_s = np.sqrt(v_orbital_km_s**2 + v_exp_km_s**2)
            
            return v_total_km_s, v_baryon
            
        def objective(ups_base):
            v_pred, _ = compute_v_pred(ups_base)
            return self.chi_squared(v_obs, v_pred, v_err)

        if optimize_ups:
            res = minimize_scalar(objective, bounds=(0.05, 10.0), method='bounded')
            best_ups = res.x
        else:
            best_ups = model.parameters.get('ups_base', 0.5) if hasattr(model, 'parameters') else 0.5
            
        v_total_km_s, v_baryon = compute_v_pred(best_ups)
        red_chi2 = objective(best_ups)
        
        return {
            'red_chi2': red_chi2,
            'v_pred': v_total_km_s,
            'v_obs': v_obs,
            'v_err': v_err,
            'v_baryon': v_baryon,
            'r': r,
            'z': z,
            'ups_base': best_ups
        }

    def evaluate_rotation_curve_3d(self, model, galaxy_data, z=0.0, optimize_ups=True, metadata=None, independent_bulge=False):
        """
        [Enhanced 3D Geometric Model]
        Evaluate a gravity model using 3D Geometric Potency Factors (gamma) for 
        disk, bulge, and gas distribution.
        
        independent_bulge: If True, optimizes Ups_disk and Ups_bulge separately.
        """
        from scipy.optimize import minimize_scalar, minimize
        from src.utils.constants import G
        
        r = galaxy_data['r'].values
        v_obs = galaxy_data['v_obs'].values
        v_err = galaxy_data['v_err'].values
        
        # 1. Determine Geometric Potency Factors (gamma)
        g_disk, g_bulge, g_gas = 0.95, 1.15, 1.0
        
        if metadata:
            if metadata.get('sb') == 'Low':
                g_disk = 0.90  
                g_gas = 1.05   
            if metadata.get('morphology') == 'Spiral':
                g_bulge = 1.10 
        
        n = model.parameters.get('n', 0.0) if hasattr(model, 'parameters') else 0.0
        z_exp = (1 + z)**(1.0 / (1.0 + n/2.0)) - 1.0 if z > 0 else 0.0
        t_ratio = (1 + z_exp)**(n/2.0)
        
        kpc_to_m = 3.086e19; km_s_to_m_s = 1000.0
        r_m = r * kpc_to_m
        
        def compute_v_pred(ups_d_base, ups_b_base):
            # Apply clock-correction to Upsilon
            Ups_d = ups_d_base / t_ratio
            Ups_b = ups_b_base / t_ratio
            
            # Newtonian acceleration components with 3D Potency Corrections
            gn_gas = g_gas * np.sign(galaxy_data['v_gas']) * (galaxy_data['v_gas'] * 1000)**2 / r_m
            gn_disk = g_disk * Ups_d * (galaxy_data['v_disk'] * 1000)**2 / r_m
            gn_bulge = g_bulge * Ups_b * (galaxy_data['v_bulge'] * 1000)**2 / r_m
            
            gn_total = gn_gas + gn_disk + gn_bulge
            m_eff = (np.maximum(gn_total, 0.0) * r_m**2) / G 
            
            h_local = np.zeros_like(r)
            try:
                res = model.compute_acceleration(r_m, m_eff, z=z)
                g_pred_m_s2, h_local = res if isinstance(res, tuple) else (res, np.zeros_like(r))
            except (TypeError, ValueError, PhysicsError):
                g_pred_m_s2 = model.compute_acceleration(r_m, m_eff)
                
            v_orbital_m_s = np.sqrt(np.maximum(g_pred_m_s2 * r_m, 0))
            v_orbital_km_s = v_orbital_m_s / km_s_to_m_s
            v_exp_km_s = (h_local / 1000.0) * r
            v_total_km_s = np.sqrt(v_orbital_km_s**2 + v_exp_km_s**2)
            
            v_baryon_km_s = np.sqrt(np.maximum(gn_total * r_m, 0)) / km_s_to_m_s
            
            return v_total_km_s, v_baryon_km_s
            
        def objective(x):
            # x is [ups_d] or [ups_d, ups_b]
            if len(x) == 2:
                v_pred, _ = compute_v_pred(x[0], x[1])
            else:
                v_pred, _ = compute_v_pred(x[0], x[0] * 1.4)
            return self.chi_squared(v_obs, v_pred, v_err)

        if optimize_ups:
            if independent_bulge and np.max(galaxy_data['v_bulge']) > 0:
                # Optimize both disk and bulge M/L
                res = minimize(objective, [0.5, 0.7], bounds=[(0.05, 5.0), (0.05, 8.0)], method='L-BFGS-B')
                best_ups_d, best_ups_b = res.x
            else:
                # Legacy linked optimization
                res = minimize_scalar(lambda x: objective([x]), bounds=(0.05, 5.0), method='bounded')
                best_ups_d = res.x
                best_ups_b = best_ups_d * 1.4
        else:
            best_ups_d = model.parameters.get('ups_base', 0.5) if hasattr(model, 'parameters') else 0.5
            best_ups_b = best_ups_d * 1.4
            
        v_total_km_s, v_baryon = compute_v_pred(best_ups_d, best_ups_b)
        red_chi2 = objective([best_ups_d, best_ups_b] if independent_bulge else [best_ups_d])
        
        return {
            'red_chi2': red_chi2,
            'v_pred': v_total_km_s,
            'v_obs': v_obs,
            'v_err': v_err,
            'v_baryon': v_baryon,
            'r': r,
            'z': z,
            'ups_base': best_ups_d,
            'ups_bulge': best_ups_b,
            'gamma': {'disk': g_disk, 'bulge': g_bulge, 'gas': g_gas}
        }

    def plot_hubble_diagram(self, sn_data, results_list, title="Supernova Hubble Diagram", save_path=None):
        """
        Plot the observed vs predicted distance modulus for multiple models using Plotly.
        results_list: List of (label, mu_pred) tuples.
        """
        import plotly.graph_objects as go

        fig = go.Figure()
        # Observed Data
        fig.add_trace(go.Scatter(
            x=sn_data['z'], y=sn_data['mu_obs'], 
            error_y=dict(type='data', array=sn_data.get('mu_err', 0.1), visible=True),
            mode='markers', name='Observed SN Ia', marker=dict(color='black', size=4, opacity=0.3)
        ))

        idx = np.argsort(np.array(sn_data['z']))
        zs_sorted = np.array(sn_data['z'])[idx]

        colors = ['red', 'green', 'blue', 'magenta', 'cyan', 'orange']
        for i, (label, mu_pred) in enumerate(results_list):
            fig.add_trace(go.Scatter(
                x=zs_sorted, y=np.array(mu_pred)[idx],
                mode='lines', name=label, 
                line=dict(color=colors[i % len(colors)], width=2.5)
            ))

        fig.update_layout(title=title, xaxis_title="Redshift (z_obs)", yaxis_title="Distance Modulus (mu)", template="plotly_white", hovermode="x unified")
        if save_path: fig.write_html(save_path.replace('.png', '.html'))
        return fig

    def plot_rotation_curve(self, galaxy_data, results_list, title="Galaxy Rotation Curve", save_path=None):
        """
        Plot rotation curve for multiple models.
        results_list: List of (label, res_dict) tuples.
        """
        import plotly.graph_objects as go
        fig = go.Figure()

        # Observed Data
        fig.add_trace(go.Scatter(
            x=galaxy_data['r'], y=galaxy_data['v_obs'], 
            error_y=dict(type='data', array=galaxy_data['v_err'], visible=True),
            mode='markers', name='Observed (Total)', marker=dict(color='black', size=6)
        ))

        r_vals = np.array(galaxy_data['r']); sort_idx = np.argsort(r_vals); r_sorted = r_vals[sort_idx]

        colors = ['red', 'green', 'magenta', 'cyan', 'orange', 'purple']
        for i, (label, res) in enumerate(results_list):
            v_pred = res['v_pred']
            
            # Format label with Upsilon and Boundary warnings if they exist
            ups_str = ""
            if 'ups_base' in res:
                ups_val = res['ups_base']
                warning = " [WARNING: out of bounds]" if res.get('hit_boundary', False) else ""
                ups_str = f" (&Upsilon;={ups_val:.2f}{warning})"
                
            display_label = f"{label}{ups_str}"
            
            fig.add_trace(go.Scatter(
                x=r_sorted, y=np.array(v_pred)[sort_idx],
                mode='lines', name=display_label,
                line=dict(color=colors[i % len(colors)], width=2.5)
            ))

        # Show baryonic baseline separately if available (calculated from Upsilon=0.5 default)
        Ups_d = 0.5; Ups_b = 0.7
        v_b_sq = (np.sign(galaxy_data['v_gas']) * galaxy_data['v_gas']**2 + 
                  Ups_d * galaxy_data['v_disk']**2 + 
                  Ups_b * galaxy_data['v_bulge']**2)
        v_baryon = np.sqrt(np.maximum(v_b_sq, 1e-10))
        fig.add_trace(go.Scatter(x=r_sorted, y=v_baryon[sort_idx], mode='lines', name='Baryonic Baseline (&Upsilon;=0.5)', line=dict(color='blue', width=2, dash='dot')))

        fig.update_layout(title=title, xaxis_title="Radius (kpc)", yaxis_title="Velocity (km/s)", template="plotly_white", hovermode="closest")
        if save_path: fig.write_html(save_path.replace('.png', '.html'))
        return fig


    def evaluate_sparc_batch(self, model, sparc_dir, master_table=None, category=None):
        """
        Evaluate a model against all galaxies in a SPARC directory.
        """
        import os
        from src.utils.data_loaders import DataLoader
        batch_results = []
        files_to_process = []
        for root, dirs, files in os.walk(sparc_dir):
            for f in files:
                if f.endswith('rotmod.dat'):
                    files_to_process.append(os.path.join(root, f))
        
        for file_path in files_to_process:
            filename = os.path.basename(file_path)
            galaxy_name = filename.replace('_rotmod.dat', '')
            data = DataLoader.load_sparc_galaxy(file_path)
            if data is not None:
                dist = data.attrs.get('dist'); lum = None
                if master_table is not None:
                    meta = master_table[master_table['name'] == galaxy_name]
                    if not meta.empty: dist = meta['dist'].values[0]; lum = meta['lum'].values[0]
                
                z = (70.0 * dist) / 3e5 if dist else 0.0
                if category == 'dwarf' and (lum is None or lum > 1e9): continue
                if category == 'giant' and (lum is None or lum <= 1e9): continue
                res = self.evaluate_rotation_curve(model, data, z=z)
                res['name'] = galaxy_name; res['dist'] = dist; res['lum'] = lum
                batch_results.append(res)
        return pd.DataFrame(batch_results)

    def plot_expansion_comparison(self, model_list, z_range=(0, 2), save_path=None):
        """
        Compare multiple cosmology models expansion rates. Returns fig.
        """
        import plotly.graph_objects as go
        zs = np.linspace(z_range[0], z_range[1], 100); fig = go.Figure()
        colors = ['black', 'red', 'green', 'blue', 'magenta']; dashes = [None, None, 'dash', 'dashdot', 'dot']
        for i, (label, model) in enumerate(model_list):
            fig.add_trace(go.Scatter(x=zs, y=model.hubble_parameter(zs), mode='lines', name=label, line=dict(color=colors[i % len(colors)], dash=dashes[i % len(dashes)], width=2)))
        fig.update_layout(title="Expansion Rate Comparison", xaxis_title="Redshift (z_obs)", yaxis_title="H(z_obs) (km/s/Mpc)", template="plotly_white")
        if save_path: fig.write_html(save_path.replace('.png', '.html'))
        return fig

    def plot_residuals_vs_distance(self, batch_results, title="Chi2 Residuals vs Distance", save_path=None):
        """
        Plot performance vs distance. Returns fig.
        """
        import plotly.graph_objects as go; import plotly.express as px
        if 'dist' not in batch_results.columns: return None
        fig = px.scatter(batch_results, x='dist', y='red_chi2', hover_name='name', log_x=True, log_y=True, title=title, labels={'dist': 'Distance (Mpc)', 'red_chi2': 'Reduced Chi2'})
        if len(batch_results) > 1:
            z = np.polyfit(np.log10(batch_results['dist']), np.log10(batch_results['red_chi2']), 1); p = np.poly1d(z)
            x_r = np.logspace(np.log10(batch_results['dist'].min()), np.log10(batch_results['dist'].max()), 100)
            fig.add_trace(go.Scatter(x=x_r, y=10**p(np.log10(x_r)), mode='lines', name='Trend', line=dict(color='red', dash='dash')))
        fig.update_layout(template="plotly_white")
        if save_path: fig.write_html(save_path.replace('.png', '.html'))
        return fig
