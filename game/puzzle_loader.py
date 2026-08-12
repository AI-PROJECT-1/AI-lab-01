"""Strict JSON-to-domain loader for Griductive puzzles."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.character import Character, parse_cell_id
from core.clue import Clue
from core.enums import ClueType, RegionType, Status
from core.puzzle import Puzzle, PuzzleCard
from core.region import Region


class PuzzleFormatError(ValueError):
    """Raised when puzzle input is malformed or violates domain contracts."""


class PuzzleLoader:
    @classmethod
    def load(cls, path: str | Path) -> Puzzle:
        source = Path(path)
        try:
            with source.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except OSError as exc:
            raise PuzzleFormatError(f"cannot read puzzle {source}: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise PuzzleFormatError(
                f"invalid JSON in {source} at line {exc.lineno}, column {exc.colno}"
            ) from exc
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: Any) -> Puzzle:
        try:
            root = cls._object(data, "puzzle")
            cls._keys(root, {"id", "title", "size", "cards"}, set(), "puzzle")
            raw_cards = root["cards"]
            if not isinstance(raw_cards, list):
                raise ValueError("puzzle.cards must be an array")
            cards = tuple(cls._parse_card(item, index) for index, item in enumerate(raw_cards))
            return Puzzle(
                id=cls._text(root["id"], "puzzle.id"),
                title=cls._text(root["title"], "puzzle.title"),
                size=cls._integer(root["size"], "puzzle.size"),
                cards=cards,
            )
        except (KeyError, TypeError, ValueError) as exc:
            if isinstance(exc, PuzzleFormatError):
                raise
            raise PuzzleFormatError(str(exc)) from exc

    @classmethod
    def _parse_card(cls, data: Any, index: int) -> PuzzleCard:
        context = f"puzzle.cards[{index}]"
        card = cls._object(data, context)
        cls._keys(
            card,
            {"cell", "name", "profession", "status", "initially_revealed", "clue"},
            set(),
            context,
        )
        cell = cls._text(card["cell"], f"{context}.cell")
        row, column = parse_cell_id(cell)
        initially_revealed = card["initially_revealed"]
        if not isinstance(initially_revealed, bool):
            raise ValueError(f"{context}.initially_revealed must be boolean")
        return PuzzleCard(
            character=Character(
                id=cell,
                name=cls._text(card["name"], f"{context}.name"),
                profession=cls._text(card["profession"], f"{context}.profession"),
                row=row,
                column=column,
            ),
            hidden_status=cls._enum(Status, card["status"], f"{context}.status"),
            clue=cls._parse_clue(card["clue"], f"{context}.clue"),
            initially_revealed=initially_revealed,
        )

    @classmethod
    def _parse_clue(cls, data: Any, context: str) -> Clue:
        clue = cls._object(data, context)
        clue_type = cls._enum(ClueType, clue.get("type"), f"{context}.type")
        optional = {"text"}
        common = {"id", "type"}
        kwargs: dict[str, Any] = {
            "id": cls._text(clue.get("id"), f"{context}.id"),
            "type": clue_type,
        }
        if "text" in clue:
            kwargs["text"] = cls._text(clue["text"], f"{context}.text")

        if clue_type is ClueType.FACT:
            cls._keys(clue, common | {"target", "status"}, optional, context)
            kwargs["target"] = cls._text(clue["target"], f"{context}.target")
            kwargs["status"] = cls._enum(Status, clue["status"], f"{context}.status")
        elif clue_type in (ClueType.SAME, ClueType.DIFFERENT, ClueType.IMPLIES):
            cls._keys(clue, common | {"characters"}, optional, context)
            characters = clue["characters"]
            if not isinstance(characters, list):
                raise ValueError(f"{context}.characters must be an array")
            kwargs["characters"] = tuple(
                cls._text(item, f"{context}.characters[{index}]")
                for index, item in enumerate(characters)
            )
        elif clue_type in (ClueType.EXACTLY, ClueType.AT_LEAST, ClueType.AT_MOST):
            cls._keys(clue, common | {"region", "k"}, optional, context)
            kwargs["region"] = cls._parse_region(clue["region"], f"{context}.region")
            kwargs["k"] = cls._integer(clue["k"], f"{context}.k")
        else:
            cls._keys(clue, common | {"region"}, optional, context)
            kwargs["region"] = cls._parse_region(clue["region"], f"{context}.region")
        return Clue(**kwargs)

    @classmethod
    def _parse_region(cls, data: Any, context: str) -> Region:
        region = cls._object(data, context)
        kind = cls._enum(RegionType, region.get("type"), f"{context}.type")
        if kind in (RegionType.ROW, RegionType.COLUMN):
            cls._keys(region, {"type", "index"}, set(), context)
            return Region(kind, index=cls._integer(region["index"], f"{context}.index"))
        if kind is RegionType.NEIGHBORS:
            cls._keys(region, {"type", "center"}, set(), context)
            return Region(kind, center=cls._text(region["center"], f"{context}.center"))
        cls._keys(region, {"type", "cells"}, set(), context)
        cells = region["cells"]
        if not isinstance(cells, list):
            raise ValueError(f"{context}.cells must be an array")
        return Region(
            kind,
            cells=tuple(cls._text(item, f"{context}.cells[{index}]") for index, item in enumerate(cells)),
        )

    @staticmethod
    def _object(value: Any, context: str) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise ValueError(f"{context} must be an object")
        return value

    @staticmethod
    def _keys(
        value: dict[str, Any], required: set[str], optional: set[str], context: str
    ) -> None:
        missing = required - value.keys()
        unknown = value.keys() - required - optional
        if missing:
            raise ValueError(f"{context} is missing fields: {sorted(missing)}")
        if unknown:
            raise ValueError(f"{context} has unknown fields: {sorted(unknown)}")

    @staticmethod
    def _text(value: Any, context: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{context} must be a non-empty string")
        return value

    @staticmethod
    def _integer(value: Any, context: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{context} must be an integer")
        return value

    @staticmethod
    def _enum(enum_type: type, value: Any, context: str):
        try:
            return enum_type(value)
        except (TypeError, ValueError) as exc:
            allowed = ", ".join(item.value for item in enum_type)
            raise ValueError(f"{context} must be one of: {allowed}") from exc
