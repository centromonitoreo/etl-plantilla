import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from etl.management.email_imp.config import Base, engine


class TableAttachmentInformation(Base):
    __tablename__ = "attachment_information"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mail_id = Column(UUID(as_uuid=True), ForeignKey('mail_information.id'), nullable=False)
    number_attachments = Column(Integer, nullable=False, default=0)
    attachment_name = Column(JSON, nullable=True)
    # Hay que crear una variable de donde se almacenan los archivos para leer y luego revisar la estructura dependiendo la extension
    # attachment_path = Column(JSON, nullable=True)

    mail = relationship('TableAttachmentInformation', back_populates='attachment')

Base.metadata.create_all(bind=engine)