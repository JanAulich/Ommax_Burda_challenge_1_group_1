# Evaluation principles & guardrails

This document tells you **what your prototype must respect**. It does not give you a scoring model — designing one is
part of the challenge.

---

## 1. The decision you support

> Which potential new TOP-List topics are relevant, differentiated and promising enough to investigate further — and why?

Your system recommends one of four statuses. It never makes the final decision.

| Status | Use it when… | Typical trigger (examples, not rules) |
|---|---|---|
| **Validate Next** | Evidence and potential justify a feasibility study now | Clear consumer problem, dated drivers, directory/award-dominated market, listable entity universe, acceptable risk |
| **Monitor** | Interesting, but evidence, timing or maturity is insufficient | Key regulation still upcoming; no population figure; only unverified signals |
| **Deprioritise** | Limited relevance, differentiation or fit right now | Well-served market; near-duplicate of an existing FACTS list |
| **Do Not Pursue** | Substantial risks or missing prerequisites | Vulnerable target group where a paid seal undermines trust; legal barrier; precedent shows the model fails |

---

## 2. The six mandatory dimensions

For each: what to ask, and which data helps.

| Dimension | Key questions | Most useful data |
|---|---|---|
| **A. Consumer relevance** | Does it affect health, money, housing, career, family? Is the decision expensive, emotional, hard to reverse? How many people face it? | `00_topic_taxonomy.ymyl_default`, signals of type `consumer_need`/`cost_pressure`, indicators counting affected people |
| **B. Timing & dynamics** | What changed recently or will change soon? Why does that create a *need for orientation* (not just a trend)? | `05_market_indicators` time series, `07_regulatory_events` (dates!), recent source-backed signals |
| **C. Competitive white space** | Who already helps the consumer? How good, national, transparent are they? | `04_competitors` attributes: `has_quality_assessment`, `coverage`, `methodology_public`, `provider_pays` |
| **D. Portfolio fit & learnings** | Covered already? Logical extension? Cannibalisation? Similar failures? | `01_portfolio`, `02_learnings` |
| **E. Commercial potential** | Who could be assessed and would value a seal? How many exist? Can you list them? Do they already pay for visibility? | `06_entity_populations` (count + master-list source), competitors with `provider_pays=yes_*` |
| **F. Risk & uncertainty** | Legal/professional rules, reputation, data, methodology, pay-to-play, vulnerable users | `02_learnings`, risks in `09_opportunity_spaces`, YMYL flag |

### Market types for dimension C
1. **Well served** — trusted, comprehensive, easy-to-use offers exist.
2. **Fragmented** — information exists but is scattered (often regional).
3. **Directory-dominated** — you can *find* providers, but get little guidance on quality or fit.
4. **Award-dominated** — providers can *buy or win* visibility, but consumers lack transparent orientation.
5. **Potential FACTS white space** — a credible FACTS list could be clearer, more transparent or more useful.

### Commercial-potential labels (dimension E)
`evidenced` · `plausible_but_unvalidated` · `unclear` · `unlikely`.
**With this dataset `evidenced` is practically unreachable** — there is no seal-buyer survey or revenue data. A large
entity population plus providers already paying for visibility elsewhere supports *plausible_but_unvalidated*, nothing more.

---

## 3. Evidence rules

| Rule | What it means in practice |
|---|---|
| **Cite IDs** | `F001`, `S101`, `C006`, `I0042`, `P007`, `R012`, `L004`, `SRC045`, `M003`. Never invent IDs. |
| **Respect evidence labels** | `source_backed_summary` = a source supports the stated observation. `curated_unverified` (original organiser assertions) and `derived_hypothesis` (broad hypotheses) are context, not proof. |
| **Keep periods** | A 2023 statistic is a 2023 statistic, even if read in 2026. Quote `period`. |
| **Count publishers, not rows** | One study cited in a signal, a competitor and a context is still **one** source. Use `source_ids` → `08_sources.publisher`. |
| **Empty ≠ zero** | An empty cell means *unknown / not supplied*, never "none", "false" or "low risk". |
| **Register ≠ quality** | An official register proves existence/admission, not quality. |
| **Gap = hypothesis** | Every `gap_hypothesis` in competitors is a hypothesis to test, not a proven market gap. |

