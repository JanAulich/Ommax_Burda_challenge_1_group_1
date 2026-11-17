# Dataset design choices and known limitations

This document explains the design problems the dataset is built to solve — in the data and in the challenge design — and the known limits you should keep in mind. The original organiser pack was careful and labelled every uncertainty, but it was **too thin to build a convincing solution** from the CSVs alone; the choices below address that.

## 1. Data design

| # | Problem in the original pack | Consequence for teams | How this dataset addresses it |
|---|---|---|---|
| D1 | **Almost no numbers.** One statistic (SRC001, home care 2023) in the whole pack. | "Why now" could only be asserted, never shown; scoring was mostly text-matching. | `05_market_indicators.csv`: hundreds of numeric observations, mostly multi-year time series (care need, heat-pump sales, PV complaints, BEV/used-BEV, overindebtedness, lawyers/tax advisers, Kita gaps, …). |
| D2 | **No market or entity sizes.** | Commercial potential and master-list feasibility were pure guesswork — the brief's own next-step questions were unanswerable even as a first proxy. | `06_entity_populations.csv`: number of entities per segment + which register/directory could seed a master list + availability class. |
| D3 | **No dated "why now" drivers.** Regulatory signals were generic. | Teams could not distinguish *timely* from *perennial* topics. | `07_regulatory_events.csv`: laws, deadlines, subsidy changes and rulings with dates and `timing` (past/upcoming). |
| D4 | **Historical learning impossible.** The brief requires it, but no paused/discontinued cases existed and fictional history was forbidden. | A mandatory guardrail could not be answered. | `02_learnings.csv`: **real, public, sourced precedents** (court rulings on seal advertising, reforms of official quality ratings, discontinued services, ranking criticism) labelled `public_external_record` |
| D5 | **25 of 53 signals unverified, 5 broad hypotheses**; only 23 source-backed. | Evidence-first guardrail hard to meet. | Original signals kept (IDs stable, labels unchanged) + many new source-backed signals linked to indicators and events. |
| D6 | **Thin competitor table** (20 rows, text-only attributes). | White-space classification required free-text interpretation. | `04_competitors.csv` with structured attributes: `coverage`, `has_quality_assessment`, `has_seal_or_award`, `provider_pays`, `methodology_public` → market types become computable. |
| D7 | **Mixed German/English**, German free text in portfolio and signals. | Harder for international teams; weaker retrieval. | All fields in English (German proper nouns kept); original German titles preserved in `title_de`. |
| D8 | **No join key across tables** — topics matched by fuzzy German labels. | Fragile joins, inconsistent topic grouping. | `00_topic_taxonomy.csv` with `topic_key` on every table + `ymyl_default`. |
| D9 | **Portfolio lacked any public context** (first edition, partner, methodology). | Portfolio fit and overlap were name-matching only. | `01_portfolio.csv` adds `public_*` columns where public information was found (with sources). |
| D10 | **Only 12 market contexts**, mostly housing/health. | Teams tended to pick from the menu. | `09_opportunity_spaces.csv`: 33 spaces across 25 topic keys, auto-linked to evidence. They remain *starting points, not answers* — and solutions are expected to also find topics outside them. |
| D11 | Two alias files (`_expanded.csv`, JSONL) duplicated evidence. | Double counting risk. | One canonical CSV per entity; `evidence/corpus.jsonl` is generated and documented as a *view*. |

## 2. Challenge-design choices

| # | Weakness in the brief | Why it hurts | Adaptation |
|---|---|---|---|
| B1 | Requires "past/discontinued project learnings" that do not exist in the data. | Unfair: teams lose points on a guardrail they cannot satisfy. | Accept **public precedents (`L…`) as historical learning**. |
| B2 | "Commercial potential" demanded but no demand or seal-buyer data. | Invites invented market sizes. | Commercial labels defined (`evidenced` practically unreachable); entity populations + paid-visibility precedent (`provider_pays`) are the allowed proxies. |
| B3 | No definition of **YMYL** per topic. | Inconsistent review flags. | `ymyl_default` in the taxonomy (yes / partial / no). |
| B4 | No guidance on when a status is justified. | Teams default to "Validate Next" for everything. | Guardrails doc gives typical triggers per status; Definition of Done requires the tool to be able to say *no*. |
| B5 | "Competitive white space" taxonomy given, but no data to classify it. | Purely subjective. | Structured competitor attributes. |
| B6 | Brief had no worked example card with evidence IDs. | Unclear citation style. | Example card in `02_evaluation_and_guardrails.md`. |
| B7 | Long, repetitive documents (brief and guardrails overlapped). | Slow onboarding in a one-day hackathon. | Brief = what/why (1 read), guardrails = rules + checklists, data guide = how to use the data. |
| B8 | "Offline" ambiguity — could teams use the web? | Unequal playing field. | Stated plainly: everything needed is local; web optional; URLs are attribution. |

## 3. What the dataset deliberately does NOT add

- **No answer key**: no scores, weights, ranked topics or "correct" statuses.
- **No invented numbers**: every figure comes from a cited public source with its observation period.
  Search-snippet observations are marked `review_method=search_result_summary`.
- **No fictional FACTS history**: learnings are public external records; FACTS-internal project history is not part of the dataset.
- **No provider master lists**: populations are counts, not lists of names.

## 4. Known limitations of the data

- Research was done on 2026-11-09 by AI-assisted desk research with web search. A large share of figures come from search
  snippets or secondary reporting of primary statistics, not full-document review. Treat each number as "what the cited
  source reports for that period".
- Some figures differ by definition between sources (e.g. car-sharing totals, NIS2 entity counts); notes say so.
- Coverage is uneven: health, care, housing/energy, finance, work and mobility are deep; dental, physiotherapy and
  veterinary are thinner.
- Legal and medical source summaries are research context, not legal or medical advice.
- Organisers should spot-check high-impact figures before external publication of any result.
