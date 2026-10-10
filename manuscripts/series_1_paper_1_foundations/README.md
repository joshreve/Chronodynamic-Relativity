# Series 1, Paper 1: Theoretical Foundations & Empirical Validation
**Chronodynamic Relativity: Unifying Cosmic Expansion, Galactic Dynamics, Gravitational Lensing, and CMB Acoustic Peaks from a Single Environmental Scalar Field**

* **Status:** Frozen Official Release Candidate (Version 1.1.0)
* **Author:** Joshua A. Shreve ([ORCID: 0009-0000-5942-5351](https://orcid.org/0009-0000-5942-5351))
* **Target Journal:** *Physical Review D* / *Monthly Notices of the Royal Astronomical Society (MNRAS)*
* **Zenodo Record ID:** [`22697885`](https://zenodo.org/records/22697885)
* **Zenodo Concept DOI (All Versions):** [`10.5281/zenodo.22697884`](https://doi.org/10.5281/zenodo.22697884)
* **Zenodo Version DOI (`v1.0.3`):** [`10.5281/zenodo.22697885`](https://doi.org/10.5281/zenodo.22697885)
* **Codebase & Framework DOI:** [`10.5281/zenodo.22697449`](https://doi.org/10.5281/zenodo.22697449)

---

## Directory Contents & Provenance

* **[`shreve_chronodynamic_relativity_foundations.tex`](shreve_chronodynamic_relativity_foundations.tex):** Complete RevTeX-4.2 LaTeX source code covering all theoretical derivations, conformal gauge duality proofs, and empirical benchmark tables.
* **[`references.bib`](references.bib):** BibTeX database with complete citations for Planck 2018 PR3, DESI 2024 DR1, Pantheon+ Supernovae, SPARC Galaxies, the Bullet Cluster, GW170817, and Quantum COW Interferometry.
* **[`shreve_chronodynamic_relativity_foundations.pdf`](shreve_chronodynamic_relativity_foundations.pdf):** Compiled 10-page publication PDF ready for journal review and preprint distribution.
* **[`generate_foundations_figures.py`](generate_foundations_figures.py):** Automated high-resolution vector figure generator producing all figures in [`figures/`](figures/).
* **[`verify_calculations.py`](verify_calculations.py):** First-principles execution script validating all numerical values, crossover radii, and table outputs against canonical physics model classes (`src/models/`).
* **[`reference_calculations.json`](reference_calculations.json):** Machine-readable reference values generated directly by `verify_calculations.py` for automated continuous integration.

---

## How to Compile to PDF:

```bash
pdflatex shreve_chronodynamic_relativity_foundations.tex
bibtex shreve_chronodynamic_relativity_foundations
pdflatex shreve_chronodynamic_relativity_foundations.tex
pdflatex shreve_chronodynamic_relativity_foundations.tex
```

Or execute the repository-wide compilation tool:
```bash
python scripts/compile_all_manuscripts.py
```

---

## Key Scientific Highlights in the Manuscript:

1. **Conformal Gauge Duality & Proper Time Invariance:** Proves exact mathematical equivalence between the cosmic scale expansion metric and the variable-lapse metric time dual.
2. **Cosmic Expansion & Hubble Tension Resolution:** Evaluates 1,701 Pantheon+ Supernovae across 4 processing tiers, matching data with $\Delta\mu_{\text{RMS}} = 0.138\text{ mag}$ ($\chi^2/\text{dof} = 0.985$) under linear physical expansion $R(t) \propto t$.
3. **Galactic Dynamics across 175 SPARC Galaxies:** Derives the Radial Acceleration Relation (RAR) and flat rotation curves via the non-linear algebraic root law $g_{\text{eff}} = \frac{1}{2}\left[g_N + \sqrt{g_N^2 + 4 g_N a_c}\right]$ with $a_c(t) = \frac{c}{4\pi} H(t) = 1.635 \times 10^{-10}\text{ m/s}^2$.
4. **Gravitational Lensing & Cluster Deflection:** Predicts the exact factor-of-two optical metric deflection, matching the Einstein radii of the Bullet Cluster ($\theta_E = 31.4''$) and El Gordo ($\theta_E = 38.6''$).
5. **Planck 2018 CMB Acoustic Peaks:** Evaluates the acoustic scale multipole $\ell_A = 301.4$ from first principles, matching Planck 2018 ($\ell_A = 301.47 \pm 0.09$) via dynamic primordial membrane tension.
6. **DESI 2024 BAO Benchmark:** Matches transverse and radial BAO scales across all 7 redshift bins ($z=0.295 \to 2.330$) without dark energy parameters.
7. **Relativistic & Quantum Integrity:** Preserves $c_g = c$ (satisfying GW170817) and reproduces the Colella-Overhauser-Werner (COW) quantum gravitational phase shift.
