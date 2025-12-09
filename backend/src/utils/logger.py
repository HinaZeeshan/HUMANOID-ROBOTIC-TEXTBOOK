"""
Logging infrastructure for the Humanoid Robotics Book + RAG Chatbot project
"""
import logging
import sys
from typing import Optional
from logging.handlers import RotatingFileHandler
from pathlib import Path

from backend.src.config import settings


def setup_logger(
    name: str = "robotics_book_api",
    log_file: Optional[str] = None,
    level: int = None
) -> logging.Logger:
    """
    Set up a logger with both file and console handlers.

    Args:
        name: Name of the logger
        log_file: Path to the log file (optional)
        level: Logging level (defaults to DEBUG if settings.debug is True, otherwise INFO)

    Returns:
        Configured logger instance
    """
    # Determine log level based on settings
    if level is None:
        level = logging.DEBUG if settings.debug else logging.INFO

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent adding handlers multiple times
    if logger.handlers:
        return logger

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)

    # File handler (if log file is specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)

    return logger


# Create a default logger instance
logger = setup_logger()


def get_logger(name: str = "robotics_book_api") -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Name of the logger (defaults to "robotics_book_api")

    Returns:
        Configured logger instance
    """
    return setup_logger(name=name)


# Initialize the main application logger
app_logger = get_logger("app")
rag_logger = get_logger("rag")
content_logger = get_logger("content")
chat_logger = get_logger("chat")