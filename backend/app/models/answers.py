import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy import ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base

if TYPE_CHECKING:
    from .sessions import Session
    from .question import Question

class Answer(Base):
    """Ответы юзеров"""
    __tablename__ = "answers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    value: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        comment="значение ответа"
    )

    weight: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Сохраненный вес ответа (для неизменности истории)"
    )

    answered_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default="now()",
        comment="Время ответа"
    )

    session: Mapped["Session"] = relationship(
        "Session",
        back_populates="answers"
    )
    
    question: Mapped["Question"] = relationship(
        "Question",
        back_populates="answers"
    )

    