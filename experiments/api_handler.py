import json

from rag.handlers.api import handler


def run_test(name, event):
    response = handler(event, None)

    print("=" * 80)
    print(name)
    print(f"Status: {response['statusCode']}")
    print(f"Body: {response['body']}")


def main():
    run_test(
        "Valid NVIDIA question",
        {
            "body": json.dumps(
                {
                    "question": (
                        "How much did NVIDIA spend on "
                        "research and development?"
                    )
                }
            )
        },
    )

    run_test(
        "Out-of-domain question",
        {
            "body": json.dumps(
                {
                    "question": "What's your name?"
                }
            )
        },
    )

    run_test(
        "Missing question",
        {
            "body": json.dumps({})
        },
    )

    run_test(
        "Invalid JSON",
        {
            "body": "not json at all"
        },
    )

    run_test(
        "Question too long",
        {
            "body": json.dumps(
                {
                    "question": "a" * 5000
                }
            )
        },
    )

    run_test(
        "JSON array instead of object",
        {
            "body": "[1,2]"
        },
    )

    run_test(
        "JSON string instead of object",
        {
            "body": '"hello"'
        },
    )


if __name__ == "__main__":
    main()