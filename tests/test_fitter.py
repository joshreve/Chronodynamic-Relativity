import unittest
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.models.chronodynamic_model import ChronodynamicModel
from src.evaluations.fitter import ModelFitter
from src.models.gravity_engine import CustomGravity
from src.models.cosmology_engine import CustomCosmology, LambdaCDM

class TestModelFitter(unittest.TestCase):
    def setUp(self):
        self.fitter = ModelFitter()

    def test_fit_gravity_mond(self):
        """Test fitting a MOND-like a0 parameter."""
        # Create mock data with a specific a0
        true_a0 = 1.5e-10
        r = np.linspace(1, 20, 10)
        v_gas = np.zeros_like(r)
        v_disk = 100 * (1 - np.exp(-r/5))
        v_bulge = 0
        v_baryon_sq = v_gas**2 + v_disk**2 + v_bulge**2
        
        # Ground truth: MOND prediction
        def mond_hook(g_baryon, r, params):
            a0 = params['a0']
            return np.sqrt(g_baryon * a0)
            
        from src.utils.constants import G
        kpc_to_m = 3.086e19
        km_s_to_m_s = 1000.0
        r_m = r * kpc_to_m
        v_baryon_m_s = np.sqrt(v_baryon_sq) * km_s_to_m_s
        m_baryon = (v_baryon_m_s**2 * r_m) / G
        
        g_baryon_m_s2 = (G * m_baryon) / r_m**2
        g_obs = np.sqrt(g_baryon_m_s2 * true_a0)
        v_obs = np.sqrt(g_obs * r_m) / km_s_to_m_s
        v_err = np.ones_like(r) * 0.1 # Very small error for clean fit
        
        data = pd.DataFrame({
            'r': r, 'v_obs': v_obs, 'v_err': v_err,
            'v_gas': v_gas, 'v_disk': v_disk, 'v_bulge': v_bulge
        })
        
        # Fit starting from a different a0
        initial_params = {'a0': 1.0e-10}
        
        # Override evaluate_rotation_curve's default ups_base by passing it via a lambda or subclass
        class FixedUpsGravity(CustomGravity):
            def __init__(self, custom_accel_func, parameters=None):
                p = parameters.copy() if parameters else {}
                p['ups_base'] = 1.0 # Force Ups_d = 1.0
                super().__init__(custom_accel_func, p)
                
        optimized, final_chi2 = self.fitter.fit_gravity(FixedUpsGravity, mond_hook, data, initial_params)

        self.assertAlmostEqual(optimized['a0'], true_a0, delta=1e-12)

    def test_fit_cosmology_w(self):
        """Test fitting a dark energy equation of state parameter w."""
        true_w = -0.95
        lcdm = LambdaCDM()
        
        def w_model_h(z, params):
            w = params['w']
            return lcdm.h0 * np.sqrt(0.3 * (1+z)**3 + 0.7 * (1+z)**(3*(1+w)))
            
        # Mock SN data
        zs = np.linspace(0.1, 1.5, 20)
        model_true = CustomCosmology(custom_h_func=w_model_h, parameters={'w': true_w})
        dl_true = model_true.luminosity_distance(zs)
        
        from src.evaluations.benchmark_suite import BenchmarkSuite
        suite = BenchmarkSuite()
        mu_obs = suite.distance_modulus(dl_true)
        mu_err = np.ones_like(zs) * 0.01
        
        sn_data = pd.DataFrame({'z': zs, 'mu_obs': mu_obs, 'mu_err': mu_err})
        
        initial_params = {'w': -1.0}
        optimized, final_chi2 = self.fitter.fit_cosmology(CustomCosmology, w_model_h, sn_data, initial_params)
        
        self.assertAlmostEqual(optimized['w'], true_w, delta=1e-3)

if __name__ == '__main__':
    unittest.main()
