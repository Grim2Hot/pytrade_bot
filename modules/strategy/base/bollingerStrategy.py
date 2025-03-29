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
    def __init__(
            self, 
            data: pd.DataFrame, 
            position: float = None,
            bollinger: Bollinger = None, 
            period: int = 20, 
            std_dev: int = 2,
            config: dict = None):
        
        super().__init__(data)
        if bollinger is None:
            self.bollinger = Bollinger(data, period, std_dev)
        else:
            self.bollinger = bollinger
        
        self.position = position if position else None
        self.config = config if config else {}
        self.buy_threshold = self.config.get('buy_threshold', 0.8)
        self.sell_threshold = self.config.get('sell_threshold', 0.2)
        self.loss = self.config.get('loss', -1)
        self.lower_bounce = self.config.get('lower_bounce', 0.05)
        self.upper_bounce = self.config.get('upper_bounce', 0.95)
        

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
        Uses 'Riding the Bands' strategy to determine what signal is relevant.
        """
        sma = SMA(self.data, self.bollinger.period, self.config)
        trend = sma.get_trend()
        band_range = self.bollinger.get_volatility()
        curr_price = self.data['Close'].iloc[-1]


        if band_range == 0:
            band_position = 0.5
        else:
            band_position = (curr_price - self.bollinger.data['Lower Band'].iloc[-1]) / band_range

        if self.position is None:
            # No position, we can only buy or hold practically, but we include sell signals for 
            # CIV calculation purposes, as it indicates the nature of the current trend.
            if trend in (Trend.STR_UP, Trend.UP):
                if band_position > self.buy_threshold:
                    print("Bollinger detected a riding buy signal")
                    return Signal.BUY
                else:
                    return Signal.HOLD
                
            elif trend in (Trend.STR_DOWN, Trend.DOWN):
                if band_position < self.sell_threshold:
                    print("Bollinger detected a riding sell signal")
                    return Signal.SELL
                else:
                    return Signal.HOLD
                
            else:
                # No clear trend
                return Signal.HOLD
        
        else:
            # We have a position, and must factor that into considerations
            entry_price = self.position
            profit_percent = (curr_price - entry_price) / entry_price * 100

            if trend in (Trend.STR_UP, Trend.UP):
                if profit_percent > 0:
                    return Signal.HOLD
                else:
                    # Could incorporate stop loss or volatility checking here.
                    return Signal.HOLD
                
            elif trend in (Trend.STR_DOWN, Trend.DOWN):
                if profit_percent < self.loss:
                    return Signal.SELL
                else:
                    return Signal.HOLD

            else:
                # No clear trend
                return Signal.HOLD

    def signal_squeeze(self) -> Signal:
        """
        Uses the 'Bollinger Squeeze' strategy to determine what signal is relevant.
        """           
        if self.bollinger.is_squeezed():
            print("Bollinger detected a squeeze signal")
            return Signal.SQUEEZE
        else:
            return Signal.HOLD

    def signal_bounce(self) -> Signal:
        """
        Asserts a trade signal if the price is bouncing off the bands.
        """
        self.bollinger.calculate()
        band_gap = self.bollinger.get_volatility()
        curr_price = self.data['Close'].iloc[-1]

        if band_gap == 0:
            band_position = 0.5
        else:
            band_position = (curr_price - self.bollinger.data['Lower Band'].iloc[-1]) / band_gap

        
        if band_position < self.lower_bounce:
            print("Bollinger detected a bounce buy signal")
            return Signal.BUY
        elif band_position > self.upper_bounce:
            print("Bollinger detected a bounce sell signal")
            return Signal.SELL
        else:
            return Signal.HOLD