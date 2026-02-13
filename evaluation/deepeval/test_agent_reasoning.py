# evaluation/deepeval/test_agent_reasoning.py

import subprocess
import sys
import re
from pathlib import Path

# --------------------------------------------------
# ✅ FIX 1: Ensure project root is on sys.path
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv()

from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import HallucinationMetric
from deepeval.models import LiteLLMModel

from evaluation.deepeval.rubrics import SECURITY_JUDGMENT_RUBRIC


# --------------------------------------------------
# ✅ Judge model (Groq via LiteLLM)
# --------------------------------------------------
judge_llm = LiteLLMModel(
    model="groq/llama-3.1-8b-instant"
)


def run_client():
    """
    Runs the MCP client and extracts the final security report.
    """
    result = subprocess.run(
        [sys.executable, "src/client/main.py"],
        capture_output=True,
        text=True,
        check=True
    )

    output = result.stdout.strip()

    match = re.search(
        r"=== FINAL SECURITY REPORT ===\n+(.*)",
        output,
        re.DOTALL
    )

    if not match:
        raise RuntimeError("Could not extract final security report")

    return match.group(1).strip()


def test_soc_agent_reasoning():
    final_report = run_client()

    test_case = LLMTestCase(
        input="Security signals and system events were collected via MCP tools.",
        actual_output=final_report,

        # DeepEval expects a LIST
        context=[final_report],

        expected_output=(
            "Analysis grounded in evidence, no hallucinated events, "
            "reasonable security recommendations, and explicit uncertainty handling."
        )
    )

    metrics = [
        HallucinationMetric(
            threshold=0.3,
            model=judge_llm
        )
    ]

    evaluate(
        test_cases=[test_case],
        metrics=metrics
    )
