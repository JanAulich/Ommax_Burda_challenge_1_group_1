#!/usr/bin/env python3
"""Offline integrity check for the dataset (standard library only).

    python3 scripts/validate_dataset.py          # from the repository root
    python3 scripts/validate_dataset.py --build-corpus   # also (re)write evidence/corpus.jsonl and manifest

Checks: parseable UTF-8 CSVs, unique IDs, every *_id(s) foreign key resolves, topic keys exist in the taxonomy,
numeric indicator values, valid enums, every new record has a source, corpus and manifest consistency.
It validates integrity, not factual truth.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TABLES = {
    "00_topic_taxonomy.csv": "topic_key", "01_portfolio.csv": "project_id", "02_learnings.csv": "learning_id",
    "03_signals.csv": "signal_id", "04_competitors.csv": "competitor_id", "05_market_indicators.csv": "indicator_id",
    "06_entity_populations.csv": "population_id", "07_regulatory_events.csv": "event_id", "08_sources.csv": "source_id",
    "09_opportunity_spaces.csv": "context_id",
}
FK = {  # column -> table it must resolve to
    "source_ids": "08_sources.csv", "source_id": "08_sources.csv", "public_source_ids": "08_sources.csv",
    "signal_ids": "03_signals.csv", "supporting_signal_ids": "03_signals.csv", "indicator_ids": "05_market_indicators.csv",
    "population_ids": "06_entity_populations.csv", "competitor_ids": "04_competitors.csv", "event_ids": "07_regulatory_events.csv",
    "learning_ids": "02_learnings.csv", "portfolio_ids": "01_portfolio.csv",
}
ENUMS = {
    ("03_signals.csv", "evidence_status"): {"curated_unverified", "derived_hypothesis", "source_backed_summary"},
    ("09_opportunity_spaces.csv", "commercial_evidence_status"): {"plausible_but_unvalidated", "unclear"},
    ("06_entity_populations.csv", "master_list_availability"): {"public_register", "chamber_directory", "association_member_list",
                                                                "commercial_database", "fragmented", "none_known"},
    ("00_topic_taxonomy.csv", "ymyl_default"): {"yes", "no", "partial"},
}


def load(name):
    with (DATA / name).open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def main(build_corpus: bool) -> int:
    errors, data = [], {}
    for name, key in TABLES.items():
        try:
            rows = load(name)
        except (OSError, csv.Error, UnicodeDecodeError) as exc:
            errors.append(f"{name}: cannot read ({exc})")
            continue
        ids = [r[key] for r in rows]
        if len(ids) != len(set(ids)):
            errors.append(f"{name}: duplicate {key}")
        data[name] = rows
    if errors:
        print("\n".join("ERROR: " + e for e in errors))
        return 1
    ids = {name: {r[TABLES[name]] for r in rows} for name, rows in data.items()}
    topics = ids["00_topic_taxonomy.csv"]
    for name, rows in data.items():
        key = TABLES[name]
        for r in rows:
            for col, target in FK.items():
                if col in r:
                    for ref in filter(None, (r[col] or "").split("|")):
                        if ref not in ids[target]:
                            errors.append(f"{name} {r[key]}: {col} -> unknown {ref}")
            for col in ("topic_key", "applies_to_topic_keys"):
                for t in filter(None, (r.get(col) or "").split("|")):
                    if t not in topics:
                        errors.append(f"{name} {r[key]}: unknown topic_key {t}")
            for (tab, col), allowed in ENUMS.items():
                if tab == name and r.get(col) not in allowed:
                    errors.append(f"{name} {r[key]}: {col}={r.get(col)!r} not in {sorted(allowed)}")
            if r.get("origin") == "v2_research" and not (r.get("source_ids") or r.get("source_id")):
                errors.append(f"{name} {r[key]}: research record without source")
    for r in data["05_market_indicators.csv"]:
        try:
            float(r["value"])
        except ValueError:
            errors.append(f"indicator {r['indicator_id']}: non-numeric value {r['value']!r}")
        if not r["source_id"]:
            errors.append(f"indicator {r['indicator_id']}: missing source")
    for r in data["08_sources.csv"]:
        if not r["url"].startswith("https://") and not r["url"].startswith("http://"):
            errors.append(f"source {r['source_id']}: missing URL")
    for r in data["09_opportunity_spaces.csv"]:
        for col in ("consumer_problem", "target_user", "potential_target_entity", "risks", "next_validation_questions"):
            if not r[col]:
                errors.append(f"space {r['context_id']}: empty {col}")

    corpus_path = ROOT / "evidence" / "corpus.jsonl"
    if build_corpus:
        corpus_path.parent.mkdir(exist_ok=True)
        with corpus_path.open("w", encoding="utf-8") as fh:
            for name, rows in data.items():
                if name == "00_topic_taxonomy.csv":
                    continue
                for r in rows:
                    fh.write(json.dumps({"id": r[TABLES[name]], "file": name, "topic_key": r.get("topic_key", ""),
                                         "text": "\n".join(f"{k}: {v}" for k, v in r.items() if v), "metadata": r},
                                        ensure_ascii=False) + "\n")
        manifest = {"dataset_version": "2.0", "snapshot_date": "2026-11-09", "csv_encoding": "UTF-8", "csv_delimiter": ",",
                    "list_separator": "|",
                    "files": {}}
        for name in list(TABLES):
            p = DATA / name
            if p.exists():
                manifest["files"]["data/" + name] = {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                                                     "rows": len(load(name))}
        manifest["files"]["evidence/corpus.jsonl"] = {"sha256": hashlib.sha256(corpus_path.read_bytes()).hexdigest(),
                                                      "rows": len(corpus_path.read_text(encoding="utf-8").splitlines())}
        (ROOT / "dataset_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    mpath = ROOT / "dataset_manifest.json"
    if mpath.exists():
        manifest = json.loads(mpath.read_text())
        for rel, entry in manifest["files"].items():
            p = ROOT / rel
            if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest() != entry["sha256"]:
                errors.append(f"manifest checksum mismatch: {rel} (re-run with --build-corpus after editing data)")

    if errors:
        print("\n".join("ERROR: " + e for e in errors[:200]))
        print(f"{len(errors)} error(s)")
        return 1
    for name, rows in data.items():
        print(f"OK {name}: {len(rows)} rows")
    print("PASS: IDs unique, all foreign keys and topic keys resolve, enums valid, every research record sourced, manifest consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main("--build-corpus" in sys.argv))
