import pytest
from colorama import Fore

from catfood.functions.print import 多行带头输出, 消息头


def test_消息头_values():
    assert 消息头.消息 == f"{Fore.BLUE}[!]{Fore.RESET}"
    assert 消息头.问题 == f"{Fore.BLUE}?{Fore.RESET}"
    assert 消息头.可选问题 == f"{Fore.BLUE}? (可选){Fore.RESET}"
    assert 消息头.信息 == f"{Fore.BLUE}INFO{Fore.RESET}"
    assert 消息头.成功 == f"{Fore.GREEN}✓{Fore.RESET}"
    assert 消息头.错误 == f"{Fore.RED}✕{Fore.RESET}"
    assert 消息头.警告 == f"{Fore.YELLOW}WARN{Fore.RESET}"
    assert 消息头.调试 == f"{Fore.CYAN}DEBUG{Fore.RESET}"
    assert 消息头.提示 == f"{Fore.YELLOW}Hint{Fore.RESET}"
    assert 消息头.内部警告 == f"{Fore.YELLOW}WARN (内部){Fore.RESET}"
    assert 消息头.内部错误 == f"{Fore.RED}✕ (内部){Fore.RESET}"

@pytest.mark.parametrize(
    "content,head,expected_lines",
    [
        ("单行内容", 消息头.信息, [f"{消息头.信息} 单行内容"]),
        ("第一行\n第二行", 消息头.提示, [f"{消息头.提示} 第一行", f"{消息头.提示} 第二行"]),
        ("", 消息头.调试, [f"{消息头.调试} "]),
        ("\n", 消息头.调试, [f"{消息头.调试} ", f"{消息头.调试} "]),
    ]
)
def test_多行带头输出_prints_correct_lines(content: str, head: str, expected_lines: list[str], capsys: pytest.CaptureFixture[str]):
    多行带头输出(content, head)
    output_lines: list[str] = capsys.readouterr().out.rstrip('\n').split('\n')
    assert output_lines == expected_lines
