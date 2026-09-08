import numpy as np
import plotly.graph_objects as go

class PlotFactory:
    """
    Centralized factory for generating all Plotly figures used in the Chronodynamic Relativity documentation.
    Takes standardized data payloads from DataProvider.
    """

    @staticmethod
    def create_hubble_diagram(data):
        sn_data = data['sn_data']
        fig = go.Figure()
        
        # Observed Data
        fig.add_trace(go.Scatter(
            x=sn_data['z'], y=sn_data['mu_obs'], 
            error_y=dict(type='data', array=sn_data.get('mu_err', 0.1), visible=True),
            mode='markers', name='Pantheon+ (Observed)', marker=dict(color='black', size=4, opacity=0.3)
        ))

        idx = np.argsort(np.array(sn_data['z']))
        zs_sorted = np.array(sn_data['z'])[idx]

        colors = ['blue', 'orange', 'red']
        dashes = ['dash', 'solid', 'dot']
        
        for i, (label, mu_pred) in enumerate(data['models']):
            fig.add_trace(go.Scatter(
                x=zs_sorted, y=np.array(mu_pred)[idx],
                mode='lines', name=label, 
                line=dict(color=colors[i % len(colors)], width=3 if i==0 else 2, dash=dashes[i % len(dashes)])
            ))

        fig.update_layout(height=450, title="Cosmic Expansion (Hubble Diagram)", xaxis_title="Redshift (z)", yaxis_title="Distance Modulus (mu)", template="plotly_white", hovermode="x unified")
        return fig

    @staticmethod
    def create_rotation_curve(galaxy_result):
        galaxy_data = galaxy_result['galaxy_data']
        models = galaxy_result['models']
        name = galaxy_result.get('name', 'Galaxy')
        meta = galaxy_result.get('meta', {})
        dist = galaxy_result.get('dist_mpc', 0.0)
        
        from plotly.subplots import make_subplots
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # 1. Observed Data
        fig.add_trace(go.Scatter(
            x=galaxy_data['r'], y=galaxy_data['v_obs'], 
            error_y=dict(type='data', array=galaxy_data['v_err'], visible=True),
            mode='markers', name='Observed (Total)', marker=dict(color='black', size=7)
        ), secondary_y=False)

        r_vals = np.array(galaxy_data['r']); sort_idx = np.argsort(r_vals); r_sorted = r_vals[sort_idx]

        colors = ['blue', 'purple', 'orange', 'red']
        dashes = ['solid', 'dash', 'dash', 'dot']
        
        # 2. Model Velocity Curves
        for i, (label, res) in enumerate(models):
            v_pred = res['v_pred']
            ups_str = f" (&Upsilon;={res['ups_base']:.2f})" if 'ups_base' in res else ""
            fig.add_trace(go.Scatter(
                x=r_sorted, y=np.array(v_pred)[sort_idx],
                mode='lines', name=f"{label}{ups_str}",
                line=dict(color=colors[i % len(colors)], width=3 if 'Chronodynamic' in label else 2, dash=dashes[i % len(dashes)])
            ), secondary_y=False)

        # 3. Baryon Component Breakdown
        cr_res = models[0][1]
        ups = cr_res['ups_base']
        gamma = cr_res.get('gamma', {'disk': 1.0, 'bulge': 1.0, 'gas': 1.0})
        
        v_gas_geo = np.array(galaxy_data['v_gas']) * np.sqrt(gamma['gas'])
        v_disk_geo = np.array(galaxy_data['v_disk']) * np.sqrt(ups * gamma['disk'])
        v_bulge_geo = np.array(galaxy_data['v_bulge']) * np.sqrt(1.4 * ups * gamma['bulge'])
        
        fig.add_trace(go.Scatter(x=r_sorted, y=v_gas_geo[sort_idx], mode='lines', name='Gas (Geo)', line=dict(color='red', width=1, dash='dot')), secondary_y=False)
        fig.add_trace(go.Scatter(x=r_sorted, y=v_disk_geo[sort_idx], mode='lines', name='Disk (Geo)', line=dict(color='green', width=1, dash='dot')), secondary_y=False)
        if np.max(v_bulge_geo) > 0:
            fig.add_trace(go.Scatter(x=r_sorted, y=v_bulge_geo[sort_idx], mode='lines', name='Bulge (Geo)', line=dict(color='orange', width=1, dash='dot')), secondary_y=False)

        # 4. Gravitational Potential (Secondary Axis)
        from scipy.integrate import cumulative_trapezoid
        r_m = r_vals * 3.086e19
        g_cr = (cr_res['v_pred'] * 1000)**2 / r_m
        phi_cr = cumulative_trapezoid(g_cr, r_m, initial=0) / (1000**2)
        
        fig.add_trace(go.Scatter(x=r_sorted, y=phi_cr[sort_idx], name='Field Potential (Relative)', line=dict(color='rgba(142, 68, 173, 0.4)', width=2)), secondary_y=True)

        meta_dict = meta if meta else {}
        title_text = f"Rotation: {name} | D={dist:.1f} Mpc | {meta_dict.get('type','')} {meta_dict.get('morphology','')} ({meta_dict.get('sb','')} SB)"
        fig.update_layout(
            height=500,
            title=title_text,
            xaxis_title="Radius (kpc)",
            yaxis_title="Velocity (km/s)",
            yaxis2_title="Potential (km^2/s^2)",
            template="plotly_white",
            legend=dict(font=dict(size=10), bgcolor='rgba(255,255,255,0.5)')
        )
        return fig

    @staticmethod
    def create_lensing_chart(data):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['names'], y=data['obs'], mode='markers', name='Observed (HST/SLACS)', marker=dict(size=12, symbol='diamond', color='black')))
        fig.add_trace(go.Scatter(x=data['names'], y=data['v8'], mode='lines+markers', name='Chronodynamic Relativity', line=dict(color='#8e44ad', width=3)))
        fig.add_trace(go.Scatter(x=data['names'], y=data['sis'], mode='lines+markers', name='LambdaCDM (SIS Ref)', line=dict(color='orange', dash='dash')))
        fig.update_layout(
            height=450, 
            title="Einstein Radii Comparison: SLACS Dataset", 
            xaxis_title="Lens Galaxy (SLACS Survey)", 
            yaxis_title="Einstein Radius (arcsec)", 
            template="plotly_white",
            margin=dict(t=50, b=50, l=50, r=50)
        )
        return fig

    @staticmethod
    def create_black_hole_chart(data):
        import pandas as pd
        res_df = pd.DataFrame(data)
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Observed (EHT)', x=res_df['name'], y=res_df['obs_uas'], error_y=dict(type='data', array=res_df['obs_err']), marker_color='black'))
        fig.add_trace(go.Bar(name='General Relativity', x=res_df['name'], y=res_df['gr_uas'], marker_color='orange'))
        fig.add_trace(go.Bar(name='Chronodynamic Relativity', x=res_df['name'], y=res_df['cr_uas'], marker_color='purple'))
        fig.update_layout(title="Black Hole Shadow Sizes (Event Horizon Telescope)", xaxis_title="Supermassive Black Hole", yaxis_title="Shadow Diameter (\u03Bcas)", barmode='group', template="plotly_white", height=500)
        return fig

    @staticmethod
    def create_impact_cosmic_chart(data):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['z'], y=data['phys'], name='Physical Distance (Linear)', line=dict(color='green', width=3)))
        fig.add_trace(go.Scatter(x=data['z'], y=data['perc_cr'], name='Perceived (Chronodynamic Relativity)', line=dict(color='#8e44ad', dash='dash')))
        fig.add_trace(go.Scatter(x=data['z'], y=data['perc_lcdm'], name='Perceived (LambdaCDM)', line=dict(color='orange', dash='dot')))
        fig.update_layout(title="Cosmic Scale: Real vs Perceived Distance", xaxis_title="Redshift (z)", yaxis_title="Distance (Mpc)", template="plotly_white", height=450)
        return fig

    @staticmethod
    def create_impact_point_chart(data):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['r'], y=data['newton'], name='Newtonian (1/r^2)', line=dict(color='black', dash='dot')))
        fig.add_trace(go.Scatter(x=data['r'], y=data['cr'], name='Chronodynamic Relativity (Non-linear)', line=dict(color='#8e44ad', width=3)))
        fig.update_xaxes(type="log"); fig.update_yaxes(type="log")
        fig.update_layout(title="Gravity Gradient: 1e11 M_sun Point Mass", xaxis_title="Radius (kpc)", yaxis_title="Acceleration (m/s^2)", template="plotly_white", height=450)
        return fig

    @staticmethod
    def create_impact_bridge_chart(data):
        fig = go.Figure(data=go.Contour(z=data['ratio'], x=data['X'][0], y=data['Y'][:,0], colorscale='Viridis', colorbar_title="Log10(Boost)"))
        fig.update_layout(title="The Gravity Bridge (Binary Pair @ 800 kpc)", xaxis_title="X (kpc)", yaxis_title="Y (kpc)", height=450)
        return fig

    @staticmethod
    def create_impact_dist_chart(data):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['r'], y=data['newton'], name='Newtonian (Jaffe)', line=dict(color='black', dash='dot')))
        fig.add_trace(go.Scatter(x=data['r'], y=data['cr'], name='Chronodynamic Relativity (Jaffe)', line=dict(color='#8e44ad', width=3)))
        fig.update_xaxes(type="log"); fig.update_yaxes(type="log")
        fig.update_layout(title="Distributed Mass: Jaffe Profile (r_s=5 kpc)", xaxis_title="Radius (kpc)", yaxis_title="Acceleration (m/s^2)", template="plotly_white", height=450)
        return fig

    @staticmethod
    def create_expansion_cc_chart(data):
        fig = go.Figure()
        cc = data['cc_data']
        fig.add_trace(go.Scatter(x=cc['z'], y=cc['H'], error_y=dict(type='data', array=cc['err'], visible=True), mode='markers', name='Cosmic Chronometers (Obs)', marker=dict(color='black', size=8)))
        idx = np.argsort(cc['z'])
        for label, h_pred in data['cc_models']:
            fig.add_trace(go.Scatter(x=cc['z'].iloc[idx], y=np.array(h_pred)[idx], mode='lines', name=label, line=dict(width=3 if 'Chronodynamic' in label else 2)))
        fig.update_layout(title="Expansion Rate H(z): Cosmic Chronometers", xaxis_title="Redshift (z)", yaxis_title="H(z) [km/s/Mpc]", template="plotly_white", height=450)
        return fig

    @staticmethod
    def create_expansion_qso_chart(data):
        fig = go.Figure()
        qso = data['qso_data']
        fig.add_trace(go.Scatter(x=qso['z'], y=qso['mu'], error_y=dict(type='data', array=qso['err'], visible=True), mode='markers', name='Quasars (Lusso 2020)', marker=dict(color='black', size=6, opacity=0.5)))
        for label, mu_pred in data['qso_models']:
            fig.add_trace(go.Scatter(x=qso['z'], y=mu_pred, mode='lines+markers', name=label))
        fig.update_layout(title="High-z Expansion: Quasar Standard Candles", xaxis_title="Redshift (z)", yaxis_title="Distance Modulus (mu)", template="plotly_white", height=450)
        return fig

    @staticmethod
    def create_impact_duality_chart(data):
        fig = go.Figure()
        # Uncertainty band
        fig.add_trace(go.Scatter(x=data['z'], y=data['eta_high'], fill=None, mode='lines', line_color='rgba(142, 68, 173, 0.1)', showlegend=False))
        fig.add_trace(go.Scatter(x=data['z'], y=data['eta_low'], fill='tonexty', mode='lines', line_color='rgba(142, 68, 173, 0.1)', name='CR uncertainty (n \u00B1 2%)'))
        
        fig.add_trace(go.Scatter(x=data['z'], y=data['eta'], name='Chronodynamic Relativity', line=dict(color='#8e44ad', width=4)))
        fig.add_trace(go.Scatter(x=data['z'], y=[1.0]*len(data['z']), name='LambdaCDM (Standard)', line=dict(color='orange', dash='dash')))
        fig.add_trace(go.Scatter(x=data['obs_z'], y=data['obs_eta'], error_y=dict(type='data', array=data['obs_err'], visible=True), mode='markers+text', name='Empirical Measurements', text=data['obs_ref'], textposition="top center", marker=dict(color='black', size=12, symbol='diamond')))
        fig.update_layout(title="Distance Duality Break: Empirical Validation", xaxis_title="Redshift (z)", yaxis_title="eta(z) = DL / [DA(1+z)^2]", template="plotly_white", height=450, yaxis_range=[0.75, 1.15])
        return fig

    @staticmethod
    def create_temporal_stratigraphy_chart(data):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['z'], y=data['dilation_cr'], name='Chronodynamic Relativity', line=dict(color='#8e44ad', width=4)))
        fig.add_trace(go.Scatter(x=data['z'], y=data['dilation_gr'], name='Standard Relativity (1+z)', line=dict(color='orange', dash='dash')))
        for label in set(data['obs_type']):
            idx = [i for i, t in enumerate(data['obs_type']) if t == label]
            fig.add_trace(go.Scatter(x=[data['obs_z'][i] for i in idx], y=[data['obs_val'][i] for i in idx], error_y=dict(type='data', array=[data['obs_err'][i] for i in idx], visible=True), mode='markers', name=f'{label} Dilation (Obs)', marker=dict(size=10)))
        fig.update_layout(title="Temporal Stratigraphy: Cosmic Clock Depth", xaxis_title="Redshift (z)", yaxis_title="Time Dilation Factor (dt_obs / dt_rest)", template="plotly_white", height=450)
        return fig

    @staticmethod
    def create_vacuum_drag_chart(data):
        fig = go.Figure()
        methods = ['GW170817 (Obs)', 'Chronodynamic Relativity (Pred)', 'Lorentz Violation (Bound)']
        v_diff = [1e-15, 1e-18, 1e-16]
        fig.add_trace(go.Bar(x=methods, y=v_diff, marker_color=['black', '#8e44ad', 'gray']))
        fig.update_yaxes(type="log", title="Fractional Speed Diff |v_gw - c|/c")
        fig.update_layout(title="Vacuum Drag: Multi-Messenger Consistency", template="plotly_white", height=400)
        return fig
