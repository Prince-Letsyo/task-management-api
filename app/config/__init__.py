from pydantic import BaseModel
from app.env import env
from .base import BaseConfig
from .dev import DevConfig
from .prod import ProdConfig
from .test import TestConfig


class Config(BaseModel):
    app_name: str
    enable_cors: bool
    log_level: str
    database: dict[str, str | bool]  # Using dict to allow flexible merging
    features: dict[str, bool]
    env: dict[str, str | int | bool]


# Environment-specific configurations
env_configs = {
    "development": DevConfig(),
    "production": ProdConfig(),
    "test": TestConfig(),
}

# Merge base config with environment-specific config
base_config = BaseConfig()
env_config = env_configs[env.ENV_MODE]

config = Config(
    app_name=base_config.app_name,
    enable_cors=base_config.enable_cors,
    log_level=base_config.log_level,
    database=env_config.database.model_dump(),
    features=env_config.features.model_dump(),
    env=env.model_dump(),
)

__all__ = ["config"]
