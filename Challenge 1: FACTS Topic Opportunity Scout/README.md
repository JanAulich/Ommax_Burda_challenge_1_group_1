# FACTS Topic Opportunity Scout — Executive Cockpit
**TUM × OMMAX AI Hackathon · Hubert Burda Media / FACTS Challenge 1**

An audit-proof, hybrid decision engine combining **deterministic relational scoring** with **Tesseracted Labs Shared AI Gateway** to prioritize new TOP-List topics for Hubert Burda Media, grounded strictly in dataset records with zero hallucination.

---

## Quick Start (Run the Live Prototype)

Run the prototype in a single command from this directory or repository root:

```bash
# 1. Run Streamlit dashboard
../.venv/bin/streamlit run app.py
```

The executive cockpit opens automatically in your browser at `http://localhost:8501`.

---

## System Architecture: The Hybrid Model

Our solution uses a **two-layer hybrid architecture**:
1. **Deterministic Relational Engine (Scoring & Governance):**
   - **No LLM touches the scores or status recommendations.**
   - Calculates 5 dimensional scores ($A: 20\%, B: 15\%, C: 25\%, D: 20\%, E: 20\%$) using pure relational queries on the 10 CSV tables.
   - Enforces a strict 9-gate waterfall (*Validate Next*, *Monitor*, *Deprioritise*, *Do Not Pursue*).
   - Guarantees 100% auditability, sub-50ms execution, and zero pass/fail gate disqualifications.
2. **Executive AI Analyst Copilot (Tesseracted Labs Shared AI Gateway):**
   - Connected to the hackathon's shared gateway endpoint:
     `https://tesseracted.com/access_83444ac6-49d6-467b-a61f-0d39a98f0e87/ai_gateway/v1`
   - Key: `sk-adc87b823faeed543c2c5755130a44199e966c90b45f8228`
   - Supported models:
     - `deepseek-ai/DeepSeek-V4.1-Flash` (Default: ultra-fast, sharp reasoning)
     - `moonshotai/Kimi-K3.1-Pro` (Long-context German/English synthesis)
     - `zai-org/GLM-5.3-Flash`
   - **Two Core AI Jobs:**
     - **✨ One-Click Executive Investment Memo:** Synthesizes a C-level investment pitch strictly grounded in the card's verified record IDs.
     - **💬 Live Jury Q&A Copilot:** Answers real-time questions from OMMAX consultants or Burda executives about risks, white space, and status rationale.

---

## Deliverables Generated

- 📄 **[cards.json](cards.json)** — Machine-readable opportunity cards.
- 📑 **[cards.md](cards.md)** — Executive opportunity cards report.
- 📐 **[LOGIC.md](LOGIC.md)** — One-page prioritisation methodology & scoring rubric.
