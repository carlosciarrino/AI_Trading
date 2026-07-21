"""
Learning engine for AI_BRIDGE V2.
The learning engine analyses historical runtime information and
produces simple learning reports.
This baseline implementation performs only basic statistical analysis
without modifying the behaviour of the trading system.
Only the Python standard library is used.
"""
from __future__ import annotations
from dataclasses import dataclass

from core_v2.memory_engine import MemoryRecord


@dataclass(slots=True)
class LearningReport:
    """Result produced by the learning engine."""
    samples: int
    recommendations: list[str]
class LearningEngine:
    """AI_BRIDGE V2 learning engine."""
    def analyse(self, sample_count: int) -> LearningReport:
        """Analyse available samples."""
        recommendations: list[str] = []
        if sample_count == 0:
            recommendations.append("No historical data available.")
        elif sample_count < 100:
            recommendations.append("Collect more historical samples.")
        else:
            recommendations.append("Dataset is sufficient for future analysis.")
        return LearningReport(
            samples=sample_count,
            recommendations=recommendations,
        )

    def analyse_records(self, records: list[MemoryRecord]) -> None:
        """Analyse a list of memory records.

        Baseline behaviour: count the received records and feed that
        count through the same counting path already used by
        analyse().
        """
        self.analyse(len(records))

    def analyse_decisions(self, records: list[MemoryRecord]) -> dict[str, int]:
        """Count how many BUY, SELL and HOLD decisions appear in records."""
        counts = {"BUY": 0, "SELL": 0, "HOLD": 0}

        for record in records:
            decision = record.data["decision"]["decision"]
            counts[decision] = counts.get(decision, 0) + 1

        return counts
