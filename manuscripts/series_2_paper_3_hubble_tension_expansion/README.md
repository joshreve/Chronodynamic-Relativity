# Chronodynamic Relativity — Series 2, Paper 3: Cosmic Expansion & Hubble Tension

**Eliminating Dark Energy and Resolving the Hubble Tension via Linear Relativistic Cosmic Expansion**

* **Status:** Frozen Official Release Candidate (Version 1.0.0)
* **Author:** Joshua A. Shreve ([ORCID: 0009-0000-5942-5351](https://orcid.org/0009-0000-5942-5351))
* **Target Journal:** *Physical Review D* / *MNRAS*
* **Zenodo Record ID:** [`23149595`](https://zenodo.org/records/23149595)
* **Zenodo Preprint DOI:** [`10.5281/zenodo.23149595`](https://doi.org/10.5281/zenodo.23149595)
* **Codebase & Framework DOI:** [`10.5281/zenodo.22697449`](https://doi.org/10.5281/zenodo.22697449)

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
