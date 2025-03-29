from ..base import SeriesIndicator
import pandas
import numpy as np



class OBV(SeriesIndicator):
    """
    On-Balance Volume (OBV) indicator.

    @param data: A pandas DataFrame containing the historical price data.
    The time period is ignorant of time units, and instead uses rows. 
    When instantiating the class, it may be best to calculate the rows before the class is instantiated.
    @description: The On-Balance Volume (OBV) indicator is a momentum indicator that uses volume flow to predict changes in stock price.
    It is based on the idea that volume precedes price movement. When the OBV line is rising, it indicates that volume is increasing on up days, which is bullish. Conversely, when the OBV line is falling, it indicates that volume is increasing on down days, which is bearish.
    The OBV line is calculated by adding the volume on up days and subtracting the volume on down days.

    This object expects a 'Volume' and 'Close' column to be present in the parsed data.
    """

    def __init__(self, data: pandas.DataFrame):
        super().__init__(data)

    def calculate(self) -> pandas.DataFrame:
        """
        Adds the calculated field to the dataframe parsed to the class.
        """
        self.data['OBV'] = np.where(
            self.data['Close'] > self.data['Close'].shift(1),  self.data['Volume'], 
            np.where(self.data['Close'] < self.data['Close'].shift(1), -self.data['Volume'], 0)
        ).cumsum()
        return self.data