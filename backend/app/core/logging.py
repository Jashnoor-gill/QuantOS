import logging
from pathlib import Path

def setup_logging():
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("quantos")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers during reload
    if logger.handlers:
        return logger

    file_handler = logging.FileHandler(log_dir / "app.log")
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    )

    logger.addHandler(file_handler)

    return logger