from pydantic import BaseModel
from typing import List
from datetime import date



class DataBaseAttachment(BaseModel):
    # mail_id: str
    attachment_name: str
    file_format: str
    structure: str
    attachment_path: str


class DataBaseMail(BaseModel):
    expediente: str
    mail_from : str
    mail_to : str
    mail_copy_to : str
    date_receipt : date
    subject  : str
    body  : str
    status  : str
    attachment: List[DataBaseAttachment]

