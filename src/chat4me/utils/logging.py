import sys
from pathlib import Path

from loguru import logger


def setup_logging(level: str = "INFO", log_file: str | None = "chat4me.log") -> None:
    logger.remove()

    logger.add(
        sys.stderr,
        level=level.upper(),
        format="<green>{time:HH:mm:ss}</green> | <level>{level:<7}</level> | <cyan>{module}</cyan> | <level>{message}</level>",
        colorize=True,
    )

    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            str(log_path),
            level=level.upper(),
            format="{time:YYYY-MM-DD HH:mm:ss} | {level:<7} | {module} | {message}",
            rotation="10 MB",
            retention=5,
        )


def get_logger() -> logger:
    return logger
