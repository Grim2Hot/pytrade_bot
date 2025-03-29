from ...indicators.series_.bollinger import Bollinger
from ...indicators.series_.ma import SMA
from ...signal.base import Signal
from ...signal.trend import Trend
from base import Strategy
import pandas as pd


class BollingerStrategy(Strategy):
    """
    Bollinger Bands trading signals strategy.
    """
    def __init__(self, data: pd.DataFrame, bollinger: Bollinger = None, period: int = 20, std_dev: int = 2):
        super().__init__(data)
        if bollinger is None:
            self.bollinger = Bollinger(data, period, std_dev)
        else:
            self.bollinger = bollinger

    def signal_breakout(self) -> Signal:
        """
        Returns a signal (BUY, SELL, HOLD) based on the Bollinger Bands strategy.
        Strategy:
        - Emit a buy signal if the close price is below the lower band.
        - Emit a sell signal if the close price is above the upper band.
        - Otherwise, emit a hold signal.

        This requires context. The hold signal is only useful in the gradient of the SMA (middle band) is positive,
        or at least in the direction that we are betting (long/short).
        """
        bollinger_data = self.bollinger.calculate()

        # Check for buy/sell signals based on Bollinger Bands
        if self.data['Close'].iloc[-1] < bollinger_data['Lower Band'].iloc[-1]:
            print("Bollinger detected a breakout buy signal")
            return Signal.BUY
        elif self.data['Close'].iloc[-1] > bollinger_data['Upper Band'].iloc[-1]:
            print("Bollinger detected a breakout sell signal")
            return Signal.SELL
        else:
            return Signal.HOLD
        
    def signal_riding(self) -> Signal:
        """

        """
        sma = SMA(self.data, self.bollinger.period)
        trend = sma.get_trend()
        sma_series = sma.get_sma()

        

