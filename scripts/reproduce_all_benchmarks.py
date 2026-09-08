r"""
Master End-to-End Benchmark & Publication Reproducibility Pipeline
==================================================================
Rebuilds the CLASS-CR C engine, executes all 4 empirical pillars, verifies
mathematical continuity, and updates all publication-grade comparison figures.
"""

import os
import sys
import time
import subprocess

def run_step(title, command, cwd=None):
    print("\n" + "=" * 85)
    print(f"STEP: {title}")
    print("=" * 85)
    t0 = time.time()
    res = subprocess.run(command, shell=True, cwd=cwd)
    dt = time.time() - t0
    if res.returncode != 0:
        print(f"[ERROR] Step failed with return code {res.returncode}")
        sys.exit(res.returncode)
    print(f"[SUCCESS] Completed in {dt:.2f} seconds.")

def main():
    print("=" * 90)
    print("CHRONODYNAMIC RELATIVITY: MASTER REPRODUCIBILITY & BENCHMARK PIPELINE")
    print("=" * 90)
    
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    python_exe = sys.executable
    
    # 1. Run DESI Native BAO Reconstruction Pipeline
    run_step(
        "Execute Native DESI BAO Reconstruction Pipeline",
        f'"{python_exe}" src/evaluations/desi_reconstruction.py',
        cwd=repo_root
    )
    
    # 2. Run Unified 4-Pillar Joint Likelihood
    run_step(
        "Evaluate Unified 4-Pillar Empirical Benchmark Suite",
        f'"{python_exe}" src/evaluations/run_unified_joint_likelihood.py',
        cwd=repo_root
    )
    
    # 3. Generate Multi-Tier 4-Pillar Overview Dashboard
    run_step(
        "Generate Multi-Tier 4-Pillar Publication Figures & Dashboard",
        f'"{python_exe}" src/evaluations/plot_unified_4pillars.py',
        cwd=repo_root
    )
    
    # 4. Generate Publication Manuscript Vector Figures
    run_step(
        "Generate Publication Manuscript Vector Figures",
        f'"{python_exe}" src/evaluations/generate_manuscript_figures.py',
        cwd=repo_root
    )
    
    # 5. Upkeep Master Documentation & HTML Pages
    run_step(
        "Upkeep Interactive HTML Documentation & Site Pages",
        f'"{python_exe}" scripts/upkeep_html_docs.py',
        cwd=repo_root
    )
    
    print("\n" + "=" * 90)
    print("ALL REPRODUCIBILITY BENCHMARKS COMPLETED SUCCESSFULLY!")
    print("=" * 90)
    print("Key Deliverables:")
    print("  * Master Documentation:  docs/index.html")
    print("  * 4-Pillar Overview:     docs/analyses/unified_4pillar_benchmark_overview.html")
    print("  * 4-Pillar Overview Img: docs/analyses/unified_4pillar_benchmark_overview.png")
    print("  * Manuscript Figures:    manuscripts/paper_1_foundations/figures/")
    print("  * 4-Pillar JSON Results: results/benchmarks/unified_4pillar_benchmark_results.json")
    print("=" * 90)

if __name__ == '__main__':
    main()
