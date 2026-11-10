import json
import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic


load_dotenv(override=True)

# Set up them keys
openai_key = os.environ.get("OPENAI_API_KEY")
anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
ollama = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


# Test the keys
if "sk-proj-" not in openai_key:
    raise ValueError("Missing OPENAI_API_KEY environment variable.")
else:
    print("Your OpenAI API key are good to go")
if "sk-ant-" not in anthropic_key:
    raise ValueError("Missing ANTHROPIC_API_KEY environment variable.")
else:
    print("Your Claude API key are good to go")
if not ollama:
    raise ValueError("Missing Ollama client.")
else:
    print("Your Ollama client is good to go")


# Initialize openai and claude clients
openai = OpenAI(api_key=openai_key)
claude = Anthropic(api_key=anthropic_key)


# OpenAI function caller
def ask_openAI(system, user):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages = [{"role": "system", "content": system},
            {"role": "user", "content": user}
            ]
    )

    return response.choices[0].message.content


# Anthropic (claude) function caller
def ask_claude(system, user):
    response = claude.messages.create(
        model="claude-haiku-5-5",
        max_tokens=1024,
        system=system,
        messages=[
            {"role": "user", "content": user}
        ]
    )

    text_blocks = []

    for block in response.content:
        text = getattr(block, "text", None)

        if isinstance(text, str):
            text_blocks.append(text)

    return "\n".join(text_blocks)


# Ollama function caller
def ask_ollama(system, user):
    response = ollama.chat.completions.create(
        model="llama3.2:latest",
        messages = [{"role": "system", "content": system},
            {"role": "user", "content": user}
            ]
    )

    return response.choices[0].message.content


# Fix all three models in a dictionary, can add more above if necessary
models = {
    "gpt": ask_openAI,
    "claude": ask_claude,
    "ollama": ask_ollama
}