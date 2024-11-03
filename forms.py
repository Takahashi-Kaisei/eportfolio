from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, DateField, SubmitField,  TextAreaField
from wtforms.validators import DataRequired, length
from widgets import ButtonField

class LoginForm(FlaskForm):
    username = StringField(
        "User Name",
        validators = [
            DataRequired(message="User Name is required."),
            length(max=64, message="User Name should be input within 64 characters."),
            ],
        )
    password = PasswordField(
        "Password",
        validators = [
            DataRequired(message="Password is required."),
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
        "Learning Field",
        validators = [
            DataRequired(message="Learning field is required."),
            length(max=64, message="Learning field should be input within 64 characters."),
        ],
    )
    learn_date = DateField(
        "Learning Date",
        validators = [
            DataRequired(message="Learning date is required."),
        ],
        format='%Y-%m-%d'
    )
    learn_content = TextAreaField(
        "Learning Content",
        validators = [
            DataRequired(message="Learning content is required."),
            length(max=256, message="Learning content should be input within 256 characters."),
        ],
    )
    cancel = ButtonField("Cancel")
    submit = SubmitField("Add Learning Log")

class SearchLearnForm(FlaskForm):
    itemname = StringField(
        "learning content",
        validators = [
            DataRequired(message="Learning content is required."),
            length(max=256, message="Learning content should be input within 256 characters."),
        ],
    )
    cancel = ButtonField("Cancel")
    submit = SubmitField("Search Learning Log")
