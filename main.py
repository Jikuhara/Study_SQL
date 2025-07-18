import sqlite3

conn = sqlite3.connect("SQLtest.db")
cur = conn.cursor()

cur.execute("SELECT * FROM users")

rows = cur.fetchall()

for row in rows:
    print(f"ID: {row[0]}, 名前: {row[1]}, 年齢: {row[2]}")

conn.close()
