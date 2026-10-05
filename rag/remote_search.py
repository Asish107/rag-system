import json
import os

import boto3

from rag.retrieval import SearchResult

lambda_client = boto3.client(
    "lambda",
    region_name="us-east-1",
)


def search_via_lambda(
    embedding: list[float],
    limit: int,
) -> list[SearchResult]:
    search_function_name = os.environ["SEARCH_FUNCTION_NAME"]

    response = lambda_client.invoke(
        FunctionName=search_function_name,
        InvocationType="RequestResponse",
        Payload=json.dumps(
            {
                "embedding": embedding,
                "limit": limit,
            }
        ).encode("utf-8"),
    )

    payload_text = response["Payload"].read().decode("utf-8")

    if response.get("FunctionError"):
        raise RuntimeError(
            f"Search Lambda failed: {payload_text}"
        )

    results = json.loads(payload_text)

    if not isinstance(results, list):
        raise RuntimeError(
            f"Unexpected search Lambda response: {results}"
        )

    return [
        SearchResult(
            source=result["source"],
            page_number=result["page"],
            chunk_index=result["chunk_index"],
            text=result["text"],
            distance=float(result["distance"]),
        )
        for result in results
    ]