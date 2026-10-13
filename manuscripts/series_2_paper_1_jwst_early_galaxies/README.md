# Chronodynamic Relativity — Series 2, Paper 1: High-Redshift JWST Galaxies

**Resolving the high-redshift JWST early galaxy and supermassive black hole crisis via chronodynamic proper time dilation**

* **Status:** Official Submission Candidate (Version 1.0.1)
* **Author:** Joshua A. Shreve ([ORCID: 0009-0000-5942-5351](https://orcid.org/0009-0000-5942-5351))
* **Target Journal:** *Astronomy & Astrophysics* (A&A, S2O, 0 USD)

---

## Zenodo Deposit & Revision Metadata (v1.0.1)

* **Deposit Title:** Resolving the high-redshift JWST early galaxy and supermassive black hole crisis via chronodynamic proper time dilation
* **Version:** `v1.0.1` (Preprint Revision)
* **Publication Date:** `2026-10-11`
* **Zenodo Record ID:** [`23149446`](https://zenodo.org/records/23149446)
* **Preprint DOI:** [`10.5281/zenodo.23149446`](https://doi.org/10.5281/zenodo.23149446)
* **Software Companion DOI:** [`10.5281/zenodo.22697449`](https://doi.org/10.5281/zenodo.22697449)
* **License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)
* **Metadata Schema File:** [`.zenodo.json`](.zenodo.json)
* **Revision Notes:** Formatted into official Astronomy & Astrophysics (A&A) two-column layout using `aa.cls` (v9.2) and `aa.bst`; aligned title, section headings, and figure captions to A&A sentence case editorial standards; lowercased generic acronym expansions; eliminated table overruns; updated software companion framework to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449).

---

## Directory Contents & Provenance

* **[`shreve_jwst_early_galaxies.tex`](shreve_jwst_early_galaxies.tex):** Complete Astronomy & Astrophysics (`aa.cls`) LaTeX source code covering the relativistic proper time dilation mechanism $\eta(z) = (1+z)^{-2}$, high-$z$ star formation efficiencies, and sub-Eddington SMBH growth tracks.
* **[`paper_jwst_references.bib`](paper_jwst_references.bib):** BibTeX database with complete citations for JWST JADES, CEERS, UNCOVER, and early AGN surveys.
* **[`shreve_jwst_early_galaxies.pdf`](shreve_jwst_early_galaxies.pdf):** Compiled 4-page publication PDF formatted to official A&A standards.
* **[`generate_jwst_figures.py`](generate_jwst_figures.py):** Automated high-resolution vector figure generator producing all figures in [`figures/`](figures/).
* **[`verify_calculations.py`](verify_calculations.py):** First-principles execution script validating all proper time integrals, halo mass functions, and black hole accretion trajectories.
* **[`reference_calculations.json`](reference_calculations.json):** Machine-readable reference values generated directly by `verify_calculations.py`.

---

## How to Compile to PDF:

```bash
pdflatex shreve_jwst_early_galaxies.tex
bibtex shreve_jwst_early_galaxies
pdflatex shreve_jwst_early_galaxies.tex
pdflatex shreve_jwst_early_galaxies.tex
```
