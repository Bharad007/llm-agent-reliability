import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

def ispalindrome(s: str) -> bool:
    s = s.lower()
    return s == s[::-1]

client = anthropic.Anthropic(
    api_key=api_key
    )
tools = [
    {
        "name" : "ispalindrome",
        "description" : "Checks if a string is a palindrome.",
        "input_schema" : {
            "type" : "object",
            "properties" : {
                "s" : {"type" : "string", "description" : "The string to check."}
            },
            "required" : ["s"]
        }
    }
]

messages = [{"role" : "user", "content" : "Is 'Bhargav' a palindrome?" }]

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=100,
    messages=messages,
    tools=tools
)

if response.stop_reason == "tool_use":
    tool_use = next(block for block in response.content if block.type == "tool_use")
    print(tool_use.model_dump_json(indent=2))

    messages.append({"role" : "assistant", "content" : response.content})

    tool_name = tool_use.name
    tool_input = tool_use.input

    if tool_name == "ispalindrome":
        result = ispalindrome(tool_input["s"])
        print(f"Result : {result}")

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
