from pydantic import BaseModel
from datetime import date


class DataBaseMail(BaseModel):
    expediente: str
    mail_from : str
    mail_to : str
    mail_copy_to : str
    date_receipt : date
    subject  : str
    body  : str
    status  : str


class DataBaseAttachment(BaseModel):
    # mail_id: str
    attachment_name: str
    file_format: str
    structure: str
    attachment_path: str


class FeedDataBaseMail(BaseModel):
    mail : DataBaseMail
    attachments: list[DataBaseAttachment] = []