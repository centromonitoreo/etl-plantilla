from etl.management.email_imp.services.mail_information_service_interface import MailInformationServiceInterface
from etl.management.email_imp.models.mail_information import TableMailInformation
from etl.management.email_imp.models.attachment_information import TableAttachmentInformation
from etl.management.email_imp.config import SessionManager
from sqlalchemy.orm import Session, joinedload, aliased
from datetime import datetime
from typing import List, Optional


class TableMailInformationService(MailInformationServiceInterface):
    
    def get_mail_information(
        self,
        expediente: Optional[str] = None,
        date_receipt: Optional[datetime] = None,
        subject: Optional[str] = None,
        file_format: Optional[List[str]] = None
    ) -> List[TableMailInformation]:

        session: Session = SessionManager().get_session()

        # Aliased para la tabla adjuntos
        Attachment = aliased(TableAttachmentInformation)

        query = session.query(TableMailInformation).join(
            Attachment,
            TableMailInformation.id == Attachment.mail_id
        )

        # Filtros básicos sobre mails
        if expediente is not None:
            query = query.filter(TableMailInformation.expediente == expediente)
        if date_receipt is not None:
            query = query.filter(TableMailInformation.date_receipt == date_receipt)
        if subject is not None:
            query = query.filter(TableMailInformation.subject == subject)

        # Filtro directo sobre adjuntos (si file_format dado)
        if file_format:
            if not isinstance(file_format, (list, tuple, set)):
                file_format = [file_format]
            query = query.filter(Attachment.file_format.in_(file_format))

        # Evitar mails duplicados (por múltiples adjuntos)
        query = query.distinct()

        # Opcional: cargar adjuntos con joinedload para no hacer lazy load después
        query = query.options(joinedload(TableMailInformation.attachments))

        mails = query.all()

        # Finalmente, opcionalmente filtrar adjuntos en Python para que solo queden los que cumplen file_format
        if file_format:
            for mail in mails:
                mail.attachments = [att for att in mail.attachments if att.file_format in file_format]

        return mails
    
    def create_mail_information(self,
                                expediente: str,
                                mail_from: str,
                                mail_to: str,
                                mail_copy_to: str,
                                date_receipt: str,
                                subject: str,
                                body: str,
                                folder: str,
                                has_attachments: bool,
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
            folder=folder,
            has_attachments=has_attachments,
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
                                      attachment_data : bytes,
                                      structure : str,
                                      label : str,
                                      attachment_path : str) -> TableAttachmentInformation:
        """
        Create a new attachment information record in the database.
        """
        new_attachment_info = TableAttachmentInformation(
            mail_id = mail_id,
            attachment_name = attachment_name,
            file_format = file_format,
            attachment_data = attachment_data,
            structure = structure,
            label = label,
            attachment_path = attachment_path
        )
        
        SessionManager().get_session().add(new_attachment_info)
        SessionManager().get_session().commit()
        SessionManager().get_session().refresh(new_attachment_info)
        return new_attachment_info