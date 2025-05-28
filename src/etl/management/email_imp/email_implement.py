from etl.management.email_imp.schemas.schemas import FeedDataBaseMail, DataBaseMail, DataBaseAttachment
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


    def feed_database(self, data: List[FeedDataBaseMail]) -> List[TableMailInformation]:
        created_records = []

        for item in data:
            email = TableMailInformationService().get_mail_information(
                expediente=item.mail.expediente,
                date_receipt=item.mail.date_receipt,
                subject=item.mail.subject
            )

            if not email:
                email = TableMailInformationService().create_mail_information(
                    expediente=item.mail.expediente,
                    mail_from=item.mail.mail_from,
                    mail_to=item.mail.mail_to,
                    mail_copy_to=item.mail.mail_copy_to,
                    date_receipt=item.mail.date_receipt,
                    subject=item.mail.subject,
                    body=item.mail.body,
                    status=item.mail.status
                )

            mail_id = email.id
            attachments = []

            for att in item.attachments:
                if att.attachment_name and att.attachment_name != "":
                    attachment = TableMailInformationService().create_attachment_information(
                        mail_id=mail_id,
                        attachment_name=att.attachment_name,
                        file_format=att.file_format,
                        structure=att.structure,
                        attachment_path=att.attachment_path
                    )
                    attachments.append(
                        DataBaseAttachment(
                            attachment_name=attachment.attachment_name,
                            file_format=attachment.file_format,
                            structure=attachment.structure,
                            attachment_path=attachment.attachment_path
                        )
                    )

            # Construir el esquema con los datos recién creados
            db_mail = DataBaseMail(
                expediente=email.expediente,
                mail_from=email.mail_from,
                mail_to=email.mail_to,
                mail_copy_to=email.mail_copy_to,
                date_receipt=email.date_receipt,
                subject=email.subject,
                body=email.body,
                status=email.status
            )

            created_records.append(
                FeedDataBaseMail(
                    mail=db_mail,
                    attachments=attachments
                )
            )

        return created_records
    
    
    def validate_input(self, data: List[FeedDataBaseMail], **kwargs) -> None:
        """
        Esta funcion valida el input
        """
        pass
