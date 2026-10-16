"""Dedicated exception hierarchy for AI_BRIDGE V2.

Every error that can occur during the AI_BRIDGE V2 bootstrap procedure
(and, going forward, in the rest of the ``core_v2`` package) is
represented here as a dedicated exception class deriving from
:class:`BootstrapError`. Centralizing every exception in a single module
lets other ``core_v2`` modules (``utils``, ``telemetry``, ``config``,
``bootstrap``) share the same error vocabulary without depending on each
other for exception definitions.

This module depends exclusively on the Python standard library.
"""

from __future__ import annotations

import json
from pathlib import Path


class BootstrapError(Exception):
    """Base class for every error raised by AI_BRIDGE V2 during bootstrap.

    All exceptions raised by ``core_v2`` bootstrap-related modules
    inherit from this class, so that callers can catch every possible
    bootstrap failure with a single ``except BootstrapError:`` clause,
    while still being able to catch a more specific subclass when
    finer-grained handling is required.
    """


class PythonVersionError(BootstrapError):
    """Raised when the running Python interpreter is older than required.

    Attributes:
        required_version: The minimum required ``(major, minor)`` version
            tuple.
        actual_version: The ``(major, minor, micro)`` version tuple of the
            interpreter that is actually running.
    """

    def __init__(
        self,
        required_version: tuple[int, int],
        actual_version: tuple[int, int, int],
    ) -> None:
        self.required_version = required_version
        self.actual_version = actual_version
        message = (
            f"AI_BRIDGE V2 requires Python >= "
            f"{required_version[0]}.{required_version[1]}, but the running "
            f"interpreter is {actual_version[0]}.{actual_version[1]}."
            f"{actual_version[2]}."
        )
        super().__init__(message)


class DirectoryInitializationError(BootstrapError):
    """Raised when a required directory cannot be verified or created.

    This typically indicates a filesystem permission problem or an
    unexpected obstruction (for example, a regular file existing where a
    directory is expected).

    Attributes:
        path: The filesystem path that could not be initialized.
        reason: A human-readable description of why initialization failed.
    """

    def __init__(self, path: Path, reason: str) -> None:
        self.path = path
        self.reason = reason
        message = f"Unable to initialize required directory '{path}': {reason}"
        super().__init__(message)


class ConfigurationError(BootstrapError):
    """Base class for every error related to loading the V2 configuration."""


class ConfigurationNotFoundError(ConfigurationError):
    """Raised when an expected configuration file does not exist or cannot
    be read.

    Attributes:
        path: The configuration file path that was expected.
        reason: A human-readable description of why the file is
            unavailable.
    """

    def __init__(self, path: Path, reason: str) -> None:
        self.path = path
        self.reason = reason
        message = f"Configuration file '{path}' is missing or unreadable: {reason}"
        super().__init__(message)


class ConfigurationParseError(ConfigurationError):
    """Raised when a configuration file exists but cannot be parsed.

    This is used both for strict JSON parsing errors and for errors
    raised by the naive ``key: value`` configuration parser used for the
    ``.yaml`` files in ``config_v2`` (see :mod:`core_v2.config`).

    Attributes:
        path: The configuration file path that failed to parse.
        original_error: The underlying error, when available. This is a
            :class:`json.JSONDecodeError` for strict JSON parsing
            failures, or ``None`` for errors raised by the naive
            configuration-line parser.
    """

    def __init__(
        self,
        path: Path,
        detail: str,
        original_error: json.JSONDecodeError | None = None,
    ) -> None:
        self.path = path
        self.original_error = original_error
        message = f"Configuration file '{path}' could not be parsed: {detail}"
        super().__init__(message)
