from ..base import SeriesIndicator
from ...signal.trend import Trend
import yaml
import pandas


"""
Contains the classes for the Moving Average indicators.
"""

class SMA(SeriesIndicator):
    """
    Simple Moving Average (SMA).
    SMA is the average of a set of prices over a specified number of periods.
    """
    def __init__(self, data: pandas.DataFrame, period: int = 14, config: dict = None):
        super().__init__(data)
        self.period = period
        self.config = config if config else {}
        self.str_up = self.config.get('strong_up_threshold', 0.2)
        self.up = self.config.get('up_threshold', 0.05)
        self.str_down = self.config.get('strong_down_threshold', -0.2)
        self.down = self.config.get('down_threshold', -0.05)

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
        Returns the trend of the SMA over the specified window.
        The trend is determined by the percentage change over the specified window.
        The values are placeholders for being inserted by the config. 
        They represent small values, suitable for high resolution data, like minutes or seconds. 
        For 5, 10, 15 minute data, the values should be adjusted to be larger.

        @param window: The number of periods to use for the trend calculation. Default is 10.
        """
        sma_col = f'SMA_{self.period}'
        if sma_col not in self.data.columns:
            self.calculate()

        recent_sma = self.data[sma_col].dropna().tail(window)
        if len(recent_sma) < window:
            return Trend.NONE

        pct_change = (recent_sma.iloc[-1] / recent_sma.iloc[0] - 1) * 100

        if pct_change > self.str_up:
            return Trend.STR_UP
        elif pct_change > self.up:
            return Trend.UP
        elif pct_change < self.down:
            return Trend.STR_DOWN
        elif pct_change < self.str_down:
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
    