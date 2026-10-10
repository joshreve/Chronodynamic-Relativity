# Chronodynamic Relativity — Series 2, Paper 2: Cluster Collision Hydrodynamics

* **Status:** Frozen Official Release Candidate (Version 1.0.0)
* **Author:** Joshua A. Shreve ([ORCID: 0009-0000-5942-5351](https://orcid.org/0009-0000-5942-5351))
* **Target Journal:** *Physical Review D* / *MNRAS*
* **Zenodo Record ID:** [`23149512`](https://zenodo.org/records/23149512)
* **Zenodo Preprint DOI:** [`10.5281/zenodo.23149512`](https://doi.org/10.5281/zenodo.23149512)
* **Codebase & Framework DOI:** [`10.5281/zenodo.22697449`](https://doi.org/10.5281/zenodo.22697449)

---

## Manuscript Files:
* **[shreve_cluster_collision_hydrodynamics.tex](shreve_cluster_collision_hydrodynamics.tex):** Complete RevTeX-4.2 LaTeX source code covering the non-equilibrium dynamic metric relaxation PDE, 3D AMR simulation results (RAMSES-CR), live N-body stellar particle tracking, multi-cluster ensemble benchmarks (Bullet Cluster, El Gordo, Abell 520, MACS J0025.4-1222), and pre-discovery predictions for 2026–2028.
* **[paper_cluster_references.bib](paper_cluster_references.bib):** BibTeX database containing all observational and theoretical citations.
* **[shreve_cluster_collision_hydrodynamics.pdf](shreve_cluster_collision_hydrodynamics.pdf):** Compiled 14-page publication PDF with high-resolution figures.
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
