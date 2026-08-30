"""Re-derive the figures in README.md.

Two modes, because the two halves of this package can be checked by different people.

    python3 rederive.py

        Needs no data and no dependencies. Checks that every relation the README
        states between its own figures actually holds, and prints the arithmetic
        behind each one. Anyone can run this right now.

    python3 rederive.py <archive-dir>

        Recomputes the figures from the stored audit artifacts, chiefly
        ct_audit/ct_support2.jsonl, and prints recomputed beside published with
        the difference. The artifacts are on an offline archive and will be
        attached as release assets; until then this half is a specification of
        exactly which aggregation produces each number, readable without them.

Where a figure cannot be recomputed, this says so instead of printing a number.
"""

from __future__ import annotations

import json
import os
import sys

# Every figure the README states. Values are as published, not as recomputed.
CLAIMED = {
    "gross_area_cm2": 93.6451,
    "ct_supported_area_cm2": 89.0245,
    "dedup_area_cm2": 82.62,
    "dedup_ct_supported_cm2": 78.54,
    "unsupported_cm2": 4.08,
    "area_weighted_support": 0.950659,
    "dedup_factor": 0.8823,
    "surfaces": 86,
    "tiles": 84,
    "spearman_rho": -0.463,
    "spearman_n": 105,
    "A150_area_cm2": 36.1035,
    "A150_in_mask": 0.9827,
    "B100_area_cm2": 14.9430,
    "B100_in_mask": 0.7853,
    "gate_threshold": 0.45,
    "MANBp_total_cm2": 55.44,
    "scale_factor_vs_MANBp": 1.49,
}

# Figures that come from the working journal rather than from an artifact, so no
# amount of data in the archive will reproduce them. The README says the same.
NOT_RECOMPUTABLE = {
    "B150_area_cm2": 36.90,
    "B150_sheetness": 0.4251,
    "B150_anomalous_tiles": 21,
    "A150_anomalous_tiles": 4,
}


