from foresight.db.models import Changeset, CellChange, new_id


def create_changeset(description: str = "") -> Changeset:
    return Changeset(id=new_id(), description=description)


def changeset_to_dict(cs: Changeset) -> dict:
    return {
        "id": cs.id,
        "description": cs.description,
        "status": cs.status,
        "created_at": cs.created_at.isoformat() if cs.created_at else None,
        "changes": [cell_change_to_dict(c) for c in cs.changes],
    }


def cell_change_to_dict(cc: CellChange) -> dict:
    return {
        "id": cc.id,
        "changeset_id": cc.changeset_id,
        "sheet": cc.sheet,
        "cell_ref": cc.cell_ref,
        "old_value": cc.old_value,
        "new_value": cc.new_value,
        "old_formula": cc.old_formula,
        "new_formula": cc.new_formula,
        "status": cc.status,
    }
