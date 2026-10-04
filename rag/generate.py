import json
import os

import boto3
from openai import OpenAI


SECRET_NAME = "rag/openrouter-api-key"

secretsmanager = boto3.client(
    "secretsmanager",
    region_name="us-east-1",
)


def get_openrouter_api_key() -> str:
    response = secretsmanager.get_secret_value(
        SecretId=SECRET_NAME,
    )

    secret_string = response["SecretString"]

    # Supports either a raw API key or {"api_key": "..."}.
    try:
        secret = json.loads(secret_string)
        if isinstance(secret, dict) and "api_key" in secret:
            return secret["api_key"]
    except json.JSONDecodeError:
        pass

    return secret_string


OPENROUTER_API_KEY = get_openrouter_api_key()

CLAUDE_MODEL_ID = os.environ["CLAUDE_MODEL_ID"]

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


def generate_answer(question: str, context: str) -> str:
    prompt = f"""
You are answering questions using only the supplied document context.

Rules:
- Use only the information in the context.
- Do not use outside knowledge.
- If the context does not contain enough information to answer, say:
  "I don't know based on the provided documents."
- Do not invent facts or citations.
- Cite factual claims using the source and page provided in the context.
- Keep the answer concise.

Question:
{question}

Document context:
{context}
"""

    response = client.chat.completions.create(
        model=CLAUDE_MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=1000,
    )

    if not response.choices:
        raise RuntimeError(
            f"OpenRouter returned no choices: {response}"
        )

    choice = response.choices[0]

    if choice.finish_reason == "length":
        raise RuntimeError(
            "OpenRouter response was truncated because it reached max_tokens."
        )

    if choice.finish_reason == "content_filter":
        raise RuntimeError(
            "OpenRouter response was blocked by a content filter."
        )

    if not choice.message.content:
        raise RuntimeError(
            f"OpenRouter returned an empty response: {response}"
        )

    return choice.message.content