import psycopg2

conn = psycopg2.connect(
    'postgresql://signlang_app:Up5sU_cStRChSAOoPxZWberU@localhost:5432/signlang_platform'
)
cur = conn.cursor()

# Check current columns in users table
cur.execute(
    "SELECT column_name FROM information_schema.columns WHERE table_name='users' ORDER BY ordinal_position"
)
columns = [r[0] for r in cur.fetchall()]
print("Existing users columns:", columns)

# Add missing columns if they don't exist
migrations = []
if 'is_active' not in columns:
    migrations.append("ALTER TABLE users ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT TRUE")
if 'updated_at' not in columns:
    migrations.append("ALTER TABLE users ADD COLUMN updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()")

for sql in migrations:
    print(f"Running: {sql}")
    cur.execute(sql)

conn.commit()

# Verify
cur.execute(
    "SELECT column_name FROM information_schema.columns WHERE table_name='users' ORDER BY ordinal_position"
)
print("Updated users columns:", [r[0] for r in cur.fetchall()])

conn.close()
print("Done!")
