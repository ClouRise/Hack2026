import uuid
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base

if TYPE_CHECKING:
    from .test import Test
    from .answers import Answer
    

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    test_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="ID теста который проходит клиент"
    )

    client_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    client_extra: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
        comment="Дополнительные поля которые запросил психолог"
    )

    metrics: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        comment="Рассчитанные метрики по формулам"
    )

    progress: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Процент прохождения (0-100)"
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment="Когда начал тест"
    )

    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        comment="Когда завершил тест"
    )

    test: Mapped["Test"] = relationship(
        "Test",
        back_populates="sessions"
    )

    answers: Mapped[list["Answer"]] = relationship(
        "Answer",
        back_populates="session"
    )
