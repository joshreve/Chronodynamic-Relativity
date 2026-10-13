# Chronodynamic Relativity — Series 2, Paper 2: Cluster Collision Hydrodynamics

**Three-dimensional relativistic shock hydrodynamics and multi-cluster decoupling without non-baryonic dark matter**

* **Status:** Official Submission Candidate (Version 1.0.1)
* **Author:** Joshua A. Shreve ([ORCID: 0009-0000-5942-5351](https://orcid.org/0009-0000-5942-5351))
* **Target Journal:** *Astronomy & Astrophysics* (A&A, S2O, 0 USD)

---

## Zenodo Deposit & Revision Metadata (v1.0.1)

* **Deposit Title:** Three-dimensional relativistic shock hydrodynamics and multi-cluster decoupling without non-baryonic dark matter
* **Version:** `v1.0.1` (Preprint Revision)
* **Publication Date:** `2026-10-11`
* **Zenodo Record ID:** [`23149512`](https://zenodo.org/records/23149512)
* **Preprint DOI:** [`10.5281/zenodo.23149512`](https://doi.org/10.5281/zenodo.23149512)
* **Software Companion DOI:** [`10.5281/zenodo.22697449`](https://doi.org/10.5281/zenodo.22697449)
* **License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)
* **Metadata Schema File:** [`.zenodo.json`](.zenodo.json)
* **Revision Notes:** Formatted into official Astronomy & Astrophysics (A&A) two-column layout using `aa.cls` (v9.2) and `aa.bst`; eliminated leading acronym/numeral from title; aligned section headings to A&A sentence case editorial standards; balanced multi-cluster table column widths; lowercased generic acronym expansions; fixed adverb hyphenation; updated software companion framework to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449).

---

## Manuscript Files:
* **[shreve_cluster_collision_hydrodynamics.tex](shreve_cluster_collision_hydrodynamics.tex):** Complete Astronomy & Astrophysics (`aa.cls`) LaTeX source code covering the non-equilibrium dynamic metric relaxation PDE, 3D AMR simulation results (RAMSES-CR), live N-body stellar particle tracking, multi-cluster ensemble benchmarks (Bullet Cluster, El Gordo, Abell 520, MACS J0025.4-1222), and pre-discovery predictions for 2026–2028.
* **[paper_cluster_references.bib](paper_cluster_references.bib):** BibTeX database containing all observational and theoretical citations.
* **[shreve_cluster_collision_hydrodynamics.pdf](shreve_cluster_collision_hydrodynamics.pdf):** Compiled 11-page publication PDF formatted to official A&A standards with high-resolution figures.
* **[verify_calculations.py](verify_calculations.py):** Automated mathematical validation suite enforcing zero-hallucination compliance against `src.models.LatestChronodynamicModel`.
* **[reference_calculations.json](reference_calculations.json):** Standardized numerical database verifying all manuscript constants, simulation metrics, and observational comparisons.
* **[generate_bullet_figures.py](generate_bullet_figures.py):** High-resolution figure generation pipeline.

---

## Key Figures:
* **Figure 1 (`figures/fig1_bullet_decoupling_evolution.pdf`):** 4-epoch 2D midplane gas density and gravitational potential contour maps from the 3D AMR simulation.
* **Figure 2 (`figures/fig2_bullet_offset_evolution.pdf`):** Physical decoupling separation $\Delta r(t)$ over time compared with the 1E 0657-56 empirical band.
* **Figure 3 (`figures/fig3_bullet_1d_profile.pdf`):** 1D collision-axis profile at peak decoupling epoch ($t = 935.6\text{ Myr}$), showing $\Delta x = 330.0\text{ kpc}$.
* **Figure 4 (`figures/fig4_bullet_semianalytical_recovery.pdf`):** 4-panel Lagrangian semi-analytical model showing long-term virial recovery, collision-epoch zoom, and metric latency hysteresis.
* **Figure 5 (`figures/fig5_bullet_semianalytical_spacetime.pdf`):** Spacetime worldsheet heatmaps of gravitational potential well depth and gas density.

---

## How to Compile to PDF:
```bash
pdflatex -interaction=nonstopmode shreve_cluster_collision_hydrodynamics.tex
bibtex shreve_cluster_collision_hydrodynamics
pdflatex -interaction=nonstopmode shreve_cluster_collision_hydrodynamics.tex
pdflatex -interaction=nonstopmode shreve_cluster_collision_hydrodynamics.tex
```
