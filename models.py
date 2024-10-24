class User:
    def __init__(self):
        self.id = None
        self.username = None
        self.password = None
    def __repr__(self):
        return "<User %r>" % self.username

class Study:
    def __init__(self):
        self.id = None
        self.user_id = None
        self.institution = None
        self.field_of_study = None  # 専攻
        self.start_date = None  # 開始日
        self.end_date = None  # 終了日
    def __repr__(self):
        return "< The user studied %r at %r>" % (self.field_of_study, self.institution)

class Learninglog:
    def __init__(self):
        self.id = None
        self.user_id = None
        self.institution = None  # 学校名または教育機関名
        self.field_of_study = None  # 専攻
        self.content = None
        self.date = None
    def __repr__(self):
        return "<Learning %r at %r>" % (self.content, self.date)

class Achievement:
    def __init__(self):
        self.id = None
        self.user_id = None
        self.content = None
        self.start_date = None  # 開始日
        self.end_date = None  # 終了日
        self.description = None  # 詳細説明
    def __repr__(self):
        return "<Achievement: %r>" % self.content

class Comment:
    def __init__(self):
        self.id = None
        self.user_id = None
        self.commnter_name = None
        self.content = None
        self.comment_date = None
    def __repr__(self):
        return "<Comment %r>" % self.id
