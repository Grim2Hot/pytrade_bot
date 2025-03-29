from enum import Enum

class Trend(Enum):
    """
    Enum class for trend types.
    """
    STR_UP = 2
    STR_DOWN = -2
    UP = 1
    DOWN = -1
    NONE = 0

    def __str__(self):
        return self.name.lower()