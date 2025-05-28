from etl.management.management_interface import ManagementInterface
from etl.management.email_imp.schemas.schemas import DataBaseMail, DataBaseAttachment
from datetime import date


mail = DataBaseMail(
    expediente="12345",
    mail_from="sergio",
    mail_to="jhon",
    mail_copy_to="jane",
    date_receipt=date(2026, 12,30),
    subject="Test Subject",
    body="This is a test email body.",
    status="received",  
    attachment=[
        DataBaseAttachment(
            attachment_name="file1.txt",
            file_format="txt",
            structure="text/plain",
            attachment_path="/path/to/file1.txt"
        ),
        DataBaseAttachment(
            attachment_name="file2.pdf",
            file_format="pdf",
            structure="application/pdf",
            attachment_path="/path/to/file2.pdf"
        )
    ]
)



implement = ManagementInterface.create()
created_records = implement.feed_database([mail])
print('Holi')