from abc import ABC, abstractmethod
from datetime import date
from etl.management.email_imp.models.mail_information import TableMailInformation
from etl.management.email_imp.models.attachment_information import TableAttachmentInformation


class MailInformationServiceInterface(ABC):

    @abstractmethod
    def create_mail_information(self,
                                expediente : str,
                                mail_from : str,
                                mail_to : str,
                                mail_copy_to : str,
                                date_receipt : date,
                                subject : str,
                                body: str,
                                folder : str,
                                has_attachments : bool,
                                status : str) -> TableMailInformation:
        """
        Create a new mail information record in the database.
        """
        pass

    @abstractmethod
    def create_attachment_information(self,
                                      mail_id: str,
                                      attachment_name : str,
                                      file_format : str,
                                      attachment_data : bytes,
                                      structure : str,
                                      label : str,
                                      attachment_path : str) -> TableAttachmentInformation:
        """
        Create a new attachment information record in the database.
        """
        pass

    @abstractmethod
    def get_mail_information(self, mail_id: str) -> TableMailInformation:
        """
        Retrieve a mail information record by its ID.
        """
        pass








