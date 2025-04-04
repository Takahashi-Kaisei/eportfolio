import sqlite3
from models import *

def get_connection(autocommit=True):
    if autocommit:
        return sqlite3.connect("education.db")
    else:
        return sqlite3.connect("education.db", isolation_level=None)

def create_db():
    query_user = """
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """

    query_learn = """
    CREATE TABLE learn (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        field TEXT NOT NULL,
        date TEXT NOT NULL,
        content TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """

    try:
        conn = get_connection(autocommit=False)
        cur = conn.cursor()
        cur.execute("BEGIN")
        cur.execute(query_user)
        cur.execute(query_learn)
        conn.commit()
    except Exception as e:
        print(e.args)
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def auth(username, password):
    query = """
    SELECT * FROM users WHERE username = ? AND password = ?
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (username, password,))
        res = cur.fetchone()
        if res:
            user = User()
            user.id = res[0]
            user.username = res[1]
            user.password = res[2]
            return user
        else:
            return None
    except Exception as e:
        print(e.args)
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def add_user(user):
    query = """
    INSERT INTO users (username, password) VALUES (?, ?) RETURNING id
    """
    try:
        conn = get_connection(autocommit=False)
        cur = conn.cursor()
        cur.execute("BEGIN")
        cur.execute(query, (user.username, user.password,))
        user.id = cur.fetchone()[0]
        conn.commit()
        return user
    except Exception as e:
        print(e.args)
        if conn:
            conn.rollback()
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def addlearn(log):
    query = """
    INSERT INTO learn (user_id, field, date, content)
    VALUES (?, ?, ?, ?) RETURNING id
    """
    try:
        conn = get_connection(autocommit=False)
        cur = conn.cursor()
        cur.execute("BEGIN")
        cur.execute(query, (
            log.user_id,
            log.field,
            log.date,
            log.content,
        ))
        log.id = cur.fetchone()[0]
        conn.commit()
        return log
    except Exception as e:
        print(e.args)
        if conn:
            conn.rollback()
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def search_user_by_username(username):
    query = """
    SELECT * FROM users WHERE username = ?
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (username,))
        res = cur.fetchone()
        if res:
            user = User()
            user.id = res[0]
            user.username = res[1]
            user.password = res[2]
            return user
        else:
            return None
    except Exception as e:
        print(e.args)
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def search_learns_by_user(user_id):
    query = """
    SELECT * FROM learn WHERE user_id = ?
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id,))
        res = cur.fetchall()
        learn_list = []
        for r in res:
            learn = Learn()
            learn.id = r[0]
            learn.user_id = r[1]
            learn.field = r[2]
            learn.date = r[3]
            learn.content = r[4]
            learn_list.append(learn)
        return learn_list
    except Exception as e:
        print(e.args)
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def search_learn_by_field(user_id, field):
    query = """
    SELECT * FROM learn WHERE user_id = ? AND field LIKE ?
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id, f"%{field}%"))
        res = cur.fetchall()
        learn_list = []
        for r in res:
            learn = Learn()
            learn.id = r[0]
            learn.user_id = r[1]
            learn.field = r[2]
            learn.date = r[3]
            learn.content = r[4]
            learn_list.append(learn)
        return learn_list
    except Exception as e:
        print(e.args)
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    create_db()

    user1 = User()
    user1.username = "alice"
    user1.password = "alicepass"
    add_user(user1)

    user2 = User()
    user2.username = "bob"
    user2.password = "bobpass"
    add_user(user2)

    auth_user = auth("alice", "alicepass")
    print(auth_user)

    log = Learn()
    log.user_id = auth_user.id
    log.field = "データベース"
    log.date = "2023-10-01"
    log.content = "データベースの勉強をした"
    addlearn(log)
