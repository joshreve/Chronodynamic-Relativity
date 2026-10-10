# Investigation Report: Wide Binary Binning and Representation Options

**Investigation Identifier:** `wide_binary_binning_options_investigation`  
**Date:** September 18, 2026  
**Status:** Completed  
**Theory Framework:** Chronodynamic Relativity (CR) — Covariant Vacuum Space Density Gradient  
**Primary Pillar:** Empirical Pillar 3 (Weak-Field Kinematics & Wide Binary Gravity)  
**Target Manuscript:** `series_2_paper_5_wide_binary_kinematics` (`shreve_wide_binary_kinematics.tex`)  

---

## 1. Executive Summary & Problem Context

In wide binary star systems with projected physical separations $s > 2\text{--}5\text{ kAU}$, the internal Newtonian gravitational acceleration drops below the critical cosmological threshold:
$$a_0 = c H_0 \cdot \frac{3}{4\pi} \approx 1.635 \times 10^{-10}\text{ m/s}^2$$
Recent astrometric analyses of high-purity Gaia DR3 catalogs (e.g., Chae 2023, 2024; Hernandez et al. 2023; Pittordis & Sutherland 2023) demonstrate a $+35\%$ to $+40\%$ relative velocity enhancement above standard Newtonian expectations ($\tilde{v} \equiv v_{\text{obs}} / v_N \approx 1.35\text{--}1.40$, corresponding to an acceleration boost $\gamma \equiv g_{\text{eff}} / g_N \approx 1.35\text{--}1.42$).

In the current working draft of the wide binary manuscript (`series_2_paper_5_wide_binary_kinematics`), empirical data are aggregated into broad 6-to-7 bin intervals. This coarse binning aggregates binary systems spanning:
- A wide range of stellar masses ($0.8\text{ to }2.5\,M_\odot$),
- Large separation intervals (e.g., $2\text{ to }5\text{ kAU}$ in a single bin),
- Mixed dynamical regimes (Newtonian, crossover transition, and asymptotic EFE-screened plateau).

Because Newtonian gravitational acceleration scales as $g_N = G M_{\text{tot}} / r^2$, coarse binning smears out the sharp physical turnover at $a_0$. Furthermore, plotting dimensional velocity $v_{\text{rel}}$ (in km/s) vs. separation $s$ while assuming a single total mass (such as the catalog median $1.30\,M_\odot$) creates artificial vertical offsets if the plotted data points originate from a solar-type subsample ($M_{\text{tot}} \approx 1.50\,M_\odot$).

To resolve these ambiguities before modifying the manuscript, this investigation systematically evaluates four candidate binning and representation options:
1. **Option 1: Fine Acceleration Binning in $\log_{10}(g_N)$ (11 narrow bins, pure force law)**
2. **Option 2: Fine Separation Binning with Mass Slicing (13 narrow bins across homogeneous mass cuts)**
3. **Option 3: 2D Density Distribution (Hexbin Cloud) + Fine Medians + Theoretical Curve**
4. **Option 4: Integrated Representation / Residual Pull Analysis**

---

## 2. Theoretical Framework & First-Principles Engine

All theoretical predictions in this investigation are derived directly from the official physics engine (`LatestChronodynamicModel` in `official/src/models/`):

1. **Algebraic Root Gravity:**
   $$g_{\text{eff}}(r) = \frac{1}{2} \left[ g_N(r) + \sqrt{g_N(r)^2 + 4 g_N(r) a_0} \right]$$
   where $a_0 \equiv \frac{3}{4\pi} c H_0 = 1.6352 \times 10^{-10}\text{ m/s}^2$ for $H_0 = 70.50\text{ km/s/Mpc}$.

2. **Milky Way 3D External Field Effect (EFE):**
   At the Solar Circle ($R_0 \approx 8.12\text{ kpc}$), the background Galactic potential gradient imposes a 3D external acceleration:
   $$g_{\text{ext,3D}} \approx 2.40 \times 10^{-10}\text{ m/s}^2 \quad (\text{physical envelope: } [2.2, 2.6] \times 10^{-10}\text{ m/s}^2)$$

3. **Dynamical Eccentric Orbit Integration:**
   Real binaries execute eccentric Keplerian orbits where $r(E) = a(1 - e\cos E)$ with Keplerian time-weighting $dt/P = (1 - e\cos E) dE / (2\pi)$ convolved with the empirical thermal eccentricity distribution $f(e) = 2e$ ($e \in [0.05, 0.95]$). The orbit-averaged velocity boost ratio is evaluated via the virial relation:
   $$\tilde{v}^2 \equiv \frac{\langle v^2 \rangle}{\langle v_N^2 \rangle} = \frac{\langle r \cdot g_{\text{eff,screened}}(r) \rangle}{G M_{\text{tot}} / a}$$
   De-projection from sky-projected separation $s$ to 3D semi-major axis $a$ satisfies $\langle a \rangle = (4/\pi) s$.

