import os
from dotenv import load_dotenv

load_dotenv()


class _Settings:
    DATABASE_USER = os.getenv("DB_USER")
    DATABASE_SECRET = os.getenv("DB_SECRET")
    DATABASE_HOST = os.getenv("DB_HOST")
    DATABASE_PORT = os.getenv("DB_PORT")
    DATABASE_NAME = os.getenv("DB_NAME")
    DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_SECRET}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"


settings = _Settings()
