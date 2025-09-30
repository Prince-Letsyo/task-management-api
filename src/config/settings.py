from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # ensures .env is loaded


class Settings(BaseSettings):
    secret_key: str
    debug: bool = False
    version: str

    model_config = ConfigDict(env_file="///./.env")


settings = Settings()
