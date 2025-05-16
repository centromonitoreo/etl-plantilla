from pydantic import BaseModel
from enum import Enum
from datetime import date
from typing import List # Optional

class DataSource(Enum):
    correo = "correo"


class FeedDatabase(BaseModel): # Yo estaba colocando lo de la plantilla, pero deben ser los del correo
    mail_from : str
    mail_to : str
    mail_copy_to : str
    date_receipt : date
    subject  : str
    body  : str
    status  : str
    number_attachments : int
    attachment_name : List[str]


class UpdateDatabase(BaseModel):
    date_receipt: date
    resource: DataSource