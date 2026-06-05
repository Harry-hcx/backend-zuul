from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    db_path: str = str(BASE_DIR / "game.db")

    upload_dir: str = str(BASE_DIR / "uploads")

    @property
    def database_url(self) -> str:
        return f"sqlite+aiosqlite:///{self.db_path}"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()