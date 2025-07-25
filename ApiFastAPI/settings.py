from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    external_source_url: str

    class Config:
        env_file = ".env"
