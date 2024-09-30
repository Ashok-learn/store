import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1")
    API_PREFIX: str = os.getenv('API_PREFIX')

settings = Settings()