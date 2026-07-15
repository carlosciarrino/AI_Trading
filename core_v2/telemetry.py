"""Logging initialization for AI_BRIDGE V2.

This module contains the single AI_BRIDGE V2 logger configuration
routine, used by the bootstrap procedure to set up a logger that writes
simultaneously to standard output and to a log file inside the
``data_v2/logs`` directory.

This module depends exclusively on the Python standard library.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Final

from core_v2.exceptions import DirectoryInitializationError

#: Name of the logger used throughout AI_BRIDGE V2.
LOGGER_NAME: Final[str] = "ai_bridge_v2"

#: Name of the log file written inside ``data_v2/logs``.
LOG_FILE_NAME: Final[str] = "ai_bridge_v2.log"

#: Log message format shared by every handler attached to the logger.
_LOG_FORMAT: Final[str] = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

#: Timestamp format used in log messages.
_LOG_DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"


def initialize_logging(data_dir: Path) -> logging.Logger:
    """Initialize and configure the AI_BRIDGE V2 logger.

    The logger writes simultaneously to standard output and to a log
    file located at ``<data_dir>/logs/ai_bridge_v2.log``. Calling this
    function more than once (for example across repeated bootstrap
    attempts within the same process) does not duplicate log handlers:
    any handler previously attached by this function is removed first.

    Args:
        data_dir: Absolute path to the ``data_v2`` directory. The
            ``logs`` subdirectory inside it must already exist (see
            :func:`core_v2.utils.ensure_directory_structure`).

    Returns:
        The fully configured :class:`logging.Logger` instance, named
        after :data:`LOGGER_NAME`.

    Raises:
        DirectoryInitializationError: If the log file cannot be created
            or opened due to a filesystem error.
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    # Remove any handler previously attached by this function, so that
    # repeated calls within the same process do not duplicate log output.
    for existing_handler in list(logger.handlers):
        logger.removeHandler(existing_handler)
        existing_handler.close()

    formatter = logging.Formatter(fmt=_LOG_FORMAT, datefmt=_LOG_DATE_FORMAT)

    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    log_file_path = data_dir / "logs" / LOG_FILE_NAME
    try:
        file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    except OSError as exc:
        raise DirectoryInitializationError(log_file_path, str(exc)) from exc

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
