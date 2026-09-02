#!/usr/bin/env python3
import json
from pathlib import Path

try:
    from .analyze import EXPECTED_PAIR_LABELS, parse
except ImportError:
    from analyze import EXPECTED_PAIR_LABELS, parse

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_MODELS = {"gemini-3.1-pro-preview", "gemini-3.1-flash-lite"}


def expected_keys(prompts: dict) -> set[tuple[str, str, str, int]]:
    pair_labels = {pair["label"] for pair in prompts["pairs"]}
    assert pair_labels == EXPECTED_PAIR_LABELS
    assert len(prompts["pairs"]) == len(EXPECTED_PAIR_LABELS)
    return {
        (model, pair, condition, run_number)
        for model in EXPECTED_MODELS
        for pair in EXPECTED_PAIR_LABELS
        for condition in ("A", "B")
        for run_number in range(1, 6)
    }


def main() -> None:
    prompts = json.loads((ROOT / "data/prompts.json").read_text())
    expected_prompts = {(pair["label"], condition): pair[field]
                        for pair in prompts["pairs"]
                        for condition, field in (("A", "prompt_a"), ("B", "prompt_b"))}
    rows = [json.loads(line) for line in (ROOT / "raw/responses.jsonl").read_text().splitlines()]
    assert len(rows) == 80
    keys = {(r["requested_model"], r["pair_label"], r["condition"], r["run_number"]) for r in rows}
    assert keys == expected_keys(prompts)
    assert len({r["response_id"] for r in rows}) == 80
    assert all(r["status"] == "ok" for r in rows)
    assert all(r["prompt"] == expected_prompts[(r["pair_label"], r["condition"])] for r in rows)
    valid, invalid = 0, 0
    for row in rows:
        _, error = parse(row["output_text"])
        valid += error is None
        invalid += error is not None
    assert (valid, invalid) == (77, 3)
    analysis = json.loads((ROOT / "results/analysis.json").read_text())
    assert {m["model"] for m in analysis["models"]} == EXPECTED_MODELS
    print("validated 80 unique successful calls, exact prompts, 80 unique response IDs, and 77/3 schema accounting")


if __name__ == "__main__":
    main()
