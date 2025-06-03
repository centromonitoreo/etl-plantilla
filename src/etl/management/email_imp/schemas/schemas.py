from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime



class DataBaseAttachment(BaseModel):
    # mail_id: str
    attachment_name: Optional[str] = None
    file_format: Optional[str] = None
    attachment_data: Any = None
    structure: Optional[str] = None
    label: Optional[str] = None
    attachment_path: Optional[str] = None


class DataBaseMail(BaseModel):
    expediente: Optional[str] = None
    mail_from : str
    mail_to : List[str]
    mail_copy_to : Optional[List[str]] = None
    date_receipt : datetime
    subject  : str
    body  : str
    folder  : str
    has_attachments: bool
    status  : Optional[str] = None
    attachment: List[DataBaseAttachment]

