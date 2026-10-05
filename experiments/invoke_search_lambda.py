import json

import boto3

from rag.embeddings import embed


def main():
    question = "How much did NVIDIA spend on research and development?"

    print("Generating query embedding...")
    vector = embed(question)

    print("Invoking deployed Lambda...")
    client = boto3.client("lambda", region_name="us-east-1")

    response = client.invoke(
        FunctionName="rag-search",
        InvocationType="RequestResponse",
        Payload=json.dumps({
            "embedding": vector,
            "limit": 3,
        }).encode("utf-8"),
    )

    payload_text = response["Payload"].read().decode("utf-8")

    if response.get("FunctionError"):
        print("Lambda execution failed:")
        print(payload_text)
        raise RuntimeError(
            f"Lambda failed: {response['FunctionError']}"
        )

    results = json.loads(payload_text)

    if not isinstance(results, list):
        raise RuntimeError(f"Unexpected Lambda response: {results}")

    for result in results:
        print("=" * 60)
        print(f"Source:   {result['source']}")
        print(f"Page:     {result['page']}")
        print(f"Chunk:    {result['chunk_index']}")
        print(f"Distance: {result['distance']:.4f}")
        print(result["text"][:500])


if __name__ == "__main__":
    main()