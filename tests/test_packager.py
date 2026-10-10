"""
Unit test for Zenodo packager in Chronodynamic Relativity official repository.
Verifies discovery, package generation, metadata schema validity, and checksums.
"""

import os
import json
import pytest
from pathlib import Path
try:
    from official.scripts.package_zenodo_deposits import (
        ZENODO_REGISTRY,
        ZenodoPackager,
        find_repo_roots
    )
except ImportError:
    from scripts.package_zenodo_deposits import (
        ZENODO_REGISTRY,
        ZenodoPackager,
        find_repo_roots
    )


def test_zenodo_registry_schema():
    """Validates that every registered deposit has all required metadata fields."""
    required_keys = {"title", "upload_type", "version", "license", "description", "keywords", "doi"}
    for key, item in ZENODO_REGISTRY.items():
        assert required_keys.issubset(item.keys()), f"Missing keys in ZENODO_REGISTRY[{key}]"
        assert len(item["keywords"]) > 0, f"Empty keywords in ZENODO_REGISTRY[{key}]"
        assert item["doi"].startswith("10.5281/zenodo."), f"Invalid DOI format in ZENODO_REGISTRY[{key}]"


def test_packager_discovery(tmp_path):
    """Tests that packager can initialize and build a targeted deposit in temporary directory."""
    workspace_root, official_root = find_repo_roots()
    packager = ZenodoPackager(
        workspace_root=workspace_root,
        official_root=official_root,
        output_dir=tmp_path,
        compile_pdfs=False,
        verify_math=False
    )
    packager.prepare_output_directory(clean=True)
    
    # Test packaging single manuscript
    res = packager.package_manuscript("series_1_paper_1_foundations", ZENODO_REGISTRY["series_1_paper_1_foundations"])
    assert res is not None, "Packaging series_1_paper_1_foundations returned None"
    
    pkg_dir = tmp_path / "series_1_paper_1_foundations"
    assert pkg_dir.exists()
    assert (pkg_dir / "shreve_chronodynamic_relativity_foundations.pdf").exists()
    assert (pkg_dir / "zenodo_deposit_metadata.json").exists()
    assert (pkg_dir / ".zenodo.json").exists()

    # Verify metadata JSON schema
    with open(pkg_dir / "zenodo_deposit_metadata.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "metadata" in data
    assert data["metadata"]["title"] == ZENODO_REGISTRY["series_1_paper_1_foundations"]["title"]
    assert data["metadata"]["doi"] == "10.5281/zenodo.22697885"
    assert data["metadata"]["upload_type"] == "publication"
    assert data["metadata"]["publication_type"] == "preprint"

    # Write release manifest
    packager.write_release_manifest()
    assert (tmp_path / "MANIFEST.json").exists()
    assert (tmp_path / "CHECKSUMS.sha256").exists()
    assert (tmp_path / "README.md").exists()
