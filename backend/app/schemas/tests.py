import uuid
from typing import List, Optional, Dict
from datetime import datetime

from pydantic import BaseModel, Field

class CreateTest(BaseModel):
    title: str = Field(max_length=255, description="Заголовок или название теста")
    description: Optional[str] = Field(max_length=500, description="Описание или рецензия курса") #собственное ограничение в 500 символов
    image_url: Optional[str] = Field(max_length=500, description="Фотографии или аватарка")
    access_link: str = Field(max_length=100, description="Ссылка на курс для участников")
    show_report_to_client: bool = Field(default=True, description="Может ли участник видеть отчёт после прохождения теста")
    is_active: bool = Field(default=True, description="Является ли тест аквтиным при создании")
    is_deleted: bool = Field(default=False, description="Является ли тест удалённым на данный момент")
    # expire_time - хз, надо ли его указывать при создании или нет, можно сразу при создании вычислять по сценарию какому-нибудь
    expire_time: Optional[datetime] = Field(description="Время существования теста")



class TestSchema(BaseModel):
    id: uuid.UUID = Field(description="Id пользователя")
    psychologist_id: uuid.UUID = Field(description="ID создателя теста")
    title: str = Field(max_length=255, description="Заголовок или название теста")
    description: Optional[str] = Field(max_length=500, description="Описание или рецензия курса") #собственное ограничение в 500 символов
    image_url: Optional[str] = Field(max_length=500, description="Фотографии или аватарка")
    access_link: str = Field(max_length=100, description="Ссылка на курс для участников")
    show_report_to_client: bool = Field(default=True, description="Может ли участник видеть отчёт после прохождения теста")
    required_fields: Optional[Dict] = Field(default={}, description="Дополнительный поля в тесте") #по умолчанию - пустой словарь!!!!! Если надо - подправьте!!!!!!
    total_completions: int = Field(default=0, description="Количество прохождений конкреного теста")
    last_completed_at: Optional[datetime] = Field(description="Время последнего прохождения")
    created_at: datetime = Field(description="Время создания теста")
    is_active: bool = Field(default=True, description="Является ли тест аквтиным при создании")
    is_deleted: bool = Field(default=False, description="Является ли тест удалённым на данный момент")
    expire_time: Optional[datetime] = Field(description="Сколько тест будет существовать")