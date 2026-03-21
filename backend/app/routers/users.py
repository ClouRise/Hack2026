import uuid

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.auth import (
    hash_password,
    generate_password,
    get_current_user,
    get_current_admin,
    verify_password,
    create_access_token,
    create_refresh_token
)
from app.schemas.users import (
    UpdateExistUser,
    UserSchema,
    CreateUser,
    CreateUserResponse
)
from app.models.user import User as UserModel, UserRole
from app.db.session import get_db
from app.core.config import settings


router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)

async def _get_login_credentials(request: Request) -> tuple[str, str]:
    content_type = request.headers.get("content-type", "").lower()

    if "application/json" in content_type:
        try:
            data = await request.json()
        except Exception as exc:
            raise HTTPException(status_code=422, detail="Некорректное тело запроса") from exc
        if not isinstance(data, dict):
            raise HTTPException(status_code=422, detail="Некорректное тело запроса")

        username = data.get("username") or data.get("email") or data.get("login")
        password = data.get("password")
    else:
        try:
            form = await request.form()
        except Exception as exc:
            raise HTTPException(status_code=422, detail="Некорректная форма запроса") from exc
        username = form.get("username") or form.get("email") or form.get("login")
        password = form.get("password")

    if not username or not password:
        raise HTTPException(
            status_code=422,
            detail="Передайте username/email/login и password",
        )

    return str(username), str(password)


@router.get("/me", response_model=UserSchema)
async def get_user_profile(
    current_user: UserModel = Depends(get_current_user)
):
    """Получить профиль текущего пользователя"""
    return current_user


@router.patch("/me", response_model=UserSchema)
async def update_user_profile(
    data: UpdateExistUser,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Обновить профиль текущего пользователя"""
    
    if data.phone is not None:
        current_user.phone = data.phone
    if data.photo_url is not None:
        current_user.photo_url = data.photo_url
    if data.bio is not None:
        current_user.bio = data.bio
    
    await db.commit()
    await db.refresh(current_user)
    
    return current_user


@router.post("/create", response_model=CreateUserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: CreateUser,
    current_admin: UserModel = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Создать нового психолога (только для админа)"""
    
    # Проверка существования email
    result = await db.execute(
        select(UserModel).where(UserModel.email == data.email)
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email уже зарегистрирован"
        )
    
    # Генерация временного пароля
    temp_password = generate_password(16)
    
    # Создание нового пользователя
    new_user = UserModel(
        email=data.email,
        hashed_password=hash_password(temp_password),
        name=data.name,
        phone=data.phone,
        role=UserRole.PSYCHOLOGIST
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return CreateUserResponse(
        user=UserSchema.model_validate(new_user),
        temp_password=temp_password
    )

@router.post("/login")
async def login(
    response: Response,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Вход в систему
    
    Возвращает access_token в теле ответа
    Refresh token сохраняется в httpOnly cookie
    """

    username, password = await _get_login_credentials(request)
    
    # Найти пользователя по email
    result = await db.execute(
        select(UserModel).where(UserModel.email == username)
    )
    user = result.scalar_one_or_none()
    
    # Проверить пароль
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Проверить блокировку
    if user.is_blocked:
        raise HTTPException(403, "Доступ заблокирован")
    
    # Создать Access Token
    access_token = create_access_token({"sub": user.email})
    
    # Создать Refresh Token
    refresh_token = await create_refresh_token(
        data={"user_id": user.id},
        db=db
    )
    
    # Установить Refresh Token в cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=settings.COOKIE_HTTPONLY,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.JWT_REFRESH_DAYS * 24 * 60 * 60,
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/psychologists", response_model=list[UserSchema])
async def get_psychologists(
    current_admin: UserModel = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Получить список всех психологов (только для админа)"""
    
    result = await db.execute(
        select(UserModel).where(UserModel.role == UserRole.PSYCHOLOGIST)
    )
    psychologists = result.scalars().all()
    
    return psychologists


@router.post("/{user_id}/block", response_model=UserSchema)
async def block_user(
    user_id: uuid.UUID,
    current_admin: UserModel = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Заблокировать пользователя (только для админа)"""
    
    user = await db.get(UserModel, user_id)
    
    if not user:
        raise HTTPException(404, "Пользователь не найден")
    
    if user.is_admin:
        raise HTTPException(400, "Нельзя заблокировать администратора")
    
    user.is_blocked = True
    await db.commit()
    await db.refresh(user)
    
    return user


@router.post("/{user_id}/unblock", response_model=UserSchema)
async def unblock_user(
    user_id: uuid.UUID,
    current_admin: UserModel = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Разблокировать пользователя (только для админа)"""
    
    user = await db.get(UserModel, user_id)
    
    if not user:
        raise HTTPException(404, "Пользователь не найден")
    
    user.is_blocked = False
    await db.commit()
    await db.refresh(user)
    
    return user
