import pytest
import os
from src.decorators import log


def test_log_to_console(capsys: pytest.CaptureFixture) -> None:
    @log()
    def example_function(x: int, y: int) -> int:
        return x + y

    result = example_function(1, 2)
    captured = capsys.readouterr()
    assert "example_function ok. Result: 3" in captured.err
    assert result == 3


def test_log_to_file() -> None:
    filename: str = "test_log.txt"

    @log(filename=filename)
    def example_function(x: int, y: int) -> int:
        return x * y

    result = example_function(3, 4)
    assert result == 12
    with open(filename, "r") as f:
        log_content = f.read()
    assert "example_function ok. Result: 12" in log_content
    os.remove(filename)


def test_log_error(capsys: pytest.CaptureFixture) -> None:
    @log()
    def example_function(x: int, y: int) -> None:
        raise ValueError("Test error")

    with pytest.raises(ValueError, match="Test error"):
        example_function(1, 2)
    captured = capsys.readouterr()
    assert "example_function error: ValueError. Inputs: (1, 2), {}" in captured.err
