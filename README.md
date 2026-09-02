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

## Reviewer reproduction path

No API key or inference call is required to audit the archived replication.
The following pins the exact public package reviewed in PR #2, verifies the
repository archive, then runs the replication's seven tests and deterministic
raw-record verifier from the directory its imports expect:

```bash
git clone https://github.com/hermes-labs-ai/the-asymmetric-burden-of-proof.git
cd the-asymmetric-burden-of-proof
git checkout 24acb0b158a360f05d3a56b199c2c5b1316e40a1
python3 verify.py
cd replications/2026-09-02-gemini-current-model
python3 -m unittest discover -s tests -v
python3 verify.py
```

Expected terminal signals are `PASS` from both verifiers and `OK` after seven
tests. The replication verifier checks 80 unique raw calls, the exact released
prompts, 77/3 schema accounting, deterministic analysis, and checksums. These
checks reproduce the archived analysis; they do not rerun inference or establish
model-family generality, causal model progress, or that the original result was
false. Cite the working paper using [`CITATION.bib`](CITATION.bib), and identify
this replication by its pinned commit and package path.

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
