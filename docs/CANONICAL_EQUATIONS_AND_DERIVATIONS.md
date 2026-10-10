# Canonical Equations, Derivation Processes, and Derived Physical Observables

This document provides the authoritative, single-source-of-truth mathematical reference for **Chronodynamic Relativity (CR)**. 
Every equation, asymptotic series limit, and zero-parameter physical observable is derived symbolically from first principles using the SymPy symbolic engine (`src.models.SymbolicChronodynamicModel`).

> [!IMPORTANT]
> **The Four-Tier Derivation Architecture:**
> 1. **Tier 1: Dynamic Continuous Field Equations** formulated strictly in continuous variables: metric coordinate time $t$, dynamic causal horizon radius $R(t) = c \cdot t$, and particle proper clock time $\tau$.
> 2. **Tier 2: Present-Epoch Boundary Evaluations** deriving the subscript-0 parameters ($H_0, t_0, R_0, a_0, \tau_0, \rho_0$) by evaluating the continuous Tier 1 equations at the present epoch $t = t_0$ ($R = R_0$).
> 3. **Tier 3: Geometric First-Principles Derivations** analytically determining the dilution exponent $n = \frac{3}{4\pi}$ and relaxation stiffness $k = \frac{3}{4\pi\sqrt{2}}$ from 3D Euclidean spatial geometry.
> 4. **Tier 4: Derived Zero-Parameter Observables & Asymptotic Series** yielding the exact formulas tested across all 11 manuscripts in Series 1 and Series 2.

---

## Relativistic Time Disentanglement: Proper Time ($\tau$) vs. Metric Coordinate Time ($t$)

A critical foundation of Chronodynamic Relativity is the rigorous separation between **observer coordinate time $t$** and **worldline proper time $\tau$**. Along any physical worldline, the differential line element establishes:
$$\mathrm{d}\tau = \eta_{\text{dyn}}(t, v) \, \mathrm{d}t = \frac{1}{\gamma_{\text{dyn}}(t)} \, \mathrm{d}t$$

Consequently, the frame conversion operator between proper time derivatives and coordinate time derivatives is:
$$\frac{\mathrm{d}}{\mathrm{d}\tau} \equiv \frac{1}{\eta_{\text{dyn}}} \frac{\mathrm{d}}{\mathrm{d}t} = \gamma_{\text{dyn}} \frac{\mathrm{d}}{\mathrm{d}t}$$

This operator prevents any derivative skew between laboratory frame tracking (where coordinate velocity $v = \mathrm{d}x/\mathrm{d}t$ and 3-force $F = \mathrm{d}p/\mathrm{d}t$ reside) and particle worldlines (where 4-acceleration $a^\mu = \mathrm{d}u^\mu/\mathrm{d}\tau$ and atomic clock frequencies reside).

---

## Tier 1: Dynamic Continuous Field Equations (Variable $t$ & Horizon $R(t)$)

These equations are the primary, fundamental field relations of Chronodynamic Relativity. They are independent of epoch boundary assumptions and expressed continuously in metric coordinate time $t$, dynamic horizon radius $R(t) = c \cdot t$, or particle proper time $\tau$.

