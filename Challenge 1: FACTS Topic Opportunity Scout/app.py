"""
FACTS Topic Opportunity Scout — Executive Cockpit
Interactive Streamlit Dashboard for Hubert Burda Media / OMMAX AI Hackathon.
"""

import os
import sys
import json
import streamlit as st
import pandas as pd

# Robust directory resolution
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(os.path.join(CURRENT_DIR, "data")):
    APP_DIR = CURRENT_DIR
else:
    APP_DIR = os.path.join(CURRENT_DIR, "Challenge 1: FACTS Topic Opportunity Scout")

sys.path.insert(0, APP_DIR)

from src.data_loader import DataLoader
from src.generator import CardGenerator
from src.models import OpportunityStatus
from src.ai_gateway import AVAILABLE_MODELS, synthesize_executive_narrative, ask_copilot_question

st.set_page_config(
    page_title="FACTS Topic Opportunity Scout | Hubert Burda Media",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_resource
def load_engine():
    data_dir = os.path.join(APP_DIR, "data")
    loader = DataLoader(data_dir)
    generator = CardGenerator(loader)
    return loader, generator

loader, generator = load_engine()

# Custom CSS styling for executive Burda aesthetic
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 16px;
        border-left: 5px solid #004085;
    }
    .badge-validate {
        background-color: #d4edda;
        color: #155724;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
    }
    .badge-monitor {
        background-color: #fff3cd;
        color: #856404;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
    }
    .badge-deprioritise {
        background-color: #e2e3e5;
        color: #383d41;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
    }
    .badge-kill {
        background-color: #f8d7da;
        color: #721c24;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
    }
    .evidence-tag {
        background-color: #e9ecef;
        padding: 2px 8px;
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.85em;
        margin-right: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Pre-calculate summary stats across all 32 taxonomy topics
all_topics = loader.get_all_topics()
all_cards = [generator.generate_card(t["topic_key"]) for t in all_topics]

count_validate = sum(1 for c in all_cards if c.recommended_status == OpportunityStatus.VALIDATE_NEXT)
count_monitor = sum(1 for c in all_cards if c.recommended_status == OpportunityStatus.MONITOR)
count_deprioritise = sum(1 for c in all_cards if c.recommended_status == OpportunityStatus.DEPRIORITISE)
count_kill = sum(1 for c in all_cards if c.recommended_status == OpportunityStatus.DO_NOT_PURSUE)

# Header
st.title("🧭 FACTS Topic Opportunity Scout")
st.caption("Hubert Burda Media · FOCUS Quality Seals & Editorial TOP-Lists Prioritisation Engine")

# KPI Summary Bar
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
with kpi1:
    st.metric("Total Taxonomies", len(all_topics))
with kpi2:
    st.metric("Validate Next", count_validate)
with kpi3:
    st.metric("Monitor", count_monitor)
with kpi4:
    st.metric("Deprioritise", count_deprioritise)
with kpi5:
    st.metric("Do Not Pursue", count_kill)

st.markdown("---")

# Sidebar Controls
st.sidebar.header("🎯 Topic Selector & Filters")
selected_ai_model = st.sidebar.selectbox("🤖 AI Model (Tesseracted Gateway):", AVAILABLE_MODELS, index=0)

# Live Jury Search / Fuzzy matcher
custom_query = st.sidebar.text_input("🔍 Live Jury Search (Type any topic/keyword):", placeholder="e.g. driving, vet, funeral, heat")

domains = sorted(list(set(t.get("domain", "") for t in all_topics if t.get("domain"))))
selected_domain = st.sidebar.selectbox("Filter by Domain:", ["All Domains"] + domains)

status_filter = st.sidebar.multiselect(
    "Filter by Status:",
    options=[s.value for s in OpportunityStatus],
    default=[s.value for s in OpportunityStatus]
)

# Filter topic keys
filtered_topics = []
for t in all_topics:
    tk = t["topic_key"]
    domain = t.get("domain", "")
    card = next(c for c in all_cards if c.topic_key == tk)
    
    if selected_domain != "All Domains" and domain != selected_domain:
        continue
    if card.recommended_status.value not in status_filter:
        continue
    if custom_query:
        q = custom_query.lower()
        search_blob = f"{tk} {t.get('label', '')} {t.get('description', '')}".lower()
        if q not in search_blob:
            continue
    filtered_topics.append(t)

if not filtered_topics:
    st.warning("No topics match your current filter criteria.")
    st.stop()

# Topic selector dropdown
topic_options = {t["topic_key"]: f"{t['topic_key']} — {t['label']} ({t.get('likely_facts_brand', '')})" for t in filtered_topics}
selected_key = st.sidebar.selectbox(
    "Select Topic Dossier:",
    options=list(topic_options.keys()),
    format_func=lambda x: topic_options[x]
)

# Showcase Shortcuts
st.sidebar.markdown("---")
st.sidebar.subheader("🌟 Showcase Demos (Quick Jump)")
col_s1, col_s2 = st.sidebar.columns(2)
with col_s1:
    if st.button("Heat Pumps (Pursue)"):
        selected_key = "heat_pumps"
with col_s2:
    if st.button("Funeral (Kill)"):
        selected_key = "end_of_life"

col_s3, col_s4 = st.sidebar.columns(2)
with col_s3:
    if st.button("Digital Health (Monitor)"):
        selected_key = "digital_health"
with col_s4:
    if st.button("Childcare (Pursue)"):
        selected_key = "childcare_schools"

# Generate card for selected topic
current_card = generator.generate_card(selected_key)
dossier = loader.get_topic_dossier(selected_key)

# Topic Selector Dropdown on Main View
main_topic_list = list(topic_options.keys())
current_idx = main_topic_list.index(selected_key) if selected_key in main_topic_list else 0
chosen_topic = st.selectbox(
    "📌 Select Taxonomy Topic to Inspect:",
    options=main_topic_list,
    index=current_idx,
    format_func=lambda x: topic_options[x],
    key="main_view_topic_selector"
)
if chosen_topic != selected_key:
    selected_key = chosen_topic
    current_card = generator.generate_card(selected_key)
    dossier = loader.get_topic_dossier(selected_key)

# Render Opportunity Card
st.subheader(f"📋 {current_card.proposed_topic}")

# Status Banner & Badges
bcol1, bcol2, bcol3 = st.columns([2, 1, 1])
with bcol1:
    st.markdown(f"**Domain:** `{dossier['taxonomy'].get('domain')}` | **Target Brand:** `{dossier['taxonomy'].get('likely_facts_brand')}` | **YMYL:** `{dossier['taxonomy'].get('ymyl_default').upper()}`")
with bcol2:
    status_val = current_card.recommended_status.value
    if status_val == "Validate Next":
        badge_html = f"<span class='badge-validate'>✅ {status_val.upper()}</span>"
    elif status_val == "Monitor":
        badge_html = f"<span class='badge-monitor'>⏳ {status_val.upper()}</span>"
    elif status_val == "Deprioritise":
        badge_html = f"<span class='badge-deprioritise'>⏸️ {status_val.upper()}</span>"
    else:
        badge_html = f"<span class='badge-kill'>🚫 {status_val.upper()}</span>"
    st.markdown(badge_html, unsafe_allow_html=True)
with bcol3:
    st.markdown(f"**Score:** `{current_card.overall_score} / 5.0`")

# Human Review Alert if required
if current_card.human_review_required:
    st.error("⚠️ **HUMAN-IN-THE-LOOP EXPERT REVIEW REQUIRED BEFORE FEASIBILITY STAGE**")
    for reason in current_card.human_review_reasons:
        st.markdown(f"- 🔴 **Trigger:** {reason}")

# 6-Dimension Score Breakdown Table / Chart
st.markdown("### 📊 Dimension Scores & Market Classification")
d1, d2, d3, d4, d5, d6 = st.columns(6)
d1.metric("Consumer Relevance", f"{current_card.scores.consumer_relevance}/5.0")
d2.metric("Timing & Why Now", f"{current_card.scores.timing_dynamics}/5.0")
d3.metric("White Space", f"{current_card.scores.competitive_white_space}/5.0")
d4.metric("Portfolio Fit", f"{current_card.scores.portfolio_fit}/5.0")
d5.metric("Commercial Potential", f"{current_card.scores.commercial_potential}/5.0")
d6.metric("Risk & Safety", f"{current_card.scores.risk_uncertainty}/5.0")

st.info(f"**Market Landscape:** `{current_card.market_type.value}` | **Commercial Potential:** `{current_card.commercial_potential_label.value}`")

# 14 Mandatory Fields Card
st.markdown("### 📑 Full Opportunity Card (Executive View)")

c1, c2 = st.columns(2)
with c1:
    st.markdown(f"**Consumer Problem:**\n\n> {current_card.consumer_problem}")
    st.markdown(f"**Target User:**\n\n{current_card.target_user}")
    st.markdown(f"**Potential Target Entity (Providers):**\n\n{current_card.target_entity}")
    st.markdown(f"**Why Now? (Dated Drivers & Signals):**\n\n{current_card.why_now}")
    st.markdown(f"**Portfolio Fit & FOCUS Brand Alignment:**\n\n{current_card.portfolio_fit}")

with c2:
    st.markdown(f"**Competitive Situation & White Space:**\n\n{current_card.competitive_situation}")
    st.markdown(f"**Legal Precedents & Historical Learnings (`02_learnings.csv`):**\n\n{current_card.historical_learning}")
    
    st.markdown("**Strictly Evidenced Facts:**")
    for f in current_card.facts:
        st.markdown(f"- ✅ {f}")
        
    st.markdown("**Unverified Hypotheses:**")
    for h in current_card.hypotheses:
        st.markdown(f"- 💡 {h}")

st.markdown("**Risks & Uncertainties (Separated, Not Hidden in Scores):**")
for r in current_card.risks_and_uncertainties:
    st.markdown(f"- ⚠️ {r}")

st.markdown("**Next Validation Questions (Feasibility Handover):**")
for q in current_card.next_validation_questions:
    st.markdown(f"- ❓ {q}")

st.markdown(f"**Grounded Record IDs Cited:** " + " ".join([f"`{rid}`" for rid in current_card.evidence]))

# Executive AI Copilot Section (Tesseracted Labs Shared Gateway)
st.markdown("---")
st.markdown("### 🤖 Executive AI Analyst Copilot (Tesseracted Labs Shared Gateway)")
st.caption(f"Powered by `{selected_ai_model}` · Zero-hallucination prompt guardrails active")

ai_col1, ai_col2 = st.columns([1, 1])

with ai_col1:
    st.markdown("#### ✨ One-Click Executive Pitch Memo")
    st.write("Generate a crisp, C-level investment summary strictly grounded in this card's record IDs.")
    if st.button("Generate Executive Memo"):
        with st.spinner("Calling Tesseracted AI Gateway..."):
            memo = synthesize_executive_narrative(
                current_card.proposed_topic,
                current_card.model_dump(),
                model=selected_ai_model
            )
            st.success("Investment Memo Generated:")
            st.markdown(memo)

with ai_col2:
    st.markdown("#### 💬 Ask the AI Analyst (Live Jury Q&A)")
    st.write("Ask any question regarding this topic's risks, white space, or why we recommended its status.")
    user_q = st.text_input("Your Question to the Analyst:", placeholder="e.g. Why is this topic dangerous to pursue?")
    if st.button("Ask Analyst") and user_q:
        with st.spinner("Analyzing dossier via AI Gateway..."):
            answer = ask_copilot_question(
                user_q,
                current_card.proposed_topic,
                current_card.model_dump(),
                model=selected_ai_model
            )
            st.markdown(f"**Analyst Response:**\n\n{answer}")

# Tabbed Evidence Explorer
st.markdown("---")
st.markdown("### 🔬 Grounded Evidence Explorer (Raw Records)")
tab_sig, tab_ind, tab_comp, tab_pop, tab_evt, tab_lrn = st.tabs([
    f"Signals ({len(dossier['signals'])})",
    f"Indicators ({len(dossier['indicators'])})",
    f"Competitors ({len(dossier['competitors'])})",
    f"Populations ({len(dossier['populations'])})",
    f"Regulatory Events ({len(dossier['events'])})",
    f"Learnings ({len(dossier['learnings'])})"
])

with tab_sig:
    if dossier['signals']:
        st.dataframe(pd.DataFrame(dossier['signals'])[['signal_id', 'signal_type', 'period', 'title', 'summary', 'evidence_status']])
    else:
        st.write("No signals recorded for this topic.")

with tab_ind:
    if dossier['indicators']:
        st.dataframe(pd.DataFrame(dossier['indicators'])[['indicator_id', 'metric', 'value', 'unit', 'period', 'note']])
    else:
        st.write("No numeric market indicators recorded.")

with tab_comp:
    if dossier['competitors']:
        st.dataframe(pd.DataFrame(dossier['competitors'])[['competitor_id', 'name', 'competitor_type', 'has_quality_assessment', 'provider_pays', 'coverage']])
    else:
        st.write("No competitors recorded.")

with tab_pop:
    if dossier['populations']:
        st.dataframe(pd.DataFrame(dossier['populations'])[['population_id', 'entity_type', 'count', 'period', 'master_list_source', 'master_list_availability']])
    else:
        st.write("No entity population recorded.")

with tab_evt:
    if dossier['events']:
        st.dataframe(pd.DataFrame(dossier['events'])[['event_id', 'event_date', 'timing', 'event_type', 'title', 'description']])
    else:
        st.write("No regulatory events recorded.")

with tab_lrn:
    if dossier['learnings']:
        st.dataframe(pd.DataFrame(dossier['learnings'])[['learning_id', 'date', 'case_type', 'title', 'lesson', 'risk_category']])
    else:
        st.write("No negative court precedents or failed rating cases recorded.")

# Export section in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("💾 Export Deliverables")

json_file = os.path.join(APP_DIR, "cards.json")
if os.path.exists(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        st.sidebar.download_button(
            label="Download cards.json",
            data=f.read(),
            file_name="cards.json",
            mime="application/json"
        )

md_file = os.path.join(APP_DIR, "cards.md")
if os.path.exists(md_file):
    with open(md_file, "r", encoding="utf-8") as f:
        st.sidebar.download_button(
            label="Download cards.md",
            data=f.read(),
            file_name="cards.md",
            mime="text/markdown"
        )

logic_file = os.path.join(APP_DIR, "LOGIC.md")
if os.path.exists(logic_file):
    with open(logic_file, "r", encoding="utf-8") as f:
        st.sidebar.download_button(
            label="Download LOGIC.md",
            data=f.read(),
            file_name="LOGIC.md",
            mime="text/markdown"
        )
