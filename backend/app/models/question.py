import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Text, Integer, Boolean, ForeignKey, Enum, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base
import enum

if TYPE_CHECKING:
    from .test import Test
    from .answers import Answer
    from .formula import Formula


class QuestionType(str, enum.Enum):
    """Типы вопросов"""
    TEXT = "text"
    TEXTAREA = "textarea"
    SINGLE = "single"
    MULTIPLE = "multiple"
    YESNO = "yesno"
    NUMBER = "number"
    RANGE = "range"
    DATE = "date"
    TIME = "time"
    RATING = "rating"

question_metrics = Table(
        "question_metrics",
        Base.metadata,
        Column("question_id", UUID(as_uuid=True), ForeignKey("questions.id",ondelete="CASCADE"),primary_key=True, index=True),
        Column("formula_id", UUID(as_uuid=True), ForeignKey("formulas.id",ondelete="CASCADE"),primary_key=True, index=True)
    )


class Question(Base):
    __tablename__ = "questions"

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

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Текст вопроса"
    )

    type: Mapped[QuestionType] = mapped_column(
        Enum(QuestionType, name="question_type"),
        nullable=False,
        comment="Тип вопроса"
    )

    order_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
        comment="Порядковый номер"
    )

    section_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sections.id", ondelete="CASCADE"),
        nullable=False,
    )
    
    is_required: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Обязательный ли вопрос"
    )

    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
        comment="Конфигурация вопроса"
    )

    is_hidden: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Скрыт ли вопрос"
    )

    # Связи
    test: Mapped["Test"] = relationship(
        "Test",
        back_populates="questions"
    )

    answers: Mapped["Answer"] = relationship(
        "Answer",
        back_populates="question"
    )

    formulas: Mapped[list["Formula"]] = relationship(
        "Formula",
        secondary=question_metrics,
        back_populates="questions_id",
    )






    # Методы
    def __repr__(self) -> str:
        return f"<Question {self.order_index}: {self.text[:30]}>"

    @property
    def has_options(self) -> bool:
        """Есть ли у вопроса варианты ответа"""
        return self.type in [
            QuestionType.SINGLE,
            QuestionType.MULTIPLE,
            QuestionType.YESNO
        ]
    
    @property
    def options(self) -> list:
        """Получить варианты ответа"""
        if not self.has_options:
            return []
        return self.config.get("options", [])

    def validate_answer(self, answer: dict) -> bool:
        """Валидация ответа"""
        if self.type in [QuestionType.TEXT, QuestionType.TEXTAREA]:
            return isinstance(answer.get("value"), str)
        
        elif self.type == QuestionType.SINGLE:
            option_id = answer.get("option_id")
            valid_ids = [opt["id"] for opt in self.options]
            return option_id in valid_ids
        
        elif self.type == QuestionType.MULTIPLE:
            option_ids = answer.get("option_ids", [])
            valid_ids = [opt["id"] for opt in self.options]
            return all(opt_id in valid_ids for opt_id in option_ids)
        
        elif self.type == QuestionType.YESNO:
            return type(answer.get("value")) is bool
        
        elif self.type == QuestionType.NUMBER:
            value = answer.get("value")
            if not isinstance(value, (int, float)):
                return False
            
            min_val = self.config.get("min")
            max_val = self.config.get("max")
            
            if min_val is not None and value < min_val:
                return False
            if max_val is not None and value > max_val:
                return False
            
            return True
        
        elif self.type == QuestionType.RANGE:
            value = answer.get("value")
            if not isinstance(value, (int, float)):
                return False
            
            min_val = self.config.get("min", 0)
            max_val = self.config.get("max", 10)
            
            return min_val <= value <= max_val
        
        elif self.type == QuestionType.DATE:
            return isinstance(answer.get("value"), str)
        
        elif self.type == QuestionType.TIME:
            return isinstance(answer.get("value"), str)
        
        elif self.type == QuestionType.RATING:
            value = answer.get("value")
            if not isinstance(value, int):
                return False
            
            min_val = self.config.get("min", 1)
            max_val = self.config.get("max", 5)
            
            return min_val <= value <= max_val
        
        return False