#!/usr/bin/env python3
"""
Package Journal Submissions for Chronodynamic Relativity
==========================================================
Generates self-contained, publication-ready submission packages for:
1. Physical Review D (APS Editorial Manager)
   - Pillar 1: series_1_paper_1_foundations
   - Pillar 1: series_1_paper_2_temporal_dissipation
   - Pillar 1: series_2_paper_3_hubble_tension_expansion
   - Pillar 1: series_2_paper_4_cmb_boltzmann_hierarchy
2. Astronomy & Astrophysics (EDP Sciences Editorial Manager)
   - Pillar 2: series_2_paper_1_jwst_early_galaxies (Letter to the Editor)
   - Pillar 2: series_2_paper_2_cluster_collision_hydrodynamics (Regular Article)
   - Pillar 2: series_2_paper_5_wide_binary_kinematics (Regular Article)

Outputs created in:
- dist/prd/<key>/
- dist/aanda/<key>/

Each package contains:
- <journal>_<key>_submission.tar.gz (isolated, self-contained LaTeX source bundle)
- <journal>_<key>_submission.zip (ZIP format for portals preferring zip)
- shreve_<key>.pdf (compiled publication-ready PDF)
- cover_letter.md & cover_letter.txt (tailored submission letter)
- suggested_referees.txt (parsed referee nominations ready for copy-paste)
- submission_metadata.json (machine-readable journal submission metadata)
- CHECKSUMS.sha256
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tarfile
import tempfile
import zipfile
from pathlib import Path


def find_project_root() -> Path:
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "pyproject.toml").exists() and (parent / "official").exists():
            return parent
    return Path(__file__).resolve().parent.parent


ROOT_DIR = find_project_root()
OFFICIAL_DIR = ROOT_DIR / "official"
MANUSCRIPTS_DIR = OFFICIAL_DIR / "manuscripts"
COVER_LETTERS_DIR = ROOT_DIR / "development" / "manuscripts" / "cover_letters"
DIST_DIR = ROOT_DIR / "dist"

JOURNAL_REGISTRY = {
    "prd": {
        "journal_name": "Physical Review D",
        "publisher": "American Physical Society (APS)",
        "submission_portal": "APS Editorial Manager (https://prd.msubmit.net)",
        "output_dir": DIST_DIR / "prd",
        "papers": {
            "series_1_paper_1_foundations": {
                "title": "Chronodynamic Relativity: Unifying Cosmic Expansion, Galactic Dynamics, Gravitational Lensing, and CMB Acoustic Peaks from a Single Environmental Scalar Field",
                "tex_file": "shreve_chronodynamic_relativity_foundations.tex",
                "bbl_file": "shreve_chronodynamic_relativity_foundations.bbl",
                "bib_file": "references.bib",
                "pdf_file": "shreve_chronodynamic_relativity_foundations.pdf",
                "cover_letter": COVER_LETTERS_DIR / "cover_letter_paper_1_1_prd.md",
                "target_section": "Cosmology",
                "article_category": "Regular Article",
                "wave": "Wave 1",
            },
            "series_1_paper_2_temporal_dissipation": {
                "title": "The Thermodynamic Arrow of Time and Quantum Relational Clocks in Chronodynamic Relativity: Unifying Cosmic Expansion, Total Field Energy Dissipation, and the Dynamic Acceleration Horizon",
                "tex_file": "shreve_temporal_dissipation.tex",
                "bbl_file": "shreve_temporal_dissipation.bbl",
                "bib_file": "paper_2_references.bib",
                "pdf_file": "shreve_temporal_dissipation.pdf",
                "cover_letter": COVER_LETTERS_DIR / "cover_letter_paper_1_2_prd.md",
                "target_section": "Gravitation",
                "article_category": "Regular Article",
                "wave": "Wave 3",
            },
            "series_2_paper_3_hubble_tension_expansion": {
                "title": "Eliminating Dark Energy and Resolving the Hubble Tension via Linear Relativistic Cosmic Expansion",
                "tex_file": "shreve_hubble_tension_expansion.tex",
                "bbl_file": "shreve_hubble_tension_expansion.bbl",
                "bib_file": "paper_hubble_references.bib",
                "pdf_file": "shreve_hubble_tension_expansion.pdf",
                "cover_letter": COVER_LETTERS_DIR / "cover_letter_paper_2_3_prd.md",
                "target_section": "Cosmology",
                "article_category": "Regular Article",
                "wave": "Wave 1",
            },
            "series_2_paper_4_cmb_boltzmann_hierarchy": {
                "title": "Primordial Acoustic Perturbations and Full-Multipole Boltzmann Hierarchy in Chronodynamic Relativity",
                "tex_file": "shreve_cmb_boltzmann_hierarchy.tex",
                "bbl_file": "shreve_cmb_boltzmann_hierarchy.bbl",
                "bib_file": "paper_cmb_references.bib",
                "pdf_file": "shreve_cmb_boltzmann_hierarchy.pdf",
                "cover_letter": COVER_LETTERS_DIR / "cover_letter_paper_2_4_prd.md",
                "target_section": "Cosmology",
                "article_category": "Regular Article",
                "wave": "Wave 3",
            },
        },
    },
    "aanda": {
        "journal_name": "Astronomy & Astrophysics",
        "publisher": "EDP Sciences / European Southern Observatory",
        "submission_portal": "A&A Editorial Manager (https://www.editorialmanager.com/aa/)",
        "output_dir": DIST_DIR / "aanda",
        "flat_package": True,
        "papers": {
            "series_2_paper_1_jwst_early_galaxies": {
                "title": "Resolving the high-redshift JWST early galaxy and supermassive black hole crisis via chronodynamic proper time dilation",
                "tex_file": "shreve_jwst_early_galaxies.tex",
                "bbl_file": "shreve_jwst_early_galaxies.bbl",
                "bib_file": "paper_jwst_references.bib",
                "pdf_file": "shreve_jwst_early_galaxies.pdf",
                "cover_letter": COVER_LETTERS_DIR / "cover_letter_paper_2_1_aanda.md",
                "target_section": "Extragalactic Astronomy",
                "article_category": "Letter to the Editor",
                "aux_files": ["aa.cls", "aa.bst", "lineno.sty", "linenoaa.sty"],
                "wave": "Wave 1",
            },
            "series_2_paper_2_cluster_collision_hydrodynamics": {
                "title": "Three-dimensional relativistic shock hydrodynamics and multi-cluster decoupling without non-baryonic dark matter",
                "tex_file": "shreve_cluster_collision_hydrodynamics.tex",
                "bbl_file": "shreve_cluster_collision_hydrodynamics.bbl",
                "bib_file": "paper_cluster_references.bib",
                "pdf_file": "shreve_cluster_collision_hydrodynamics.pdf",
                "cover_letter": COVER_LETTERS_DIR / "cover_letter_paper_2_2_aanda.md",
                "target_section": "Extragalactic Astronomy",
                "article_category": "Regular Article",
                "aux_files": ["aa.cls", "aa.bst", "lineno.sty", "linenoaa.sty"],
                "wave": "Wave 2",
            },
            "series_2_paper_5_wide_binary_kinematics": {
                "title": "Gaia DR3 wide binary star kinematics and the low-acceleration velocity plateau in Chronodynamic Relativity",
                "tex_file": "shreve_wide_binary_kinematics.tex",
                "bbl_file": "shreve_wide_binary_kinematics.bbl",
                "bib_file": "references.bib",
                "pdf_file": "shreve_wide_binary_kinematics.pdf",
                "cover_letter": COVER_LETTERS_DIR / "cover_letter_paper_2_5_aanda.md",
                "target_section": "Galactic Astronomy",
                "article_category": "Regular Article",
                "aux_files": ["aa.cls", "aa.bst", "lineno.sty", "linenoaa.sty"],
                "wave": "Wave 2",
            },
        },
    },
}


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def parse_referees_from_markdown(cover_letter_path: Path) -> list[dict[str, str]]:
    if not cover_letter_path.exists():
        return []
    content = cover_letter_path.read_text(encoding="utf-8")
    referees = []
    # Pattern: 1. **Name** (Affiliation) — `email` \n *Expertise:* ...
    pattern = re.compile(
        r"\d+\.\s+\*\*(Prof\.|Dr\.|)(?P<name>[^*]+)\*\*\s+\((?P<affiliation>[^)]+)\)\s+[—\-]\s+`(?P<email>[^`]+)`(?:\s*\n\s*\*Expertise:\*\s*(?P<expertise>[^\n]+))?",
        re.MULTILINE,
    )
    for m in pattern.finditer(content):
        name = m.group("name").strip()
        affil = m.group("affiliation").strip()
        email = m.group("email").strip()
        exp = (m.group("expertise") or "").strip()
        referees.append({
            "name": name,
            "affiliation": affil,
            "email": email,
            "expertise": exp,
        })
    return referees


def format_referees_plain_text(referees: list[dict[str, str]]) -> str:
    lines = ["SUGGESTED INDEPENDENT REFEREES", "==============================", ""]
    for i, r in enumerate(referees, start=1):
        lines.append(f"{i}. Name: {r['name']}")
        lines.append(f"   Affiliation: {r['affiliation']}")
        lines.append(f"   Email: {r['email']}")
        if r.get("expertise"):
            lines.append(f"   Expertise: {r['expertise']}")
        lines.append("")
    return "\n".join(lines)


def run_sandbox_compilation(tar_path: Path, main_tex: str) -> bool:
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        with tarfile.open(tar_path, "r:gz") as tar:
            if hasattr(tarfile, "data_filter"):
                tar.extractall(path=tmp_path, filter="data")
            else:
                tar.extractall(path=tmp_path)

        cmd = ["pdflatex", "-interaction=nonstopmode", main_tex]
        res1 = subprocess.run(cmd, cwd=tmp_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res1.returncode != 0:
            print(f"      [!] Sandbox pass 1 failed: {res1.stdout[-800:]}")
            return False

        res2 = subprocess.run(cmd, cwd=tmp_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res2.returncode != 0:
            print(f"      [!] Sandbox pass 2 failed: {res2.stdout[-800:]}")
            return False

        out_pdf = tmp_path / (Path(main_tex).stem + ".pdf")
        if not out_pdf.exists() or out_pdf.stat().st_size == 0:
            print(f"      [!] Sandbox generated empty/missing PDF.")
            return False

        return True


def package_journal_submissions():
    print("=" * 80)
    print("  Chronodynamic Relativity — Journal Submission Packaging Pipeline")
    print("=" * 80)

    summary_records = []

    for journal_key, j_info in JOURNAL_REGISTRY.items():
        j_name = j_info["journal_name"]
        j_out_dir = j_info["output_dir"]
        j_out_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n[+] Packaging for: {j_name} ({j_info['publisher']})")
        print(f"    Output Directory: {j_out_dir}")

        for paper_key, p_meta in j_info["papers"].items():
            print(f"\n  --- Paper: {paper_key} ---")
            src_dir = MANUSCRIPTS_DIR / paper_key
            pkg_dir = j_out_dir / paper_key
            pkg_dir.mkdir(parents=True, exist_ok=True)

            main_tex = p_meta["tex_file"]
            main_bbl = p_meta["bbl_file"]
            main_bib = p_meta["bib_file"]
            main_pdf = p_meta["pdf_file"]

            # 1. Collect required source files
            files_to_bundle = []

            # Main TeX
            tex_path = src_dir / main_tex
            if not tex_path.exists():
                raise FileNotFoundError(f"Missing TeX file: {tex_path}")
            files_to_bundle.append((tex_path, main_tex))

            # BBL file
            bbl_path = src_dir / main_bbl
            if bbl_path.exists():
                files_to_bundle.append((bbl_path, main_bbl))

            # Bib file
            bib_path = src_dir / main_bib
            if bib_path.exists():
                files_to_bundle.append((bib_path, main_bib))

            # Auxiliary files (e.g., aa.cls, aa.bst)
            for aux_name in p_meta.get("aux_files", []):
                aux_path = src_dir / aux_name
                if aux_path.exists():
                    files_to_bundle.append((aux_path, aux_name))

            # Figures: bundle 100% flat at root for strict Editorial Manager compatibility
            figures_dir = src_dir / "figures"
            pkg_fig_dir = pkg_dir / "figures"
            if pkg_fig_dir.exists():
                shutil.rmtree(pkg_fig_dir)
            if figures_dir.exists():
                for fig in sorted(figures_dir.glob("*.pdf")):
                    files_to_bundle.append((fig, fig.name))
                    shutil.copy2(fig, pkg_dir / fig.name)
                for fig in sorted(figures_dir.glob("*.png")):
                    files_to_bundle.append((fig, fig.name))
                    shutil.copy2(fig, pkg_dir / fig.name)

            # Copy all root files into pkg_dir for direct file upload
            for src_file, arcname in files_to_bundle:
                dest_file = pkg_dir / arcname
                if not dest_file.exists() or src_file.stat().st_mtime > dest_file.stat().st_mtime:
                    shutil.copy2(src_file, dest_file)
            print(f"    -> Flattened all {len(files_to_bundle)} source and figure files directly into {pkg_dir.name}/")

            # 2. Build tar.gz source package
            tar_filename = f"{journal_key}_{paper_key}_submission.tar.gz"
            tar_path = pkg_dir / tar_filename
            with tarfile.open(tar_path, "w:gz") as tar:
                for src_file, arcname in files_to_bundle:
                    tar.add(src_file, arcname=arcname)
            print(f"    -> Built Source Tarball: {tar_filename} ({tar_path.stat().st_size:,} bytes)")

            # 3. Build zip package
            zip_filename = f"{journal_key}_{paper_key}_submission.zip"
            zip_path = pkg_dir / zip_filename
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for src_file, arcname in files_to_bundle:
                    zf.write(src_file, arcname=arcname)
            print(f"    -> Built Source ZIP: {zip_filename} ({zip_path.stat().st_size:,} bytes)")

            # 4. Copy precompiled publication PDF
            pdf_path = src_dir / main_pdf
            if pdf_path.exists():
                dest_pdf = pkg_dir / main_pdf
                shutil.copy2(pdf_path, dest_pdf)
                print(f"    -> Copied Publication PDF: {main_pdf} ({dest_pdf.stat().st_size:,} bytes)")
            else:
                dest_pdf = None

            # 5. Process Cover Letter & Suggested Referees
            cover_src = p_meta["cover_letter"]
            referees = []
            if cover_src.exists():
                # Markdown cover letter
                shutil.copy2(cover_src, pkg_dir / "cover_letter.md")
                # Plain text cover letter
                cl_text = cover_src.read_text(encoding="utf-8")
                (pkg_dir / "cover_letter.txt").write_text(cl_text, encoding="utf-8")
                # Parse referees
                referees = parse_referees_from_markdown(cover_src)
                (pkg_dir / "suggested_referees.txt").write_text(
                    format_referees_plain_text(referees), encoding="utf-8"
                )
                print(f"    -> Extracted {len(referees)} Suggested Referees from cover letter")

            # 6. Emit Submission Metadata JSON
            sub_meta = {
                "journal": j_name,
                "publisher": j_info["publisher"],
                "submission_portal": j_info["submission_portal"],
                "paper_key": paper_key,
                "title": p_meta["title"],
                "target_section": p_meta["target_section"],
                "article_category": p_meta["article_category"],
                "wave": p_meta["wave"],
                "corresponding_author": {
                    "name": "Joshua A. Shreve",
                    "email": "j.a.shreve@gmail.com",
                    "affiliation": "Chronodynamic Relativity Research Initiative, Acton, MA, USA",
                    "orcid": "0009-0000-5942-5351",
                },
                "packages": {
                    "tar_gz": tar_filename,
                    "tar_gz_sha256": compute_sha256(tar_path),
                    "zip": zip_filename,
                    "zip_sha256": compute_sha256(zip_path),
                    "pdf": main_pdf,
                    "pdf_sha256": compute_sha256(dest_pdf) if dest_pdf else None,
                },
                "bundled_source_files": [arcname for _, arcname in files_to_bundle],
                "suggested_referees": referees,
            }
            meta_path = pkg_dir / "submission_metadata.json"
            meta_path.write_text(json.dumps(sub_meta, indent=2), encoding="utf-8")
            print(f"    -> Emitted: submission_metadata.json")

            # 7. Generate directory checksums
            checksum_lines = []
            for item in sorted(pkg_dir.iterdir()):
                if item.is_file() and item.name != "CHECKSUMS.sha256":
                    checksum_lines.append(f"{compute_sha256(item)}  {item.name}")
            (pkg_dir / "CHECKSUMS.sha256").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")

            # 8. Dry-Run Sandbox Test Compilation
            print(f"    -> Executing sandbox compilation verification...")
            test_ok = run_sandbox_compilation(tar_path, main_tex)
            if test_ok:
                print(f"    -> SUCCESS: Sandbox isolated compilation PASSED!")
            else:
                print(f"    -> ERROR: Sandbox isolated compilation FAILED!")
                raise RuntimeError(f"Sandbox compilation failed for {tar_filename}")

            summary_records.append({
                "journal": j_name,
                "paper_key": paper_key,
                "title": p_meta["title"],
                "category": p_meta["article_category"],
                "section": p_meta["target_section"],
                "tar_gz": f"dist/{journal_key}/{paper_key}/{tar_filename}",
                "pdf": f"dist/{journal_key}/{paper_key}/{main_pdf}",
            })

    # Write summary README for prd and aanda
    for journal_key, j_info in JOURNAL_REGISTRY.items():
        j_out_dir = j_info["output_dir"]
        readme_lines = [
            f"# {j_info['journal_name']} Submission Packages",
            f"**Publisher:** {j_info['publisher']}  ",
            f"**Portal:** {j_info['submission_portal']}  ",
            "",
            "| Paper Key | Category | Section | Submission Archive | Publication PDF |",
            "|---|---|---|---|---|",
        ]
        for p_key, p_meta in j_info["papers"].items():
            tar_name = f"{journal_key}_{p_key}_submission.tar.gz"
            pdf_name = p_meta["pdf_file"]
            readme_lines.append(
                f"| **{p_key}** | {p_meta['article_category']} | {p_meta['target_section']} | [{tar_name}]({p_key}/{tar_name}) | [{pdf_name}]({p_key}/{pdf_name}) |"
            )
        readme_lines.append("\nEach directory contains self-contained LaTeX source archives, cover letter, suggested referees, and metadata JSON.\n")
        (j_out_dir / "README.md").write_text("\n".join(readme_lines), encoding="utf-8")

    # Update top-level dist/README.md
    dist_readme = [
        "# Chronodynamic Relativity — Distribution Release Packages",
        "",
        "This directory contains publication, deposit, and preprint distribution packages for Chronodynamic Relativity.",
        "",
        "## Package Categories",
        "",
        "1. **Zenodo Release Packages ([`dist/zenodo/`](zenodo/)):**",
        "   * Complete preprint release bundles for all 7 monograph papers and software framework v1.1.1.",
        "   * Contains `.zenodo.json` schemas, API payloads, and source archives.",
        "",
        "2. **Physical Review D Submissions ([`dist/prd/`](prd/)):**",
        "   * Self-contained submission packages for American Physical Society (APS) Editorial Manager.",
        "   * Covers: Paper 1.1 (Foundations), Paper 1.2 (Thermodynamics), Paper 2.3 (Expansion/Hubble), Paper 2.4 (CMB Boltzmann).",
        "",
        "3. **Astronomy & Astrophysics Submissions ([`dist/aanda/`](aanda/)):**",
        "   * Self-contained submission packages for EDP Sciences Editorial Manager.",
        "   * Covers: Paper 2.1 (JWST Early Galaxies — Letter to the Editor), Paper 2.2 (Bullet Cluster AMR Hydrodynamics), Paper 2.5 (Gaia Wide Binaries).",
        "",
        "All packages have been verified with isolated sandbox compilation tests and SHA-256 checksums.",
    ]
    (DIST_DIR / "README.md").write_text("\n".join(dist_readme) + "\n", encoding="utf-8")

    print("\n" + "=" * 80)
    print("  Journal Packaging Pipeline Complete: All 7 Papers Packaged & Verified!")
    print("=" * 80)


if __name__ == "__main__":
    package_journal_submissions()
