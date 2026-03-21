import uuid
from typing import TYPE_CHECKING, List
from sqlalchemy import Text, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base

class Section(Base):
    __tablename__= "sections"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Номер секции"
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )