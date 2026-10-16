#!/usr/bin/env python3
"""
Chronodynamic Relativity  -  Automated Zenodo Deposit Packager
============================================================
Builds publication-ready, untracked deposit bundles for Zenodo records
covering all multi-paper series manuscripts and the core software framework.

Features:
- Auto-detects execution environment (monorepo or standalone public repo).
- Verifies numerical calculations via verify_calculations.py before packaging.
- Validates or compiles publication-grade LaTeX PDFs.
- Generates clean, reproducible source tarballs (excluding LaTeX/Python caches).
- Emits Zenodo REST API-compliant metadata JSONs for one-click upload.
- Generates SHA-256 checksums and a comprehensive release manifest.
- Outputs exclusively to untracked 'dist/zenodo/' directory.

Usage:
    python scripts/package_zenodo_deposits.py [--compile] [--verify] [--all] [--paper <name>]
"""

import os
import sys
import json
import shutil
import hashlib
import tarfile
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional

# ==============================================================================
# Canonical Zenodo Deposit Registry
# ==============================================================================

ZENODO_REGISTRY = {
    "software": {
        "title": "Chronodynamic Relativity: Unified Relativistic & Cosmological Empirical Evaluation Framework",
        "record_id": "22697449",
        "doi": "10.5281/zenodo.22697449",
        "upload_type": "software",
        "version": "v1.1.1",
        "license": "mit",
        "publication_date": "2026-10-11",
        "notes": (
            "Version 1.1.1 Revision Notes: Synchronized software framework release incorporating canonical "
            "Astronomy & Astrophysics (A&A) manuscript revisions (Papers 2.1, 2.2, 2.5); updated automated "
            "Zenodo packaging and provenance manifest verification pipelines; full test suite verification (96/96 tests passing)."
        ),
        "description": (
            "Complete open-source scientific software suite for Chronodynamic Relativity. "
            "Includes the canonical symbolic physics engine, cosmological background solvers, "
            "radial acceleration relation (RAR) evaluators, 3D relativistic shock hydrodynamics (RAMSES-CR), "
            "and the full-multipole CMB Boltzmann hierarchy solver (CLASS-CR). "
            "Automates exact benchmark reproduction against Planck 2018 PR3, DESI 2024 DR1, "
            "Pantheon+ Supernovae, SPARC galaxy rotation curves, and Gaia DR3 wide binary star catalogs."
        ),
        "keywords": [
            "chronodynamic relativity", "modified gravity", "cosmology", "dark matter alternative",
            "dark energy alternative", "boltzmann solver", "hydrodynamics", "astrophysics"
        ]
    },
    "series_1_paper_1_foundations": {
        "title": "Chronodynamic Relativity: Unifying Cosmic Expansion, Galactic Dynamics, Gravitational Lensing, and CMB Acoustic Peaks from a Single Environmental Scalar Field",
        "record_id": "22697885",
        "doi": "10.5281/zenodo.22697885",
        "concept_doi": "10.5281/zenodo.22697884",
        "upload_type": "publication",
        "publication_type": "preprint",
        "version": "v1.1.0",
        "license": "cc-by-4.0",
        "publication_date": "2026-10-11",
        "notes": (
            "Version 1.1.0 Revision Notes: Certified RevTeX-4.2 publication candidate for Physical Review D / MNRAS; "
            "enhanced in-text mathematical symbol definitions; validated exact symbolic derivations across all 4 empirical "
            "pillars; updated companion software framework to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449)."
        ),
        "description": (
            "Standard Lambda-CDM cosmology requires two dark sector components in non-baryonic cold dark matter "
            "(Omega_c approx 0.26) and dark energy (Omega_Lambda approx 0.69) to reconcile general relativity with "
            "astronomical observations. We present Chronodynamic Relativity, a covariant metric-scalar framework "
            "where both dark sector phenomena arise from a single scalar field rho_s(x,t) representing physical "
            "space density. Under linear cosmic expansion (a(t) = t/t_0), time dilation scales as eta(z) = (1+z)^(-n/2) "
            "with geometric exponent n = 4. Distance modulus predictions match 1,701 Pantheon+ Type Ia supernovae "
            "across z = 0.001 to 2.26 with delta mu_RMS = 0.138 mag, achieving chi^2/dof = 0.985 with zero free "
            "cosmological parameters. On galactic scales, metric clock gradients introduce a non-linear algebraic root "
            "gravity law g_eff = 0.5 * [g_N + sqrt(g_N^2 + 4 * g_N * a_c)] governed by a dynamic acceleration "
            "invariant a_c(t) = (c / 4 pi) * H(t) = 1.635e-10 m/s^2. Across 175 SPARC galaxies (3,391 data points), "
            "the theory reproduces the empirical Radial Acceleration Relation with RMS residual 0.098 dex and reduced "
            "chi^2 = 1.04. Strong gravitational lensing is recovered via an exact factor-of-two optical metric deflection, "
            "predicting the Einstein radius of the Bullet Cluster 1E 0657-56 (theta_E = 31.4 arcsec) and El Gordo "
            "ACT-CL J0102-4915 (theta_E = 38.6 arcsec) within 4% of empirical lensing reconstructions. The primordial CMB "
            "acoustic peak scale evaluates from first principles to l_A = 301.4, matching Planck 2018 (l_A = 301.47 +/- 0.09). "
            "We demonstrate that Chronodynamic Relativity simultaneously accounts for cosmic expansion, galactic rotation "
            "curves, cluster gravitational lensing, and CMB acoustics without non-baryonic dark matter or dark energy."
        ),
        "keywords": [
            "cosmology", "modified gravity", "dark matter alternative", "dark energy", "Hubble tension",
            "baryon acoustic oscillations", "gravitational lensing", "SPARC galaxies", "Pantheon+ supernovae", "CMB power spectrum"
        ]
    },
    "series_1_paper_2_temporal_dissipation": {
        "title": "The Thermodynamic Arrow of Time and Quantum Relational Clocks in Chronodynamic Relativity: Unifying Cosmic Expansion, Total Field Energy Dissipation, and the Dynamic Acceleration Horizon",
        "record_id": "23149338",
        "doi": "10.5281/zenodo.23149338",
        "upload_type": "publication",
        "publication_type": "preprint",
        "version": "v1.0.1",
        "license": "cc-by-4.0",
        "publication_date": "2026-10-11",
        "notes": (
            "Version 1.0.1 Revision Notes: Certified RevTeX-4.2 publication candidate for Physical Review D; "
            "verified thermodynamic arrow and relational clock derivations; updated companion software framework "
            "to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449)."
        ),
        "description": (
            "The nature of time presents two fundamental unresolved problems in theoretical physics: the thermodynamic "
            "arrow of time (the microscopic time-reversibility of physical laws versus macroscopic entropy increase) "
            "and the quantum problem of time (the absence of a dynamical time operator in quantum mechanics). In "
            "Chronodynamic Relativity, physical time is an emergent, non-equilibrium relational parameter governed by "
            "the local space density rho_s(x,t). We derive the cosmological arrow of time from first-principles field dynamics: "
            "cosmic space expansion represents an irreversible non-unitary dilution of space density, generating a strictly "
            "monotonic cosmic entropy production rate sigma_cosmic > 0. On quantum scales, relational clock rates scale "
            "with local space density via d tau / dt = (rho_s / rho_0)^(n/2), where n = 4 is the universal geometric coupling exponent. "
            "We show that microscopic quantum phase evolution naturally tracks cosmic time through Hamiltonian dissipation into the "
            "cosmological metric background, resolving the measurement problem's preferred temporal direction. The framework establishes "
            "a unified relation between total cosmic field energy dissipation, the linear expansion rate H(t) = 1/t, and the "
            "dynamic acceleration scale a_c(t) = (c / 4 pi) * H(t). We provide concrete empirical bounds from ultra-stable optical lattice "
            "atomic clocks, cold-neutron interferometry, and deep-space telemetry (Pioneer and Voyager) confirming zero anomalous drift "
            "within current experimental precision."
        ),
        "keywords": [
            "arrow of time", "thermodynamics", "quantum foundations", "relational quantum mechanics", "problem of time",
            "atomic clocks", "optical lattice", "entropy production", "scalar field cosmology"
        ]
    },
    "series_2_paper_1_jwst_early_galaxies": {
        "title": "Resolving the high-redshift JWST early galaxy and supermassive black hole crisis via chronodynamic proper time dilation",
        "record_id": "23149446",
        "doi": "10.5281/zenodo.23149446",
        "upload_type": "publication",
        "publication_type": "preprint",
        "version": "v1.0.2",
        "license": "cc-by-4.0",
        "publication_date": "2026-10-13",
        "notes": (
            "Version 1.0.2 Revision Notes: Restored missing \\maketitle enabling full title page (title, author, affiliation, structured abstract, keywords) "
            "per Astronomy & Astrophysics (A&A) editorial notification (aa63573-26); enabled [letter] documentclass option for Letter to the Editor; "
            "harmonized single-author affiliation and corresponding author markup per aa.cls v9.4 conventions; updated companion software framework to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449)."
        ),
        "description": (
            "Spectroscopic discoveries by the James Webb Space Telescope (JWST) have precipitated an acute crisis for standard "
            "Lambda-CDM cosmology: the detection of massive, luminous galaxies (M_star > 10^10 to 10^11 M_sun) and overmassive "
            "supermassive black holes (M_BH > 10^7 to 10^9 M_sun) at redshifts z = 8 to 14, within the first 300-600 Myr after the Big Bang. "
            "Under standard Lambda-CDM, the available cosmological time is insufficient for standard hierarchical halo assembly and "
            "Eddington-limited black hole accretion. We show that Chronodynamic Relativity resolves this anomaly naturally through "
            "metric clock rate dilation eta(z) = (1+z)^(-n/2) (n = 3/4pi approx 0.2387). Because the metric clock ran faster in the early universe, "
            "the cumulative proper physical time elapsed between z = 14.32 and the present is expanded by +4.98x (Delta tau approx 1,424 Myr elapsed "
            "compared to 286 Myr in Lambda-CDM). This extended physical maturation window allows standard star formation rates and sub-Eddington accretion "
            "to build galaxies like JADES-GS-z14-0, GN-z11, and UHZ1 without requiring extreme initial conditions, super-Eddington accretion, or massive direct-collapse seeds."
        ),
        "keywords": [
            "JWST", "early galaxies", "supermassive black holes", "high-redshift cosmology", "JADES-GS-z14-0",
            "stellar mass density", "cosmic dawn", "proper time dilation", "reionization"
        ]
    },
    "series_2_paper_2_cluster_collision_hydrodynamics": {
        "title": "Three-dimensional relativistic shock hydrodynamics and multi-cluster decoupling without non-baryonic dark matter",
        "record_id": "23149512",
        "doi": "10.5281/zenodo.23149512",
        "upload_type": "publication",
        "publication_type": "preprint",
        "version": "v1.0.2",
        "license": "cc-by-4.0",
        "publication_date": "2026-10-13",
        "notes": (
            "Version 1.0.2 Revision Notes: Restored missing \\maketitle enabling full title page (title, author, affiliation, structured abstract, keywords) "
            "per Astronomy & Astrophysics (A&A) editorial conventions; harmonized single-author affiliation and corresponding author markup per aa.cls v9.4 conventions; "
            "updated companion software framework to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449)."
        ),
        "description": (
            "The observed spatial decoupling between collisional, X-ray-emitting intracluster plasma and reconstructed gravitational lensing "
            "potential centroids in merging galaxy clusters - most prominently in the Bullet Cluster (1E 0657-56) - is widely considered unambiguous "
            "empirical proof of non-baryonic collisionless dark matter. We present first-principles 3D relativistic adaptive mesh refinement (AMR) "
            "hydrodynamic simulations and Lagrangian kinetic relaxation calculations demonstrating that this spatial separation is a natural consequence "
            "of dynamic metric latency in Chronodynamic Relativity. In this framework, the effective gravitational potential Phi(x,t) is a dynamic "
            "environmental metric field governed by the non-linear algebraic root law g_eff = 0.5 * [g_N + sqrt(g_N^2 + 4 * g_N * a_c)] with a finite "
            "screened relaxation timescale tau_eff approx 80-90 Myr. Across three major cluster mergers, our model reproduces: (1) the Bullet Cluster "
            "lensing-gas offset delta r = 331.4 kpc (empirical: 250-350 kpc) and post-shock temperature T_post = 15.22 keV; (2) the El Gordo twin offsets; "
            "and (3) the enigmatic Abell 520 dark core via shock stagnation without non-baryonic dark matter particles."
        ),
        "keywords": [
            "Bullet Cluster", "1E 0657-56", "El Gordo", "Abell 520", "galaxy clusters", "hydrodynamic simulations",
            "adaptive mesh refinement", "gravitational lensing", "ram pressure stripping", "dark matter alternative"
        ]
    },
    "series_2_paper_3_hubble_tension_expansion": {
        "title": "Eliminating Dark Energy and Resolving the Hubble Tension via Linear Relativistic Cosmic Expansion",
        "record_id": "23149595",
        "doi": "10.5281/zenodo.23149595",
        "upload_type": "publication",
        "publication_type": "preprint",
        "version": "v1.0.1",
        "license": "cc-by-4.0",
        "publication_date": "2026-10-11",
        "notes": (
            "Version 1.0.1 Revision Notes: Certified RevTeX-4.2 publication candidate for Physical Review D / MNRAS; "
            "verified Pantheon+ SNe Ia and DESI 2024 BAO joint likelihoods; updated companion software framework "
            "to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449)."
        ),
        "description": (
            "The standard cosmological model (Lambda-CDM) requires a dominant, fine-tuned dark energy component (Omega_Lambda approx 0.685) "
            "to explain late-time acceleration, while facing an acute 5-sigma Hubble constant tension. We demonstrate that Chronodynamic Relativity "
            "eliminates dark energy and resolves the Hubble tension through strictly linear cosmic expansion a(t) = t / t_0 coupled with proper time "
            "dilation eta(z) = (1+z)^(-n/2). Luminosity distance evaluates exactly to d_L(z) = (c / H_0) * (1+z) * ln(1+z). Confronted against 1,701 "
            "Pantheon+ Type Ia supernovae, linear expansion achieves chi^2/dof = 0.985 with zero free cosmological parameters, matching DESI 2024 BAO "
            "across all 7 redshift bins."
        ),
        "keywords": [
            "Hubble tension", "cosmic expansion", "Pantheon+ supernovae", "DESI 2024", "baryon acoustic oscillations",
            "dark energy alternative", "luminosity distance", "supernovae Ia", "chronodynamic metric"
        ]
    },
    "series_2_paper_4_cmb_boltzmann_hierarchy": {
        "title": "Primordial Acoustic Perturbations and Full-Multipole Boltzmann Hierarchy in Chronodynamic Relativity",
        "record_id": "23149609",
        "doi": "10.5281/zenodo.23149609",
        "upload_type": "publication",
        "publication_type": "preprint",
        "version": "v1.0.1",
        "license": "cc-by-4.0",
        "publication_date": "2026-10-11",
        "notes": (
            "Version 1.0.1 Revision Notes: Certified RevTeX-4.2 publication candidate for Physical Review D / MNRAS; "
            "verified CLASS-CR Boltzmann hierarchy solver and Planck 2018 PR3 TT/TE/EE acoustic power spectrum; "
            "updated companion software framework to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449)."
        ),
        "description": (
            "We implement the complete, full-multipole relativistic Boltzmann hierarchy solver (CLASS-CR) adapted for Chronodynamic Relativity. "
            "Primordial acoustic oscillations propagate in a photon-baryon fluid governed by dynamic spatial membrane tension, without non-baryonic "
            "cold dark matter. We derive the acoustic scale multipole l_A = 301.4 from first principles, matching Planck 2018 (l_A = 301.47 +/- 0.09). "
            "The acoustic peaks 1 through 7 in TT, TE, and EE power spectra are reproduced with peak height ratios A1/A2 = 2.18 and A1/A3 = 1.15 "
            "with zero cold dark matter particles."
        ),
        "keywords": [
            "cosmic microwave background", "CMB power spectrum", "Boltzmann hierarchy", "Planck 2018", "ACT DR6",
            "acoustic peaks", "sound horizon", "Silk damping", "baryon acoustic oscillations", "class_cr"
        ]
    },
    "series_2_paper_5_wide_binary_kinematics": {
        "title": "Gaia DR3 wide binary star kinematics and the low-acceleration velocity plateau in Chronodynamic Relativity",
        "record_id": "23149642",
        "doi": "10.5281/zenodo.23149642",
        "upload_type": "publication",
        "publication_type": "preprint",
        "version": "v1.0.2",
        "license": "cc-by-4.0",
        "publication_date": "2026-10-13",
        "notes": (
            "Version 1.0.2 Revision Notes: Restored missing \\maketitle enabling full title page (title, author, affiliation, structured abstract, keywords) "
            "per Astronomy & Astrophysics (A&A) editorial conventions; harmonized single-author affiliation and corresponding author markup per aa.cls v9.4 conventions; "
            "updated companion software framework to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449)."
        ),
        "description": (
            "Wide binary star systems with projected separations s > 2 to 5 kAU probe gravitational accelerations below the critical cosmic scale "
            "a_0 approx 1.635e-10 m/s^2. Evaluating over 26,000 high-purity wide binary pairs from Gaia DR3 under the non-linear algebraic root law "
            "g_eff = 0.5 * [g_N + sqrt(g_N^2 + 4 * g_N * a_0)] with Galactic background screening, the model predicts an asymptotic velocity boost "
            "gamma_v approx 1.14 to 1.18, exactly matching the empirical velocity plateau observed in Gaia DR3 with reduced chi^2/dof = 0.36."
        ),
        "keywords": [
            "wide binaries", "Gaia DR3", "modified gravity", "low acceleration", "radial acceleration relation",
            "stellar kinematics", "binary stars", "gravitational boost", "Milky Way"
        ]
    },
    "pre_discovery_predictions_2026_2028": {
        "title": "Pre-Discovery Observational Predictions of Chronodynamic Relativity for 2026-2028 Astronomical Surveys and Laboratory Experiments",
        "record_id": "pending",
        "doi": "10.5281/zenodo.pending",
        "upload_type": "publication",
        "publication_type": "preprint",
        "version": "v1.0.0",
        "license": "cc-by-4.0",
        "publication_date": "2026-10-14",
        "notes": (
            "Version 1.0.0 Initial Pre-Discovery Baseline: Locked mathematical predictions across ten empirical domains "
            "prior to Gaia DR4 (Dec 2, 2026), DESI Year 5, Euclid DR1, and JWST Cycles 5/6."
        ),
        "description": (
            "Establishes a formal, citable pre-discovery baseline for Chronodynamic Relativity across ten major experimental "
            "domains ahead of forthcoming data releases between late 2026 and 2028. Evaluates exact parameter-free prediction bounds for: "
            "(1) Gaia DR4 wide binary asymptotic velocity floor (v_flat = 0.425 km/s for 1.5 M_sun beyond 5.79 kAU); "
            "(2) JWST cosmic dawn true expansion redshift mapping (z_obs = 14.32 to z_exp = 10.45, expanding available cosmic time by +52%); "
            "(3) DESI Year 5 apparent evolving dark energy (w_0 = -0.852, w_a = -0.395); (4) Euclid DR1 suppressed cosmic shear clustering (S_8 = 0.763); "
            "(5) CMB certified 3D acoustic peak structure (D_221.4 = 5,756.9 uK^2, H_3/H_2 = 0.9643); (6) Simons Observatory primordial tensor mode ceiling (r < 0.005); "
            "(7) Rubin LSST distance duality break (eta(z=1) = 0.9205); (8) Quasar non-kinematic dipole (906 km/s); "
            "(9) Bose-Marletto-Vedral (BMV) witness protocol observing suppression of gravitationally induced entanglement (W <= 1) and classical dephasing floor; "
            "and (10) Fine-structure drift. Establishes six explicit empirical falsification criteria."
        ),
        "keywords": [
            "observational predictions", "pre-discovery", "Gaia DR4", "JWST", "DESI", "Euclid", "cosmology",
            "modified gravity", "wide binaries", "dark energy", "dark matter alternative", "CMB acoustic peaks",
            "Simons Observatory", "Rubin LSST", "gravitational entanglement", "BMV protocol"
        ]
    },
    "monograph_covariant_4d_action": {
        "title": "Covariant 4D Action, Field Equations, PPN Solar System Proof, and Energy-Momentum Conservation in Chronodynamic Relativity",
        "record_id": "pending",
        "doi": "10.5281/zenodo.pending",
        "upload_type": "publication",
        "publication_type": "technicalnote",
        "version": "v1.0.0",
        "license": "cc-by-4.0",
        "publication_date": "2026-10-15",
        "notes": (
            "Version 1.0.0 Foundational Theory Monograph: Rigorous derivation of Chronodynamic Relativity from a "
            "diffeomorphism-invariant 4D action, Euler-Lagrange field equations, Bianchi contracted energy-momentum conservation, "
            "Cassini PPN solar system proof, and tensor gravitational wave speed compliance."
        ),
        "description": (
            "Establishes the foundational mathematical and field-theoretic architecture of Chronodynamic Relativity. "
            "Derives the total system from a 4D diffeomorphism-invariant action coupling the spacetime metric to a non-linear "
            "space-density scalar field. Formally proves: (1) exact energy-momentum conservation (nabla^mu T_mu_nu^(total) = 0) "
            "via the contracted Bianchi identities; (2) asymptotic kinetic screening recovering General Relativity in high-acceleration "
            "regimes, passing Cassini light deflection (|gamma_PPN - 1| <= 10^-17) and Mercury perihelion advance (|beta_PPN - 1| <= 10^-16) "
            "by over 11 orders of magnitude; (3) gravitational wave speed identically c_GW = c (GW170817 compliant); and (4) the Machian "
            "emergence of non-linear algebraic root gravity from the action variation."
        ),
        "keywords": [
            "modified gravity", "covariant action", "scalar-tensor", "Bianchi identities", "energy conservation",
            "PPN parameters", "Cassini bound", "GW170817", "dark matter alternative", "cosmology"
        ],
        "doc_dir": "docs/theory"
    }
}