| Equation | Name | Derivative Frame | Paper Cross-Reference |
| :--- | :--- | :--- | :--- |
| $R{\left(t \right)} = c t$ | **Dynamic Causal Horizon Radius** | `coordinate_time_t` | Paper 1.1 Sec. II; Paper 1.4 Sec. II |
| $H{\left(t \right)} = \frac{1}{t}$ | **Dynamic Expansion Rate (Temporal)** | `coordinate_time_t` | Paper 1.1 Sec. II; Paper 1.2 Sec. III |
| $H{\left(R \right)} = \frac{c}{R}$ | **Dynamic Expansion Rate (Geometric)** | `spatial_horizon_radius_R` | Paper 1.1 Sec. II |
| $a_{c}{\left(t \right)} = \frac{c n}{t}$ | **Dynamic Critical Acceleration Scale (Temporal)** | `coordinate_time_t` | Paper 1.1 Sec. II; Paper 1.3 Sec. II; Paper 2.1 Sec. III |
| $a_{c}{\left(R \right)} = \frac{c^{2} n}{R}$ | **Dynamic Critical Acceleration Scale (Geometric)** | `spatial_horizon_radius_R` | Paper 1.1 Sec. II; Paper 2.5 Sec. II |
| $\eta{\left(t \right)} = \left(\frac{t}{t_{\text{ref}}}\right)^{\frac{n}{2}}$ | **Dynamic Metric Clock Lapse** | `proper_worldline_tau_to_coordinate_t` | Paper 1.1 Sec. II; Paper 1.2 Sec. II; Paper 1.6 Sec. II |
| $\mathrm{d}\tau = \eta_{\text{dyn}} \mathrm{d}t$ | **Worldline Proper-Time Metric Relation** | `worldline_differential` | Paper 1.2 Sec. II; Paper 1.3 Sec. II |
| $\frac{\mathrm{d}}{\mathrm{d}\tau} = \frac{\mathrm{d}}{\mathrm{d}t} \gamma_{\text{dyn}}$ | **Worldline Derivative Transformation Operator** | `operator_transformation` | Paper 1.3 Sec. II |
| $- a_{c} g_{N} - g_{N} g_{\text{eff}} + g_{\text{eff}}^{2} = 0$ | **Root Gravity Algebraic Constraint** | `algebraic_field_constraint` | Paper 1.1 Eq. (13); Paper 2.5 Eq. (2) |
| $g_{\text{eff}}{\left(g_{N},t \right)} = \frac{\sqrt{g_{N}} \sqrt{\frac{4 c n}{t} + g_{N}}}{2} + \frac{g_{N}}{2}$ | **Dynamic Non-Linear Root Gravity Solution** | `spatial_radius_r_and_time_t` | Paper 1.1 Eq. (14); Paper 2.2 Eq. (2); Paper 2.5 Eq. (3) |
| $\tau{\left(t,g_{N} \right)} = \frac{\sqrt{2} t e^{- \frac{\sqrt{2} g_{N} t}{2 c}}}{n}$ | **Dynamic Vacuum Relaxation Timescale** | `coordinate_time_t` | Paper 1.3 Sec. II; Paper 2.2 Eq. (4) |
| $\frac{\mathrm{d}\eta_{\text{dyn}}}{\mathrm{d}t} = - \frac{\eta_{\text{dyn}} - \sqrt{1 - \frac{v^{2}}{c^{2}}}}{\tau_{\text{eff}}}$ | **Dynamic Vacuum Relaxation ODE (Coordinate Frame)** | `coordinate_time_t` | Paper 1.3 Eq. (83); Paper 2.2 Sec. II |
| $\frac{\mathrm{d}\eta_{\text{dyn}}}{\mathrm{d}\tau} = - \frac{\gamma_{\text{dyn}} \left(\eta_{\text{dyn}} - \sqrt{1 - \frac{v^{2}}{c^{2}}}\right)}{\tau_{\text{eff}}}$ | **Dynamic Vacuum Relaxation ODE (Proper Worldline Frame)** | `proper_worldline_tau` | Paper 1.3 Sec. II |

### Dynamic Causal Horizon Radius
**Classification:** Tier 1: Dynamic Continuous Variable | **Frame:** `coordinate_time_t`

Continuous causal expansion horizon scale R(t) = c * t in metric coordinate time t.

$$R{\left(t \right)} = c t$$

* **Paper Citation & Reference:** Paper 1.1 Sec. II; Paper 1.4 Sec. II
* **SymPy Formulation:** `Eq(R(t), c*t)`

### Dynamic Expansion Rate (Temporal)
**Classification:** Tier 1: Dynamic Continuous Variable | **Frame:** `coordinate_time_t`

Continuous cosmological expansion rate H(t) = 1 / t as a function of metric time.

$$H{\left(t \right)} = \frac{1}{t}$$

* **Paper Citation & Reference:** Paper 1.1 Sec. II; Paper 1.2 Sec. III
* **SymPy Formulation:** `Eq(H(t), 1/t)`

### Dynamic Expansion Rate (Geometric)
**Classification:** Tier 1: Dynamic Continuous Variable | **Frame:** `spatial_horizon_radius_R`

Continuous expansion rate expressed in horizon radius H(R) = c / R.

$$H{\left(R \right)} = \frac{c}{R}$$

