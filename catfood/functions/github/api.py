"""
提供一些与 GitHub API 操作相关的函数

GitHub REST API 文档: https://docs.github.com/zh/rest
"""

import base64
import requests
import warnings
from typing import Any, cast
from ...constant import VERSION
from ...exceptions.request import RequestException

def 获取GitHub文件内容(repo: str, path: str, github_token: str | int | None = None, token: str | None = None) -> str | None:
    """
    尝试通过 GitHub API 获取文本文件 base64，解码后返回。
    
    :param repo: 文件所在的仓库，应为 `owner/repo` 的格式
    :type repo: str
    :param path: 需要获取的文件在仓库中的相对路径
    :type path: str
    :param token: 请求时附带的 GitHub Token
    :type token: str | None
    :param github_token: (将在 2.0.0 移除，请改用 token 参数) 请求时附带的 GitHub Token
    :type github_token: str | int | None
    :return: UTF-8 编码解码后的文本文件字符串，获取失败返回 None
    :rtype: str | None
    """

    if isinstance(github_token, str) and github_token:
        token = github_token
        warnings.warn(
            message="""
catfood.functions.github.api 的 "获取GitHub文件内容" 函数的 github_token 参数将在 catfood 2.0.0 移除，
请改用 token 参数。
""",
            category=DeprecationWarning
        )

    try:
        if (len(repo.split("/")) < 2) or (len(repo.split("/")) > 3):
            raise ValueError("指定的仓库格式不对")
        
        response = 请求GitHubAPI(
            f"https://api.github.com/repos/{repo}/contents/{path.replace("\\", "/")}",
            token=token
        )

        if not response:
            raise RequestException("响应为空")

        return base64.b64decode(response["content"]).decode("utf-8")
    except Exception:
        return None
    
def 请求GitHubAPI(
    api: str,
    github_token: str | int | None = None,
    params: dict[str, Any] = {},
    headers: dict[str, Any] = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"DuckDuckStudio/catfood {VERSION}"
    },
    json: dict[str, Any] = {},
    data: dict[str, Any] = {},
    token: str | None = None,
    method: str = "GET",
    raiseException: bool = False
) -> Any | None:
    """
    向指定的 GitHub API 发送请求，返回 `.json()` 后的响应内容
    
    :param api: 指定的 GitHub API 链接
    :type api: str
    :param github_token: (将在 2.0.0 移除，请改用 token 参数) 请求时附带的 GitHub Token
    :type github_token: str | int | None
    :param params: 请求的参数
    :type params: dict[str, Any]
    :param headers: 请求头
    :type headers: dict[str, Any]
    :param json: 请求附带的 json
    :type json: dict[str, Any]
    :param data: 请求附带的 data
    :type data: dict[str, Any]
    :param token: 请求使用的 GitHub Token
    :type token: str | None
    :param method: 请求使用的方法，默认为 GET
    :type method: str
    :param raiseException: 在捕获到异常时是否直接 `raise` 出来
    :type raiseException: bool
    :return: 返回 `.json()` 后的响应。捕获到异常且 `raiseException` 为 `False` 时返回 None。
    :rtype: Any | None
    """

    if isinstance(github_token, str) and github_token:
        token = github_token
        warnings.warn(
            message="""
catfood.functions.github.api 的 "请求GitHubAPI" 函数的 github_token 参数将在 catfood 2.0.0 移除，
请改用 token 参数。
""",
            category=DeprecationWarning
        )

    if token:
        headers["Authorization"] = f"token {token}"

    try:
        response = requests.request(method=method, url=api, params=params, headers=headers, json=json, data=data)
        response.raise_for_status()
        return response.json()
    except Exception:
        if raiseException:
            raise
        else:
            return None

def 这是谁的Token(token: str | None) -> str | None:
    """
    通过 GitHub API 来确认这个 Token 是谁的
    
    :param token: 指定的 GitHub Token
    :type token: str | None
    :return: 返回 str 的所有者，失败返回 None
    :rtype: str | None
    """

    if not isinstance(token, str):
        return None
    
    token = token.strip()
    if not token:
        return None

    response: Any | None = 请求GitHubAPI(
        "https://api.github.com/user",
        token=token
    )

    if isinstance(response, dict):
        response = cast(dict[str, Any], response)
        login: Any | None = response.get("login", None)
        if isinstance(login, str):
            return login
    
    return None