def _close(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol


def check_arithmetic() -> int:
    """Check the relations the README states between its own figures."""
    c = CLAIMED
    checks = [
        (
            "area-weighted support = CT-supported / gross",
            c["ct_supported_area_cm2"] / c["gross_area_cm2"],
            c["area_weighted_support"],
            5e-6,
        ),
        (
            "dedup factor = deduplicated / gross",
            c["dedup_area_cm2"] / c["gross_area_cm2"],
            c["dedup_factor"],
            5e-5,
        ),
        (
            "headline 2 = deduplicated x area-weighted support",
            c["dedup_area_cm2"] * c["area_weighted_support"],
            c["dedup_ct_supported_cm2"],
            5e-3,
        ),
        (
            "unsupported = headline 1 - headline 2",
            c["dedup_area_cm2"] - c["dedup_ct_supported_cm2"],
            c["unsupported_cm2"],
            5e-3,
        ),
        (
            "scale factor = this run / PHercMANBp total",
            c["dedup_area_cm2"] / c["MANBp_total_cm2"],
            c["scale_factor_vs_MANBp"],
            5e-3,
        ),
        (
            "surfaces = tiles + the two grown surfaces",
            c["tiles"] + 2,
            c["surfaces"],
            0,
        ),
        (
            "Spearman n = surfaces in the CT file minus the two without sheetness",
            107 - 2,
            c["spearman_n"],
            0,
        ),
    ]

    print("Relations the README states between its own figures")
    print("-" * 78)
    failures = 0
    for name, computed, published, tol in checks:
        ok = _close(computed, published, tol)
        failures += 0 if ok else 1
        print(
            f"  [{'ok' if ok else 'FAIL'}] {name}\n"
            f"         computed {computed:.6f}   published {published}   "
            f"diff {abs(computed - published):.2e}"
        )

    # The mean tile area is not a published figure; it is the sanity check behind
    # the phrase "84 of them tiles of roughly half a cm2".
    rest = c["gross_area_cm2"] - c["A150_area_cm2"] - c["B100_area_cm2"]
    mean_tile = rest / c["tiles"]
    ok = 0.4 < mean_tile < 0.6
    failures += 0 if ok else 1
    print(
        f"  [{'ok' if ok else 'FAIL'}] the 84 tiles average roughly half a cm2\n"
        f"         computed {mean_tile:.4f} cm2 per tile"
    )

    print("-" * 78)
    print(f"{len(checks) + 1} relations checked, {failures} failed.\n")

    print("Figures that no data will reproduce, listed so they are not mistaken")
    print("for recomputed ones (the README and PROVENANCE.md say the same):")
    for k, v in NOT_RECOMPUTABLE.items():
        print(f"  {k:24s} {v}")
    print()
    return 1 if failures else 0


def _first_key(record: dict, *names: str):
    for n in names:
        if n in record and record[n] is not None:
            return record[n]
    return None


def _spearman(xs: list[float], ys: list[float]) -> float:
    """Rank correlation, average ranks for ties. No dependencies on purpose."""

    def ranks(v: list[float]) -> list[float]:
        order = sorted(range(len(v)), key=lambda i: v[i])
        out = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                out[order[k]] = avg
            i = j + 1
        return out

    rx, ry = ranks(xs), ranks(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = sum((a - mx) ** 2 for a in rx) ** 0.5
    dy = sum((b - my) ** 2 for b in ry) ** 0.5
    return num / (dx * dy) if dx and dy else float("nan")


def find_ct_file(root: str) -> str | None:
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in filenames:
            if fn == "ct_support2.jsonl":
                return os.path.join(dirpath, fn)
    return None


def recompute(root: str) -> int:
    path = find_ct_file(root)
    if path is None:
        print(f"ct_support2.jsonl not found under {root}")
        print("Nothing is recomputed. The relations above still hold on their own.")
        return 1

    records = []
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

    print(f"Recomputing from {path}")
    print(f"  {len(records)} records read (the README's audit had 107)\n")

    if not records:
        return 1

    sample = records[0]
    area_key = next(
        (k for k in ("area_cm2", "area", "surface_area_cm2", "cm2") if k in sample), None
    )
    supp_key = next(
        (k for k in ("in_mask", "support", "supported_fraction", "ct_support") if k in sample),
        None,
    )
    sheet_key = next((k for k in ("sheetness", "sheet_score") if k in sample), None)

    print("  fields used, chosen from the first record:")
    print(f"    area      -> {area_key or 'NOT FOUND'}")
    print(f"    support   -> {supp_key or 'NOT FOUND'}")
    print(f"    sheetness -> {sheet_key or 'NOT FOUND'}")
    if not (area_key and supp_key and sheet_key):
        print("\n  The field names in this file are not the expected ones. Keys present:")
        print("   ", sorted(sample.keys()))
        return 1
    print()

    # The counted set: patches passing the pre-registered gate, plus the two grown
    # surfaces, which carry sheetness null because they were gated elsewhere.
    gate = CLAIMED["gate_threshold"]
    counted = [
        r
        for r in records
        if r.get(sheet_key) is None or float(r[sheet_key]) >= gate
    ]
    gross = sum(float(_first_key(r, area_key) or 0.0) for r in counted)
    supported = sum(
        float(_first_key(r, area_key) or 0.0) * float(_first_key(r, supp_key) or 0.0)
        for r in counted
    )

    with_sheet = [r for r in records if r.get(sheet_key) is not None]
    rho = _spearman(
        [float(r[sheet_key]) for r in with_sheet],
        [float(_first_key(r, supp_key) or 0.0) for r in with_sheet],
    )

    rows = [
        ("surfaces counted", len(counted), CLAIMED["surfaces"], 0),
        ("gross area cm2", gross, CLAIMED["gross_area_cm2"], 5e-3),
        ("CT-supported cm2", supported, CLAIMED["ct_supported_area_cm2"], 5e-3),
        (
            "area-weighted support",
            supported / gross if gross else float("nan"),
            CLAIMED["area_weighted_support"],
            5e-5,
        ),
        ("Spearman rho", rho, CLAIMED["spearman_rho"], 5e-3),
        ("Spearman n", len(with_sheet), CLAIMED["spearman_n"], 0),
    ]
    print(f"  {'figure':24s} {'recomputed':>14s} {'published':>14s}   verdict")
    print("  " + "-" * 74)
    bad = 0
    for name, got, want, tol in rows:
        ok = _close(float(got), float(want), tol)
        bad += 0 if ok else 1
        print(f"  {name:24s} {float(got):14.6f} {float(want):14.6f}   {'ok' if ok else 'DIFFERS'}")
    print()

    # The deduplication factor is the one figure the archive cannot return: the
    # overlaps it was computed from were not kept. README and PROVENANCE say so.
    print("  dedup factor             not recomputable: the overlaps were not kept.")
    print("                           82.62 / 93.6451 = "
          f"{CLAIMED['dedup_area_cm2'] / CLAIMED['gross_area_cm2']:.6f} is consistency,")
    print("                           not an independent re-derivation.")
    print()
    print("  If dedup_result.json is also in this archive, it reports 65.8877 cm2 and")
    print("  factor 0.9053 for the same 86 surfaces. That is a superseded run, kept in")
    print("  the package on purpose. PROVENANCE.md explains it.")
    return 1 if bad else 0


def main(argv: list[str]) -> int:
    status = check_arithmetic()
    if len(argv) > 1:
        root = argv[1]
        if not os.path.isdir(root):
            print(f"archive directory not found: {root}")
            return 1
        status |= recompute(root)
    else:
        print("No archive directory given, so nothing was recomputed from data.")
        print("Pass one to recompute: python3 rederive.py <archive-dir>")
    return status


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
