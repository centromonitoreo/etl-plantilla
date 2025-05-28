from etl.management.email_imp.schemas.schemas import DataBaseMail, DataBaseAttachment
from etl.management.management_interface import ManagementInterface
from etl.management.email_imp.services.imp.default_mail_information_service_imp import TableMailInformationService
from etl.management.email_imp.models.mail_information import TableMailInformation
from etl.management.email_imp.models.attachment_information import TableAttachmentInformation
from etl.management.email_imp.config import SessionManager
from typing import List


class EmailImplement(ManagementInterface, default=True):
    """
    Class to implement the email information service interface.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


    def feed_database(self, data: List[DataBaseMail]) -> List[TableMailInformation]:
        created_records = []

        for item in data:
            email = TableMailInformationService().get_mail_information(
                expediente=item.expediente,
                date_receipt=item.date_receipt,
                subject=item.subject
            )

            if email:
                continue

            email = TableMailInformationService().create_mail_information(
                expediente=item.expediente,
                mail_from=item.mail_from,
                mail_to=item.mail_to,
                mail_copy_to=item.mail_copy_to,
                date_receipt=item.date_receipt,
                subject=item.subject,
                body=item.body,
                status=item.status
            )

            mail_id = email.id
            for att in item.attachment:
                if att.attachment_name and att.attachment_name != "":
                    attachment = TableMailInformationService().create_attachment_information(
                        mail_id=mail_id,
                        attachment_name=att.attachment_name,
                        file_format=att.file_format,
                        structure=att.structure,
                        attachment_path=att.attachment_path
                    )

            SessionManager().get_session().refresh(email)
            created_records.append(email)

        return created_records
    
    
    def validate_input(self, data: List[DataBaseMail], **kwargs) -> None:
        """
        Esta funcion valida el input
        """
        for item in data:
            if not isinstance(item, DataBaseMail):
                raise ValueError(f"Invalid data type: {type(item)}. Expected DataBaseMail.")