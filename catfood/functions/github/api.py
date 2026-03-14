"""
提供一些与 GitHub API 操作相关的函数

GitHub REST API 文档: https://docs.github.com/zh/rest
"""

import base64
from typing import Any, Literal, cast

import requests

from ...constant import VERSION
from ...exceptions.request import RequestException


def 获取GitHub文件内容(repo: str, path: str, token: str | None = None) -> str | None:
    """
    尝试通过 GitHub API 获取文本文件 base64，解码后返回。
    
    :param repo: 文件所在的仓库，应为 `owner/repo` 的格式
    :type repo: str
    :param path: 需要获取的文件在仓库中的相对路径
    :type path: str
    :param token: 请求时附带的 GitHub Token
    :type token: str | None
    :return: UTF-8 编码解码后的文本文件字符串，获取失败返回 None
    :rtype: str | None
    """

    try:
        if (len(repo.split("/")) < 2) or (len(repo.split("/")) > 3):
            raise ValueError("指定的仓库格式不对")

        normalized_path = path.replace("\\", "/")
        response = 请求GitHubAPI(
            f"https://api.github.com/repos/{repo}/contents/{normalized_path}",
            token=token
        )

        if not response:
            raise RequestException("响应为空")

        return base64.b64decode(response["content"]).decode("utf-8")
    except Exception:
        return None

def 请求GitHubAPI(
    api: str,
    params: dict[str, Any] | None = None,
    headers: dict[str, Any] | None = None,
    json: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
    token: str | None = None,
    method: str = "GET",
    timeout: int = 10,
    api_version: Literal["2022-11-28", "2026-03-10"] = "2026-03-10",
    raiseException: bool = False
) -> Any | None:
    """
    向指定的 GitHub API 发送请求，返回 `.json()` 后的响应内容
    
    :param api: 指定的 GitHub API 链接
    :type api: str
    :param params: 请求的参数
    :type params: dict[str, Any] | None
    :param headers: 请求头，`None` 为默认请求头
    :type headers: dict[str, Any] | None
    :param json: 请求附带的 json
    :type json: dict[str, Any] | None
    :param data: 请求附带的 data
    :type data: dict[str, Any] | None
    :param token: 请求使用的 GitHub Token
    :type token: str | None
    :param method: 请求使用的方法，默认为 GET
    :type method: str
    :param timeout: 请求超时的时间（秒）
    :type timeout: int
    :param api_version: 请求时 `X-GitHub-Api-Version` 指定的 GitHub API 版本。有关 GitHub API 版本信息请参考 https://docs.github.com/zh/rest/about-the-rest-api/api-versions
    :type api_version: Literal["2022-11-28", "2026-03-10"]
    :param raiseException: 在捕获到异常时是否直接 `raise` 出来
    :type raiseException: bool
    :return: 返回 `.json()` 后的响应。捕获到异常且 `raiseException` 为 `False` 时返回 None。
    :rtype: Any | None
    """

    if api_version not in ["2022-11-28", "2026-03-10"]:
        raise ValueError("不正确的 GitHub API 版本")

    # 默认值
    if headers is None:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": f"DuckDuckStudio/catfood {VERSION}",
            "X-GitHub-Api-Version": api_version
        }

    if token:
        headers["Authorization"] = f"token {token}"

    try:
        response = requests.request(
            method=method,
            url=api,
            params=params,
            headers=headers,
            json=json,
            data=data,
            timeout=timeout
        )
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
