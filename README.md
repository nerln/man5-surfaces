# man5-surfaces

Traced surface geometry on PHerc. MAN5, a scroll with no published segments. This is the
quality gate that decided what counted, an independent CT check that graded the same
surfaces a second way, and what both of them found.

Two numbers, because they answer different questions: **82.62 cm²** of deduplicated surface
passed the gate, and **78.54 cm²** of that is supported by the CT.

The second was re-derived independently from the stored artifacts with no difference at all.
The first is partly re-derived: the gross area it starts from, 93.6451 cm², reconciles
exactly, but the deduplication factor applied to it does not, because the overlaps it came
from were not kept. That is set out below and in `PROVENANCE.md` rather than left for a
reader to discover.

On scale, stated so it cannot be read as more than it is. The gate accepted 86 surfaces
totalling 93.64 cm², 84 of them tiles of roughly half a cm²; after deduplication that is
82.62. The largest single surface here is A-150 at 36.10 cm².

The comparison anyone can check is PHercMANBp. Ten of its eleven published segments expose an
`area_cm2` in `mesh/intermediate/tifxyz_original/meta.json` on the open-data bucket; the
eleventh publishes a `meta.json` without that field. Those ten run from 0.48 to 13.13 cm²,
median 4.67, total 55.44. Against that total this run is a factor of 1.49, not an order of
magnitude. Two more figures from the same source, equally repeatable: the median published
PHerc0139 segment is 38.42 cm², which A-150 sits below, and PHerc0814 carries single surfaces
of 111.18 and 108.98 cm², each larger than this entire total.

Those depend on two choices, stated because a reader who makes them differently will get
different numbers. The area is read from `tifxyz_original`, whose sibling `tifxyz_normalized`
and `tifxyz_flattened` documents carry `area_cm2: null`. And segments publishing no area are
left out of the statistics rather than counted as zero: on PHerc0139 that is 34 segments of
38, on PHerc0814 12 of 19. `public_areas.sh` prints that listing for any of the three scrolls,
anonymously over HTTP, and is where these figures come from.

On how those surfaces were made, the public record supports less than I first wrote here.
There is no `auto_grown` field in the catalogue, and no PHercMANBp segment carries that string
in its name. What each of the ten does carry is a `seed_surface_id` beginning `auto_grown_`.
Several of those ids end in `_inp_hr` or `-w3`, which point to processing after the seed. The
record therefore says what a surface was grown from, not how much hand work followed, and this
comparison should not be read as one against hand-curated segments.

What is new here is that the scroll had nothing published at all, not that any one surface is
large.

## The gate rejected what looked best

Four figures in this section cannot be recomputed from the stored artifacts: B-150's area
and its sheetness, and the two anomalous-tile counts. B-150 was rejected and does not appear
in the audit file at all. They come from a work log written at the time, entry `3c0e47`.
`PROVENANCE.md` says which figures are recomputable and which are not.

`B-150` came out at 36.90 cm² and looked like the best surface of the run. The gate refused
it: sheetness 0.4251 against a counting bar of 0.45, and 21 of 49 tiles anomalous against 4
of 49 for the surface that passed. That is drift at the edges. It does not enter the total.

What can be checked about that bar is that it was applied without exception. Three surfaces
fall in the 0.40 to 0.45 band and none of them is counted, including two half-cm² production
patches that appear in no table here and that nobody had a reason to drop. The two counted
surfaces closest to the bar sit at 0.4528 and 0.4652, just above it.

Without the gate the run would have counted about 75 cm² of degraded surface as sound,
B-150 and C-150 together, for a total 90% larger with the added part mostly wrong.

What counted: `A-150` at 36.1 cm² (sheetness 0.59, 4 of 49 anomalous), `B-100` at 14.9 cm²
(sheetness 0.62), and 84 production patches. 86 surfaces, dedup factor 0.882, with the
method declared before the count.

That factor is the one number here that cannot be recomputed from the archive. The pairwise
overlaps it came from were not kept, and the only dedup artifact in the archive is from a
superseded run that gives 0.9053. Everything downstream of 82.62 cm² reconciles exactly;
82.62 itself rests on a gross area of 93.6451 cm², which does reconcile, times a factor that
does not.

## A second channel that shares no code with the first

The gate is geometric. This check is radiometric, computed from the CT, and shares no
threshold with it. For each surface: what fraction of its support falls inside the sheet mask
within ±29 µm, and the sign of the mean profile.

| surface | in mask | mean profile | verdict |
|---|---|---|---|
| A-150 | 98.3% | +0.017 (L1), +0.021 (L0), enrichment 1.74× over ambient | supported |
| B-100 | 78.53% | — | overflow at the east margin, ~3.2 of its 14.94 cm² unsupported |
| C-150 | 2% | — | rejected, and the CT agrees with the gate |

Over all 107 surfaces at 1296 to 1500 cells each, the deduplicated set of 86 has an
area-weighted support of 95.07%. That is where the two headline numbers come from. One step
in that is an assumption rather than a measurement: the 95.07% is weighted over the gross
93.6451 cm², and applying it to the deduplicated 82.62 assumes that removing overlap removes
supported and unsupported area in the same proportion. The overlaps were not kept, so that
cannot be checked.

