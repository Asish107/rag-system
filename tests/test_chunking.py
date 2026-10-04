import pytest

from rag.chunking import chunk_text, clean_text



def test_alphabet_example():
    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    result = chunk_text(text, chunk_size=10, overlap=3)

    assert result == [
        "ABCDEFGHIJ",
        "HIJKLMNOPQ",
        "OPQRSTUVWX",
        "VWXYZ",
    ]


def test_empty_text_returns_empty_list():
    assert chunk_text("", chunk_size=10, overlap=3) == []


def test_short_text_returns_one_chunk():
    text = "Hello"

    assert chunk_text(text, chunk_size=10, overlap=3) == ["Hello"]


def test_zero_overlap():
    text = "ABCDEFGHIJ"

    assert chunk_text(text, chunk_size=5, overlap=0) == [
        "ABCDE",
        "FGHIJ",
    ]


def test_zero_chunk_size_raises():
    with pytest.raises(ValueError, match="chunk_size"):
        chunk_text("hello", chunk_size=0, overlap=0)

def test_negative_chunk_size_raises():
    with pytest.raises(ValueError, match="chunk_size"):
        chunk_text("hello", chunk_size=-1, overlap=0)


def test_negative_overlap_raises():
    with pytest.raises(ValueError, match="overlap"):
        chunk_text("hello", chunk_size=5, overlap=-1)


def test_overlap_equal_to_chunk_size_raises():
    with pytest.raises(ValueError, match="overlap"):
        chunk_text("hello", chunk_size=5, overlap=5)


def test_overlap_greater_than_chunk_size_raises():
    with pytest.raises(ValueError, match="overlap"):
        chunk_text("hello", chunk_size=5, overlap=6)


def test_no_redundant_tail_chunk():
    text = "ABCDEFGHIJKLMNOPQ"

    result = chunk_text(text, chunk_size=10, overlap=3)

    assert result == [
        "ABCDEFGHIJ",
        "HIJKLMNOPQ",
    ]

def test_clean_text_replaces_nbsp_and_collapses_spaces():
    text = "Yes\xa0\xa0☒\xa0\xa0No"

    result = clean_text(text)

    assert result == "Yes ☒ No"

def test_clean_text_strips_outer_whitespace():
    text = "   Hello   world   "

    result = clean_text(text)

    assert result == "Hello world"