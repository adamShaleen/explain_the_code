import json
from unittest.mock import MagicMock, patch

import pytest
from explainer.bedrock import stream_explanation


@pytest.fixture
def mock_bedrock_client():
    mock_client = MagicMock()
    with patch("explainer.bedrock.boto3.client", return_value=mock_client):
        yield mock_client


def make_chunk(chunk_dict: dict) -> dict:
    return {"chunk": {"bytes": json.dumps(chunk_dict).encode()}}


def test_stream_explanation_prints_output(capsys, mock_bedrock_client):
    mock_events = [
        make_chunk(
            {"type": "message_start", "message": {"usage": {"input_tokens": 10}}}
        ),
        make_chunk({"type": "content_block_delta", "delta": {"text": "Hello "}}),
        make_chunk({"type": "content_block_delta", "delta": {"text": "world"}}),
        make_chunk({"type": "message_delta", "usage": {"output_tokens": 5}}),
    ]

    mock_bedrock_client.invoke_model_with_response_stream.return_value = {
        "body": mock_events
    }

    stream_explanation(code="print('hi')", language="python")

    captured = capsys.readouterr()
    assert "Hello world" in captured.out


def test_stream_explanation_verbose(capsys, mock_bedrock_client):
    mock_events = [
        make_chunk(
            {"type": "message_start", "message": {"usage": {"input_tokens": 100}}}
        ),
        make_chunk({"type": "content_block_delta", "delta": {"text": "Explanation"}}),
        make_chunk({"type": "message_delta", "usage": {"output_tokens": 50}}),
    ]

    mock_bedrock_client.invoke_model_with_response_stream.return_value = {
        "body": mock_events
    }

    stream_explanation(code="print('hi')", language="python", verbose=True)

    captured = capsys.readouterr()
    assert "input: 100" in captured.out
    assert "output: 50" in captured.out
    assert "$" in captured.out
