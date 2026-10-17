"""提供一些与打印输出相关的函数和类"""

import sys
from typing import Final

from colorama import Fore

if sys.version_info < (3, 13):
    from typing_extensions import deprecated
else:
    from warnings import deprecated


class MSHead:  # pylint: disable=too-few-public-methods / R0903
    """
    消息头类。
    """

    # 特殊
    Message: Final = f"{Fore.BLUE}[!]{Fore.RESET}"
    Question: Final = f"{Fore.BLUE}?{Fore.RESET}"
    OptionalQuestion: Final = f"{Fore.BLUE}? (可选){Fore.RESET}"
    # 日志输出
    Information: Final = f"{Fore.BLUE}INFO{Fore.RESET}"
    Success: Final = f"{Fore.GREEN}✓{Fore.RESET}"
    Error: Final = f"{Fore.RED}✕{Fore.RESET}"
    Warning: Final = f"{Fore.YELLOW}WARN{Fore.RESET}"
    Debug: Final = f"{Fore.CYAN}DEBUG{Fore.RESET}"
    Hint: Final = f"{Fore.YELLOW}Hint{Fore.RESET}"
    # 内部
    InternalWarning: Final = f"{Fore.YELLOW}WARN (内部){Fore.RESET}"
    InternalError: Final = f"{Fore.RED}✕ (内部){Fore.RESET}"


@deprecated("请改用 MSHead 类")
class 消息头:  # pylint: disable=non-ascii-name / C2401, too-few-public-methods / R0903
    """
    消息头类已改为 MSHead 类，请改用新名称。

    此类仅作为过渡保留，未来可能移除。
    """

    # 特殊
    消息: Final = MSHead.Message
    问题: Final = MSHead.Question
    可选问题: Final = MSHead.OptionalQuestion
    # 日志输出
    信息: Final = MSHead.Information
    成功: Final = MSHead.Success
    错误: Final = MSHead.Error
    警告: Final = MSHead.Warning
    调试: Final = MSHead.Debug
    提示: Final = MSHead.Hint
    # 内部
    内部警告: Final = MSHead.InternalWarning
    内部错误: Final = MSHead.InternalError


def print_multiline_with_prefix(content: str, head: str) -> None:
    """
    输出多行带指定头的内容。

    Args:
        content: 需要输出的内容。
        head: 每行内容前面的消息头。
    """

    for line in content.split("\n"):
        print(f"{head} {line}")


@deprecated("请改用 print_multiline_with_prefix() 函数")
def 多行带头输出(content: str, head: str) -> None:  # pylint: disable=non-ascii-name / C2401
    """
    此函数的名称已修改为 print_multiline_with_prefix，请改用新名称。

    此函数仅作为过渡保留，未来可能移除。

    ---

    输出多行带指定头的内容。

    Args:
        content: 需要输出的内容。
        head: 每行内容前面的消息头。
    """

    return print_multiline_with_prefix(content, head)
