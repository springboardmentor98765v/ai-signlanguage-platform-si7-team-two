import uuid

from sqlalchemy import Column, String
from app.database.database import Base


class Role(Base):
    """Minimal Role model used by Backend service (SQLite-compatible)."""
    __tablename__ = "roles"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    name = Column(
        String(30),
        nullable=False,
        unique=True,
    )

    def __repr__(self):
        return f"<Role id={self.id} name={self.name!r}>"
