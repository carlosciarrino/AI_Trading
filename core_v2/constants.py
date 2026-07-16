"""Shared constants for AI_BRIDGE V2.

This module centralizes the constants used by :mod:`core_v2.config` and
:mod:`core_v2.bootstrap`. It does not duplicate the constants already
defined inside :mod:`core_v2.utils` (``CONFIG_DIRECTORY_NAME``,
``DATA_DIRECTORY_NAME``, ``DATA_SUBDIRECTORIES``) or
:mod:`core_v2.telemetry` (``LOGGER_NAME``, ``LOG_FILE_NAME``): those two
modules already own their constants and are not modified by this
reconstruction.

This module depends exclusively on the Python standard library.
"""

from __future__ import annotations

from typing import Final

#: Minimum Python version required to run AI_BRIDGE V2, as (major, minor).
MINIMUM_PYTHON_VERSION: Final[tuple[int, int]] = (3, 10)

#: ASCII banner printed at the beginning of every bootstrap.
BANNER: Final[str] = (
    "\n"
    "==============================================================\n"
    "   AI_BRIDGE V2 - Trading Operating System (Bootstrap)\n"
    "==============================================================\n"
)

#: Mapping between the configuration section name (used as a top-level
#: key in the configuration dictionary returned by
#: :func:`core_v2.config.load_configuration`) and the file name, inside
#: ``config_v2``, that provides that section.
CONFIG_SECTIONS: Final[dict[str, str]] = {
    "system": "system.yaml",
    "runtime": "runtime.yaml",
    "market": "market.yaml",
    "risk": "risk.yaml",
}
