import os
from etl.extraction.extraction_interface import DataExtractionInterface
from outlook_manager import OutlookMailManager
from outlook_manager.models import MailQueryParams
import asyncio
from pathlib import Path


EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

class DataExtractionEmails(DataExtractionInterface):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = EMAIL_USERNAME
        self.password = EMAIL_PASSWORD

    def read_data(self, start_date=None, end_date=None, top=None) -> list:
        """
        Reads data from emails and returns a list of email data dictionaries.
        """
        query_params = MailQueryParams(
            start_date=start_date,
            end_date=end_date,
            top=top
        )
        mail_manager = OutlookMailManager(
            username=self.username,
            password=self.password
        )
        excluded_exts = ('.png', '.jpg', '.jpeg', '.gif')
        loop = asyncio.get_event_loop()
        folders = mail_manager.get_folders()
        email_data = []
        for folder in folders:
            mail_manager.set_folder(folder["id"])
        mails = mail_manager.get_mails(query_params=query_params.to_query())

        for sort_mail in mails:

            """
            Garantizar la lista con los diccionarios -> Mi data
            """

            attachment_name = None
            file_format = None
            file_bytes = None

            if sort_mail["hasAttachments"] is True:
                task  = loop.create_task(mail_manager.get_attachments(
                    message_id=sort_mail["id"],
                    name_filter=None
                ))

                completed_tasks, _ = loop.run_until_complete(asyncio.wait([task]))
                
                for completed in completed_tasks:
                    results = completed.result()
                    filtered = [
                        (nombre, file_bytes)
                        for (_, nombre, file_bytes) in results
                        if not nombre.lower().endswith(excluded_exts)
                    ]

                    if filtered:
                        attachment_name, file_bytes = filtered[0]
                        file_format = Path(attachment_name).suffix[1:]
                
                email_data.append({
                    "expediente": None,
                    "mail_from": sort_mail["from"]["emailAddress"]["address"],
                    "mail_to": [recipient["emailAddress"]["address"] for recipient in sort_mail["toRecipients"]],
                    "mail_copy_to": [r["emailAddress"]["address"] for r in sort_mail.get("ccRecipients", [])],
                    "date_receipt": sort_mail["receivedDateTime"],
                    "subject": sort_mail.get("subject", "(Sin asunto)"),
                    "body": sort_mail.get("bodyPreview", "(Sin cuerpo)"),
                    "folder": folder["displayName"],
                    "has_attachments": sort_mail["hasAttachments"],
                    "status": None,
                    "attachment_name": attachment_name,
                    "file_format": file_format,
                    "attachment_data": file_bytes,
                    "structure": None,
                    "label": None,
                    "attachment_path": None
                })
            
            elif sort_mail["hasAttachments"] is False:
                email_data.append({
                    "expediente": None,
                    "mail_from": sort_mail["from"]["emailAddress"]["address"],
                    "mail_to": [recipient["emailAddress"]["address"] for recipient in sort_mail["toRecipients"]],
                    "mail_copy_to": [r["emailAddress"]["address"] for r in sort_mail.get("ccRecipients", [])],
                    "date_receipt": sort_mail["receivedDateTime"],
                    "subject": sort_mail.get("subject", "(Sin asunto)"),
                    "body": sort_mail.get("bodyPreview", "(Sin cuerpo)"),
                    "folder": folder["displayName"],
                    "has_attachments": sort_mail["hasAttachments"],
                    "status": None,
                    "attachment_name": None,
                    "file_format": None,
                    "attachment_data": None,
                    "structure": None,
                    "label": None,
                    "attachment_path": None
                })
        raise NotImplementedError("This method should be implemented in a subclass.")

    def validate_inputs(self):
        """
        Validates the inputs for the data extraction process.
        """
        if not self.username or not self.password:
            raise ValueError("Username and password must be provided.")
