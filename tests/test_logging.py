from pathlib import Path
from loguru import logger

from chat4me.utils.logging import setup_logging


def test_setup_logging_does_not_crash():
    setup_logging(level="DEBUG", log_file=None)
    logger.debug("test debug message")
    logger.info("test info message")
    logger.warning("test warning message")


def test_setup_logging_with_file(tmp_path: Path):
    log_file = str(tmp_path / "test.log")
    setup_logging(level="INFO", log_file=log_file)
    logger.info("file log test")
    assert Path(log_file).exists()


def test_setup_logging_default():
    setup_logging()
    logger.info("default setup works")
