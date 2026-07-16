"""Market engine for AI_BRIDGE V2.

The market engine is responsible for exposing normalized market
information to the rest of the system.

Current responsibilities:

- Load market-related configuration.
- Maintain the list of watched symbols.
- Maintain broker definitions.
- Report whether the market engine is available.
- Provide a future extension point for live market updates.

Only the Python standard library is used.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Broker:
    """Broker definition loaded from configuration."""

    name: str
    platform: str
    connection_type: str
    terminal_path: str
    account_id: str
    enabled: bool


@dataclass
class MarketSnapshot:
    """Latest market snapshot."""

    market_open: bool = False
    update_counter: int = 0


@dataclass
class MarketEngine:
    """AI_BRIDGE V2 market engine."""

    configuration: dict[str, str]

    watched_symbols: list[str] = field(default_factory=list)
    brokers: list[Broker] = field(default_factory=list)
    snapshot: MarketSnapshot = field(default_factory=MarketSnapshot)

    def initialize(self) -> None:
        """Load symbols and broker definitions."""

        self._load_symbols()
        self._load_brokers()
        self.snapshot.market_open = True

    def _load_symbols(self) -> None:
        """Load watched symbols."""

        count = int(self.configuration.get("watched_symbols_count", "0"))

        self.watched_symbols.clear()

        for index in range(1, count + 1):
            symbol = self.configuration.get(f"symbol_{index}")

            if symbol:
                self.watched_symbols.append(symbol)

    def _load_brokers(self) -> None:
        """Load broker definitions."""

        count = int(self.configuration.get("broker_count", "0"))

        self.brokers.clear()

        for index in range(1, count + 1):
            broker = Broker(
                name=self.configuration.get(f"broker_{index}_name", ""),
                platform=self.configuration.get(f"broker_{index}_platform", ""),
                connection_type=self.configuration.get(
                    f"broker_{index}_connection_type", ""
                ),
                terminal_path=self.configuration.get(
                    f"broker_{index}_terminal_path", ""
                ),
                account_id=self.configuration.get(
                    f"broker_{index}_account_id", ""
                ),
                enabled=self.configuration.get(
                    f"broker_{index}_enabled", "false"
                ).lower() == "true",
            )

            self.brokers.append(broker)

    def update(self) -> None:
        """Perform one market update cycle."""

        self.snapshot.update_counter += 1

    def is_ready(self) -> bool:
        """Return True if the engine is initialized."""

        return self.snapshot.market_open

    def get_symbols(self) -> list[str]:
        """Return watched symbols."""

        return list(self.watched_symbols)

    def get_brokers(self) -> list[Broker]:
        """Return broker definitions."""

        return list(self.brokers)
