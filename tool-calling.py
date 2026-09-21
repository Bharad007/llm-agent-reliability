import os
import anthropic
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")


def add_numbers(a: int, b: int) -> int:
    """
    Adds two numbers together.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of the two numbers.
    """
    return a + b

client = anthropic.Anthropic(
    api_key=api_key
)

tools = [
    {
        "name": "add_numbers",
        "description": "Adds two numbers together.",
        "input_schema": {
            "type": "object",
            "properties": {
                "a": {"type": "integer", "description": "The first number."},
                "b": {"type": "integer", "description": "The second number."}
            },
            "required": ["a", "b"]
        }
    }
]

messages = [{"role": "user", "content": "What is 2023 + 1978?"}]

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=100,
    messages=messages,
    tools=tools
)

if response.stop_reason == "tool_use":
    tool_use = next(block for block in response.content if block.type == "tool_use")
    print(tool_use.model_dump_json(indent=2))

    messages.append({"role": "assistant", "content": response.content})

    tool_name = tool_use.name
    tool_input = tool_use.input

    if tool_name == "add_numbers":
        result = add_numbers(tool_input["a"], tool_input["b"])
        print(f"Local function executed. Result: {result}")

        tool_result_message = {
            "role" : "user",
            "content" : [
                {
                    "type" : "tool_result",
                    "tool_use_id" : tool_use.id,
                    "content" : str(result)
                }
            ]
        }

        messages.append(tool_result_message)

        final_response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=100,
            messages=messages,
            tools=tools
        )

        print(final_response.content[0].text)