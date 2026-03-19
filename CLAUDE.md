# explain_the_code

A terminal-based CLI tool that reads source code from a file or stdin and streams an explanation back using Amazon Bedrock (Claude Haiku). No UI, no hosting, no infrastructure — just a Python script and AWS credentials.

## Tech stack

- Python 3.11+
- boto3 (AWS SDK — Bedrock runtime)
- argparse (CLI argument parsing)
- rich (terminal output formatting)
- AWS Bedrock — model: `anthropic.claude-haiku-4-5-20251001`

## Communication style

- Be terse. Omit filler words, preamble, and sign-off phrases.
- No "Great question!", "Certainly!", or similar openers.
- Drop articles and pleasantries where meaning is preserved ("Add error handling" not "You should add error handling here").
- Bullet points over prose for multi-part answers.
- If something is wrong, say what and why — skip the apology.

## Project structure

```
explain-code/
├── CLAUDE.md
├── README.md
├── requirements.txt
├── explain.py        # main entrypoint
└── explainer/
    ├── __init__.py
    ├── bedrock.py    # Bedrock client and streaming logic
    ├── prompt.py     # prompt construction
    └── cli.py        # argparse setup and entry point wiring
```

## Common commands

```bash
# One-time setup: create venv and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

# Run with a file (via shell function — see README setup)
explain path/to/file.py

# Run via stdin (pipe)
cat myfile.py | explain

# Ask a specific question about the code
explain path/to/file.py --question "What does the main function do?"

# Override the language hint
explain path/to/file.py --language rust

# Show token usage and estimated cost after response
explain path/to/file.py --verbose
```

## Coding standards

- Use type hints on all function signatures
- Prefer `pathlib.Path` over `os.path`
- Stream tokens to stdout using `print(..., end="", flush=True)` — do not buffer the full response
- Handle both file path and stdin input gracefully; if no file is given, read from stdin
- Auto-detect language from file extension when `--language` is not provided
- Never hardcode AWS credentials; rely on the standard boto3 credential chain (env vars, ~/.aws/credentials, IAM role)
- Keep prompt construction in `prompt.py` — do not inline prompts in `bedrock.py`

## Bedrock streaming pattern

Use `invoke_model_with_response_stream`. Parse `content_block_delta` events from the response stream. Extract `delta.text` and print immediately. Do not collect the full response before printing.

```python
for event in response["body"]:
    chunk = json.loads(event["chunk"]["bytes"])
    if chunk["type"] == "content_block_delta":
        print(chunk["delta"]["text"], end="", flush=True)
```

## Error handling

- If the file path does not exist, print a clear error and exit with code 1
- If stdin is a TTY and no file is provided, print usage hint and exit
- Wrap Bedrock calls in try/except for `botocore.exceptions.ClientError` and surface the error message clearly
- If `--verbose` is set, print token counts and a cost estimate after the response (input: $0.00025/1K tokens, output: $0.00125/1K tokens for Claude Haiku)

## What NOT to do

- Do not add a web server, REST API, or any hosted component
- Do not persist conversation history between invocations — each run is stateless
- Do not use LangChain or any LLM framework — raw boto3 only
- Do not add a config file or `.env` — AWS credentials come from the environment
