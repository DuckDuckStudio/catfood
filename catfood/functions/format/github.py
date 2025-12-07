"""
将传入的字符统一为某种 GitHub 上的格式。
"""

def IssueNumber(string: str | int | None) -> str | None:
    """
    从给定的字符串中获取 Issue 或 PR 的编号。
    
    :param string: 给定的字符串或整数或 None
    :type string: str | int | None
    :return: 返回字符串的编号，获取失败返回 None
    :rtype: str | None
    """

    if not string:
        return None
    elif isinstance(string, int) and (string > 0):
        return str(string)
    elif isinstance(string, str):
        string = string.strip()
        if (not string) or (string == "0"):
            return None
        elif string.isdigit(): # 正整数
            return string
        elif string.startswith("#") and string[1:].isdigit():
            return string[1:]
        elif string.startswith("https://"):
            for path in reversed(string.split("#", 1)[0].split("/")):
                if path.isdigit():
                    return path

    return None

def ResolvesIssue(string: str) -> str | None:
    """
    将给定的字符串格式化为 GitHub PR 的 Resolves Issue 格式

    GitHub Docs: https://docs.github.com/zh/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword
    
    :param string: 给定的字符串
    :type string: str
    :return: 格式化成功返回字符串结果，失败返回 None
    :rtype: str | None
    """

    num = IssueNumber(string)

    if num:
        # TODO: 支持 Fixes 等更多前缀
        return f"- Resolves {num}"
    else:
        return None
