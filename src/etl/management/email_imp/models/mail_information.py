import uuid
from sqlalchemy import Column, String, DateTime
from datetime import timezone
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from etl.management.email_imp.config import Base, engine


class TableMailInformation(Base):
    __tablename__ = "mail_information"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    expediente = Column(String(255), nullable=True)
    mail_from = Column(String(255), nullable=False)
    mail_to = Column(ARRAY(String), nullable=False)
    mail_copy_to = Column(ARRAY(String), nullable=False)
    date_receipt = Column(DateTime(timezone=True), nullable=False)
    subject = Column(String(255), nullable=False)
    body = Column(String, nullable=False)
    folder = Column(String(255), nullable=False)
    has_attachments = Column(String(255), nullable=False)
    status = Column(String, nullable=True)

    attachments = relationship('TableAttachmentInformation', back_populates='mail')

Base.metadata.create_all(bind=engine)