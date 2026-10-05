from rag.rag import answer_question
from rag.retrieval import SearchResult


def make_result(
    text: str,
    distance: float,
) -> SearchResult:
    return SearchResult(
        source="test.pdf",
        page_number=1,
        chunk_index=0,
        text=text,
        distance=distance,
    )


def test_no_results_returns_dont_know(monkeypatch):
    def fake_search(embedding, limit):
        return []

    def fake_embed(question):
        return [0.1, 0.2, 0.3]

    monkeypatch.setattr(
        "rag.rag.embed",
        fake_embed,
    )

    result = answer_question(
        "What happened?",
        fake_search,
    )

    assert result == "I don't know based on the provided documents."


def test_all_results_too_far_does_not_generate(monkeypatch):
    generate_calls = []

    def fake_search(embedding, limit):
        return [
            make_result(
                "This is irrelevant context.",
                0.9,
            )
        ]

    def fake_embed(question):
        return [0.1, 0.2, 0.3]

    def fake_generate_answer(question, context):
        generate_calls.append(
            {
                "question": question,
                "context": context,
            }
        )
        return "fake answer"

    monkeypatch.setattr(
        "rag.rag.embed",
        fake_embed,
    )

    monkeypatch.setattr(
        "rag.rag.generate_answer",
        fake_generate_answer,
    )

    result = answer_question(
        "What happened?",
        fake_search,
    )

    assert result == "I don't know based on the provided documents."
    assert generate_calls == []


def test_mixed_distances_only_uses_relevant_results(monkeypatch):
    generate_calls = []

    def fake_search(embedding, limit):
        return [
            make_result(
                "This is relevant context.",
                0.4,
            ),
            make_result(
                "This is irrelevant context.",
                0.9,
            ),
        ]

    def fake_embed(question):
        return [0.1, 0.2, 0.3]

    def fake_generate_answer(question, context):
        generate_calls.append(
            {
                "question": question,
                "context": context,
            }
        )
        return "fake answer"

    monkeypatch.setattr(
        "rag.rag.embed",
        fake_embed,
    )

    monkeypatch.setattr(
        "rag.rag.generate_answer",
        fake_generate_answer,
    )

    result = answer_question(
        "What happened?",
        fake_search,
    )

    assert result == "fake answer"
    assert len(generate_calls) == 1

    context = generate_calls[0]["context"]

    assert "This is relevant context." in context
    assert "This is irrelevant context." not in context