import anthropic
from core.llm_json import request_json

def failing_request():
    raise anthropic.APIConnectionError(request=None)

result = request_json(failing_request, max_attempts=3, retry_delay_seconds=0.5)
print(result)