from ....utils.utils import is_local_min, is_local_max
from ...indicators.series_.bollinger import Bollinger
from ...indicators.series_.ma import SMA
from ...signal.trade import Trade
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
        
        self.bollinger.calculate() # Depending on decoupling of Bollinger, this may not be necessary.
        self.position = position if position else None
        self.config = config if config else {}
        self.buy_threshold = self.config.get('buy_threshold', 0.8)
        self.sell_threshold = self.config.get('sell_threshold', 0.2)
        self.loss = self.config.get('loss', -1)
        self.lower_bounce = self.config.get('lower_bounce', 0.10)
        self.upper_bounce = self.config.get('upper_bounce', 0.90)
        self.lookback = self.config.get('lookback', 20)
        

    def signal_breakout(self) -> Trade:
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
            return Trade.BUY
        elif self.data['Close'].iloc[-1] > bollinger_data['Upper Band'].iloc[-1]:
            print("Bollinger detected a breakout sell signal")
            return Trade.SELL
        else:
            return Trade.HOLD
        
    def signal_riding(self) -> Trade:
        """
        Uses 'Riding the Bands' strategy to determine what signal is relevant.
        """
        # TODO: If self.sma is None, we should calculate it here.
        # Otherwise, we recalculate every time this function is called.
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
                if (band_position > self.buy_threshold) & (band_position <= 1):
                    print("Bollinger detected a riding buy signal")
                    return Trade.BUY
                else:
                    return Trade.HOLD
                
            elif trend in (Trend.STR_DOWN, Trend.DOWN):
                if (band_position < self.sell_threshold) & (band_position >= 0):
                    print("Bollinger detected a riding sell signal")
                    return Trade.SELL
                else:
                    return Trade.HOLD
                
            else:
                # No clear trend
                # TODO: A Hold signal is a deterministic signal - it is a positive action,
                # it is not a neutral action. This could be reconsidered to an uncertainty signal.
                return Trade.HOLD
        
        else:
            # We have a position, and must factor that into considerations
            # TODO: self.position might not be numeric - it may be an object.
            # Update this type/accessor to be more generic if so.
            entry_price = self.position
            profit_percent = (curr_price - entry_price) / entry_price * 100

            if trend in (Trend.STR_UP, Trend.UP):
                if profit_percent > 0:
                    return Trade.HOLD
                else:
                    # Could incorporate stop loss or volatility checking here.
                    return Trade.HOLD
                
            elif trend in (Trend.STR_DOWN, Trend.DOWN):
                if profit_percent < self.loss:
                    return Trade.SELL
                else:
                    return Trade.HOLD

            else:
                # No clear trend
                return Trade.HOLD

    def signal_squeeze(self) -> Trade:
        """
        Uses the 'Bollinger Squeeze' strategy to determine what signal is relevant.
        """
        # TODO: Review this 'is_squeezed' method if            
        if self.bollinger.is_squeezed():
            print("Bollinger detected a squeeze signal")
            return Trade.SQUEEZE
        else:
            return Trade.HOLD

    def signal_bounce(self) -> Trade:
        """
        Asserts a trade signal if the price is bouncing off the bands.
        """
        # TODO: Depending on object decoupling of bollinger indicator, the calculate() 
        # may not need to be called here.
        self.bollinger.calculate()
        band_gap = self.bollinger.get_volatility()
        curr_price = self.data['Close'].iloc[-1]

        if band_gap == 0:
            band_position = 0.5
        else:
            band_position = (curr_price - self.bollinger.data['Lower Band'].iloc[-1]) / band_gap
        
        # Account for oddities in the data
        lookback = self.lookback
        if len(self.data) < lookback + 1:
            return Trade.HOLD
        
        recent_prices = self.data['Close'].iloc[-(lookback+1):].values

        if band_position < self.lower_bounce and is_local_min(recent_prices):
            print("Bollinger detected a bounce buy signal")
            return Trade.BUY
        elif band_position > self.upper_bounce and is_local_max(recent_prices):
            print("Bollinger detected a bounce sell signal")
            return Trade.SELL
        else:
            return Trade.HOLD
                