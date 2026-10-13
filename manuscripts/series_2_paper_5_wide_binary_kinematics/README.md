# Chronodynamic Relativity — Series 2, Paper 5: Gaia Wide Binary Kinematics

**Gaia DR3 wide binary star kinematics and the low-acceleration velocity plateau in Chronodynamic Relativity**

* **Status:** Official Submission Candidate (Version 1.0.1)
* **Author:** Joshua A. Shreve ([ORCID: 0009-0000-5942-5351](https://orcid.org/0009-0000-5942-5351))
* **Target Journal:** *Astronomy & Astrophysics* (A&A, S2O, 0 USD)

---

## Zenodo Deposit & Revision Metadata (v1.0.1)

* **Deposit Title:** Gaia DR3 wide binary star kinematics and the low-acceleration velocity plateau in Chronodynamic Relativity
* **Version:** `v1.0.1` (Preprint Revision)
* **Publication Date:** `2026-10-11`
* **Zenodo Record ID:** [`23149642`](https://zenodo.org/records/23149642)
* **Preprint DOI:** [`10.5281/zenodo.23149642`](https://doi.org/10.5281/zenodo.23149642)
* **Software Companion DOI:** [`10.5281/zenodo.22697449`](https://doi.org/10.5281/zenodo.22697449)
* **License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)
* **Metadata Schema File:** [`.zenodo.json`](.zenodo.json)
* **Revision Notes:** Formatted into official Astronomy & Astrophysics (A&A) two-column layout using `aa.cls` (v9.2) and `aa.bst`; aligned title and section headings to A&A sentence case editorial standards; lowercased generic acronym expansions; updated software companion framework to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449).

---

## Directory Contents & Provenance

* **[`shreve_wide_binary_kinematics.tex`](shreve_wide_binary_kinematics.tex):** Complete Astronomy & Astrophysics (`aa.cls`) LaTeX source code covering 26,000+ Gaia DR3 wide binary pairs, eccentric orbit Monte Carlo integration, Galactic external field screening, and Sun-Earth L1 saddle point quantum test.
* **[`references.bib`](references.bib):** BibTeX database containing all wide binary, Gaia DR3, and gravitational test citations.
* **[`shreve_wide_binary_kinematics.pdf`](shreve_wide_binary_kinematics.pdf):** Compiled 9-page publication PDF formatted to official A&A standards with high-resolution figures.
* **[`generate_wide_binary_figures.py`](generate_wide_binary_figures.py):** Automated high-resolution figure generator producing all figures in [`figures/`](figures/).
* **[`verify_calculations.py`](verify_calculations.py):** First-principles execution script validating all velocity boosts, sample purities, and saddle point bubble parameters.
* **[`reference_calculations.json`](reference_calculations.json):** Standardized numerical database verifying all manuscript values.

---

## How to Compile to PDF:

```bash
pdflatex shreve_wide_binary_kinematics.tex
bibtex shreve_wide_binary_kinematics
pdflatex shreve_wide_binary_kinematics.tex
pdflatex shreve_wide_binary_kinematics.tex
```
