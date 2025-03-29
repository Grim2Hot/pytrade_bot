from ...indicators.series_.bollinger import Bollinger
from ...signal.base import Signal
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

    def get_signal(self) -> Signal:
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
            print("Bollinger detected a buy signal")
            return Signal.BUY
        elif self.data['Close'].iloc[-1] > bollinger_data['Upper Band'].iloc[-1]:
            print("Bollinger detected a sell signal")
            return Signal.SELL
        else:
            return Signal.HOLD
        