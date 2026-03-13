from typing import NoReturn
from unittest.mock import MagicMock

import pytest

import catfood.functions.github.api


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
    def raise_exc(api: str, token: str | None = None) -> NoReturn: raise Exception("我不是专业养鸭的，但是我知道，遇到鸭的时候，你慢慢靠近，让它感觉你没有恶意，然后轻轻抚摸鸭头，正常它是不会咬你的，如果它咬你了，就当我没说，毕竟开头我也说了，我不是专业的。")
    monkeypatch.setattr(catfood.functions.github.api, "请求GitHubAPI", raise_exc)
    assert catfood.functions.github.api.获取GitHub文件内容("owner/repo", "README.md") is None

def test_请求GitHubAPI_success(monkeypatch: pytest.MonkeyPatch):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"呐": "吸铁石"}
    mock_resp.raise_for_status.return_value = None
    monkeypatch.setattr(catfood.functions.github.api.requests, "request", lambda **kwargs: mock_resp) # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]
    assert catfood.functions.github.api.请求GitHubAPI("http://api.github.com/", token="abc") == {"呐": "吸铁石"}

def test_请求GitHubAPI_raises(monkeypatch: pytest.MonkeyPatch):
    def raise_exc(**kwargs) -> NoReturn: raise Exception("抱歉，今天不行。") # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
    monkeypatch.setattr(catfood.functions.github.api.requests, "request", raise_exc) # pyright: ignore[reportUnknownArgumentType]
    with pytest.raises(Exception):
        catfood.functions.github.api.请求GitHubAPI("http://api.github.com/", raiseException=True)

def test_请求GitHubAPI_returns_none_on_exception(monkeypatch: pytest.MonkeyPatch):
    def raise_exc(**kwargs) -> NoReturn: raise Exception("都过年了，不要再讨论什么音游了。你带你的理论值回到家并不能给你带来任何实质性作用，朋友们兜里掏出一大把钱购物旅行，你默默的在家里推分。亲戚朋友吃饭问你收获了什么，你说我收了首歌，亲戚们懵逼了，你还在心里默默嘲笑他们，笑他们不懂你的手法，理论达成的那一刻的自豪，也笑他们对于音游的认知只是钢琴块。你父母的同事都在说自己的子女一年的收获，儿子升职加薪了，女儿结婚了，姑娘生了个可爱的宝宝，你的父母默默无言，说我的儿子在对着板子戳戳戳，家里平板屏幕越来越烂了。时间流逝，一年又一年，你还在想着下一个章节的魔王出来了，继续推新的谱面，而你身边的人在考虑买什么豪车、去哪个度假胜地，你还在纠结你的破音游。") # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
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
