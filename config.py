from pydantic_settings import BaseSettings
from typing import List, Optional
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

class Settings(BaseSettings):
    BOT_TOKEN: str = "7836504683:AAHLbkLPxjJtJMtcKQNO-pAFbB_9jPudlMM"
    ADMIN_IDS: str = "353890607,8689976952,8293437517"
    DATABASE_URL: str = f"sqlite+aiosqlite:///{BASE_DIR / 'guarantor.db'}"
    SUPPORT_USERNAME: str = "@Support"
    PROXY_URL: Optional[str] = "http://47.81.56.193:8888"

    @property
    def admin_id_list(self) -> List[int]:
        return [int(x.strip()) for x in self.ADMIN_IDS.split(",") if x.strip().isdigit()]

    class Config:
        env_file = str(ENV_FILE)
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
