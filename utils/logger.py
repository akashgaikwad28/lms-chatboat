import logging
import os
from logging.handlers import TimedRotatingFileHandler
import sys

def get_logger(name="lms_chatbot", log_level=logging.DEBUG):
    # Create logs folder if not exists
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Check if logger already has handlers
    if logger.hasHandlers():
        return logger

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)

    # File handler (rotates daily, keeps 7 backup files)
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(log_dir, "chatbot.log"),
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8",
        utc=True
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
