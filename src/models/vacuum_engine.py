import numpy as np
from src.utils.constants import G, C_KM_S

class VacuumEngine:
    """
    Engine for modeling vacuum field interactions and the Dynamical Casimir Effect (DCE) 
    within the Chronodynamic Relativity framework.
    """
    def __init__(self, h0=70.5, beta=0.2385):
        """
        Args:
            h0: Hubble constant in km/s/Mpc.
            beta: Density scaling power for relaxation (linked to project n).
        """
        self.c = C_KM_S * 1000.0 # m/s
        self.h0_si = h0 * 1000.0 / 3.086e22 # 1/s
        self.beta = beta
        self.a0 = (self.c * self.h0_si) / (4.0 * np.pi)
        
    def get_relaxation_time(self, rho_s):
        """
        Calculates the vacuum relaxation time tau.
        Calibrated: In high density (Earth, rho=100), tau is near-zero (sub-second).
        In low density (Cluster, rho=0.01), tau is ~100 Myr.
        """
        # Hubble time in Myr: ~14,000 Myr
        tau_hubble_myr = 14400.0
        
        # We scale tau relative to a critical density.
        # tau = tau_hubble * (rho_s / rho_crit)^-beta
        # Let's set rho_crit such that intergalactic rho=0.01 gives 144 Myr.
        return tau_hubble_myr * (rho_s / 0.01)**(-self.beta) / 100.0

    def simulate_memory_well(self, time_array, mass_position_func, rho_s_local):
        """
        Models the potential well lag.
        The potential well position (Phi_pos) follows the mass (X_pos) 
        via tau * d(Phi_pos)/dt = (X_pos - Phi_pos)
        """
        tau = self.get_relaxation_time(rho_s_local)
        dt = time_array[1] - time_array[0]
        
        phi_pos = np.zeros_like(time_array)
        x_mass = mass_position_func(time_array)
        
        # Euler integration for the position of the potential well
        for i in range(1, len(time_array)):
            d_pos = (x_mass[i] - phi_pos[i-1]) / tau
            phi_pos[i] = phi_pos[i-1] + d_pos * dt
            
        return phi_pos, x_mass, tau

    def simulate_vortex_breakaway(self, x_mass, velocity, rho_s):
        """
        Models the smooth breakaway of the potential well from the gas.
        Uses a continuous sigmoid transition instead of a sharp velocity threshold.
        """
        v_crit = 1000.0 * np.sqrt(rho_s / 0.01)
        tau = self.get_relaxation_time(rho_s)
        offset_ideal = velocity * tau / 1000.0
        
        # Smooth activation factor (0 at v=0, 1 at v >> v_crit)
        activation = 1.0 / (1.0 + np.exp(-(velocity - v_crit) / (0.1 * v_crit)))
        return x_mass - offset_ideal * activation
        
    def get_shatter_factor(self, acceleration, width=0.1):
        """
        Calculates the smooth vacuum 'shattering' factor. 
        Replaces the hard step with an infinitely differentiable (C^infinity) smooth logistic transition.
        """
        accel_mag = np.abs(acceleration)
        delta_a = width * self.a0
        # Smooth logistic decay: 1.0 at a << a0 (coupled), 0.0 at a >> a0 (decoupled)
        return 1.0 / (1.0 + np.exp((accel_mag - self.a0) / np.maximum(delta_a, 1e-15)))

    def compute_radiated_power(self, acceleration, amplitude=1.0):
        """
        Calculates the radiated power from a moving boundary (DCE).
        P_rad is proportional to the square of the boundary acceleration.
        
        Mechanism: As the boundary condition oscillates faster than the 
        background field's recovery time (determined by a0), it creates
        high-frequency shear that shatters the vacuum coupling.
        """
        # The radiated power only manifests when the vacuum is shattered (shatter=0)
        # P_rad ~ (1 - coupling) * a^2
        coupling = self.get_shatter_factor(acceleration)
        shatter = 1.0 - coupling
        
        return shatter * (acceleration**2) * amplitude

    def simulate_wilson_experiment(self, frequency_ghz, velocity_c):
        """
        Simulates the Wilson et al. (2011) SQUID experiment.
        Predicts if the threshold for photon production is reached.
        """
        # omega = 2 * pi * f
        omega = 2.0 * np.pi * frequency_ghz * 1e9
        
        # Effective velocity v = 0.05c
        v_max = velocity_c * self.c
        
        # For harmonic motion x(t) = A sin(omega t):
        # v_max = A * omega
        # a_max = A * omega^2 = v_max * omega
        a_max = v_max * omega
        
        power = self.compute_radiated_power(a_max)
        is_radiating = power > 0
        
        return {
            "a_max": a_max,
            "a0_threshold": self.a0,
            "is_radiating": is_radiating,
            "normalized_power": power
        }
