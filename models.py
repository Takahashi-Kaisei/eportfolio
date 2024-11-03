class User:
    def __init__(self):
        self.id = None
        self.username = None
        self.password = None
    def __repr__(self):
        return "<User %r>" % self.username

class Learn:
    def __init__(self):
        self.id = None
        self.user_id = None
        self.field = None
        self.date = None
        self.content = None
    def __repr__(self):
        return "<Learning %r at %r>" % (self.content, self.date)
