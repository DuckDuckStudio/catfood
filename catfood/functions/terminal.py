import re
import sys
from ..exceptions.operation import OperationNotSupported

def calculateCharactersDisplayed(content: str) -> int:
    """
    计算内容在 Windows 终端上显示占多少字符的位置。

    方法请参阅我的文章: https://duckduckstudio.github.io/Articles/#/%E4%BF%A1%E6%81%AF%E9%80%9F%E6%9F%A5/Python/%E8%BE%93%E5%87%BA/%E8%AE%A1%E7%AE%97%E8%BE%93%E5%87%BA%E7%9A%84%E5%86%85%E5%AE%B9%E5%9C%A8Windows%E7%BB%88%E7%AB%AF%E4%B8%8A%E7%9A%84%E6%98%BE%E7%A4%BA%E5%8D%A0%E5%A4%9A%E5%B0%91%E5%AD%97%E7%AC%A6
    
    :param content: 指定的内容
    :type content: str
    :return: 显示所占的字数
    :rtype: int
    """
    
    if (sys.platform != "win32"):
        raise OperationNotSupported("calculateCharactersDisplayed 仅在 Windows 终端中可用")

    # 移除颜色转义
    content = re.sub(r"\x1b\[[0-9;]*m", "", content)

    total = 0
    for char in content:
        total += 1
        if not ((ord(char) < 128) or (char in ["♪"])):
            total += 1

    return total
