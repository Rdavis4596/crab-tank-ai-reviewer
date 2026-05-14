#!/usr/bin/env python3
"""
Crab Tank AI Reviewer
Baltimore Homecoming — Crab Tank Entrepreneurship Program

Scores a submitted application across 10 rubric dimensions (1-5 each)
and flags eligibility issues. Requires an Anthropic API key.

Usage:
    python scripts/score.py

Set your API key:
    export ANTHROPIC_API_KEY=your_key_here
"""

import anthropic
import json
import os

SYSTEM_PROMPT = """You are an expert evaluator for the Baltimore Homecoming Crab Tank Entrepreneurship Program.

Score the application on exactly 10 dimensions using the official rubric below.
Rating scale: 1 = Very weak / unclear / little evidence, 3 = Adequate, 5 = Very strong / compelling evidence.

Rubric dimensions:
1. Problem & Solution — Clear problem definition, strength and feasibility of solution
2. Business Model & Revenue Potential — Well-defined model, viable path to revenue/profitability
3. Market Understanding — Clear target market, evidence of customer demand
4. Traction & Validation — Evidence of traction, revenue activity, market validation
5. Scalability & Growth — Scalability and realistic growth potential in Baltimore
6. Baltimore Impact — Current/potential contributions to Baltimore economic/community landscape
7. Baltimore Commitment — Clearly articulates Baltimore relationship and commitment to operating in Baltimore City
8. Founder & Team Strength — Credibility, relevant skills, commitment to execution
9. Execution Plan & Goals — Realistic short/long-term goals and feasible execution plan
10. Overall Fit for Crab Tank — Overall strength as a Crab Tank candidate

Eligibility rules — flag if any of the following apply:
- Company is NOT headquartered in Baltimore City
- Business is NOT revenue-generating (no paying customers or investment)
- Founder is NOT actively running the business
- Business does NOT demonstrate scalability
- Application appears incomplete

Instructions:
- Ground every rationale in specific details from the application text
- Do not invent facts not present in the application
- Return ONLY valid JSON, no other text

Return this exact JSON structure:
{
  "scores": [
    {"dimension": "Problem & Solution", "score": 4, "rationale": "One sentence grounded in application text."},
    {"dimension": "Business Model & Revenue Potential", "score": 3, "rationale": "..."},
    {"dimension": "Market Understanding", "score": 4, "rationale": "..."},
    {"dimension": "Traction & Validation", "score": 5, "rationale": "..."},
    {"dimension": "Scalability & Growth", "score": 3, "rationale": "..."},
    {"dimension": "Baltimore Impact", "score": 4, "rationale": "..."},
    {"dimension": "Baltimore Commitment", "score": 4, "rationale": "..."},
    {"dimension": "Founder & Team Strength", "score": 4, "rationale": "..."},
    {"dimension": "Execution Plan & Goals", "score": 3, "rationale": "..."},
    {"dimension": "Overall Fit for Crab Tank", "score": 4, "rationale": "..."}
  ],
  "total": 38,
  "eligibility_flags": []
}"""


def score_application(application_text: str) -> dict:
    """Send application to Claude and return structured scores."""
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        temperature=0.2,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"Application:\n\n{application_text}"}
        ]
    )
    raw = response.content[0].text.strip()
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)


def print_results(results: dict) -> None:
    """Print a formatted scoring table to the console."""
    print("\n" + "=" * 65)
    print("  CRAB TANK AI REVIEWER — SCORING RESULTS")
    print("  Baltimore Homecoming Entrepreneurship Program")
    print("=" * 65)

    if results.get("eligibility_flags"):
        print("\n  ⚠️  ELIGIBILITY FLAGS:")
        for flag in results["eligibility_flags"]:
            print(f"     • {flag}")

    print(f"\n  {'DIMENSION':<35} {'SCORE':>5}")
    print("  " + "-" * 45)
    for item in results["scores"]:
        print(f"  {item['dimension']:<35} {item['score']:>3}/5")
        print(f"     {item['rationale']}")
        print()

    print("  " + "-" * 45)
    print(f"  {'TOTAL SCORE':<35} {results['total']:>3}/50")
    print("\n" + "=" * 65)
    print("  ⚠️  AI scores are for committee reference only.")
    print("  All selections require human review and final")
    print("  committee approval.")
    print("=" * 65 + "\n")


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        print("Run: export ANTHROPIC_API_KEY=your_key_here")
        return

    print("\nCrab Tank AI Reviewer")
    print("Paste the application text below, then press Enter twice and type END:\n")

    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    application_text = "\n".join(lines)
    if not application_text.strip():
        print("No application text provided.")
        return

    print("\nScoring application...")
    results = score_application(application_text)
    print_results(results)

    save = input("Save results to JSON? (y/n): ").strip().lower()
    if save == "y":
        filename = "scoring_output.json"
        with open(filename, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {filename}")


if __name__ == "__main__":
    main()
