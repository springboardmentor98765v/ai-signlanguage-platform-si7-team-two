"""Day 3: initial base tables (roles, users, courses, lessons)

This migration formalizes, as versioned Alembic history, exactly the DDL
for the 4 tables in Day 3's scope (SRS §6, Intern 5, Day 3) — the same DDL
already reviewed in db/schema/schema.sql. It intentionally does NOT include
practice_sessions / assessments / feedback / learner_analytics — those are
Day 4 scope and will arrive in a later migration.

Revision ID: 0001_initial_base_tables
Revises:
Create Date: Day 3

IMPORTANT — running this against your Day 2 database:
Day 2 already created ALL 8 tables (including these 4) via Docker's
one-time init-script bootstrap (infra/init/01-schema.sql), not via Alembic.
So on your existing Day 2 database, do NOT run `alembic upgrade head`
(it will fail with "relation already exists"). Instead run:

    alembic stamp head

This tells Alembic "the database already matches this revision" without
re-running the DDL. From this point forward, any NEW schema change should
be made as a new Alembic migration, not by hand-editing schema.sql.

Only run `alembic upgrade head` for real on a genuinely fresh, empty
database (e.g. a new teammate's local Postgres with no init-script
bootstrap, or a CI test database).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0001_initial_base_tables"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')

    op.create_table(
        "roles",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("name", sa.String(30), nullable=False),
        sa.UniqueConstraint("name", name="uq_roles_name"),
    )

    op.create_table(
        "users",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("role_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("full_name", sa.String(120), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(
            ["role_id"], ["roles.id"], name="fk_users_role_id_roles", ondelete="RESTRICT"
        ),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("idx_users_role_id", "users", ["role_id"])

    op.create_table(
        "courses",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("level", sa.String(20), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.CheckConstraint(
            "level IN ('Beginner', 'Intermediate', 'Advanced')",
            name="level_valid_values",
        ),
    )

    op.create_table(
        "lessons",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("letter", sa.String(2), nullable=False),
        sa.Column("title", sa.String(120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("reference_image_url", sa.String(500), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(
            ["course_id"], ["courses.id"], name="fk_lessons_course_id_courses", ondelete="CASCADE"
        ),
    )
    op.create_index("idx_lessons_course_id", "lessons", ["course_id"])


def downgrade() -> None:
    op.drop_index("idx_lessons_course_id", table_name="lessons")
    op.drop_table("lessons")
    op.drop_table("courses")
    op.drop_index("idx_users_role_id", table_name="users")
    op.drop_table("users")
    op.drop_table("roles")
