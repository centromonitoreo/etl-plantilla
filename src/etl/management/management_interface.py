from abc import ABC, abstractmethod
from typing import List
from etl.management.schemas.schemas import FeedDatabase # , UpdateDatabase

class ManagementInterface(ABC):
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def feed_database(
        self, data: List[FeedDatabase], **kwargs
    ) -> List[FeedDatabase]:
        """
        Esta funcion crea y devuelve solo los que creo, es decir los que no existian
        """
        pass

    @abstractmethod
    def validate_input(self, data: List[FeedDatabase], **kwargs) -> None:
        """
        Esta funcion valida el input
        """
        pass