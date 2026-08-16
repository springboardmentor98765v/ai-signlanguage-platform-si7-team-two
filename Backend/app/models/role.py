import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name = Column(
        String(30),
        nullable=False,
        unique=True,
    )

    def __repr__(self):
        return f"<Role id={self.id} name={self.name!r}>"