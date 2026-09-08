# Scientific References and Accepted Parameters

This document provides the foundational parameters and literature references used as baselines for the Chronodynamic Relativity tool.

## 1. Global Cosmological Parameters ($\Lambda$CDM)

The standard baseline for cosmic expansion is derived from the Cosmic Microwave Background (CMB) measurements and Type Ia Supernova (SN Ia) surveys.

| Parameter | Symbol | Value | Source |
| :--- | :--- | :--- | :--- |
| Hubble Constant (CMB) | $H_0$ | $67.4 \pm 0.5$ km/s/Mpc | Planck 2018 [1] |
| Hubble Constant (Local) | $H_0$ | $73.5 \pm 1.1$ km/s/Mpc | Pantheon+ / SH0ES [2] |
| Matter Density | $\Omega_m$ | $0.315 \pm 0.007$ | Planck 2018 [1] |
| Dark Energy Density | $\Omega_\Lambda$ | $0.685 \pm 0.007$ | Planck 2018 [1] |
| DE Equation of State | $w$ | $-1.028 \pm 0.032$ | Pantheon+ [2] |
| Space Curvature | $\Omega_k$ | $0.001 \pm 0.002$ | Planck 2018 [1] |

### Citations
- **[1] Planck Collaboration (2020).** "Planck 2018 results. VI. Cosmological parameters." *Astronomy & Astrophysics*, 641, A6. [DOI: 10.1051/0004-6361/201833910](https://doi.org/10.1051/0004-6361/201833910)
- **[2] Scolnic, D., et al. (2022).** "The Pantheon+ Analysis: The Combined Sample of Type Ia Supernovae and Cosmological Constraints." *The Astrophysical Journal*, 938, 113. [DOI: 10.3847/1538-4357/ac8b7a](https://doi.org/10.3847/1538-4357/ac8b7a)

---

## 2. Galactic Dynamics and Modified Gravity

The alternative physics baseline uses Modified Newtonian Dynamics (MOND) as the primary comparison for galactic rotation curves without dark matter halos.

| Parameter | Symbol | Value | Source |
| :--- | :--- | :--- | :--- |
| MOND Acceleration Scale | $a_0$ | $1.2 \times 10^{-10}$ m/s² | Milgrom 1983 [3] |
| Empirical a0 (SPARC) | $a_0$ | $1.21 \pm 0.02$ m/s² | Lelli et al. 2016 [4] |

### Citations
- **[3] Milgrom, M. (1983).** "A modification of the Newtonian dynamics as a possible alternative to the hidden mass hypothesis." *The Astrophysical Journal*, 270, 365. [DOI: 10.1086/161130](https://doi.org/10.1086/161130)
- **[4] Lelli, F., McGaugh, S. S., & Schombert, J. M. (2016).** "SPARC: Spatzer Photometry and Accurate Rotation Curves." *The Astronomical Journal*, 152, 157. [DOI: 10.3847/0004-6256/152/6/157](https://doi.org/10.3847/0004-6256/152/6/157)
- **[5] Begeman, K. G., Broeils, A. H., & Sanders, R. H. (1991).** "Extended rotation curves of spiral galaxies: dark haloes and modified dynamics." *MNRAS*, 249, 439.

---

## 3. Foundational Machian & Metric Origin Literature

Foundational literature connecting local inertia, acceleration thresholds, and cosmic boundary conditions:

- **[6] Mach, E. (1883).** *Die Mechanik in ihrer Entwickelung historisch-kritisch dargestellt.* Leipzig: F. A. Brockhaus.
- **[7] Sciama, D. W. (1953).** "On the origin of inertia." *Monthly Notices of the Royal Astronomical Society*, 113(1), 34–42. [DOI: 10.1093/mnras/113.1.34](https://doi.org/10.1093/mnras/113.1.34)
- **[8] Brans, C., & Dicke, R. H. (1961).** "Mach's Principle and a Relativistic Theory of Gravitation." *Physical Review*, 124(3), 925–935. [DOI: 10.1103/PhysRev.124.925](https://doi.org/10.1103/PhysRev.124.925)
- **[9] Milgrom, M. (1999).** "The MOND limit from spacetime scale invariance." *Physics Letters A*, 253(5-6), 273–279. [DOI: 10.1016/S0375-9601(99)00077-8](https://doi.org/10.1016/S0375-9601(99)00077-8)

---

## 4. Data Ingestion Standards

The Chronodynamic Relativity tool is designed to interface with the following standard data formats:

- **SPARC (Galaxies):** Tabulated text files with columns: `R`, `Vobs`, `errV`, `Vgas`, `Vdisk`, `Vbulge`.
- **Pantheon+ (Supernovae):** CSV files with columns: `zcmb` (redshift), `mu` (distance modulus), `mu_err`.

