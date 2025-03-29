from ..base import SeriesIndicator
import pandas


"""
Contains the classes for the Moving Average indicators.
"""

class SMA(SeriesIndicator):
    """
    Simple Moving Average (SMA).
    SMA is the average of a set of prices over a specified number of periods.
    """
    def __init__(self, data: pandas.DataFrame, period: int = 14):
        super().__init__(data)
        self.period = period

    def calculate(self):
        """
        Adds the calculated field to the dataframe parsed to the class.
        """
        self.data[f'SMA_{self.period}'] = self.data['Close'].rolling(window=self.period).mean()
        return self.data
    
class EMA(SeriesIndicator):
    """
    Exponential Moving Average (EMA).
    EMA puts more weight on the most recent prices, making it more responsive to new information.
    """
    def __init__(self, data: pandas.DataFrame, period: int = 14):
        super().__init__(data)
        self.period = period

    def calculate(self, adjust: bool = False) -> pandas.DataFrame:
        """
        Adds the Exponential Moving Average (EMA) to the dataframe parsed to the class.

        @param adjust: If True, the EMA's weights are calculated using the full history (less efficient). Default is False.
        """
        self.data[f'EMA_{self.period}'] = self.data['Close'].ewm(
            span=self.period, 
            adjust=adjust
            ).mean()
        return self.data
    