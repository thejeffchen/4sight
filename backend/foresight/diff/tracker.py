from __future__ import annotations

from typing import Any, TYPE_CHECKING

from foresight.db.models import CellChange, Changeset, new_id
from foresight.diff.snapshot import CellSnapshot
from foresight.diff.changeset import create_changeset

if TYPE_CHECKING:
    from foresight.spreadsheet.interface import SpreadsheetInterface
    from sqlalchemy.ext.asyncio import AsyncSession


class DiffTracker:
    """Tracks all AI-initiated cell changes with before/after snapshots."""

    def __init__(self, spreadsheet: SpreadsheetInterface, session: AsyncSession):
        self.spreadsheet = spreadsheet
        self.session = session
        self._current_changeset: Changeset | None = None

    async def begin_changeset(self, description: str = "") -> Changeset:
        cs = create_changeset(description)
        self.session.add(cs)
        await self.session.flush()
        self._current_changeset = cs
        return cs

    async def end_changeset(self) -> Changeset | None:
        cs = self._current_changeset
        self._current_changeset = None
        if cs:
            await self.session.commit()
        return cs

    @property
    def current_changeset(self) -> Changeset | None:
        return self._current_changeset

    async def snapshot_cell(self, sheet: str, cell_ref: str) -> CellSnapshot:
        value = await self.spreadsheet.read_cell(sheet, cell_ref)
        formula = await self.spreadsheet.get_formula(sheet, cell_ref)
        return CellSnapshot(sheet=sheet, cell_ref=cell_ref, value=value, formula=formula)

    async def track_write(
        self,
        sheet: str,
        cell_ref: str,
        new_value: Any,
        new_formula: str | None = None,
    ) -> CellChange:
        if not self._current_changeset:
            await self.begin_changeset()

        # Snapshot before
        before = await self.snapshot_cell(sheet, cell_ref)

        # Execute the write
        if new_formula:
            await self.spreadsheet.set_formula(sheet, cell_ref, new_formula)
            # Re-read to get computed value
            computed = await self.spreadsheet.read_cell(sheet, cell_ref)
            actual_new_value = computed
        else:
            await self.spreadsheet.write_cell(sheet, cell_ref, new_value)
            actual_new_value = new_value

        # Record the change
        change = CellChange(
            id=new_id(),
            changeset_id=self._current_changeset.id,
            sheet=sheet,
            cell_ref=cell_ref,
            old_value=before.value,
            new_value=actual_new_value,
            old_formula=before.formula,
            new_formula=new_formula,
            status="pending",
        )
        self.session.add(change)
        self._current_changeset.changes.append(change)
        await self.session.flush()

        return change

    async def track_range_write(
        self,
        sheet: str,
        start_cell: str,
        values: list[list[Any]],
    ) -> list[CellChange]:
        from foresight.spreadsheet.interface import cell_offset

        changes = []
        for row_idx, row in enumerate(values):
            for col_idx, val in enumerate(row):
                cell_ref = cell_offset(start_cell, row_idx, col_idx)
                change = await self.track_write(sheet, cell_ref, val)
                changes.append(change)
        return changes
