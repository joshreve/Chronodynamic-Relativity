import numpy as np
from scipy.integrate import quad
from src.models.base import CosmologyModel, PhysicsError
from src.utils.constants import C_KM_S, H0_DEFAULT, OMEGA_M_DEFAULT, OMEGA_L_DEFAULT, OMEGA_R_DEFAULT, OMEGA_K_DEFAULT

class LambdaCDM(CosmologyModel):
    """
    Standard Lambda-CDM cosmological model.
    """
    def __init__(self, h0=H0_DEFAULT, omega_m=OMEGA_M_DEFAULT, omega_l=OMEGA_L_DEFAULT, 
                 omega_r=OMEGA_R_DEFAULT, omega_k=OMEGA_K_DEFAULT):
        self.h0 = h0
        self.omega_m = omega_m
        self.omega_l = omega_l
        self.omega_r = omega_r
        self.omega_k = omega_k

    def hubble_parameter(self, z, **kwargs):
        """
        H^2(z) = H0^2 [ Omega_r(1+z)^4 + Omega_m(1+z)^3 + Omega_k(1+z)^2 + Omega_Lambda ]
        """
        z = np.array(z)
        term_r = self.omega_r * (1 + z)**4
        term_m = self.omega_m * (1 + z)**3
        term_k = self.omega_k * (1 + z)**2
        term_l = self.omega_l
        
        h_squared = self.h0**2 * (term_r + term_m + term_k + term_l)
        
        if np.any(h_squared < 0):
            raise PhysicsError("H^2(z) is negative, leading to non-physical imaginary expansion rates.")
            
        h = np.sqrt(h_squared)
        return self.validate_result(h, "H(z)")

    def luminosity_distance(self, z, **kwargs):
        """
        dL(z) = (1+z) * c * integral_0^z (dz' / H(z'))
        """
        z_array = np.atleast_1d(z)
        distances = []
        
        for val in z_array:
            if val == 0:
                distances.append(0.0)
                continue
                
            # Integrand: 1 / H(z')
            integrand = lambda zp: 1.0 / self.hubble_parameter(zp)
            integral, _ = quad(integrand, 0, val)
            
            dl = (1 + val) * C_KM_S * integral
            distances.append(dl)
            
        result = np.array(distances)
        if np.isscalar(z):
            return self.validate_result(result[0], "dL(z)")
        return self.validate_result(result, "dL(z)")

    def angular_diameter_distance(self, z, **kwargs):
        """
        dA(z) = dL(z) / (1+z)^2
        """
        dl = self.luminosity_distance(z, **kwargs)
        da = dl / (1 + np.array(z))**2
        return self.validate_result(da, "dA(z)")

class CustomCosmology(CosmologyModel):
    """
    Cosmological model with a custom Hubble parameter injection hook.
    """
    def __init__(self, custom_h_func, h0=H0_DEFAULT, parameters=None):
        """
        Args:
            custom_h_func: A function with signature f(z, parameters) -> float (H in km/s/Mpc).
            h0: Standard H0 for reference.
            parameters: Dictionary of parameters for the custom function.
        """
        self.custom_h_func = custom_h_func
        self.h0 = h0
        self.parameters = parameters or {}

    def hubble_parameter(self, z, **kwargs):
        # Merge initialization parameters with call-time overrides
        params = {**self.parameters, **kwargs}
        
        # Ensure z is handled correctly (the custom function might expect a scalar or array)
        if np.iterable(z):
            h = np.array([self.custom_h_func(val, params) for val in z])
        else:
            h = self.custom_h_func(z, params)
            
        if np.any(h < 0):
             raise PhysicsError("Custom Hubble parameter returned negative values.")
             
        return self.validate_result(h, "Custom H(z)")

    def luminosity_distance(self, z, **kwargs):
        z_array = np.atleast_1d(z)
        params = {**self.parameters, **kwargs}
        distances = []
        
        for val in z_array:
            if val == 0:
                distances.append(0.0)
                continue
                
            integrand = lambda zp: 1.0 / self.hubble_parameter(zp, **params)
            integral, _ = quad(integrand, 0, val)
            
            dl = (1 + val) * C_KM_S * integral
            distances.append(dl)
            
        result = np.array(distances)
        if np.isscalar(z):
            return self.validate_result(result[0], "dL(z)")
        return self.validate_result(result, "dL(z)")

    def angular_diameter_distance(self, z, **kwargs):
        """
        dA(z) = dL(z) / (1+z)^2
        """
        dl = self.luminosity_distance(z, **kwargs)
        da = dl / (1 + np.array(z))**2
        return self.validate_result(da, "dA(z)")
