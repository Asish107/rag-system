from rag.loader import Page, chunk_document


def test_chunk_document_preserves_metadata_and_skips_empty_pages():
    pages = [
        Page(
            source="report_a.pdf",
            page_number=1,
            text="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ),
        Page(
            source="report_a.pdf",
            page_number=2,
            text="   "
        ),
        Page(
            source="report_a.pdf",
            page_number=3,
            text="1234567890"
        ),
    ]

    chunks = chunk_document(
        pages,
        chunk_size=10,
        overlap=0,
    )

    assert len(chunks) == 4

    assert chunks[0].source == "report_a.pdf"
    assert chunks[0].page_number == 1
    assert chunks[0].chunk_index == 0
    assert chunks[0].text == "ABCDEFGHIJ"

    assert chunks[1].source == "report_a.pdf"
    assert chunks[1].page_number == 1
    assert chunks[1].chunk_index == 1
    assert chunks[1].text == "KLMNOPQRST"

    assert chunks[2].source == "report_a.pdf"
    assert chunks[2].page_number == 1
    assert chunks[2].chunk_index == 2
    assert chunks[2].text == "UVWXYZ"

    assert chunks[3].source == "report_a.pdf"
    assert chunks[3].page_number == 3
    assert chunks[3].chunk_index == 0
    assert chunks[3].text == "1234567890"