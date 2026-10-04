import os

from rag.db import get_connection
from rag.embeddings import embed
from rag.generate import generate_answer
from rag.retrieval import search_chunks


MAX_DISTANCE = float(
    os.getenv("RETRIEVAL_MAX_DISTANCE", "0.70")
)


def answer_question(
    question: str,
    limit: int = 5,
) -> str:
    query_embedding = embed(question)

    with get_connection() as connection:
        results = search_chunks(
            connection,
            query_embedding,
            limit=limit,
        )

    if not results:
        return "I don't know based on the provided documents."

    # The results are ordered by distance, so the first result
    # is the most similar chunk.
    if results[0].distance > MAX_DISTANCE:
        return "I don't know based on the provided documents."

    # Only pass chunks that meet the relevance threshold to Claude.
    relevant_results = [
        result
        for result in results
        if result.distance <= MAX_DISTANCE
    ]

    context_parts = []

    for i, result in enumerate(relevant_results, start=1):
        context_parts.append(
            f"""
[Context {i}]
Source: {result.source}
Page: {result.page_number}
Chunk: {result.chunk_index}

{result.text}
""".strip()
        )

    context = "\n\n".join(context_parts)

    return generate_answer(
        question=question,
        context=context,
    )