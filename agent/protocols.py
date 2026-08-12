"""Narrow public-only interface implemented by development and production agents."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

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
