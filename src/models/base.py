from abc import ABC, abstractmethod
import numpy as np

class PhysicsError(Exception):
    """Exception raised for non-physical results in cosmology or gravity calculations."""
    pass

class CosmologyModel(ABC):
    """
    Abstract base class for cosmological expansion models.
    """

    @abstractmethod
    def hubble_parameter(self, z, **kwargs):
        """
        Compute the Hubble parameter H(z).
        
        Args:
            z: Redshift (float or array-like).
            **kwargs: Model-specific parameters.
            
        Returns:
            H(z) in km/s/Mpc.
        """
        pass

    @abstractmethod
    def luminosity_distance(self, z, **kwargs):
        """
        Compute the luminosity distance d_L(z).
        
        Args:
            z: Redshift (float or array-like).
            **kwargs: Model-specific parameters.
            
        Returns:
            d_L(z) in Mpc.
        """
        pass

    @abstractmethod
    def angular_diameter_distance(self, z, **kwargs):
        """
        Compute the angular diameter distance d_A(z).
        
        Args:
            z: Redshift (float or array-like).
            **kwargs: Model-specific parameters.
            
        Returns:
            d_A(z) in Mpc.
        """
        pass

    def luminosity_modulus(self, z, **kwargs):
        """
        Computes the distance modulus mu = 5 * log10(dL) + 25.
        Standard for distance candles.
        """
        dl = self.luminosity_distance(z, **kwargs)
        return 5 * np.log10(np.maximum(dl, 1e-10)) + 25

    def validate_result(self, value, name="Result"):
        """
        Validate that the result is physical.
        """
        if np.any(np.isnan(value)):
            raise PhysicsError(f"{name} contains NaN.")
        if np.any(np.isinf(value)):
            raise PhysicsError(f"{name} contains infinity.")
        if np.any(np.iscomplex(value)):
            raise PhysicsError(f"{name} contains complex numbers.")
        return value

class GravityModel(ABC):
    """
    Abstract base class for local kinematics and gravity models.
    """

    @abstractmethod
    def compute_acceleration(self, r, baryonic_mass_profile, **kwargs):
        """
        Compute total acceleration at distance r.

        Args:
            r: Radial distance from center (float or array-like).
            baryonic_mass_profile: Function or object providing M_baryon(r).
            **kwargs: Model-specific parameters (e.g., DM halo parameters).

        Returns:
            Total acceleration g(r).
        """
        pass

    def validate_result(self, value, name="Acceleration"):
        """
        Validate that the result is physical.
        """
        if np.any(np.isnan(value)):
            raise PhysicsError(f"{name} contains NaN.")
        if np.any(np.isinf(value)):
            raise PhysicsError(f"{name} contains infinity.")
        if np.any(value < 0):
            # In this context, we usually deal with the magnitude of centripetal acceleration
            raise PhysicsError(f"{name} contains non-physical negative values.")
        return value
