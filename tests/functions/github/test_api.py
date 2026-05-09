from typing import NoReturn
from unittest.mock import MagicMock

import pytest

import catfood.functions.github.api


def raise_exc(**kwargs) -> NoReturn: # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
    raise Exception("测试异常")

def test_获取GitHub文件内容_success(monkeypatch: pytest.MonkeyPatch):
    mock_response: dict[str, str] = {"content": "aGVsbG8gd29ybGQ="}
    monkeypatch.setattr(catfood.functions.github.api, "请求GitHubAPI", lambda api, token: mock_response) # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]
    assert catfood.functions.github.api.获取GitHub文件内容("owner/repo", "README.md", token="abc") == "hello world"

def test_获取GitHub文件内容_invalid_repo():
    assert catfood.functions.github.api.获取GitHub文件内容("invalidrepo", "README.md") is None

def test_获取GitHub文件内容_no_response(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(catfood.functions.github.api, "请求GitHubAPI", lambda api, token: None) # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]
    assert catfood.functions.github.api.获取GitHub文件内容("owner/repo", "README.md") is None

def test_获取GitHub文件内容_exception(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(catfood.functions.github.api, "请求GitHubAPI", raise_exc) # pyright: ignore[reportUnknownArgumentType]
    assert catfood.functions.github.api.获取GitHub文件内容("owner/repo", "README.md") is None

def test_请求GitHubAPI_success(monkeypatch: pytest.MonkeyPatch):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"呐": "吸铁石"}
    mock_resp.raise_for_status.return_value = None
    monkeypatch.setattr(catfood.functions.github.api.requests, "request", lambda **kwargs: mock_resp) # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]
    assert catfood.functions.github.api.请求GitHubAPI("http://api.github.com/", token="abc") == {"呐": "吸铁石"}

def test_请求GitHubAPI_raises(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(catfood.functions.github.api.requests, "request", raise_exc) # pyright: ignore[reportUnknownArgumentType]
    with pytest.raises(Exception):
        catfood.functions.github.api.请求GitHubAPI("http://api.github.com/", raiseException=True)

def test_请求GitHubAPI_returns_none_on_exception(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(catfood.functions.github.api.requests, "request", raise_exc) # pyright: ignore[reportUnknownArgumentType]
    assert catfood.functions.github.api.请求GitHubAPI("http://api.github.com/") is None

def test_请求GitHubAPI_headers_and_token(monkeypatch: pytest.MonkeyPatch):
    called = {}
    def fake_request(**kwargs) -> MagicMock: # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
        called.update(kwargs) # pyright: ignore[reportUnknownMemberType]
        mock_resp = MagicMock()
        mock_resp.json.return_value = {}
        mock_resp.raise_for_status.return_value = None
        return mock_resp
    monkeypatch.setattr(catfood.functions.github.api.requests, "request", fake_request) # pyright: ignore[reportUnknownArgumentType]
    catfood.functions.github.api.请求GitHubAPI("http://api.github.com/", token="好吃的")
    assert "Authorization" in called["headers"]
    assert called["headers"]["Authorization"] == "token 好吃的"

def test_请求GitHubAPI_wrong_api_version():
    with pytest.raises(ValueError):
        catfood.functions.github.api.请求GitHubAPI("999", api_version="123") # pyright: ignore[reportArgumentType]

def test_这是谁的Token_success(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(catfood.functions.github.api, "请求GitHubAPI", lambda *a, **k: {"login": "樱羽艾玛"}) # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]
    assert catfood.functions.github.api.这是谁的Token("abc") == "樱羽艾玛"

def test_这是谁的Token_invalid_token():
    assert catfood.functions.github.api.这是谁的Token(None) is None
    assert catfood.functions.github.api.这是谁的Token("") is None

def test_这是谁的Token_no_respones(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(catfood.functions.github.api, "请求GitHubAPI", lambda api, token: None) # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]
    assert catfood.functions.github.api.这是谁的Token("abc") is None

def test_这是谁的Token_response_not_dict(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(catfood.functions.github.api, "请求GitHubAPI", lambda api, token: 123) # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]
    assert catfood.functions.github.api.这是谁的Token("abc") is None
