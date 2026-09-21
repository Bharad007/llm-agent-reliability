import os
import anthropic 
from dotenv import load_dotenv
load_dotenv()   
api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(
    api_key=api_key
)

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=100,
    messages=[{
        "role": "user", "content": "Hello, World!"
    }],
)

print(message.content)
print(message.stop_reason)