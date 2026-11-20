"""
Script to generate the official hackathon deliverables:
- cards.json (machine readable)
- cards.md (executive report)
- LOGIC.md (1-page methodology explanation)
"""

import json
import os
import sys

# Add challenge root to path
CHALLENGE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CHALLENGE_DIR)

from src.data_loader import DataLoader
from src.generator import CardGenerator

def main():
    data_dir = os.path.join(CHALLENGE_DIR, "data")
    loader = DataLoader(data_dir)
    generator = CardGenerator(loader)

    # 4 showcase topics spanning Validate Next, Monitor, and Do Not Pursue
    showcase_keys = [
        "home_adaptation",
        "heat_pumps",
        "digital_health",
        "end_of_life",
    ]

    cards = []
    for tk in showcase_keys:
        card = generator.generate_card(tk)
        cards.append(card)
        print(f"[{card.recommended_status.value}] {card.proposed_topic} (Score: {card.overall_score}/5.0) | Human Review: {card.human_review_required}")

    # 1. Export cards.json
    json_path = os.path.join(CHALLENGE_DIR, "cards.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump([c.model_dump() for c in cards], f, indent=2, ensure_ascii=False)
    print(f"Exported {json_path}")

    # 2. Export cards.md
    md_path = os.path.join(CHALLENGE_DIR, "cards.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# FACTS Topic Opportunity Scout — Opportunity Cards\n\n")
        f.write("**TUM × OMMAX AI Hackathon · Hubert Burda Media / FACTS**\n\n---\n\n")
        for c in cards:
            status_badge = f"**`{c.recommended_status.value.upper()}`**"
            review_badge = "⚠️ **YES**" if c.human_review_required else "✅ NO"
            f.write(f"## {c.proposed_topic}\n\n")
            f.write(f"- **Recommended Status:** {status_badge}\n")
            f.write(f"- **Overall Score:** `{c.overall_score} / 5.0`\n")
            f.write(f"- **Human-in-the-Loop Review:** {review_badge}\n")
            if c.human_review_reasons:
                for r in c.human_review_reasons:
                    f.write(f"  - 🔴 {r}\n")
            f.write("\n| Mandatory Field | Strategic Assessment & Evidenced Claims |\n")
            f.write("|---|---|\n")
            f.write(f"| **Proposed TOP-List Topic** | {c.proposed_topic} |\n")
            f.write(f"| **Consumer Problem** | {c.consumer_problem} |\n")
            f.write(f"| **Target User** | {c.target_user} |\n")
            f.write(f"| **Potential Target Entity** | {c.target_entity} |\n")
            f.write(f"| **Why Now?** | {c.why_now} |\n")
            f.write(f"| **Portfolio Fit** | {c.portfolio_fit} |\n")
            f.write(f"| **Competitive Situation** | {c.competitive_situation} |\n")
            f.write(f"| **Facts (Evidenced)** | " + "<br>".join([f"• {fact}" for fact in c.facts]) + " |\n")
            f.write(f"| **Hypotheses (Unverified)** | " + "<br>".join([f"• {hyp}" for hyp in c.hypotheses]) + " |\n")
            f.write(f"| **Risks & Uncertainties** | " + "<br>".join([f"• {rk}" for rk in c.risks_and_uncertainties]) + " |\n")
            f.write(f"| **Historical Learning** | {c.historical_learning} |\n")
            f.write(f"| **Next Validation Questions** | " + "<br>".join([f"• {q}" for q in c.next_validation_questions]) + " |\n")
            f.write(f"| **Evidence Record IDs** | {', '.join(c.evidence)} |\n")
            f.write("\n---\n\n")
    print(f"Exported {md_path}")

    # 3. Export LOGIC.md
    logic_path = os.path.join(CHALLENGE_DIR, "LOGIC.md")
    with open(logic_path, "w", encoding="utf-8") as f:
        f.write("""# FACTS Topic Opportunity Scout — Prioritisation & Decision Logic (LOGIC.md)

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
- Pydantic models validate regex pattern `^[A-Z]{1,3}\\d{3,4}$` on every cited ID.
- Hypotheses vs. Facts are strictly segregated: commercial willingness to pay remains an unverified hypothesis.
""")
    print(f"Exported {logic_path}")

if __name__ == "__main__":
    main()

