#!/usr/bin/env python3
import json
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALID_LABELS = {"Confirmed", "Likely", "Unsupported", "Refuted"}
PRICES = {
    "gemini-3.1-pro-preview": (2.0, 12.0),
    "gemini-3.1-flash-lite": (0.25, 1.50),
}


def parse(text: str) -> tuple[dict | None, str | None]:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        stripped = "\n".join(lines[1:-1])
    try:
        obj = json.loads(stripped)
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON: {exc}"
    if obj.get("classification") not in VALID_LABELS:
        return None, "invalid classification"
    probs = obj.get("probability_distribution", {})
    keys = ("effect_greater_than_zero", "effect_approximately_zero", "effect_less_than_zero")
    vals = [probs.get(key) for key in keys]
    if any(type(value) is not int or not 0 <= value <= 100 for value in vals):
        return None, "probabilities must be integers in [0,100]"
    if sum(vals) != 100:
        return None, "probabilities do not sum to 100"
    if not isinstance(obj.get("top_3_reasons"), list) or len(obj["top_3_reasons"]) != 3:
        return None, "top_3_reasons must have length 3"
    return obj, None


def percentile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    pos = (len(ordered) - 1) * p
    lo = int(pos)
    hi = min(lo + 1, len(ordered) - 1)
    weight = pos - lo
    return ordered[lo] * (1 - weight) + ordered[hi] * weight


def analyze_model(model: str, rows: list[dict]) -> dict:
    parsed = {}
    failures = []
    labels = Counter()
    usage = Counter()
    returned_models = Counter()
    for row in rows:
        for key, value in row.get("usage", {}).items():
            if isinstance(value, int):
                usage[key] += value
        returned_models[row.get("returned_model")] += 1
        obj, error = parse(row.get("output_text", "")) if row.get("status") == "ok" else (None, row.get("error", "API error"))
        unit = (row["pair_label"], row["condition"], row["run_number"])
        if error:
            failures.append({"unit": unit, "error": error})
        else:
            parsed[unit] = obj
            labels[(row["condition"], obj["classification"])] += 1
    by_pair = defaultdict(list)
    for pair in sorted({row["pair_label"] for row in rows}):
        for run in range(1, 6):
            a = parsed.get((pair, "A", run))
            b = parsed.get((pair, "B", run))
            if a and b:
                gap = a["probability_distribution"]["effect_greater_than_zero"] - b["probability_distribution"]["effect_approximately_zero"]
                by_pair[pair].append(gap)
    all_gaps = [gap for gaps in by_pair.values() for gap in gaps]
    pair_names = sorted(by_pair)
    rng = random.Random(20260902)
    boot = []
    for _ in range(10_000):
        sampled = [rng.choice(pair_names) for _ in pair_names]
        boot.append(statistics.mean(gap for pair in sampled for gap in by_pair[pair]))
    estimate = statistics.mean(all_gaps)
    ci = [percentile(boot, .025), percentile(boot, .975)]
    verdict = "persists" if ci[0] > 0 else "reverses" if ci[1] < 0 else "inconclusive"
    in_price, out_price = PRICES[model]
    input_tokens = usage.get("promptTokenCount", 0)
    output_tokens = usage.get("candidatesTokenCount", 0) + usage.get("thoughtsTokenCount", 0)
    cost = input_tokens / 1_000_000 * in_price + output_tokens / 1_000_000 * out_price
    return {
        "model": model,
        "returned_models": dict(returned_models),
        "responses": len(rows),
        "valid_responses": len(parsed),
        "schema_failures": failures,
        "complete_paired_units": len(all_gaps),
        "mean_paired_gap_pp": round(estimate, 3),
        "pair_cluster_bootstrap_95_ci_pp": [round(value, 3) for value in ci],
        "verdict": verdict,
        "positive_gap_units": sum(gap > 0 for gap in all_gaps),
        "zero_gap_units": sum(gap == 0 for gap in all_gaps),
        "negative_gap_units": sum(gap < 0 for gap in all_gaps),
        "per_pair_mean_gap_pp": {pair: round(statistics.mean(gaps), 3) for pair, gaps in by_pair.items()},
        "classification_counts": {f"{condition}:{label}": count for (condition, label), count in sorted(labels.items())},
        "usage": dict(usage),
        "estimated_cost_usd": round(cost, 6),
    }


def main() -> None:
    path = ROOT / "raw/responses.jsonl"
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["requested_model"]].append(row)
    result = {
        "analysis": "preregistered pair-cluster bootstrap",
        "models": [analyze_model(model, grouped[model]) for model in sorted(grouped)],
    }
    result["total_estimated_cost_usd"] = round(sum(item["estimated_cost_usd"] for item in result["models"]), 6)
    out = ROOT / "results/analysis.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
