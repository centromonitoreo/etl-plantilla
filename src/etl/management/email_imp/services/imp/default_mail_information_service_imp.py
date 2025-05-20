from etl.management.email_imp.services.mail_information_service_interface import MailInformationServiceInterface
from etl.management.email_imp.models.mail_information import TableMailInformation
from etl.management.email_imp.models.attachment_information import TableAttachmentInformation
from etl.management.email_imp.config import SessionManager
from datetime import date
from typing import List


class TableMailInformationService(MailInformationServiceInterface):
    
    def get_mail_information(self, expediente: str, date_receipt: date, subject: str) -> List[TableMailInformation]:
        return SessionManager().get_session().query(TableMailInformation).filter(TableMailInformation.expediente == expediente,
                                                                               TableMailInformation.date_receipt == date_receipt,
                                                                               TableMailInformation.subject == subject).all()
    
    def create_mail_information(self,
                                expediente: str,
                                mail_from: str,
                                mail_to: str,
                                mail_copy_to: str,
                                date_receipt: str,
                                subject: str,
                                body: str,
                                status: int) -> TableMailInformation:
        """
        Create a new mail information record in the database.
        """
        new_mail_info = TableMailInformation(
            expediente=expediente,
            mail_from=mail_from,
            mail_to=mail_to,
            mail_copy_to=mail_copy_to,
            date_receipt=date_receipt,
            subject=subject,
            body=body,
            status=status
        )
        SessionManager().get_session().add(new_mail_info)
        SessionManager().get_session().commit()
        SessionManager().get_session().refresh(new_mail_info)
        return new_mail_info

    
    def create_attachment_information(self,
                                      mail_id: str,
                                      attachment_name : str,
                                      file_format : str,
                                      structure : str,
                                      attachment_path : str) -> TableAttachmentInformation:
        """
        Create a new attachment information record in the database.
        """
        new_attachment_info = TableAttachmentInformation(
            mail_id = mail_id,
            attachment_name = attachment_name,
            file_format = file_format,
            structure = structure,
            attachment_path = attachment_path
        )
        
        SessionManager().get_session().add(new_attachment_info)
        SessionManager().get_session().commit()
        SessionManager().get_session().refresh(new_attachment_info)
        return new_attachment_info