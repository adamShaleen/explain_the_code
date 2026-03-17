import pytest
from unittest.mock import patch


def test_file_not_found(tmp_path):
    with patch("sys.argv", ["explain.py", "nonexistent.py"]):
        from explain import main

        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 1


def test_stdin_tty_exits(monkeypatch):
    monkeypatch.setattr("sys.stdin.isatty", lambda: True)
    with patch("sys.argv", ["explain.py"]):
        from explain import main

        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 1


def test_file_input_calls_stream(tmp_path):
    code_file = tmp_path / "sample.py"
    code_file.write_text("print('hello')")

    with patch("sys.argv", ["explain.py", str(code_file)]):
        with patch("explain.stream_explanation") as mock_stream:
            from explain import main

            main()
            mock_stream.assert_called_once_with(
                code="print('hello')",
                language="python",
                question=None,
                verbose=False,
            )
