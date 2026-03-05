import pytest

from catfood.functions.format.github import IssueNumber, ResolvesIssue


@pytest.mark.parametrize(
    "input_value,expected",
    [
        (None, None),
        ("", None),
        (0, None),
        (-1, None),
        (123, "123"),
        ("123", "123"),
        ("#123", "123"),
        ("000123", "123"),
        ("#000123", "123"),
        ("  #000123  ", "123"),
        ("https://github.com/owner/repo/issues/456", "456"),
        ("https://github.com/owner/repo/pull/789", "789"),
        ("https://github.com/owner/repo/issues/000789", "789"),
        ("https://github.com/owner/repo/issues/notanumber", None),
        ("#notanumber", None),
        ("abc", None),
        ("#000", None),
        ("https://github.com/owner/repo/issues/", None),
        ("https://github.com/owner/repo/issues/123#discussion", "123"),
        ("https://github.com/owner/repo/issues/123#issuecomment-456", "123"),
    ]
)
def test_IssueNumber(input_value: None | str | int, expected: str | None):
    assert IssueNumber(input_value) == expected

@pytest.mark.parametrize(
    "input_value,keyword,expected",
    [
        (123, "Fixes", "- Fixes #123"),
        ("123", "Resolves", "- Resolves #123"),
        ("#123", "Closes", "- Closes #123"),
        ("000123", "Fixes", "- Fixes #123"),
        ("https://github.com/owner/repo/issues/456", "Resolves", "- Resolves #456"),
        ("", "Resolves", None),
        (None, "Resolves", None),
        ("notanumber", "Resolves", None),
        ("#000", "Resolves", None),
        ("https://github.com/owner/repo/issues/", "Resolves", None),
        ("https://github.com/owner/repo/issues/123#discussion", "Fixes", "- Fixes #123"),
        ("https://github.com/owner/repo/pull/789", "Closes", "- Closes #789"),
    ]
)
def test_ResolvesIssue(input_value: int | str | None, keyword: str, expected: str | None):
    assert ResolvesIssue(input_value, keyword) == expected

def test_ResolvesIssue_default_keyword():
    assert ResolvesIssue("123") == "- Resolves #123"
    assert ResolvesIssue("#456") == "- Resolves #456"
