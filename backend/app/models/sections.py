import uuid
from typing import TYPE_CHECKING, List
from sqlalchemy import Text, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base

if TYPE_CHECKING:
    from .test import Test
    from .question import Question

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

    test_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tests.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )


    test: Mapped["Test"] = relationship(
        "Test",
        back_populates="sections"
    )

    questions: Mapped[list["Question"]] = relationship(
        "Question",
        back_populates="section",
        order_by="Question.order_index",
    )