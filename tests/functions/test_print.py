import pytest
from colorama import Fore

from catfood.functions.print import MSHead, print_multiline_with_prefix


def test_MSHead_values():
    assert MSHead.Message == f"{Fore.BLUE}[!]{Fore.RESET}"
    assert MSHead.Question == f"{Fore.BLUE}?{Fore.RESET}"
    assert MSHead.OptionalQuestion == f"{Fore.BLUE}? (可选){Fore.RESET}"
    assert MSHead.Information == f"{Fore.BLUE}INFO{Fore.RESET}"
    assert MSHead.Success == f"{Fore.GREEN}✓{Fore.RESET}"
    assert MSHead.Error == f"{Fore.RED}✕{Fore.RESET}"
    assert MSHead.Warning == f"{Fore.YELLOW}WARN{Fore.RESET}"
    assert MSHead.Debug == f"{Fore.CYAN}DEBUG{Fore.RESET}"
    assert MSHead.Hint == f"{Fore.YELLOW}Hint{Fore.RESET}"
    assert MSHead.InternalWarning == f"{Fore.YELLOW}WARN (内部){Fore.RESET}"
    assert MSHead.InternalError == f"{Fore.RED}✕ (内部){Fore.RESET}"


@pytest.mark.parametrize(
    "content,head,expected_lines",
    [
        ("单行内容", MSHead.Information, [f"{MSHead.Information} 单行内容"]),
        (
            "第一行\n第二行",
            MSHead.Hint,
            [f"{MSHead.Hint} 第一行", f"{MSHead.Hint} 第二行"],
        ),
        ("", MSHead.Debug, [f"{MSHead.Debug} "]),
        ("\n", MSHead.Debug, [f"{MSHead.Debug} ", f"{MSHead.Debug} "]),
    ],
)
def test_print_multiline_with_prefix(
    content: str,
    head: str,
    expected_lines: list[str],
    capsys: pytest.CaptureFixture[str],
):
    print_multiline_with_prefix(content, head)
    output_lines: list[str] = capsys.readouterr().out.rstrip("\n").split("\n")
    assert output_lines == expected_lines