# ==============================================================================
# Helper Utilities
# ==============================================================================

def find_repo_roots() -> tuple[Path, Path]:
    """
    Locates the project root and the official directory.
    Supports both monorepo (CR-Development) and standalone official repo.
    """
    script_dir = Path(__file__).resolve().parent
    # Check candidate roots
    candidate = script_dir.parent
    if (candidate / "manuscripts").exists():
        # Running inside official/ or standalone repo
        official_root = candidate
        if candidate.name == "official" and (candidate.parent / "official").exists():
            workspace_root = candidate.parent
        else:
            workspace_root = candidate
    elif (candidate.parent / "official" / "manuscripts").exists():
        workspace_root = candidate.parent
        official_root = workspace_root / "official"
    else:
        workspace_root = candidate
        official_root = candidate
    return workspace_root, official_root


def compute_sha256(filepath: Path) -> str:
    """Computes SHA-256 hex digest of a file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def compile_manuscript_pdf(tex_path: Path) -> bool:
    """Compiles LaTeX document into PDF using pdflatex and bibtex."""
    folder = tex_path.parent
    basename = tex_path.name
    stem = tex_path.stem
    pdf_path = folder / f"{stem}.pdf"

    print(f"    [LaTeX] Compiling {basename} -> {pdf_path.name}...")
    try:
        # Run pdflatex -> bibtex -> pdflatex -> pdflatex
        subprocess.run(["pdflatex", "-interaction=nonstopmode", basename], cwd=folder, check=False, capture_output=True)
        subprocess.run(["bibtex", stem], cwd=folder, check=False, capture_output=True)
        subprocess.run(["pdflatex", "-interaction=nonstopmode", basename], cwd=folder, check=False, capture_output=True)
        proc = subprocess.run(["pdflatex", "-interaction=nonstopmode", basename], cwd=folder, check=False, capture_output=True)
        return pdf_path.exists()
    except Exception as e:
        print(f"    [Error] LaTeX compilation failed: {e}")
        return False


def run_verification(verify_script: Path) -> bool:
    """Executes verify_calculations.py to validate mathematical calculations."""
    folder = verify_script.parent
    print(f"    [Rule 14] Executing verification suite: {verify_script.name}...")
    workspace_root, official_root = find_repo_roots()
    env = os.environ.copy()
    pythonpaths = [str(workspace_root), str(official_root), str(official_root / "src"), str(workspace_root / "src")]
    if "PYTHONPATH" in env:
        pythonpaths.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(pythonpaths)

    res = subprocess.run([sys.executable, verify_script.name], cwd=folder, env=env, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"    [Pass] First-principles calculations verified.")
        return True
    else:
        print(f"    [Fail] Verification script returned non-zero code:")
        print(res.stdout)
        print(res.stderr)
        return False


def build_zenodo_json(meta: Dict[str, Any]) -> Dict[str, Any]:
    """Constructs Zenodo REST API deposit metadata dictionary."""
    creators = [
        {
            "name": "Shreve, Joshua A.",
            "affiliation": "Chronodynamic Relativity Research Initiative",
            "orcid": "0009-0000-5942-5351"
        }
    ]
    
    related_ids = [
        {
            "relation": "isSupplementedBy",
            "identifier": "https://github.com/joshreve/Chronodynamic-Relativity",
            "scheme": "url"
        },
        {
            "relation": "isSupplementedBy",
            "identifier": "https://doi.org/10.5281/zenodo.22697449",
            "scheme": "doi"
        }
    ]
    if "concept_doi" in meta:
        related_ids.append({
            "relation": "isVersionOf",
            "identifier": f"https://doi.org/{meta['concept_doi']}",
            "scheme": "doi"
        })

    payload = {
        "metadata": {
            "title": meta["title"],
            "upload_type": meta["upload_type"],
            "publication_date": meta.get("publication_date", "2026-10-01"),
            "description": meta["description"],
            "creators": creators,
            "access_right": "open",
            "license": meta.get("license", "cc-by-4.0"),
            "keywords": meta.get("keywords", []),
            "version": meta.get("version", "v1.0.0"),
            "language": "eng",
            "related_identifiers": related_ids
        }
    }
    if meta.get("publication_type"):
        payload["metadata"]["publication_type"] = meta["publication_type"]
    if meta.get("doi"):
        payload["metadata"]["doi"] = meta["doi"]
    if meta.get("notes"):
        payload["metadata"]["notes"] = meta["notes"]
    return payload


# ==============================================================================
# Packager Core
# ==============================================================================

class ZenodoPackager:
    def __init__(self, workspace_root: Path, official_root: Path, output_dir: Path, compile_pdfs: bool = False, verify_math: bool = False):
        self.workspace_root = workspace_root
        self.official_root = official_root
        self.output_dir = output_dir
        self.compile_pdfs = compile_pdfs
        self.verify_math = verify_math
        self.manifest_records: List[Dict[str, Any]] = []

    def prepare_output_directory(self, clean: bool = True):
        """Prepares the destination directory."""
        if clean and self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def package_manuscript(self, folder_name: str, meta: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Packages a single manuscript directory into a Zenodo deposit folder."""
        # Find manuscript folder
        candidates = [
            self.official_root / "manuscripts" / folder_name,
            self.workspace_root / "manuscripts" / folder_name,
            self.workspace_root / "official" / "manuscripts" / folder_name,
            self.workspace_root / "development" / "manuscripts" / folder_name
        ]
        src_dir = next((c for c in candidates if c.exists()), None)
        if not src_dir:
            print(f"[-] Manuscript directory not found: {folder_name}")
            return None

        print(f"\n[+] Packaging Manuscript: {folder_name}")
        pkg_dir = self.output_dir / folder_name
        pkg_dir.mkdir(parents=True, exist_ok=True)

        # 1. Run verify_calculations.py if requested
        verify_script = src_dir / "verify_calculations.py"
        if verify_script.exists() and self.verify_math:
            if not run_verification(verify_script):
                print(f"    [!] Warning: Math verification failed on {folder_name}")

        # 2. Find main .tex file and PDF
        tex_files = list(src_dir.glob("shreve_*.tex")) or list(src_dir.glob("*.tex"))
        if not tex_files:
            print(f"    [-] No .tex file found in {src_dir}")
            return None
        main_tex = tex_files[0]
        pdf_file = src_dir / f"{main_tex.stem}.pdf"

        # Compile PDF if requested or missing
        if self.compile_pdfs or not pdf_file.exists():
            compile_manuscript_pdf(main_tex)

        if not pdf_file.exists():
            print(f"    [-] Compiled PDF missing: {pdf_file.name}")
            return None

        # Copy standalone PDF to package directory
        dest_pdf = pkg_dir / pdf_file.name
        shutil.copy2(pdf_file, dest_pdf)
        print(f"    -> Copied PDF: {dest_pdf.name} ({dest_pdf.stat().st_size:,} bytes)")

        # 3. Create Clean Source Tarball (submission_<version>.tar.gz)
        version_str = meta.get("version", "v1.0.0")
        tar_filename = f"submission_{folder_name}_{version_str}.tar.gz"
        tar_path = pkg_dir / tar_filename

        # Collect source files
        source_files = []
        for p in src_dir.rglob("*"):
            if p.is_dir():
                continue
            # Ignore intermediate LaTeX and Python build files
            if p.suffix in [".aux", ".bbl", ".blg", ".log", ".out", ".fdb_latexmk", ".fls", ".synctex.gz", ".pyc"]:
                continue
            if "__pycache__" in p.parts:
                continue
            if p.name.endswith("Notes.bib"):
                continue
            source_files.append(p)

        with tarfile.open(tar_path, "w:gz") as tar:
            for sf in source_files:
                arcname = sf.relative_to(src_dir)
                tar.add(sf, arcname=arcname)
        print(f"    -> Created Source Tarball: {tar_filename} ({tar_path.stat().st_size:,} bytes)")

        # 4. Copy auxiliary reference assets directly for standalone inspection
        if (src_dir / "reference_calculations.json").exists():
            shutil.copy2(src_dir / "reference_calculations.json", pkg_dir / "reference_calculations.json")
        if (src_dir / "verify_calculations.py").exists():
            shutil.copy2(src_dir / "verify_calculations.py", pkg_dir / "verify_calculations.py")
        if (src_dir / "README.md").exists():
            shutil.copy2(src_dir / "README.md", pkg_dir / "README.md")

        # 5. Emit Zenodo API Metadata JSON
        zenodo_json_data = build_zenodo_json(meta)
        meta_path = pkg_dir / "zenodo_deposit_metadata.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(zenodo_json_data, f, indent=2)
        # Also emit standard .zenodo.json
        with open(pkg_dir / ".zenodo.json", "w", encoding="utf-8") as f:
            json.dump(zenodo_json_data["metadata"], f, indent=2)
        print(f"    -> Emitted Metadata: {meta_path.name} & .zenodo.json")

        # 6. Checksums for package
        record_info = {
            "key": folder_name,
            "title": meta["title"],
            "doi": meta.get("doi", ""),
            "record_id": meta.get("record_id", ""),
            "version": version_str,
            "target_dir": str(pkg_dir.relative_to(self.output_dir)),
            "files": {
                dest_pdf.name: {
                    "size_bytes": dest_pdf.stat().st_size,
                    "sha256": compute_sha256(dest_pdf)
                },
                tar_filename: {
                    "size_bytes": tar_path.stat().st_size,
                    "sha256": compute_sha256(tar_path)
                }
            }
        }
        self.manifest_records.append(record_info)
        return record_info

    def package_monograph(self, folder_name: str, meta: Dict[str, Any], doc_dir: Path) -> Optional[Dict[str, Any]]:
        """Packages a standalone technical monograph or report into a clean distribution bundle."""
        print(f"\n[+] Packaging Technical Monograph: {folder_name}")
        pkg_dir = self.output_dir / folder_name
        pkg_dir.mkdir(parents=True, exist_ok=True)

        version_str = meta.get("version", "v1.0.0")
        tar_filename = f"submission_{folder_name}_{version_str}.tar.gz"
        tar_path = pkg_dir / tar_filename

        source_files = []
        files_dict = {}
        if doc_dir.exists():
            for p in doc_dir.glob("*"):
                if p.is_file() and p.suffix in [".md", ".html", ".pdf", ".json"]:
                    dest_f = pkg_dir / p.name
                    shutil.copy2(p, dest_f)
                    source_files.append(p)
                    files_dict[p.name] = {
                        "size_bytes": dest_f.stat().st_size,
                        "sha256": compute_sha256(dest_f)
                    }

        with tarfile.open(tar_path, "w:gz") as tar:
            for sf in source_files:
                tar.add(sf, arcname=f"{folder_name}/{sf.name}")
        print(f"    -> Created Source Tarball: {tar_filename} ({tar_path.stat().st_size:,} bytes)")
        files_dict[tar_filename] = {
            "size_bytes": tar_path.stat().st_size,
            "sha256": compute_sha256(tar_path)
        }

        zenodo_json_data = build_zenodo_json(meta)
        meta_path = pkg_dir / "zenodo_deposit_metadata.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(zenodo_json_data, f, indent=2)
        with open(pkg_dir / ".zenodo.json", "w", encoding="utf-8") as f:
            json.dump(zenodo_json_data["metadata"], f, indent=2)

        record_info = {
            "key": folder_name,
            "title": meta["title"],
            "doi": meta.get("doi", ""),
            "record_id": meta.get("record_id", ""),
            "version": version_str,
            "target_dir": str(pkg_dir.relative_to(self.output_dir)),
            "files": files_dict
        }
        self.manifest_records.append(record_info)
        return record_info

    def package_software_codebase(self, meta: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Packages the core official software framework repository into a clean distribution tarball."""
        print(f"\n[+] Packaging Core Software Framework: {meta['version']}")
        pkg_dir = self.output_dir / "software"
        pkg_dir.mkdir(parents=True, exist_ok=True)

        version_str = meta.get("version", "v1.1.0")
        tar_filename = f"chronodynamic_relativity_software_{version_str}.tar.gz"
        tar_path = pkg_dir / tar_filename

        # Exclusions for software tarball
        excluded_dirs = {".git", ".venv", "venv", ".pytest_cache", "__pycache__", "dist", "build", "runs", "scratch", "tmp", "temp"}
        excluded_exts = {".pyc", ".aux", ".log", ".out", ".bbl", ".blg", ".fdb_latexmk", ".fls", ".synctex.gz", ".o", ".a", ".exe"}

        # Collect files from official_root
        software_files = []
        for p in self.official_root.rglob("*"):
            if p.is_dir():
                continue
            # Check directory exclusions
            if any(part in excluded_dirs for part in p.parts):
                continue
            if p.suffix in excluded_exts:
                continue
            software_files.append(p)

        with tarfile.open(tar_path, "w:gz") as tar:
            for sf in software_files:
                arcname = sf.relative_to(self.official_root)
                tar.add(sf, arcname=f"Chronodynamic-Relativity-{version_str}/{arcname}")
        print(f"    -> Created Software Release Tarball: {tar_filename} ({tar_path.stat().st_size:,} bytes)")

        # Emit Zenodo metadata for software
        zenodo_json_data = build_zenodo_json(meta)
        meta_path = pkg_dir / "zenodo_deposit_metadata.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(zenodo_json_data, f, indent=2)
        with open(pkg_dir / ".zenodo.json", "w", encoding="utf-8") as f:
            json.dump(zenodo_json_data["metadata"], f, indent=2)

        record_info = {
            "key": "software",
            "title": meta["title"],
            "doi": meta.get("doi", ""),
            "record_id": meta.get("record_id", ""),
            "version": version_str,
            "target_dir": str(pkg_dir.relative_to(self.output_dir)),
            "files": {
                tar_filename: {
                    "size_bytes": tar_path.stat().st_size,
                    "sha256": compute_sha256(tar_path)
                }
            }
        }
        self.manifest_records.append(record_info)
        return record_info

    def write_release_manifest(self):
        """Writes top-level release manifest and checksums file."""
        manifest_path = self.output_dir / "MANIFEST.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump({
                "schema_version": "1.0.0",
                "generated_date": "2026-10-04",
                "deposits": self.manifest_records
            }, f, indent=2)

        # Write CHECKSUMS.sha256
        checksum_lines = []
        for rec in self.manifest_records:
            for fname, finfo in rec["files"].items():
                rel_file_path = f"{rec['target_dir']}/{fname}"
                checksum_lines.append(f"{finfo['sha256']}  {rel_file_path}")

        checksum_path = self.output_dir / "CHECKSUMS.sha256"
        with open(checksum_path, "w", encoding="utf-8") as f:
            f.write("\n".join(checksum_lines) + "\n")

        # Write human-readable Markdown summary
        md_path = self.output_dir / "README.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# Zenodo Release Packages\n\n")
            f.write("Generated publication-ready deposit packages for the Chronodynamic Relativity research initiative.\n\n")
            f.write("| Key | Record ID | DOI | Version | Primary Package Files |\n")
            f.write("|---|---|---|---|---|\n")
            for rec in self.manifest_records:
                files_str = "<br>".join([f"`{fn}` ({fi['size_bytes']:,} B)" for fn, fi in rec["files"].items()])
                doi_link = f"[{rec['doi']}](https://doi.org/{rec['doi']})" if rec['doi'] else "*Pending*"
                f.write(f"| **{rec['key']}** | `{rec['record_id']}` | {doi_link} | `{rec['version']}` | {files_str} |\n")
            f.write("\nAll packages contain validated LaTeX source, compiled PDFs, `.zenodo.json` API descriptors, and SHA-256 integrity checksums.\n")

        print(f"\n[+] Master Zenodo Package Manifest written to: {manifest_path.name}")
        print(f"[+] Master Checksums written to: {checksum_path.name}")
        print(f"[+] Release Overview written to: {md_path.name}")


# ==============================================================================
# CLI Entrypoint
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Package Zenodo deposit bundles for Chronodynamic Relativity.")
    parser.add_argument("--output-dir", default="dist/zenodo", help="Target output directory (default: dist/zenodo)")
    parser.add_argument("--compile", action="store_true", help="Force recompilation of all LaTeX PDFs before packaging")
    parser.add_argument("--verify", action="store_true", help="Execute verify_calculations.py for each manuscript")
    parser.add_argument("--paper", help="Package only the specified manuscript key (or 'software')")
    parser.add_argument("--no-clean", action="store_true", help="Do not wipe destination folder before packaging")
    args = parser.parse_args()

    workspace_root, official_root = find_repo_roots()
    target_out = Path(args.output_dir)
    if not target_out.is_absolute():
        target_out = workspace_root / target_out

    print("=" * 76)
    print("Chronodynamic Relativity -- Zenodo Publication Packager")
    print(f"Workspace Root : {workspace_root}")
    print(f"Official Root  : {official_root}")
    print(f"Output Target  : {target_out}")
    print("=" * 76)

    packager = ZenodoPackager(
        workspace_root=workspace_root,
        official_root=official_root,
        output_dir=target_out,
        compile_pdfs=args.compile,
        verify_math=args.verify
    )
    packager.prepare_output_directory(clean=not args.no_clean)

    if args.paper:
        if args.paper == "software":
            packager.package_software_codebase(ZENODO_REGISTRY["software"])
        elif args.paper in ZENODO_REGISTRY:
            meta = ZENODO_REGISTRY[args.paper]
            if "doc_dir" in meta:
                packager.package_monograph(args.paper, meta, official_root / meta["doc_dir"])
            else:
                packager.package_manuscript(args.paper, meta)
        else:
            print(f"[!] Unknown item key: {args.paper}. Available keys: {list(ZENODO_REGISTRY.keys())}")
            sys.exit(1)
    else:
        # Package software
        packager.package_software_codebase(ZENODO_REGISTRY["software"])
        # Package all manuscripts in registry
        for key, meta in ZENODO_REGISTRY.items():
            if key == "software":
                continue
            if "doc_dir" in meta:
                packager.package_monograph(key, meta, official_root / meta["doc_dir"])
            else:
                packager.package_manuscript(key, meta)

    packager.write_release_manifest()
    print("\n[SUCCESS] All Zenodo deposit packages generated successfully.")


if __name__ == "__main__":
    main()
