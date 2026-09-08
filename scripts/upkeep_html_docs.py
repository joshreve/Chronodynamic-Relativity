r"""
Upkeep Documentation Index & Universal Navigation Header
========================================================
Maintains mathematical, structural, and navigation consistency across the Chronodynamic Relativity
documentation suites:
  1. Distinguishes Development vs Official documentation trees:
     - Development (`development/docs/`): Internal investigations, Boltzmann solvers, MCMC runs, working notes.
     - Official (`official/docs/` & `Chronodynamic-Relativity/docs/`): Canonical 4-pillar benchmarks, foundational monographs, ready to share.
  2. Ensures only ONE `index.html` exists per root (`docs/index.html` and `development/docs/index.html`).
     All sub-portals are explicitly named (e.g. `analyses_overview.html`, `cosmic_expansion_overview.html`).
  3. Ensures all HTML pages have a clean top navigation bar returning to the root Documentation Index without self-references.
  4. Supports fast document upkeeps without regenerating the 175-galaxy SPARC Atlas unless `--rerun-atlas` is passed.
"""

import os
import sys
import re
import glob
import argparse

# Ensure repo root and official are on sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
OFFICIAL_DIR = os.path.join(REPO_ROOT, 'official')
if OFFICIAL_DIR not in sys.path:
    sys.path.insert(0, OFFICIAL_DIR)

TOP_NAV_CSS = """
<style id="cr-universal-top-nav-style">
.cr-top-nav-bar {
    background: #0f172a !important;
    color: #ffffff !important;
    padding: 12px 28px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 99999 !important;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif !important;
}
.cr-nav-return-btn {
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
    background: #1e293b !important;
    color: #38bdf8 !important;
    text-decoration: none !important;
    font-weight: 600 !important;
    font-size: 0.9em !important;
    padding: 7px 16px !important;
    border-radius: 6px !important;
    border: 1px solid #334155 !important;
    transition: all 0.2s ease !important;
}
.cr-nav-return-btn:hover {
    background: #334155 !important;
    color: #ffffff !important;
    border-color: #38bdf8 !important;
}
.cr-nav-brand {
    font-size: 0.95em !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    letter-spacing: 0.5px !important;
}
@media (max-width: 640px) {
    .cr-top-nav-bar { padding: 10px 16px !important; flex-direction: column !important; gap: 8px !important; align-items: flex-start !important; }
}
</style>
"""

