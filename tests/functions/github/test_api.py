from typing import NoReturn
from unittest.mock import MagicMock

import pytest

import catfood.functions.github.api


def raise_exc(**kwargs) -> NoReturn: # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
    raise Exception("测试异常") # pylint: disable=broad-exception-raised / W0719

def test_get_github_file_content_success(monkeypatch: pytest.MonkeyPatch):
    mock_response: dict[str, str] = {"content": "aGVsbG8gd29ybGQ="}
    monkeypatch.setattr(catfood.functions.github.api, "request_github_api", lambda api, token: mock_response) # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]
    assert catfood.functions.github.api.get_github_file_content("owner/repo", "README.md", token="abc") == "hello world"

def test_get_github_file_content_invalid_repo():
    assert catfood.functions.github.api.get_github_file_content("invalidrepo", "README.md") is None

def test_get_github_file_content_no_response(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(catfood.functions.github.api, "request_github_api", lambda api, token: None) # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]
    assert catfood.functions.github.api.get_github_file_content("owner/repo", "README.md") is None

def test_get_github_file_content_exception(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(catfood.functions.github.api, "request_github_api", raise_exc) # pyright: ignore[reportUnknownArgumentType]
    assert catfood.functions.github.api.get_github_file_content("owner/repo", "README.md") is None

def test_request_github_api_success(monkeypatch: pytest.MonkeyPatch):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"呐": "吸铁石"}
    mock_resp.raise_for_status.return_value = None
    monkeypatch.setattr(catfood.functions.github.api.requests, "request", lambda **kwargs: mock_resp) # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]
    assert catfood.functions.github.api.request_github_api("http://api.github.com/", token="abc") == {"呐": "吸铁石"}

def test_request_github_api_raises(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(catfood.functions.github.api.requests, "request", raise_exc) # pyright: ignore[reportUnknownArgumentType]
    with pytest.raises(Exception):
        catfood.functions.github.api.request_github_api("http://api.github.com/", raiseException=True)

def test_request_github_api_returns_none_on_exception(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(catfood.functions.github.api.requests, "request", raise_exc) # pyright: ignore[reportUnknownArgumentType]
    assert catfood.functions.github.api.request_github_api("http://api.github.com/") is None

def test_request_github_api_headers_and_token(monkeypatch: pytest.MonkeyPatch):
    called = {}
    def fake_request(**kwargs) -> MagicMock: # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
        called.update(kwargs) # pyright: ignore[reportUnknownMemberType]
        mock_resp = MagicMock()
        mock_resp.json.return_value = {}
        mock_resp.raise_for_status.return_value = None
        return mock_resp
    monkeypatch.setattr(catfood.functions.github.api.requests, "request", fake_request) # pyright: ignore[reportUnknownArgumentType]
    catfood.functions.github.api.request_github_api("http://api.github.com/", token="好吃的")
    assert "Authorization" in called["headers"]
    assert called["headers"]["Authorization"] == "token 好吃的"

def test_request_github_api_wrong_api_version():
    with pytest.raises(ValueError):
        catfood.functions.github.api.request_github_api("999", api_version="123") # pyright: ignore[reportArgumentType]

def test_get_github_token_owner_success(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(catfood.functions.github.api, "request_github_api", lambda *a, **k: {"login": "樱羽艾玛"}) # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]
    assert catfood.functions.github.api.get_github_token_owner("abc") == "樱羽艾玛"

def test_get_github_token_owner_invalid_token():
    assert catfood.functions.github.api.get_github_token_owner(None) is None
    assert catfood.functions.github.api.get_github_token_owner("") is None

def test_get_github_token_owner_no_respones(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(catfood.functions.github.api, "request_github_api", lambda api, token: None) # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]
    assert catfood.functions.github.api.get_github_token_owner("abc") is None

def test_get_github_token_owner_response_not_dict(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(catfood.functions.github.api, "request_github_api", lambda api, token: 123) # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]
    assert catfood.functions.github.api.get_github_token_owner("abc") is None
