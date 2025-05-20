from etl.management.schemas.schemas import FeedDatabase, FeedDatabaseMail
from etl.management.email_imp.services.mail_information_service_interface import MailInformationServiceInterface
from etl.management.email_imp.services.imp.default_mail_information_service_imp import TableMailInformationService
from etl.management.email_imp.models.mail_information import TableMailInformation
from etl.management.email_imp.models.attachment_information import TableAttachmentInformation
from etl.management.email_imp.config import SessionManager
from typing import List


class EmailImplement(MailInformationServiceInterface):
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
        date_receipt = [date.date_receipt for date in data]

        exist_mail = TableMailInformationService().get_mail_information( #####################33 AQUI
            expediente=data[0].expediente,
            date_receipt=date_receipt[0],
            subject=data[0].subject
        )
        exist_mail = [date.date_receipt for date in exist_mail]

        new_mail = [mail for mail in data if mail.date_receipt not in exist_mail]

        if not new_mail:
            return None
        
        created_emails = []
        for mail in new_mail:
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
    
    def create_mail_information(self, mail: dict) -> str:
        return self._service.create_mail_information(mail)

    def create_attachment_information(self, mail_id: str, attachments: list[dict]):
        return self._service.create_attachment_information(mail_id, attachments)

    def get_mail_information(self, expediente: str, date_receipt: str, subject: str) -> str | None:
        return self._service.get_mail_information(expediente, date_receipt, subject)
    
    def validate_input(self, data: List[FeedDatabase], **kwargs) -> None:
        """
        Esta funcion valida el input
        """
        pass
