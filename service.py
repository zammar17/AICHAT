from json import load
import os
from openai import OpenAI
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(base_dir, ".env")

load_dotenv(dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print(f"DEBUG: Looking for .env at {dotenv_path}")
    print(f"DEBUG: Current directory: {os.getcwd()}")
    raise ValueError("OPENAI_API_KEY is not set in .env file!")

client = OpenAI(api_key=api_key)

#pricing rates per token for GPT-4omini
INPUT_RATE = 0.80 / 1_000_000  
OUTPUT_RATE = 3.20 / 1_000_000  

def get_openai_response(messages, temperature=0.7, max_tokens=500):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )

    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens

    cost = (prompt_tokens * INPUT_RATE) + (completion_tokens * OUTPUT_RATE)

    return {
        "content": response.choices[0].message.content,
        "tokens": prompt_tokens + completion_tokens,
        "cost": cost
    }
