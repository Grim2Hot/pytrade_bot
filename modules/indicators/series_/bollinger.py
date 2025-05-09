from ..base import SeriesIndicator
import pandas


class Bollinger(SeriesIndicator):
    """
    @param data: A pandas DataFrame containing the historical price data.
    @param period: The number of periods to use for the Bollinger Bands calculation. Default is 20.
    The time period is ignorant of time units, and instead uses rows.
    When instantiating the class, it may be best to calculate the rows before the class is instantiated.
    @param mult: The number of standard deviations to use for the upper and lower bands. Default is 2.

    Bollinger Bands indicator.
    The Bollinger Bands indicator consists of three lines:
        - Middle Band: 20-period simple moving average (SMA)
        - Upper Band: Middle Band + (2 * 20-period standard deviation)
        - Lower Band: Middle Band - (2 * 20-period standard deviation)
    """

    def __init__(self, data: pandas.DataFrame, period: int = 20, mult: int = 2):
        super().__init__(data)
        self.period = period
        self.mult = mult
        self.current_volatility = None

    def calculate(self) -> pandas.DataFrame:
        """
        Adds the calculated field to the dataframe parsed to the class.
        """
        self.data['Middle Band'] = self.data['Close'].rolling(window=self.period).mean()
        self.data['Upper Band'] = self.data['Middle Band'] + (self.data['Close'].rolling(window=self.period).std() * self.mult)
        self.data['Lower Band'] = self.data['Middle Band'] - (self.data['Close'].rolling(window=self.period).std() * self.mult)
        self.current_volatility = self.data['Upper Band'].iloc[-1] - self.data['Lower Band'].iloc[-1]
        return self.data
    
    def get_volatility(self) -> float:
        """
        Returns the current volatility of the Bollinger Bands.
        """
        return self.current_volatility
    
    def is_squeezed(self, window: int = 20, quantile: float = 0.2) -> bool:
        """
        Returns True if the Bollinger Bands are squeezed, False otherwise.
        A squeeze is defined as the current volatility being below the specified quantile of the rolling volatility.
        """
        rolling_volatility = self.data['Upper Band'].rolling(window=window).std()
        return self.current_volatility < rolling_volatility.quantile(quantile)
    