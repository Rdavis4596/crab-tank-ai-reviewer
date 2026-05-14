# Evaluation Results

## Test Set
Two real anonymized Crab Tank applications scored three ways:
- **Structured AI** — this tool (full rubric system prompt + JSON output constraint)
- **Baseline AI** — minimal prompt, no rubric, no structure
- **Human** — Robinson scoring manually using the official scorecard

## Scores by Application

### App 1 — Food & Beverage startup (anonymized)

| Dimension | Structured AI | Baseline AI | Human |
|---|---|---|---|
| Problem & Solution | 4 | 4 | 5 |
| Business Model & Revenue Potential | 4 | 4 | 5 |
| Market Understanding | 4 | 3 | 5 |
| Traction & Validation | 5 | 5 | 4 |
| Scalability & Growth | 4 | 4 | 3 |
| Baltimore Impact | 3 | 3 | 4 |
| Baltimore Commitment | 4 | 3 | 5 |
| Founder & Team Strength | 4 | 3 | 4 |
| Execution Plan & Goals | 4 | 4 | 4 |
| Overall Fit for Crab Tank | 4 | 4 | 5 |
| **Total** | **40** | **37** | **44** |

### App 2 — Healthcare startup (anonymized)

| Dimension | Structured AI | Baseline AI | Human |
|---|---|---|---|
| Problem & Solution | 5 | 5 | 5 |
| Business Model & Revenue Potential | 4 | 4 | 3 |
| Market Understanding | 4 | 4 | 5 |
| Traction & Validation | 4 | 4 | 4 |
| Scalability & Growth | 4 | 4 | 5 |
| Baltimore Impact | 4 | 4 | 2 |
| Baltimore Commitment | 2 | 3 | 2 |
| Founder & Team Strength | 4 | 4 | 3 |
| Execution Plan & Goals | 3 | 4 | 5 |
| Overall Fit for Crab Tank | 3 | 4 | 2 |
| **Total** | **37** | **40** | **35** |

## Summary Metrics (combined, 20 dimension scores)

| Metric | Structured AI | Baseline AI |
|---|---|---|
| MAE vs. human | **0.85** | 1.05 |
| Agreement rate (within ±1) | **90%** | 80% |

## Key Findings

- The structured tool outperformed the baseline on both MAE and agreement rate
- Most important qualitative difference: the structured tool scored App 2's Baltimore Commitment a 2 — correctly flagging that the company is headquartered outside Baltimore City. The baseline scored it a 3 and missed the nuance. Human score: 2.
- App 1 achieved 100% agreement rate with the structured tool — every dimension within ±1 of human scoring
- The structured tool met the 75% agreement rate target set in the project plan, achieving 90%

## Where the Tool Breaks Down

- Very short or vague applications produce lower-confidence scores
- Subjective dimensions like "Overall Fit" showed the most divergence
- The tool cannot assess tone, body language, or verified track record
- Applicants who mirror rubric language in their answers may receive inflated scores
