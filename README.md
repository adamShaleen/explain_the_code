# explain_the_code

A terminal-based CLI tool that reads source code from a file or stdin and streams an explanation back using Amazon Bedrock (Claude Haiku).

## Requirements

- Python 3.11+
- AWS credentials configured (`aws configure` or environment variables)
- Bedrock access in `us-east-1`

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
# Explain a file
python3 explain.py path/to/file.py

# Pipe via stdin
cat myfile.py | python3 explain.py

# Ask a specific question
python3 explain.py path/to/file.py --question "What does the main function do?"

# Override the language hint
python3 explain.py path/to/file.py --language rust

# Show token usage and estimated cost
python3 explain.py path/to/file.py --verbose
```

## Project structure

```
explain_the_code/
├── explain.py          # entrypoint
├── requirements.txt
└── explainer/
    ├── bedrock.py      # Bedrock client and streaming logic
    ├── cli.py          # argparse setup
    └── prompt.py       # prompt construction
```

## Running tests

```bash
python3 -m pytest
```
