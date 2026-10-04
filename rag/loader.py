
import io
from dataclasses import dataclass

import boto3
from pypdf import PdfReader

from rag.chunking import chunk_text, clean_text


@dataclass
class Page:
    source: str
    page_number: int
    text: str


@dataclass
class Chunk:
    source: str
    page_number: int
    chunk_index: int
    text: str


s3 = boto3.client("s3")


def list_documents(bucket: str, prefix: str) -> list[str]:
    """Return S3 object keys under the given prefix."""
    paginator = s3.get_paginator("list_objects_v2")
    keys = []

    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if key.lower().endswith(".pdf"):
                keys.append(key)

    return keys


def load_document(bucket: str, key: str) -> list[Page]:
    """Download a PDF from S3 and extract text page by page."""
    response = s3.get_object(Bucket=bucket, Key=key)
    pdf_bytes = response["Body"].read()

    reader = PdfReader(io.BytesIO(pdf_bytes))
    pages = []

    for page_number, pdf_page in enumerate(reader.pages, start=1):
        text = pdf_page.extract_text() or ""
        text = clean_text(text)

        pages.append(
            Page(
                source=key,
                page_number=page_number,
                text=text
            )
        )

    return pages


def chunk_document(
    pages: list[Page],
    chunk_size: int = 2000,
    overlap: int = 200,
) -> list[Chunk]:
    """Split each page into chunks while preserving its source metadata."""
    chunks = []

    for page in pages:
        page_chunks = chunk_text(
            page.text,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        for chunk_index, text in enumerate(page_chunks):
            chunks.append(
                Chunk(
                    source=page.source,
                    page_number=page.page_number,
                    chunk_index=chunk_index,
                    text=text,
                )
            )

    return chunks