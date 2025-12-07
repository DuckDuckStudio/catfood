"""
Cat Food - A collection of various commonly used functions.

猫粮 🐱 - 各种常用函数的集合。
"""

from .functions.print import 消息头
from .functions.files import open_file
from .exceptions.request import RequestException
from .functions.terminal import calculateCharactersDisplayed
from .functions.github.token import read_token, 这是谁的Token
from .functions.format.github import IssueNumber, ResolvesIssue
from .functions.github.api import 获取GitHub文件内容, 请求GitHubAPI
from .exceptions.operation import OperationFailed, TryOtherMethods, CancelOther, OperationNotSupported

__version__ = "1.0.2"
__all__ = [
    "消息头",
    "open_file",
    "calculateCharactersDisplayed",
    "IssueNumber",
    "ResolvesIssue",
    "获取GitHub文件内容",
    "请求GitHubAPI",
    "read_token",
    "这是谁的Token",
    "OperationFailed",
    "TryOtherMethods",
    "CancelOther",
    "OperationNotSupported",
    "RequestException",
]
