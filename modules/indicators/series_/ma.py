from ..base import SeriesIndicator
from ...signal.trend import Trend
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
    
    def get_sma(self) -> pandas.Series:
        """
        Returns the calculated SMA series.
        """
        return self.data[f'SMA_{self.period}']
    
    def get_trend(self, window: int = 10) -> Trend:
        """
        """
        sma_col = f'SMA_{self.period}'
        if sma_col not in self.data.columns:
            self.calculate()

        recent_sma = self.data[sma_col].dropna().tail(window)
        if len(recent_sma) < window:
            return Trend.NONE

        pct_change = (recent_sma.iloc[-1] / recent_sma.iloc[0] - 1) * 100

        if pct_change > 5:
            return Trend.STR_UP
        elif pct_change > 1:
            return Trend.UP
        elif pct_change < -5:
            return Trend.STR_DOWN
        elif pct_change < -1:
            return Trend.DOWN
        else:
            return Trend.NONE
    
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
    