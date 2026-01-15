"""提供一些与终端操作相关的函数"""

import re
import sys
import time
import subprocess
from colorama import Fore
from ..functions.print import 消息头
from ..exceptions.operation import OperationNotSupported

def runCommand(command: list[str] | str, retry: int = -1) -> int:
    """
    运行指定命令，并允许设置自动重试。

    拒绝重试 git 因非网络错误导致的失败。
    
    :param command: 需要运行的命令
    :type command: list[str] | str
    :param retry: 重试前的等待时间，-1 表示不重试
    :type retry: int
    :return: 退出代码
    :rtype: int
    """

    if isinstance(command, str):
        command = command.split(" ")

    try:
        while True:
            try:
                result = subprocess.run(command, capture_output=True, text=True)
                if result.stdout.strip():
                    print(result.stdout.strip())
                if result.stderr.strip():
                    print(result.stderr.strip())

                if result.returncode == 0:
                    return 0
                else:
                    print(f"{消息头.错误} 运行 {Fore.BLUE}{" ".join(command)}{Fore.RESET} 失败，{command[0]} 返回非零退出代码 {Fore.BLUE}{result.returncode}{Fore.RESET}")

                    if retry < 0:
                        return result.returncode
                    elif retry > 0:
                        if command[0] == "git":
                            if not any(keyword in result.stderr.lower() for keyword in (
                                "unable to access", "could not resolve host",
                                "failed to connect", "operation timed out",
                                "early eof", "rpc failed"
                            )):
                                print(f"{消息头.警告} 这看起来像是 Git 遇到了网络之外的问题，拒绝重试")
                                return result.returncode

                        try:
                            for i in reversed(range(1, retry+1)):
                                print(f"\r{i}秒后重试...", end="")
                                time.sleep(1)
                        except KeyboardInterrupt:
                            raise
                        finally:
                            print("\r", end="")
            except FileNotFoundError:
                print(f"{消息头.错误} 未找到 {command[0]}")
                return 1

            print(f"{消息头.信息} 正在重试 ...")
    except KeyboardInterrupt:
        print(f"{消息头.错误} 终止运行命令 {Fore.BLUE}{" ".join(command)}{Fore.RESET}，因为收到了 Ctrl + C (KeyboardInterrupt)")
        raise KeyboardInterrupt

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
