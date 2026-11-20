"""
AI Gateway Client connecting to Tesseracted Labs Shared Gateway.
Uses OpenAI-compatible endpoints to power executive synthesis and live Q&A.
"""

import os
from typing import Dict, Any, Optional

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

GATEWAY_BASE_URL = "https://tesseracted.com/access_83444ac6-49d6-467b-a61f-0d39a98f0e87/ai_gateway/v1"
GATEWAY_API_KEY = "sk-adc87b823faeed543c2c5755130a44199e966c90b45f8228"

AVAILABLE_MODELS = [
    "deepseek-ai/DeepSeek-V4.1-Flash",
    "moonshotai/Kimi-K3.1-Pro",
    "zai-org/GLM-5.3-Flash",
    "google/gemma-4-31B-it",
    "Qwen/Qwen3.6-35B-A3B-FP8",
]

DEFAULT_MODEL = "deepseek-ai/DeepSeek-V4.1-Flash"

def get_client() -> Optional[Any]:
    if not HAS_OPENAI:
        return None
    return OpenAI(
        base_url=GATEWAY_BASE_URL,
        api_key=GATEWAY_API_KEY,
    )

def synthesize_executive_narrative(topic_label: str, card: Dict[str, Any], model: str = DEFAULT_MODEL) -> str:
    """Uses LLM to synthesize an executive presentation pitch strictly grounded in card evidence."""
    client = get_client()
    if not client:
        return "OpenAI library not found. Please install it in .venv."

    dossier_text = f"""
TOPIC: {topic_label} (Status: {card.get('recommended_status')}, Score: {card.get('overall_score')}/5.0)
CONSUMER PROBLEM: {card.get('consumer_problem')}
TARGET ENTITY: {card.get('target_entity')}
WHY NOW: {card.get('why_now')}
PORTFOLIO FIT: {card.get('portfolio_fit')}
COMPETITIVE SITUATION: {card.get('competitive_situation')}
EVIDENCED FACTS: {'; '.join(card.get('facts', []))}
HYPOTHESES: {'; '.join(card.get('hypotheses', []))}
RISKS & UNCERTAINTIES: {'; '.join(card.get('risks_and_uncertainties', []))}
HISTORICAL LEARNING: {card.get('historical_learning')}
CITED RECORD IDS: {', '.join(card.get('evidence', []))}
"""

    prompt = f"""You are a Managing Director at Hubert Burda Media leading the FACTS / FOCUS quality rankings division.
Provide a crisp, compelling 3-paragraph executive investment memo for executive leadership on whether to pursue: '{topic_label}'.

Mandatory Rules:
1. Every single fact, indicator, competitor, or court ruling cited MUST reference its exact record ID in brackets (e.g. [S101], [I0042], [C006], [L015]).
2. NEVER invent IDs or statistics that are not explicitly present in the dossier below.
3. If the status is 'Do Not Pursue' or 'Monitor', state clearly the legal, reputational, or data blockers that justify saying NO.
4. Keep the tone strategic, objective, and executive-ready.

DOSSIER:
{dossier_text}
"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=600,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Tesseracted AI Gateway response error: {str(e)}"

def ask_copilot_question(question: str, topic_label: str, card: Dict[str, Any], model: str = DEFAULT_MODEL) -> str:
    """Answers a live question from judges or executives about a topic using only verified dossier facts."""
    client = get_client()
    if not client:
        return "OpenAI library not found."

    context = f"""
TOPIC: {topic_label}
STATUS: {card.get('recommended_status')}
SCORE: {card.get('overall_score')}/5.0
HUMAN REVIEW REQUIRED: {card.get('human_review_required')} (Reasons: {card.get('human_review_reasons')})
FACTS: {card.get('facts')}
RISKS: {card.get('risks_and_uncertainties')}
LEARNING: {card.get('historical_learning')}
WHY NOW: {card.get('why_now')}
EVIDENCE IDS: {card.get('evidence')}
"""
    prompt = f"""You are the Lead Forward Deployed AI Engineer for the FACTS Topic Opportunity Scout.
Answer this question from an OMMAX consultant or Burda executive regarding the topic '{topic_label}'.

Question: "{question}"

Rules:
1. Base your answer strictly on the facts, risks, and precedents in the context below.
2. Cite exact record IDs where applicable (e.g. [L015], [C006], [I0042]).
3. Be concise, sharp, and transparent about what is a verified fact versus an unproven hypothesis.

Context:
{context}
"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=400,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Tesseracted AI Gateway error: {str(e)}"

