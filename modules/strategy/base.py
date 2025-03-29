import pandas
from abc import ABC, abstractmethod



class Strategy(ABC):
    def __init__(self, data : pandas.DataFrame, indicators : list = None):
        raise NotImplementedError("This is an abstract class. Please implement the methods in a subclass.")
    
    @abstractmethod
    def get_signal(self):
        raise NotImplementedError("This is an abstract class. Please implement the methods in a subclass.")