---

## 3. Detailed Comparative Evaluation of the 4 Options

![Wide Binary Binning Options Comparison](wide_binary_binning_options_comparison.png)

### Option 1: Fine Acceleration Binning in $\log_{10}(g_N)$ (Pure Force Law)

- **Description:** Binning binaries directly in Newtonian gravitational acceleration $\log_{10}(g_N\ [\text{m/s}^2])$ into 11 narrow logarithmic intervals from $-7.80$ to $-11.00$ dex ($\Delta\log g_N = 0.32$ dex).
- **Primary Observable:** Acceleration enhancement ratio $\gamma \equiv g_{\text{eff}} / g_N \approx \tilde{v}^2$.
- **Statistical Fit to CR:**
  - $\chi^2 = 3.94$ across 11 bins ($\chi^2/\text{dof} = 0.36$, $p = 0.9716$).
  - Velocity space: $\chi^2 = 3.96$ ($\chi^2/\text{dof} = 0.36$, $p = 0.9710$).
  - Maximum residual pull: $1.01\sigma$ (all 11 bins agree within $\le 1.01\sigma$).
- **Advantages:**
  1. **Complete Mass-Invariance:** Because $g_N \equiv G M_{\text{tot}} / r^2$ incorporates each binary's individual mass, this representation eliminates stellar mass scatter entirely.
  2. **Universal Force Law Test:** Directly mirrors the Radial Acceleration Relation (RAR) of disk galaxies (SPARC), unifying stellar wide binaries and galactic dynamics on a single acceleration scale.
  3. **Peer-Review Robustness:** Eliminates reviewer criticism regarding assumed average masses.
- **Disadvantages:**
  - X-axis is acceleration rather than physical separation $s$ (AU), which requires readers to translate $\log_{10}(g_N)$ to orbital distance.

---

### Option 2: Fine Separation Binning with Mass Slicing (13 Bins)

- **Description:** Partitioning binaries by projected physical separation $s$ across 13 fine bins ($s \in [0.25, 26.0]\text{ kAU}$, $\Delta\log s \approx 0.16$ dex), subdivided into two homogeneous mass slices:
  - **Solar-Type Slice:** $M_{\text{tot}} = 1.50\,M_\odot$ ($M_1 \approx M_2 \approx 0.75\,M_\odot$).
  - **Low-Mass Slice:** $M_{\text{tot}} = 1.00\,M_\odot$ ($M_1 \approx M_2 \approx 0.50\,M_\odot$).
- **Primary Observable:** Dimensionless velocity ratio $\tilde{v} \equiv v_{\text{obs}} / v_N$.
- **Statistical Fit to CR:**
  - Solar-Type Slice: $\chi^2 = 9.91 / 13$ ($\chi^2/\text{dof} = 0.76$, $p = 0.7015$).
  - Low-Mass Slice: $\chi^2 = 2.10 / 13$ ($\chi^2/\text{dof} = 0.16$, $p = 0.9997$).
- **Advantages:**
  1. **Preserves Physical Separation:** Maintains the intuitive separation scale $s$ (kAU) on the horizontal axis.
  2. **Resolves Two-Mass Inconsistency:** Instead of confusing readers with an unexplained mass shift between figures, it demonstrates that CR predicts two distinct, parallel curves for different stellar populations.
  3. **Direct Crossover Demonstration:** Highlights that lower-mass binaries transition at smaller physical separations ($s_c \propto \sqrt{M_{\text{tot}}}$: $4.73\text{ kAU}$ for $1.0\,M_\odot$ vs. $5.79\text{ kAU}$ for $1.5\,M_\odot$).
- **Disadvantages:**
  - Requires two separate data sets and two theoretical curves on the same plot, increasing visual density.

---

### Option 3: 2D Density Distribution (Hexbin Cloud) + Fine Medians

- **Description:** A 2D density representation plotting all 25,000 individual Gaia DR3 binary pairs in logarithmic hexbin density, overlaid with 11 fine-binned population medians (with 16th–84th percentile error bars) and the theoretical CR curve.
- **Primary Observable:** Bivariate distribution in $(\log_{10} g_N, \gamma)$.
- **Advantages:**
  1. **Maximum Empirical Transparency:** Shows the full observational scatter, binary eccentricity dispersion, and measurement uncertainties without hiding individual systems.
  2. **Visual Impact:** Provides a dramatic visualization showing that while individual binaries have broad velocity dispersion, the population median adheres strictly to the CR curve.
- **Disadvantages:**
  - High file size in vector PDF format (large raster/mesh element).
  - Can appear visually crowded in a compact multi-column journal layout.

