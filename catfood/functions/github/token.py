import keyring
from typing import cast, Any
from ...functions.print import 消息头
from ...functions.github.api import 请求GitHubAPI

def read_token(silent: bool = False) -> str | None:
    """
    尝试从钥匙环中读取 github-access-token.glm 密钥 (aka glm 设置的 GitHub Token)
    
    :param silent: 是否阻止输出
    :type silent: bool
    :return: 返回 str 的 GitHub Token，失败返回 None
    :rtype: str | None
    """

    try:
        token = keyring.get_password("github-access-token.glm", "github-access-token")
        if token:
            return token
        elif not silent:
            print("你可能还没设置 glm 的 Token, 请尝试使用以下命令设置 Token:\n    glm config --token <YOUR-TOKEN>\n")
        return None
    except Exception as e:
        if not silent:
            print(f"{消息头.错误} 读取Token时出错:\n{e}")
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
