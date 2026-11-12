import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent.parent / "logs" / "database.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
try:
    cursor.execute("ALTER TABLE users ADD COLUMN contact TEXT")
    conn.commit()
    print("Column 'contact' added.")
except Exception as e:
    print(e)
finally:
    conn.close()
