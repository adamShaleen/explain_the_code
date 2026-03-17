import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Explain source code using Amazon Bedrock."
    )

    parser.add_argument(
        "file", nargs="?", help="Path to the source file (omit to read from stdin)"
    )

    parser.add_argument(
        "--question", "-q", help="Ask a specific question about the code"
    )

    parser.add_argument(
        "--language",
        "-l",
        help="Override the language hint (e.g. python, rust, javascript, go)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print token usage and estimated cost after response",
    )

    return parser
