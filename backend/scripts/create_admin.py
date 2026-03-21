import argparse
import asyncio
import os
import sys
from pathlib import Path


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

    venv_python = PROJECT_ROOT / ".venv" / "bin" / "python"
    if not venv_python.exists():
        return

    os.environ["_CREATE_ADMIN_REEXEC_DONE"] = "1"
    os.execv(
        str(venv_python),
        [str(venv_python), str(Path(__file__).resolve()), *sys.argv[1:]],
    )


_reexec_into_venv_if_needed()

try:
    from sqlalchemy import select
    from sqlalchemy.exc import SQLAlchemyError
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Не найдены зависимости. Запусти скрипт через виртуалку проекта:\n"
        "  `.venv/bin/python backend/scripts/create_admin.py`\n"
        "или установи зависимости из `backend/requirements.txt`."
    ) from exc

from app.auth import hash_password
from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models.user import User as UserModel, UserRole


async def upsert_admin(
    *,
    email: str,
    password: str,
    name: str,
    reset_password: bool,
    promote: bool,
) -> None:
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
                print(f"OK: обновлен админ {email}")
            else:
                print(f"OK: админ {email} уже существует (без изменений)")
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
        print(f"OK: создан админ {email}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create/update admin user")
    parser.add_argument("--email", default="admin@example.com")
    parser.add_argument("--password", default="admin")
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
    except Exception as exc:
        print(f"ERROR: {exc.__class__.__name__}: {exc}", file=sys.stderr)
        try:
            url = settings.ASYNC_DATABASE_URL
            redacted = url
            if "://" in url and "@" in url:
                scheme, rest = url.split("://", 1)
                creds, after = rest.split("@", 1)
                user = creds.split(":", 1)[0] if ":" in creds else creds
                redacted = f"{scheme}://{user}:***@{after}"
            print(f"DB: {redacted}", file=sys.stderr)
        except Exception:
            pass
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
