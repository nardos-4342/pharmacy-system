import sqlite3

conn=sqlite3.connect("pharmacy.db")
for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    print(row)
for col in conn.execute("PRAGMA table_info(batches)"):
    print(col)
conn.execute("INSERT INTO products (name, price) VALUES (?, ?)", ("Paracetamol", 12.5))
