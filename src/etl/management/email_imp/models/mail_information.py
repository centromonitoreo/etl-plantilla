import uuid
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from etl.management.email_imp.config import Base, engine


class TableMailInformation(Base):
    __tablename__ = "mail_information"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    expediente = Column(String(255), nullable=False)
    mail_from = Column(String(255), nullable=False)
    mail_to = Column(String(255), nullable=False)
    mail_copy_to = Column(String(255), nullable=True)
    date_receipt = Column(Date, nullable=False)
    subject = Column(String(255), nullable=False)
    body = Column(String, nullable=False)
    status = Column(Integer, default=0)
    # Aca deberia tomar el nombre de la empresa o aqui viene el nombre del proyecto o algo asi
    # Tambien fuente de la que proviene, aunque es evidente que es correo por estar en esta estrategia

    attachment = relationship('TableAttachmentInformation', back_populates='mail')

Base.metadata.create_all(bind=engine)