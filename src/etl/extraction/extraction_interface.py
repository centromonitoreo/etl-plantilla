from abc import ABC, abstractmethod
from typing import Union, List, Dict

class DataExtractionInterface(ABC):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def read_data(self) -> Union[List[Dict]]:
        pass

    @abstractmethod
    def validate_inputs(self) -> None:
        pass