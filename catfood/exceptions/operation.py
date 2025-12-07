"""操作异常"""

class OperationFailed(Exception):
    """当前操作失败"""

class TryOtherMethods(Exception):
    """尝试当前方法失败，请尝试其他方法。"""

class CancelOther(Exception):
    """取消后续操作"""

class OperationNotSupported(Exception):
    """不支持的操作"""
