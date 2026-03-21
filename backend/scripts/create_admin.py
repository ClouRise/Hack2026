# scripts/create_admin.py

import argparse
import asyncio
import os
import sys
import time
from pathlib import Path
from app.core.config import settings

def _bootstrap_paths() -> tuple[Path, Path]:
    backend_dir = Path(__file__).resolve().parents[1]
    project_root = backend_dir.parent
    sys.path.insert(0, str(backend_dir))
    os.chdir(backend_dir)
    return project_root, backend_dir


PROJECT_ROOT, BACKEND_DIR = _bootstrap_paths()


def _reexec_into_venv_if_needed() -> None:
    if os.environ.get("_CREATE_ADMIN_REEXEC_DONE") == "1":
        return

    base_prefix = getattr(sys, "base_prefix", sys.prefix)
    in_venv = (sys.prefix != base_prefix) or bool(os.environ.get("VIRTUAL_ENV"))
    if in_venv:
        return

    # Windows использует Scripts/, не bin/
    if sys.platform == "win32":
        venv_python = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
    else:
        venv_python = PROJECT_ROOT / ".venv" / "bin" / "python"
    
    if not venv_python.exists():
        print(f"⚠️ venv python not found: {venv_python}", file=sys.stderr)
        return

    os.environ["_CREATE_ADMIN_REEXEC_DONE"] = "1"
    os.execv(
        str(venv_python),
        [str(venv_python), str(Path(__file__).resolve()), *sys.argv[1:]],
    )


_reexec_into_venv_if_needed()

# ✅ Настройка event loop для Windows + asyncpg
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

try:
    from sqlalchemy import select
    from sqlalchemy.exc import SQLAlchemyError
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Не найдены зависимости. Запусти скрипт через виртуалку проекта:\n"
        "  `.venv\\Scripts\\python.exe scripts\\create_admin.py` (Windows)\n"
        "  `.venv/bin/python scripts/create_admin.py` (Linux/Mac)\n"
    ) from exc

from app.auth import hash_password
from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models.user import User as UserModel, UserRole


# ══════════════════════════════════════════════
# RETRY-ЛОГИКА ДЛЯ ПОДКЛЮЧЕНИЯ К БД
# ══════════════════════════════════════════════

async def wait_for_db(max_retries: int = 10, delay: int = 2):
    """
    Ждёт готовности базы данных.
    Возвращает True если успешно, False если нет.
    """
    for attempt in range(max_retries):
        try:
            async with AsyncSessionLocal() as session:
                await session.execute(select(1))
                print(f"✅ Database connection successful (attempt {attempt + 1})")
                return True
        except Exception as e:
            print(f"⚠️ Database not ready (attempt {attempt + 1}/{max_retries}): {type(e).__name__}: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(delay)
            else:
                print(f"❌ Failed to connect after {max_retries} attempts")
                return False


# ══════════════════════════════════════════════
# ОСНОВНАЯ ЛОГИКА
# ══════════════════════════════════════════════

async def upsert_admin(
    *,
    email: str,
    password: str,
    name: str,
    reset_password: bool,
    promote: bool,
) -> None:
    # ✅ Сначала ждём подключения к БД
    if not await wait_for_db():
        raise RuntimeError("Не удалось подключиться к базе данных. Проверь:\n"
                          "  1. Запущен ли PostgreSQL?\n"
                          "  2. Правильный ли DATABASE_URL в .env?\n"
                          "  3. Существует ли база данных?")

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(UserModel).where(UserModel.email == email))
        user = result.scalar_one_or_none()

        if user:
            changed = False

            if user.role != UserRole.ADMIN:
                if not promote:
                    raise RuntimeError(
                        f"Пользователь {email} уже существует и не админ. "
                        "Запусти с флагом --promote чтобы сделать его админом."
                    )
                user.role = UserRole.ADMIN
                changed = True

            if reset_password:
                user.hashed_password = hash_password(password)
                changed = True

            if changed:
                await db.commit()
                print(f"✅ Обновлен админ: {email}")
            else:
                print(f"ℹ️ Админ {email} уже существует (без изменений)")
            return

        admin = UserModel(
            email=email,
            hashed_password=hash_password(password),
            name=name,
            role=UserRole.ADMIN,
            is_blocked=False,
        )
        db.add(admin)
        await db.commit()
        print(f"✅ Создан админ: {email} / {password}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create/update admin user")
    parser.add_argument("--email", default="admin@example.com")
    parser.add_argument("--password", default="admin123")
    parser.add_argument("--name", default="Admin")
    parser.add_argument(
        "--reset-password",
        action="store_true",
        help="Сбросить пароль на указанный (если пользователь уже существует)",
    )
    parser.add_argument(
        "--promote",
        action="store_true",
        help="Повысить роль до ADMIN (если пользователь уже существует)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    
    print(f"🔧 Creating admin: {args.email}")
    print(f"🔗 Database: {settings.DATABASE_URL[:50]}...")
    
    try:
        asyncio.run(
            upsert_admin(
                email=args.email,
                password=args.password,
                name=args.name,
                reset_password=args.reset_password,
                promote=args.promote,
            )
        )
        print("🎉 Done!")
    except Exception as exc:
        print(f"❌ ERROR: {exc.__class__.__name__}: {exc}", file=sys.stderr)
        
        # Показываем замаскированный DATABASE_URL для дебага
        try:
            url = str(settings.DATABASE_URL)
            if "://" in url and "@" in url:
                scheme, rest = url.split("://", 1)
                creds, after = rest.split("@", 1)
                user = creds.split(":", 1)[0] if ":" in creds else creds
                redacted = f"{scheme}://{user}:***@{after}"
                print(f"🔗 DB: {redacted}", file=sys.stderr)
        except Exception:
            pass
        
        # Советы по исправлению
        print("\n💡 Возможные решения:", file=sys.stderr)
        print("  1. Запусти PostgreSQL: `Start-Service postgresql-x64-15`", file=sys.stderr)
        print("  2. Проверь подключение: `psql -U hack2026user -d hack2026_db -h localhost`", file=sys.stderr)
        print("  3. Убедись что база создана: `CREATE DATABASE hack2026_db;`", file=sys.stderr)
        print("  4. Проверь .env: DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/db", file=sys.stderr)
        
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()