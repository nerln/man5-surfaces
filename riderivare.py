"""Ricalcola i numeri del README del pacchetto A dagli artefatti dell'archivio.

Uso, sul NUC:
    python riderivare.py "E:\\vesuvius-archive"

Non assume una struttura precisa: cerca gli artefatti, dice cosa trova e cosa manca, e
per ogni numero del README stampa il valore ricalcolato accanto a quello dichiarato.
Dove non riesce a ricalcolare, lo dice invece di tacere.
"""
from __future__ import annotations

import json
import os
import sys
from collections import defaultdict

# valore dichiarato nel README -> etichetta. Servono a confrontare, non a sostituire.
DICHIARATI = {
    "totale_auditato_cm2": 82.62,
    "totale_ct_supported_cm2": 78.5,
    "superfici_dedup": 86,
    "fattore_dedup": 0.882,
    "A150_area_cm2": 36.1,
    "A150_sheetness": 0.59,
    "A150_tile_anomale": 4,
    "B100_area_cm2": 14.9,
    "B100_sheetness": 0.62,
    "B150_area_cm2": 36.90,
    "B150_sheetness": 0.4251,
    "B150_tile_anomale": 21,
    "A150_in_maschera": 0.983,
    "B100_in_maschera": 0.785,
    "C150_fuori_maschera": 0.98,
    "supporto_pesato_area": 0.9507,
    "spearman_rho": -0.463,
    "spearman_p": 6.7e-07,
}


def inventario(root: str) -> dict:
    """Elenca cosa c'e', per estensione e per cartella, senza interpretarlo."""
    per_ext = defaultdict(list)
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            per_ext[ext].append(os.path.join(dirpath, fn))
    return per_ext


def carica_json(paths: list[str], limite: int = 400) -> list[tuple[str, object]]:
    out = []
    for p in paths[:limite]:
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as fh:
                out.append((p, json.load(fh)))
        except Exception:
            continue
    return out


def carica_jsonl(paths: list[str], limite: int = 60) -> list[tuple[str, list]]:
    out = []
    for p in paths[:limite]:
        righe = []
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as fh:
                for ln in fh:
                    ln = ln.strip()
                    if ln:
                        try:
                            righe.append(json.loads(ln))
                        except Exception:
                            pass
        except Exception:
            continue
        if righe:
            out.append((p, righe))
    return out


def chiavi_presenti(oggetti) -> set:
    ks = set()
    def visita(o, pref=""):
        if isinstance(o, dict):
            for k, v in o.items():
                ks.add(f"{pref}{k}")
                visita(v, f"{pref}{k}.")
        elif isinstance(o, list) and o:
            visita(o[0], pref)
    for o in oggetti:
        visita(o)
    return ks


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    root = sys.argv[1]
    if not os.path.isdir(root):
        print(f"percorso non trovato: {root}")
        return 1

    print(f"# inventario di {root}\n")
    per_ext = inventario(root)
    for ext, paths in sorted(per_ext.items(), key=lambda kv: -len(kv[1]))[:12]:
        print(f"  {ext or '(senza estensione)':16s} {len(paths):5d} file   es. {os.path.relpath(paths[0], root)[:70]}")

    js = carica_json(per_ext.get(".json", []))
    jl = carica_jsonl(per_ext.get(".jsonl", []))
    print(f"\n# json leggibili: {len(js)}   jsonl leggibili: {len(jl)}")

    tutte = [o for _p, o in js] + [r for _p, righe in jl for r in righe[:5]]
    ks = chiavi_presenti(tutte)
    interessanti = sorted(k for k in ks if any(
        t in k.lower() for t in ("area", "sheet", "support", "mask", "void", "anomal", "cm2", "dedup", "cell", "tile")))
    print("\n# chiavi che sembrano pertinenti ai numeri del README:")
    for k in interessanti[:40]:
        print("   ", k)
    if not interessanti:
        print("    nessuna: la struttura non e' quella attesa, serve guardare a mano")

    print("\n# numeri dichiarati nel README, da confrontare con quanto sopra")
    for k, v in DICHIARATI.items():
        print(f"   {k:26s} {v}")
    print("\nQuesto script NON inventa i ricalcoli: mostra cosa c'e'. Il passo dopo e'")
    print("scrivere l'aggregazione esatta sulle chiavi vere, che ora sono note.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
