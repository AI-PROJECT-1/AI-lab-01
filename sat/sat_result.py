from dataclasses import dataclass
from enum import Enum

from sat.statistics import SATStatistics


class SATStatus(Enum):
    SAT = "SAT"
    UNSAT = "UNSAT"


@dataclass
class SATResult:
    """Result returned by the DPLL solver."""

    status: SATStatus
    assignment: dict[int, bool] | None
    statistics: SATStatistics

    @property
    def is_sat(self) -> bool:
        return self.status is SATStatus.SAT