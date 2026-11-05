from interpreter import parse_tokens, join_tokens, is_valid_greek_number, interpretations


def label(number):
    return "VALID" if is_valid_greek_number(number) else "INVALID"


def main():
    print("Enter the recognized numbers separated by spaces (empty line to quit).")
    while True:
        try:
            text = input("\nEnter a number: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not text.strip():
            break

        try:
            tokens = parse_tokens(text)
        except ValueError as error:
            print(error)
            continue

        number = join_tokens(tokens)
        print(f"Number: {number}  Phone number: {label(number)}")

        results = interpretations(tokens)
        width = max(len(r) for r in results)
        print(f"\nPossible interpretations ({len(results)}):")
        for i, result in enumerate(results, start=1):
            print(f"  {i:>2}. {result.ljust(width)}  {label(result)}")


if __name__ == "__main__":
    main()
