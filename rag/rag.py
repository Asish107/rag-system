import os

from rag.embeddings import embed
from rag.generate import generate_answer

MAX_DISTANCE = float(
    os.getenv("RETRIEVAL_MAX_DISTANCE", "0.70")
)


def answer_question(
    question: str,
    search_fn,
    limit: int = 5,
) -> str:
    query_embedding = embed(question)

    results = search_fn(query_embedding, limit)

    if not results:
        return "I don't know based on the provided documents."

    if results[0].distance > MAX_DISTANCE:
        return "I don't know based on the provided documents."

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