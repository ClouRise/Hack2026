import requests
from fastapi import APIRouter, HTTPException
from ..models.chat import AnswersRequest, ChatResponse
from ..services.gigachat import gigachat

router = APIRouter(prefix="/chat", tags=["chat"])


def build_prompt(answers: list[str]) -> str:
    joined = "\n".join([f"{i+1}. {a}" for i, a in enumerate(answers)])

    return f"""
Ты профессиональный психолог.
Проанализируй ответы пользователя и дай развернутый, поддерживающий и эмпатичный ответ.

Ответы пользователя:
{joined}

Сформируй:
- краткий анализ состояния
- возможные причины
- рекомендации
"""


@router.post("/", response_model=ChatResponse)
def chat(data: AnswersRequest):
    prompt = build_prompt(data.answers)

    # Используем метод chat_with_system_message нового клиента
    result = gigachat.chat_with_system_message(
        system_message="Ты психолог",
        user_message=prompt,
        model="GigaChat"
    )

    if not result or "choices" not in result:
        raise HTTPException(status_code=500, detail="Ошибка при генерации ответа")

    text = result["choices"][0]["message"]["content"]
    return ChatResponse(result=text)