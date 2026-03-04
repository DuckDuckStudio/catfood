"""提供一些异常类"""

from .operation import (CancelOther, OperationFailed, OperationNotSupported,
                        TryOtherMethods)
from .request import RequestException

__all__ = [
    "OperationFailed",
    "TryOtherMethods",
    "CancelOther",
    "OperationNotSupported",
    "RequestException",
]
