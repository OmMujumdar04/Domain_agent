from app.graph import graph


def main():
    while True:
        text = input("\nEnter a domain (or 'q' to quit): ").strip()
        if text.lower() in ("q", "quit", "exit"):
            break
        if not text:
            continue

        result = graph.invoke({"raw_input": text})
        print(result["answer"])


if __name__ == "__main__":
    main()