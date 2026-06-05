import os
import uuid
from pathlib import Path

from app.config import settings


def save_avatar(file_bytes: bytes, player_name: str) -> str:
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = "png"
    filename = f"{player_name}_{uuid.uuid4().hex[:8]}.{ext}"
    filepath = upload_dir / filename
    filepath.write_bytes(file_bytes)

    return f"/uploads/{filename}"