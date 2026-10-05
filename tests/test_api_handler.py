import json

import pytest

from rag.handlers.api import handler


@pytest.mark.parametrize(
    "event",
    [
        {},
        {
            "body": "not json",
        },
        {
            "body": "[1,2]",
        },
        {
            "body": json.dumps({}),
        },
        {
            "body": json.dumps({"question": ""}),
        },
        {
            "body": json.dumps({"question": "a" * 5000}),
        },
    ],
)
def test_bad_inputs_return_400(event):
    response = handler(event, None)

    assert response["statusCode"] == 400


def test_valid_question_returns_answer(monkeypatch):
    def fake_answer_question(question, search_fn):
        return "fake answer"

    monkeypatch.setattr(
        "rag.handlers.api.answer_question",
        fake_answer_question,
    )

    response = handler(
        {
            "body": json.dumps(
                {
                    "question": "How much did NVIDIA spend?"
                }
            )
        },
        None,
    )

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {
        "answer": "fake answer"
    }


def test_internal_error_returns_500_without_details(monkeypatch):
    def fake_answer_question(question, search_fn):
        raise RuntimeError("secret internal detail")

    monkeypatch.setattr(
        "rag.handlers.api.answer_question",
        fake_answer_question,
    )

    response = handler(
        {
            "body": json.dumps(
                {
                    "question": "How much did NVIDIA spend?"
                }
            )
        },
        None,
    )

    assert response["statusCode"] == 500
    assert json.loads(response["body"]) == {
        "error": "Internal error"
    }
    assert "secret internal detail" not in response["body"]