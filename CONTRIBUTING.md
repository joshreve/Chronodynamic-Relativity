# Contributing to Chronodynamic Relativity

Thank you for your interest in contributing to the **Chronodynamic Relativity** research framework and empirical evaluation suite.

## Origin & Theoretical Governance
Chronodynamic Relativity was originated and formulated by **Joshua A. Shreve** ([ORCID: 0009-0000-5942-5351](https://orcid.org/0009-0000-5942-5351)). All theoretical derivations, core relativistic models, and reference physics implementations maintain strict mathematical consistency and single-source-of-truth governance across all four empirical pillars.

## How to Contribute
We welcome contributions in the following areas:
1. **Numerical Solver Optimization:** Accelerating Boltzmann linear perturbation integrators (`class_cr`) and 3D hydrodynamic AMR pipelines (`ramses3d_mpi`).
2. **Observational Data Ingestion:** Expanding certified empirical loaders (e.g. DESI Y3, Euclid lensing, Roman high-redshift cluster catalogues).
3. **Reproducibility Benchmarks:** Validating analytical tests, parameter likelihood estimators, and test suites.

## Scientific Rigor Guidelines
- **Single Source of Truth:** All physical evaluations must utilize canonical model engines in `src/models/`.
- **First-Principles Derivation:** Theoretical curves must be derived directly from fundamental field and fluid equations without piecewise empirical fitting.
- **Test Integrity:** All pull requests must pass the complete unit test suite (`pytest tests/`) prior to review.

## Citation & Attribution
Contributions are governed by the MIT License. In research publications utilizing this framework, please cite:
```bibtex
@software{shreve2026chronodynamic,
  author       = {Shreve, Joshua A.},
  title        = {{Chronodynamic Relativity: Unified Relativistic \& Cosmological Empirical Evaluation Framework}},
  year         = 2026,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.22697449},
  url          = {https://doi.org/10.5281/zenodo.22697449}
}
```
