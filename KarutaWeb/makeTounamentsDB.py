import sqlite3

conn = sqlite3.connect('SQLtest.db')
cur = conn.cursor()

# 大会テーブルの作成
cur.execute('''
CREATE TABLE IF NOT EXISTS tournaments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL,
    location TEXT NOT NULL,
    max_participants INTEGER,
    registration_deadline TEXT,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users (id)
)
''')

conn.commit()
conn.close()

print("Tournaments table created successfully!")