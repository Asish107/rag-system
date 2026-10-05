import os

import boto3
import psycopg
from pgvector.psycopg import register_vector

from rag.retrieval import search_chunks

DB_PORT = 5432
DB_NAME = "rag"
DB_USER = "rag_reader"

rds = boto3.client(
    "rds",
    region_name="us-east-1",
)

connection = None


def get_connection():
    global connection

    if connection is not None:
        try:
            connection.execute("SELECT 1")
            return connection
        except psycopg.Error:
            try:
                connection.close()
            except psycopg.Error:
                pass

            connection = None

    db_host = os.environ["DB_HOST"]

    token = rds.generate_db_auth_token(
        DBHostname=db_host,
        Port=DB_PORT,
        DBUsername=DB_USER,
    )

    connection = psycopg.connect(
        host=db_host,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=token,
        sslmode="require",
        autocommit=True,
    )

    register_vector(connection)

    return connection


def handler(event, context):
    embedding = event["embedding"]
    limit = event.get("limit", 5)

    results = search_chunks(
        get_connection(),
        embedding,
        limit=limit,
    )

    return [
        {
            "source": result.source,
            "page": result.page_number,
            "chunk_index": result.chunk_index,
            "text": result.text,
            "distance": result.distance,
        }
        for result in results
    ]