# FACTS Topic Opportunity Scout — Scoring Formulas, Math & Tuning Guide

This document is your reference manual for how scores, gates, and statuses are computed in `src/scorer.py`. You can adjust any weights, baselines, or thresholds in `src/scorer.py` and immediately test the impact on all 32 taxonomy sectors.

---

## 1. Executive Summary of the Math Model

Every topic is evaluated across **6 Core Dimensions** on a scale from **0.0 to 5.0**:
- **$CR$ (Consumer Relevance)** — Weight: `15%` (`0.15`)
- **$TD$ (Timing & Market Dynamics)** — Weight: `15%` (`0.15`)
- **$WS$ (Competitive White Space)** — Weight: `20%` (`0.20`)
- **$PF$ (Portfolio Fit & Cannibalisation)** — Weight: `10%` (`0.10`)
- **$CP$ (Commercial Potential)** — Weight: `15%` (`0.15`)
- **$Risk$ (Risk & Safety Governance)** — Weight: `25%` (`0.25`)

### The Master Composite Formula:
$$\text{Overall Score} = (CR \times 0.15) + (TD \times 0.15) + (WS \times 0.20) + (PF \times 0.10) + (CP \times 0.15) + (Risk \times 0.25)$$

---

## 2. Dimension 1: Consumer Relevance ($CR$)

### Why is the Base Score 2.0?
- **Domain Reality:** Every single topic in `00_topic_taxonomy.csv` (e.g. Heat Pumps, Elder Care, Veterinary, Childcare) was pre-selected by Burda and TUM as an active consumer sector in Germany. There are no trivial topics (like "paperclips" or "shoelaces") in the database.
- **Scale Calibration:** On a 0.0 to 5.0 scale, `2.0` represents a *"Moderate, everyday consumer decision"*.
- **Additive Logic:**
  - High-impact YMYL domains (health/finance/legal) add $+1.0$ or $+1.5$.
  - Specific verified consumer need / cost pressure signals add up to $+1.5$.
  - Result: Routine topics score around $2.0 - 2.5$, while life-altering health/energy/care topics reach $4.5 - 5.0$.

### The Exact Formula:
$$CR = \min\Big(5.0,\; 2.0 + \text{YMYL\_Bonus} + \min(1.5,\; N_{\text{consumer\_signals}} \times 0.4)\Big)$$

| Factor | Condition in Data | Points Added |
|---|---|---|
| **Baseline** | Every topic in taxonomy | `+2.0` |
| **YMYL Status** | `ymyl_default == 'yes'` (Health, Finance, Legal) | `+1.5` |
| | `ymyl_default == 'partial'` (Housing, Pets, Education) | `+1.0` |
| | `ymyl_default == 'no'` | `+0.0` |
| **Consumer Signals** | Signal in `03_signals.csv` with `signal_type` in `['consumer_need', 'cost_pressure', 'trend']` | `+0.4` per signal (max `+1.5`) |

---

## 3. Dimension 2: Timing & Why Now ($TD$)

Measures regulatory catalysts, deadlines, and recent market growth.

### The Exact Formula:
$$TD = \min\Big(5.0,\; 1.0 + \min(2.0,\; N_{\text{upcoming}} \times 0.8 + N_{\text{past}} \times 0.3) + \min(1.5,\; N_{\text{source\_signals}} \times 0.3) + \text{Indicator\_Bonus}\Big)$$

| Factor | Condition in Data | Points Added |
|---|---|---|
| **Baseline** | Any topic | `+1.0` |
| **Upcoming Events** | Event in `07_regulatory_events.csv` with `timing == 'upcoming'` | `+0.8` per event |
| **Past Events** | Event in `07_regulatory_events.csv` with `timing == 'past'` | `+0.3` per event (events capped at `+2.0`) |
| **Source Signals** | Signal in `03_signals.csv` with `evidence_status == 'source_backed_summary'` | `+0.3` per signal (capped at `+1.5`) |
| **Hard Statistics** | At least one numeric series in `05_market_indicators.csv` | `+0.5` |

---

## 4. Dimension 3: Competitive White Space ($WS$) & Market Type

Measures whether consumers are currently underserved.

We inspect all competitors in `04_competitors.csv`:
- `quality_like`: Competitors with `has_quality_assessment == 'yes'`
- `directory_like`: Competitors with `has_quality_assessment in ['no', 'partial', 'unknown']`
- `paid_visibility`: Competitors where `provider_pays` starts with `'yes'`

### Decision Tree & Score:
1. **Well served (Score: 2.0):** If `quality_like >= 3` and `directory_like <= 1`.
   *(Consumers already have Stiftung Warentest or dominant media rankings. Burda would face entrenched competition).*
2. **Directory-dominated (Score: 4.2):** If `directory_like >= 2`.
   *(Consumers only have yellow pages, lead brokers, or simple lists with no quality vetting. Huge white space for FOCUS).*
