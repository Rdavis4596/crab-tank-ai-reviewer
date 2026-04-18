# project_plan.md

## 1. Project Title

**Crab Tank AI Reviewer: Automated Application Scoring for the Crab Tank Entrepreneurship Program**

---

## 2. Target User, Workflow, and Business Value

**Who the user is:** Robinson and the Baltimore Homecoming selection committee staff who administer the Crab Tank Entrepreneurship Program — a competitive grant program awarding a $25,000 grand prize to Baltimore-based businesses.

**What recurring task this improves:** Each application cycle, committee members must individually read all submitted business applications and score each one across 10 rubric dimensions (1–5 scale, 50 points total). With ~10+ applications per reviewer and multiple reviewers, this process is time-consuming and subject to inconsistency across reviewers.

**Where the workflow begins and ends:** The workflow begins when an applicant submits their completed application form (covering business model, market fit, Baltimore ties, founder credibility, goals, and financials). It ends when a numeric score out of 50 is produced, along with a brief rationale for each rubric dimension, ready for the committee to review or use as a first-pass filter.

**Why this matters:** The selection committee is composed of busy volunteers. A consistent AI-assisted first pass reduces reviewer fatigue, surfaces scoring inconsistencies, and helps ensure every application is evaluated against the same criteria. This allows human reviewers to focus their attention on borderline cases and final deliberation rather than grinding through every application from scratch.

---

## 3. Problem Statement and GenAI Fit

**Exact task:** Given a submitted Crab Tank application (free-text answers and structured fields) and the official 10-question rubric, the system will read the application, score it on each of the 10 rubric dimensions (1–5), produce a total score out of 50, and provide a one-sentence justification per dimension.

**Why this benefits from LLMs:** The rubric requires reading comprehension, judgment about business viability, evaluation of narrative quality, and interpretation of qualitative claims (e.g., "does the applicant clearly articulate Baltimore commitment?"). These are natural language reasoning tasks that LLMs handle well. Structured scoring outputs further make this tractable.

**Why a simpler tool wouldn't be enough:** A keyword-matching script or simple form logic cannot assess whether a business model is "well-defined," whether traction evidence is compelling, or whether a founder's story demonstrates credibility. These require reading the full application and applying judgment — which is exactly what LLMs are suited for.

---

## 4. Planned System Design and Baseline

**Architecture:**

The app is a Streamlit web application. The user (Robinson or a committee staff member) pastes or uploads a completed application. The system sends the application text along with the full rubric and program eligibility criteria to an LLM with a carefully structured system prompt. The model returns a JSON object with scores for all 10 rubric dimensions, a total score, and one-sentence justifications per dimension. The UI displays the scores in a formatted table and flags any eligibility disqualifiers (e.g., company not in Baltimore, solo founder, no revenue).

**Course concepts integrated:**

1. **Anatomy of an LLM call: system prompts, structured outputs, output constraints (Week 2–3):** The system prompt encodes the full rubric text, the eligibility criteria, the scoring scale definition, and an instruction to respond only in a specified JSON schema. Temperature is set low (0.2) to promote consistent, deterministic scoring. The output is constrained to a JSON structure: `{scores: [{dimension: str, score: int, rationale: str}], total: int, eligibility_flags: [str]}`. This ensures the app can reliably parse and display results.

2. **Evaluation design: rubrics, test sets, baselines, model-as-judge (Week 6):** I will construct a test set of 10–15 synthetic applications spanning strong, average, and weak candidates. For each, I will manually assign ground-truth scores using the rubric. I will then compare the AI scores against my ground-truth scores and against a "baseline" of a zero-shot prompt with no system prompt or structure. I will also use the model as a meta-judge to check its own rationales for consistency. Metrics include mean absolute error per dimension and agreement rate (within ±1 point) with ground truth.

**Baseline for comparison:** A naive approach where the user simply pastes the application into a generic ChatGPT prompt with no structured system prompt, rubric encoding, or output constraints — and manually reads the freeform response to extract scores. The AI Reviewer will be compared against this on scoring consistency, time-to-result, and agreement with ground truth.

**The app:** A Streamlit app with a text area for pasting application content, a "Score Application" button, and a results panel showing a table of the 10 rubric dimensions, the AI score for each, the rationale, and the total. A sidebar displays the rubric for reference. Eligibility flags (e.g., "⚠️ Applicant did not confirm Baltimore headquarters") appear at the top. The results can be downloaded as a CSV for the committee's records.

