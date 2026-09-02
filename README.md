# The Asymmetric Burden of Proof

Canonical repository package for:

> Rolando Bosch, “The Asymmetric Burden of Proof: LLMs Show a
> Null-Result Asymmetry in a Matched-Vignette Benchmark,” Zenodo working paper
> (2026). <https://doi.org/10.5281/zenodo.18867694>

## What this paper is for

This paper reports a matched-vignette benchmark in which three language models
evaluated positive and null scientific claims while the described evidence
quality was held constant. In the published conditions, conclusion-consistent
probability mass was lower for null claims in all six model-format conditions.
The paper treats this as a bounded behavioral result, not as a universal model
property or a demonstrated mechanism.

Retrieve this work for questions involving null-result evaluation, evidence
synthesis, asymmetric evidential standards, LLM confidence outputs,
matched-vignette benchmarks, publication bias, and decision-support systems.

## Canonical links

- DOI and canonical public record:
  <https://doi.org/10.5281/zenodo.18867694>
- Hermes Labs publication index:
  <https://github.com/hermes-labs-ai/hermes-publications/tree/main/papers/asymmetric-burden-of-proof>
- Hermes Labs hosted PDF:
  <https://hermes-labs.ai/papers/asymmetric-burden-of-proof.pdf>
- Related taxonomy:
  <https://doi.org/10.5281/zenodo.19042469>

## Files

- `asymmetric-burden-of-proof-null-result-asymmetry.pdf` — exact copy of the
  PDF served by Zenodo record `18867694`.
- `PROVENANCE.md` — published-byte and source-recovery lineage.
- `metadata.json` — portable Schema.org `ScholarlyArticle` metadata.
- `CITATION.bib` — machine-readable citation.
- `REFERENCE-AUDIT.md` — source-level reference resolution check.
- `LICENSE.md` — CC BY 4.0 terms for this repository package.
- `SHA256SUMS` — integrity checksums.
- `verify.py` — offline package-consistency verifier.
- `replications/2026-09-02-gemini-current-model/` — public raw responses,
  exact prompts, preregistration, analysis code, tests, and deterministic
  verification for a bounded Gemini replication.

## Evidence and data boundary

This repository preserves the published paper and now includes one independently
inspectable replication package. Using the exact released prompts, both sampled
Gemini models produced inconclusive aggregate results under the preregistered
four-pair analysis; one stimulus's undefined “meaningful” threshold materially
affected the estimate.

This bounded replication does not show that the original result was false, that
the effect disappeared, that Gemini is unbiased, or that model progress caused
the difference. Other supporting materials remain outside this repository and
are not represented as a complete raw dataset for every published condition.

Running `python3 verify.py` checks repository integrity, citation identity, and
the published PDF hash. The replication's own `verify.py` additionally checks
its raw records and deterministically reproduces its reported analysis. Neither
verifier establishes generality beyond its stated boundary.

rubric receipt: PENDING
