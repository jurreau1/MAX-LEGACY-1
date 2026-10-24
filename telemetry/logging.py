"""Structured logging utilities."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional


def get_logger(name: str = "max-legacy", level: Optional[int] = None) -> logging.Logger:
    """Return a configured logger for application telemetry."""
    logger = logging.getLogger(name)
    if level is not None:
        logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.propagate = False
    return logger


def log_event(message: str, **context: Dict[str, Any]) -> None:
    logger = get_logger()
    if context:
        logger.info("%s | context=%s", message, context)
    else:
        logger.info(message)
