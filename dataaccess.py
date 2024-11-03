import sqlite3
from models import *

# get_connection
# create_db
# auth
# add_user
# addlearn





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


# これがあっているかわからない
def add_learn(user_id, field, date, content):
    query = """
    INSERT INTO learn (user_id, field, date, content)
    VALUES (?, ?, ?, ?)
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id, field, date, content))
        conn.commit()
    except Exception as e:
        print(e.args)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def search_learn(user_id):
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
    SELECT * FROM learn WHERE user_id = ? AND field LIKE ? ORDER BY date ASC
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


def search_user_by_username(username):
    query = """
    SELECT * FROM users WHERE username = ?
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (username,))
        row = cur.fetchone()
        if row:
            user = User()
            user.id = row[0]
            user.username = row[1]
            user.password = row[2]
            # 他の必要なフィールドをセット
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


if __name__ == "__main__":
    # データベースの作成
    create_db()
    # ユーザーの一覧．追加．
    user1 = User()
    user1.username = "alice"
    user1.password = "alicepass"
    add_user(user1)

    user2 = User()
    user2.username = "bob"
    user2.password = "bobpass"
    add_user(user2)

    # 認証テスト
    auth_user = auth("alice", "alicepass")
    print(auth_user)

    # 学習ログの追加
    log = Learn()
    log.user_id = auth_user.id
    log.field = "データベース"
    log.date = "2023-10-01"
    log.content = "データベースの勉強をした"
    add_learn(log)
