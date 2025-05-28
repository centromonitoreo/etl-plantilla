from abc import ABC, abstractmethod
from typing import List
from etl.management.schemas.schemas import FeedDataBase # , UpdateDatabase

class ManagementInterface(ABC):
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def feed_database(
        self, data: List[FeedDataBase], **kwargs
    ) -> List[FeedDataBase]:
        """
        Esta funcion crea y devuelve solo los que creo, es decir los que no existian
        """
        pass

    @abstractmethod
    def validate_input(self, data: List[FeedDataBase], **kwargs) -> None:
        """
        Esta funcion valida el input
        """
        pass