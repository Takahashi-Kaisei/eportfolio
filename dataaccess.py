import sqlite3

con = sqlite3.connect("eportfolio.db")
cur = con.cursor()
cur.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
                )
""")
con.close()
