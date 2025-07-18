import sqlite3

conn = sqlite3.connect('SQLtest.db')
cur = conn.cursor()

# テーブルに level カラムを追加
try:
    cur.execute("ALTER TABLE tournaments ADD COLUMN level TEXT")
    conn.commit()
    print("Level column added successfully!")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("Level column already exists.")
    else:
        print(f"Error: {e}")
finally:
    conn.close()