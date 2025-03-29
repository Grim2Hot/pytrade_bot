from base import LiteralIndicator
from bollinger import Bollinger
import pandas


class VolatilityZScore(LiteralIndicator):
    """
    
    """
    def __init__(self, data: pandas.DataFrame, bollinger: Bollinger, period: int = 20):
        super().__init__(data)
        self.period = period
        self.bollinger = bollinger

    def calculate(self) -> float:
        """
        Calculates the Z-Score of the volatility of the Bollinger Bands.
        Returns a float which represents a normalised score of the local volaitility of the asset at the most recent time period.
        """
        if 'Middle Band' not in self.bollinger.data.columns:
            self.bollinger.calculate()
            self.data = self.bollinger.data.copy()

        band_width = self.data['Upper Band'] - self.data['Lower Band']
        noise_score = band_width / self.data['Middle Band']
        z_noise = (noise_score - noise_score.rolling(window=self.period).mean()) / noise_score.rolling(window=self.period).std()

        self.z_noise = z_noise
        return z_noise.iloc[-1]
