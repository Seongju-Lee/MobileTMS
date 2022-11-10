import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_TITLE: str = "WatsonTMS"
    PROJECT_VERSION: str = "1.0.0"

    
    DB_USER: str = os.getenv("DB_USER")
    DB_PW: str = os.getenv("DB_PW")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", 5432)
    DB_NAME: str = os.getenv("DB_NAME", "ready")

    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 18000


settings = Settings()