* **Paper Citation & Reference:** Paper 1.1 Sec. II
* **SymPy Formulation:** `Eq(H(R), c/R)`

### Dynamic Critical Acceleration Scale (Temporal)
**Classification:** Tier 1: Dynamic Continuous Variable | **Frame:** `coordinate_time_t`

Fundamental horizon acceleration scale in metric time: a_c(t) = (c * n) / t.

$$a_{c}{\left(t \right)} = \frac{c n}{t}$$

* **Paper Citation & Reference:** Paper 1.1 Sec. II; Paper 1.3 Sec. II; Paper 2.1 Sec. III
* **SymPy Formulation:** `Eq(a_c(t), c*n/t)`

### Dynamic Critical Acceleration Scale (Geometric)
**Classification:** Tier 1: Dynamic Continuous Variable | **Frame:** `spatial_horizon_radius_R`

Fundamental horizon acceleration scale in horizon radius: a_c(R) = (c^2 / R) * n.

$$a_{c}{\left(R \right)} = \frac{c^{2} n}{R}$$

* **Paper Citation & Reference:** Paper 1.1 Sec. II; Paper 2.5 Sec. II
* **SymPy Formulation:** `Eq(a_c(R), c**2*n/R)`

### Dynamic Metric Clock Lapse
**Classification:** Tier 1: Dynamic Continuous Variable | **Frame:** `proper_worldline_tau_to_coordinate_t`

Differential conversion rate between proper time tau and coordinate time t: eta(t) = (t / t_ref)^(n/2).

$$\eta{\left(t \right)} = \left(\frac{t}{t_{\text{ref}}}\right)^{\frac{n}{2}}$$

* **Paper Citation & Reference:** Paper 1.1 Sec. II; Paper 1.2 Sec. II; Paper 1.6 Sec. II
* **SymPy Formulation:** `Eq(\eta(t), (t/t_{\text{ref}})**(n/2))`

### Worldline Proper-Time Metric Relation
**Classification:** Tier 1: Dynamic Continuous Variable | **Frame:** `worldline_differential`

Exact relativistic line element differential connecting clock proper time tau to coordinate time t.

$$\mathrm{d}\tau = \eta_{\text{dyn}} \mathrm{d}t$$

* **Paper Citation & Reference:** Paper 1.2 Sec. II; Paper 1.3 Sec. II
* **SymPy Formulation:** `Eq(\mathrm{d}\tau, \eta_{\text{dyn}}*\mathrm{d}t)`

### Worldline Derivative Transformation Operator
**Classification:** Tier 1: Dynamic Continuous Variable | **Frame:** `operator_transformation`

Formal operator relation preventing derivative skew between proper time and coordinate time.

$$\frac{\mathrm{d}}{\mathrm{d}\tau} = \frac{\mathrm{d}}{\mathrm{d}t} \gamma_{\text{dyn}}$$

* **Paper Citation & Reference:** Paper 1.3 Sec. II
* **SymPy Formulation:** `Eq(\frac{\mathrm{d}}{\mathrm{d}\tau}, \frac{\mathrm{d}}{\mathrm{d}t}*\gamma_{\text{dyn}})`

### Root Gravity Algebraic Constraint
**Classification:** Tier 1: Dynamic Continuous Variable | **Frame:** `algebraic_field_constraint`

The fundamental quadratic field constraint g_eff^2 - g_N * g_eff - g_N * a_c = 0.

$$- a_{c} g_{N} - g_{N} g_{\text{eff}} + g_{\text{eff}}^{2} = 0$$

* **Paper Citation & Reference:** Paper 1.1 Eq. (13); Paper 2.5 Eq. (2)
* **SymPy Formulation:** `Eq(-a_c*g_N - g_N*g_{\text{eff}} + g_{\text{eff}}**2, 0)`

### Dynamic Non-Linear Root Gravity Solution
**Classification:** Tier 1: Dynamic Continuous Variable | **Frame:** `spatial_radius_r_and_time_t`

First-principles algebraic solution for effective acceleration at epoch t, derived from the quadratic constraint.

$$g_{\text{eff}}{\left(g_{N},t \right)} = \frac{\sqrt{g_{N}} \sqrt{\frac{4 c n}{t} + g_{N}}}{2} + \frac{g_{N}}{2}$$

