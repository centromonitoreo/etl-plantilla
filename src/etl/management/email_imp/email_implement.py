from etl.management.schemas.schemas import FeedDatabase, FeedDatabaseMail
from etl.management.management_interface import ManagementInterface
from etl.management.email_imp.services.imp.default_mail_information_service_imp import TableMailInformationService
from etl.management.email_imp.models.mail_information import TableMailInformation
from etl.management.email_imp.models.attachment_information import TableAttachmentInformation
from etl.management.email_imp.config import SessionManager
from typing import List


class EmailImplement(ManagementInterface):
    """
    Class to implement the email information service interface.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def feed_database(self, data: List[FeedDatabaseMail]) -> List[TableMailInformation]:
        """
        Create a new mail information record in the database.
        """
        created_emails = []
        for mail in data:
            email = TableMailInformationService().get_mail_information(
                expediente=mail.expediente,
                date_receipt=mail.date_receipt,
                subject=mail.subject
                )
            if not email:
                email = TableMailInformationService().create_mail_information(
                    expediente=mail.expediente,
                    mail_from=mail.mail_from,
                    mail_to=mail.mail_to,
                    mail_copy_to=mail.mail_copy_to,
                    date_receipt=mail.date_receipt,
                    subject=mail.subject,
                    body=mail.body,
                    status=mail.status
                )
                created_emails.append(email)

            mail_id = email.id
            if mail.attachment_name is None or mail.attachment_name == "":
                continue  # No attachment to create
            else:
                attachment = TableMailInformationService().create_attachment_information(
                    mail_id=mail_id,
                    attachment_name=mail.attachment_name,
                    file_format=mail.file_format,
                    structure=mail.structure,
                    attachment_path=mail.attachment_path
                )
                # Opcional: almacenar attachments si lo necesitas

        return created_emails
    
    
    def validate_input(self, data: List[FeedDatabase], **kwargs) -> None:
        """
        Esta funcion valida el input
        """
        pass
