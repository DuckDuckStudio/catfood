"""
Cat Food - A collection of various commonly used functions.

猫粮 🐱 - 各种常用函数的集合。
"""

from .constant import VERSION
from .exceptions.operation import (CancelOther, OperationFailed,
                                   OperationNotSupported, TryOtherMethods)
from .exceptions.request import RequestException
from .functions.files import open_file
from .functions.format.github import IssueNumber, ResolvesIssue
from .functions.github.api import 获取GitHub文件内容, 请求GitHubAPI
from .functions.github.token import read_token, 这是谁的Token
from .functions.print import 消息头
from .functions.terminal import calculateCharactersDisplayed

__version__ = VERSION
__all__ = [
    "VERSION",
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