* **Paper Citation & Reference:** Paper 1.1 Eq. (14); Paper 2.2 Eq. (2); Paper 2.5 Eq. (3)
* **SymPy Formulation:** `Eq(g_{\text{eff}}(g_N, t), sqrt(g_N)*sqrt(4*c*n/t + g_N)/2 + g_N/2)`

### Dynamic Vacuum Relaxation Timescale
**Classification:** Tier 1: Dynamic Continuous Variable | **Frame:** `coordinate_time_t`

Screened vacuum healing timescale tau(t, g_N) derived from base timescale, stiffness, and critical acceleration.

$$\tau{\left(t,g_{N} \right)} = \frac{\sqrt{2} t e^{- \frac{\sqrt{2} g_{N} t}{2 c}}}{n}$$

* **Paper Citation & Reference:** Paper 1.3 Sec. II; Paper 2.2 Eq. (4)
* **SymPy Formulation:** `Eq(\tau(t, g_N), sqrt(2)*t*exp(-sqrt(2)*g_N*t/(2*c))/n)`

### Dynamic Vacuum Relaxation ODE (Coordinate Frame)
**Classification:** Tier 1: Dynamic Continuous Variable | **Frame:** `coordinate_time_t`

Dissipation equation for dynamic metric lapse in observer laboratory frame coordinate time t.

$$\frac{\mathrm{d}\eta_{\text{dyn}}}{\mathrm{d}t} = - \frac{\eta_{\text{dyn}} - \sqrt{1 - \frac{v^{2}}{c^{2}}}}{\tau_{\text{eff}}}$$

* **Paper Citation & Reference:** Paper 1.3 Eq. (83); Paper 2.2 Sec. II
* **SymPy Formulation:** `Eq(\frac{\mathrm{d}\eta_{\text{dyn}}}{\mathrm{d}t}, -(\eta_{\text{dyn}} - sqrt(1 - v**2/c**2))/\tau_{\text{eff}})`

### Dynamic Vacuum Relaxation ODE (Proper Worldline Frame)
**Classification:** Tier 1: Dynamic Continuous Variable | **Frame:** `proper_worldline_tau`

Dissipation equation for dynamic metric lapse derived via worldline transformation operator d/d tau.

$$\frac{\mathrm{d}\eta_{\text{dyn}}}{\mathrm{d}\tau} = - \frac{\gamma_{\text{dyn}} \left(\eta_{\text{dyn}} - \sqrt{1 - \frac{v^{2}}{c^{2}}}\right)}{\tau_{\text{eff}}}$$

* **Paper Citation & Reference:** Paper 1.3 Sec. II
* **SymPy Formulation:** `Eq(\frac{\mathrm{d}\eta_{\text{dyn}}}{\mathrm{d}\tau}, -\gamma_{\text{dyn}}*(\eta_{\text{dyn}} - sqrt(1 - v**2/c**2))/\tau_{\text{eff}})`

---

## Tier 2: Present-Epoch Boundary Evaluations ($t \to t_0, R \to R_0$)

Subscript-0 parameters are **not starting assumptions**. They are derived boundary evaluations obtained by evaluating the continuous Tier 1 equations at the present cosmological epoch $t = t_0$ (corresponding to horizon scale $R_0 = c \cdot t_0$).

| Equation | Name | Derivative Frame | Paper Cross-Reference |
| :--- | :--- | :--- | :--- |
| $H_{0} = \frac{1}{t_{0}}$ | **Present Hubble Rate Boundary Evaluation** | `epoch_boundary_evaluation` | Paper 1.1 Sec. II; Paper 2.3 Sec. II |
| $R_{0} = \frac{c}{H_{0}}$ | **Present Causal Horizon Scale** | `epoch_boundary_evaluation` | Paper 1.1 Sec. II |
| $a_{0} = H_{0} c n$ | **Present Critical Acceleration Scale** | `epoch_boundary_evaluation` | Paper 1.1 Sec. II; Paper 2.5 Sec. II |
| $\tau_{0} = \frac{\sqrt{2} t_{0}}{n}$ | **Present Unscreened Relaxation Timescale** | `epoch_boundary_evaluation` | Paper 2.2 Sec. II |

