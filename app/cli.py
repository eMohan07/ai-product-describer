"""Command-line entry point: `python -m app.cli --help`."""
import argparse
from app.core import milestone_1, milestone_2


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

    # Milestone 2: Byte-pair tokenizer & embeddings
    embed_parser = sub.add_parser("embed", help="train byte-pair tokenizer and generate embeddings (milestone 2)")
    embed_parser.add_argument("--vocab-size", type=int, default=350, help="target BPE vocabulary size")
    embed_parser.add_argument("--embed-dim", type=int, default=64, help="embedding dimension")

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
    elif args.command == "embed":
        result = milestone_2(vocab_size=args.vocab_size, embed_dim=args.embed_dim)
        print("=== Milestone 2: Byte-Pair Tokenizer & Embeddings ===")
        print(f"BPE Vocabulary Size: {result['vocab_size']}")
        print(f"Merges Learned: {result['num_merges']}")
        print(f"Embedding Dimension: {result['embedding_layer'].embed_dim}")
        print(f"Sample Tokens Count: {len(result['sample_tokens'])}")
        print(f"Token Compression Ratio: {result['compression_ratio']}x")
        print(f"Input Tensor Shape: {result['input_tensor_shape']}")
        print(f"Generated Embeddings Shape: {result['embeddings_shape']}")
        print(f"\n--- Sample Token IDs (First 15) ---")
        print(result['sample_tokens'][:15])
        print(f"\nRound-trip Lossless Verification: {result['decoded_text'] == result['sample_text']}")


if __name__ == "__main__":
    main()
