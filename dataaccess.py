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
    query_study = """
    CREATE TABLE study (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        institution TEXT NOT NULL,
        field_of_study TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """
    query_learninglog = """
    CREATE TABLE learninglog (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        institution TEXT NOT NULL,
        field_of_study TEXT NOT NULL,
        content TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """
    query_achievement = """
    CREATE TABLE achievement (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT,
        description TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """
    query_comment = """
    CREATE TABLE comment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        commenter_name TEXT NOT NULL,
        content TEXT NOT NULL,
        comment_date TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """
    try:
        conn = get_connection(autocommit=False)
        cur = conn.cursor()
        cur.execute("BEGIN")
        cur.execute(query_user)
        cur.execute(query_study)
        cur.execute(query_learninglog)
        cur.execute(query_achievement)
        cur.execute(query_comment)
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

def add_study(study):
    query = """
    INSERT INTO study (user_id, institution, field_of_study, start_date, end_date)
    VALUES (?, ?, ?, ?, ?) RETURNING id
    """
    try:
        conn = get_connection(autocommit=False)
        cur = conn.cursor()
        cur.execute("BEGIN")
        cur.execute(query, (
            study.user_id,
            study.institution,
            study.field_of_study,
            study.start_date,
            study.end_date
        ))
        study.id = cur.fetchone()[0]
        conn.commit()
        return study
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

def get_studies_by_user(user_id):
    query = """
    SELECT * FROM study WHERE user_id = ?
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id,))
        rows = cur.fetchall()
        studies = []
        for row in rows:
            study = Study()
            study.id = row[0]
            study.user_id = row[1]
            study.institution = row[2]
            study.field_of_study = row[3]
            study.start_date = row[4]
            study.end_date = row[5]
            studies.append(study)
        return studies
    except Exception as e:
        print(e.args)
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def add_learninglog(log):
    query = """
    INSERT INTO learninglog (user_id, institution, field_of_study, content, date)
    VALUES (?, ?, ?, ?, ?) RETURNING id
    """
    try:
        conn = get_connection(autocommit=False)
        cur = conn.cursor()
        cur.execute("BEGIN")
        cur.execute(query, (
            log.user_id,
            log.institution,
            log.field_of_study,
            log.content,
            log.date
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

def get_learninglogs_by_user(user_id):
    query = """
    SELECT * FROM learninglog WHERE user_id = ?
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id,))
        rows = cur.fetchall()
        logs = []
        for row in rows:
            log = Learninglog()
            log.id = row[0]
            log.user_id = row[1]
            log.institution = row[2]
            log.field_of_study = row[3]
            log.content = row[4]
            log.date = row[5]
            logs.append(log)
        return logs
    except Exception as e:
        print(e.args)
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def add_achievement(achievement):
    query = """
    INSERT INTO achievement (user_id, content, start_date, end_date, description)
    VALUES (?, ?, ?, ?, ?) RETURNING id
    """
    try:
        conn = get_connection(autocommit=False)
        cur = conn.cursor()
        cur.execute("BEGIN")
        cur.execute(query, (
            achievement.user_id,
            achievement.content,
            achievement.start_date,
            achievement.end_date,
            achievement.description
        ))
        achievement.id = cur.fetchone()[0]
        conn.commit()
        return achievement
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

def get_achievements_by_user(user_id):
    query = """
    SELECT * FROM achievement WHERE user_id = ?
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id,))
        rows = cur.fetchall()
        achievements = []
        for row in rows:
            achievement = Achievement()
            achievement.id = row[0]
            achievement.user_id = row[1]
            achievement.content = row[2]
            achievement.start_date = row[3]
            achievement.end_date = row[4]
            achievement.description = row[5]
            achievements.append(achievement)
        return achievements
    except Exception as e:
        print(e.args)
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def add_comment(comment):
    query = """
    INSERT INTO comment (user_id, commenter_name, content, comment_date)
    VALUES (?, ?, ?, ?) RETURNING id
    """
    try:
        conn = get_connection(autocommit=False)
        cur = conn.cursor()
        cur.execute("BEGIN")
        cur.execute(query, (
            comment.user_id,
            comment.commenter_name,
            comment.content,
            comment.comment_date
        ))
        comment.id = cur.fetchone()[0]
        conn.commit()
        return comment
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

def get_comments_by_user(user_id):
    query = """
    SELECT * FROM comment WHERE user_id = ?
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id,))
        rows = cur.fetchall()
        comments = []
        for row in rows:
            comment = Comment()
            comment.id = row[0]
            comment.user_id = row[1]
            comment.commenter_name = row[2]
            comment.content = row[3]
            comment.comment_date = row[4]
            comments.append(comment)
        return comments
    except Exception as e:
        print(e.args)
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # データベースの作成
    create_db()
    # ユーザーの追加
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

    # 学習履歴の追加
    study = Study()
    study.user_id = auth_user.id
    study.institution = "XYZ大学"
    study.field_of_study = "コンピュータサイエンス"
    study.start_date = "2020-04-01"
    study.end_date = "2024-03-31"
    add_study(study)

    # 学習ログの追加
    log = Learninglog()
    log.user_id = auth_user.id
    log.institution = "XYZ大学"
    log.field_of_study = "コンピュータサイエンス"
    log.content = "データベースの勉強をした"
    log.date = "2023-10-01"
    add_learninglog(log)

    # 実績の追加
    achievement = Achievement()
    achievement.user_id = auth_user.id
    achievement.content = "プログラミングコンテスト優勝"
    achievement.start_date = "2023-05-01"
    achievement.end_date = "2023-05-01"
    achievement.description = "全国プログラミングコンテストで優勝した"
    add_achievement(achievement)

    # コメントの追加
    comment = Comment()
    comment.user_id = auth_user.id
    comment.commenter_name = "charlie"
    comment.content = "おめでとうございます！"
    comment.comment_date = "2023-05-02"
    add_comment(comment)

    # データの取得テスト
    studies = get_studies_by_user(auth_user.id)
    print(studies)

    logs = get_learninglogs_by_user(auth_user.id)
    print(logs)

    achievements = get_achievements_by_user(auth_user.id)
    print(achievements)

    comments = get_comments_by_user(auth_user.id)
    print(comments)
