import argparse
import sys


def process_data(name: str, count: int, verbose: bool = False) -> int:
    """Process data with given parameters"""
    print(f"Processing data for: {name}")
    print(f"Item count: {count}")

    # Demonstrate loops and conditionals
    total = 0
    for i in range(count):
        total += i
        if verbose and i % 5 == 0:
            print(f"  Processed item {i}")

    # While loop example
    counter = count
    while counter > 0:
        counter -= 1

    print(f"Total sum: {total}")
    return total


def main() -> None:
    # Method 1: Simple sys.argv
    print("Command line arguments:", sys.argv)

    # Method 2: Using argparse (recommended)
    parser = argparse.ArgumentParser(description="Data Analyzer CLI")
    parser.add_argument("name", help="Name for processing")
    parser.add_argument("count", type=int, help="Number of items to process")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args()

    print("\n=== Data analyser ===")
    result = process_data(args.name, args.count, args.verbose)
    print(f"Final result: {result}")


if __name__ == "__main__":
    main()
