import logging

from logging import Logger


def get_logger(name: str = "Asset Management Service Logger") -> Logger:
    """
    A simple logger instance for the application.

    Returns:
        Logger: The logger instance.
    """

    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)

        handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))

        logger.addHandler(handler)
        logger.propagate = False

    return logger
