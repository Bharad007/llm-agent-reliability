import json
from pathlib import Path
from AgentA import agentic_code_evaluation
from AgentB import judge_agent_output

MAX_ITERATIONS = 3
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run_review_loop(code_str: str, ground_truth: dict) -> dict:
    feedback = None
    a_result = None
    b_result = None
    prev_scores = None

    for iteration in range(1, MAX_ITERATIONS + 1):
        print(f"Iteration {iteration}: feedback={feedback}")
        a_result = agentic_code_evaluation(code_str, feedback=feedback)
        b_result = judge_agent_output(a_result, ground_truth)
        print(f"Iteration {iteration}: verdict={b_result.get('verdict')}")

        if b_result.get("verdict") == "approve":
            return {
                "status": "approved",
                "iterations": iteration,
                "agent_a_report": a_result,
                "agent_b_review": b_result,
            }

        current_scores = (b_result.get("correctness_score", 0), b_result.get("completeness_score", 0))
        if prev_scores is not None and current_scores <= prev_scores:
            return {
                "status": "stalled",
                "iterations": iteration,
                "agent_a_report": a_result,
                "agent_b_report": b_result,
            }

        prev_scores = current_scores
        feedback = b_result.get("feedback")

    return {
        "status": "max_iterations_reached",
        "iterations": MAX_ITERATIONS,
        "agent_a_report": a_result,
        "agent_b_review": b_result,
    }


if __name__ == "__main__":
    snippet_path = PROJECT_ROOT / "snippets" / "split_001.py"
    ground_truth_path = PROJECT_ROOT / "ground_truth.json"

    with snippet_path.open("r", encoding="utf-8") as file:
        code_str = file.read()

    with ground_truth_path.open("r", encoding="utf-8") as file:
        gt_data = json.load(file)
        ground_truth = next(s for s in gt_data["snippets"] if s["snippet_id"] == "split_001")

    result = run_review_loop(code_str, ground_truth)
    print(json.dumps(result, indent=2))