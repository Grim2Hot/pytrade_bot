from base import LiteralIndicator
import pandas


class RSI(LiteralIndicator):
    def __init__(self, data: pandas.DataFrame):
        super().__init__(data)

    def calculate(self, period: int = 14) -> int:
        """
        Calculates the RSI indicator for a given dataframe. 

        @param period: The period of 'n' days' down closes. n is rows, but represents unit of time parsed.
        @return: An int representing the RSI.

        @description: The RSI is a momentum oscillator that measures the speed and change of price movements.
        It is calculated using the average gain and average loss over a specified period. The RSI ranges from 0 to 100,
        with values above 70 indicating overbought conditions and values below 30 indicating oversold conditions.

        RS refers to Relative Strength.
        RS = average gain / average loss
        RSI = 100 - (100 / (1 + RS))
        """
        df = self.data[:period].copy()
        avg_gain = df['close'].diff().where(df['close'].diff() > 0, 0).mean()
        avg_loss = df['close'].diff().where(df['close'].diff() < 0, 0).mean()
        rs = avg_gain / abs(avg_loss) if avg_loss != 0 else 0
        rsi = 100 - (100 / (1 + rs))
        return rsi 
        