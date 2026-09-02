#!/usr/bin/env python3
import json
from pathlib import Path

from analyze import parse

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    prompts = json.loads((ROOT / "data/prompts.json").read_text())
    expected_prompts = {(pair["label"], condition): pair[field]
                        for pair in prompts["pairs"]
                        for condition, field in (("A", "prompt_a"), ("B", "prompt_b"))}
    rows = [json.loads(line) for line in (ROOT / "raw/responses.jsonl").read_text().splitlines()]
    assert len(rows) == 80
    keys = {(r["requested_model"], r["pair_label"], r["condition"], r["run_number"]) for r in rows}
    assert len(keys) == 80
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
    assert {m["model"] for m in analysis["models"]} == {"gemini-3.1-pro-preview", "gemini-3.1-flash-lite"}
    print("validated 80 unique successful calls, exact prompts, 80 unique response IDs, and 77/3 schema accounting")


if __name__ == "__main__":
    main()
