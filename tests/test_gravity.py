import unittest
import os
import sys
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.models.gravity_engine import NewtonianGravity, NFWHalo, MOGGravity, CustomGravity
from src.models.base import PhysicsError
from src.utils.constants import G

class TestGravityEngine(unittest.TestCase):
    def test_newtonian_point_mass(self):
        """Test Newtonian acceleration for a point mass."""
        model = NewtonianGravity()
        
        # M = 1e11 solar masses
        M_sun = 1.989e30 # kg
        M = 1e11 * M_sun
        
        # r = 10 kpc
        kpc_to_m = 3.086e19
        r = 10 * kpc_to_m
        
        g_expected = (G * M) / (r**2)
        g_calc = model.compute_acceleration(r, M)
        
        self.assertAlmostEqual(g_calc, g_expected)

    def test_nfw_halo(self):
        """Test NFW halo mass and acceleration."""
        rho0 = 1e-21 # kg/m^3
        rs = 20 * 3.086e19 # 20 kpc in meters
        halo = NFWHalo(rho0, rs)
        
        # At r = rs, M = 4 * pi * rho0 * rs^3 * (ln(2) - 0.5)
        m_expected = 4 * np.pi * rho0 * (rs**3) * (np.log(2) - 0.5)
        self.assertAlmostEqual(halo.mass(rs), m_expected)
        
        model = NewtonianGravity(dm_halo=halo)
        # Point mass center (baryon) = 0
        g_calc = model.compute_acceleration(rs, 0.0)
        g_expected = (G * m_expected) / (rs**2)
        self.assertAlmostEqual(g_calc, g_expected)

    def test_custom_gravity(self):
        """Test custom gravity acceleration hook."""
        def mond_like(g_baryon, r, params):
            a0 = params.get('a0', 1.2e-10)
            # Simple interpolation: g = sqrt(g_baryon * a0) for g_baryon << a0
            return np.sqrt(g_baryon * a0)
            
        model = CustomGravity(custom_accel_func=mond_like, parameters={'a0': 1.0e-10})
        
        g_baryon_test = 1.0e-12
        g_expected = np.sqrt(g_baryon_test * 1.0e-10)
        
        # We need to provide a baryon mass profile that gives g_baryon_test
        # g = GM/r^2 => M = g * r^2 / G
        r = 1.0e20
        M = (g_baryon_test * r**2) / G
        
        g_calc = model.compute_acceleration(r, M)
        self.assertAlmostEqual(g_calc, g_expected)

    def test_gravity_error_handling(self):
        """Test PhysicsError for invalid gravity results."""
        model = NewtonianGravity()
        
        # Negative mass
        with self.assertRaises(PhysicsError):
            model.compute_acceleration(1.0e20, -1e30)
            
        # NaN result (e.g., r=0 if not handled)
        # Note: I added handling for r=0, so let's check it returns 0
        self.assertEqual(model.compute_acceleration(0.0, 1e30), 0.0)

if __name__ == '__main__':
    unittest.main()