The two channels rank the surfaces the same way without being told to. Void fraction against
the gate's sheetness gives Spearman ρ = −0.463, p = 6.7 × 10⁻⁷, with accepted surfaces
averaging 1.8% void and rejected ones 14.1%. Neither measure is derived from the other.

## A blind self-check, not a third party

26 images, key sealed before the read. The reader was me. I was blind to the key, not
independent of the experiment, and this repository carries my name, so this is a self-check
and not a third opinion. It is worth reporting anyway, because a self-check can still fail.

On the ink question I could not separate the MAN5 positives from the displaced controls,
4 of 5 against 4 of 6 called "lines". Those were the rasters of the first pass, the one
withdrawn above, so that read says nothing about the corrected re-run. On and off sheet at
8 to 13 voxels was not separable either, which is what a thin sheet predicts.

The four catch trials I identified were rendered to completely empty volumes: 159 kB each
against 5.6 to 6.2 MB for every positive and every displaced control. Getting those right
shows I was paying attention. It is not a grading of void against tissue, and it is not a
third channel agreeing with the other two.

One result from that read limits what anyone can claim from this material later. The reader
saw "lines" in the off-sheet controls too. A claim that lines are visible here, offered
without displaced controls, is pareidolia.

## What did not work

The biggest failure of the run was the first ink pass, and it is the reason the rule in
#1648 exists. It went wrong before it went right, and the order matters.

The first pass was pre-registered, ran to completion, and returned a clean negative. It was
not usable. `ink_pass.py` called the preparer with `--level 0` and never passed
`--flip-normals`, which is the cell of the 2×2 matrix in #1648 that scores at chance
whatever else is true, and the 13 jobs it ran contained no positive control. By the rule
stated at the end of that issue — a null is uninterpretable without a positive control
through the identical harness in the same execution — that first pass says nothing.

The two faults were isolated and the pass was redone at the correct scale and in both depth
orders. That corrected re-run is not conclusive either, and no ink result is reported here.
The pre-registration covers the design, not the run that was withdrawn.

On the instrument: the harness scores AUC 0.949/0.955 on `w035`, but `w035` is in the
training corpus of those checkpoints, so that is an in-training figure. The out-of-training
check is `w024`, where the output reaches Pearson 0.50 against the two published models'
agreement with each other of 0.54.

A per-cell contrast test does not discriminate on this scroll. CT modulation is 2 to 5% and
the windings are in contact, so it calls 51 to 53% positive even on validated surfaces. It
was dropped, and the two measures above replaced it.

Three separate paths in the audit code produced the same silent zero: flank sampling landing
on neighbouring wraps, cache eviction before use, and a negative cache that wrote a permanent
"empty" marker on any exception. One of them took a surface from 0% to 99% "empty" in a single
run. All three were fixed before the numbers above were computed, and a surface that read 89%
drift read 46% once the sampling was batched.

## Where this sits

`automesh` and similar work validate tracing where a reference surface already exists. This
is the other case. There are no published segments, so the only checks available are internal
consistency and an independent physical channel. The two approaches answer different
questions.

## Limits

Neither of the two instruments is a ground truth, because on MAN5 there is none: no segment
has been published on this scroll. What they measure is agreement between two checks that
share no code, no thresholds and no inputs, with a blind self-check alongside them. That is
weaker than a reference.

One scroll. The gate's thresholds have not been tested on another. 78.54 cm² is CT-supported
and the remaining 4.08 cm² is not, with B-100's east margin the known part of that. No ink
result is claimed here at all: the pre-registered pass was withdrawn and the corrected re-run
is not conclusive.

## Data

Raw `tifxyz` surfaces, ink rasters and per-cell JSONL are on an offline archive and will be
attached as release assets in early September. `PROVENANCE.md` records, for every figure
above, where it comes from and whether it was re-derived. `rederive.py` needs neither the
archive nor any dependency to check that the published figures are consistent with each
other; given the archive it recomputes them from the audit records.

## Disclosure

Investigation, implementation, measurement and documentation used Claude Code and OpenAI
Codex agentically under my direction. Every figure comes from runs on public data or on the
archive described above, and `PROVENANCE.md` says for each one whether it was recomputed.

## Related

- [ScrollPrize/villa#1547](https://github.com/ScrollPrize/villa/issues/1547) — duplicate traced surfaces in the published catalogue
- [ScrollPrize/villa#1580](https://github.com/ScrollPrize/villa/pull/1580) — prepared-input scale check for ink inference
- [ScrollPrize/villa#1582](https://github.com/ScrollPrize/villa/issues/1582) — representation-family provenance
- [ScrollPrize/villa#1648](https://github.com/ScrollPrize/villa/issues/1648) — what the two ink input faults cost
- [nerln/vesuvius-ladder](https://github.com/nerln/vesuvius-ladder) — the duplicate detector behind #1547