3. **Award-dominated (Score: 3.8):** If `paid_visibility >= 2`.
   *(Providers are already paying for badges, but consumers lack transparent methodology).*
4. **Fragmented (Score: 3.5):** If 0 competitors are listed.
5. **Potential White Space (Score: 4.0):** Default for underserved sectors.

---

## 5. Dimension 4: Portfolio Fit ($PF$)

Checks `01_portfolio.csv` to reward brand expansion while penalizing cannibalization.

| Condition in `01_portfolio.csv` | Portfolio Fit Score | Strategic Rationale |
|---|---|---|
| $\ge 2$ active products on same topic | `2.5` | High cannibalization risk; FOCUS already covers this heavily. |
| $1$ active product on same topic | `3.8` | Logical adjacent extension (e.g. Care Homes $\rightarrow$ Home Conversion). |
| $0$ active products on topic | `4.5` | Fresh, uncontested white space for Hubert Burda Media. |

---

## 6. Dimension 5: Commercial Potential ($CP$)

Measures whether there is a large, listable pool of businesses willing to buy a seal.

### The Exact Formula:
$$CP = \min\Big(5.0,\; 1.5 + \text{Population\_Bonus} + \text{Register\_Bonus} + \text{Paid\_Proof}\Big)$$

| Factor | Condition in Data | Points Added |
|---|---|---|
| **Baseline** | Any topic | `+1.5` |
| **Entity Population (`06_entity_populations.csv`)** | $\ge 10,000$ entities (e.g. Handwerk, doctors) | `+2.0` |
| | $\ge 1,000$ entities | `+1.2` |
| | $> 0$ entities | `+0.5` |
| **Master List Availability** | `master_list_availability` in `['public_register', 'chamber_directory']` | `+1.0` |
| **Paid Market Proof** | Any competitor in `04_competitors.csv` has `provider_pays == yes_*` | `+0.5` |

### Commercial Potential Label:
- If entities $\ge 1,000$ OR paid competitors exist $\rightarrow$ `plausible_but_unvalidated`
- If entities $< 100$ $\rightarrow$ `unlikely`
- Otherwise $\rightarrow$ `unclear`
*(Note: As required by the judges, `evidenced` is NEVER produced because the dataset contains no seal-buyer survey).*

---

## 7. Dimension 6: Risk & Safety Governance ($Risk$)

*In this dimension, a HIGHER score means SAFER / LESS RISK. A LOWER score means DANGEROUS.*

### Starting Score: `4.0` (Clean Baseline)

| Risk Factor | Condition in Data | Penalty | Trigger |
|---|---|---|---|
| **YMYL Impact** | `ymyl_default == 'yes'` | `-1.0` | Triggers Human-in-the-Loop review |
| **Negative Precedent** | Precedent in `02_learnings.csv` applies | `-1.5` | Triggers Human-in-the-Loop review |
| **Acutely Vulnerable Group** | Topic is `end_of_life` or `debt_and_credit` | `-2.0` | Severe public backlash trigger |
| **Direct Overlap** | Active product in `01_portfolio.csv` | `0.0` | Triggers Human Review for cannibalization |
| **No Population Data** | No count in `06_entity_populations.csv` | `-0.5` | Data feasibility flag |

*Score is clamped between `1.0` and `5.0`.*

---

## 8. Status Decision Waterfall (Evaluated in Order)

```
1. DO NOT PURSUE
   Is topic == 'end_of_life' OR (learnings exist AND YMYL == 'yes' AND Risk <= 1.5)?
   ──► YES: Output DO NOT PURSUE

2. DEPRIORITISE
   Is Market Type == 'Well served' OR (>= 2 overlapping products AND White Space <= 2.5)?
   ──► YES: Output DEPRIORITISE

3. MONITOR
   Is maximum entity count < 200 OR (upcoming events exist but source signals <= 1)?
   ──► YES: Output MONITOR

4. VALIDATE NEXT
   Is White Space >= 3.5 AND Timing >= 2.5 AND Commercial >= 3.0 AND Risk >= 2.2?
   (Or Overall Score >= 3.4 AND Risk >= 2.2)
   ──► YES: Output VALIDATE NEXT

5. FALLBACK
   ──► Default to MONITOR
```

---

## 9. How to Tune and Test Different Values

To test different weights or thresholds:
1. Open [`src/scorer.py`](file:///Users/prashantjoshi/Desktop/Projects-Nidhi/Hackathon-OMMAX-x-Burda/Challenge%201:%20FACTS%20Topic%20Opportunity%20Scout/src/scorer.py).
2. Modify any number (for example, change the baseline in line 35 from `2.0` to `1.5`, or change the weights in line 140).
3. Re-run:
   ```bash
   .venv/bin/python3 Challenge\ 1\:\ FACTS\ Topic\ Opportunity\ Scout/generate_deliverables.py
   ```
4. The script will instantly print the new recommendations and update `cards.json` and `cards.md`!
