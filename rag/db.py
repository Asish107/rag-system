import json
import os

import boto3
import psycopg
from pgvector.psycopg import register_vector

from rag.loader import Chunk


def get_connection():
    """Create a PostgreSQL connection using a password from Secrets Manager."""
    endpoint = os.environ["DB_ENDPOINT"]
    secret_arn = os.environ["DB_SECRET_ARN"]

    secretsmanager = boto3.client("secretsmanager")

    response = secretsmanager.get_secret_value(
        SecretId=secret_arn
    )

    secret = json.loads(response["SecretString"])
    password = secret["password"]

    connection = psycopg.connect(
        host=endpoint,
        port=5432,
        dbname="rag",
        user="rag",
        password=password,
        sslmode="require",
    )

    register_vector(connection)

    return connection


def upsert_chunks(
    connection,
    chunks: list[Chunk],
    embeddings: list[list[float]],
) -> None:
    """Insert or update all chunks for one document."""
    query = """
        INSERT INTO chunks (
            source,
            page_number,
            chunk_index,
            text,
            embedding
        )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (source, page_number, chunk_index)
        DO UPDATE SET
            text = EXCLUDED.text,
            embedding = EXCLUDED.embedding,
            created_at = now()
    """

    rows = [
        (
            chunk.source,
            chunk.page_number,
            chunk.chunk_index,
            chunk.text,
            embedding,
        )
        for chunk, embedding in zip(chunks, embeddings, strict=True)
    ]

    with connection.cursor() as cursor:
        cursor.executemany(query, rows)