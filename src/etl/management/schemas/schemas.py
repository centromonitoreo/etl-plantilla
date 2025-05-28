from pydantic import BaseModel
from enum import Enum
from datetime import date
from typing import List, Union # Optional
from etl.management.email_imp.schemas.schemas import FeedDataBaseMail


# class DataSource(Enum):
#     correo = "correo"



class FeedDataBase(BaseModel):
    data : Union[FeedDataBaseMail]

# class UpdateDatabase(BaseModel):
#     date_receipt: date
#     resource: DataSource