"""Narrow public-only interface implemented by development and production agents."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from agent.deduction_trace import Deduction, HintResult, UniquenessResult
from core.enums import Classification
from core.public_state import PublicKnowledgeState


@runtime_checkable
class LogicAgentProtocol(Protocol):
    def classify(
        self,
        public_state: PublicKnowledgeState,
        character_id: str,
    ) -> Classification:
        """Classify one character using only the supplied public snapshot."""


@runtime_checkable
class ProgressiveLogicAgentProtocol(LogicAgentProtocol, Protocol):
    last_trace: tuple

    def get_hint(self, public_state: PublicKnowledgeState) -> HintResult: ...

    def solve_next(self, public_state: PublicKnowledgeState) -> Deduction | None: ...

    def auto_solve(self, public_state: PublicKnowledgeState) -> tuple[Deduction, ...]: ...

    def check_uniqueness(self, complete_state: PublicKnowledgeState) -> UniquenessResult: ...

    def reset_trace(self) -> None: ...