### Present Hubble Rate Boundary Evaluation
**Classification:** Tier 2: Present-Epoch Boundary Evaluation | **Frame:** `epoch_boundary_evaluation`

Boundary evaluation of continuous H(t) at present cosmological observation epoch t = t_0: H_0 = 1 / t_0.

$$H_{0} = \frac{1}{t_{0}}$$

* **Paper Citation & Reference:** Paper 1.1 Sec. II; Paper 2.3 Sec. II
* **SymPy Formulation:** `Eq(H_0, 1/t_0)`

### Present Causal Horizon Scale
**Classification:** Tier 2: Present-Epoch Boundary Evaluation | **Frame:** `epoch_boundary_evaluation`

Boundary evaluation of continuous R(t) at present epoch: R_0 = c * t_0 = c / H_0.

$$R_{0} = \frac{c}{H_{0}}$$

* **Paper Citation & Reference:** Paper 1.1 Sec. II
* **SymPy Formulation:** `Eq(R_0, c/H_0)`

### Present Critical Acceleration Scale
**Classification:** Tier 2: Present-Epoch Boundary Evaluation | **Frame:** `epoch_boundary_evaluation`

Boundary evaluation of continuous a_c(t) at present epoch: a_0 = c * H_0 * n.

$$a_{0} = H_{0} c n$$

* **Paper Citation & Reference:** Paper 1.1 Sec. II; Paper 2.5 Sec. II
* **SymPy Formulation:** `Eq(a_0, H_0*c*n)`

### Present Unscreened Relaxation Timescale
**Classification:** Tier 2: Present-Epoch Boundary Evaluation | **Frame:** `epoch_boundary_evaluation`

Boundary evaluation of continuous unscreened vacuum memory timescale tau(t_0, 0) at present epoch.

$$\tau_{0} = \frac{\sqrt{2} t_{0}}{n}$$

* **Paper Citation & Reference:** Paper 2.2 Sec. II
* **SymPy Formulation:** `Eq(\tau_0, sqrt(2)*t_0/n)`

---

## Tier 3: Geometric First-Principles Derivations ($n = \frac{3}{4\pi}$)

Chronodynamic Relativity contains zero manual tunable exponents. The dilution exponent $n$ and dynamic relaxation stiffness $k$ are derived analytically from 3D Euclidean spatial geometry and spherical horizon topology.

| Equation | Name | Derivative Frame | Paper Cross-Reference |
| :--- | :--- | :--- | :--- |
| $n = \frac{3}{4 \pi}$ | **Geometric Dilution Exponent Derivation** | `geometric_invariant` | Paper 1.1 Sec. I; Paper 2.3 Sec. II |
| $k = \frac{3 \sqrt{2}}{8 \pi}$ | **Geometric Relaxation Stiffness Factor** | `geometric_invariant` | Paper 2.2 Sec. II |

### Geometric Dilution Exponent Derivation
**Classification:** Tier 3: Geometric First-Principles Derivation | **Frame:** `geometric_invariant`

Analytic derivation of n from the dimensional ratio of 3D Euclidean volume to 2D spherical horizon: n = 3 / (4 * pi).

$$n = \frac{3}{4 \pi}$$

* **Paper Citation & Reference:** Paper 1.1 Sec. I; Paper 2.3 Sec. II
* **SymPy Formulation:** `Eq(n, 3/(4*pi))`

### Geometric Relaxation Stiffness Factor
**Classification:** Tier 3: Geometric First-Principles Derivation | **Frame:** `geometric_invariant`

Analytic derivation of dynamic relaxation stiffness: k = n / sqrt(2) = 3 / (4 * pi * sqrt(2)).

$$k = \frac{3 \sqrt{2}}{8 \pi}$$

* **Paper Citation & Reference:** Paper 2.2 Sec. II
* **SymPy Formulation:** `Eq(k, 3*sqrt(2)/(8*pi))`

---

## Tier 4: Derived Zero-Parameter Observables & Asymptotic Limits

By substituting the Tier 3 geometric invariants into the Tier 1 and Tier 2 relations, the framework yields certified, zero-parameter closed-form expressions for all astrophysical and cosmological observables across the 11 manuscripts.

