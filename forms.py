from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length
from widgets import ButtonField

class LoginForm(FlaskForm):
    username = StringField(
        "User Name",
        validators = [
            DataRequired(message="User Name is required."),
            length(max=64, message="User Name should be input within 64 characters。"),
        ],
    )
    password = PasswordField(
        "Password",
        validators = [
            DataRequired(message="Password is required。"),
        ],
    )
    cancel = ButtonField("Cancel")
    submit = SubmitField("Login")

    def copy_from(self, user):
        self.username.data = user.username
        self.password.data = user.password

    def copy_to(self, user):
        user.username = self.username.data
        user.password = self.password.data

class AddLearnForm(FlaskForm):
    learn_field = StringField(
        "learning field",  # フィールドの追加
        validators = [
            DataRequired(message="Learning field is required."),
            length(max=64, message="Learning field should be input within 64 characters."),
        ],
    )
    learn_date = StringField(
        "learning date",
        validators = [
            DataRequired(message="Learning date is required."),
            length(max=10, message="Learning date should be input within 10 characters."),
        ],
    )
    learn_content = StringField(
        "learning content",
        validators = [
            DataRequired(message="Learning content is required."),
            length(max=256, message="Learning content should be input within 256 characters."),
        ],
    )
    cancel = ButtonField("Cancel")
    submit = SubmitField("Add Learning Log")

    def copy_from(self, learn):
        self.learn_field.data = learn.field
        self.learn_date.data = learn.date
        self.learn_content.data = learn.content

    def copy_to(self, learn):
        learn.field = self.learn_field.data
        learn.date = self.learn_date.data
        learn.content = self.learn_content.data

class SearchLearnForm(FlaskForm):
    itemname = StringField(
        "learning content",
        validators = [
            DataRequired(message="Learning content is required."),
            length(max=256, message="Learning content should be input within 256 characters."),
        ]
    )
    cancel = ButtonField("Cancel")
    submit = SubmitField("Search Learning Log")
