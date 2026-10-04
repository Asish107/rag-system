from rag.db import get_connection, upsert_chunks
from rag.embeddings import embed
from rag.loader import chunk_document, list_documents, load_document


BUCKET = "rag-system-docs-10ks"
PREFIX = "raw/"


def main():
    keys = list_documents(BUCKET, PREFIX)

    print(f"Found {len(keys)} documents")

    for document_number, key in enumerate(keys, start=1):
        print(f"\n[{document_number}/{len(keys)}] {key}")

        pages = load_document(BUCKET, key)
        print(f"      {len(pages)} pages")

        chunks = chunk_document(pages)
        print(f"      {len(chunks)} chunks")

        embeddings = [
            embed(chunk.text)
            for chunk in chunks
        ]
        print(f"      embedded: {len(embeddings)}")

        with get_connection() as connection:
            upsert_chunks(connection, chunks, embeddings)

        print(f"      stored: {len(chunks)}")


if __name__ == "__main__":
    main()