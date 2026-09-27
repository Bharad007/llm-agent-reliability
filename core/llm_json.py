import json
import time 
import anthropic
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
    retry_delay_seconds: float = 1.0,
) -> dict:
    last_raw_output = None
    last_error = None

    for attempt in range(max_attempts):
        try:
            message = request()
        except (
            anthropic.APIConnectionError,
            anthropic.RateLimitError,
            anthropic.APIStatusError,
            anthropic.APITimeoutError,
        ) as api_error:
            last_error = f"{type(api_error).__name__}: {api_error}"
            if attempt < max_attempts - 1:
                time.sleep(retry_delay_seconds)
            continue

        raw_output = " ".join(
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
        "error": f"Failed after {max_attempts} attempts.",
        "last_raw_output": last_raw_output,
        "last_api_error": last_error,
    }