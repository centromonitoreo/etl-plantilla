from pydantic import BaseModel
from enum import Enum
from datetime import date
from typing import Optional

class DataSource(Enum):
    correo = "correo"


class FeedDatabase(BaseModel):
    expediente_number : str


class UpdateDatabase(BaseModel):
    radicado_number: str
    resource: DataSource