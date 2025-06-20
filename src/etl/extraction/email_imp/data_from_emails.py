import os
from etl.extraction.extraction_interface import DataExtractionInterface
from outlook_manager import OutlookMailManager
from outlook_manager.models import MailQueryParams
import asyncio
from pathlib import Path
from etl.extraction.email_imp.config import FOLDERS_EMAIL, EXCLUDED_EXTS
from etl.management.email_imp.schemas.schemas import DataBaseMail, DataBaseAttachment
from etl.management.management_interface import ManagementInterface
from datetime import datetime


class DataExtractionEmails(DataExtractionInterface):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not hasattr(self, 'username') or not hasattr(self, 'password'):
            self.username = os.getenv("EMAIL_USERNAME")
            self.password = os.getenv("EMAIL_PASSWORD")
            if not self.username or not self.password:
                raise ValueError("EMAIL_USERNAME and EMAIL_PASSWORD environment variables must be set.")
  

    async def read_data(self, expediente:str = 'UNIDEFINED', folders_name:list = None,start_date=None, end_date=None, top=None) -> list:
        """
        Reads data from emails and returns a list of email data dictionaries.
        """
        if folders_name is None and FOLDERS_EMAIL is None:
            raise ValueError("No folders specified for email extraction. Please provide a list of folders or set FOLDERS_EMAIL in the configuration.")
        if folders_name is None:
            folders_name = FOLDERS_EMAIL

        query_params = MailQueryParams(
            start_date=start_date,
            end_date=end_date,
            top=top
        )
        mail_manager = OutlookMailManager(
            username=self.username,
            password=self.password
        )

        folders = mail_manager.get_folders()

        for folder in folders:
            if folder["displayName"] in folders_name:
                print(f"Processing folder: {folder['displayName']}")
                mail_manager.set_folder(folder["id"])
                messages = mail_manager.get_mails(query_params=query_params.to_query())
                self.get_data_mails(mail_manager, folder["displayName"], expediente, messages)

            elif folder["childFolderCount"] > 0 and folder["displayName"] in folders_name:
                child_folders = mail_manager.get_child_folders(folder["id"])
                
                for child_folder in child_folders:
                    mail_manager.set_folder(child_folder["id"])
                    messages = mail_manager.get_mails(query_params=query_params.to_query())
                    self.get_data_mails(mail_manager, os.path.join(folder["displayName"], child_folder["displayName"]), expediente, messages)


    def get_data_mails(self, mail_manager, folder, expediente, messages):
        """
        Processes the messages from a specific folder and returns a list of email data dictionaries.
        """
        email_data=[]
        for sort_mail in messages:
            email_info = DataBaseMail(
                    expediente=expediente,
                    mail_from=sort_mail["from"]["emailAddress"]["address"],
                    mail_to=[recipient["emailAddress"]["address"] for recipient in sort_mail["toRecipients"]],
                    mail_copy_to=[r["emailAddress"]["address"] for r in sort_mail.get("ccRecipients", [])],
                    date_receipt=datetime.fromisoformat(sort_mail["receivedDateTime"].replace("Z", "+00:00")),
                    subject=sort_mail.get("subject", "(Sin asunto)"),
                    body=sort_mail.get("bodyPreview", "(Sin cuerpo)"),
                    folder=folder,
                    has_attachments=sort_mail["hasAttachments"],
                    status=None,
                    attachment=[]
                )

            if sort_mail["hasAttachments"]:

                loop = asyncio.get_event_loop()
                tasks = []
                tasks.append(loop.create_task(mail_manager.get_attachments(
                    message_id=sort_mail["id"],
                    name_filter=None
                )))
                if tasks:
                    completed_tasks, _ = loop.run_until_complete(asyncio.wait(tasks))
                for completed in completed_tasks:
                    results = completed.result()
                    filtered = [
                        (nombre, file_bytes)
                        for (_, nombre, file_bytes) in results
                        if not nombre.lower().endswith(EXCLUDED_EXTS)
                    ]

                    for attachment_name, file_bytes in filtered:
                        file_format = Path(attachment_name).suffix[1:]
                        email_info.attachment.append(DataBaseAttachment(
                            attachment_name=attachment_name,
                            file_format=file_format,
                            attachment_data=file_bytes.read(),
                        ))

            ManagementInterface.create().feed_database([email_info])


    def validate_inputs(self):
        """
        Validates the inputs for the data extraction process.
        """
        if not self.username or not self.password:
            raise ValueError("Username and password must be provided.")
    