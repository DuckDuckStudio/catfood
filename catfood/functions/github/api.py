"""
提供一些与 GitHub API 操作相关的函数

GitHub REST API 文档: https://docs.github.com/zh/rest
"""

import base64
import sys
from typing import Any, Literal, cast

import requests

from ...constant import VERSION
from ...exceptions.request import RequestException

if sys.version_info < (3, 13):
    from typing_extensions import deprecated
else:
    from warnings import deprecated


def get_github_file_content(
    repo: str, path: str, token: str | None = None
) -> str | None:
    """
    尝试通过 GitHub API 获取文本文件 base64，解码后返回。

    Args:
        repo (str): 文件所在的仓库，应为 `owner/repo` 的格式。
        path (str): 需要获取的文件在仓库中的相对路径。
        token (str | None): 请求时附带的 GitHub Token。

    Returns:
        str: UTF-8 编码解码后的文本文件字符串。
        None: 获取失败。
    """

    try:
        if (len(repo.split("/")) < 2) or (len(repo.split("/")) > 3):
            raise ValueError("指定的仓库格式不对")

        normalized_path = path.replace("\\", "/")
        response = request_github_api(
            f"https://api.github.com/repos/{repo}/contents/{normalized_path}",
            token=token,
        )

        if not response:
            raise RequestException("响应为空")

        return base64.b64decode(response["content"]).decode("utf-8")
    except Exception:
        return None


@deprecated("请改用 get_github_file_content() 函数")
def 获取GitHub文件内容(repo: str, path: str, token: str | None = None) -> str | None:  # pylint: disable=non-ascii-name / C2401
    """
    此函数的名称已修改为 get_github_file_content，请改用新名称。

    此函数仅作为过渡保留，未来可能移除。

    ---

    尝试通过 GitHub API 获取文本文件 base64，解码后返回。

    Args:
        repo (str): 文件所在的仓库，应为 `owner/repo` 的格式。
        path (str): 需要获取的文件在仓库中的相对路径。
        token (str | None): 请求时附带的 GitHub Token。

    Returns:
        str: UTF-8 编码解码后的文本文件字符串。
        None: 获取失败。
    """

    return get_github_file_content(repo, path, token)


def request_github_api(
    api: str,
    params: dict[str, Any] | None = None,
    headers: dict[str, Any] | None = None,
    json: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
    token: str | None = None,
    method: str = "GET",
    api_version: Literal["2022-11-28", "2026-03-10"] = "2026-03-10",
    raiseException: bool = False,
) -> Any | None:
    """
    向指定的 GitHub API 发送请求，返回 `.json()` 后的响应内容

    Args:
        api (str): 指定的 GitHub API 链接
        params (dict[str, Any] | None): 请求的参数
        headers (dict[str, Any] | None): 请求头，`None` 为默认请求头
        json (dict[str, Any] | None): 请求附带的 json
        data (dict[str, Any] | None): 请求附带的 data
        token (str | None): 请求使用的 GitHub Token
        method (str): 请求使用的方法，默认为 GET
        api_version (Literal["2022-11-28", "2026-03-10"]): 请求时 `X-GitHub-Api-Version` 指定的 GitHub API 版本。有关 GitHub API 版本信息请参考 https://docs.github.com/zh/rest/about-the-rest-api/api-versions
        raiseException (bool): 在捕获到异常时是否直接 `raise` 出来

    Returns:
        Any: `.json()` 后的响应。
        None: 捕获到异常且 `raiseException` 为 `False` 时返回。
    """

    if api_version not in ["2022-11-28", "2026-03-10"]:
        raise ValueError("不正确的 GitHub API 版本")

    # 默认值
    if headers is None:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": f"DuckDuckStudio/catfood {VERSION}",
            "X-GitHub-Api-Version": api_version,
        }

    if token:
        headers["Authorization"] = f"token {token}"

    try:
        response = requests.request(
            method=method, url=api, params=params, headers=headers, json=json, data=data
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        if raiseException:
            raise
        else:
            return None


@deprecated("请改用 request_github_api() 函数")
def 请求GitHubAPI(  # pylint: disable=non-ascii-name / C2401
    api: str,
    params: dict[str, Any] | None = None,
    headers: dict[str, Any] | None = None,
    json: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
    token: str | None = None,
    method: str = "GET",
    api_version: Literal["2022-11-28", "2026-03-10"] = "2026-03-10",
    raiseException: bool = False,
) -> Any | None:
    """
    此函数的名称已修改为 request_github_api，请改用新名称。

    此函数仅作为过渡保留，未来可能移除。

    ---

    向指定的 GitHub API 发送请求，返回 `.json()` 后的响应内容

    Args:
        api (str): 指定的 GitHub API 链接
        params (dict[str, Any] | None): 请求的参数
        headers (dict[str, Any] | None): 请求头，`None` 为默认请求头
        json (dict[str, Any] | None): 请求附带的 json
        data (dict[str, Any] | None): 请求附带的 data
        token (str | None): 请求使用的 GitHub Token
        method (str): 请求使用的方法，默认为 GET
        api_version (Literal["2022-11-28", "2026-03-10"]): 请求时 `X-GitHub-Api-Version` 指定的 GitHub API 版本。有关 GitHub API 版本信息请参考 https://docs.github.com/zh/rest/about-the-rest-api/api-versions
        raiseException (bool): 在捕获到异常时是否直接 `raise` 出来

    Returns:
        Any: `.json()` 后的响应。
        None: 捕获到异常且 `raiseException` 为 `False` 时返回。
    """

    return request_github_api(
        api, params, headers, json, data, token, method, api_version, raiseException
    )


def get_github_token_owner(token: str | None) -> str | None:
    """
    通过 GitHub API 来获取这个 Token 的所有者。

    Args:
        token (str | None): 指定的 GitHub Token。

    Returns:
        str: Token 的所有者。
        None: 获取失败。
    """

    if not isinstance(token, str):
        return None

    token = token.strip()
    if not token:
        return None

    response: Any | None = request_github_api(
        "https://api.github.com/user", token=token
    )

    if isinstance(response, dict):
        response = cast(dict[str, Any], response)
        login: Any | None = response.get("login", None)
        if isinstance(login, str):
            return login

    return None


@deprecated("请改用 get_github_token_owner() 函数")
def 这是谁的Token(token: str | None) -> str | None:  # pylint: disable=non-ascii-name / C2401
    """
    此函数的名称已修改为 get_github_token_owner，请改用新名称。

    此函数仅作为过渡保留，未来可能移除。

    ---

    通过 GitHub API 来获取这个 Token 的所有者。

    Args:
        token (str | None): 指定的 GitHub Token。

    Returns:
        str: Token 的所有者。
        None: 获取失败。
    """

    return get_github_token_owner(token)
