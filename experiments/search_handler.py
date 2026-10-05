from rag.embeddings import embed
from rag.handlers.search import handler


def main():
    question = "How much did NVIDIA spend on research and development?"

    vector = embed(question)

    results = handler(
        {
            "embedding": vector,
            "limit": 3,
        },
        None,
    )

    for result in results:
        print("=" * 80)
        print(f"Source: {result['source']}")
        print(f"Page: {result['page']}")
        print(f"Chunk: {result['chunk_index']}")
        print(f"Distance: {result['distance']}")
        print(result["text"])


if __name__ == "__main__":
    main()