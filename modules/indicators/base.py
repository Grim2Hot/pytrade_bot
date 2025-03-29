from abc import ABC, abstractmethod
import pandas



class SeriesIndicator(ABC):
    def __init__(self, data: pandas.DataFrame):
        self.data = data

    @abstractmethod
    def calculate(self) -> pandas.DataFrame:
        """
        Adds the calculated field to the dataframe parsed to the class.
        """
        pass

class LiteralIndicator(ABC):
    def __init__(self, data: pandas.DataFrame):
        self.data = data

    @abstractmethod
    def calculate(self) -> int:
        """
        Adds the calculated field to the dataframe parsed to the class.
        """
        pass