# Chronodynamic Relativity: The Space Density Theory

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22697450.svg)](https://doi.org/10.5281/zenodo.22697450)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0000--5942--5351-green.svg)](https://orcid.org/0009-0000-5942-5351)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Chronodynamic Relativity (CR)** is a Covariant Scalar-Tensor Gravity framework. It fundamentally reimagines gravitational dynamics and cosmic acceleration not as dark matter halos or a cosmological constant, but as the non-linear spatial gradient and temporal dilation of a universal background space energy density scalar field ($\rho_s(\vec{x}, t)$).

By linking the local metric clock rate ($\eta$) to space energy density, Chronodynamic Relativity natively replicates the primary observational pillars of modern cosmology with zero internal tunable parameters ($k_{\text{internal}} = 0$).

## Core Validations
This repository contains the physics engine, automated benchmark suite, and interactive visualization generators that empirically validate the theory against major astrophysical datasets:
*   **Cosmic Expansion:** Evaluated across 1,701 Type Ia Supernovae (Pantheon+ SH0ES) and Cosmic Chronometers across 4 data processing tiers, addressing the Hubble tension with a unified $H_0 \approx 70.5\text{ km/s/Mpc}$.
*   **Galactic Dynamics:** Resolves flat rotation curves and the Radial Acceleration Relation (RAR) for 175 SPARC galaxies via an algebraic root formulation, bypassing the NFW core-cusp problem without dark matter halos.
*   **The CDM Inverse-Poisson Duality:** Demonstrates that Dark Matter halos (spatial gradients) and Dark Energy acceleration (temporal dilation) in $\Lambda\text{CDM}$ are inverse-Poisson projections of a single scalar field $\rho_s(\vec{x}, t)$.
*   **Strong Gravitational Lensing:** Integrates a 3D field density inversion to yield a theoretical "Factor of $\pi$" boost, matching SLACS Einstein Radii.
*   **Cluster Mergers:** Utilizes dynamic non-equilibrium vacuum relaxation ($\tau_{\text{relax}}$) to predict the spatial offset of the Bullet Cluster (1E 0657-56) without dark matter particles.
*   **CMB Acoustic Oscillations:** Matches Planck 2018 PR3 acoustic peaks 1–3 ($\ell=220, 540, 810$) via dynamic primordial membrane tension $a_0(t) = c/(4\pi t)$.

---

## ⚙️ Setup & Installation

The project requires Python 3.10+ and uses standard scientific computing libraries (NumPy, SciPy, Pandas, Matplotlib, Plotly).

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/joshreve/Chronodynamic-Relativity.git
    cd Chronodynamic-Relativity
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv .venv
    ```
    *   *Windows:* `.\.venv\Scripts\activate`
    *   *Mac/Linux:* `source .venv/bin/activate`

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 📊 Generating the Documentation (Single Source of Truth)

Chronodynamic Relativity utilizes a **Single Source of Truth (SSOT)** architecture for its theoretical reporting. All mathematical models, parameter audits, and Plotly visualizations are driven by centralized physics engines to ensure consistency across all benchmark suites.

To generate the full suite of interactive HTML reports:

```bash
python scripts/upkeep_html_docs.py
```

*Pass `--rerun-atlas` if you need to force a full re-computation of all 175 SPARC 3D galaxies (fast-skipped by default).*

This maintains:
*   `docs/index.html`: The canonical Master Documentation Index for publication-ready benchmarks and foundational monographs.
*   `docs/analyses/analyses_overview.html`: The interactive Omnibus summary across all empirical pillars.

---

## 🧪 Running the Automated Test Suite

To ensure the physics engines, relativistic field equations, and data provenance integrity are mathematically consistent, run the automated test suite:

```bash
pytest tests/
```
Or with unittest:
```bash
python -m unittest discover tests/
```

---

## 📂 Project Structure

*   `manifest.json`: Machine-readable provenance manifest mapping raw inputs $\to$ evaluation scripts $\to$ results $\to$ figures.
*   `data/`: Curated raw empirical datasets ONLY (SPARC, Pantheon+ SNe Ia, Planck PR3 spectra, DESI BAO, MW Gaia, Quantum bounds).
*   `results/`: Generated numerical outputs, benchmark summaries, and parameter sets (`benchmarks/`, `cosmology/`, `global/`, `investigations/`).
*   `src/models/`: Core theoretical physics engines (Gravity, Cosmology, Space Density).
*   `src/evaluations/`: Automated evaluation pipelines, joint likelihood suites, and SSOT site builder.
*   `manuscripts/`: Publication-ready RevTeX 4-2 manuscript, vector figures, and compiled PDF.
*   `docs/`: Interactive SSOT HTML analyses and foundational monographs.
*   `tests/`: Test suite protecting physical invariants, field equations, and data provenance integrity.

---

## 📜 Citation & Archival Record

If you use this framework or empirical reproduction pipelines in your research, please cite the software archive:

```bibtex
@software{shreve_chronodynamic_2026,
  author       = {Shreve, Joshua A.},
  title        = {{Chronodynamic Relativity: Unified Relativistic \& Cosmological Empirical Evaluation Framework}},
  month        = sep,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v1.0.2},
  doi          = {10.5281/zenodo.22697450},
  url          = {https://github.com/joshreve/Chronodynamic-Relativity}
}
```
* **Author:** Joshua A. Shreve ([ORCID: 0009-0000-5942-5351](https://orcid.org/0009-0000-5942-5351))  
* **DOI:** [10.5281/zenodo.22697450](https://doi.org/10.5281/zenodo.22697450)  
* Formal metadata is provided in `CITATION.cff` and `.zenodo.json`.

---

## 📖 Foundational Documentation & Monographs

*   **[Parameter Definitions & Domain Applications Guide](docs/PARAMETER_DEFINITIONS_AND_APPLICATIONS.md):** Complete systematic dictionary of all universal invariants, derived scales, observational variables, domain applications, and cross-model parameter mappings ($\Lambda\text{CDM}$, MOND, CR).
*   **[Theoretical Paradigm Niche & Observational Methodology](docs/THEORETICAL_NICHE_AND_OBSERVATIONAL_METHODOLOGY.md):** Formal treatise on the architectural origin of the theory, resolution of historical theoretical roadblocks, zero-parameter geometric derivations ($n = 3/4\pi, a_0 = 3 c H_0 / 4\pi$), and 4-tier Bayesian model-independent data conditioning audits.
*   **[Mathematical Foundations & Symbology](docs/MATHEMATICAL_FOUNDATIONS_AND_SYMBOLOGY.md):** Complete mathematical symbology and relativistic tensor definitions.
*   **[Scientific References & Parameters](docs/REFERENCES.md):** Accepted cosmological and galactic empirical parameters and literature citations.

---

## 🤖 Scientific Methodology & AI Assistance Disclosure

In accordance with open-science transparency standards, codebase engineering and benchmark automation in this repository are assisted by AI developer tooling (Google Antigravity / Gemini). The theoretical framework, underlying physical principles, mathematical formulations, empirical methodology, and conclusions are conceived, directed, and verified by the primary human investigator (Joshua A. Shreve), who retains sole scientific and intellectual responsibility for the framework.
