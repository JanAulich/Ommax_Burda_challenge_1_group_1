# FACTS Topic Opportunity Scout

**TUM × OMMAX AI Hackathon · Challenge 1.** Build an AI prototype that recommends 3–5 specific new TOP-List topics
for FACTS, backed by evidence, with risks, open questions and a recommended status. **Everything you need is in this
folder — no crawling or scraping.**

## Start here (15 minutes)

1. **[docs/01_challenge_brief.md](docs/01_challenge_brief.md)** — what FACTS does, the task, the deliverable, how you're judged.
2. **[docs/02_evaluation_and_guardrails.md](docs/02_evaluation_and_guardrails.md)** — the six dimensions, evidence rules, when a human must review, an example card.
3. **[docs/03_data_guide.md](docs/03_data_guide.md)** — data model, columns, IDs, how to cite.
4. **[docs/05_deliverables_and_judging.md](docs/05_deliverables_and_judging.md)** — what to hand in, demo format, pass/fail gates, the full judging scorecard.
5. *(optional)* [docs/04_dataset_design_and_limitations.md](docs/04_dataset_design_and_limitations.md) — design choices behind the data and known limits.

## What's in the data

| File | Rows | What it gives you |
|---|---:|---|
| `data/00_topic_taxonomy.csv` | 32 | Topic keys that join every table, YMYL flag, likely FACTS brand |
| `data/01_portfolio.csv` | 43 | 36 organiser-supplied FACTS products (English) + 7 publicly observed ones; public edition/partner/method info |
| `data/02_learnings.csv` | 28 | Real public precedents: court rulings on seals (incl. FOCUS doctor seals), abolished/failed rating systems, ranking criticism |
| `data/03_signals.csv` | 173 | "Why now" observations — 143 source-backed, 25 curated-unverified, 5 derived hypotheses |
| `data/04_competitors.csv` | 149 | Rankings, seals, portals, registers, tests — with coverage / quality / provider-pays / methodology attributes |
| `data/05_market_indicators.csv` | 633 | Numeric observations (397 metrics, 50 series with ≥3 points): care demand, costs, sales, complaints, registrations, … |
| `data/06_entity_populations.csv` | 78 | How many entities exist per segment + where a master list could come from |
| `data/07_regulatory_events.csv` | 94 | Dated laws, deadlines, funding changes and rulings (18 still upcoming) |
| `data/08_sources.csv` | 403 | 296 publishers; period, review method (212 page reviews, 191 search snippets), limitations |
| `data/09_opportunity_spaces.csv` | 33 | Curated research starting points with linked evidence — **not answers, not ranked** |
| `evidence/corpus.jsonl` | 1,634 | Same records as JSON lines for RAG/embeddings (a view, not extra evidence) |

Snapshot date **2026-11-09**. All numbers keep their **observation period**. URLs are for attribution only.

## Quick start

```python
import csv
def load(name): return list(csv.DictReader(open(f"data/{name}", encoding="utf-8")))
spaces, indicators = load("09_opportunity_spaces.csv"), load("05_market_indicators.csv")
care = sorted((r["period"], r["value"]) for r in indicators if r["topic_key"] == "care_elderly")
```

Check integrity at any time: `python3 scripts/validate_dataset.py` (add `--build-corpus` after editing CSVs).

## Golden rules

1. Cite record IDs (`F001`, `S215`, `I0042`, `P007`, `C057`, `R012`, `L003`, `SRC145`, `M013`). Never invent IDs or numbers.
2. Facts ≠ hypotheses. Market size, data availability and willingness to buy a seal are hypotheses unless a record proves them.
3. Count independent **publishers**, not rows. Keep periods. Empty means unknown.
4. Show risks separately; flag human review with reasons (YMYL, overlap, precedents, weak evidence).
5. Be able to say **no** — Deprioritise and Do Not Pursue are valid, valuable outputs.

## Folder map

```
./
├── README.md                     ← you are here
├── docs/                         ← brief, guardrails, data guide, dataset design & limits, deliverables & judging
├── data/                         ← the dataset (participant input)
├── evidence/corpus.jsonl         ← retrieval view of data/
├── dataset_manifest.json         ← checksums and row counts
└── scripts/validate_dataset.py   ← integrity check
```
