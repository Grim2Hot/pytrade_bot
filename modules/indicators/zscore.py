from base import LiteralIndicator
from bollinger import Bollinger
import pandas


class VolatilityZScore(LiteralIndicator):
    """
    Z Score of the volatility of the Bollinger Bands.
    This score states how far a data point is from the mean, in units of standard deviations

    ~0 indicates typical behaviour
    > 1 or > -1 indicates unusual behaviour
    > 2 or > -2 indicates extreme behaviour
    > 3 or > -3 indicates Rare or Extreme event(s)

    Requries that a Bollinger object be parsed, to minimise calculations.

    @param data: A pandas DataFrame containing the historical price data.
    @param bollinger: A Bollinger object containing the Bollinger Bands data.
    @param period: Optional. The number of periods to use for the Z-Score calculation. Default is 20.
    @param sma_interval: Optional. The number of periods to use for the SMA calculation. Default is None.
    If sma_interval is not set, it uses the interval of the Bollinger object provided.
    """
    def __init__(self, data: pandas.DataFrame, bollinger: Bollinger, period: int = 20, sma_interval: int = None):
        super().__init__(data)
        self.period = period
        self.bollinger = bollinger
        self.sma_interval = sma_interval
        self.z_score = None

    def calculate(self) -> float:
        """
        Calculates the Z-Score of the volatility of the Bollinger Bands.
        Returns a float which represents a normalised score of the local volaitility of the asset at the most recent time period.
        """
        if 'Middle Band' not in self.bollinger.data.columns:
            self.bollinger.calculate()
            self.data = self.bollinger.data.copy()

        band_width = self.data['Upper Band'] - self.data['Lower Band']

        if self.sma_interval is None:
            noise_score = band_width / self.data['Middle Band']
        else:
            noise_score = band_width / self.data['Middle Band'].rolling(window=self.sma_interval).mean()
        
        z_score = (noise_score - noise_score.rolling(window=self.period).mean()) / noise_score.rolling(window=self.period).std()
        self.z_score = z_score

        return z_score.iloc[-1]
