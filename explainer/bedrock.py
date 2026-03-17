import json
import boto3
from botocore.exceptions import ClientError
from explainer.prompt import build_prompt


def stream_explanation(
    code: str, language: str, question: str | None = None, verbose: bool = False
) -> None:
    prompt = build_prompt(code, language, question)
    client = boto3.client("bedrock-runtime")

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}],
        }
    )

    try:
        response = client.invoke_model_with_response_stream(
            modelId="us.anthropic.claude-haiku-4-5-20251001-v1:0", body=body
        )
    except ClientError as e:
        print(f"Bedrock error: {e.response['Error']['Message']}")
        raise SystemExit(1)

    input_tokens = 0
    output_tokens = 0

    for event in response["body"]:
        chunk = json.loads(event["chunk"]["bytes"])

        if chunk["type"] == "content_block_delta":
            print(chunk["delta"]["text"], end="", flush=True)

        elif chunk["type"] == "message_delta":
            output_tokens = chunk.get("usage", {}).get("output_tokens", 0)

        elif chunk["type"] == "message_start":
            input_tokens = (
                chunk.get("message", {}).get("usage", {}).get("input_tokens", 0)
            )

    print()  # newline after streaming ends

    if verbose:
        input_cost = (input_tokens / 1000) * 0.00025
        output_cost = (output_tokens / 1000) * 0.00125
        print(f"\n[tokens] input: {input_tokens}, output: {output_tokens}")
        print(f"[cost]   ${input_cost + output_cost:.6f}")
