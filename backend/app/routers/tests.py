# routers/tests.py
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.auth import get_current_psychologist
from app.models.user import User
from app.models.test import Test
from app.models.sessions import Session
from app.services.test_io import (
    import_test, export_test, get_test_for_guest,
    save_session_answers, calculate_and_save_metrics
)
from fastapi.responses import StreamingResponse
from app.services.report_service import generate_guest_report, generate_psychologist_report

router = APIRouter()


# =====================================
# ТЕСТЫ для психолога
# =====================================

@router.post("/tests/import", status_code=status.HTTP_201_CREATED)
async def route_import_test(
    data: dict,
    db:   AsyncSession = Depends(get_db),
    user: User         = Depends(get_current_psychologist),
):
    """сохранение json в бд"""
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
    user:    User         = Depends(get_current_psychologist),
):
    """отправляет json со всеми полями(в том числе веса)"""
    try:
        data = await export_test(db, test_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return data


# =====================================
# тесты для гостей
# =====================================

@router.get("/guest/{access_link}")
async def route_get_test_for_guest(
    access_link: str,
    db:          AsyncSession = Depends(get_db),
):
    """отправляет json скрывая веса"""
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
    """создает сессию при сохранении ответов юзера"""
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
    """по сессии сохраняет ответы гостя"""
    try:
        await save_session_answers(db, session_id, data)
        db.expire_all()
        await calculate_and_save_metrics(db, session_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return {"ok": True}


@router.get("/guest/sessions/{session_id}/report")
async def route_guest_report(
    session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """docx отчет для гостя"""
    try:
        buf = await generate_guest_report(db, session_id)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=report_{session_id}.docx"},
    )

@router.get("/psychologist/sessions/{session_id}/report")
async def route_psychologist_report(
    session_id: uuid.UUID,
    db:   AsyncSession = Depends(get_db),
    user: User         = Depends(get_current_psychologist),
):
    """docx отчет для психолога"""
    try:
        buf = await generate_psychologist_report(db, session_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=report_{session_id}.docx"},
    )