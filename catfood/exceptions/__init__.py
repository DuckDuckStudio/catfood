"""提供一些异常类"""

from .request import RequestException
from .operation import OperationFailed, TryOtherMethods, CancelOther, OperationNotSupported

__all__ = [
    "OperationFailed",
    "TryOtherMethods",
    "CancelOther",
    "OperationNotSupported",
    "RequestException",
]
