import re
import json
from loguru import logger
from app.config import config


def app_logger():
    """
    Configure Loguru logger with file sink, rotation, and sensitive data filter.
    """
    logger.add(
        "logs/app_{time:YYYY-MM-DD}.log",
        rotation="10 MB",
        retention="7 days",
        level=(
            "DEBUG" if config.env.get("ENV_MODE") in {"development", "test"} else "INFO"
        ),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {extra} | {message}",
        enqueue=True,
        compression="zip",
    )

    # Add JSON sink for structured logging
    def json_sink(message):
        record = message.record
        log_entry = {
            "time": record["time"].strftime("%Y-%m-%d %H:%M:%S"),
            "level": record["level"].name,
            "module": record["name"],
            "function": record["function"],
            "line": record["line"],
            "message": record["message"],
            "extra": record["extra"],
        }
        with open("logs/json.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    logger.add(json_sink, format="{message}")
    return logger


# Regex patterns
PASSWORD_PATTERN = re.compile(r"\b[Pp][Aa][Ss][Ss][Ww][Oo][Rr][Dd]\b", re.IGNORECASE)
TOKEN_PATTERN = re.compile(r"\b(token|api_key|secret|auth)\b", re.IGNORECASE)


def filter_sensitive(data):
    if isinstance(data, dict):
        for key in data:
            if PASSWORD_PATTERN.search(key):
                data[key] = "***"
            elif TOKEN_PATTERN.search(key):
                data[key] = "[REDACTED]"
    return data


main_logger = app_logger()
