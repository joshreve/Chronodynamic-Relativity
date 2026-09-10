"""
Tests for Data & Analysis Manifest Integrity
===========================================
Verifies that all entries in manifest.json point to valid existing files on disk,
and asserts that data/ contains no misplaced result outputs.
"""

import os
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

class TestManifestIntegrity(unittest.TestCase):

    def test_manifest_file_exists(self):
        manifest_path = REPO_ROOT / "manifest.json"
        self.assertTrue(manifest_path.exists(), "manifest.json does not exist in repository root.")

    def test_manifest_structure_and_files_exist(self):
        manifest_path = REPO_ROOT / "manifest.json"
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        
        self.assertIn("analyses", manifest, "Manifest missing 'analyses' section.")
        
        missing_files = []
        for key, analysis in manifest["analyses"].items():
            self.assertIn("pillar", analysis, f"Analysis '{key}' missing 'pillar'.")
            self.assertIn("scope", analysis, f"Analysis '{key}' missing 'scope'.")
            
            for category in ["inputs", "scripts", "results", "figures", "documentation"]:
                items = analysis.get(category, [])
                for item in items:
                    target_path = REPO_ROOT / item
                    if not target_path.exists():
                        missing_files.append(f"[{key} -> {category}] {item}")
                        
        self.assertFalse(missing_files, f"Files listed in manifest.json do not exist on disk:\n" + "\n".join(missing_files))

    def test_data_directory_contains_no_results(self):
        """Asserts that data/ does not contain misplaced results or benchmark json files."""
        data_dir = REPO_ROOT / "data"
        misplaced = [
            p.relative_to(REPO_ROOT)
            for p in data_dir.rglob("*.json")
            if "results" in p.name or "study" in p.name or "baseline" in p.name or "params" in p.name
        ]
        self.assertFalse(misplaced, f"Misplaced result files detected in data/ directory:\n" + "\n".join(str(p) for p in misplaced))

    def test_results_directory_structure(self):
        """Verifies standard results subdirectories exist."""
        results_dir = REPO_ROOT / "results"
        self.assertTrue(results_dir.exists(), "results/ directory missing.")
        for subdir in ["benchmarks", "cosmology", "global"]:
            self.assertTrue((results_dir / subdir).exists(), f"results/{subdir} directory missing.")

    def test_zenodo_metadata_integrity(self):
        """Verifies .zenodo.json exists, is valid JSON, and adheres to Zenodo upload schema."""
        zenodo_path = REPO_ROOT / ".zenodo.json"
        self.assertTrue(zenodo_path.exists(), ".zenodo.json does not exist in repository root.")
        with open(zenodo_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        required_fields = ["title", "description", "creators", "access_right", "license", "upload_type"]
        for field in required_fields:
            self.assertIn(field, data, f".zenodo.json missing required field '{field}'.")

        self.assertIsInstance(data["creators"], list, "creators must be a list in .zenodo.json.")
        self.assertGreater(len(data["creators"]), 0, "creators list cannot be empty.")
        for creator in data["creators"]:
            self.assertIn("name", creator, "Creator missing 'name'.")
            self.assertIn("orcid", creator, "Creator missing 'orcid'.")
            self.assertEqual(creator["orcid"], "0009-0000-5942-5351", "Unexpected ORCID in .zenodo.json.")

    def test_citation_cff_integrity(self):
        """Verifies CITATION.cff exists and contains required citation metadata."""
        cff_path = REPO_ROOT / "CITATION.cff"
        self.assertTrue(cff_path.exists(), "CITATION.cff does not exist in repository root.")
        with open(cff_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("cff-version:", content, "CITATION.cff missing 'cff-version'.")
        self.assertIn("title:", content, "CITATION.cff missing 'title'.")
        self.assertIn("0009-0000-5942-5351", content, "CITATION.cff missing canonical ORCID.")
        self.assertIn("https://github.com/joshreve/Chronodynamic-Relativity", content, "CITATION.cff missing repository-code.")

if __name__ == '__main__':
    unittest.main()

