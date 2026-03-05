import sys

import pytest

from catfood.functions.files import open_file


def test_open_file_not_supported(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(sys, "platform", "darwin")
    assert open_file(__file__) == 1

def test_open_file_not_exists():
    assert open_file("abc") == 1
