from abc import ABC, abstractmethod
from typing import List, ClassVar
from etl.management.schemas.schemas import FeedDataBase # , UpdateDatabase

class ManagementInterface(ABC):

    _registry: ClassVar[dict[str, type["ManagementInterface"]]] = {}
    _default:  ClassVar[type["ManagementInterface"] | None] = None
    _scanned:  ClassVar[bool] = False
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init_subclass__(cls, /, *, default: bool = False, **kw):
        super().__init_subclass__(**kw)
        ManagementInterface._registry[cls.__name__] = cls
        if default or ManagementInterface._default is None:
            ManagementInterface._default = cls


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

    @classmethod
    def create(cls, name: str | None = None, **kw) -> "ManagementInterface":
        target_cls = (
            cls._registry.get(name)
            if name else cls._default 
        )
        if target_cls is None:
            raise RuntimeError("No hay implementaciones registradas")
        return target_cls(**kw)