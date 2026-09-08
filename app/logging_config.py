import logging
import os

from logging.handlers import RotatingFileHandler

from app.config import settings


def setup_logging() -> None:

    log_level = getattr(
        logging,
        settings.log_level.upper(),
        logging.INFO,
    )

    formatter = logging.Formatter(settings.log_format)

    handlers: list[logging.Handler] = []

    if settings.log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        handlers.append(console_handler)

    if settings.log_to_file:
        log_directory = os.path.dirname(settings.log_file)

        if log_directory:
            os.makedirs(log_directory, exist_ok=True)

        file_handler = RotatingFileHandler(
            settings.log_file,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    root_logger = logging.getLogger()


    if root_logger.handlers:
        root_logger.handlers.clear()

    root_logger.setLevel(log_level)

    for handler in handlers:
        root_logger.addHandler(handler)

    logging.getLogger(settings.log_name).info(
        "Logging initialized | level=%s | console=%s | file=%s",
        settings.log_level,
        settings.log_to_console,
        settings.log_to_file,
    )
