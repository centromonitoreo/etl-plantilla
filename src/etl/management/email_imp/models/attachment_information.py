import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, LargeBinary
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from etl.management.email_imp.config import Base, engine


class TableAttachmentInformation(Base):
    __tablename__ = "attachment_information"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mail_id = Column(UUID(as_uuid=True), ForeignKey('mail_information.id'), nullable=False)
    # number_attachments = Column(Integer, nullable=False, default=0)
    attachment_name = Column(String(255), nullable=True)
    file_format = Column(String(255), nullable=True)
    structure = Column(ARRAY(String), nullable=True)
    attachment_data = Column(LargeBinary, nullable=True)
    label = Column(String(255), nullable=True)
    attachment_path = Column(String(255), nullable=True)
    create_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    update_at = Column(DateTime(timezone=True), nullable=True, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    mail = relationship('TableMailInformation', back_populates='attachments')

Base.metadata.create_all(bind=engine)