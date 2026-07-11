import sqlite3
from pathlib import Path

db = Path(__file__).resolve().parents[1] / 'db.sqlite3'
conn = sqlite3.connect(db)
c = conn.cursor()
cols = c.execute("PRAGMA table_info(packages_package)").fetchall()
print([r[1] for r in cols])
