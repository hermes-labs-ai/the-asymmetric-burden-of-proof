# Contributing

This repository is the archival package for a Zenodo-deposited research
paper:

> Rolando Bosch, "The Asymmetric Burden of Proof: LLMs Show a Null-Result
> Asymmetry in a Matched-Vignette Benchmark," Zenodo working paper (2026).
> <https://doi.org/10.5281/zenodo.18867694>

It is not a software project. It does not accept feature contributions, new
functionality, or general code submissions, and there is no development
workflow or code review process to join. `verify.py` (and the replication's
own `verify.py` under `replications/`) are offline integrity and
reproduction checkers, not applications to extend.

## What is useful

- Corrections to the archived text: a typo, a broken link, or a reference
  that does not resolve as described in `REFERENCE-AUDIT.md`.
- Corrections to the metadata or citation records: `CITATION.cff`,
  `CITATION.bib`, `metadata.json`, `codemeta.json`, or `.zenodo.json`.
- A concrete, reproducible defect in the archived
  `replications/2026-09-02-gemini-current-model/` package (for example, a
  step in the reviewer reproduction path that does not run as documented).
- Reports of a mismatch between this repository and the canonical Zenodo
  record or DOI (`10.5281/zenodo.18867694`).

This is not an invitation to submit new replications, additional models, or
extended analyses as pull requests; those are separate research contributions
and outside what this repository accepts.

## How to raise one

Open an issue in this repository describing the specific correction, with a
reference to the exact file, page, or section affected. If you would rather
not use GitHub, email <roli@hermes-labs.ai>.

There is no fixed review timeline. The published PDF itself is not edited in
place — a substantive correction to the paper's content is handled through a
new Zenodo version, not a pull request here. Corrections confined to this
repository's non-PDF files (citation and metadata records, documentation
prose) may be made directly in this repository.
