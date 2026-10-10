# Chronodynamic Relativity — Series 2, Paper 1: High-Redshift JWST Galaxies

**Resolving the High-Redshift JWST Early Galaxy and Supermassive Black Hole Crisis via Chronodynamic Proper Time Dilation**

* **Status:** Frozen Official Release Candidate (Version 1.0.0)
* **Author:** Joshua A. Shreve ([ORCID: 0009-0000-5942-5351](https://orcid.org/0009-0000-5942-5351))
* **Target Journal:** *The Astrophysical Journal* / *MNRAS*
* **Zenodo Record ID:** [`23149446`](https://zenodo.org/records/23149446)
* **Zenodo Preprint DOI:** [`10.5281/zenodo.23149446`](https://doi.org/10.5281/zenodo.23149446)
* **Codebase & Framework DOI:** [`10.5281/zenodo.22697449`](https://doi.org/10.5281/zenodo.22697449)

---

## Directory Contents & Provenance

* **[`shreve_jwst_early_galaxies.tex`](shreve_jwst_early_galaxies.tex):** Complete RevTeX-4.2 LaTeX source code covering the relativistic proper time dilation mechanism $\eta(z) = (1+z)^{-2}$, high-$z$ star formation efficiencies, and sub-Eddington SMBH growth tracks.
* **[`paper_jwst_references.bib`](paper_jwst_references.bib):** BibTeX database with complete citations for JWST JADES, CEERS, UNCOVER, and early AGN surveys.
* **[`shreve_jwst_early_galaxies.pdf`](shreve_jwst_early_galaxies.pdf):** Compiled 6-page publication PDF ready for journal review.
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
