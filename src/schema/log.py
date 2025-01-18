from pathlib import Path

from loguru import logger
from pydantic import BaseModel, DirectoryPath


class LoggingSettings(BaseModel):
    """Creates a Pydantic's base model for logging settings.

    Args:
        BaseModel (pydantic.BaseModel): Pydantic base model instance.
    """

    LOG_LEVEL: str
    LOG_PATH: DirectoryPath


log_settings = LoggingSettings(
    LOG_LEVEL="INFO",
    LOG_PATH=Path.cwd(),
)
logger.add(
    Path.joinpath(log_settings.LOG_PATH, "loguru.log"),
    rotation="1 day",
    retention="7 days",
    compression="zip",
    backtrace=True,
    diagnose=True,
    watch=True,
    mode="w",
)
