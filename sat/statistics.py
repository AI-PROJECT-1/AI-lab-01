from dataclasses import dataclass


@dataclass
class SATStatistics:
    """Statistics collected during one DPLL solve."""

    decisions: int = 0
    propagations: int = 0
    backtracks: int = 0
    runtime: float = 0.0