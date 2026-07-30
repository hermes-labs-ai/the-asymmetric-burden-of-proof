#!/usr/bin/env python3
"""Verify the minimum archival package for The Asymmetric Burden of Proof."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOI = "10.5281/zenodo.18867694"
TITLE = (
    "The Asymmetric Burden of Proof: LLMs Show a Null-Result Asymmetry "
    "in a Matched-Vignette Benchmark"
)
PDF = ROOT / "asymmetric-burden-of-proof-null-result-asymmetry.pdf"
PDF_SHA256 = "2acef493a55dd0e27f87008fc2de9a20731f0f0eff97294857c84debf5ecc940"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def verify_manifest() -> None:
    expected_files = {"SHA256SUMS"}
    for raw_line in (ROOT / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            continue
        expected, relative = raw_line.split("  ", 1)
        expected_files.add(relative)
        path = ROOT / relative
        require(path.is_file(), f"missing manifest file: {relative}")
        require(not path.is_symlink(), f"manifest path is a symlink: {relative}")
        require(digest(path) == expected, f"checksum mismatch: {relative}")
    actual_files = {
        path.name
        for path in ROOT.iterdir()
        if path.name != ".git"
    }
    require(actual_files == expected_files, "unmanifested or missing package file")


def main() -> None:
    require(PDF.read_bytes().startswith(b"%PDF-"), "paper is not a PDF")
    require(digest(PDF) == PDF_SHA256, "published PDF checksum mismatch")

    metadata = json.loads((ROOT / "metadata.json").read_text(encoding="utf-8"))
    require(metadata["@id"] == f"https://doi.org/{DOI}", "metadata DOI mismatch")
    require(metadata["name"] == TITLE, "metadata title mismatch")
    require(metadata["license"].endswith("/by/4.0/"), "metadata license mismatch")

    citation = " ".join(
        (ROOT / "CITATION.bib").read_text(encoding="utf-8").split()
    )
    require(DOI in citation and TITLE in citation, "citation identity mismatch")

    verify_manifest()
    print("PASS: package identity, checksums, citation, and published PDF hash")
    print("BOUNDARY: this does not rerun or independently replicate the evaluations")


if __name__ == "__main__":
    main()
