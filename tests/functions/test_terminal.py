import sys
from typing import Literal, NoReturn

import pytest

from catfood.functions import terminal
from catfood.functions.print import 消息头


def test_runCommand_success(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]):
    def dummy_run(cmd: list[str], capture_output: Literal[True], text: Literal[True], check: Literal[False]):
        class Result:
            returncode = 0
            stdout: str = "你所热爱的，就是你的生活。"
            stderr: str = ""
        return Result()
    monkeypatch.setattr(terminal.subprocess, "run", dummy_run)
    ret: int = terminal.runCommand(["fcm", "get"])
    out: str = capsys.readouterr().out
    assert ret == 0
    assert out == ("你所热爱的，就是你的生活。" + '\n')

def test_runCommand_failure_no_retry(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]):
    def dummy_run(cmd: list[str], capture_output: Literal[True], text: Literal[True], check: Literal[False]):
        class Result:
            returncode = 1
            stdout = ""
            stderr = "error"
        return Result()
    monkeypatch.setattr(terminal.subprocess, "run", dummy_run)
    ret = terminal.runCommand(["Ciallo"], retry=-1)
    out = capsys.readouterr().out
    assert ret == 1
    assert 消息头.错误 in out
    assert "Ciallo" in out

def test_runCommand_failure_git_non_network(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]):
    def dummy_run(cmd: list[str], capture_output: Literal[True], text: Literal[True], check: Literal[False]):
        class Result:
            returncode = 128
            stdout: str = ""
            stderr: str = "fatal: not a git repository"
        return Result()
    monkeypatch.setattr(terminal.subprocess, "run", dummy_run)
    ret: int = terminal.runCommand(["git", "status"], retry=30)
    out: str = capsys.readouterr().out
    assert ret == 128
    assert 消息头.错误 in out
    assert 消息头.警告 in out

def test_runCommand_failure_git_network(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]):
    call_count: int = 0
    def dummy_run(cmd: list[str], capture_output: Literal[True], text: Literal[True], check: Literal[False]):
        nonlocal call_count
        call_count += 1
        class Result:
            returncode: int = 1 if call_count < 2 else 0
            stdout: str = ""
            stderr: str = "unable to access" if call_count < 2 else ""
        return Result()
    monkeypatch.setattr(terminal.subprocess, "run", dummy_run)
    monkeypatch.setattr(terminal.time, "sleep", lambda x: None) # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]
    ret: int = terminal.runCommand(["git", "pull"], retry=1)
    out: str = capsys.readouterr().out
    assert ret == 0
    assert 消息头.错误 in out
    assert 消息头.信息 in out

def test_runCommand_FileNotFound(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]):
    def dummy_run(cmd: list[str], capture_output: Literal[True], text: Literal[True], check: Literal[False]) -> NoReturn:
        raise FileNotFoundError()
    monkeypatch.setattr(terminal.subprocess, "run", dummy_run)
    ret: int = terminal.runCommand(["notfound"])
    out: str = capsys.readouterr().out
    assert ret == 1
    assert 消息头.错误 in out
    assert "未找到" in out

def test_runCommand_keyboard_interrupt(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]):
    def dummy_run(cmd: list[str], capture_output: Literal[True], text: Literal[True], check: Literal[False]) -> NoReturn:
        raise KeyboardInterrupt()
    monkeypatch.setattr(terminal.subprocess, "run", dummy_run)
    with pytest.raises(KeyboardInterrupt):
        terminal.runCommand(["TEmPTaTiON"])
    out: str = capsys.readouterr().out
    assert 消息头.错误 in out
    assert "KeyboardInterrupt" in out

def test_calculateCharactersDisplayed_win(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(sys, "platform", "win32")
    # 仅 ASCII
    assert terminal.calculateCharactersDisplayed("abc") == 3
    # 中文字符
    assert terminal.calculateCharactersDisplayed("一块钱还是神秘礼物？") == 20
    # 特殊字符
    assert terminal.calculateCharactersDisplayed("♪") == 1
    # 混合
    assert terminal.calculateCharactersDisplayed("a你b好") == 6
    # 带 ANSI 颜色
    assert terminal.calculateCharactersDisplayed("\x1b[31m红色\x1b[0m") == 4

def test_calculateCharactersDisplayed_nonwin(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(sys, "platform", "linux")
    with pytest.raises(terminal.OperationNotSupported):
        terminal.calculateCharactersDisplayed("abc")
