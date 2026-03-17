import sys
from pathlib import Path
from explainer.cli import build_parser
from explainer.bedrock import stream_explanation


LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".rs": "rust",
    ".go": "go",
    ".java": "java",
    ".rb": "ruby",
    ".sh": "bash",
    ".c": "c",
    ".cpp": "cpp",
}


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"Error: file not found: {args.file}")
            raise SystemExit(1)
        code = path.read_text()
        language = args.language or LANGUAGE_MAP.get(path.suffix, "")
    else:
        if sys.stdin.isatty():
            print(
                "Usage: explain.py <file> [--question ...] [--language ...], [--verboase]"
            )
            raise SystemExit(1)
        code = sys.stdin.read()
        language = args.language or ""

    stream_explanation(
        code=code, language=language, question=args.question, verbose=args.verbose
    )


if __name__ == "__main__":
    main()
