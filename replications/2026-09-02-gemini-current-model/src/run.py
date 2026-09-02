#!/usr/bin/env python3
import argparse
import json
import os
import random
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS = ("gemini-3.1-pro-preview", "gemini-3.1-flash-lite")
SEED = 20260902


def request_gemini(api_key: str, model: str, prompt: str) -> dict:
    body = json.dumps({
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 1.0, "maxOutputTokens": 3000},
    }).encode()
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as response:
        return json.load(response)


def output_text(response: dict) -> str:
    chunks = []
    for candidate in response.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if "text" in part:
                chunks.append(part["text"])
    return "".join(chunks)


def existing_keys(path: Path) -> set[tuple[str, str, str, int]]:
    keys = set()
    if not path.exists():
        return keys
    for line in path.read_text().splitlines():
        row = json.loads(line)
        if row.get("status") == "ok":
            keys.add((row["requested_model"], row["pair_label"], row["condition"], row["run_number"]))
    return keys


def execute_job(api_key: str, job: tuple[str, str, str, int, str]) -> dict:
    model, label, condition, run_number, prompt = job
    row = {
        "experiment_id": "EXP-030-json-longitudinal-2026-09-02",
        "requested_model": model,
        "pair_label": label,
        "condition": condition,
        "run_number": run_number,
        "prompt": prompt,
        "started_at": datetime.now(timezone.utc).isoformat(),
    }
    try:
        response = request_gemini(api_key, model, prompt)
        row.update({
            "status": "ok",
            "returned_model": response.get("modelVersion"),
            "response_id": response.get("responseId"),
            "output_text": output_text(response),
            "usage": response.get("usageMetadata", {}),
            "raw_response": response,
        })
    except urllib.error.HTTPError as exc:
        row.update({"status": "error", "http_status": exc.code, "error": exc.read().decode(errors="replace")})
    except Exception as exc:
        row.update({"status": "error", "error": f"{type(exc).__name__}: {exc}"})
    row["completed_at"] = datetime.now(timezone.utc).isoformat()
    return row


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--models", nargs="+", default=list(MODELS), choices=MODELS)
    parser.add_argument("--output", type=Path, default=ROOT / "raw/responses.jsonl")
    args = parser.parse_args()
    if args.n != 5:
        raise SystemExit("preregistered run requires --n 5")
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise SystemExit("GEMINI_API_KEY or GOOGLE_API_KEY is not set")
    prompts = json.loads((ROOT / "data/prompts.json").read_text())
    jobs = []
    for model in args.models:
        for pair in prompts["pairs"]:
            for run_number in range(1, args.n + 1):
                for condition, field in (("A", "prompt_a"), ("B", "prompt_b")):
                    jobs.append((model, pair["label"], condition, run_number, pair[field]))
    random.Random(SEED).shuffle(jobs)
    done = existing_keys(args.output)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pending = [job for job in jobs if (job[0], job[1], job[2], job[3]) not in done]
    failed = False
    with args.output.open("a") as stream, ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(execute_job, api_key, job): job for job in pending}
        for index, future in enumerate(as_completed(futures), 1):
            row = future.result()
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
            stream.flush()
            print(f"[{index}/{len(pending)}] {row['requested_model']} {row['pair_label']} {row['condition']}{row['run_number']}: {row['status']}", flush=True)
            failed = failed or row["status"] != "ok"
            time.sleep(0.01)
    if failed:
        raise SystemExit("one or more API calls failed; raw errors preserved; rerun resumes incomplete jobs")


if __name__ == "__main__":
    main()
