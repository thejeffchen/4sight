from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select

from foresight.db.models import CellChange, Changeset

if TYPE_CHECKING:
    from foresight.spreadsheet.interface import SpreadsheetInterface
    from sqlalchemy.ext.asyncio import AsyncSession


async def reject_cell_change(
    change: CellChange,
    spreadsheet: SpreadsheetInterface,
    session: AsyncSession,
) -> None:
    """Revert a single cell to its previous value."""
    if change.old_formula:
        await spreadsheet.set_formula(change.sheet, change.cell_ref, change.old_formula)
    else:
        await spreadsheet.write_cell(
            change.sheet, change.cell_ref, change.old_value
        )
    change.status = "denied"
    await session.flush()


async def accept_cell_change(
    change: CellChange,
    session: AsyncSession,
) -> None:
    """Mark a cell change as accepted (value already in spreadsheet)."""
    change.status = "accepted"
    await session.flush()


async def reject_changeset(
    changeset: Changeset,
    spreadsheet: SpreadsheetInterface,
    session: AsyncSession,
) -> None:
    """Revert all pending changes in a changeset."""
    for change in reversed(changeset.changes):
        if change.status == "pending":
            await reject_cell_change(change, spreadsheet, session)
    changeset.status = "denied"
    await session.commit()


async def accept_changeset(
    changeset: Changeset,
    session: AsyncSession,
) -> None:
    """Accept all pending changes in a changeset."""
    for change in changeset.changes:
        if change.status == "pending":
            change.status = "accepted"
    changeset.status = "accepted"
    await session.commit()


def _update_changeset_status(changeset: Changeset) -> None:
    """Recalculate changeset status based on individual change statuses."""
    statuses = {c.status for c in changeset.changes}
    if statuses == {"accepted"}:
        changeset.status = "accepted"
    elif statuses == {"denied"}:
        changeset.status = "denied"
    elif "pending" not in statuses:
        changeset.status = "partial"
