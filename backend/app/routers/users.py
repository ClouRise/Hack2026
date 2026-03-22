import uuid

from app.core.email import send_new_psychologist_email
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import (
    hash_password,
    generate_password,
    get_current_user,
    get_current_admin,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    get_current_active_psychologist,
)
from fastapi import File, UploadFile
from app.core.image import save_image 

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
    data: UpdateExistUser = Depends(),
    photo: UploadFile | None = File(None),
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Обновить профиль текущего пользователя"""
    
    if data.phone is not None:
        current_user.phone = data.phone
    if data.bio is not None:
        current_user.bio = data.bio

    if photo is not None:
        current_user.photo_url = await save_image(photo, foldername="users")
    elif data.photo_url is not None:
        current_user.photo_url = data.photo_url

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
    
    await send_new_psychologist_email(email=data.email, name=data.name, password=temp_password)

    return CreateUserResponse(
        user=UserSchema.model_validate(new_user),
        temp_password=temp_password
    )

@router.post("/token")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Аутентифицирует пользователя и возвращает JWT токены.
    Refresh-токен сохраняется в httpOnly cookie.
    """
    result = await db.execute(
        select(UserModel).where(UserModel.email == form_data.username)
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.has_active_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Срок доступа истёк или аккаунт заблокирован",
        )
    
    
    access_token = create_access_token(data={"sub": user.email, "id": str(user.id)})
    
    refresh_token = await create_refresh_token(
        data={"user_id": user.id},
        db=db,
    )
    
    # Сохраняем refresh-токен в cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=settings.COOKIE_HTTPONLY,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=settings.JWT_REFRESH_DAYS * 24 * 60 * 60,
        path="/",
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=settings.COOKIE_HTTPONLY,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=settings.JWT_ACCESS_EXPIRE_MINUT * 60,  # 30 минут
        path="/",
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
async def refresh_token_endpoint(
    response: Response,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Обновляет пару токенов.
    Берёт старый refresh-токен из cookie, возвращает новый в cookie.
    """
    refresh_token = request.cookies.get("refresh_token")
    
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found in cookies",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await verify_refresh_token(db, refresh_token)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.has_active_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Срок доступа истёк или аккаунт заблокирован",
        )
    new_access_token = create_access_token(
        data={"sub": user.email, "id": str(user.id)}
    )
    
    new_refresh_token = await create_refresh_token(
        data={"user_id": user.id},
        db=db,
    )
    
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=settings.COOKIE_HTTPONLY,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=settings.JWT_REFRESH_DAYS * 24 * 60 * 60,
        path="/",
    )
    
    return {
        "access_token": new_access_token,
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
