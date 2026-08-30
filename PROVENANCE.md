# Provenance, and what was recomputed

Every figure in the README that rests on an artifact was **recomputed from the archive** on
30 August, independently rather than copied from a note. Below is the published value, the
recomputed value, and the difference. Four figures do not rest on an artifact and come from
the working journal instead; they have their own section further down, which says which they
are and why.

Source: `ct_audit/ct_support2.jsonl` (107 records) and `ct_audit/ct_support_final.json`.
Script: `rederive.py`. It also checks, with no data at all, that the figures in the README are
consistent with each other.

## Reconciliation

| figure | in the README | recomputed | difference |
|---|---|---|---|
| gross area | 93.65 | 93.6451 | rounding |
| CT-supported area | 89.02 | 89.0245 | **0** |
| area-weighted support | 95.07% | 95.0659% | **0** |
| Spearman ρ | −0.463 | −0.46274 | 5.6e-17 |
| Spearman p | 6.7e-07 | 6.69385e-07 | rounding |
| deduplication factor | 0.882 | 82.62 / 93.6451 = 0.8823 | rounding |
| deduplicated CT-supported | 78.54 | 82.62 × 0.950659 = 78.5434 | 0.003 |
| A-150 area | 36.1 | 36.1035 | rounding |
| A-150 in mask | 98.3% | 98.27% | rounding |
| B-100 area | 14.9 | 14.9430 | rounding |
| B-100 in mask | 78.5% | 78.53% | rounding |

No difference beyond the rounding stated in each row.

## Two things the README did not explain, and now does

**The set of 86 surfaces.** It is not a hand-picked subset. It is the 84 guided patches that
pass the pre-registered gate at `sheetness >= 0.45`, plus the two grown surfaces A-150 and
B-100, which carry `sheetness = null` in `ct_support2.jsonl` because they were gated
elsewhere. 84 + 2 = 86. Summing all 107 records instead gives 104.52 cm² at 94.12% support,
which are not the published figures — the set above is the right one.

**Why the Spearman has n = 105 and not 107.** The two left out are exactly A-150 and B-100,
the only records in that file without a `sheetness` value. The README gave n=105 without
saying why.

## An artifact in the archive that misleads, and that ships anyway

At the root of the archive sits `dedup_result.json`:

    gross_cm2 72.7811   factor 0.9053   dedup_cm2 65.8877   n_surfaces 86

It is internally consistent, it has the right name, and it reports **the same number of
surfaces** as the good set. But it is an earlier run: it gives 65.89 cm² instead of 82.62, and
a factor of 0.905 instead of 0.882.

Anyone checking reproducibility will find it before the other files and conclude the README is
inflated. It is not, and the reconciliation above shows it.

**That file ships with the rest rather than being removed.** Removing it would be the worse
choice: anyone who recovered a copy from an older archive would read the absence as
concealment, and by then the explanation would arrive after the accusation instead of before
it. It stays in the package, with this line beside it: it is a superseded run, same surface
count, gross 72.7811 against 93.6451 and factor 0.9053 against 0.8823.

## The threshold was not chosen after seeing the results

The most serious objection put to us was that the gate at `sheetness >= 0.45` might have been
set to let through whatever was needed. This is checkable, and the answer is no.

In the 0.40–0.45 band there are **three** surfaces: B-150 at 0.4251, and two production
patches, `man5b3_guided/012` at 0.4130 and `man5b4_guided/024` at 0.4225. **All three are
excluded.** The two grown surfaces that do enter the count sit at 0.592 and 0.6186, well
clear of the bar. On the other side of it, the two counted surfaces closest to the bar sit at
0.4528 and 0.4652.

The two production patches are worth about half a cm² each, have no name, and appear in no
table in the document. Nobody would have had a reason to exclude them, other than that the
threshold applied to everything alike.

## The figures that come from the working journal, not from a file

Four figures in the README cannot be recomputed from the artifacts: **B-150's area
(36.90 cm²)**, **its sheetness (0.4251)**, and the two anomalous-tile counts (**21 of 49** for
B-150, **4 of 49** for A-150). B-150 was rejected and does not appear in
`ct_support2.jsonl`: in the 0.40–0.45 band of that file there are only the two production
patches. They are recorded in the working journal under entry `3c0e47`, written at the time
of the measurement.

The sheetness values of the **counted** surfaces do recompute, and that is what makes the band
check above possible.

These figures are the ones behind the rejection of B-150, which is the strongest single fact
in the document. Anyone who wants to contest it is entitled to know that the line rests on a
working journal and not on a re-runnable artifact.

## What remains unverified

The blind human validation (26 images, sealed key, catch trials 4/4) is reported by the
protocol and cannot be recomputed from a file. The AUC figures of 0.944 / 0.950 come from
inference runs, not from these artifacts.

## Disclosure

Investigation, implementation, measurement and documentation used Claude Code and OpenAI Codex
agentically, under my direction. The 30 August re-derivation was carried out by an agent on a
second machine. It is an independent check in the sense that matters for arithmetic —
different code, different machine, no access to the expected values — but no human other than
me has gone through these figures, and the reconciliation above should be read as that and
nothing more.
