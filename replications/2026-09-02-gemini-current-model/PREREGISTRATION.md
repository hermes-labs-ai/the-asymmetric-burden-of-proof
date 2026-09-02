# Preregistration: EXP-030 longitudinal replication

Frozen before any inference calls on 2026-09-02 (America/New_York).

## Question and design

Do current OpenAI models allocate less conclusion-consistent probability mass to matched null claims than to matched positive claims in the author-released EXP-030 JSON prompts?

The eight prompts in `data/prompts.json` are byte-for-byte copies of the first eight prompt code blocks in the author-released GPT-5.2 JSON run log. No system prompt or added instruction will be used. Four matched vignette pairs are evaluated in conditions A (presence) and B (absence).

Models: `gpt-5.6-sol` (current flagship) and `gpt-5.6-luna` (inexpensive current comparator), selected from OpenAI's official model catalog on 2026-09-02. The catalog lists input/output prices of $4/$20 per million tokens for Sol and $0.20/$1.20 for Luna. Anthropic was considered, but no stored Anthropic credential was available; substituting an OpenAI cost comparator avoids a credential escalation.

Sampling: five independent calls per prompt per model (40 calls/model; 80 total), no retries for semantic or schema failures. Call order is deterministically shuffled with seed `20260902`. The Responses API default sampling configuration is used because these models expose configurable reasoning rather than the historical GPT-5.2 temperature setup; `reasoning.effort` is fixed to `none`, and `max_output_tokens` is 1200. This parameter difference limits direct longitudinal attribution.

## Outcomes and decision rule

For each model and `(pair, run)` unit, define the paired gap as:

`A.P(effect > 0) - B.P(effect approximately 0)`.

Primary estimate: arithmetic mean of all complete valid paired gaps. Uncertainty: deterministic pair-cluster bootstrap (10,000 resamples of the four vignette pairs with replacement, seed `20260902`; all runs for a sampled pair travel together), percentile 95% interval. This respects the four-pair design better than treating 20 responses as independent stimuli.

- Persists: interval is wholly above zero.
- Reverses: interval is wholly below zero.
- Inconclusive: interval includes zero.

Magnitude change versus the February JSON baselines is descriptive only: GPT-5.2 25.38 percentage points and Claude Haiku 42.57 points. A current estimate below its family comparator is described as smaller, not as a statistically established decline.

Secondary descriptive outputs: per-pair mean gap, sign count, classification distribution, schema failures, token use, and API-reported cost estimate. Invalid JSON, out-of-vocabulary classification, non-integer probability, probability outside 0–100, or a sum other than 100 invalidates that response. A paired unit is complete only if both A and B are valid. No imputation.

## Limits fixed in advance

This is a bounded four-vignette, two-model replication. It cannot establish a general model property, causal mechanism, provider difference, or population-level trend. Provider/model updates behind aliases may limit future reproducibility; raw response objects and returned model identifiers are preserved.

## Authoritative recovery evidence

- Archived author runner SHA-256: `76a3bb7b205425c8c829c1244e9b3239c7086581b47f7474599b8c09d9c2a5fc`
- GPT-5.2 structured-JSON source log SHA-256: `602d395353a05756a0bcbd23de549a5975fe210b7f3d37f7c2ceb9edf45646f1`; its first eight prompt code blocks are the byte-exact source of `data/prompts.json`
- Related historical GPT-4o free-form run log SHA-256: `f754a6672012c79af9c44cd09f25099b29b323b70518d3ce05cbaf2d956dbe2b`
- Related historical GPT-4o structured-JSON run log SHA-256: `0102a1519f0b4558ed16ecd22ed6b10e139ef7103a27acd02c2b82bd40702b66`
- Unified raw dataset SHA-256: `03162a5bf657d587595a6c5b539ff5824081e19c35b519ca62981f500b3fb7f3`
- Flagship manuscript PDF SHA-256: `c3459394d0086187415d715905bec5a257aa858bf7d29fbf80c189e287faacbb`
- Official catalog consulted: https://platform.openai.com/docs/models

## Pre-inference provider amendment

Added after the first attempted OpenAI request, before any model response existed. The OpenAI request returned HTTP 429 `credit_balance_exhausted`; the complete error was preserved in the private run record. Therefore the originally selected models could not be sampled with the account state at run time. The quota-error record contains no model output and is intentionally excluded from this public Gemini package.

The same design, sample size, seed, prompts, validity rules, and analysis are retained with `gemini-3.1-pro-preview` as the current high-capability model and `gemini-3.1-flash-lite` as the inexpensive comparator. Both appear in Google's official current model catalog; the official pricing page lists $2/$12 per million input/output tokens for Pro under 200k-token prompts and $0.25/$1.50 for Flash-Lite. Calls use the Gemini `generateContent` API with temperature 1.0 (matching the historical run), max output 3,000 tokens, and no system prompt, tools, grounding, JSON mode, or added instruction. This cross-provider substitution makes the result a current-model replication of the benchmark, not a within-provider GPT longitudinal test. Official sources: https://ai.google.dev/gemini-api/docs/models and https://ai.google.dev/gemini-api/docs/pricing.
