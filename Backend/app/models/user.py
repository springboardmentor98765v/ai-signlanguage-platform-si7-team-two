import uuid

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    role_id = Column(
        String(36),
        ForeignKey("roles.id"),
        nullable=False,
    )

    full_name = Column(
        String(120),
        nullable=False,
    )

    mascot_id = Column(
        String(50),
        nullable=True,
        default="owl",
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationship to Role — needed by auth_service.login to read role.name
    role = relationship("Role", foreign_keys=[role_id])