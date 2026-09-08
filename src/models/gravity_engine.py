import numpy as np
from src.models.base import GravityModel, PhysicsError
from src.utils.constants import G

class NewtonianGravity(GravityModel):
    """
    Standard Newtonian gravity baseline, optionally including a DM halo.
    """
    def __init__(self, dm_halo=None):
        """
        Args:
            dm_halo: An object with a mass(r) method, e.g., an NFWHalo.
        """
        self.dm_halo = dm_halo

    def compute_acceleration(self, r, baryonic_mass_profile, **kwargs):
        """
        g_total = g_baryon + g_dm
        g = G * M(<r) / r^2
        """
        r = np.atleast_1d(r)
        
        # Avoid division by zero at the center
        r_safe = np.where(r == 0, np.inf, r)
        
        # M_baryon can be a callable or a scalar if mass is constant (unlikely for profiles)
        if callable(baryonic_mass_profile):
            m_baryon = baryonic_mass_profile(r)
        else:
            m_baryon = baryonic_mass_profile
            
        g_baryon = (G * m_baryon) / (r_safe**2)
        
        g_dm = 0.0
        if self.dm_halo is not None:
            m_dm = self.dm_halo.mass(r)
            g_dm = (G * m_dm) / (r_safe**2)
            
        g_total = g_baryon + g_dm
        
        # Handle the r=0 case: acceleration at center is 0 for spherical symmetry
        g_total = np.where(r == 0, 0.0, g_total)
        
        result = g_total if len(g_total) > 1 or not np.isscalar(r) else g_total[0]
        return self.validate_result(result)

class NFWHalo:
    """
    Navarro-Frenk-White Dark Matter Halo profile.
    """
    def __init__(self, rho0, rs):
        """
        Args:
            rho0: Characteristic density.
            rs: Scale radius.
        """
        self.rho0 = rho0
        self.rs = rs

    def mass(self, r):
        """
        M(r) = 4 * pi * rho0 * rs^3 * [ln((rs+r)/rs) - r/(rs+r)]
        """
        x = r / self.rs
        m = 4 * np.pi * self.rho0 * (self.rs**3) * (np.log(1 + x) - x / (1 + x))
        return m

class CustomGravity(GravityModel):
    """
    Gravity model with a custom acceleration injection hook.
    """
    def __init__(self, custom_accel_func, parameters=None):
        """
        Args:
            custom_accel_func: Function f(g_baryon, r, parameters) -> float.
            parameters: Dictionary of model parameters.
        """
        self.custom_accel_func = custom_accel_func
        self.parameters = parameters or {}

    def compute_acceleration(self, r, baryonic_mass_profile, **kwargs):
        r = np.atleast_1d(r)
        r_safe = np.where(r == 0, np.inf, r)
        
        if callable(baryonic_mass_profile):
            m_baryon = baryonic_mass_profile(r)
        else:
            m_baryon = baryonic_mass_profile
            
        g_baryon = (G * m_baryon) / (r_safe**2)
        g_baryon = np.where(r == 0, 0.0, g_baryon)
        
        params = {**self.parameters, **kwargs}
        
        # The hook can be vectorized or called in a loop
        g_custom = self.custom_accel_func(g_baryon, r, params)

        result = g_custom if len(g_custom) > 1 or not np.isscalar(r) else g_custom[0]
        return self.validate_result(result)

class MOGGravity(GravityModel):
    """
    Moffat's Scalar-Tensor-Vector Gravity (STVG / MOG).
    g(r) = (G_N * M / r^2) * [1 + alpha - alpha * (1 + mu*r) * exp(-mu*r)]
    """
    def __init__(self, alpha_mog=8.89, mu_mog=0.042):
        self.alpha_mog = alpha_mog
        self.mu_mog = mu_mog # kpc^-1

    def compute_acceleration(self, r, baryonic_mass_profile, **kwargs):
        r = np.atleast_1d(r)
        r_safe = np.where(r == 0, np.inf, r)
        
        if callable(baryonic_mass_profile):
            m_baryon = baryonic_mass_profile(r)
        else:
            m_baryon = baryonic_mass_profile
            
        g_newton = (G * m_baryon) / (r_safe**2)
        
        # MOG factor
        # mu converted to meters^-1 if r is in meters
        # but SPARC radii are in kpc. Let's assume standard Mog params in kpc.
        # mu ~ 0.042 kpc^-1, alpha ~ 8.89
        
        mog_factor = 1.0 + self.alpha_mog - self.alpha_mog * (1.0 + self.mu_mog * r) * np.exp(-self.mu_mog * r)
        g_total = g_newton * mog_factor
        
        g_total = np.where(r == 0, 0.0, g_total)
        result = g_total if len(g_total) > 1 or not np.isscalar(r) else g_total[0]
        return self.validate_result(result)
