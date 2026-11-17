# Challenge 1 — FACTS Topic Opportunity Scout

**TUM × OMMAX AI Hackathon · Client: FACTS / Hubert Burda Media · One-day AI engineering challenge · Teams of 3–5**

> **In one sentence:** build an AI prototype that reads the supplied dataset and recommends **3–5 specific new
> TOP-List topics** FACTS should investigate next, explaining for each one *why*, *with which evidence*, *what could go
> wrong* and *what to validate next*.

---

## 1. Who FACTS is and what a "TOP List" is

FACTS builds **data-based consumer-orientation products** for FOCUS media brands (FOCUS Gesundheit, FOCUS Business,
FOCUS Money, Deutschland Test, FOCUS Mobility). Typical products:

| Product type | Example | Who pays? |
|---|---|---|
| TOP List / recommendation list | FOCUS-Gesundheit Ärzteliste (doctors), TOP Kliniken, TOP Pflegeheime | Readers (magazine / digital reach) |
| Quality seal | "TOP Arbeitgeber Mittelstand" logo used by a listed company in its own marketing | The listed organisation (licence fee) |
| Test / ranking | Krankenkassentest, Baufinanzierer | Readers; partly seal licences |

A good FACTS product combines **a real consumer question**, **a transparent methodology**, **reliable data**, an
**understandable result**, **editorial reach** and — where appropriate — **a seal that recognised organisations can
license**. That last point is the commercial engine, and also the main reputational risk (see learnings `L…` in the data).

## 2. The problem you solve

Before FACTS invests in data collection and methodology, someone must answer:

> **Which new topic is relevant enough, differentiated enough and promising enough to investigate further?**

Today this is done by experience and manual research. Signals are scattered, previous projects are not checked
systematically, and topics that look attractive often fail later because of competition, legal risk, an incomplete
provider list or weak willingness to pay.

**The goal is not many ideas. It is a few well-reasoned ones — and clear "no"s.**

### Reference example: TOP Pflegeheime (nursing homes)
1. *Growing relevance* — Germany ages; more families must choose a care home (see `I…` care statistics, `S101`).
2. *Orientation gap* — directories and official quality data exist (`C006`, `S108`), but not a clear, consumer-friendly,
   transparent recommendation.
3. *Credible FACTS role* — health-list experience, FOCUS Gesundheit reach, a seal proposition for operators.

## 3. What your prototype must do

| # | Capability | What "good" looks like |
|---|---|---|
| A | **Understand the portfolio** | Detects topics already covered (`01_portfolio.csv`), adjacent extensions and cannibalisation risk |
| B | **Detect external signals** | Uses signals, numeric indicator time series and regulatory events to explain *why now* |
| C | **Judge competitive white space** | Distinguishes well-served, fragmented, directory-dominated and award-dominated markets — competitors ≠ automatic rejection |
| D | **Create specific opportunity hypotheses** | "TOP providers for age-appropriate bathroom conversions", not "housing" |
| E | **Separate facts / hypotheses / risks / open questions** | Every fact cites a record ID; market size and seal demand stay hypotheses unless proven |
| F | **Recommend a status — and keep the human in charge** | One of *Validate Next / Monitor / Deprioritise / Do Not Pursue*, plus an explicit human-review flag with reasons |

## 4. Users

| User | Needs from your tool |
|---|---|
| Product & Portfolio team | A structured, ranked pipeline of candidate topics |
| Research & Methodology | Evidence, sources, data feasibility, open validation questions |
| Commercial / Sales | A first view of who could license a seal and why |
| Editorial | Consumer relevance and content potential |
| Management | A transparent basis for deciding what to explore next |

## 5. Deliverable

A working prototype or clickable demo that outputs **3–5 opportunity cards**. Each card contains:

| Field | Content |
|---|---|
| Proposed TOP-List topic | Specific, understandable title |
| Consumer problem | The decision or uncertainty it resolves |
| Target user | Who needs orientation |
| Potential target entity | Which organisations/professionals would later be assessed (and roughly how many — `P…`) |
| Why now? | Dated drivers — trends (`I…`), events (`R…`), signals (`S…`) |
| Portfolio fit | Relation to current FACTS products (`F…`) |
| Competitive situation | Existing offers (`C…`) and the possible white space |
| Evidence | The record IDs used |
| Facts / Hypotheses | Strictly separated |
| Risks & uncertainties | Legal, reputational, data, market, competition — shown separately, not hidden in a score |
| Historical learning | Relevant public precedents (`L…`), or an explicit note that none was found |
| Next validation questions | What FACTS must check next (master list? data? seal-buyer interest? law?) |
| Recommended status | Validate Next / Monitor / Deprioritise / Do Not Pursue |
| Human review required? | Yes/No with the reason(s) |

