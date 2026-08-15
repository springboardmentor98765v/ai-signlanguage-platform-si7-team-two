import sqlite3
import uuid

conn = sqlite3.connect('Backend/signlang.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS roles (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    role_id TEXT NOT NULL REFERENCES roles(id),
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)
''')

learner_id = str(uuid.uuid4())
c.execute("INSERT OR IGNORE INTO roles (id, name) VALUES (?, ?)", (learner_id, 'Learner'))
c.execute("INSERT OR IGNORE INTO roles (id, name) VALUES (?, ?)", (str(uuid.uuid4()), 'Teacher'))
c.execute("INSERT OR IGNORE INTO roles (id, name) VALUES (?, ?)", (str(uuid.uuid4()), 'Admin'))

conn.commit()
conn.close()
print("SQLite DB initialized")