| Equation | Name | Derivative Frame | Paper Cross-Reference |
| :--- | :--- | :--- | :--- |
| $a_{0} = \frac{3 H_{0} c}{4 \pi}$ | **Zero-Parameter Boundary Acceleration Scale** | `dimensionless_geometric_evaluation` | Paper 1.1 Eq. (4); Paper 2.5 Eq. (2) |
| $\tau_{0} = \frac{4 \sqrt{2} \pi}{3 H_{0}}$ | **Zero-Parameter Base Relaxation Timescale** | `dimensionless_geometric_evaluation` | Paper 2.2 Eq. (3) |
| $a_{c}{\left(z \right)} = a_{0} \left(z + 1\right)^{\frac{3}{2 \pi}}$ | **Zero-Parameter Redshift Critical Acceleration** | `cosmological_redshift_z` | Paper 1.1 Sec. II; Paper 2.1 Sec. III |
| $g_{\text{eff, high}} = - \frac{a_{0}^{2}}{g_{N}} + a_{0} + g_{N}$ | **Asymptotic Keplerian Screening Series** | `asymptotic_series_expansion` | Paper 1.1 Sec. II; Paper 2.5 Sec. II |
| $g_{\text{eff, low}} = \sqrt{a_{0}} \sqrt{g_{N}} + \frac{g_{N}}{2}$ | **Asymptotic Deep-Field MOND Limit** | `asymptotic_series_expansion` | Paper 1.1 Sec. II; Paper 2.5 Sec. II |
| $v_{\text{flat}}^{4} = \frac{3 G H_{0} M c}{4 \pi}$ | **Baryonic Tully-Fisher Relation** | `galactic_kinematics` | Paper 1.1 Eq. (16); Paper 2.5 Sec. III |
| $D_{C}{\left(z \right)} = \frac{c \log{\left(z + 1 \right)}}{H_{0}}$ | **Cosmological Comoving Distance** | `cosmological_redshift_z` | Paper 1.1 Eq. (6); Paper 2.3 Eq. (2) |
| $d_{L}{\left(z \right)} = \frac{c \left(z + 1\right) \left(z + 1\right)^{\frac{3}{8 \pi}} \log{\left(z + 1 \right)}}{H_{0}}$ | **Zero-Parameter Luminosity Distance** | `cosmological_redshift_z` | Paper 1.1 Eq. (8); Paper 2.3 Eq. (4) |
| $\mu{\left(z \right)} = \frac{5 \log{\left(d_{L}{\left(z \right)} \right)}}{\log{\left(10 \right)}} + 25$ | **Zero-Parameter Distance Modulus** | `cosmological_redshift_z` | Paper 1.1 Eq. (9); Paper 2.3 Eq. (5) |
| $\Delta t_{\text{obs}} = \frac{\Delta t_{\text{emit}} \left(z + 1\right)}{\left(z + 1\right)^{\frac{3}{8 \pi}}}$ | **Supernova Duration Redshift Stretching** | `cosmological_redshift_z` | Paper 1.1 Eq. (10); Paper 1.2 Sec. III; Paper 2.3 Sec. III |
| $\Delta r = \tau_{\text{eff}} v_{\text{rel}} \left(1 - e^{- \frac{t_{\text{stop}}}{\tau_{\text{eff}}}}\right)$ | **Cluster Decoupling Displacement Offset** | `kinematic_offset` | Paper 2.2 Eq. (5) |
| $\gamma_{\text{wb}} = \sqrt{\frac{\sqrt{\frac{3 H_{0} c}{\pi g_{N}} + 1}}{2} + \frac{1}{2}}$ | **Zero-Parameter Wide Binary Velocity Boost** | `binary_kinematics` | Paper 2.5 Eq. (6) |

### Zero-Parameter Boundary Acceleration Scale
**Classification:** Tier 4: Derived Zero-Parameter Observable | **Frame:** `dimensionless_geometric_evaluation`

Derived by substituting n = 3 / (4*pi) into epoch acceleration: a_0 = (3 * c * H_0) / (4 * pi).

$$a_{0} = \frac{3 H_{0} c}{4 \pi}$$

* **Paper Citation & Reference:** Paper 1.1 Eq. (4); Paper 2.5 Eq. (2)
* **SymPy Formulation:** `Eq(a_0, 3*H_0*c/(4*pi))`

