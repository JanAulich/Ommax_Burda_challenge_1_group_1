# FACTS Topic Opportunity Scout — Prioritisation & Decision Logic (LOGIC.md)

## 1. Decision Engine Principles
The Opportunity Scout uses an audit-proof, deterministic relational evaluation engine rather than probabilistic vector search. Every claim is strictly grounded in dataset record IDs (`[F...]`, `[S...]`, `[I...]`, `[C...]`, `[P...]`, `[R...]`, `[L...]`, `[SRC...]`).

## 2. The Six Evaluation Dimensions & Weights
Total composite score is computed on a 0.0 to 5.0 scale using weights aligned with the OMMAX judging rubric:

| Dimension | Weight | Primary Data Sources & Evaluation Rules |
|---|---:|---|
| **1. Consumer Relevance** | 15% | `00_topic_taxonomy.ymyl_default`, `03_signals`. High impact on life, health, housing, or finance decisions. |
| **2. Timing & Market Dynamics** | 15% | `07_regulatory_events` (dated laws/deadlines), `05_market_indicators` (time-series), recent `03_signals`. Identifies *why an orientation need exists today*. |
| **3. Competitive White Space** | 20% | `04_competitors`. Differentiates directory-dominated / award-dominated markets from well-served markets. Directories with `has_quality_assessment=no` represent high opportunity white space. |
| **4. Portfolio Fit & Cannibalisation** | 10% | `01_portfolio`. Rewards natural adjacencies (e.g. Care Home List -> Home Adaptation) while penalising direct duplicates to avoid brand cannibalisation. |
| **5. Initial Commercial Potential** | 15% | `06_entity_populations`, `04_competitors.provider_pays`. Evaluates pool of potential seal licensees (>10k entities + chamber/public register availability = high score). Labeled as `plausible_but_unvalidated` unless revenue proof exists. |
| **6. Risk & Governance** | 25% | `02_learnings`, BGH court precedents, YMYL liability, and consumer vulnerability. Higher score indicates lower/manageable risk. |

## 3. Status Recommendation Rules
- **Validate Next:** High consumer need (CR >= 3.0), dated regulatory/market drivers (TD >= 2.5), directory-dominated white space (WS >= 3.5), sizable entity universe (CP >= 3.0), and manageable risk (Risk >= 2.5).
- **Monitor:** Promising emerging domain, but entity population is still small (< 200 entities) or key regulatory framework is still pending implementation.
- **Deprioritise:** Market is already well-served by trusted, transparent public comparison portals, or represents a near-duplicate of an existing FOCUS list.
- **Do Not Pursue:** High legal exposure (direct BGH court ruling on paid seal illegality `L...`) OR vulnerable consumer demographic (e.g. acute bereavement, consumer over-indebtedness) where a commercial seal risks public scandal.

## 4. Human-in-the-Loop Triggers
Human expert sign-off (`human_review_required = True`) is mandatory when:
1. Topic is classified as **YMYL** (Health, Legal, Financial decisions).
2. Negative legal precedent or court ruling exists in `02_learnings.csv`.
3. Direct overlap with an active FOCUS/FACTS product in `01_portfolio.csv`.
4. Target group is vulnerable (bereavement, debt, elderly dementia).
5. Target provider universe is fragmented with no centralized official register.

## 5. Pass/Fail Governance & Verification
- Pydantic models validate regex pattern `^[A-Z]{1,3}\d{3,4}$` on every cited ID.
- Hypotheses vs. Facts are strictly segregated: commercial willingness to pay remains an unverified hypothesis.
