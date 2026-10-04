from rag.rag import answer_question


def main():
    question = input("Question: ")

    answer = answer_question(question)

    print("\n" + "=" * 80)
    print("Answer")
    print("=" * 80)
    print(answer)


if __name__ == "__main__":
    main()