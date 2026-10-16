"""Configuration loading for AI_BRIDGE V2.

This module loads the AI_BRIDGE V2 configuration from the files listed
in :data:`core_v2.constants.CONFIG_SECTIONS`, inside ``config_v2``.

Important:
    No YAML parsing library is used, since AI_BRIDGE V2 depends
    exclusively on the Python standard library. Each file is read with a
    deliberately naive line-based parser that only understands flat
    ``key: value`` pairs, blank lines, and full-line comments starting
    with ``#``. It does not support YAML nesting, lists, multi-line
    strings, anchors, or any other YAML feature beyond a flat mapping of
    strings.

This module depends exclusively on the Python standard library.
"""

from __future__ import annotations

from pathlib import Path

from core_v2.constants import CONFIG_SECTIONS
from core_v2.exceptions import ConfigurationNotFoundError, ConfigurationParseError


def _parse_simple_config_file(path: Path) -> dict[str, str]:
    """Parse a single configuration file using the naive flat ``key:
    value`` parser described in the module docstring.

    Args:
        path: Absolute path to the configuration file to parse.

    Returns:
        A flat dictionary mapping each key found in the file to its
        stripped string value.

    Raises:
        ConfigurationNotFoundError: If the file does not exist or cannot
            be read.
        ConfigurationParseError: If the file is empty, or if a
            non-blank, non-comment line does not contain a ``:``
            separator.
    """
    if not path.exists():
        raise ConfigurationNotFoundError(path, "expected configuration file does not exist")

    try:
        raw_text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ConfigurationNotFoundError(path, str(exc)) from exc

    if raw_text.strip() == "":
        raise ConfigurationParseError(
            path, "file is empty: expected at least one 'key: value' line"
        )

    section_values: dict[str, str] = {}

    for line_number, raw_line in enumerate(raw_text.splitlines(), start=1):
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        if ":" not in line:
            raise ConfigurationParseError(
                path, f"line {line_number} has no ':' separator: '{raw_line}'"
            )

        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()

        if not key:
            raise ConfigurationParseError(
                path, f"line {line_number} has an empty key: '{raw_line}'"
            )

        section_values[key] = value

    return section_values


def load_configuration(config_dir: Path) -> dict[str, dict[str, str]]:
    """Load the full AI_BRIDGE V2 configuration from ``config_dir``.

    Every file listed in :data:`core_v2.constants.CONFIG_SECTIONS` is
    expected to already exist inside ``config_dir``: this function does
    not create default configuration files, it only reads what is
    already present.

    Args:
        config_dir: Absolute path to the ``config_v2`` directory.

    Returns:
        A dictionary with one top-level key per entry in
        :data:`core_v2.constants.CONFIG_SECTIONS` (``"system"``,
        ``"runtime"``, ``"market"``, ``"risk"``), each mapping to the
        flat dictionary of key/value string pairs parsed from the
        corresponding file.

    Raises:
        ConfigurationNotFoundError: If any of the expected configuration
            files is missing or unreadable.
        ConfigurationParseError: If any configuration file is empty or
            contains a line that cannot be parsed.
    """
    configuration: dict[str, dict[str, str]] = {}

    for section_name, file_name in CONFIG_SECTIONS.items():
        file_path = config_dir / file_name
        configuration[section_name] = _parse_simple_config_file(file_path)

    return configuration
