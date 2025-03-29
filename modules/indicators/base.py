from abc import ABC, abstractmethod
import pandas



class Indicator(ABC):
    def __init__(self, data: pandas.DataFrame):
        self.data = data

    @abstractmethod
    def calculate(self) -> pandas.DataFrame:
        """
        Adds the calculated field to the dataframe parsed to the class.
        """
        pass