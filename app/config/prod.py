from pydantic import BaseModel, HttpUrl
from app.core.env import env


class DatabaseConfig(BaseModel):
    url: HttpUrl | str | None = env.DB_URL  # Use validated env variable
    logging: bool = False


class FeaturesConfig(BaseModel):
    enable_debug_routes: bool = False


class ProdConfig(BaseModel):
    database: DatabaseConfig = DatabaseConfig()
    features: FeaturesConfig = FeaturesConfig()
