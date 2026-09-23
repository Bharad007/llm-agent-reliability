import json
from collections.abc import Callable
from typing import Any


def extract_json(raw_text: str) -> str:
    text = raw_text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        lines = lines[1:] if lines and lines[0].startswith("```") else lines
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text


def request_json(
    request: Callable[[], Any],
    max_attempts: int = 3,
) -> dict:
    last_raw_output = None

    for _ in range(max_attempts):
        message = request()
        raw_output = "".join(
            block.text
            for block in message.content
            if getattr(block, "type", None) == "text"
        )
        last_raw_output = raw_output

        try:
            parsed = json.loads(extract_json(raw_output))
            if not isinstance(parsed, dict):
                raise ValueError("Expected a JSON object")
            return parsed
        except (json.JSONDecodeError, ValueError):
            continue

    return {
        "error": f"Failed to parse JSON after {max_attempts} attempts.",
        "last_raw_output": last_raw_output,
    }
