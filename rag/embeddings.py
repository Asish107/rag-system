import json

import boto3

# Create the client once when the module is loaded.
bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")

EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"


def embed(text: str) -> list[float]:
    """Generate an embedding vector for the supplied text."""
    response = bedrock_runtime.invoke_model(
        modelId=EMBEDDING_MODEL_ID,
        body=json.dumps({"inputText": text}),
        contentType="application/json",
        accept="application/json",
    )

    result = json.loads(response["body"].read())
    return result["embedding"]

