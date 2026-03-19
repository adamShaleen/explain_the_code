# explain_the_code

A terminal-based CLI tool that reads source code from a file or stdin and streams an explanation back using Amazon Bedrock (Claude Haiku).

## Requirements

- Python 3.11+
- AWS credentials configured (`aws configure` or environment variables)
- Bedrock access in `us-east-1`

## Setup

**1. Create the venv and install dependencies:**

```bash
cd /path/to/explain_the_code
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

**2. Add a shell function to `~/.zshrc` (or `~/.bashrc`):**

```bash
explain() {
  source /path/to/explain_the_code/venv/bin/activate
  python /path/to/explain_the_code/explain.py "$@"
  deactivate
}
```

Replace `/path/to/explain_the_code` with the actual path on your machine. Then reload your shell:

```bash
source ~/.zshrc
```

**3. Request Bedrock model access:**

In the AWS console, go to **Bedrock → Model access** and request access to Anthropic Claude Haiku.

## Usage

After setup, run `explain` from anywhere — no venv activation needed.

```bash
# Explain a file
explain path/to/file.py

# Pipe via stdin
cat myfile.py | explain

# Ask a specific question
explain path/to/file.py --question "What does the main function do?"

# Override the language hint
explain path/to/file.py --language rust

# Show token usage and estimated cost
explain path/to/file.py --verbose
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
