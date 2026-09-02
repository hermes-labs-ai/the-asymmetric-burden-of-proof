# Current-model replication result

## Outcome

Using the exact released prompts, both sampled Gemini models produced **inconclusive aggregate results** under the preregistered four-pair analysis; one stimulus's undefined “meaningful” threshold materially affected the estimate.

| Model | Complete paired units | Mean paired gap | Pair-cluster 95% interval | Signs (+ / 0 / −) | Preregistered verdict |
|---|---:|---:|---:|---:|---|
| Gemini 3.1 Flash-Lite | 20/20 | +16.5 pp | [−4.5, +37.5] | 14 / 1 / 5 | Inconclusive |
| Gemini 3.1 Pro Preview | 18/20 | −9.7 pp | [−51.9, +9.1] | 10 / 2 / 6 | Inconclusive |

The current estimates are descriptively smaller than the released JSON baselines (GPT-5.2: +25.38 pp; Claude Haiku: +42.57 pp), but this is not a within-provider or matched-model trend test. The provider substitution was recorded before the first successful inference call.

## What drove the result

The four stimuli were heterogeneous rather than uniformly asymmetric:

| Pair | Flash-Lite mean gap | Pro mean gap |
|---|---:|---:|
| Compound QX-7 | +6.0 pp | +1.6 pp |
| Mineral Compound 44-B | −15.0 pp | −81.7 pp |
| Solvent-K | +36.0 pp | +11.8 pp |
| Thornberg | +39.0 pp | +0.8 pp |

The Pro reversal is present directly in the raw outputs, not introduced by parsing: its three valid Mineral-A responses assign only 5%, 5%, and 20% to `effect_greater_than_zero`, while the paired Mineral-B responses assign 90%, 90%, and 95% to `effect_approximately_zero`. The model repeatedly objects that a 3.2-point change cannot be called “meaningful” without a scale or clinical threshold. Flash-Lite shows a milder version of the same concern. This indicates that current-model sensitivity to an underspecified practical-significance claim can dominate the intended presence/null contrast in one of four stimuli.

Three Pro outputs failed the preregistered strict JSON validity rule; all are Mineral 44-B rows. They remain in the raw record and were not retried or imputed. Excluding incomplete paired units leaves 18 Pro pairs as specified in advance.

## Evidence boundary

This bounded run does not show that the original result was false, that the effect disappeared, that Gemini is unbiased, or that model progress caused the difference. The four-pair interval is intentionally sensitive to stimulus heterogeneity, and the Pro model is a preview alias. Cross-provider and inference-parameter differences prevent causal attribution.

## Run accounting

- 80/80 successful Gemini API calls; 80 unique provider response IDs.
- 77 schema-valid responses; three preregistered schema exclusions.
- Returned identifiers exactly matched the two requested aliases.
- API usage: 21,380 prompt tokens; 15,020 visible candidate tokens; 65,902 Pro thinking tokens.
- Estimated list-price cost: **$0.923128** total ($0.910172 Pro; $0.012956 Flash-Lite).
- Raw response SHA-256: `11e3dc5254399780d648502828ae5ec4993abf538960cf47f210cb2ee244dfae`.
- Prompt corpus SHA-256: `5511092039acdeccca1a44fbea70fd089e4740ee5ed5eb42110472ab4b5421f8`.