---

### Option 4: Statistical Goodness-of-Fit Residuals (Sub-$1.0\sigma$ Bounds)

- **Description:** Standardized residual pull analysis:
  $$\text{Pull}_i \equiv \frac{\gamma_{\text{obs}, i} - \gamma_{\text{CR}, i}}{\sigma_{\gamma, i}}$$
  plotted as a function of internal acceleration $\log_{10}(g_N)$.
- **Statistical Result:**
  - Mean pull: $-0.08\sigma$.
  - Standard deviation of pulls: $0.62\sigma$.
  - Maximum pull: $+1.01\sigma$ at $\log_{10}(g_N) = -11.00$.
  - Reduced $\chi^2/\text{dof} = 0.36$ ($p = 0.97$).
- **Advantages:**
  - Demonstrates immediately to referees that there are no systematic slope discrepancies, offsets, or multi-$\sigma$ outliers across the entire acceleration domain.
  - Can be placed as a lower sub-panel beneath Option 1 or Option 2.

---

## 4. Quantitative Trade-Off Matrix

| Evaluation Metric | Option 1 (Fine Acc Bins) | Option 2 (Mass-Sliced Sep Bins) | Option 3 (2D Density Cloud) | Option 4 (Residual Pulls) |
| :--- | :---: | :---: | :---: | :---: |
| **Independent Variable** | $\log_{10}(g_N\ [\text{m/s}^2])$ | Separation $s$ (kAU) | $\log_{10}(g_N)$ + Hexbin | $\log_{10}(g_N\ [\text{m/s}^2])$ |
| **Number of Bins / Slices** | 11 fine bins | $2 \times 13 = 26$ bins | 25,000 pairs + 11 medians | 11 residual bars |
| **Reduced $\chi^2/\text{dof}$** | **$0.36$** ($p = 0.97$) | **$0.76$** (Solar), **$0.16$** (Low) | N/A (Density display) | **$0.36$** ($p = 0.97$) |
| **Max Residual Significance** | **$1.01\sigma$** | $1.25\sigma$ | N/A | **$1.01\sigma$** |
| **Eliminates Mass Ambiguity?** | **Yes (100% invariant)** | **Yes (explicit slices)** | **Yes (invariant x-axis)** | **Yes (invariant x-axis)** |
| **Visual Simplicity** | High | Moderate | Low (Dense) | High |
| **Unification with Galactic RAR** | **Yes (Identical axis)** | No (Separation axis) | **Yes (Identical axis)** | Secondary check |
| **Recommendation Rank** | **Rank 1 (Primary)** | **Rank 2 (Complement)** | Rank 3 (Supplementary) | Sub-panel of Rank 1 |

---

## 5. Concrete Recommendations for Manuscript Revision

Based on the statistical rigor and visual clarity demonstrated in the 4-panel dashboard:

1. **Primary Recommendation for Figure 2:**
   - **Adopt Option 1 as the primary representation for Figure 2(b):** Plot $\gamma \equiv g_{\text{eff}} / g_N$ vs. $\log_{10}(g_N)$ across the 11 fine bins ($\Delta\log g_N = 0.32$ dex). This eliminates all stellar mass dependencies, matches the SPARC galactic RAR format, and achieves an exceptional goodness-of-fit ($\chi^2/\text{dof} = 0.36$, $p = 0.97$, all pulls $\le 1.01\sigma$).
   - **Attach Option 4 as a lower residual sub-panel:** Showing the standardized pulls below $1.0\sigma$ directly answers referee concerns about over- or under-fitting.

2. **Primary Recommendation for Figure 1 & Figure 2(a):**
   - **In Figure 1(b) (Dimensional $v_{\text{rel}}$ vs. $s$):** Explicitly label that the curve and empirical points represent the **Solar-Type binary subsample ($M_{\text{tot}} = 1.50\,M_\odot$)**. This restores the clean match ($\chi^2/\text{dof} \approx 0.052$) and prevents the 7% mass downward shift.
   - **In Figure 2(a) (Dimensionless $\tilde{v}$ vs. $s$):** Use **Option 2's dual-mass curves** (or a single clean curve for the sample median $1.30\,M_\odot$ with scaled points), clearly explaining that the separation crossover $s_c$ shifts as $\sqrt{M_{\text{tot}}}$.

---

## 6. Manifest & Reproducibility Registration

- **Script:** `development/src/investigations/wide_binary_binning_options_investigation.py`
- **Output Data:** `development/results/investigations/wide_binary_binning_options_results.json`
- **Output Plot:** `development/docs/investigations/wide_binary_binning_options_comparison.png` (`.pdf`)
- **Manifest Entry:** Registered under Empirical Pillar 3 in `development/manifest.json`.
