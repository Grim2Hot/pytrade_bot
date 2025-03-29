from abc import ABC, abstractmethod
from typing import Any
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
    def calculate(self) -> Any:
        """
        Adds the calculated field to the dataframe parsed to the class.
        """
        pass