### Zero-Parameter Base Relaxation Timescale
**Classification:** Tier 4: Derived Zero-Parameter Observable | **Frame:** `dimensionless_geometric_evaluation`

Derived by substituting n = 3 / (4*pi) into epoch relaxation: tau_0 = (4 * pi * sqrt(2)) / (3 * H_0).

$$\tau_{0} = \frac{4 \sqrt{2} \pi}{3 H_{0}}$$

* **Paper Citation & Reference:** Paper 2.2 Eq. (3)
* **SymPy Formulation:** `Eq(\tau_0, 4*sqrt(2)*pi/(3*H_0))`

### Zero-Parameter Redshift Critical Acceleration
**Classification:** Tier 4: Derived Zero-Parameter Observable | **Frame:** `cosmological_redshift_z`

Derived by substituting n = 3 / (4*pi) into redshift-scaled critical acceleration: a_c(z) = a_0 * (1+z)^(3 / (2*pi)).

$$a_{c}{\left(z \right)} = a_{0} \left(z + 1\right)^{\frac{3}{2 \pi}}$$

* **Paper Citation & Reference:** Paper 1.1 Sec. II; Paper 2.1 Sec. III
* **SymPy Formulation:** `Eq(a_c(z), a_0*(z + 1)**(3/(2*pi)))`

### Asymptotic Keplerian Screening Series
**Classification:** Tier 4: Derived Zero-Parameter Observable | **Frame:** `asymptotic_series_expansion`

Taylor series expansion of root gravity in high-acceleration regime (g_N >> a_0), recovering standard General Relativity.

$$g_{\text{eff, high}} = - \frac{a_{0}^{2}}{g_{N}} + a_{0} + g_{N}$$

* **Paper Citation & Reference:** Paper 1.1 Sec. II; Paper 2.5 Sec. II
* **SymPy Formulation:** `Eq(g_{\text{eff, high}}, -a_0**2/g_N + a_0 + g_N)`

### Asymptotic Deep-Field MOND Limit
**Classification:** Tier 4: Derived Zero-Parameter Observable | **Frame:** `asymptotic_series_expansion`

Puiseux series expansion of root gravity in low-acceleration regime (g_N << a_0), yielding deep MOND scaling.

$$g_{\text{eff, low}} = \sqrt{a_{0}} \sqrt{g_{N}} + \frac{g_{N}}{2}$$

* **Paper Citation & Reference:** Paper 1.1 Sec. II; Paper 2.5 Sec. II
* **SymPy Formulation:** `Eq(g_{\text{eff, low}}, sqrt(a_0)*sqrt(g_N) + g_N/2)`

### Baryonic Tully-Fisher Relation
**Classification:** Tier 4: Derived Zero-Parameter Observable | **Frame:** `galactic_kinematics`

Zero-parameter analytical proof of the flat rotation curve relation v^4 = G * M * a_0.

$$v_{\text{flat}}^{4} = \frac{3 G H_{0} M c}{4 \pi}$$

* **Paper Citation & Reference:** Paper 1.1 Eq. (16); Paper 2.5 Sec. III
* **SymPy Formulation:** `Eq(v_{\text{flat}}**4, 3*G*H_0*M*c/(4*pi))`

### Cosmological Comoving Distance
**Classification:** Tier 4: Derived Zero-Parameter Observable | **Frame:** `cosmological_redshift_z`

Exact first-principles integral of coordinate distance: D_C(z) = (c / H_0) * ln(1+z).

$$D_{C}{\left(z \right)} = \frac{c \log{\left(z + 1 \right)}}{H_{0}}$$

* **Paper Citation & Reference:** Paper 1.1 Eq. (6); Paper 2.3 Eq. (2)
* **SymPy Formulation:** `Eq(D_C(z), c*log(z + 1)/H_0)`

### Zero-Parameter Luminosity Distance
**Classification:** Tier 4: Derived Zero-Parameter Observable | **Frame:** `cosmological_redshift_z`

Derived by substituting n = 3 / (4*pi) into parametric luminosity distance: d_L(z) = (c / H_0) * (1+z)^(1 + 3/(8*pi)) * ln(1+z).

