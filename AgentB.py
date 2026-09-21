import os
import sys
import json
import anthropic
from dotenv import load_dotenv
from llm_json import request_json

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables. Please set it in the .env file.")


client = anthropic.Anthropic(api_key=api_key)


def judge_agent_output(
    agent_a_report: dict,
    ground_truth: dict,
    max_attempts: int = 3
) -> dict:
    prompt = f"""
    You are evaluating the quality of a code-analysis agent.
    Compare Agent A's report against the ground truth.

    Evaluate:
    1. Correctness: 
        Are Agent A's explanations and bug descriptions factually accurate?
        Penalize claims that are unsupported or wrong.
    2. Completeness:
        How many important ground-truth bugs did Agent A identify?
        Consider equivalent descriptions as matches even if the wording differs.
    3. Feedback
        Explain which bugs were correctly identified, which were missed.
        Mention false positives separately.

    Return only valid JSON in this exact shape:

    {{
        "correctness_score": 0,
        "completeness_score": 0,
        "verdict": "approve|revise",
        "feedback": "Detailed evaluation"
    }}  
    AGENT_A Report:
    <agent_a_report>
    {json.dumps(agent_a_report, indent=2)}
    </agent_a_report>

    GROUND TRUTH:
    <ground_truth>
    {json.dumps(ground_truth, indent=2)}    
    </ground_truth>
    """

    def request_judgment():
        return client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=800,
            messages=[{
                "role": "user", "content": prompt
            }],
        )

    return request_json(request_judgment, max_attempts=max_attempts)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python AgentB.py <agent-a-report.json> <ground-truth.json>")
        sys.exit(1)

    try:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            agent_a_report = json.load(file)

        with open(sys.argv[2], "r", encoding="utf-8") as file:
            ground_truth = json.load(file)
    except FileNotFoundError as error:
        raise SystemExit(f"Input file not found: {error.filename}") from error
    except json.JSONDecodeError as error:
        raise SystemExit(
            f"Invalid JSON in input file at line {error.lineno}, column {error.colno}: {error.msg}"
        ) from error

    result = judge_agent_output(agent_a_report, ground_truth)
    print(json.dumps(result, indent=2))


