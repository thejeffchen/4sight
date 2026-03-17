from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import Any


class SpreadsheetInterface(ABC):
    """Abstract interface for spreadsheet interaction."""

    @abstractmethod
    async def read_cell(self, sheet: str, cell_ref: str) -> Any:
        ...

    @abstractmethod
    async def write_cell(self, sheet: str, cell_ref: str, value: Any) -> None:
        ...

    @abstractmethod
    async def read_range(self, sheet: str, range_ref: str) -> list[list[Any]]:
        ...

    @abstractmethod
    async def get_formula(self, sheet: str, cell_ref: str) -> str | None:
        ...

    @abstractmethod
    async def set_formula(self, sheet: str, cell_ref: str, formula: str) -> None:
        ...

    @abstractmethod
    async def get_workbook_structure(self) -> dict:
        ...


def col_to_num(col: str) -> int:
    """Convert column letter(s) to 0-based number. A=0, B=1, Z=25, AA=26."""
    result = 0
    for c in col.upper():
        result = result * 26 + (ord(c) - ord("A") + 1)
    return result - 1


def num_to_col(n: int) -> str:
    """Convert 0-based number to column letter(s)."""
    result = ""
    n += 1
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        result = chr(65 + remainder) + result
    return result


def parse_cell_ref(cell_ref: str) -> tuple[str, int]:
    """Parse 'B14' into ('B', 14)."""
    match = re.match(r"([A-Za-z]+)(\d+)", cell_ref)
    if not match:
        raise ValueError(f"Invalid cell reference: {cell_ref}")
    return match.group(1).upper(), int(match.group(2))


def cell_offset(start_cell: str, row_offset: int, col_offset: int) -> str:
    """Get a cell reference offset from a starting cell."""
    col, row = parse_cell_ref(start_cell)
    new_col = num_to_col(col_to_num(col) + col_offset)
    new_row = row + row_offset
    return f"{new_col}{new_row}"
