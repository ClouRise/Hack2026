# routers/tests.py
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.auth import get_current_user  # берём у коллеги
from app.models.user import User
from app.services.test_io import import_test, export_test, get_test_for_guest, save_session_answers

router = APIRouter()


# ══════════════════════════════════════════════
# ТЕСТЫ — для психолога
# ══════════════════════════════════════════════
from app.models.user import UserRole
async def get_current_user():
    return User(
        id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
        role=UserRole.PSYCHOLOGIST,
        email="test@test.com",
        hashed_password="",
        name="Test Psychologist",
    )

@router.post("/tests/import", status_code=status.HTTP_201_CREATED)
async def route_import_test(
    data: dict,
    db:   AsyncSession = Depends(get_db),
    user: User         = Depends(get_current_user),
):
    """Импорт теста из JSON — создаёт новую копию теста в БД."""
    try:
        test = await import_test(db, data, psychologist_id=user.id)
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Отсутствует обязательное поле: {e}",
        )
    return {"test_id": str(test.id), "access_link": test.access_link}


@router.get("/tests/{test_id}/export")
async def route_export_test(
    test_id: uuid.UUID,
    db:      AsyncSession = Depends(get_db),
    user:    User         = Depends(get_current_user),
):
    """Экспорт теста в JSON."""
    try:
        data = await export_test(db, test_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return data


# ══════════════════════════════════════════════
# ГОСТЕВОЕ ПРОХОЖДЕНИЕ
# ══════════════════════════════════════════════

@router.get("/guest/{access_link}")
async def route_get_test_for_guest(
    access_link: str,
    db:          AsyncSession = Depends(get_db),
):
    """Получить тест по ссылке — без весов и служебных полей."""
    try:
        data = await get_test_for_guest(db, access_link)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return data


@router.post("/guest/{access_link}/start", status_code=status.HTTP_201_CREATED)
async def route_start_session(
    access_link: str,
    guest_data:  dict,
    db:          AsyncSession = Depends(get_db),
):
    """
    Создаёт сессию для гостя перед началом прохождения.
    guest_data: {"client_name": "Миша", "client_extra": {...}}
    Возвращает session_id который фронт использует при отправке ответов.
    """
    from sqlalchemy import select
    from models.test import Test
    from models.sessions import Session

    result = await db.execute(
        select(Test).where(
            Test.access_link == access_link,
            Test.is_active   == True,
            Test.is_deleted  == False,
        )
    )
    test = result.scalar_one_or_none()
    if not test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тест не найден")

    session = Session(
        id=uuid.uuid4(),
        test_id=test.id,
        client_name=guest_data.get("client_name", ""),
        client_extra=guest_data.get("client_extra", {}),
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)

    return {"session_id": str(session.id)}


@router.post("/guest/sessions/{session_id}/answers", status_code=status.HTTP_201_CREATED)
async def route_save_answers(
    session_id: uuid.UUID,
    data:       dict,
    db:         AsyncSession = Depends(get_db),
):
    """Сохранить ответы гостя."""
    try:
        await save_session_answers(db, session_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return {"ok": True}