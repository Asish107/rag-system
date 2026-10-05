import base64
import json
import traceback

from rag.rag import answer_question
from rag.remote_search import search_via_lambda


MAX_QUESTION_LENGTH = 1000


def _response(status_code: int, body_dict: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(body_dict),
    }


def handler(event, context):
    body = event.get("body")

    if body is None:
        return _response(
            400,
            {"error": "Request body is required"},
        )

    if event.get("isBase64Encoded") is True:
        try:
            body = base64.b64decode(body).decode("utf-8")
        except (ValueError, UnicodeDecodeError):
            return _response(
                400,
                {"error": "Request body is not valid JSON"},
            )

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return _response(
            400,
            {"error": "Request body is not valid JSON"},
        )

    if not isinstance(data, dict):
        return _response(
            400,
            {"error": "Request body must be a JSON object"},
        )

    question = data.get("question")

    if (
        not isinstance(question, str)
        or not question.strip()
    ):
        return _response(
            400,
            {"error": "Question is required"},
        )

    if len(question) > MAX_QUESTION_LENGTH:
        return _response(
            400,
            {
                "error": (
                    "Question must be 1000 characters or fewer"
                )
            },
        )

    try:
        answer = answer_question(
            question,
            search_via_lambda,
        )
    except Exception as exc:
        print(f"Request failed: {exc}")
        traceback.print_exc()

        return _response(
            500,
            {"error": "Internal error"},
        )

    return _response(
        200,
        {"answer": answer},
    )