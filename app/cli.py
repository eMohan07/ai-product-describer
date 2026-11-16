"""Command-line entry point: `python -m app.cli --help`."""
import argparse
from app.core import milestone_1


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="ai-product-describer",
        description="Small business owners use a CLI tool to generate creative product descriptions for their inventory by training a custom GPT on examples of existing product texts."
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("hello", help="check that everything is wired up")
    
    # Milestone 1: Collect & clean product corpus
    collect_parser = sub.add_parser("collect", help="collect and clean product descriptions for milestone 1")
    collect_parser.add_argument("--category", default="Handcrafted Leather Goods", help="product category to collect")
    collect_parser.add_argument("--show-sample", action="store_true", help="display a sample cleaned description")

    args = parser.parse_args(argv)
    if args.command == "hello":
        print("AI Product Describer is ready. Open README.md for your milestones.")
    elif args.command == "collect":
        result = milestone_1(category=args.category)
        print(f"=== Milestone 1: Data Collection & Text Cleaning ===")
        print(f"Category: {result['category']}")
        print(f"Total Products Collected: {result['count']}")
        print(f"Total Words: {result['total_words']}")
        print("Corpus successfully cleaned and saved to store.")
        if args.show_sample or True:
            sample = result["sample"]
            print(f"\n--- Sample Product: {sample['name']} ---")
            print(f"Cleaned Description:\n{sample['cleaned_description']}")


if __name__ == "__main__":
    main()
