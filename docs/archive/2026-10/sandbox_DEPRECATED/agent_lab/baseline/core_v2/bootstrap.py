"""Bootstrap coordinator for AI_BRIDGE V2.

This module implements the AI_BRIDGE V2 bootstrap procedure. It acts as
a coordinator: the actual work is delegated to the specialized modules
of the ``core_v2`` package -- :mod:`core_v2.utils` for filesystem
checks and directory creation, :mod:`core_v2.telemetry` for logger
initialization, :mod:`core_v2.config` for configuration loading, and
:mod:`core_v2.exceptions` for the dedicated exception hierarchy.

This module depends exclusively on the Python standard library. It does
not import, read, or otherwise depend on anything from the legacy
``core/`` package or any other legacy file of the repository.
"""

from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from core_v2.config import load_configuration
from core_v2.constants import BANNER, MINIMUM_PYTHON_VERSION
from core_v2.exceptions import PythonVersionError
from core_v2.telemetry import initialize_logging
from core_v2.utils import ensure_directory_structure, resolve_repo_root


@dataclass(frozen=True)
class BootstrapContext:
    """Immutable snapshot of the environment produced by a successful
    bootstrap of AI_BRIDGE V2.

    Attributes:
        repo_root: Absolute path to the repository root.
        config_dir: Absolute path to the ``config_v2`` directory.
        data_dir: Absolute path to the ``data_v2`` directory.
        config: Parsed configuration loaded from ``config_v2``, as a
            dictionary with one top-level key per configuration section
            (``"system"``, ``"runtime"``, ``"market"``, ``"risk"``).
        logger: A fully configured :class:`logging.Logger` instance ready
            to be used by the rest of the AI_BRIDGE V2 system.
    """

    repo_root: Path
    config_dir: Path
    data_dir: Path
    config: dict[str, dict[str, Any]]
    logger: logging.Logger


def _check_python_version(
    minimum_version: tuple[int, int] = MINIMUM_PYTHON_VERSION,
) -> tuple[int, int, int]:
    """Validate that the running Python interpreter meets the minimum
    required version.

    Args:
        minimum_version: The minimum required ``(major, minor)`` version
            tuple. Defaults to :data:`core_v2.constants.MINIMUM_PYTHON_VERSION`.

    Returns:
        The ``(major, minor, micro)`` version tuple of the interpreter
        that is currently running.

    Raises:
        PythonVersionError: If the running interpreter is older than
            ``minimum_version``.
    """
    actual_version = (
        sys.version_info.major,
        sys.version_info.minor,
        sys.version_info.micro,
    )
    actual_major_minor = (actual_version[0], actual_version[1])

    if actual_major_minor < minimum_version:
        raise PythonVersionError(minimum_version, actual_version)

    return actual_version


def bootstrap() -> BootstrapContext:
    """Run the full AI_BRIDGE V2 bootstrap procedure.

    This is the single public entry point of this module. It performs,
    in order:

    1. Verifying the running Python interpreter version.
    2. Resolving the repository root.
    3. Ensuring the required directory structure exists.
    4. Initializing the AI_BRIDGE V2 logger.
    5. Printing the bootstrap banner.
    6. Loading the AI_BRIDGE V2 configuration.
    7. Logging success.
    8. Assembling and returning a :class:`BootstrapContext`.

    Any failure at any step raises a dedicated exception derived from
    :class:`~core_v2.exceptions.BootstrapError`; the function never
    returns a partially initialized context.

    Returns:
        A fully populated, immutable :class:`BootstrapContext` describing
        the environment that was just initialized.

    Raises:
        PythonVersionError: If the running interpreter is older than
            :data:`core_v2.constants.MINIMUM_PYTHON_VERSION`.
        DirectoryInitializationError: If a required directory cannot be
            verified, created, or used to initialize logging.
        ConfigurationNotFoundError: If any expected configuration file is
            missing or unreadable.
        ConfigurationParseError: If any configuration file is empty or
            cannot be parsed.
    """
    _check_python_version()

    repo_root = resolve_repo_root()
    config_dir, data_dir, _created_directories = ensure_directory_structure(repo_root)

    logger = initialize_logging(data_dir)

    print(BANNER)

    config = load_configuration(config_dir)

    logger.info("AI_BRIDGE V2 bootstrap completed successfully.")

    return BootstrapContext(
        repo_root=repo_root,
        config_dir=config_dir,
        data_dir=data_dir,
        config=config,
        logger=logger,
    )
