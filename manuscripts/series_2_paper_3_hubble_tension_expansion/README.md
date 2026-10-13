# Chronodynamic Relativity — Series 2, Paper 3: Cosmic Expansion & Hubble Tension

**Eliminating Dark Energy and Resolving the Hubble Tension via Linear Relativistic Cosmic Expansion**

* **Status:** Official Submission Candidate (Version 1.0.1)
* **Author:** Joshua A. Shreve ([ORCID: 0009-0000-5942-5351](https://orcid.org/0009-0000-5942-5351))
* **Target Journal:** *Physical Review D* / *MNRAS*

---

## Zenodo Deposit & Revision Metadata (v1.0.1)

* **Deposit Title:** Eliminating Dark Energy and Resolving the Hubble Tension via Linear Relativistic Cosmic Expansion
* **Version:** `v1.0.1` (Preprint Revision)
* **Publication Date:** `2026-10-11`
* **Zenodo Record ID:** [`23149595`](https://zenodo.org/records/23149595)
* **Preprint DOI:** [`10.5281/zenodo.23149595`](https://doi.org/10.5281/zenodo.23149595)
* **Software Companion DOI:** [`10.5281/zenodo.22697449`](https://doi.org/10.5281/zenodo.22697449)
* **License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)
* **Metadata Schema File:** [`.zenodo.json`](.zenodo.json)
* **Revision Notes:** Certified RevTeX-4.2 publication candidate for Physical Review D / MNRAS; verified Pantheon+ SNe Ia and DESI 2024 BAO joint likelihoods; updated companion software framework to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449).

---

## Directory Contents & Provenance

* **[`shreve_hubble_tension_expansion.tex`](shreve_hubble_tension_expansion.tex):** Complete RevTeX-4.2 LaTeX source code covering linear cosmic expansion $R(t) = ct$, metric clock scaling $\eta(z) = (1+z)^{-2}$, 1,701 Pantheon+ Supernovae likelihood analysis, and DESI 2024 BAO reconstruction.
* **[`paper_hubble_references.bib`](paper_hubble_references.bib):** BibTeX database containing all supernovae, BAO, and cosmological reference citations.
* **[`shreve_hubble_tension_expansion.pdf`](shreve_hubble_tension_expansion.pdf):** Compiled 8-page publication PDF with high-resolution figures.
* **[`generate_hubble_figures.py`](generate_hubble_figures.py):** High-resolution figure generation pipeline.
* **[`verify_calculations.py`](verify_calculations.py):** Automated mathematical validation suite enforcing zero-hallucination compliance.
* **[`reference_calculations.json`](reference_calculations.json):** Standardized numerical database verifying all cosmological distance moduli and BAO observables.

---

## How to Compile to PDF:

```bash
pdflatex shreve_hubble_tension_expansion.tex
bibtex shreve_hubble_tension_expansion
pdflatex shreve_hubble_tension_expansion.tex
pdflatex shreve_hubble_tension_expansion.tex
```
