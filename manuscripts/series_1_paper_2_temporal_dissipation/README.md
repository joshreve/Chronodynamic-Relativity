# Series 1, Paper 2: Thermodynamic Arrow of Time & Relational Clocks
**The Thermodynamic Arrow of Time and Quantum Relational Clocks in Chronodynamic Relativity: Unifying Cosmic Expansion, Total Field Energy Dissipation, and the Dynamic Acceleration Horizon**

* **Status:** Certified Official Manuscript (Version 1.0.1)
* **Author:** Joshua A. Shreve ([ORCID: 0009-0000-5942-5351](https://orcid.org/0009-0000-5942-5351))
* **Target Journal:** *Physical Review D*

---

## Zenodo Deposit & Revision Metadata (v1.0.1)

* **Deposit Title:** The Thermodynamic Arrow of Time and Quantum Relational Clocks in Chronodynamic Relativity: Unifying Cosmic Expansion, Total Field Energy Dissipation, and the Dynamic Acceleration Horizon
* **Version:** `v1.0.1` (Preprint Revision)
* **Publication Date:** `2026-10-11`
* **Zenodo Record ID:** [`23149338`](https://zenodo.org/records/23149338)
* **Preprint DOI:** [`10.5281/zenodo.23149338`](https://doi.org/10.5281/zenodo.23149338)
* **Software Companion DOI:** [`10.5281/zenodo.22697449`](https://doi.org/10.5281/zenodo.22697449)
* **License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)
* **Metadata Schema File:** [`.zenodo.json`](.zenodo.json)
* **Revision Notes:** Certified RevTeX-4.2 publication candidate for Physical Review D; verified thermodynamic arrow and relational clock derivations; updated companion software framework to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449).

---

## Directory Contents & Provenance

* **[`shreve_temporal_dissipation.tex`](shreve_temporal_dissipation.tex):** Complete RevTeX-4.2 LaTeX source code covering the thermodynamic derivation of the arrow of time, Page-Wootters relational quantum clocks, and dynamic acceleration horizon crossover proofs.
* **[`paper_2_references.bib`](paper_2_references.bib):** BibTeX database with complete peer-reviewed citations.
* **[`shreve_temporal_dissipation.pdf`](shreve_temporal_dissipation.pdf):** Compiled 6-page publication PDF ready for journal review and preprint distribution.
* **[`figures/`](figures/):** Vector publication figures (`optical_lattice_clock_test.pdf`, `deep_space_and_wide_binary_tests.pdf`).
* **[`verify_calculations.py`](verify_calculations.py):** First-principles execution script validating all numerical values, crossover radii, and table outputs against canonical physics model classes (`src/models/`).
* **[`reference_calculations.json`](reference_calculations.json):** Machine-readable reference values generated directly by `verify_calculations.py`.

---

## How to Compile to PDF:

```bash
pdflatex shreve_temporal_dissipation.tex
bibtex shreve_temporal_dissipation
pdflatex shreve_temporal_dissipation.tex
pdflatex shreve_temporal_dissipation.tex
```

Or execute the repository-wide compilation tool:
```bash
python scripts/compile_all_manuscripts.py
```

---

## Key Scientific Highlights in the Manuscript:

1. **Thermodynamic Arrow of Time from Space Dilution:** Proves that cosmic space expansion represents an irreversible dilution of space density, generating a strictly monotonic cosmic entropy production rate $\sigma_{\text{cosmic}} > 0$.
2. **Page-Wootters Relational Quantum Clocks:** Shows that microscopic atomic transition frequencies scale with local field density $\omega_0(\rho_s) \propto \sqrt{\rho_s}$, deriving cosmological clock rate scaling $\eta(z) = (1+z)^{-n/2}$.
3. **Dynamic Acceleration Horizon:** Derives $a_c(t) = \frac{c}{4\pi} H(t) = 1.635 \times 10^{-10}\text{ m/s}^2$ as the exact boundary where local gravitational perturbation rates balance cosmic field dissipation ($\Gamma_{\text{local}} = \Gamma_{\text{cosmic}}$).
4. **Interplanetary Saddle Points & Wide Binaries:** Predicts anomalous non-Newtonian restoring acceleration at interplanetary Lagrange saddle points ($|\Delta x| \le 654\text{ m}$) and matches Gaia DR3 wide binary velocity plateaus ($\chi^2/\text{dof} = 0.64$).
