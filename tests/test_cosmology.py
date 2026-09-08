import unittest
import os
import sys
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.models.cosmology_engine import LambdaCDM, CustomCosmology
from src.models.base import PhysicsError
from src.utils.constants import H0_DEFAULT

class TestCosmologyEngine(unittest.TestCase):
    def test_lambdacdm_hubble(self):
        """Test Hubble parameter calculation for LambdaCDM."""
        model = LambdaCDM(h0=70.0, omega_m=0.3, omega_l=0.7, omega_r=0.0, omega_k=0.0)

        # At z=0, H(0) should be H0
        self.assertAlmostEqual(model.hubble_parameter(0.0), 70.0)
        
        # Test array input
        zs = np.array([0.0, 1.0, 2.0])
        hs = model.hubble_parameter(zs)
        self.assertEqual(len(hs), 3)
        self.assertAlmostEqual(hs[0], 70.0)
        self.assertTrue(np.all(hs[1:] > 70.0)) # Expansion should be faster in the past for these params

    def test_lambdacdm_luminosity_distance(self):
        """Test luminosity distance calculation for LambdaCDM."""
        model = LambdaCDM(h0=70.0, omega_m=0.3, omega_l=0.7)
        
        # At z=0, dL should be 0
        self.assertEqual(model.luminosity_distance(0.0), 0.0)
        
        # Test a small redshift (linear Hubble law approximation dL ~ c*z/H0)
        from src.utils.constants import C_KM_S
        z_small = 0.01
        dl_expected = (C_KM_S * z_small) / 70.0
        dl_calc = model.luminosity_distance(z_small)
        
        # Allow some deviation as LambdaCDM isn't perfectly linear even at low z
        self.assertAlmostEqual(dl_calc, dl_expected, delta=dl_expected * 0.05)

    def test_custom_cosmology(self):
        """Test the custom expansion hook."""
        def constant_h(z, params):
            return params.get('const_h', 100.0)
            
        model = CustomCosmology(custom_h_func=constant_h, parameters={'const_h': 80.0})
        
        self.assertEqual(model.hubble_parameter(0.5), 80.0)
        
        # Test integration with constant H
        # dL = (1+z) * c * integral(dz/H) = (1+z) * c * z / H
        from src.utils.constants import C_KM_S
        z = 1.0
        dl_expected = (1 + z) * C_KM_S * z / 80.0
        self.assertAlmostEqual(model.luminosity_distance(z), dl_expected)

    def test_physics_error_handling(self):
        """Test that non-physical results raise PhysicsError."""
        # LambdaCDM with negative densities (non-physical)
        model = LambdaCDM(h0=70.0, omega_m=-1.0, omega_l=-1.0)
        with self.assertRaises(PhysicsError):
            model.hubble_parameter(1.0)
            
        # Custom model returning negative H
        def bad_h(z, params):
            return -10.0
        model_bad = CustomCosmology(custom_h_func=bad_h)
        with self.assertRaises(PhysicsError):
            model_bad.hubble_parameter(0.0)

if __name__ == '__main__':
    unittest.main()
