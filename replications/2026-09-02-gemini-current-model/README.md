# September 2026 Gemini replication

This package is a public, raw-preserving record of a bounded current-model replication of the four-pair structured-JSON benchmark associated with *The Asymmetric Burden of Proof*.

Using the exact released prompts, both sampled Gemini models produced **inconclusive aggregate results** under the preregistered four-pair analysis; one stimulus's undefined “meaningful” threshold materially affected the estimate.

This does **not** show that the original result was false, that the effect disappeared, that Gemini is unbiased, or that model progress caused the difference. The run contains only four vignette pairs, crosses provider families and inference configurations, and uses a preview alias for one sampled model.

## Inspect and verify

No API access is required to inspect or recompute the result:

```bash
python3 -m unittest discover -s tests -v
python3 verify.py
```

`verify.py` checks the exact prompt corpus, all 80 raw API records, unique response identifiers, returned aliases, the 77/3 schema-validity accounting, deterministic analysis reproduction, and package checksums.

To repeat inference with current aliases, set `GEMINI_API_KEY` or `GOOGLE_API_KEY` and run:

```bash
python3 src/run.py
python3 src/analyze.py
python3 src/validate_run.py
```

Provider aliases can change after this recorded run. A new inference run is therefore a new observation, not a recreation of the same provider state.

## Contents

- `PREREGISTRATION.md` — frozen design plus the pre-inference provider amendment.
- `data/prompts.json` — eight exact released prompts.
- `raw/responses.jsonl` — complete raw Gemini API objects, exact submitted prompts, identifiers, usage, and timestamps for 80 successful calls.
- `results/analysis.json` — preregistered analysis output.
- `results/environment.json` — recorded inference environment and configuration.
- `results/REPORT.md` — bounded interpretation and run accounting.
- `src/` and `tests/` — inference, analysis, validation, and unit-test code.
- `SHA256SUMS` and `verify.py` — package integrity and reproducibility checks.

No credentials, quota-error records, private handoffs, caches, or local filesystem paths are included.
