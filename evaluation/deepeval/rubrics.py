# evaluation/deepeval/rubrics.py

SECURITY_JUDGMENT_RUBRIC = """
You are evaluating a cybersecurity SOC agent.

Given MCP tool outputs and the final security report,
judge whether the agent:

1. Correctly interprets the available security signals
2. Does NOT hallucinate attacks, indicators, or facts
3. Makes reasonable next-step recommendations
4. Avoids unjustified confidence when evidence is weak

Scoring guide:
- 1–2: Hallucinated, misleading, or unsafe analysis
- 3: Mostly reasonable but vague or overly generic
- 4–5: Grounded, cautious, and appropriate analysis

Only judge based on evidence present in the input.
"""
