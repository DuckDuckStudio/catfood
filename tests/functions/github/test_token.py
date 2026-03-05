import pytest

from catfood.functions.github.token import read_token, 这是谁的Token


def test_read_token():
    with pytest.deprecated_call():
        assert read_token() is None # pyright: ignore[reportDeprecated]

def test_这是谁的Token():
    with pytest.deprecated_call():
        assert 这是谁的Token(None) is None # pyright: ignore[reportDeprecated]
        assert 这是谁的Token(read_token()) is None # pyright: ignore[reportDeprecated]
