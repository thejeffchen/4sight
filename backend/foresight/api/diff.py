from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from foresight.db.models import CellChange, Changeset
from foresight.db.session import get_session
from foresight.diff.changeset import changeset_to_dict, cell_change_to_dict
from foresight.diff.rollback import (
    accept_cell_change,
    reject_cell_change,
    accept_changeset,
    reject_changeset,
)
from foresight.api.chat import get_spreadsheet

router = APIRouter(prefix="/api/diff")


@router.get("/changesets")
async def list_changesets(session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Changeset)
        .options(selectinload(Changeset.changes))
        .order_by(Changeset.created_at.desc())
    )
    changesets = result.scalars().all()
    return [changeset_to_dict(cs) for cs in changesets]


@router.get("/changesets/{changeset_id}")
async def get_changeset(changeset_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Changeset)
        .options(selectinload(Changeset.changes))
        .where(Changeset.id == changeset_id)
    )
    cs = result.scalar_one_or_none()
    if not cs:
        return {"error": "Changeset not found"}, 404
    return changeset_to_dict(cs)


@router.post("/changes/{change_id}/accept")
async def accept_change(change_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(CellChange).where(CellChange.id == change_id))
    change = result.scalar_one_or_none()
    if not change:
        return {"error": "Change not found"}, 404
    await accept_cell_change(change, session)
    await session.commit()
    return {"status": "accepted"}


@router.post("/changes/{change_id}/reject")
async def reject_change(change_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(CellChange).where(CellChange.id == change_id))
    change = result.scalar_one_or_none()
    if not change:
        return {"error": "Change not found"}, 404
    spreadsheet = await get_spreadsheet()
    await reject_cell_change(change, spreadsheet, session)
    await session.commit()
    return {"status": "rejected"}


@router.post("/changesets/{changeset_id}/accept")
async def accept_all(changeset_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Changeset)
        .options(selectinload(Changeset.changes))
        .where(Changeset.id == changeset_id)
    )
    cs = result.scalar_one_or_none()
    if not cs:
        return {"error": "Changeset not found"}, 404
    await accept_changeset(cs, session)
    return {"status": "accepted"}


@router.post("/changesets/{changeset_id}/reject")
async def reject_all(changeset_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Changeset)
        .options(selectinload(Changeset.changes))
        .where(Changeset.id == changeset_id)
    )
    cs = result.scalar_one_or_none()
    if not cs:
        return {"error": "Changeset not found"}, 404
    spreadsheet = await get_spreadsheet()
    await reject_changeset(cs, spreadsheet, session)
    return {"status": "rejected"}
