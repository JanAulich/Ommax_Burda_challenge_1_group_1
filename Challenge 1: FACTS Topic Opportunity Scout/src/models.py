"""
Pydantic data models for Opportunity Cards and evaluation scoring.
Strictly enforces field schemas, enums, and valid record ID formats.
"""

from enum import Enum
from typing import List, Optional
import re
from pydantic import BaseModel, Field, field_validator

class OpportunityStatus(str, Enum):
    VALIDATE_NEXT = "Validate Next"
    MONITOR = "Monitor"
    DEPRIORITISE = "Deprioritise"
    DO_NOT_PURSUE = "Do Not Pursue"

class CommercialPotentialLabel(str, Enum):
    EVIDENCED = "evidenced"
    PLAUSIBLE_BUT_UNVALIDATED = "plausible_but_unvalidated"
    UNCLEAR = "unclear"
    UNLIKELY = "unlikely"

class MarketTypeLabel(str, Enum):
    WELL_SERVED = "Well served"
    FRAGMENTED = "Fragmented"
    DIRECTORY_DOMINATED = "Directory-dominated"
    AWARD_DOMINATED = "Award-dominated"
    POTENTIAL_WHITE_SPACE = "Potential FACTS white space"

class DimensionScores(BaseModel):
    consumer_relevance: float = Field(..., ge=0.0, le=5.0, description="1. Consumer relevance (health, money, home, career, family)")
    timing_dynamics: float = Field(..., ge=0.0, le=5.0, description="2. Timing & market dynamics (why now drivers, indicators, regulations)")
    competitive_white_space: float = Field(..., ge=0.0, le=5.0, description="3. Competitive white space (directory vs quality)")
    portfolio_fit: float = Field(..., ge=0.0, le=5.0, description="4. Portfolio fit & learnings (adjacent expansion vs cannibalisation)")
    commercial_potential: float = Field(..., ge=0.0, le=5.0, description="5. Initial commercial potential (entity population & willingness to pay)")
    risk_uncertainty: float = Field(..., ge=0.0, le=5.0, description="6. Risk & uncertainty (reputational, legal, pay-to-play, YMYL)")

class OpportunityCard(BaseModel):
    proposed_topic: str = Field(..., description="Specific, understandable title")
    topic_key: str = Field(..., description="Taxonomy topic key")
    consumer_problem: str = Field(..., description="The decision or uncertainty it resolves")
    target_user: str = Field(..., description="Who needs orientation")
    target_entity: str = Field(..., description="Which organisations/professionals would later be assessed")
    why_now: str = Field(..., description="Dated drivers with cited record IDs")
    portfolio_fit: str = Field(..., description="Relation to current FACTS products")
    competitive_situation: str = Field(..., description="Existing offers and white space")
    evidence: List[str] = Field(default_factory=list, description="All record IDs cited")
    facts: List[str] = Field(..., description="Strictly evidenced facts citing IDs")
    hypotheses: List[str] = Field(..., description="Unverified hypotheses")
    risks_and_uncertainties: List[str] = Field(..., description="Legal, reputational, data, market, competition risks")
    historical_learning: str = Field(..., description="Relevant public precedents (L...) or none found")
    next_validation_questions: List[str] = Field(..., description="What FACTS must check next")
    recommended_status: OpportunityStatus = Field(..., description="Validate Next / Monitor / Deprioritise / Do Not Pursue")
    human_review_required: bool = Field(..., description="Human in the loop required flag")
    human_review_reasons: List[str] = Field(default_factory=list, description="Explicit reasons for human review")
    commercial_potential_label: CommercialPotentialLabel = Field(
        default=CommercialPotentialLabel.PLAUSIBLE_BUT_UNVALIDATED,
        description="Commercial potential rating"
    )
    market_type: MarketTypeLabel = Field(
        default=MarketTypeLabel.POTENTIAL_WHITE_SPACE,
        description="Market landscape type"
    )
    scores: DimensionScores = Field(..., description="Scores for the 6 mandatory dimensions")
    overall_score: float = Field(..., ge=0.0, le=5.0, description="Weighted composite score")

    @field_validator("evidence")
    @classmethod
    def validate_record_ids(cls, ids: List[str]) -> List[str]:
        pattern = re.compile(r"^[A-Z]{1,3}\d{3,4}$")
        for rec_id in ids:
            if not pattern.match(rec_id):
                raise ValueError(f"Invalid record ID format: '{rec_id}'. Must match pattern ^[A-Z]{{1,3}}\\d{{3,4}}$")
        return ids

