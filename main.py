from app.graph.graph import build_graph


def main():
    graph = build_graph()

    print("Chatbot Started.")
    print("Type 'exit' to quit\n")

    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        initial_state = {
            "question": question,
            "classification": None,
            "search_results": [],
            "answer": "",
            "error": None,
        }
        try:
            result = graph.invoke(initial_state)
            print(f"\nBot: {result['answer']}\n")
        except Exception as exc:
            print("\nBot: Error Occured")

            print(f"{exc}")


if __name__ == "__main__":
    main()
