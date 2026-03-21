import uuid
import secrets
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import String, Text, DateTime, Boolean, Integer, ForeignKey

from app.db.base import Base

if TYPE_CHECKING:
    from .user import User
    from .question import Question
    from .sessions import Session
    from .formula import Formula
    from .sections import Section


class Test(Base):
    """ТЕСТ СОЗДАННЫЙ ПСИХОЛОГОМ"""
    __tablename__ = "tests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    psychologist_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True 
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    image_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True
    )

    access_link: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )    
    
    show_report_to_client: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Может ли клиент видеть отчёт после прохождения"
    )

    required_fields: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
        comment="Дополнительные обязательные поля для клиента"
    )

    total_completions: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Количество завершённых прохождений"
    )

    last_completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        comment="Дата последнего прохождения"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True, 
        comment="Активен ли тест"
    )
    
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        comment="Soft delete"
    )

    expire_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Связи
    psychologist: Mapped["User"] = relationship(
        "User",
        back_populates="tests"
    )

    sessions: Mapped[list["Session"]] = relationship(
        "Session",
        back_populates="test",
        cascade="all, delete-orphan"
    )

    questions: Mapped[list["Question"]] = relationship(
        "Question",
        back_populates="test",
        cascade="all, delete-orphan",
        order_by="Question.order_index"
    )

    formula: Mapped["Formula"] = relationship(
        "Formula",
        back_populates="test"
    )

    section: Mapped["Section"] = relationship(
        "Seqtion",
        back_populates="test"
    )


    # Методы
    def __repr__(self) -> str:
        return f"<Test {self.title}>"

    @staticmethod
    def generate_access_link() -> str:
        """Генерация уникальной ссылки"""
        return secrets.token_urlsafe(12)

    def increment_completions(self, completed_at: datetime):
        """Увеличить счётчик прохождений"""
        self.total_completions += 1
        self.last_completed_at = completed_at

    @property
    def full_access_link(self) -> str:
        """Полная ссылка для клиента"""
        return f"https://profdna.com/test/{self.access_link}"