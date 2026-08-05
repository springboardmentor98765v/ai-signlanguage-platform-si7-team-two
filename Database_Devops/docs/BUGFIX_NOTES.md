# Milestone 3 — Bugfix Notes (Day 6)

Two issues reported by teammates while integrating against the badges/streaks/notifications work, both fixed here.

---

## Bug 1 — Alembic migration fails with `InvalidTextRepresentation`

**Reported error:**
```
psycopg2.errors.InvalidTextRepresentation:
invalid input syntax for type uuid: "gen_random_uuid()"
```
with `alembic current` at `0005_update_assessments_feedback`.

**Root cause:** the migration (and the model columns backing it) declared
```python
server_default='gen_random_uuid()'
```
as a plain Python string. SQLAlchemy/psycopg2 then tried to bind that string
as a literal UUID *value* instead of emitting it as a raw SQL default
expression — so Postgres tried (and failed) to parse the text
`"gen_random_uuid()"` as a UUID.

**Fix:**
- `Database_Devops/db/migrations/versions/0006_add_badges_streaks_notifications.py`
  — every `id` column now uses `server_default=sa.text("gen_random_uuid()")`,
  and `down_revision` is set to `0005_update_assessments_feedback` to match
  what `alembic current` actually shows on your machine.
- All ORM models (including `badge.py`, `streaks.py`, `notifications.py`, `users.py`)
  now declare `server_default=text("gen_random_uuid()")` explicitly,
  so future `alembic revision --autogenerate` runs compare against the correct
  server default and won't regenerate broken string versions.

---

## Bug 2 — `Mapper 'Mapper[User(users)]' has no property 'streak'`

**Reported error:** Notification API fails at mapper-configuration time
(before any endpoint runs), because `Streak` declares
`relationship(back_populates="streak")` pointing at `User`, but `User` never
defined a matching `streak` attribute. SQLAlchemy configures all mappers
together the first time *any* mapped class is queried — so a broken
relationship on `Streak` can surface as a failure in an unrelated API, like
Notifications, with no obvious connection at first glance.

**Fix:**
- `Database_Devops/db/models/streaks.py` & `badges.py` — declare relationships
  pointing to `User` and alias properties for `user`/`learner`.
- `Database_Devops/db/models/users.py` — added the missing relationship attributes:
  ```python
  streak: Mapped["Streak | None"] = relationship(
      back_populates="learner", uselist=False, cascade="all, delete-orphan"
  )
  badges: Mapped[list["Badge"]] = relationship(
      back_populates="learner", cascade="all, delete-orphan"
  )
  notifications: Mapped[list["Notification"]] = relationship(
      back_populates="user", cascade="all, delete-orphan"
  )
  ```

---

## Summary

Both fixes ensure clean `alembic upgrade head` execution and seamless ORM mapper initialization for all API endpoints.

---

## Bug 3 — Alembic migration fails with `value too long for type character varying(32)`

**Reported error:**
```
value too long for type character varying(32)
```
while updating `alembic_version.version_num`.

**Root cause:**
The revision ID string `0006_add_badges_streaks_notifications` was 35 characters long. Alembic's default table `alembic_version` stores version numbers in a `VARCHAR(32)` column. Inserting a 35-character revision identifier resulted in a Postgres string truncation error, causing the entire migration transaction (including creation of `badges`, `streaks`, and `notifications` tables) to roll back.

**Fix:**
- Updated `Database_Devops/db/migrations/versions/0006_add_badges_streaks_notifications.py` revision identifier to `0006_add_badges_streaks_notif` (27 characters).

---

## Bug 4 — `users` table missing `is_active` column for Bulk Activation/Deactivation

**Reported request:**
Bulk user activation/deactivation feature could not proceed without `is_active` status field on `users`.

**Fix:**
- Added `is_active` (`BOOLEAN NOT NULL DEFAULT TRUE`) to:
  - `Database_Devops/db/models/users.py` (`User` model)
  - `Database_Devops/db/schema/schema.sql`, `Database_Devops/db/schema/01-schema.sql`, and `Database_Devops/infra/init/01-schema.sql`
  - Base migration `0001_initial_base_tables.py`
  - Created new migration `Database_Devops/db/migrations/versions/0007_add_is_active_to_users.py`

