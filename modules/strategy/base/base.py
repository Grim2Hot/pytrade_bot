import pandas
from abc import ABC, abstractmethod




class Strategy(ABC):
    """
    Abstract base class for all trading strategies.
    """
    def __init__(self, data : pandas.DataFrame, indicators : list = None):
        self.data = data
        self.indicators = indicators if indicators is not None else []
    
    @abstractmethod
    def get_signal(self):
        """
        Returns a signal (BUY, SELL, HOLD) based on the strategy's logic.
        """
        raise NotImplementedError("This is an abstract class. Please implement the methods in a subclass.")