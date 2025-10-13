from pydantic import BaseModel


class BaseConfig(BaseModel):
    app_name: str = "Task Management API"
    enable_cors: bool = True
    log_level: str = "info"
