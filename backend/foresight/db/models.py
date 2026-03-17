import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


def new_id() -> str:
    return str(uuid.uuid4())


class Changeset(Base):
    __tablename__ = "changesets"

    id = Column(String, primary_key=True, default=new_id)
    description = Column(Text, default="")
    status = Column(String, default="pending")  # pending | partial | accepted | denied
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    changes = relationship("CellChange", back_populates="changeset", order_by="CellChange.created_at")


class CellChange(Base):
    __tablename__ = "cell_changes"

    id = Column(String, primary_key=True, default=new_id)
    changeset_id = Column(String, ForeignKey("changesets.id"), nullable=False)
    sheet = Column(String, nullable=False)
    cell_ref = Column(String, nullable=False)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    old_formula = Column(Text, nullable=True)
    new_formula = Column(Text, nullable=True)
    status = Column(String, default="pending")  # pending | accepted | denied | reverted
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    changeset = relationship("Changeset", back_populates="changes")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True, default=new_id)
    role = Column(String, nullable=False)  # user | assistant
    content = Column(Text, nullable=False)
    changeset_id = Column(String, ForeignKey("changesets.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
