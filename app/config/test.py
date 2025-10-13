from pydantic import BaseModel, HttpUrl
from app.env import env


class DatabaseConfig(BaseModel):
    url: HttpUrl | str = "sqlite+aiosqlite:///./test.db"
    logging: bool = False


class FeaturesConfig(BaseModel):
    enable_debug_routes: bool = False


class TestConfig(BaseModel):
    database: DatabaseConfig = DatabaseConfig()
    features: FeaturesConfig = FeaturesConfig()
