# Chronodynamic Relativity — Series 2, Paper 4: CMB Boltzmann Hierarchy

**Primordial Acoustic Perturbations and Full-Multipole Boltzmann Hierarchy in Chronodynamic Relativity**

* **Status:** Frozen Official Release Candidate (Version 1.0.0)
* **Author:** Joshua A. Shreve ([ORCID: 0009-0000-5942-5351](https://orcid.org/0009-0000-5942-5351))
* **Target Journal:** *Physical Review D* / *MNRAS*
* **Zenodo Record ID:** [`23149609`](https://zenodo.org/records/23149609)
* **Zenodo Preprint DOI:** [`10.5281/zenodo.23149609`](https://doi.org/10.5281/zenodo.23149609)
* **Codebase & Framework DOI:** [`10.5281/zenodo.22697449`](https://doi.org/10.5281/zenodo.22697449)

---

## Directory Contents & Provenance

* **[`shreve_cmb_boltzmann_hierarchy.tex`](shreve_cmb_boltzmann_hierarchy.tex):** Complete RevTeX-4.2 LaTeX source code formulating the non-linear hybrid Boltzmann hierarchy (`class_cr`), Peebles recombination kinetics, Silk damping, and full TT/TE/EE acoustic power spectra against Planck 2018 PR3 and ACT DR6 data.
* **[`paper_cmb_references.bib`](paper_cmb_references.bib):** BibTeX database containing all CMB, cosmological perturbation, and Boltzmann solver citations.
* **[`shreve_cmb_boltzmann_hierarchy.pdf`](shreve_cmb_boltzmann_hierarchy.pdf):** Compiled 10-page publication PDF with high-resolution figures.
* **[`generate_cmb_figures.py`](generate_cmb_figures.py):** Automated high-resolution figure generator producing all figures in [`figures/`](figures/).
* **[`verify_calculations.py`](verify_calculations.py):** First-principles execution script validating all acoustic peak locations, sound horizon integrals, and transfer metrics.
* **[`reference_calculations.json`](reference_calculations.json):** Standardized numerical database verifying all manuscript values.

---

## How to Compile to PDF:

```bash
pdflatex shreve_cmb_boltzmann_hierarchy.tex
bibtex shreve_cmb_boltzmann_hierarchy
pdflatex shreve_cmb_boltzmann_hierarchy.tex
pdflatex shreve_cmb_boltzmann_hierarchy.tex
```
