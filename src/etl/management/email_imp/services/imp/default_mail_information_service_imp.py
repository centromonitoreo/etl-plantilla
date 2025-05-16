from etl.management.email_imp.services.mail_information_service_interface import MailInformationServiceInterface
from etl.management.email_imp.models.mail_information import TableMailInformation
from etl.management.email_imp.config import SessionManager


class TableMailInformationService(MailInformationServiceInterface):
    def get_mail_information(self, mail_id: str) :
        """
        Retrieve a mail information record by its ID.
        """
        session = SessionManager.get_session()
        mail_info = session.query(TableMailInformation).filter_by(id=mail_id).first()
        # session.close() # Esto se usa ahi o abajo
        return mail_info

    def create_mail_information(self,
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