from dataclasses import dataclass


@dataclass
class SearchResult:
    source: str
    page_number: int
    chunk_index: int
    text: str
    distance: float


def search_chunks(
    connection,
    query_embedding: list[float],
    limit: int = 5,
) -> list[SearchResult]:
    """Return the most similar chunks for an embedding."""

    query = """
        SELECT
            source,
            page_number,
            chunk_index,
            text,
            embedding <=> %s::vector AS distance
        FROM chunks
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """

    with connection.cursor() as cursor:
        cursor.execute(
            query,
            (query_embedding, query_embedding, limit),
        )

        rows = cursor.fetchall()

    return [
        SearchResult(
            source=row[0],
            page_number=row[1],
            chunk_index=row[2],
            text=row[3],
            distance=float(row[4]),
        )
        for row in rows
    ]