A full worked example is in [02_evaluation_and_guardrails.md](02_evaluation_and_guardrails.md#5-example-card).
**What exactly to hand in, the demo format and the scoring rubric:** [05_deliverables_and_judging.md](05_deliverables_and_judging.md).

## 6. Scoring logic — your design

FACTS deliberately gives **no** scoring framework. You must cover these six dimensions and explain your rules:

1. **Consumer relevance** — does it affect health, money, home, career or family decisions?
2. **Timing & market dynamics** — demographic, regulatory, economic, technological drivers (and *why they create an orientation need*).
3. **Competitive white space** — is there a meaningful gap existing offers don't close?
4. **Portfolio fit & prior learnings** — strategic fit, overlap, similar past cases.
5. **Initial commercial potential** — is there a large, listable group of organisations that would value visibility or a seal? (label: *evidenced / plausible but unvalidated / unclear / unlikely*)
6. **Risk & uncertainty** — legal, reputational, data, methodology, pay-to-play.

You decide sub-criteria, weights or rules, how missing evidence is treated, how risk changes the result, and when a
human must review.

## 7. Guardrails (mandatory)

1. **Evidence first** — every recommendation links to dataset records.
2. **No black box** — a user can see why a topic was proposed, which criteria were positive/negative, what is missing.
3. **Facts ≠ hypotheses** — never present market size, data availability or willingness to buy as fact without evidence.
4. **Historical learnings visible** — show relevant public precedents.
5. **Human-in-the-loop** — flag cases for expert review, with reasons.
6. **Careful with YMYL** — health, finance, legal and other high-impact topics need extra transparency.

Details and checklists: [02_evaluation_and_guardrails.md](02_evaluation_and_guardrails.md).

## 8. Out of scope

You do **not** need: a final list methodology, entity-level scoring, a final ranking of providers, a market-sizing
model, a master list, a data-collection pipeline, seal pricing or a Salesforce integration. But your tool should
**say when these are the next questions** ("Can FACTS build a complete master list of ~X entities from register Y?").

## 9. Data

Everything you need is in [`../data/`](../data/) — **no crawling, scraping or web access is required**. Source URLs
are attribution only. See [03_data_guide.md](03_data_guide.md) for the data model and
[04_dataset_design_and_limitations.md](04_dataset_design_and_limitations.md) for the design choices behind the data and its known limits.

| File | What it gives you |
|---|---|
| `00_topic_taxonomy.csv` | The topic keys that join everything, with YMYL flag |
| `01_portfolio.csv` | 36 FACTS products (current / to validate), in English, with public footprint |
| `02_learnings.csv` | Real, public precedents (court rulings, reforms, discontinued services, criticism) |
| `03_signals.csv` | Qualitative + quantitative "why now" observations |
| `04_competitors.csv` | Rankings, seals, portals, registers, directories with structured attributes |
| `05_market_indicators.csv` | Numeric time series (demand, supply, cost, adoption) |
| `06_entity_populations.csv` | How many entities exist per segment and where a master list could come from |
| `07_regulatory_events.csv` | Laws, deadlines, rulings with dates |
| `08_sources.csv` | Every source with publisher, period, review method and limitations |
| `09_opportunity_spaces.csv` | Curated research starting points (not answers, not ranked) |

## 10. How you are judged

| Category | Weight | Criteria (weights) |
|---|---:|---|
| 1. Business relevance | 34 % | Topic specificity (8), consumer need (8), FACTS & portfolio fit (10), commercial potential (8) |
| 2. Opportunity logic | 22 % | Why now (8), competitive white space (9), status recommendation (5) |
| 3. Evidence, trust & explainability | 20 % | Evidence & sources (10), facts vs. hypotheses (6), risk & precedent check (4) |
| 4. Technical quality | 15 % | Traceable logic (5), robustness & data validation (5), generalisability (5) |
| 5. User experience & pitch | 9 % | Clarity of opportunity cards (5), demo & pitch quality (4) |

The full 15-criterion scoring sheet with guiding questions, pass/fail gates and the tie-break are in [05_deliverables_and_judging.md](05_deliverables_and_judging.md#5-judging-rubric).

## 11. Definition of done

- [ ] Uses portfolio, signals, competitors **and** at least two of: indicators, populations, events, learnings
- [ ] Produces ≥ 3 concrete opportunity cards with all fields
- [ ] Every fact and why-now claim cites existing record IDs (no invented IDs or numbers)
- [ ] Shows at least one portfolio overlap and one competitor that weakens a white-space claim
- [ ] Separates facts, hypotheses, risks and open questions
- [ ] Recommends a status for each card — and is able to say "Deprioritise" / "Do Not Pursue"
- [ ] Flags human review with reasons (YMYL, overlap, precedents, weak evidence)
- [ ] States which topics should proceed to feasibility and what to validate first

## 12. What happens after the hackathon

The best topics enter FACTS' feasibility stage: data availability, master-list feasibility, target-group size,
seal-buyer interest and commercial viability. Your tool should hand over exactly those questions.

> **Final challenge statement:** Build an AI-powered FACTS Topic Opportunity Scout that turns portfolio knowledge,
> market signals and competitor information into transparent, evidence-based recommendations for the next
> generation of FACTS TOP Lists.
