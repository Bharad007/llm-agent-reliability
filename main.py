import json
from AgentA import agentic_code_evaluation
from AgentB import judge_agent_output

MAX_ITERATIONS = 3


def run_review_loop(code_str: str, ground_truth: dict) -> dict:
    feedback = None
    a_result = None
    b_result = None

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

        feedback = b_result.get("feedback")

    return {
        "status": "max_iterations_reached",
        "iterations": MAX_ITERATIONS,
        "agent_a_report": a_result,
        "agent_b_review": b_result,
    }


if __name__ == "__main__":
    with open("snippets/scraper_001.js", "r", encoding="utf-8") as file:
        code_str = file.read()

    with open("ground_truth.json", "r", encoding="utf-8") as file:
        gt_data = json.load(file)
        ground_truth = next(s for s in gt_data["snippets"] if s["snippet_id"] == "scraper_001")

    result = run_review_loop(code_str, ground_truth)
    print(json.dumps(result, indent=2))