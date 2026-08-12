"""CNF encoding and canonical region resolution for public knowledge state."""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Sequence

from core.character import Character
from core.clue import Clue
from core.enums import ClueType, Status
from core.public_state import PublicKnowledgeState
from logic.region_resolver import RegionResolver

Clause = tuple[int, ...]


@dataclass(frozen=True, slots=True)
class CNFEncoding:
    clauses: tuple[Clause, ...]
    primary_variable_count: int
    auxiliary_variable_count: int

    @property
    def clause_count(self) -> int:
        return len(self.clauses)

    def report(self) -> dict[str, int]:
        return {
            "primary_variables": self.primary_variable_count,
            "auxiliary_variables": self.auxiliary_variable_count,
            "clauses": self.clause_count,
        }


@dataclass(frozen=True, slots=True)
class VariableMapper:
    """Deterministic character-to-variable mapping."""

    primary_variable_count: int
    _mapping: dict[str, int]
    _inverse: dict[int, str]

    @classmethod
    def from_characters(cls, characters: Sequence[Character]) -> "VariableMapper":
        sorted_characters = tuple(sorted(characters, key=lambda item: (item.row, item.column, item.id)))
        character_ids = [character.id for character in sorted_characters]
        if len(character_ids) != len(set(character_ids)):
            raise ValueError("character ids must be unique for variable mapping")
        mapping = {character.id: index + 1 for index, character in enumerate(sorted_characters)}
        inverse = {variable: character_id for character_id, variable in mapping.items()}
        return cls(len(sorted_characters), mapping, inverse)

    def variable_for(self, character_id: str) -> int:
        try:
            return self._mapping[character_id]
        except KeyError as exc:
            raise ValueError(f"unknown character id: {character_id}") from exc

    def character_id_for(self, variable: int) -> str:
        try:
            return self._inverse[variable]
        except KeyError as exc:
            raise ValueError(f"unknown variable: {variable}") from exc

    @property
    def variables(self) -> tuple[int, ...]:
        return tuple(range(1, self.primary_variable_count + 1))


class CNFEncoder:
    """Build propositional CNF from public clues and proved verdicts."""

    def __init__(self, public_state: PublicKnowledgeState) -> None:
        self._public_state = public_state
        self.mapper = VariableMapper.from_characters(public_state.characters)
        self.region_resolver = RegionResolver(public_state.characters)
        self._auxiliary_counter = self.mapper.primary_variable_count

    @property
    def primary_variable_count(self) -> int:
        return self.mapper.primary_variable_count

    @property
    def auxiliary_variable_count(self) -> int:
        return self._auxiliary_counter - self.mapper.primary_variable_count

    def build_kb(self) -> CNFEncoding:
        clauses: list[Clause] = []
        for revealed in self._public_state.revealed_clues:
            clauses.extend(self.encode_clue(revealed.clue))
        for verdict in self._public_state.known_verdicts:
            literal = self._literal_for_status(verdict.character_id, verdict.status)
            clauses.append((literal,))
        return CNFEncoding(tuple(clauses), self.primary_variable_count, self.auxiliary_variable_count)

    def encode_clue(self, clue: Clue) -> list[Clause]:
        if clue.type is ClueType.FACT:
            return self._encode_fact(clue)
        if clue.type is ClueType.SAME:
            return self._encode_same(clue)
        if clue.type is ClueType.DIFFERENT:
            return self._encode_different(clue)
        if clue.type is ClueType.IMPLIES:
            return self._encode_implies(clue)
        if clue.type is ClueType.EXACTLY:
            return self._encode_exactly(clue)
        if clue.type is ClueType.AT_LEAST:
            return self._encode_at_least(clue)
        if clue.type is ClueType.AT_MOST:
            return self._encode_at_most(clue)
        if clue.type is ClueType.ODD:
            return self._encode_odd(clue)
        raise ValueError(f"unsupported clue type: {clue.type!r}")

    def _encode_fact(self, clue: Clue) -> list[Clause]:
        return [(self._literal_for_status(clue.target, clue.status),)]

    def _encode_same(self, clue: Clue) -> list[Clause]:
        first, second = clue.characters
        first_var = self.mapper.variable_for(first)
        second_var = self.mapper.variable_for(second)
        return [(-first_var, second_var), (first_var, -second_var)]

    def _encode_different(self, clue: Clue) -> list[Clause]:
        first, second = clue.characters
        first_var = self.mapper.variable_for(first)
        second_var = self.mapper.variable_for(second)
        return [(first_var, second_var), (-first_var, -second_var)]

    def _encode_implies(self, clue: Clue) -> list[Clause]:
        antecedent, consequent = clue.characters
        return [(-self.mapper.variable_for(antecedent), self.mapper.variable_for(consequent))]

    def _encode_exactly(self, clue: Clue) -> list[Clause]:
        region_ids = self._resolve_counting_region(clue)
        return [*self._at_least_k(region_ids, clue.k), *self._at_most_k(region_ids, clue.k)]

    def _encode_at_least(self, clue: Clue) -> list[Clause]:
        region_ids = self._resolve_counting_region(clue)
        return self._at_least_k(region_ids, clue.k)

    def _encode_at_most(self, clue: Clue) -> list[Clause]:
        region_ids = self._resolve_counting_region(clue)
        return self._at_most_k(region_ids, clue.k)

    def _encode_odd(self, clue: Clue) -> list[Clause]:
        region_ids = self.region_resolver.resolve(clue.region)
        variables = tuple(self.mapper.variable_for(cell_id) for cell_id in region_ids)
        clauses: list[Clause] = []
        for values in itertools.product((False, True), repeat=len(variables)):
            if sum(values) % 2 == 0:
                clauses.append(
                    tuple(-variable if value else variable for variable, value in zip(variables, values, strict=True))
                )
        return clauses

    def _resolve_counting_region(self, clue: Clue) -> tuple[str, ...]:
        region_ids = self.region_resolver.resolve(clue.region)
        if clue.k > len(region_ids):
            raise ValueError(
                f"clue {clue.id} has k={clue.k} greater than region size {len(region_ids)}"
            )
        return region_ids

    def _literal_for_status(self, character_id: str, status: Status) -> int:
        variable = self.mapper.variable_for(character_id)
        return variable if status is Status.CRIMINAL else -variable

    def _at_least_k(self, region_ids: tuple[str, ...], k: int) -> list[Clause]:
        if k <= 0:
            return []
        region_size = len(region_ids)
        if k > region_size:
            raise ValueError("k is larger than the region size")
        subset_size = region_size - k + 1
        return [tuple(self.mapper.variable_for(cell_id) for cell_id in subset) for subset in itertools.combinations(region_ids, subset_size)]

    def _at_most_k(self, region_ids: tuple[str, ...], k: int) -> list[Clause]:
        region_size = len(region_ids)
        if k >= region_size:
            return []
        if k < 0:
            raise ValueError("k must be non-negative")
        subset_size = k + 1
        return [tuple(-self.mapper.variable_for(cell_id) for cell_id in subset) for subset in itertools.combinations(region_ids, subset_size)]
