from pydantic import BaseModel
from enum import Enum
from datetime import date
from typing import List, Union # Optional


# class DataSource(Enum):
#     correo = "correo"


class FeedDatabaseMail(BaseModel):
    mail_from : str
    mail_to : str
    mail_copy_to : str
    date_receipt : date
    subject  : str
    body  : str
    status  : str
    attachment_name : str
    file_format : str
    structure : str
    attachment_path : str

class FeedDatabase(BaseModel):
    data : Union[FeedDatabaseMail]

# class UpdateDatabase(BaseModel):
#     date_receipt: date
#     resource: DataSource