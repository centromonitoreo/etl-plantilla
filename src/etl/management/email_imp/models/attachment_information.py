import uuid
from sqlalchemy import Column, String, Date, ForeignKey, LargeBinary
from datetime import date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from etl.management.email_imp.config import Base, engine


class TableAttachmentInformation(Base):
    __tablename__ = "attachment_information"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mail_id = Column(UUID(as_uuid=True), ForeignKey('mail_information.id'), nullable=False)
    # number_attachments = Column(Integer, nullable=False, default=0)
    attachment_name = Column(String(255), nullable=True)
    file_format = Column(String(255), nullable=True)
    structure = Column(String(255), nullable=True) # Esta creo que deberia ser un enum
    attachment_data = Column(LargeBinary, nullable=True)
    label = Column(String(255), nullable=True)
    attachment_path = Column(String(255), nullable=True)
    create_at = Column(Date, nullable=False, default=date.today())
    update_at = Column(Date, nullable=True, default=date.today(), onupdate=date.today())

    mail = relationship('TableMailInformation', back_populates='attachment')

Base.metadata.create_all(bind=engine)