def generate_master_index_html():
    """Builds the comprehensive Official Master Documentation Index at docs/index.html."""
    return r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chronodynamic Relativity | Documentation & Empirical Research Index</title>
    <script>
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$']]
            },
            svg: { fontCache: 'global' }
        };
    </script>
    <script type="text/javascript" id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
    <style>
        :root {
            --primary: #0f172a;
            --primary-accent: #2563eb;
            --secondary: #0d9488;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --border: #e2e8f0;
            --text-main: #1e293b;
            --text-muted: #64748b;
        }
        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            margin: 0;
            padding: 0;
            background-color: var(--bg);
            color: var(--text-main);
            line-height: 1.6;
        }
        .hero-banner {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0369a1 100%);
            color: #ffffff;
            padding: 50px 30px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }
        .hero-banner h1 {
            font-size: 2.6em;
            margin: 0 0 10px 0;
            letter-spacing: -0.5px;
            font-weight: 700;
        }
        .hero-banner p {
            font-size: 1.15em;
            max-width: 860px;
            margin: 0 auto 20px auto;
            color: #cbd5e1;
            font-weight: 300;
        }
        .badge-bar {
            display: flex;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 15px;
        }
        .badge {
            background: rgba(255, 255, 255, 0.12);
            border: 1px solid rgba(255, 255, 255, 0.25);
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            color: #e2e8f0;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 24px;
        }
        .section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 2px solid var(--border);
            padding-bottom: 10px;
            margin: 40px 0 24px 0;
        }
        .section-header h2 {
            margin: 0;
            color: var(--primary);
            font-size: 1.6em;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
            gap: 22px;
            margin-bottom: 30px;
        }
        .card {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 24px;
            border: 1px solid var(--border);
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.04);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.2s ease;
        }
        .card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.08);
            border-color: #cbd5e1;
        }
        .card h3 {
            margin-top: 0;
            color: var(--primary);
            font-size: 1.25em;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .card p {
            color: var(--text-muted);
            font-size: 0.95em;
            margin: 8px 0 18px 0;
            flex-grow: 1;
        }
        .card-link {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            color: var(--primary-accent);
            text-decoration: none;
            font-weight: 600;
            font-size: 0.92em;
        }
        .card-link:hover {
            color: #1d4ed8;
            text-decoration: underline;
        }
        .status-pill {
            font-size: 0.75em;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: inline-block;
            margin-bottom: 8px;
        }
        .status-official { background: #dbeafe; color: #1e40af; }
        .status-pillar { background: #ccfbf1; color: #0f766e; }
        .status-info { background: #f1f5f9; color: #475569; }
        .footer {
            text-align: center;
            padding: 40px;
            color: var(--text-muted);
            font-size: 0.9em;
            border-top: 1px solid var(--border);
            background: #ffffff;
            margin-top: 60px;
        }
    </style>
</head>
<body>

    <div class="hero-banner">
        <h1>Chronodynamic Relativity</h1>
        <p>A Covariant Scalar-Tensor Theory of Variable Space Density & Metric Clock Invariance: Unifying Dark Matter Halos, Dark Energy, and Early JWST Horizons.</p>
        <div class="badge-bar">
            <span class="badge">&alpha;<sub>0</sub> = 1.20 &times; 10<sup>-10</sup> m/s<sup>2</sup></span>
            <span class="badge">n = 0.2385 (Universal Temporal Power)</span>
            <span class="badge">&chi;<sup>2</sup>/dof = 0.865 (Pantheon+ SNe Ia)</span>
            <span class="badge">&chi;<sup>2</sup>/dof = 1.07 (175 SPARC Galaxies)</span>
            <span class="badge">0 Phantom Dark Fluids</span>
        </div>
    </div>

    <div class="container">

        <!-- CORE MONOGRAPHS & FORMALISMS -->
        <div class="section-header">
            <h2>Foundational Monographs & Formalisms</h2>
            <span class="badge" style="background:#f1f5f9; color:#475569;">Core Rigor & Mathematics</span>
        </div>
        <div class="grid">
            <div class="card">
                <div>
                    <span class="status-pill status-official">Canonical Monograph</span>
                    <h3>Mathematical Foundations & Symbology</h3>
                    <p>Complete theoretical compilation: Action principle, stress-energy conservation, exact field equations, metric conventions, and rigorous symbology glossary.</p>
                </div>
                <a href="MATHEMATICAL_FOUNDATIONS_AND_SYMBOLOGY.html" class="card-link">View Monograph &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-official">Reference Matrix</span>
                    <h3>Parameter Definitions & Empirical Applications</h3>
                    <p>Comprehensive mathematical dictionary of all cosmological, galactic, lensing, and quantum parameters with explicit SI units, values, and cross-references.</p>
                </div>
                <a href="PARAMETER_DEFINITIONS_AND_APPLICATIONS.html" class="card-link">View Parameter Reference &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-official">Methodology</span>
                    <h3>Theoretical Niche & Observational Methodology</h3>
                    <p>Methodological analysis contrasting Chronodynamic Relativity against &Lambda;CDM, MOND/AQUAL, and MOG/STVG across relativistic symmetries and experimental regimes.</p>
                </div>
                <a href="THEORETICAL_NICHE_AND_OBSERVATIONAL_METHODOLOGY.html" class="card-link">View Methodology &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-official">Registry</span>
                    <h3>HTML Documentation Registry & Purpose Tracker</h3>
                    <p>Catalog of all generated interactive reports, test suites, and empirical diagnostic pages across the entire repository.</p>
                </div>
                <a href="HTML_DOCUMENTATION_REGISTRY.html" class="card-link">View Documentation Registry &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-official">Bibliography</span>
                    <h3>Empirical & Theoretical References</h3>
                    <p>Full academic citations and bibliographic records for all observational datasets (Planck, SPARC, Pantheon+, DESI, JWST, EHT) and foundational physics literature.</p>
                </div>
                <a href="REFERENCES.html" class="card-link">View References &rarr;</a>
            </div>
        </div>

        <!-- THE FOUR EMPIRICAL PILLARS -->
        <div class="section-header">
            <h2>The Four Empirical Pillars</h2>
            <span class="badge" style="background:#ccfbf1; color:#0f766e;">Benchmark Suite</span>
        </div>
        <div class="grid">
            <div class="card">
                <div>
                    <span class="status-pill status-pillar">Unified Suite</span>
                    <h3>Unified 4-Pillar Empirical Benchmark</h3>
                    <p>Master synthesis evaluating Chronodynamic Relativity simultaneously across SNe Ia, SPARC RAR, Strong Gravitational Lensing, and JWST early massive galaxy epochs.</p>
                </div>
                <a href="analyses/unified_4pillar_benchmark_overview.html" class="card-link">View 4-Pillar Overview &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-pillar">Pillar I</span>
                    <h3>Cosmic Expansion & Pantheon+ Supernovae</h3>
                    <p>Environmental clock-shift distance modulus fit over 1,701 Type Ia Supernovae ($\chi^2/\text{dof} = 0.865$), eliminating the requirement for dark energy.</p>
                </div>
                <a href="analyses/cosmic_expansion/cosmic_expansion_overview.html" class="card-link">View Pillar I Overview &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-pillar">Pillar II</span>
                    <h3>Galactic Kinematics & 175 SPARC Galaxies</h3>
                    <p>Non-linear root gravity engine fitting 175 SPARC galactic rotation curves ($\chi^2/\text{dof} = 1.07$) without dark matter halos.</p>
                </div>
                <a href="analyses/galactic_rotation/atlas.html" class="card-link">View SPARC 175 Atlas &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-pillar">Pillar III</span>
                    <h3>Strong Gravitational Lensing</h3>
                    <p>Relativistic line-of-sight integration reproducing SLACS and CASTLES Einstein radii and light deflection across massive elliptical lens galaxies without dark matter halos.</p>
                </div>
                <a href="analyses/strong_lensing/strong_lensing_overview.html" class="card-link">View Strong Lensing Overview &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-pillar">Pillar IV</span>
                    <h3>Early Massive Galaxies (JADES z > 14)</h3>
                    <p>Analysis of high-redshift massive galaxy formation observed by JWST, resolved naturally by accelerated early clock rates without unphysical dark matter spikes.</p>
                </div>
                <a href="analyses/early_universe/jades_z14.html" class="card-link">View JADES z > 14 Analysis &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-pillar">Omnibus Portal</span>
                    <h3>Omnibus Analysis & Diagnostics Portal</h3>
                    <p>Interactive dashboard comparing empirical performance and mathematical deviations across all observational domains.</p>
                </div>
                <a href="analyses/analyses_overview.html" class="card-link">View Omnibus Analyses &rarr;</a>
            </div>
        </div>

        <!-- THEORETICAL INVESTIGATIONS & ASTROPHYSICS -->
        <div class="section-header">
            <h2>Theoretical Deep Dives & Astrophysical Diagnostics</h2>
            <span class="badge" style="background:#f1f5f9; color:#475569;">Specialized Reports</span>
        </div>
        <div class="grid">
            <div class="card">
                <div>
                    <span class="status-pill status-info">Field Theory</span>
                    <h3>Fundamental Equations & Action</h3>
                    <p>Derivation of the covariant scalar-tensor action, stress-energy conservation, and cosmological field equations.</p>
                </div>
                <a href="analyses/theory/fundamental_equations.html" class="card-link">View Equations &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-info">Duality</span>
                    <h3>CDM Inverse-Poisson Duality</h3>
                    <p>Derivation demonstrating the exact mathematical mapping between phantom dark matter halos and coordinate clock lapse scaling.</p>
                </div>
                <a href="analyses/theory/cdm_unification_duality.html" class="card-link">View Duality Analysis &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-info">Bayesian MCMC</span>
                    <h3>Bayesian Multi-Tier Model Selection</h3>
                    <p>Nested sampling and MCMC posterior evaluations assessing Bayesian Information Criterion (&Delta;BIC) against &Lambda;CDM.</p>
                </div>
                <a href="analyses/theory/bayesian_posteriors.html" class="card-link">View Bayesian Posteriors &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-info">QFT</span>
                    <h3>Quantum Kinematics & Phase Shifts</h3>
                    <p>Analysis of COW neutron interferometry, microscopic clock shifts, and equivalence principle bounds under scalar space-density.</p>
                </div>
                <a href="analyses/theory/scale_invariance_quantum_refraction.html" class="card-link">View Quantum Phase Shifts &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-info">Black Holes</span>
                    <h3>EHT Shadow Metrics & Horizons</h3>
                    <p>Event Horizon Telescope shadow profiles, photon sphere radius, and singularity avoidance in non-linear scalar gravity.</p>
                </div>
                <a href="analyses/black_holes/metrics.html" class="card-link">View Black Hole Metrics &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-info">Multi-Messenger</span>
                    <h3>GW170817 Speed of Gravity Constraint</h3>
                    <p>Analytical proof of exact tensor gravitational wave propagation at light speed ($c_g = c$), satisfying multi-messenger neutron star bounds.</p>
                </div>
                <a href="analyses/theory/gw170817_constraint_report.html" class="card-link">View GW170817 Report &rarr;</a>
            </div>
        </div>

    </div>

    <div class="footer">
        Chronodynamic Relativity Research Suite &bull; Rigorous Open-Source Theoretical Physics &bull; Rochester Institute of Technology Alumni Research Initiative
    </div>

</body>
</html>
"""

def generate_development_index_html():
    """Builds the comprehensive Development Research & Investigations Index at development/docs/index.html."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chronodynamic Relativity | Development & Active Research Index</title>
    <script>
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$']]
            },
            svg: { fontCache: 'global' }
        };
    </script>
    <script type="text/javascript" id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
    <style>
        :root {
            --primary: #0f172a;
            --primary-accent: #6366f1;
            --secondary: #0ea5e9;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --border: #e2e8f0;
            --text-main: #1e293b;
            --text-muted: #64748b;
        }
        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            margin: 0;
            padding: 0;
            background-color: var(--bg);
            color: var(--text-main);
            line-height: 1.6;
        }
        .hero-banner {
            background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #0369a1 100%);
            color: #ffffff;
            padding: 50px 30px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }
        .hero-banner h1 {
            font-size: 2.5em;
            margin: 0 0 10px 0;
            letter-spacing: -0.5px;
            font-weight: 700;
        }
        .hero-banner p {
            font-size: 1.15em;
            max-width: 900px;
            margin: 0 auto 20px auto;
            color: #cbd5e1;
            font-weight: 300;
        }
        .badge-bar {
            display: flex;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 15px;
        }
        .badge {
            background: rgba(255, 255, 255, 0.12);
            border: 1px solid rgba(255, 255, 255, 0.25);
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            color: #e2e8f0;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 24px;
        }
        .section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 2px solid var(--border);
            padding-bottom: 10px;
            margin: 40px 0 24px 0;
        }
        .section-header h2 {
            margin: 0;
            color: var(--primary);
            font-size: 1.5em;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
            gap: 22px;
            margin-bottom: 30px;
        }
        .card {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 24px;
            border: 1px solid var(--border);
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.04);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.2s ease;
        }
        .card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.08);
            border-color: #cbd5e1;
        }
        .card h3 {
            margin-top: 0;
            color: var(--primary);
            font-size: 1.2em;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .card p {
            color: var(--text-muted);
            font-size: 0.93em;
            margin: 8px 0 18px 0;
            flex-grow: 1;
        }
        .card-link {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            color: var(--primary-accent);
            text-decoration: none;
            font-weight: 600;
            font-size: 0.92em;
        }
        .card-link:hover {
            color: #4338ca;
            text-decoration: underline;
        }
        .status-pill {
            font-size: 0.75em;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: inline-block;
            margin-bottom: 8px;
        }
        .status-dev { background: #e0e7ff; color: #3730a3; }
        .status-boltzmann { background: #fef3c7; color: #92400e; }
        .status-astro { background: #dcfce7; color: #166534; }
        .status-quantum { background: #f3e8ff; color: #6b21a8; }
        .footer {
            text-align: center;
            padding: 40px;
            color: var(--text-muted);
            font-size: 0.9em;
            border-top: 1px solid var(--border);
            background: #ffffff;
            margin-top: 60px;
        }
    </style>
</head>
<body>

    <div class="hero-banner">
        <h1>Chronodynamic Relativity | Development & Active Research</h1>
        <p>Internal workspace repository for exploratory numerical simulations, in-progress Boltzmann perturbation codes, dynamic lag formulations, and ongoing research diagnostics.</p>
        <div class="badge-bar">
            <span class="badge">Repository: CR-Development (Internal)</span>
            <span class="badge">Phase: Active Experimental Research</span>
            <span class="badge">Paper II & III In-Work Studies</span>
            <span class="badge">50+ Empirical Investigations</span>
        </div>
        <div style="margin-top: 20px;">
            <a href="../../official/docs/index.html" style="color: #38bdf8; text-decoration: none; font-weight: 600; background: rgba(0,0,0,0.3); padding: 8px 18px; border-radius: 6px; border: 1px solid rgba(56, 189, 248, 0.4);">&larr; Switch to Official Public Documentation Suite</a>
        </div>
    </div>

    <div class="container">

        <!-- BOLTZMANN & CMB PERTURBATION INVESTIGATIONS -->
        <div class="section-header">
            <h2>Active Boltzmann Solver & CMB Perturbation Suites (Paper II)</h2>
            <span class="badge" style="background:#fef3c7; color:#92400e;">Paper II Studies</span>
        </div>
        <div class="grid">
            <div class="card">
                <div>
                    <span class="status-pill status-boltzmann">CLASS-CR Engine</span>
                    <h3>CLASS-CR Planck 2018 Power Spectrum</h3>
                    <p>Full Boltzmann perturbation solver integrating the coupled scalar-tensor fluid equations and acoustic peaks against Planck 2018 PR3 TT/TE/EE data.</p>
                </div>
                <a href="investigations/class_cr_planck_spectrum.html" class="card-link">View CLASS-CR Analysis &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-boltzmann">Boltzmann Solvers</span>
                    <h3>Coupled Oscillator High-&ell; Acoustic Peaks</h3>
                    <p>Investigation of scalar refractive coupling on early acoustic oscillation transfer functions and damping tail dissipation.</p>
                </div>
                <a href="investigations/cr_coupled_oscillator_cmb.html" class="card-link">View Coupled Oscillator Report &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-boltzmann">Low-&ell; Anomalies</span>
                    <h3>Low-&ell; Quadrupole Anomaly Suppression</h3>
                    <p>Analysis of horizon-scale space-density gradients damping anomalous low multipoles (&ell; = 2 to 5) in the Planck temperature spectrum.</p>
                </div>
                <a href="investigations/cr_aggressive_low_l_nodes.html" class="card-link">View Low-&ell; Anomaly Report &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-boltzmann">MCMC Sampling</span>
                    <h3>Unconstrained MCMC Likelihood Sweeps</h3>
                    <p>Full parameter space exploration investigating scalar tension degenerate modes across cosmological data sets.</p>
                </div>
                <a href="investigations/cr_unconstrained_best_fit.html" class="card-link">View Unconstrained MCMC &rarr;</a>
            </div>
        </div>

        <!-- ASTROPHYSICAL & GRAVITATIONAL INVESTIGATIONS -->
        <div class="section-header">
            <h2>In-Work Gravity, Dynamic Lag & Astrophysical Reports</h2>
            <span class="badge" style="background:#dcfce7; color:#166534;">Diagnostics</span>
        </div>
        <div class="grid">
            <div class="card">
                <div>
                    <span class="status-pill status-astro">Dynamic Vacuum</span>
                    <h3>Dynamic Lag Vacuum (V8 Formulation)</h3>
                    <p>Non-local memory-well and density-dependent relaxation rates modeling complex dynamic cluster collisions and gas-lensing offsets.</p>
                </div>
                <a href="investigations/v8_dynamic_lag_test.html" class="card-link">View Dynamic Lag Test &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-astro">Astrophysics</span>
                    <h3>Space Field Drag & Kinematic Jet Effects</h3>
                    <p>Analysis of ambient space-density drag on ultra-relativistic jets, GRB Lorentz factors, and high-energy photon propagation.</p>
                </div>
                <a href="investigations/astrophysical_space_field_effects.html" class="card-link">View Space Field Drag Report &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-astro">Galactic Surveys</span>
                    <h3>Outer Milky Way Decline (Gaia DR3)</h3>
                    <p>Detailed investigation comparing Gaia DR3 outer disk Keplerian decline with Chronodynamic root gravity and MOND predictions.</p>
                </div>
                <a href="investigations/gaia_decline_report.html" class="card-link">View Gaia Decline Report &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-astro">Fluid Mechanics</span>
                    <h3>Viscosity Displacement & Potential Wells</h3>
                    <p>Hydrodynamic simulations of scalar vacuum viscosity displacing effective mass distributions during high-velocity mergers.</p>
                </div>
                <a href="investigations/viscosity_displacement_report.html" class="card-link">View Viscosity Displacement Report &rarr;</a>
            </div>
        </div>

        <!-- QUANTUM & FUNDAMENTAL STUDIES -->
        <div class="section-header">
            <h2>Quantum, High-Energy & Fundamental Investigations</h2>
            <span class="badge" style="background:#f3e8ff; color:#6b21a8;">Fundamental Physics</span>
        </div>
        <div class="grid">
            <div class="card">
                <div>
                    <span class="status-pill status-quantum">Quantization</span>
                    <h3>Chronon Discreteness & Quantum Bounds</h3>
                    <p>Empirical constraints on the fundamental chronon timescale ($\tau_0$) and discreteness bounds from high-energy gamma-ray bursts.</p>
                </div>
                <a href="investigations/chronon_quantization.html" class="card-link">View Chronon Quantization &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-quantum">Quantum Mechanics</span>
                    <h3>Quantum Schrödinger Wavepacket Simulations</h3>
                    <p>Numerical integration of non-linear wavepacket propagation in variable scalar space-density potentials.</p>
                </div>
                <a href="investigations/quantum_schrodinger_simulation.html" class="card-link">View Schrödinger Simulation &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-quantum">Precision Tests</span>
                    <h3>Precision QED & Electron g-2 Shifts</h3>
                    <p>1-loop radiative corrections from quantum scalar density operators and laboratory bounds on preferred-frame Lorentz violation.</p>
                </div>
                <a href="investigations/laboratory_qed_bounds.html" class="card-link">View QED Bounds &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-quantum">Cosmic Rays</span>
                    <h3>UHECR Arrival Anisotropies</h3>
                    <p>Testing potential scalar refractive steering on ultra-high-energy cosmic ray propagation trajectories across the cosmic web.</p>
                </div>
                <a href="investigations/uhecr_anisotropy.html" class="card-link">View UHECR Report &rarr;</a>
            </div>
        </div>

        <!-- EXPLORATORY & PHENOMENOLOGICAL INVESTIGATIONS -->
        <div class="section-header">
            <h2>Exploratory & Phenomenological Investigations</h2>
            <span class="badge" style="background:#fef2f2; color:#991b1b;">In-Progress / Scaffolding</span>
        </div>
        <div class="grid">
            <div class="card">
                <div>
                    <span class="status-pill status-dev">Merger Hydro</span>
                    <h3>Cluster Mergers Overview</h3>
                    <p>Exploratory 1D kinematic profiles modeling supersonic baryonic shock decelerations and lag potential wells.</p>
                </div>
                <a href="investigations/cluster_mergers_overview.html" class="card-link">View Merger Overview &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-dev">Spectroscopy</span>
                    <h3>Quasar Alpha Dipole Map</h3>
                    <p>Mollweide projection mapping spatial space-density gradients against large-scale potential repellers.</p>
                </div>
                <a href="investigations/quasar_dipole.html" class="card-link">View Alpha Dipole Map &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-dev">Structure Formation</span>
                    <h3>Matter Power Spectrum P(k)</h3>
                    <p>Exploratory matter power spectrum transfer models evaluating growth rates and turnover scales.</p>
                </div>
                <a href="investigations/pk_spectrum.html" class="card-link">View P(k) Investigation &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-dev">Quantum Optics</span>
                    <h3>Hawking Radiation Dynamic Horizons</h3>
                    <p>Kinematic boundary oscillation models evaluating dynamical Casimir effect radiation mechanisms.</p>
                </div>
                <a href="investigations/hawking_radiation.html" class="card-link">View Hawking Radiation &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-dev">IGM Physics</span>
                    <h3>Lyman-Alpha Temperature Anomaly</h3>
                    <p>Coordinate clock-shift evaluations of intergalactic medium photoheating and spectral line widths.</p>
                </div>
                <a href="investigations/lyman_alpha.html" class="card-link">View Lyman-Alpha Report &rarr;</a>
            </div>
        </div>

        <!-- WORKING PAPERS & MONOGRAPHS -->
        <div class="section-header">
            <h2>Working Drafts & Development Theory Monographs</h2>
            <span class="badge" style="background:#e0e7ff; color:#3730a3;">Working Notes</span>
        </div>
        <div class="grid">
            <div class="card">
                <div>
                    <span class="status-pill status-dev">Working Paper</span>
                    <h3>Paper 1: Foundations & Early Galaxies (PDF Preview)</h3>
                    <p>Compiled PDF preview of Paper 1: Foundations of Chronodynamic Relativity and early JWST massive galaxy resolution.</p>
                </div>
                <a href="papers/paper1_jades_z14.pdf" class="card-link">View Paper 1 PDF &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-dev">Working Paper</span>
                    <h3>Paper 2: SNe Ia & Cosmic Expansion (PDF Preview)</h3>
                    <p>Compiled PDF preview of Paper 2: Cosmological clock-shift fitting of 1,701 Pantheon+ Type Ia supernovae.</p>
                </div>
                <a href="papers/paper2_pantheon_fit.pdf" class="card-link">View Paper 2 PDF &rarr;</a>
            </div>
            <div class="card">
                <div>
                    <span class="status-pill status-dev">Registry</span>
                    <h3>HTML Documentation Registry & Purpose Tracker</h3>
                    <p>Classification catalog of all official, development, and simulation HTML documents in the repository.</p>
                </div>
                <a href="HTML_DOCUMENTATION_REGISTRY.html" class="card-link">View Documentation Registry &rarr;</a>
            </div>
        </div>

    </div>

    <div class="footer">
        Chronodynamic Relativity Development Workspace &bull; Internal Research &bull; RIT Alumni Theoretical Physics Group
    </div>

</body>
</html>
"""

def clean_and_inject_navigation(html_path, docs_root):
    """
    Cleans an HTML file:
      - Removes leftover left sidebar / nav drawer.
      - Adjusts body/main CSS to full-width centered layout.
      - Injects the top navigation return-to-index bar pointing to the root index.html.
    """
    with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Determine depth relative to docs_root
    rel_path = os.path.relpath(html_path, docs_root).replace('\\', '/')
    depth = rel_path.count('/')
    
    # Calculate relative path to index.html in docs_root
    prefix_to_index = "../" * depth if depth > 0 else "./"
    index_url = f"{prefix_to_index}index.html"

    # 1. Remove left-hand sidebar HTML if present
    content = re.sub(r'<nav\b[^>]*>.*?</nav>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<aside\b[^>]*>.*?</aside>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<div[^>]*class=[\'"][^\'"]*sidebar[^\'"]*[\'"][^>]*>.*?</div>\s*<!--\s*/sidebar\s*-->', '', content, flags=re.DOTALL | re.IGNORECASE)

    # 2. Adjust CSS that fixed layout to left-sidebar
    content = re.sub(r'display:\s*flex\s*;', '/* display: flex; */', content)
    content = re.sub(r'margin-left:\s*290px\s*;', 'margin-left: auto; margin-right: auto;', content)
    content = re.sub(r'margin-left:\s*270px\s*;', 'margin-left: auto; margin-right: auto;', content)
    content = re.sub(r'margin-left:\s*250px\s*;', 'margin-left: auto; margin-right: auto;', content)

    # 3. Check if top return-to-index bar already exists
    top_nav_html = f"""<header class="cr-top-nav-bar">
    <a href="{index_url}" class="cr-nav-return-btn">&larr; Return to Documentation Index</a>
    <span class="cr-nav-brand">Chronodynamic Relativity Research Suite</span>
</header>"""

    # If old navigation header exists, replace it
    if 'cr-top-nav-bar' in content:
        content = re.sub(r'<header class=[\'"]cr-top-nav-bar[\'"].*?</header>', top_nav_html, content, flags=re.DOTALL)
    elif 'top-nav-bar' in content:
        content = re.sub(r'<header class=[\'"]top-nav-bar[\'"].*?</header>', top_nav_html, content, flags=re.DOTALL)
    else:
        # Inject right after <body>
        if '<body' in content:
            content = re.sub(r'(<body[^>]*>)', r'\1\n' + top_nav_html + '\n', content, count=1, flags=re.IGNORECASE)
        else:
            content = top_nav_html + '\n' + content

    # 4. Inject CSS style block if not present
    if 'cr-universal-top-nav-style' not in content:
        if '</head>' in content:
            content = content.replace('</head>', TOP_NAV_CSS + '\n</head>')
        else:
            content = TOP_NAV_CSS + '\n' + content

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)

def remove_legacy_subdirectory_indexes(docs_dir):
    """Removes any index.html in subdirectories so only docs/index.html exists."""
    for root, dirs, files in os.walk(docs_dir):
        if root == docs_dir:
            continue
        if 'index.html' in files:
            p = os.path.join(root, 'index.html')
            os.remove(p)
            print(f"  - Removed legacy subdirectory index: {p}")

def upkeep_all(rerun_atlas=False):
    print("=" * 80)
    print("UPKEEP DOCUMENTATION SUITE & INDEX LINK INTEGRITY")
    print(f"Atlas Mode: {'Force Rebuild (--rerun-atlas)' if rerun_atlas else 'Fast Skip (re-use existing atlas.html)'}")
    print("=" * 80)

    from src.evaluations.site_builder.generate_site import SiteGenerator
    try:
        from scripts.render_markdown_docs import render_all_docs_in_directory
    except ImportError:
        from render_markdown_docs import render_all_docs_in_directory

    is_multi_tree = os.path.exists(os.path.join(REPO_ROOT, "official"))

    if is_multi_tree:
        # 1. UPKEEP OFFICIAL SUITE (CR-Development/official/docs)
        off_docs = os.path.abspath(os.path.join(REPO_ROOT, "official/docs"))
        off_analyses = os.path.abspath(os.path.join(REPO_ROOT, "official/docs/analyses"))
        print(f"\n[1/3] Processing Official Documentation: {off_docs}")
        
        # Remove any old subdirectory index.html files
        remove_legacy_subdirectory_indexes(off_docs)

        render_all_docs_in_directory(off_docs)
        if os.path.exists(off_analyses):
            print(f"  * Regenerating official site builder pages in {off_analyses}...")
            site_gen = SiteGenerator(output_dir=off_analyses)
            site_gen.build_all(rerun_atlas=rerun_atlas)

        # Generate the single official root Master Index
        master_index_path = os.path.join(off_docs, "index.html")
        with open(master_index_path, "w", encoding="utf-8") as f:
            f.write(generate_master_index_html())
        print(f"  + Generated Official Master Index: {master_index_path}")

        # Standardize navigation across all official HTML pages
        for root, _, files in os.walk(off_docs):
            for f in files:
                if not f.endswith(".html"):
                    continue
                p = os.path.join(root, f)
                if p == master_index_path:
                    continue
                clean_and_inject_navigation(p, off_docs)

        # 2. UPKEEP DEVELOPMENT SUITE (CR-Development/development/docs)
        dev_docs = os.path.abspath(os.path.join(REPO_ROOT, "development/docs"))
        print(f"\n[2/3] Processing Development Documentation: {dev_docs}")
        if os.path.exists(dev_docs):
            remove_legacy_subdirectory_indexes(dev_docs)
            render_all_docs_in_directory(dev_docs)
            
            dev_index_path = os.path.join(dev_docs, "index.html")
            with open(dev_index_path, "w", encoding="utf-8") as f:
                f.write(generate_development_index_html())
            print(f"  + Generated Development Research Index: {dev_index_path}")

            for root, _, files in os.walk(dev_docs):
                for f in files:
                    if not f.endswith(".html"):
                        continue
                    p = os.path.join(root, f)
                    if p == dev_index_path:
                        continue
                    clean_and_inject_navigation(p, dev_docs)

        # 3. UPKEEP PUBLIC REPOSITORY (Chronodynamic-Relativity/docs)
        pub_docs = os.path.abspath(os.path.join(REPO_ROOT, "../Chronodynamic-Relativity/docs"))
        pub_analyses = os.path.abspath(os.path.join(REPO_ROOT, "../Chronodynamic-Relativity/docs/analyses"))
        if os.path.exists(pub_docs):
            print(f"\n[3/3] Processing Public Release Documentation: {pub_docs}")
            remove_legacy_subdirectory_indexes(pub_docs)
            render_all_docs_in_directory(pub_docs)
            if os.path.exists(pub_analyses):
                site_gen_pub = SiteGenerator(output_dir=pub_analyses)
                site_gen_pub.build_all(rerun_atlas=rerun_atlas)

            pub_master_path = os.path.join(pub_docs, "index.html")
            with open(pub_master_path, "w", encoding="utf-8") as f:
                f.write(generate_master_index_html())
            print(f"  + Generated Public Master Index: {pub_master_path}")

            for root, _, files in os.walk(pub_docs):
                for f in files:
                    if not f.endswith(".html"):
                        continue
                    p = os.path.join(root, f)
                    if p == pub_master_path:
                        continue
                    clean_and_inject_navigation(p, pub_docs)

        print("\nDocumentation upkeep complete across all official, development, and public targets.")
    else:
        # Standalone repository mode (e.g., Chronodynamic-Relativity)
        repo_docs = os.path.abspath(os.path.join(REPO_ROOT, "docs"))
        repo_analyses = os.path.abspath(os.path.join(REPO_ROOT, "docs/analyses"))
        print(f"\nProcessing Repository Documentation: {repo_docs}")
        remove_legacy_subdirectory_indexes(repo_docs)
        render_all_docs_in_directory(repo_docs)
        if os.path.exists(repo_analyses):
            print(f"  * Regenerating site builder pages in {repo_analyses}...")
            site_gen = SiteGenerator(output_dir=repo_analyses)
            site_gen.build_all(rerun_atlas=rerun_atlas)

        master_index_path = os.path.join(repo_docs, "index.html")
        with open(master_index_path, "w", encoding="utf-8") as f:
            f.write(generate_master_index_html())
        print(f"  + Generated Master Index: {master_index_path}")

        for root, _, files in os.walk(repo_docs):
            for f in files:
                if not f.endswith(".html"):
                    continue
                p = os.path.join(root, f)
                if p == master_index_path:
                    continue
                clean_and_inject_navigation(p, repo_docs)

        print("\nDocumentation upkeep complete.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Chronodynamic Relativity Documentation Upkeep Suite")
    parser.add_argument("--rerun-atlas", action="store_true", help="Force rebuild of 175-galaxy SPARC Atlas (slow)")
    args = parser.parse_args()
    upkeep_all(rerun_atlas=args.rerun_atlas)
