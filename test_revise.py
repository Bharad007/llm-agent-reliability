import json
from core.AgentB import judge_agent_output

with open("agent_a_report.json", "r", encoding="utf-8") as f:
    agent_a_report = json.load(f)

with open("ground_truth.json", "r", encoding="utf-8") as f:
    gt_data = json.load(f)
    ground_truth = next(s for s in gt_data["snippets"] if s["snippet_id"] == "scraper_001")

for i in range(3):
    result = judge_agent_output(agent_a_report, ground_truth)
    print(f"--- Run {i+1} ---")
    print(f"verdict: {result['verdict']}, correctness: {result['correctness_score']}, completeness: {result['completeness_score']}")
    print(result["feedback"])
    print()