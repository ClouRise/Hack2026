import uuid
from typing import TYPE_CHECKING, List
from sqlalchemy import Text, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base
import enum
from .question import Question, question_metrics
if TYPE_CHECKING:
    from .test import Test
    

class QuestionType(str, enum.Enum):
    """Типы операций"""
    SUM_O = "sum"
    AVG_O = "avg"
    MIN_O = "min"
    MAX_O = "max"
    PERCENT_O = "percent"

class Formula(Base):
    """Формулы для подсчета метрик"""
    __tablename__ = "formulas"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    test_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tests.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Название метрики",
    )

    expression: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Формула"
    )

    ranges: Mapped[List] = mapped_column(
        JSONB,
        default=list,
        comment="Диапазоны для интерпретации"
    )

    coefficient: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="множитель"
    )

    test: Mapped["Test"] = relationship(
        "Test",
        back_populates="formula"
    )

    questions_id: Mapped[list["Question"]] = relationship(
        "Question",
        secondary=question_metrics,
        back_populates="formulas",
    )