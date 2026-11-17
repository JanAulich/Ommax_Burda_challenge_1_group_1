# Deliverables & judging

**One day, one focused goal:** show a working prototype that turns the supplied data into **3–5 evidence-backed
opportunity cards** and helps FACTS decide what to investigate next. Depth beats breadth.

---

## 1. Scope for the day

| In scope (expected) | Out of scope (don't spend time on it) |
|---|---|
| Using the prepared data in `data/` | Crawling, scraping, collecting new data |
| Your own prioritisation logic (rules, weights, agents, …) | A final TOP-List methodology or provider ranking |
| 3–5 opportunity cards with all fields | Market-sizing models, seal pricing |
| Explaining *why* each card got its status | Master lists of providers |
| Flagging risks and human review | Production deployment, logins, Salesforce integration |
| A simple UI or a clean notebook / CLI output | Polished design systems or mobile apps |

**Data:** use `data/` only. Web access is not needed and does not earn points. LLM APIs are allowed — but every fact on a card
must cite a record ID from `data/`.

**Prepared for you:** the dataset, the [data guide](03_data_guide.md), a retrieval view (`evidence/corpus.jsonl`) and an integrity
check (`scripts/validate_dataset.py`). The card fields are defined in the [brief](01_challenge_brief.md#5-deliverable).

---

## 2. What to hand in

Submit **by the deadline announced on the day** (repo link or zip):

| # | Deliverable | Minimum content |
|---|---|---|
| 1 | **Working prototype** | Runs on the supplied data; run instructions in a `README.md` (≤ 5 commands) |
| 2 | **Opportunity cards** | 3–5 cards exported as Markdown, HTML or PDF, **plus** JSON (machine-readable). All fields from the [brief](01_challenge_brief.md#5-deliverable) |
| 3 | **One-page logic note** (`LOGIC.md`) | Your criteria, weights or rules, how missing evidence is handled, when human review is triggered, known limits |
| 4 | **Live demo** | See §3 |

Optional: an architecture diagram, a short screen recording as a backup for the live demo.

---

## 3. Demo format

**5 minutes demo + 3 minutes Q&A per team.** Show the running prototype, not slides about it (max. 2 slides of context).

Your demo should show, in this order:
1. **The question in, the shortlist out** — how a FACTS user gets from data to 3–5 ranked opportunities.
2. **One "Validate Next" card in depth** — trace one *why-now* claim to its record and source period, show the portfolio overlap
   check and one competitor that weakens the white-space claim.
3. **One "no"** — a Deprioritise or Do Not Pursue card and the reason.
4. **Trust** — where facts vs. hypotheses are separated, which risks are flagged, and why a human must review.

**Jury challenge (expect it):** the jury may name a topic (e.g. "funeral services" or "driving schools") and ask your tool to
assess it live. This shows the logic generalises and is not hard-coded to your showcase cards.

---

## 4. Pass/fail gates

A submission must pass all gates to be ranked:

- [ ] Runs on the supplied data (live or recorded fallback)
- [ ] ≥ 3 opportunity cards with all required fields and a recommended status
- [ ] Every fact and why-now claim cites existing record IDs — **invented IDs or invented numbers disqualify the card**
- [ ] Human-review flag with reasons on every card

---

## 5. Judging rubric

This is the scoring sheet the jury uses for your pitch and demo. Each of the 15 criteria is scored **1–5** by every juror;
the score is multiplied by the weight and summed (maximum 5.00). Read the guiding questions as a checklist for your own prototype.

| Category | Criterion | Guiding question | Weight |
|---|---|---|---:|
| **1. Business relevance (34 %)** | Topic specificity | Is the proposed Top List topic specific, understandable, and not just a broad category? | 8 % |
| | Consumer need | Does it address a relevant, difficult, or consequential consumer decision? | 8 % |
| | FACTS and portfolio fit | Does it fit FACTS, the FOCUS brands, and the existing portfolio — without unnecessary cannibalisation? | 10 % |
| | Commercial potential | Is there a plausible, sufficiently large, and fundamentally listable target group of organisations? If not evidenced, is this honestly treated as a hypothesis? | 8 % |
| **2. Opportunity logic (22 %)** | Why now? | Are trends, indicators, or regulatory events used and clearly linked to an orientation need? | 8 % |
| | Competitive white space | Is the competitive landscape analysed in a differentiated way — e.g. directory-dominated, fragmented, or well-served — rather than treating competition as a blanket exclusion criterion? | 9 % |
| | Status recommendation | Is the recommendation (*Validate Next / Monitor / Deprioritise / Do Not Pursue*) logical, nuanced, and consistently justified? | 5 % |
| **3. Evidence, trust & explainability (20 %)** | Evidence & sources | Are facts and "why now" claims backed by valid dataset record IDs? | 10 % |
| | Facts vs. hypotheses | Are facts, hypotheses, risks, and open questions clearly separated? | 6 % |
| | Risk and precedent check | Are legal, methodological, data, and reputational risks as well as relevant learnings made visible? | 4 % |
| **4. Technical quality (15 %)** | Traceable logic | Is it clear how the data leads to a recommendation? Is there no black-box evaluation? | 5 % |
| | Robustness & data validation | Does the solution prevent invented IDs, numbers, or sources? Does it work reproducibly with the provided data? | 5 % |
| | Generalisability | Can the tool assess a newly mentioned topic on the fly, instead of only evaluating pre-prepared showcase cards? | 5 % |
| **5. User experience & pitch (9 %)** | Clarity of the opportunity cards | Can FACTS experts quickly understand and challenge the recommendation, evidence, risks, and next steps? | 5 % |
| | Demo & pitch quality | Is the demo clear, focused, convincing, and within the time? | 4 % |
| | **Total** | | **100 %** |

**Score scale (all criteria):** 1 = missing or misleading (e.g. broad category, claims without IDs, black-box score, hard-coded
output) · 3 = solid and mostly consistent · 5 = excellent, specific, traceable and honest about gaps.

**Final score** = Σ (average juror score × weight). **Tie-break:** higher category 3 (*Evidence, trust & explainability*), then
higher category 1 (*Business relevance*).

### What does not earn extra points
- More than 5 cards, or more topics generated
- Data from outside the pack
- Model size or number of agents for its own sake
- Visual polish without working logic

---

## 6. Suggested timeline for the day

| Time | Focus |
|---|---|
| First hour | Read brief + guardrails, explore data, agree on scoring logic |
| Late morning | Pipeline: load → retrieve evidence → assess → status |
| Early afternoon | Cards with citations, review flags, minimal UI |
| Mid-afternoon | Test against a random topic (prepare for the jury challenge); fix evidence gaps |
| Last hour | `README.md`, `LOGIC.md`, record a backup video, rehearse the 5-minute demo |

---

## 7. Submission checklist

- [ ] `README.md` with run instructions
- [ ] `LOGIC.md` (one page)
- [ ] Cards: `cards.md`/`.html`/`.pdf` **and** `cards.json`
- [ ] Prototype runs from a fresh clone on the supplied data
- [ ] All gates in §4 pass
- [ ] Demo rehearsed in ≤ 5 minutes; backup recording ready
