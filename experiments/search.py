from rag.db import get_connection
from rag.embeddings import embed
from rag.retrieval import search_chunks


def main():
    question = input("Question: ")

    query_embedding = embed(question)

    with get_connection() as connection:
        results = search_chunks(
            connection,
            query_embedding,
            limit=5,
        )

    print(f"\nFound {len(results)} relevant chunks:\n")

    for i, result in enumerate(results, start=1):
        print("=" * 80)
        print(f"Result {i}")
        print(f"Distance: {result.distance:.4f}")
        print(f"Source: {result.source}")
        print(f"Page: {result.page_number}")
        print(f"Chunk: {result.chunk_index}")
        print()
        print(result.text)


if __name__ == "__main__":
    main()