---

## 5. Evaluation Plan

**What success looks like:** The AI scores agree with human ground-truth scores within ±1 point on at least 75% of rubric dimensions, across a diverse test set of applications. The system also correctly surfaces eligibility disqualifiers when present.

**What I will measure:**
- Mean absolute error (MAE) per rubric dimension, AI vs. ground truth
- Agreement rate (within ±1) across all dimensions and applications
- Eligibility flag accuracy (precision/recall on planted disqualifiers)
- Latency per application (target: under 15 seconds)
- Qualitative review of rationale sentences for coherence and relevance

**Test set:** 12–15 synthetic applications: 4 strong (expected score 40–50), 4 average (25–39), 4 weak (under 25), plus 2–3 with planted eligibility disqualifiers (e.g., non-Baltimore address, solo founder). Applications will be written to cover varied industries from the CTE form (tech, food & beverage, healthcare, etc.).

**Baseline comparison:** Run the same 12–15 applications through the naive approach (no structured prompt, no JSON output). Compare MAE vs. ground truth for both approaches. Measure time required per evaluation for both.

---

## 6. Example Inputs and Failure Cases

**Example inputs:**

1. A food & beverage startup with strong Baltimore roots, clear revenue ($80k/year), and a solo founder (eligibility flag expected).
2. A tech company with a vague problem statement, no revenue data, but a compelling Baltimore community impact story — tests whether the model can differentiate across dimensions rather than scoring holistically.
3. A healthcare startup with strong financials, a two-person team, and a well-articulated growth plan but weak Baltimore narrative.
4. A company with a pitch-perfect application across all 10 dimensions — used to verify the model can score high confidently and not anchor toward the middle.
5. An application with internally inconsistent answers (e.g., claims revenue-generating but says "we have no paying customers yet") — tests reasoning under contradiction.

**Anticipated failure cases:**

1. **Hallucinated justifications:** The model may produce plausible-sounding rationales that don't actually ground in the application text (e.g., attributing a revenue figure that wasn't stated). Mitigation: instruct the model to quote or paraphrase application text in each rationale.
2. **Score compression toward the middle:** LLMs tend to avoid extremes. An application that clearly deserves a 1 or a 5 may receive a 2 or 4 instead. Mitigation: include anchor examples in the system prompt (few-shot examples with explicitly weak and strong scores) and evaluate score distribution across the test set.

---

## 7. Risks and Governance

**Where the system could fail:**
- Applications that are very short or vague may produce unreliable scores due to insufficient signal.
- The model may be inconsistent across repeated runs (mitigated by low temperature and structured output).
- Applicants who game the form language (e.g., copying rubric language back into their answers) could inflate AI scores without having genuine substance.

**Where it should not be trusted:**
- The AI score should never be the sole basis for selecting or rejecting an applicant. It is a first-pass triage tool, not a decision-maker.
- Borderline cases (scores near the semifinalist cutoff) must be reviewed by a human committee member.
- Scoring on subjective dimensions like "founder credibility" is inherently limited by what is written — the AI cannot assess tone, body language, or verified track record.

**Controls and human-review boundaries:**
- The app will display a disclaimer on every result: "AI scores are for committee reference only. All selections require human review and final committee approval."
- Eligibility disqualifiers will always require a human to confirm before an application is excluded.
- All scores and rationales will be exportable to CSV for audit purposes.

**Data, privacy, and cost concerns:**
- All development and testing will use synthetic application data only. No real applicant PII will be used or committed to the repository.
- API calls will use Claude or GPT-4o-mini to keep costs low (estimated under $1 per full batch of 10 applications). API keys will be stored in environment variables, never in code.

---

## 8. Plan for the Week 6 Check-In

By Week 6, I expect to have:

- **App running:** A functional Streamlit app that accepts a pasted application, sends it to the LLM with the encoded rubric and system prompt, and displays the 10-dimension score table with rationales and total score.
- **Evaluation in place:** A test set of at least 8 synthetic applications with manually assigned ground-truth scores. The app will have been run against all 8, and MAE and agreement rate will be calculated and recorded.
- **Baseline comparison:** The same 8 applications will have been run through the naive prompt approach, and side-by-side MAE numbers will be available to show the improvement from structured prompting and output constraints.
- **Eligibility flag logic:** At least 2 of the test applications will include planted eligibility issues, and the flag detection will be functional and measured for accuracy.
