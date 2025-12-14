"""
提供一些与 GitHub API 操作相关的函数

GitHub REST API 文档: https://docs.github.com/zh/rest
"""

import base64
import requests
from typing import Any, cast
from ...exceptions.request import RequestException

def 获取GitHub文件内容(repo: str, path: str, github_token: str | int | None = None) -> str | None:
    """
    尝试通过 GitHub API 获取文本文件 base64，解码后返回。
    
    :param repo: 文件所在的仓库，应为 `owner/repo` 的格式
    :type repo: str
    :param path: 需要获取的文件在仓库中的相对路径
    :type path: str
    :param github_token: 请求时附带的 GitHub Token
    :type github_token: str | int | None
    :return: UTF-8 编码解码后的文本文件字符串，获取失败返回 None
    :rtype: str | None
    """

    try:
        if (len(repo.split("/")) < 2) or (len(repo.split("/")) > 3):
            raise ValueError("指定的仓库格式不对")
        
        response = 请求GitHubAPI(
            f"https://api.github.com/repos/{repo}/contents/{path.replace("\\", "/")}",
            github_token
        )

        if not response:
            raise RequestException("响应为空")

        return base64.b64decode(response["content"]).decode("utf-8")
    except Exception:
        return None
    
def 请求GitHubAPI(api: str, github_token: str | int | None = None) -> Any | None:
    """
    尝试向指定的 api 发送 GET 请求，返回响应的 json 内容
    
    :param api: api 的 URL
    :type api: str
    :param github_token: 请求时附带的 GitHub Token
    :type github_token: str | int | None
    :return: 返回 `.json()` 后的响应，失败时返回 None
    :rtype: Any | None
    """

    headers: dict[str, str] = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    if not github_token:
        headers.pop("Authorization", None)

    try:
        response = requests.get(api, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception:
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
        "https://api.github.com/user", token
    )

    if isinstance(response, dict):
        response = cast(dict[str, Any], response)
        login: Any | None = response.get("login", None)
        if isinstance(login, str):
            return login
    
    return None
