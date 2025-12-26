import logging
import sys


def setup_logging(
    level: str = "INFO",
    name: str = "agentkit",
    json_format: bool = False,
) -> logging.Logger:
    """Configures and returns a logger."""
    logger = logging.getLogger(name)
    logger.propagate = False

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)

    handler = logging.StreamHandler(sys.stdout)

    if json_format:
        # Simplified JSON-like format for now without extra deps
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": "%(message)s"}'
        )
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
