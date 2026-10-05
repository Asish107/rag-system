from rag.rag import answer_question
from rag.remote_search import search_via_lambda


def main():
    question = input("Question: ")

    answer = answer_question(
        question,
        search_via_lambda,
    )

    print("\n" + "=" * 80)
    print("Answer")
    print("=" * 80)
    print(answer)


if __name__ == "__main__":
    main()