#!/usr/bin/env python3
"""
Automated Zenodo Deposit Updater for Chronodynamic Relativity.

Reads ZENODO_ACCESS_TOKEN from .env or environment, creates new version drafts
for specified deposits, uploads updated PDF and source bundle files, and synchronizes
metadata. By default, leaves records as reviewable drafts; pass --publish to publish immediately.
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any, Optional

def load_env_file(env_path: Path):
    """Loads key-value pairs from .env into os.environ if not already set."""
    if not env_path.exists():
        return
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip("'\"")
            if k and k not in os.environ:
                os.environ[k] = v

TARGET_DEPOSITS = {
    "series_2_paper_1_jwst_early_galaxies": {
        "record_id": "23344804",
        "new_version": "v1.0.3",
        "pub_date": "2026-10-14",
        "dist_folder": "series_2_paper_1_jwst_early_galaxies",
        "files": [
            "shreve_jwst_early_galaxies.pdf",
            "submission_series_2_paper_1_jwst_early_galaxies_v1.0.2.tar.gz"
        ],
        "notes": (
            "Version 1.0.3 Revision Notes: Restored full Astronomy & Astrophysics (A&A) title page "
            "(title, author, affiliation, structured abstract, keywords) per editorial formatting notification (aa63573-26); "
            "enabled Letter to the Editor documentclass option; harmonized single-author affiliation and corresponding author markup "
            "per aa.cls v9.4 conventions; updated companion software framework reference to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449)."
        )
    },
    "series_2_paper_2_cluster_collision_hydrodynamics": {
        "record_id": "23345092",
        "new_version": "v1.0.3",
        "pub_date": "2026-10-14",
        "dist_folder": "series_2_paper_2_cluster_collision_hydrodynamics",
        "files": [
            "shreve_cluster_collision_hydrodynamics.pdf",
            "submission_series_2_paper_2_cluster_collision_hydrodynamics_v1.0.2.tar.gz"
        ],
        "notes": (
            "Version 1.0.3 Revision Notes: Restored full Astronomy & Astrophysics (A&A) title page "
            "(title, author, affiliation, structured abstract, keywords) per editorial conventions; "
            "harmonized single-author affiliation and corresponding author markup per aa.cls v9.4 conventions; "
            "updated companion software framework reference to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449)."
        )
    },
    "series_2_paper_5_wide_binary_kinematics": {
        "record_id": "23345184",
        "new_version": "v1.0.3",
        "pub_date": "2026-10-15",
        "dist_folder": "series_2_paper_5_wide_binary_kinematics",
        "files": [
            "shreve_wide_binary_kinematics.pdf",
            "submission_series_2_paper_5_wide_binary_kinematics_v1.0.2.tar.gz"
        ],
        "notes": (
            "Version 1.0.3 Revision Notes: Restored full Astronomy & Astrophysics (A&A) title page "
            "(title, author, affiliation, structured abstract, keywords) per editorial conventions; "
            "harmonized single-author affiliation and corresponding author markup per aa.cls v9.4 conventions; "
            "updated companion software framework reference to v1.1.1 (Concept DOI: 10.5281/zenodo.22697449)."
        )
    },
    "series_2_paper_3_hubble_tension_expansion": {
        "record_id": "23329028",
        "new_version": "v1.0.2",
        "pub_date": "2026-10-15",
        "dist_folder": "series_2_paper_3_hubble_tension_expansion",
        "files": [
            "shreve_hubble_tension_expansion.pdf",
            "submission_series_2_paper_3_hubble_tension_expansion_v1.0.1.tar.gz"
        ],
        "notes": (
            "Version 1.0.2 Revision Notes: Synchronized companion paper citations and validated joint Pantheon+ "
            "and DESI BAO likelihood contours against software framework v1.1.1 (Concept DOI: 10.5281/zenodo.22697449)."
        )
    }
}

class ZenodoUpdater:
    def __init__(self, token: str, workspace_root: Path, publish: bool = False):
        self.token = token
        self.workspace_root = workspace_root
        self.dist_dir = workspace_root / "dist" / "zenodo"
        self.publish = publish
        self.base_url = "https://zenodo.org/api/deposit/depositions"

    def _request(self, url: str, method: str = "GET", data: Optional[bytes] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        h = {
            "Authorization": f"Bearer {self.token}",
            "User-Agent": "CR-Zenodo-Updater/1.0"
        }
        if headers:
            h.update(headers)
        req = urllib.request.Request(url, data=data, headers=h, method=method)
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8")
            return json.loads(content) if content else {}

    def update_deposit(self, key: str, config: Dict[str, Any]):
        rec_id = config["record_id"]
        print(f"\n[+] Processing '{key}' (Current Zenodo ID: {rec_id})...")

        # 1. Trigger newversion action
        print(f"    Creating new version draft on Zenodo...")
        new_ver_url = f"{self.base_url}/{rec_id}/actions/newversion"
        try:
            res = self._request(new_ver_url, method="POST")
        except urllib.error.HTTPError as e:
            print(f"    [Error] Failed to create new version draft: {e}")
            if e.code == 403:
                print("    [Hint] Verify your token has 'deposit:write' and 'deposit:actions' scopes.")
            return False

        latest_draft_url = res.get("links", {}).get("latest_draft")
        if not latest_draft_url:
            print(f"    [Error] No latest_draft link in Zenodo response: {res}")
            return False

        draft_id = latest_draft_url.rstrip("/").split("/")[-1]
        print(f"    Created draft ID: {draft_id}")

        # 2. Get draft details to inspect existing files and bucket link
        draft_info = self._request(f"{self.base_url}/{draft_id}")
        bucket_url = draft_info.get("links", {}).get("bucket")

        existing_files = draft_info.get("files", [])
        for f in existing_files:
            fid = f.get("id")
            fname = f.get("filename")
            print(f"    Deleting old draft file: {fname} ({fid})...")
            self._request(f"{self.base_url}/{draft_id}/files/{fid}", method="DELETE")

        # 3. Upload new files from dist/zenodo/
        target_dir = self.dist_dir / config["dist_folder"]
        for fname in config["files"]:
            fpath = target_dir / fname
            if not fpath.exists():
                print(f"    [Warning] Local file not found: {fpath}")
                continue
            print(f"    Uploading {fname} ({fpath.stat().st_size:,} bytes)...")
            with open(fpath, "rb") as fp:
                file_data = fp.read()

            if bucket_url:
                upload_url = f"{bucket_url}/{fname}"
                self._request(upload_url, method="PUT", data=file_data, headers={"Content-Type": "application/octet-stream"})
            else:
                upload_url = f"{self.base_url}/{draft_id}/files"
                boundary = "----WebKitFormBoundaryZenodoUpload"
                body = (
                    f"--{boundary}\r\n"
                    f'Content-Disposition: form-data; name="file"; filename="{fname}"\r\n'
                    f"Content-Type: application/octet-stream\r\n\r\n"
                ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")
                headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
                self._request(upload_url, method="POST", data=body, headers=headers)
            print(f"    [Uploaded] {fname}")

        # 4. Update metadata
        metadata = draft_info.get("metadata", {})
        metadata["version"] = config["new_version"]
        metadata["publication_date"] = config["pub_date"]
        metadata["notes"] = config["notes"]

        print(f"    Updating metadata (Version: {config['new_version']}, Date: {config['pub_date']})...")
        update_body = json.dumps({"metadata": metadata}).encode("utf-8")
        self._request(f"{self.base_url}/{draft_id}", method="PUT", data=update_body, headers={"Content-Type": "application/json"})
        print(f"    [Updated] Metadata saved for draft {draft_id}")

        # 5. Publish if requested
        if self.publish:
            print(f"    Publishing new version...")
            pub_res = self._request(f"{self.base_url}/{draft_id}/actions/publish", method="POST")
            new_doi = pub_res.get("doi", "")
            print(f"    [PUBLISHED] New Version DOI: {new_doi}")
        else:
            print(f"    [Draft Ready] Draft saved at: https://zenodo.org/deposit/{draft_id}")

        return True

def main():
    parser = argparse.ArgumentParser(description="Update Zenodo deposits with revised files and metadata.")
    parser.add_argument("--publish", action="store_true", help="Publish drafts immediately (default: leave as reviewable drafts)")
    parser.add_argument("--paper", help="Only update specific paper key")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent.parent
    load_env_file(repo_root / ".env")

    token = os.getenv("ZENODO_ACCESS_TOKEN", "").strip()
    if not token:
        print("[!] Error: ZENODO_ACCESS_TOKEN is not set.")
        print("    Add your token to .env (ZENODO_ACCESS_TOKEN=...) or set $env:ZENODO_ACCESS_TOKEN.")
        sys.exit(1)

    updater = ZenodoUpdater(token=token, workspace_root=repo_root, publish=args.publish)

    targets = [args.paper] if args.paper else list(TARGET_DEPOSITS.keys())
    for t in targets:
        if t in TARGET_DEPOSITS:
            updater.update_deposit(t, TARGET_DEPOSITS[t])
        else:
            print(f"[!] Unknown target: {t}")

if __name__ == "__main__":
    main()
