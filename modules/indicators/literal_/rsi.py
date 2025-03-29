from ..base import LiteralIndicator
import pandas


class RSI(LiteralIndicator):
    """
    Relative Strength Indicator (RSI).

    @param data: A pandas DataFrame containing the historical price data.
    @param period: The number of periods to use for the RSI calculation. Default is 14.
    The time period is ignorant of time units, and instead uses rows. 
    When instantiating the class, it may be best to calculate the rows before the class is instantiated.
    """
    def __init__(self, data: pandas.DataFrame, period: int = 14):
        super().__init__(data)
        self.period = period

    def calculate(self) -> int:
        """
        Calculates the RSI indicator for a given dataframe. 

        @return: An int representing the RSI.

        @description: The RSI is a momentum oscillator that measures the speed and change of price movements.
        It is calculated using the average gain and average loss over a specified period. The RSI ranges from 0 to 100,
        with values above 70 indicating overbought conditions and values below 30 indicating oversold conditions.

        RS refers to Relative Strength.
        RS = average gain / average loss
        RSI = 100 - (100 / (1 + RS))
        """
        df = self.data[:self.period].copy()
        avg_gain = df['close'].diff().where(df['close'].diff() > 0, 0).mean()
        avg_loss = df['close'].diff().where(df['close'].diff() < 0, 0).mean()
        rs = avg_gain / abs(avg_loss) if avg_loss != 0 else 0
        rsi = 100 - (100 / (1 + rs))
        # Set self.rsi for later calling
        self.rsi = rsi
        return rsi 
        