from __future__ import annotations

import asyncio
from typing import Any

from foresight.spreadsheet.interface import SpreadsheetInterface


class ExcelInterface(SpreadsheetInterface):
    """Excel via xlwings (macOS and Windows)."""

    def __init__(self):
        self._app = None
        self._book = None

    async def connect(self, workbook_name: str | None = None):
        """Connect to an open Excel workbook."""
        import xlwings as xw

        def _connect():
            self._app = xw.apps.active
            if not self._app:
                raise ConnectionError("No Excel instance found. Please open Excel first.")
            if workbook_name:
                self._book = self._app.books[workbook_name]
            else:
                self._book = self._app.books.active
            if not self._book:
                raise ConnectionError("No workbook is open in Excel.")

        await asyncio.to_thread(_connect)

    def _get_sheet(self, sheet: str):
        if not self._book:
            raise ConnectionError("Not connected to a workbook.")
        return self._book.sheets[sheet]

    async def read_cell(self, sheet: str, cell_ref: str) -> Any:
        def _read():
            s = self._get_sheet(sheet)
            return s.range(cell_ref).value
        return await asyncio.to_thread(_read)

    async def write_cell(self, sheet: str, cell_ref: str, value: Any) -> None:
        def _write():
            s = self._get_sheet(sheet)
            s.range(cell_ref).value = value
        await asyncio.to_thread(_write)

    async def read_range(self, sheet: str, range_ref: str) -> list[list[Any]]:
        def _read():
            s = self._get_sheet(sheet)
            data = s.range(range_ref).value
            if data is None:
                return [[]]
            if not isinstance(data, list):
                return [[data]]
            if data and not isinstance(data[0], list):
                return [data]
            return data
        return await asyncio.to_thread(_read)

    async def get_formula(self, sheet: str, cell_ref: str) -> str | None:
        def _get():
            s = self._get_sheet(sheet)
            formula = s.range(cell_ref).formula
            if formula and str(formula).startswith("="):
                return str(formula)
            return None
        return await asyncio.to_thread(_get)

    async def set_formula(self, sheet: str, cell_ref: str, formula: str) -> None:
        def _set():
            s = self._get_sheet(sheet)
            s.range(cell_ref).formula = formula
        await asyncio.to_thread(_set)

    async def get_workbook_structure(self) -> dict:
        def _get():
            if not self._book:
                raise ConnectionError("Not connected to a workbook.")
            sheets = []
            for s in self._book.sheets:
                used = s.used_range
                sheets.append({
                    "name": s.name,
                    "rows": used.last_cell.row if used else 0,
                    "cols": used.last_cell.column if used else 0,
                })
            return {
                "workbook": self._book.name,
                "sheets": sheets,
            }
        return await asyncio.to_thread(_get)
