# CLASS-CR: Chronodynamic Relativity Boltzmann Code Fork
==========================================================

**CLASS-CR** is a dedicated relativistic Boltzmann solver fork of the Cosmic Linear Anisotropy Solving System (CLASS), modified from first principles for **Chronodynamic Relativity (CR)**.

## Core Chronodynamic Physics Implemented:
1. **Background Module (`source/background.c`):**
   * Physical expansion redshift mapping: $(1 + z_{\text{obs}}) = (1 + z_{\text{exp}})^{1 + n/2}$ with $n = 0.239$.
   * Metric clock dilation scaling: $\eta(z) = (1+z)^{n/2}$.
   * Variable space-density conformal time integration $\tau(a)$.

2. **Thermodynamics Module (`source/thermodynamics.c`):**
   * Multi-level Peebles recombination ODE scaled by metric clock dilation $\eta(z)$.
   * Free electron fraction $X_e(z)$, Thomson optical depth $\kappa(\tau)$, and visibility $g(\tau) = \dot{\kappa}e^{-\kappa}$.

3. **Perturbations Module (`source/perturbations.c`):**
   * Full high-multipole Boltzmann hierarchy ($\ell_{\text{max}} = 17$ for photons, $\ell_{\text{max}} = 8$ for neutrinos).
   * Dynamic algebraic-root gravitational potential boost $\Phi_{\text{eff}}(k, \tau) = \Phi_{\text{GR}} \times \mu_{\text{CR}}(k, \tau)$.
   * Redshift-scaled critical acceleration $a_0(z) = a_0(1+z)^{2n}$.
   * Direct time-differential extraction of the Early-ISW source term $S_{\text{ISW}} = e^{-\kappa}(\dot{\Phi} + \dot{\Psi})$.

4. **Transfer & Spectra Modules (`source/transfer.c`, `source/spectra.c`):**
   * Line-of-sight spherical Bessel convolution across $N_k \ge 1500$ Fourier modes.
   * Direct computation of $C_\ell^{TT}, C_\ell^{EE}, C_\ell^{TE}, C_\ell^{\phi\phi}$.
   * 3D baryonic space-density refractive lensing convolution.

## Compilation & Usage:
```bash
make
./class cr_planck.ini
```
