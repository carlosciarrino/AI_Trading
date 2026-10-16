"""Filesystem utilities for AI_BRIDGE V2.

This module contains every filesystem-related helper used by the
AI_BRIDGE V2 bootstrap procedure: resolving the repository root, and
verifying/creating the required top-level directory structure
(``config_v2`` and ``data_v2``, plus the required ``data_v2``
subdirectories).

This module depends exclusively on the Python standard library.
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

from core_v2.exceptions import DirectoryInitializationError

#: Name of the top-level configuration directory, relative to the repo root.
CONFIG_DIRECTORY_NAME: Final[str] = "config_v2"

#: Name of the top-level data directory, relative to the repo root.
DATA_DIRECTORY_NAME: Final[str] = "data_v2"

#: Subdirectories that must exist inside the data directory.
DATA_SUBDIRECTORIES: Final[tuple[str, ...]] = ("logs", "state")


def resolve_repo_root() -> Path:
    """Resolve the absolute path of the AI_BRIDGE V2 repository root.

    This module lives at ``<repo_root>/core_v2/utils.py``, so the
    repository root is exactly one directory above the ``core_v2``
    package directory.

    Returns:
        The absolute :class:`~pathlib.Path` of the repository root.
    """
    this_file = Path(__file__).resolve()
    core_v2_dir = this_file.parent
    repo_root = core_v2_dir.parent
    return repo_root


def ensure_directory(path: Path) -> bool:
    """Ensure that a single directory exists, creating it if necessary.

    Args:
        path: The directory path to verify or create.

    Returns:
        ``True`` if the directory did not exist and was created by this
        call, ``False`` if it already existed.

    Raises:
        DirectoryInitializationError: If ``path`` exists but is not a
            directory (for example, a regular file with the same name),
            or if the directory could not be created due to a filesystem
            error (for example, insufficient permissions).
    """
    if path.exists():
        if not path.is_dir():
            raise DirectoryInitializationError(
                path, "path exists but is not a directory"
            )
        return False

    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise DirectoryInitializationError(path, str(exc)) from exc

    return True


def ensure_directory_structure(
    repo_root: Path,
) -> tuple[Path, Path, tuple[Path, ...]]:
    """Verify that the required AI_BRIDGE V2 directory structure exists,
    creating any missing directory automatically.

    The required structure is:

    * ``<repo_root>/config_v2/``
    * ``<repo_root>/data_v2/``
    * ``<repo_root>/data_v2/logs/``
    * ``<repo_root>/data_v2/state/``

    Args:
        repo_root: Absolute path to the repository root, as returned by
            :func:`resolve_repo_root`.

    Returns:
        A three-element tuple ``(config_dir, data_dir, created_directories)``
        where ``config_dir`` and ``data_dir`` are the absolute paths of the
        two top-level directories, and ``created_directories`` lists every
        directory (top-level or nested) that did not exist before this
        call and was created automatically.

    Raises:
        DirectoryInitializationError: If any required directory cannot be
            verified or created. See :func:`ensure_directory`.
    """
    config_dir = repo_root / CONFIG_DIRECTORY_NAME
    data_dir = repo_root / DATA_DIRECTORY_NAME

    created_directories: list[Path] = []

    if ensure_directory(config_dir):
        created_directories.append(config_dir)

    if ensure_directory(data_dir):
        created_directories.append(data_dir)

    for subdirectory_name in DATA_SUBDIRECTORIES:
        subdirectory_path = data_dir / subdirectory_name
        if ensure_directory(subdirectory_path):
            created_directories.append(subdirectory_path)

    return config_dir, data_dir, tuple(created_directories)
