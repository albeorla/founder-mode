import logging
import sys
from pathlib import Path

from foundermode.config import settings


def setup_logging() -> None:
    """Configures the application-wide logging."""
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # Create logs directory
    log_dir = Path(".out")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "app.log"

    # Define formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File Handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)  # Always capture debug in file

    # Console Handler (less verbose by default)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    # Root Logger
    root_logger = logging.getLogger("foundermode")
    root_logger.setLevel(logging.DEBUG)  # Allow all logs to flow to handlers
    root_logger.addHandler(file_handler)
    # root_logger.addHandler(console_handler) # CLI already prints, maybe keep console log sparse or separate

    # Silence noisy libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)

    # Verify setup
    root_logger.debug("Logging initialized.")