$$d_{L}{\left(z \right)} = \frac{c \left(z + 1\right) \left(z + 1\right)^{\frac{3}{8 \pi}} \log{\left(z + 1 \right)}}{H_{0}}$$

* **Paper Citation & Reference:** Paper 1.1 Eq. (8); Paper 2.3 Eq. (4)
* **SymPy Formulation:** `Eq(d_L(z), c*(z + 1)*(z + 1)**(3/(8*pi))*log(z + 1)/H_0)`

### Zero-Parameter Distance Modulus
**Classification:** Tier 4: Derived Zero-Parameter Observable | **Frame:** `cosmological_redshift_z`

Hubble diagram distance modulus mu(z) evaluated from zero-parameter luminosity distance.

$$\mu{\left(z \right)} = \frac{5 \log{\left(d_{L}{\left(z \right)} \right)}}{\log{\left(10 \right)}} + 25$$

* **Paper Citation & Reference:** Paper 1.1 Eq. (9); Paper 2.3 Eq. (5)
* **SymPy Formulation:** `Eq(\mu(z), 5*log(d_L(z))/log(10) + 25)`

### Supernova Duration Redshift Stretching
**Classification:** Tier 4: Derived Zero-Parameter Observable | **Frame:** `cosmological_redshift_z`

Derived by substituting n = 3 / (4*pi) into light-curve duration stretching: Delta t_obs = Delta t_emit * (1+z)^(1 - 3/(8*pi)).

$$\Delta t_{\text{obs}} = \frac{\Delta t_{\text{emit}} \left(z + 1\right)}{\left(z + 1\right)^{\frac{3}{8 \pi}}}$$

* **Paper Citation & Reference:** Paper 1.1 Eq. (10); Paper 1.2 Sec. III; Paper 2.3 Sec. III
* **SymPy Formulation:** `Eq(\Delta t_{\text{obs}}, \Delta t_{\text{emit}}*(z + 1)/(z + 1)**(3/(8*pi)))`

### Cluster Decoupling Displacement Offset
**Classification:** Tier 4: Derived Zero-Parameter Observable | **Frame:** `kinematic_offset`

Kinematic lag offset Delta r for colliding cluster mergers under screened vacuum relaxation.

$$\Delta r = \tau_{\text{eff}} v_{\text{rel}} \left(1 - e^{- \frac{t_{\text{stop}}}{\tau_{\text{eff}}}}\right)$$

* **Paper Citation & Reference:** Paper 2.2 Eq. (5)
* **SymPy Formulation:** `Eq(\Delta r, \tau_{\text{eff}}*v_{\text{rel}}*(1 - exp(-t_{\text{stop}}/\tau_{\text{eff}})))`

### Zero-Parameter Wide Binary Velocity Boost
**Classification:** Tier 4: Derived Zero-Parameter Observable | **Frame:** `binary_kinematics`

Orbital velocity boost ratio gamma = v_rel / v_N derived from root gravity with zero-parameter acceleration scale a_0.

$$\gamma_{\text{wb}} = \sqrt{\frac{\sqrt{\frac{3 H_{0} c}{\pi g_{N}} + 1}}{2} + \frac{1}{2}}$$

* **Paper Citation & Reference:** Paper 2.5 Eq. (6)
* **SymPy Formulation:** `Eq(\gamma_{\text{wb}}, sqrt(sqrt(3*H_0*c/(pi*g_N) + 1)/2 + 1/2))`

---

## Verification & Reproducibility

All equations cataloged above are validated automatically by the test suite [`official/tests/test_symbolic_engine.py`](../tests/test_symbolic_engine.py):
1. **Continuity & Limit Verification:** Exact algebraic verification of asymptotic limits ($g_N \gg a_0 \implies g_{\text{eff}} \to g_N + a_0$; $g_N \ll a_0 \implies g_{\text{eff}} \to \sqrt{g_N a_0}$).
2. **Tully-Fisher Invariance:** Exact verification that the velocity exponent $\mathrm{d}\ln v / \mathrm{d}\ln M = 1/4$ holds identically.
3. **Numerical Precision:** Floating-point evaluation of lambdified symbolic formulas matches the numerical `ChronodynamicModel` to within $< 10^{-12}$.
4. **Export Automation:** The catalog can be regenerated at any time via `python scripts/export_symbolic_mathjax.py`.
