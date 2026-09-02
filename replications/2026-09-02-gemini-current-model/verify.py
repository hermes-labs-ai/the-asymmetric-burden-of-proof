#!/usr/bin/env python3
"""Verify the public Gemini replication package without API access."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from analyze import analyze_model, parse  # noqa: E402
from validate_run import expected_keys  # noqa: E402

EXPECTED_RAW_SHA256 = "11e3dc5254399780d648502828ae5ec4993abf538960cf47f210cb2ee244dfae"
EXPECTED_PROMPT_SHA256 = "5511092039acdeccca1a44fbea70fd089e4740ee5ed5eb42110472ab4b5421f8"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_checksums() -> None:
    expected_files = set()
    for line in (ROOT / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split("  ", 1)
        expected_files.add(relative)
        path = ROOT / relative
        require(path.is_file() and not path.is_symlink(), f"missing or linked file: {relative}")
        require(digest(path) == expected, f"checksum mismatch: {relative}")
    actual_files = set()
    for directory, subdirectories, filenames in os.walk(ROOT):
        subdirectories[:] = [name for name in subdirectories if name not in {".git", "__pycache__"}]
        for filename in filenames:
            if filename != "SHA256SUMS":
                actual_files.add((Path(directory) / filename).relative_to(ROOT).as_posix())
    require(actual_files == expected_files, "unmanifested or missing replication file")


def main() -> None:
    prompts_path = ROOT / "data/prompts.json"
    raw_path = ROOT / "raw/responses.jsonl"
    require(digest(prompts_path) == EXPECTED_PROMPT_SHA256, "prompt corpus hash mismatch")
    require(digest(raw_path) == EXPECTED_RAW_SHA256, "raw response hash mismatch")

    prompts = json.loads(prompts_path.read_text(encoding="utf-8"))
    expected_prompts = {
        (pair["label"], condition): pair[field]
        for pair in prompts["pairs"]
        for condition, field in (("A", "prompt_a"), ("B", "prompt_b"))
    }
    rows = [json.loads(line) for line in raw_path.read_text(encoding="utf-8").splitlines()]
    require(len(rows) == 80, "expected 80 raw rows")
    keys = {(row["requested_model"], row["pair_label"], row["condition"], row["run_number"]) for row in rows}
    require(keys == expected_keys(prompts), "raw key matrix differs from the preregistered Cartesian product")
    require(len({row["response_id"] for row in rows}) == 80, "duplicate provider response ID")
    require(all(row["status"] == "ok" for row in rows), "non-successful API row")
    require(all(row["prompt"] == expected_prompts[(row["pair_label"], row["condition"])] for row in rows), "submitted prompt mismatch")

    valid = sum(parse(row["output_text"])[1] is None for row in rows)
    require(valid == 77, "schema-valid response count mismatch")
    grouped = {}
    for row in rows:
        grouped.setdefault(row["requested_model"], []).append(row)
    recomputed = {
        "analysis": "preregistered pair-cluster bootstrap",
        "models": [analyze_model(model, grouped[model]) for model in sorted(grouped)],
    }
    recomputed["total_estimated_cost_usd"] = round(sum(model["estimated_cost_usd"] for model in recomputed["models"]), 6)
    recomputed = json.loads(json.dumps(recomputed))
    recorded = json.loads((ROOT / "results/analysis.json").read_text(encoding="utf-8"))
    require(recomputed == recorded, "recomputed analysis differs from recorded analysis")
    verify_checksums()
    print("PASS: 80 unique raw calls, exact prompts, 77/3 schema accounting, deterministic analysis, and checksums")
    print("BOUNDARY: this is one bounded four-pair run, not evidence of model-family generality or causal model progress")


if __name__ == "__main__":
    main()
