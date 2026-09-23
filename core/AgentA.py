import os
import sys
import json
import anthropic
from dotenv import load_dotenv
from core.llm_json import request_json

load_dotenv()   
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables. Please set it in the .env file")

client = anthropic.Anthropic(api_key=api_key)

def agentic_code_evaluation(code_str: str, max_attempts: int = 3, feedback: str | None = None) -> dict:
    prompt = f"""You are a senior software engineer reviewing code.
                Analyze the code and return:
                1. What the code is trying to do.
                2. Any potential issues or bugs.
                3. A suggested fix for each issue.
                4. A confidence score from 1 to 10 on the accuracy of your analysis.

                Only report bugs supported by evidence in the code. Do not invent problems.

                {f"Previous judge feedback: {feedback}\nUse that feedback to revise your analysis and fix any missed or incorrect issues.\n" if feedback else ""}

                Return only valid JSON:

                {{
                    "summary": "What the code is trying to do",
                    "bugs": [
                        {{
                            "type": "Security",
                            "severity": "High",
                            "description": "What is wrong",
                            "suggested_fix": "How to fix it",
                            "line": "Line number or unknown"
                        }}
                    ],
                    "confidence_score": 8
                }}

                Here is the code:
                {code_str}
                """
    def request_analysis():
        return client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1500,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]   
        )
    return request_json(request_analysis, max_attempts=max_attempts)

if __name__ == "__main__":
    if len(sys.argv) not in {2, 3}:
        print("Usage: python AgentA.py <path_to_code_file> [output_json_file]")
        sys.exit(1)

    file_path = sys.argv[1]

    with open(file_path, "r", encoding="utf-8") as file:
        source_code = file.read()

    result = agentic_code_evaluation(source_code)
    if len(sys.argv) == 3:
        with open(sys.argv[2], "w", encoding="utf-8") as file:
            json.dump(result, file, indent=2)
    else:
        print(json.dumps(result, indent=2))