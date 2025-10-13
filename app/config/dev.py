from pydantic import BaseModel, HttpUrl


class DatabaseConfig(BaseModel):
    url: HttpUrl | str = "sqlite+aiosqlite:///./database.db"
    logging: bool = True


class FeaturesConfig(BaseModel):
    enable_debug_routes: bool = True


class DevConfig(BaseModel):
    database: DatabaseConfig = DatabaseConfig()
    features: FeaturesConfig = FeaturesConfig()