### Fact vs. hypothesis vs. risk vs. open question

| Type | Definition | Example |
|---|---|---|
| Fact | Directly supported by a record | "5.69 m people were in need of care in Germany at end-2023 `[I00xx]`" |
| Hypothesis | Plausible, unproven | "Ambulatory care services may value a regional quality seal." |
| Risk | Possible barrier | "Provider universe may be too fragmented for a complete master list." |
| Open question | Needed before a decision | "Can the Pflegekassen data seed a complete list of ~15,000 services?" |

---

## 4. Human-in-the-loop — when review is mandatory

Flag **human review = Yes** and state the reason whenever:

- the topic is **YMYL** (health, finance, legal, other high-impact decisions);
- evidence is **contradictory, incomplete, outdated** or mostly `curated_unverified`;
- the topic **substantially overlaps** an existing FACTS product;
- a **similar precedent** (`L…`) shows legal, reputational or methodological failure;
- **legal, regulatory or reputational** risks are visible (e.g. professional advertising rules);
- **data availability or master-list feasibility** is unclear;
- the **commercial case relies mainly on assumptions**;
- the target group is **vulnerable** (debt, children, end of life, dementia) and a paid seal could look like pay-to-play.

---

## 5. Example card

> Illustrative format only — not an answer key. IDs below are examples of the citation style.

**TOP providers for age-appropriate bathroom & home conversions** — *Validate Next* · human review: **Yes**

| Field | Example content |
|---|---|
| Consumer problem | Older homeowners and relatives cannot tell which local firms reliably plan and execute barrier-free conversions. |
| Target user | Homeowners 65+, relatives, people with a new Pflegegrad |
| Target entity | Craft businesses (SHK, carpenters, builders) doing barrier-free conversions; housing-advice centres as partners |
| Why now? | Rising number of people in need of care `[I…]`; KfW funding programme status `[R…]`; Pflegekasse grant for home improvements `[R…]` |
| Portfolio fit | Adjacent to TOP Pflegeheime `F001` (same families, same moment of need) — no direct overlap |
| Competitive situation | Housing-advice network `C007` (advice, not firms), lead marketplaces `C…` (no transparent quality) → directory-dominated |
| Facts | X Handwerk businesses in the relevant trades `[P…]`; KfW programme facts `[R…]` |
| Hypotheses | Firms would license a seal for trust with older customers; a referral-based methodology is feasible |
| Risks | Fragmented, regional provider universe (data); safety-relevant work (liability); pay-to-play perception with older buyers (reputational) `[L…]` |
| Historical learning | Public precedent on seal advertising `[L…]` |
| Next questions | Which register (Handwerksrolle?) seeds a master list? What quality data exists? Would Pflegekassen/advice centres cooperate? |

---

## 6. Out of scope (but name it as a next step)

Final methodology, entity-level scoring, a final ranking, a complete master list, data collection, market sizing,
seal pricing, Salesforce integration, publication content. Your tool should flag when these become the critical next
question.

## 7. Jury criteria

| Criterion | Weight | What the jury looks for |
|---|---:|---|
| Business relevance for FACTS | 30 % | Topics FACTS could plausibly build and sell; realistic seal logic; respects the portfolio |
| Quality and clarity of opportunity logic | 25 % | Specific topics, explicit criteria, honest statuses including "no" |
| Evidence, trust, explainability | 20 % | Every claim traceable; facts vs. hypotheses; risks visible; human review explained |
| Technical quality and feasibility | 15 % | Reproducible, robust, no hallucinated evidence, runs on the supplied data |
| User experience and demo | 10 % | A FACTS expert can use it and challenge it |
