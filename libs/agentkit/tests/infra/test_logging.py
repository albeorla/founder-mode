import logging

from agentkit.infra.logging import setup_logging


def test_setup_logging() -> None:
    logger = setup_logging(level="DEBUG", name="test-logger")
    assert logger.level == logging.DEBUG
    assert logger.name == "test-logger"
    assert len(logger.handlers) > 0
