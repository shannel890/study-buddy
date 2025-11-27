import logging
from logging import Logger
from typing import Optional

LOG_FILE = "study_buddy.log"


def setup_logger(name: Optional[str] = None) -> Logger:
    """Configure and return a logger writing to `study_buddy.log`.

    If the logger already has handlers, do not add another handler (prevents duplicates).
    """
    logger_name = name or __name__
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    fh = logging.FileHandler(LOG_FILE)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    # Also ensure exceptions are visible on stderr during development
    sh = logging.StreamHandler()
    sh.setLevel(logging.ERROR)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    return logger
