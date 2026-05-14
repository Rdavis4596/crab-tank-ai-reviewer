# Crab Tank AI Reviewer

AI-powered application scoring tool for Baltimore Homecoming's Crab Tank Entrepreneurship Program.

---

## 1. Context, User, and Problem

**Who the user is:** Robinson and the Baltimore Homecoming selection committee — volunteers who administer the Crab Tank Entrepreneurship Program, a competitive grant awarding a $25,000 grand prize to Baltimore-based businesses.

**What workflow this improves:** Each application cycle, committee members individually read 10+ business applications and score each one across 10 rubric dimensions (1–5 scale, 50 points total). This process is time-consuming, inconsistent across reviewers, and fatiguing for busy volunteers.

**Why it matters:** A consistent AI-assisted first pass reduces reviewer fatigue, surfaces eligibility issues automatically, and ensures every application is evaluated against the same criteria. Human reviewers can focus their energy on borderline cases and final deliberation rather than reading every application from scratch.

---

## 2. Solution and Design

**What I built:** A Python-based scoring tool that reads a Crab Tank application (free-text answers and structured fields), scores it across 10 rubric dimensions (1–5 each), produces a total score out of 50, and provides a one-sentence justification grounded in the application text for each dimension. It also flags eligibility issues automatically.

**How it works:**

1. Application text is passed to Claude via the Anthropic API along with a carefully structured system prompt
2. The system prompt encodes the full 10-dimension rubric, scoring anchors (1 = very weak, 3 = adequate, 5 = very strong), and eligibility criteria
3. The model returns a structured JSON object: scores, rationales, total, and eligibility flags
4. Results are displayed in a formatted table ready for committee review

**Key design choices:**

- **Structured system prompt:** The full rubric, scoring anchors, and output schema are encoded in the system prompt — not left to the model's defaults. This is the core design decision that separates this tool from simply pasting an application into ChatGPT.
- **Low temperature (0.2):** Promotes consistent, deterministic scoring across repeated runs.
- **JSON output constraint:** The model is instructed to return only a specific JSON schema, making results parseable and reliable.
- **Eligibility flag logic:** The system prompt includes hard eligibility rules (Baltimore City headquarters, revenue-generating, active founder) and instructs the model to surface violations explicitly.
- **Rationale grounding:** The model is instructed to ground each rationale in the application text — not generate plausible-sounding but unsupported justifications.

**The 10 rubric dimensions:**
1. Problem & Solution
2. Business Model & Revenue Potential
3. Market Understanding
4. Traction & Validation
5. Scalability & Growth
6. Baltimore Impact
7. Baltimore Commitment
8. Founder & Team Strength
9. Execution Plan & Goals
10. Overall Fit for Crab Tank

---

## 3. Evaluation and Results

### Baseline
The naive baseline is pasting the same application into an LLM with a minimal prompt — no rubric encoding, no structured output, no scoring anchors, no eligibility logic. This simulates how the task might be done without this tool.

### Test Set
Two real (anonymized) Crab Tank applications were used: one food & beverage startup and one healthcare company. Both were scored three ways:
- **Structured AI** (this tool, full system prompt + rubric + JSON constraint)
- **Baseline AI** (minimal prompt, no rubric, no structure)
- **Human ground truth** (Robinson scoring manually using the official scorecard)

### Results

| | Structured AI | Baseline AI |
|---|---|---|
| MAE vs. human | **0.85** | 1.05 |
| Agreement rate (within ±1) | **90%** | 80% |

The structured tool agreed with human scores within ±1 point on 18 of 20 dimension scores. The baseline agreed on only 16 of 20.

**Per-application breakdown:**

| Application | Structured MAE | Baseline MAE | Structured Agreement | Baseline Agreement |
|---|---|---|---|---|
| App 1 (F&B) | 0.80 | 1.10 | 100% | 80% |
| App 2 (Healthcare) | 0.90 | 1.00 | 80% | 80% |

**Totals (out of 50):**

| Application | Structured | Baseline | Human |
|---|---|---|---|
| App 1 (F&B) | 40 | 37 | 44 |
| App 2 (Healthcare) | 37 | 40 | 35 |

### Key findings

- The structured tool outperformed the baseline on both MAE and agreement rate
- The most important qualitative difference: the structured tool correctly flagged that App 2 was headquartered outside Baltimore City and scored Baltimore Commitment a 2 — matching the human score exactly. The baseline scored it a 3 and missed the nuance entirely
- App 1 (F&B) showed 100% agreement rate with the structured tool — every dimension within ±1 of human scoring
- Score compression was not a major issue; the model scored confidently at both ends of the scale when evidence was clear

### Where it breaks down
- Applications with very short or vague answers produce lower-confidence scores
- Subjective dimensions like "Overall Fit" showed the most divergence between AI and human
- The tool cannot assess tone, body language, or verified track record — only what is written
- Applicants who copy rubric language back into their answers may receive inflated scores

---

## 4. Artifact Snapshot

The tool accepts application text and returns a structured scoring table like this:

| Dimension | Score | Rationale |
|---|---|---|
| Problem & Solution | 5/5 | Applicant identifies a deeply underserved gap with the first brown breast form, grounded in the founder's personal experience. |
| Business Model | 4/5 | $150k YTD revenue and $850k 12-month goal supported by DTC and hospital partnership model show a credible path. |
| Baltimore Commitment | 2/5 | Company is headquartered in Prince George's County, not Baltimore City; founder is not a Baltimore native. |
| ... | ... | ... |
| **Total** | **37/50** | |

**Eligibility flags surfaced:**
- ⚠️ Company headquartered outside Baltimore City — priority given to Baltimore City-based businesses

> **Disclaimer:** AI scores are for committee reference only. All selections require human review and final committee approval.

---

## Setup and Usage

### Requirements
```
anthropic
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### API Key
This tool requires an Anthropic API key. Set it as an environment variable:
```bash
export ANTHROPIC_API_KEY=your_key_here
```

Never commit your API key to the repository.

### Running the scorer
```bash
python scripts/score.py
```

The script will prompt you to paste application text, then return a formatted scoring table with rationales, total score, and any eligibility flags.

### Input format
Paste the full application text when prompted. The tool works best with complete applications including business description, goals, funding details, and community impact sections.

---

## Repository Structure

```
crab-tank-ai-reviewer/
├── README.md
├── requirements.txt
├── scripts/
│   └── score.py               ← main scoring script
├── prompts/
│   └── system_prompt.txt      ← full rubric system prompt
├── data/
│   └── sample_applicants.csv  ← anonymized test data
├── evaluation/
│   ├── ground_truth_scores.csv
│   ├── ai_scores.csv
│   ├── baseline_scores.csv
│   └── eval_results.md
└── assets/
    └── screenshot.png
```

---

## Governance and Limitations

- AI scores are a **first-pass triage tool only** — never the sole basis for selection or rejection
- Borderline cases must always go to human committee review
- All scores and rationales should be exported and retained for audit purposes
- No real applicant PII is stored or committed to this repository — all test data is anonymized
