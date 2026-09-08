import unittest
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.evaluations.benchmark_suite import BenchmarkSuite
from src.models.gravity_engine import NewtonianGravity

class TestBenchmarkSuite(unittest.TestCase):
    def setUp(self):
        self.suite = BenchmarkSuite()

    def test_chi_squared(self):
        observed = [10.0, 20.0, 30.0]
        predicted = [11.0, 19.0, 31.0]
        errors = [1.0, 1.0, 1.0]
        
        # chi2 = (1)^2 + (-1)^2 + (1)^2 = 3
        # red_chi2 = 3 / 3 = 1.0
        self.assertAlmostEqual(self.suite.chi_squared(observed, predicted, errors), 1.0)

    def test_evaluate_rotation_curve_newtonian(self):
        # Create a mock galaxy where observed matches Newtonian + DM
        r = np.linspace(1, 20, 10) # kpc
        v_gas = np.ones_like(r) * 10.0
        v_disk = np.ones_like(r) * 50.0
        v_bulge = np.zeros_like(r)
        
        v_baryon_sq = v_gas**2 + v_disk**2 + v_bulge**2
        
        # Add a mock DM component to observed velocity
        v_dm_sq = 100.0 * r # Linear increase for mock purposes
        v_obs_sq = v_baryon_sq + v_dm_sq
        v_obs = np.sqrt(v_obs_sq)
        v_err = np.ones_like(r) * 2.0
        
        data = pd.DataFrame({
            'r': r,
            'v_obs': v_obs,
            'v_err': v_err,
            'v_gas': v_gas,
            'v_disk': v_disk,
            'v_bulge': v_bulge
        })
        
        # Test with Newtonian (no DM halo initially)
        model_no_dm = NewtonianGravity()
        
        # Turn off optimization to test the pure deterministic output
        model_no_dm.parameters = {'ups_base': 1.0}
        result_no_dm = self.suite.evaluate_rotation_curve(model_no_dm, data, optimize_ups=False)
        
        # Without DM, v_pred should be sqrt(v_baryon_sq)
        # Note: evaluate_rotation_curve uses Ups_d = ups_base and Ups_b = ups_base * 1.4
        # Since ups_base = 1.0, Ups_d = 1.0, Ups_b = 1.4
        # Our mock has v_bulge = 0, so v_baryon_sq = v_gas^2 + 1.0 * v_disk^2
        v_pred_no_dm = np.sqrt(v_gas**2 + 1.0 * v_disk**2)
        np.testing.assert_allclose(result_no_dm['v_pred'], v_pred_no_dm, rtol=1e-5)
        
        # Check that chi2 is large since we added v_dm_sq to v_obs
        self.assertTrue(result_no_dm['red_chi2'] > 10.0)

    def test_evaluate_cluster_mergers(self):
        # Create mock merger data
        merger_data = pd.DataFrame({
            'name': ['Bullet', 'Galactic'],
            'v_km_s': [4000.0, 300.0],
            'offset_obs': [250.0, 0.0],
            'err': [30.0, 5.0],
            'mass_1e14': [20.0, 0.01]
        })
        
        # Mock model with viscosity params
        class MockModel:
            def __init__(self):
                self.lag_params = {'a_0': 0.001360}
        
        model = MockModel()
        result = self.suite.evaluate_cluster_mergers(model, merger_data)
        
        self.assertIn('red_chi2', result)
        self.assertIn('offset_pred', result)
        self.assertEqual(len(result['offset_pred']), 2)
        
        # Bullet should have significant offset, Galactic should have a smaller offset (~20 kpc)
        self.assertTrue(result['offset_pred'][0] > 100.0)
        self.assertTrue(result['offset_pred'][1] < 25.0)

if __name__ == '__main__':
    unittest.main()
