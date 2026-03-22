from pathlib import Path
import uuid
from fastapi import UploadFile, HTTPException, status

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MEDIA_ROOT = BASE_DIR / "media"
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_IMAGE_SIZE = 2 * 1024 * 1024


async def save_image(file: UploadFile, foldername: str) -> str:
    """
    Сохраняет изображение в media/{foldername}/ и возвращает относительный URL.
    """
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Only JPG, PNG or WebP images are allowed")

    content = await file.read()

    if len(content) > MAX_IMAGE_SIZE:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Image is too large")

    extension = Path(file.filename or "").suffix.lower() or ".jpg"
    file_name = f"{uuid.uuid4()}{extension}"

    folder_path = MEDIA_ROOT / foldername
    folder_path.mkdir(parents=True, exist_ok=True)

    file_path = folder_path / file_name
    file_path.write_bytes(content)

    return f"/media/{foldername}/{file_name}"


async def delete_image(url: str) -> None:
    """
    Удаляет изображение по относительному URL.
    Не падает если файл не существует.
    """
    if not url:
        return

    relative_path = url.lstrip("/")
    file_path = BASE_DIR / relative_path

    if file_path.exists():
        file_path.unlink()