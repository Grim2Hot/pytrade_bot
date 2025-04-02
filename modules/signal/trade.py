from enum import Enum

class Trade(Enum):
    """
    Enum class for signal types.
    """
    BUY = 1
    SELL = -1
    HOLD = 0
    SQUEEZE = 2