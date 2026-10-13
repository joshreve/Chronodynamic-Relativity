# Zenodo Deposit Revision Guide & Metadata Reference
**Chronodynamic Relativity Monograph Series & Software Framework**  
*Revision Date:* October 11, 2026  
*Primary Author:* Joshua A. Shreve ([ORCID: 0009-0000-5942-5351](https://orcid.org/0009-0000-5942-5351))  
*Software Framework Concept DOI:* [`10.5281/zenodo.22697449`](https://doi.org/10.5281/zenodo.22697449)

---

## 1. Summary of Version Revisions

| Deposit Target | Current Version | Record ID | Permanent / Concept DOI | Revision Focus |
|---|---|---|---|---|
| **Software Engine** | `v1.1.1` | `22697449` | [`10.5281/zenodo.22697449`](https://doi.org/10.5281/zenodo.22697449) | Support A&A dual-format export; package 1.0.1 preprints; update dependencies |
| **Series 1, Paper 1** | `v1.1.0` | `22697885` | [`10.5281/zenodo.22697884`](https://doi.org/10.5281/zenodo.22697884) | RevTeX-4.2 certified candidate; enhanced in-text mathematical definitions |
| **Series 1, Paper 2** | `v1.0.1` | `23149338` | [`10.5281/zenodo.23149338`](https://doi.org/10.5281/zenodo.23149338) | RevTeX-4.2 candidate; verified thermodynamic arrow and relational clock derivations |
| **Series 2, Paper 1** | `v1.0.1` | `23149446` | [`10.5281/zenodo.23149446`](https://doi.org/10.5281/zenodo.23149446) | Converted to Astronomy & Astrophysics (`aa.cls` v9.2); sentence case titles; eliminated table overruns |
| **Series 2, Paper 2** | `v1.0.1` | `23149512` | [`10.5281/zenodo.23149512`](https://doi.org/10.5281/zenodo.23149512) | Converted to A&A layout; removed acronym from title; balanced multi-cluster table columns |
| **Series 2, Paper 3** | `v1.0.1` | `23149595` | [`10.5281/zenodo.23149595`](https://doi.org/10.5281/zenodo.23149595) | RevTeX-4.2 candidate; verified Pantheon+ SNe Ia and DESI 2024 BAO joint likelihoods |
| **Series 2, Paper 4** | `v1.0.1` | `23149609` | [`10.5281/zenodo.23149609`](https://doi.org/10.5281/zenodo.23149609) | RevTeX-4.2 candidate; verified CLASS-CR Boltzmann hierarchy and Planck 2018 PR3 spectra |
| **Series 2, Paper 5** | `v1.0.1` | `23149642` | [`10.5281/zenodo.23149642`](https://doi.org/10.5281/zenodo.23149642) | Converted to A&A layout; aligned title and section headings to sentence case editorial standards |

---

## 2. Adjacent Metadata Files

Zenodo deposit metadata is maintained in adjacent files in each manuscript directory:
* **`.zenodo.json`**: Official GitHub-Zenodo integration metadata descriptor.
* **`zenodo_deposit_metadata.json`**: Complete Zenodo REST API payload.
* **`README.md`**: Human-readable overview and revision log.

Packaged release tarballs and PDFs are located in:
`dist/zenodo/<deposit_name>/`

---

## 3. Copy-Pasteable Fields for Zenodo Web UI ("New Version")

### Deposit 0: Software Framework (`v1.1.1`)
* **Version:** `v1.1.1`
* **Publication Date:** `2026-10-11`
* **Title:** Chronodynamic Relativity: Covariant Space Density, Environmental Clock Scaling, and Relativistic Boltzmann Hierarchy Solvers
* **Additional Notes:**
  ```text
  Version 1.1.1 Release Notes: Integrated Astronomy & Astrophysics (A&A aa.cls v9.2) layout support for Papers 2.1, 2.2, and 2.5; packaged v1.0.1 manuscript preprints; updated publication pipelines and automated Zenodo deposit packaging.
  ```
* **Files:** `dist/zenodo/software/chronodynamic_relativity_software_v1.1.1.tar.gz`

---

### Deposit 1: Series 1, Paper 1 (`v1.1.0`)
* **Version:** `v1.1.0`
* **Publication Date:** `2026-10-11`
* **Title:** Chronodynamic Relativity: Unifying Cosmic Expansion, Galactic Dynamics, Gravitational Lensing, and CMB Acoustic Peaks from a Single Environmental Scalar Field
* **Additional Notes:**
  ```text
  Version 1.1.0 Revision Notes: Certified RevTeX-4.2 publication candidate for Physical Review D / MNRAS; enhanced in-text mathematical symbol definitions; validated exact symbolic derivations across all 4 empirical pillars; updated companion software framework to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449).
  ```
* **Files:**
  * `dist/zenodo/series_1_paper_1_foundations/shreve_chronodynamic_relativity_foundations.pdf`
  * `dist/zenodo/series_1_paper_1_foundations/submission_series_1_paper_1_foundations_v1.1.0.tar.gz`

---

### Deposit 2: Series 1, Paper 2 (`v1.0.1`)
* **Version:** `v1.0.1`
* **Publication Date:** `2026-10-11`
* **Title:** The Thermodynamic Arrow of Time and Quantum Relational Clocks in Chronodynamic Relativity: Unifying Cosmic Expansion, Total Field Energy Dissipation, and the Dynamic Acceleration Horizon
* **Additional Notes:**
  ```text
  Version 1.0.1 Revision Notes: Certified RevTeX-4.2 publication candidate for Physical Review D; verified thermodynamic arrow and relational clock derivations; updated companion software framework to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449).
  ```
* **Files:**
  * `dist/zenodo/series_1_paper_2_temporal_dissipation/shreve_temporal_dissipation.pdf`
  * `dist/zenodo/series_1_paper_2_temporal_dissipation/submission_series_1_paper_2_temporal_dissipation_v1.0.1.tar.gz`

---

### Deposit 3: Series 2, Paper 1 (`v1.0.1`)
* **Version:** `v1.0.1`
* **Publication Date:** `2026-10-11`
* **Title:** Resolving the high-redshift JWST early galaxy and supermassive black hole crisis via chronodynamic proper time dilation
* **Additional Notes:**
  ```text
  Version 1.0.1 Revision Notes: Formatted into official Astronomy & Astrophysics (A&A) two-column layout using aa.cls (v9.2) and aa.bst; aligned title, section headings, and figure captions to A&A sentence case editorial standards; lowercased generic acronym expansions; eliminated table overruns; updated companion software framework to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449).
  ```
* **Files:**
  * `dist/zenodo/series_2_paper_1_jwst_early_galaxies/shreve_jwst_early_galaxies.pdf`
  * `dist/zenodo/series_2_paper_1_jwst_early_galaxies/submission_series_2_paper_1_jwst_early_galaxies_v1.0.1.tar.gz`

---

### Deposit 4: Series 2, Paper 2 (`v1.0.1`)
* **Version:** `v1.0.1`
* **Publication Date:** `2026-10-11`
* **Title:** Three-dimensional relativistic shock hydrodynamics and multi-cluster decoupling without non-baryonic dark matter
* **Additional Notes:**
  ```text
  Version 1.0.1 Revision Notes: Formatted into official Astronomy & Astrophysics (A&A) two-column layout using aa.cls (v9.2) and aa.bst; eliminated leading acronym/numeral from title; aligned section headings to A&A sentence case editorial standards; balanced multi-cluster table column widths; lowercased generic acronym expansions; fixed adverb hyphenation; updated companion software framework to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449).
  ```
* **Files:**
  * `dist/zenodo/series_2_paper_2_cluster_collision_hydrodynamics/shreve_cluster_collision_hydrodynamics.pdf`
  * `dist/zenodo/series_2_paper_2_cluster_collision_hydrodynamics/submission_series_2_paper_2_cluster_collision_hydrodynamics_v1.0.1.tar.gz`

---

### Deposit 5: Series 2, Paper 3 (`v1.0.1`)
* **Version:** `v1.0.1`
* **Publication Date:** `2026-10-11`
* **Title:** Eliminating Dark Energy and Resolving the Hubble Tension via Linear Relativistic Cosmic Expansion
* **Additional Notes:**
  ```text
  Version 1.0.1 Revision Notes: Certified RevTeX-4.2 publication candidate for Physical Review D / MNRAS; verified Pantheon+ SNe Ia and DESI 2024 BAO joint likelihoods; updated companion software framework to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449).
  ```
* **Files:**
  * `dist/zenodo/series_2_paper_3_hubble_tension_expansion/shreve_hubble_tension_expansion.pdf`
  * `dist/zenodo/series_2_paper_3_hubble_tension_expansion/submission_series_2_paper_3_hubble_tension_expansion_v1.0.1.tar.gz`

---

### Deposit 6: Series 2, Paper 4 (`v1.0.1`)
* **Version:** `v1.0.1`
* **Publication Date:** `2026-10-11`
* **Title:** Primordial Acoustic Perturbations and Full-Multipole Boltzmann Hierarchy in Chronodynamic Relativity
* **Additional Notes:**
  ```text
  Version 1.0.1 Revision Notes: Certified RevTeX-4.2 publication candidate for Physical Review D / MNRAS; verified CLASS-CR Boltzmann hierarchy solver and Planck 2018 PR3 TT/TE/EE acoustic power spectrum; updated companion software framework to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449).
  ```
* **Files:**
  * `dist/zenodo/series_2_paper_4_cmb_boltzmann_hierarchy/shreve_cmb_boltzmann_hierarchy.pdf`
  * `dist/zenodo/series_2_paper_4_cmb_boltzmann_hierarchy/submission_series_2_paper_4_cmb_boltzmann_hierarchy_v1.0.1.tar.gz`

---

### Deposit 7: Series 2, Paper 5 (`v1.0.1`)
* **Version:** `v1.0.1`
* **Publication Date:** `2026-10-11`
* **Title:** Gaia DR3 wide binary star kinematics and the low-acceleration velocity plateau in Chronodynamic Relativity
* **Additional Notes:**
  ```text
  Version 1.0.1 Revision Notes: Formatted into official Astronomy & Astrophysics (A&A) two-column layout using aa.cls (v9.2) and aa.bst; aligned title and section headings to A&A sentence case editorial standards; lowercased generic acronym expansions; updated companion software framework to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449).
  ```
* **Files:**
  * `dist/zenodo/series_2_paper_5_wide_binary_kinematics/shreve_wide_binary_kinematics.pdf`
  * `dist/zenodo/series_2_paper_5_wide_binary_kinematics/submission_series_2_paper_5_wide_binary_kinematics_v1.0.1.tar.gz`
